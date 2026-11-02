#!/usr/bin/env python3
"""Bounded local Ollama proposer; apply runs tests and rolls back on failure."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "anime-blender-pipeline" / "scripts"
OUTBOX = ROOT / "qwen-helper" / "outbox"
MODEL = "qwen2.5-coder:7b-instruct-q4_K_M"
KINDS = {"bugfix", "new_utility", "test", "logging"}
PROTECTED = {"pipeline.py", "blender_tools.py", "pmx_inventory.py", "math_tools.py"}

class Stop(ValueError):
    pass

def safe_path(name):
    if not isinstance(name, str) or not name or "\\" in name:
        raise Stop("Invalid path")
    p = (ROOT / name).resolve()
    if p.parent not in {SCRIPTS.resolve(), (SCRIPTS / "tests").resolve()}:
        raise Stop("Only scripts/ or scripts/tests/ files allowed")
    if p.suffix != ".py" or p.name in PROTECTED or not re.fullmatch(r"[A-Za-z_]\w*\.py", p.name):
        raise Stop("Protected or non-Python file")
    return p

def load_task(path):
    task = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(task, dict) or task.get("kind") not in KINDS:
        raise Stop("Unsupported task category")
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{2,50}", str(task.get("task_id", ""))):
        raise Stop("Invalid task ID")
    for key in ("objective", "expected_behavior"):
        v = task.get(key)
        if not isinstance(v, str) or not v.strip() or len(v) > 1600:
            raise Stop("Missing or oversized objective/expected output")
    if task.get("cross_subsystem") or task.get("requires_visual_judgment"):
        raise Stop("Complex or visual work belongs to Codex")
    target = safe_path(task.get("target"))
    if task["kind"] == "new_utility":
        if target.exists() or not target.name.startswith("qwen_") or target.parent != SCRIPTS.resolve():
            raise Stop("New tools must be new scripts/qwen_*.py")
    elif not target.is_file():
        raise Stop("Target does not exist")
    refs = task.get("references", [])
    if not isinstance(refs, list) or len(refs) > 1:
        raise Stop("At most one reference file")
    sources = []
    for p in [target] + [safe_path(r) for r in refs]:
        if p.exists():
            if not p.is_file() or p.stat().st_size > 5500:
                raise Stop("File exceeds verified admission budget")
            sources.append({"path": str(p.relative_to(ROOT)), "content": p.read_text(encoding="utf-8")})
        elif p != target:
            raise Stop("Missing reference")
    if sum(len(s["content"]) for s in sources) + len(task["objective"]) + len(task["expected_behavior"]) > 9200:
        raise Stop("Context too large")
    return task, target, sources

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None

def propose(args):
    task, target, sources = load_task(args.task)
    prompt = ("Implement exactly one Python file. Do not change architecture, approvals, rigs, physics or shaders. "
              "Return JSON {target, code, explanation}; code is COMPLETE file content, no markdown. "
              "Return empty code if unable.\n" + json.dumps({"task": task, "source": sources}))
    payload = {"model": MODEL, "prompt": prompt, "stream": False, "format": "json",
               "options": {"num_ctx": 4096, "num_predict": 1536, "temperature": 0.1}}
    req = Request("http://127.0.0.1:11434/api/generate", data=json.dumps(payload).encode(),
                  headers={"Content-Type": "application/json"})
    with urlopen(req, timeout=180) as response:
        proposal = json.loads(json.loads(response.read().decode())["response"])
    code = proposal.get("code") if isinstance(proposal, dict) else None
    if proposal.get("target") != task["target"] or not isinstance(code, str) or not code.strip() or len(code.encode()) > 6500:
        raise Stop("Model could not produce an eligible patch")
    compile(code, str(target), "exec")
    OUTBOX.mkdir(exist_ok=True)
    dest = OUTBOX / (task["task_id"] + ".json")
    if dest.exists():
        raise Stop("Proposal ID already exists")
    dest.write_text(json.dumps({"task": task, "base_sha256": digest(target), "proposal": proposal}, indent=2) + "\n")
    print("Review proposal:", dest)

def apply(args):
    task, target, _ = load_task(args.task)
    record = json.loads(Path(args.proposal).read_text())
    if record["task"] != task or record["base_sha256"] != digest(target):
        raise Stop("Task or original file changed; stale proposal")
    code = record["proposal"]["code"]
    if record["proposal"].get("target") != task["target"] or not isinstance(code, str) or len(code.encode()) > 6500:
        raise Stop("Unexpected replacement")
    compile(code, str(target), "exec")
    previous = target.read_bytes() if target.exists() else None
    cmds = [[sys.executable, "-m", "unittest", "discover", "-s", str(SCRIPTS / "tests"), "-v"],
            [sys.executable, str(SCRIPTS / "blender_tools.py"), "validate-seeds"]]
    logs, success = [], False
    target.write_text(code, encoding="utf-8")
    try:
        for cmd in cmds:
            p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=180)
            logs.append({"command": cmd, "exit_code": p.returncode, "log": (p.stdout + p.stderr)[-10000:]})
            if p.returncode:
                raise Stop("Tests failed, proposal rolled back")
        success = True
    finally:
        if not success:
            if previous is None:
                target.unlink(missing_ok=True)
            else:
                target.write_bytes(previous)
        Path(args.proposal).with_suffix(".validation.json").write_text(
            json.dumps({"task_id": task["task_id"], "passed": success, "logs": logs}, indent=2) + "\n")
    print("Tests pass. Check git diff and behavior before recording approval.")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("propose"); p.add_argument("--task", required=True)
    p = sub.add_parser("apply"); p.add_argument("--task", required=True); p.add_argument("--proposal", required=True)
    args = parser.parse_args()
    try:
        {"propose": propose, "apply": apply}[args.command](args)
    except (ValueError, OSError, KeyError, TimeoutError, subprocess.TimeoutExpired) as exc:
        print("STOP / ESCALATE:", exc, file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
