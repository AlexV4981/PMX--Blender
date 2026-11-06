"""Hash-bound bridge with two independent Blender processes.

Phase A runs the untrusted candidate and creates a derivative. Phase B is a fresh
process with trusted oracle code and read-only access to Phase A's artifacts.
Only Phase B can write the verifier result. No candidate code runs in Phase B.
"""
import json
from pathlib import Path
import re
import subprocess
import tempfile
import time
import uuid

from .ledger import LedgerError, fixture_hash, loads_strict, sha256_bytes

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ORACLE = ROOT / "astra-qwen-weight-lab" / "blender_oracle.py"
PROBE = HERE / "isolation_probe.py"
BUILDER = HERE / "trusted_builder.py"
VERIFIER = HERE / "trusted_verifier.py"
EXECUTABLE_TASKS = {"geometry_weight_normalize", "left_arm_ik", "face_driver_setup", "motion_tip_verify"}
PINNED = re.compile(r"[A-Za-z0-9_./:-]+@sha256:[0-9a-f]{64}\Z")
OFFICIAL_ACK = "I_ACKNOWLEDGE_NO_NETWORK_SANDBOX"
LEGACY_ORACLE_LIMITATIONS = [
    "fresh-process synthetic oracle; Blender runtime and container isolation not verified in this release",
    "sandbox cannot prevent an operator who controls the host from replacing trusted evidence",
]
CRITICAL_REASONS = ("Geometry, MASK, or shape keys changed", "Accepted armature rest data changed",
                    "Shape key topology changed", "Neutral pose not restored",
                    "Pole placement unresolved")
STAGE_CATEGORY = {"03": "deformation", "04": "rig_space", "05": "morph", "06": "rig_space"}
RUBRIC = "pmx-synth-v1: critical = protected invariant (source geometry/morph/rest data, accepted rig, pole) violated"


class ProbeResult:
    def __init__(self, verified, runtime_identity, details):
        self.verified, self.runtime_identity, self.details = verified, runtime_identity, details


def oracle_version():
    data = ORACLE.read_bytes()
    commit = "unknown"
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True,
                                timeout=10, check=True).stdout.strip()
    except Exception:
        pass
    return "oracle_sha256:%s;repo_commit:%s" % (sha256_bytes(data), commit)


def sandbox_flags(image, mounts, *, mem="5g", cpus="4", pids="128", name=None):
    """docker argv up to and including the image name. mounts = [(src, dst, readonly)]."""
    if not PINNED.fullmatch(image):
        raise LedgerError("Blender image must be pinned as name@sha256:<digest>")
    cmd = ["docker", "run", "--rm"] + (["--name", name] if name else []) + ["--network", "none", "--read-only", "--cap-drop", "ALL", "--user", "65534:65534",
           "--security-opt", "no-new-privileges", "--pids-limit", pids, "--memory", mem,
           "--cpus", cpus, "--ipc", "private", "--entrypoint", "blender",
           "--tmpfs", "/tmp:rw,nosuid,size=268435456",
           "--env", "PMX_QWEN_ISOLATED_BLENDER=" + OFFICIAL_ACK,
           "--env", "HOME=/tmp", "--env", "XDG_CONFIG_HOME=/tmp/.config",
           "--env", "XDG_CACHE_HOME=/tmp/.cache"]
    for src, dst, ro in mounts:
        cmd += ["--mount", "type=bind,src=%s,dst=%s%s" % (Path(src).resolve(), dst, ",readonly" if ro else "")]
    return cmd + [image]


def assert_mounts_exclude(mounts, forbidden_dirs):
    for src, _dst, _ro in mounts:
        p = Path(src).resolve()
        for f in forbidden_dirs:
            f = Path(f).resolve()
            if p == f or f in p.parents or p in f.parents:
                raise LedgerError("mount %s would expose ledger/artifact storage" % p)


