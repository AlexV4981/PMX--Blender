#!/usr/bin/env python3
"""Bounded NVIDIA Cycles smoke qualification; never saves preferences or a blend.

Run with normal Python and the exact trusted Blender executable. The worker
runs inside a separate factory-startup Blender process on a synthetic scene.
A successful render with GPU-only configuration but no process-specific
utilization witness is explicitly unverified, not incompatible.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import threading
import time

BACKENDS = ("OPTIX", "CUDA")
SIZE = 512
SAMPLES = 128


def save_json(path, value):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")


def digest(path):
    with Path(path).open("rb") as stream:
        h = hashlib.sha256()
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
        return h.hexdigest()


def parse_pmon(text, pid):
    """Only positive SM activity for the launched compute process counts."""
    matches = []
    for line in text.splitlines():
        parts = line.split()
        if len(parts) < 5 or line.lstrip().startswith("#"):
            continue
        try:
            gpu, process, sm = int(parts[0]), int(parts[1]), int(parts[3])
        except ValueError:
            continue
        if process == pid and "C" in parts[2] and 0 < sm <= 100:
            matches.append({"gpu_index": gpu, "pid": process, "sm_percent": sm})
    return matches


def configure_gpu(prefs, backend, device_id=None):
    prefs.compute_device_type = backend
    prefs.refresh_devices()
    devices = list(prefs.devices)
    candidates = [d for d in devices if d.type == backend
                  and (device_id is None or d.id == device_id)]
    selected = candidates[0] if len(candidates) == 1 else None
    for d in devices:
        d.use = d is selected
    inventory = [{"name": d.name, "type": d.type, "id": d.id,
                  "enabled": bool(d.use)} for d in devices]
    if not candidates:
        return "no_matching_gpu", inventory
    if selected is None:
        return "device_selection_required", inventory
    if (prefs.compute_device_type != backend
            or sum(bool(d.use) for d in devices) != 1 or not selected.use):
        raise RuntimeError("GPU-only selection did not persist")
    return "gpu_configured", inventory


def valid_png(path):
    path = Path(path)
    if not path.is_file() or path.stat().st_size < 45:
        return False
    with path.open("rb") as stream:
        head = stream.read(24)
        stream.seek(-12, 2)
        tail = stream.read(12)
    return (head[:8] == b"\x89PNG\r\n\x1a\n" and head[12:16] == b"IHDR"
            and int.from_bytes(head[16:20], "big") == SIZE
            and int.from_bytes(head[20:24], "big") == SIZE
            and tail == b"\x00\x00\x00\x00IEND\xaeB\x60\x82")


def worker(backend, directory, device_id=None):
    import bpy
    directory = Path(directory)
    result = {"backend": backend, "pid": os.getpid(),
              "blender_version": bpy.app.version_string,
              "build_hash": bpy.app.build_hash.decode(errors="replace"),
              "status": "configuration_failed", "devices": []}
    try:
        if not bpy.app.background or bpy.data.filepath:
            raise RuntimeError("Use an empty factory-startup background process")
        scene = bpy.context.scene
        scene.render.engine = "CYCLES"
        prefs = bpy.context.preferences.addons["cycles"].preferences
        try:
            state, inventory = configure_gpu(prefs, backend, device_id)
        except (TypeError, ValueError) as exc:
            result.update(status="backend_configuration_unavailable", error=str(exc))
            return
        result.update(status=state, devices=inventory)
        if state != "gpu_configured":
            return
        result["status"] = "configuration_failed"
        scene.cycles.device = "GPU"
        if scene.cycles.device != "GPU" or scene.camera is None:
            raise RuntimeError("GPU scene or factory camera not available")
        scene.render.resolution_x = scene.render.resolution_y = SIZE
        scene.render.resolution_percentage = 100
        scene.cycles.samples = SAMPLES
        scene.cycles.use_adaptive_sampling = False
        scene.cycles.use_denoising = False
        scene.render.image_settings.file_format = "PNG"
        scene.render.filepath = str(directory / "fixture.png")
        result.update(status="render_failed", render_start=time.time())
        try:
            outcome = bpy.ops.render.render(write_still=True)
        finally:
            result["render_end"] = time.time()
        if "FINISHED" not in outcome or not valid_png(directory / "fixture.png"):
            raise RuntimeError("No completed fixture PNG")
        result.update(status="gpu_render_completed",
                      image_sha256=digest(directory / "fixture.png"))
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    finally:
        save_json(directory / "worker.json", result)


def monitor(pid, executable, done, records):
    if not executable:
        return
    while not done.is_set():
        start = time.time()
        try:
            r = subprocess.run([executable, "pmon", "-s", "u", "-c", "1"],
                               capture_output=True, text=True, timeout=5, check=False)
            records.append({"start": start, "end": time.time(), "exit_code": r.returncode,
                            "matches": parse_pmon(r.stdout, pid),
                            "error": r.stderr[-1000:] if r.returncode else None})
            if r.returncode:
                return
        except (OSError, subprocess.TimeoutExpired) as exc:
            records.append({"start": start, "end": time.time(), "error": str(exc)})
            return
        done.wait(0.15)


def classify(result, returncode, timed_out, samples, image_valid, pid):
    if timed_out:
        return "probe_timeout"
    if returncode != 0 or not result or result.get("pid") != pid:
        return "probe_process_failed"
    state = result.get("status", "probe_process_failed")
    if state != "gpu_render_completed":
        return state
    enabled = [d for d in result.get("devices", []) if d.get("enabled")]
    if (not image_valid or len(enabled) != 1
            or enabled[0].get("type") != result.get("backend")
            or result.get("backend") not in BACKENDS):
        return "render_evidence_invalid"
    start, end = result.get("render_start"), result.get("render_end")
    if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or end <= start:
        return "render_evidence_invalid"
    for sample in samples:
        if (sample.get("exit_code") == 0 and sample.get("start", end) < end
                and sample.get("end", start) > start
                and any(m.get("pid") == pid and 0 < m.get("sm_percent", 0) <= 100
                        for m in sample.get("matches", []))):
            return "gpu_render_verified"
    return "gpu_render_completed_unverified"


def attempt(blender, backend, directory, timeout, device_id=None):
    directory.mkdir()
    cmd = [str(blender), "--background", "--factory-startup", "--disable-autoexec",
           "--python-exit-code", "2", "--python", str(Path(__file__).resolve()),
           "--", "worker", backend, str(directory)]
    if device_id:
        cmd += ["--device-id", device_id]
    samples, done = [], threading.Event()
    timed_out, rc = False, None
    with (directory / "blender.log").open("xb") as log:
        try:
            proc = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT,
                                    stdin=subprocess.DEVNULL)
        except OSError as exc:
            return {"backend": backend, "status": "probe_process_failed", "error": str(exc)}
        watcher = threading.Thread(target=monitor, daemon=True,
                                   args=(proc.pid, shutil.which("nvidia-smi"), done, samples))
        watcher.start()
        try:
            rc = proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            proc.kill()
            rc = proc.wait()
        finally:
            done.set()
            if proc.poll() is None:
                proc.kill()
                proc.wait()
            watcher.join(timeout=6)
    result = {}
    try:
        result = json.loads((directory / "worker.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        pass
    image = directory / "fixture.png"
    image_valid = valid_png(image) and result.get("image_sha256") == digest(image)
    return {"backend": backend, "status": classify(result, rc, timed_out, samples,
                                                     image_valid, proc.pid),
            "worker": result, "exit_code": rc, "timed_out": timed_out,
            "gpu_samples": samples, "log_sha256": digest(directory / "blender.log")}


def summarize(attempts):
    states = [a["status"] for a in attempts]
    if "gpu_render_verified" in states:
        return "gpu_render_verified"
    if "gpu_render_completed_unverified" in states:
        return "gpu_render_completed_unverified"
    if "device_selection_required" in states:
        return "device_selection_required"
    if states and all(s in ("no_matching_gpu", "backend_configuration_unavailable") for s in states):
        return "no_usable_device_detected_in_test_session"
    return "gpu_qualification_blocked"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--blender", required=True, help="Exact pinned Blender executable")
    p.add_argument("--output", required=True, help="New private evidence directory")
    p.add_argument("--backend", choices=("auto", *BACKENDS), default="auto")
    p.add_argument("--device-id", help="Exact Cycles device ID; requires explicit backend")
    p.add_argument("--timeout", type=int, default=120, help="Seconds per backend, 15–180")
    args = p.parse_args(argv)
    if not 15 <= args.timeout <= 180 or (args.device_id and args.backend == "auto"):
        p.error("timeout must be 15–180; --device-id requires --backend")
    exe = shutil.which(args.blender)
    if not exe:
        p.error("Pinned Blender executable not found")
    blender = Path(exe).resolve(strict=True)
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=False)
    backends = BACKENDS if args.backend == "auto" else (args.backend,)
    attempts = []
    for backend in backends:
        a = attempt(blender, backend, out / backend.lower(), args.timeout, args.device_id)
        attempts.append(a)
        if a["status"] in ("gpu_render_verified", "gpu_render_completed_unverified",
                           "device_selection_required"):
            break
    status = summarize(attempts)
    selected = next((a for a in attempts if a["status"] == "gpu_render_verified"), None)
    report = {"schema": 1, "status": status, "blender": str(blender),
              "blender_sha256": digest(blender), "attempts": attempts,
              "qualified_backend": selected["backend"] if selected else None,
              "scope": "NVIDIA headless synthetic render only; not viewport FPS or model qualification",
              "limitations": ["No CPU fallback accepted as GPU success",
                              "No positive pmon sample does not establish GPU incompatibility",
                              "GPU utilization corroborates execution, not every individual kernel",
                              "Fixture is bounded, not a hard RAM/VRAM enforcement mechanism",
                              "No user preferences or production project saved"]}
    save_json(out / "gpu-qualification.json", report)
    print(json.dumps({"status": status, "report": str(out / "gpu-qualification.json")}))
    return 0 if status == "gpu_render_verified" else 3


if __name__ == "__main__":
    if "--" in sys.argv and sys.argv[sys.argv.index("--") + 1:][:1] == ["worker"]:
        parser = argparse.ArgumentParser()
        parser.add_argument("backend", choices=BACKENDS)
        parser.add_argument("directory")
        parser.add_argument("--device-id")
        a = parser.parse_args(sys.argv[sys.argv.index("--") + 2:])
        worker(a.backend, a.directory, a.device_id)
    else:
        raise SystemExit(main())