def parse_probe(stdout):
    """Decide from probe output. Verified only if every observed check passes."""
    matches = [l for l in stdout.splitlines() if l.startswith("ISOLATION_PROBE_RESULT ")]
    if len(matches) != 1:
        return {"verified": False, "why": "missing or multiple probe results"}
    line = matches[0]
    try:
        d = json.loads(line.split(" ", 1)[1])
    except ValueError:
        return {"verified": False, "why": "unparsable probe output"}
    ok = (d.get("network_blocked") is True and d.get("root_readonly") is True
          and d.get("forbidden_paths_present") == [] and d.get("secret_env_keys") == []
          and isinstance(d.get("blender_version"), str) and d.get("blender_version"))
    return {"verified": bool(ok), "details": d, "why": "" if ok else "a probe check failed or Blender version missing"}


def run_probe(image, *, runner=subprocess.run, forbidden_dirs=()):
    """Run the probe in the real container configuration. Unverified if docker/image is unavailable."""
    mounts = [(PROBE, "/lab/probe.py", True)]
    assert_mounts_exclude(mounts, forbidden_dirs)
    try:
        cmd = sandbox_flags(image, mounts) + ["--background", "--factory-startup", "--disable-autoexec", "--python-exit-code", "1", "--python", "/lab/probe.py"]
        r = runner(cmd, capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired, LedgerError) as exc:
        return ProbeResult(False, "unavailable", {"why": type(exc).__name__ + ": " + str(exc)[:200]})
    p = parse_probe(r.stdout or "")
    if r.returncode != 0:
        p = {"verified": False, "why": "probe command exited nonzero: %s" % r.returncode,
             "details": p.get("details", {})}
    ident = "%s;blender:%s" % (image, (p.get("details") or {}).get("blender_version"))
    return ProbeResult(p["verified"], ident, p)


def _clean(text, n=300):
    return re.sub(r"[\x00-\x1f\x7f]", " ", str(text))[:n]


def derive_verdict(attempt, *, oracle_result, exit_code, timed_out, candidate_sha, fixture_sha, probe, wall,
                   builder_exit_code=None, trusted_oracle_sha=None):
    """Pure function: map observed evidence to verdict fields. Never returns pass on doubtful evidence."""
    base = {"attempt_id": attempt["attempt_id"], "candidate_sha256": attempt["candidate_sha256"],
            "fixture_sha256": attempt["fixture_sha256"], "oracle_version": oracle_version(),
            "runtime_identity": probe.runtime_identity, "failure_category": "none", "severity": "none",
            "severe_regression": False, "evidence_sha256": None, "evidence_path": None,
            "wall_seconds": wall, "isolation_verified": bool(probe.verified),
            "evaluator_limitations": list(LEGACY_ORACLE_LIMITATIONS), "reason": "", "reevaluation_of": None}

    def out(result, cat="none", sev="none", reason="", blocked=None):
        v = dict(base, result=result, failure_category=cat, severity=sev, reason=_clean(reason))
        v["severe_regression"] = sev == "critical"
        if blocked:
            v["blocked_reason"] = blocked
        return v

    if candidate_sha is None:
        return out("not_run", "invalid_output", "none", "model produced no usable candidate code", "no_candidate")
    if candidate_sha != attempt["candidate_sha256"]:
        return out("blocked", "integrity", "none", "candidate bytes do not match attempt hash", "candidate_hash_mismatch")
    if fixture_sha != attempt["fixture_sha256"]:
        return out("blocked", "integrity", "none", "fixture does not match attempt hash", "fixture_hash_mismatch")
    if not probe.verified:
        return out("blocked", "sandbox", "none", "sandbox isolation not verified", "isolation_unverified")
    if timed_out:
        return out("blocked", "timeout", "none", "execution exceeded time limit", "timeout")
    if builder_exit_code != 0 or exit_code != 0:
        return out("blocked", "evaluator", "none",
                   "candidate or fresh verifier exited nonzero (builder=%s verifier=%s)" % (builder_exit_code, exit_code),
                   "nonzero_execution_exit")
    if not isinstance(oracle_result, dict):
        return out("blocked", "evaluator", "none", "no parsable oracle result (exit %s)" % exit_code, "no_oracle_result")
    r = oracle_result
    if (r.get("verifier_phase") != "fresh_process_no_candidate_exec"
            or r.get("blender_executed") is not True or not isinstance(r.get("blender_pass"), bool)
            or r.get("source_sha256") != candidate_sha
            or r.get("fixture_sha256") != fixture_sha
            or r.get("oracle_sha256") != trusted_oracle_sha
            or r.get("case_id") != attempt["case_id"]
            or r.get("stage") != attempt["stage"]):
        return out("blocked", "integrity", "none", "oracle result failed identity/hash binding", "oracle_binding_failed")
    if r["blender_pass"]:
        return out("pass", "none", "none", r.get("oracle_detail", ""))
    detail, feedback = str(r.get("oracle_detail", "")), str(r.get("error_feedback", ""))
    if "Script must expose callable solve" in feedback:
        cat = "invalid_output"
    elif "Traceback (most recent call last)" in detail:
        cat = "blender_api"
    else:
        cat = STAGE_CATEGORY.get(attempt["stage"], "evaluator")
    sev = "critical" if any(feedback.startswith(c) for c in CRITICAL_REASONS) else "major"
    return out("fail", cat, sev, feedback)


def default_executor(cmd, timeout):
    t0 = time.monotonic()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr, False, time.monotonic() - t0
    except subprocess.TimeoutExpired as exc:
        if "--name" in cmd:  # killing the docker client does not stop the container
            subprocess.run(["docker", "kill", cmd[cmd.index("--name") + 1]], capture_output=True, timeout=30)
        return None, (exc.stdout or ""), (exc.stderr or ""), True, time.monotonic() - t0
    except OSError as exc:
        return None, "", str(exc), False, time.monotonic() - t0


def evaluate_attempt(ledger, store, experiment_id, attempt_id, *, image, probe, executor=default_executor,
                     timeout=240, reevaluation_of=None, scratch_root=None):
    """Evaluate one attempt and append the verdict. `probe` must come from run_probe (or a test double)."""
    events = ledger.read()
    attempt = next((e for e in events if e["event_type"] == "attempt" and e["attempt_id"] == attempt_id), None)
    if attempt is None:
        raise LedgerError("unknown attempt " + attempt_id)
    if attempt["task_id"] not in EXECUTABLE_TASKS or attempt["stage"] not in ("03", "04", "05", "06"):
        raise LedgerError("task/stage not authorised for execution")
    if attempt["fixture_kind"] != "synthetic":
        raise LedgerError("only synthetic fixtures are executable by the legacy oracle")
    started = time.monotonic()
    cand_sha = fix_sha = None
    case_bytes = cand_bytes = None
    try:
        if attempt["candidate_sha256"]:
            cand_bytes = store.get("candidates", attempt["candidate_sha256"], ".py")
            cand_sha = sha256_bytes(cand_bytes)
        case_bytes = store.get("fixtures", attempt["fixture_sha256"], ".json")
        fix_sha = fixture_hash(loads_strict(case_bytes.decode("utf-8")))
    except LedgerError:
        cand_sha = "0" * 64 if attempt["candidate_sha256"] else None  # forces a binding failure
        fix_sha = fix_sha or "0" * 64
    oracle_result, exit_code, builder_exit, timed_out = None, None, None, False
    so, se, builder_stdout, builder_stderr = "", "", "", ""
    staged_hashes = {}
    trusted_oracle_sha = sha256_bytes(ORACLE.read_bytes())
    if cand_bytes is not None and probe.verified and cand_sha == attempt["candidate_sha256"] \
            and fix_sha == attempt["fixture_sha256"]:
        with tempfile.TemporaryDirectory(dir=scratch_root) as temp:
            td = Path(temp)
            for name in ("in", "candidate_out", "trusted_out"):
                (td / name).mkdir()
            # Ephemeral output mounts only; never mount ledger/artifact store.
            (td / "candidate_out").chmod(0o777)
            (td / "trusted_out").chmod(0o777)
            files = {"candidate.py": cand_bytes, "case.json": case_bytes,
                     "oracle.py": ORACLE.read_bytes(),
                     "builder.py": BUILDER.read_bytes(), "verifier.py": VERIFIER.read_bytes()}
            for name, data in files.items():
                f = td / "in" / name
                f.write_bytes(data)
                f.chmod(0o444)
                staged_hashes[name] = sha256_bytes(data)
            # The candidate process can write ONLY candidate_out, never trusted_out.
            builder_mounts = [(td / "in" / name, "/lab/" + name, True)
                              for name in ("candidate.py", "case.json", "oracle.py", "builder.py")]
            builder_mounts += [(td / "candidate_out", "/candidate_out", False)]
            assert_mounts_exclude(builder_mounts, [ledger.path.parent, store.root])
            builder_cmd = sandbox_flags(image, builder_mounts, name="pmx-build-" + uuid.uuid4().hex[:12]) \
                + ["--background", "--factory-startup", "--disable-autoexec", "--python-exit-code", "1", "--python", "/lab/builder.py"]
            builder_exit, builder_stdout, builder_stderr, timeout_a, _ = executor(builder_cmd, timeout)
            timed_out = bool(timeout_a)
            derived = td / "candidate_out" / "candidate.blend"
            summary = td / "candidate_out" / "result.json"
            # Fresh verifier never mounts builder.py and does not exec candidate.py.
            if not timed_out and builder_exit == 0 and derived.is_file() and not derived.is_symlink() \
                    and 0 < derived.stat().st_size < 256 * 1024 * 1024 and summary.is_file() \
                    and not summary.is_symlink() and summary.stat().st_size < 1000000:
                verifier_mounts = [(td / "in" / name, "/lab/" + name, True)
                                   for name in ("candidate.py", "case.json", "oracle.py", "verifier.py")]
                verifier_mounts += [(td / "candidate_out", "/candidate_artifacts", True),
                                    (td / "trusted_out", "/trusted_out", False)]
                assert_mounts_exclude(verifier_mounts, [ledger.path.parent, store.root])
                verifier_cmd = sandbox_flags(image, verifier_mounts, name="pmx-check-" + uuid.uuid4().hex[:12]) \
                    + ["--background", "--factory-startup", "--disable-autoexec", "--python-exit-code", "1", "--python", "/lab/verifier.py"]
                exit_code, so, se, timeout_b, _ = executor(verifier_cmd, timeout)
                timed_out = bool(timeout_b)
                out = td / "trusted_out" / "oracle.json"
                if out.is_file() and not out.is_symlink() and out.stat().st_size < 1000000:
                    try:
                        oracle_result = loads_strict(out.read_text(encoding="utf-8"))
                    except ValueError:
                        pass
            for name, data in files.items():
                if sha256_bytes((td / "in" / name).read_bytes()) != staged_hashes[name]:
                    oracle_result = None
    wall = round(time.monotonic() - started, 3)
    v = derive_verdict(attempt, oracle_result=oracle_result, exit_code=exit_code,
                       builder_exit_code=builder_exit, trusted_oracle_sha=trusted_oracle_sha,
                       timed_out=timed_out, candidate_sha=cand_sha, fixture_sha=fix_sha,
                       probe=probe, wall=wall)
    bundle = {"trusted_verifier_result": oracle_result, "builder_exit_code": builder_exit,
              "verifier_exit_code": exit_code, "timed_out": timed_out,
              "builder_stdout_tail": (builder_stdout or "")[-4000:],
              "builder_stderr_tail": (builder_stderr or "")[-4000:],
              "verifier_stdout_tail": (so or "")[-4000:], "verifier_stderr_tail": (se or "")[-4000:],
              "staged_sha256": staged_hashes, "probe": probe.details,
              "rubric": RUBRIC, "trusted_oracle_sha256": trusted_oracle_sha}
    ev_sha = store.put("evidence", json.dumps(bundle, sort_keys=True).encode(), ".json")
    v["evidence_sha256"], v["evidence_path"] = ev_sha, "evidence/%s.json" % ev_sha
    if v["result"] == "pass" and not v["evidence_sha256"]:
        raise LedgerError("refusing pass without evidence")
    v["reevaluation_of"] = reevaluation_of
    return ledger.append("verdict", "trusted_evaluator", experiment_id, v, artifacts=store)
