#!/usr/bin/env python3
"""Portable, bounded Ollama coding worker. Propose first; apply only after review."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "qwen-helper"
OUTBOX = HELPER / "outbox"
CONFIG = HELPER / "project.json"
KINDS = {"bugfix", "new_tool", "test", "logging"}

# Legacy manual tasks use the configured original Qwen model. Qualified specialists
# are opted into explicitly by task and are never assumed to be installed.
def resolve_model(task, config):
    if "specialist" not in task:
        return config["model"]
    import specialists
    return specialists.model_for_task(task, config["model"])

SCOPES = {"generic", "character_specific"}
BLOCKED_PARTS = {".git", ".github", ".agents", "qwen-helper", ".venv",
                 "node_modules", "__pycache__", ".env", "vendor", "dist", "build"}

class Stop(ValueError):
    pass

def read_config():
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    if cfg.get("version") != 1 or not isinstance(cfg.get("allow_paths"), list) or not cfg["allow_paths"]:
        raise Stop("Run setup.py before using the helper")
    checks = cfg.get("checks")
    if not isinstance(checks, list) or not checks or any(
        not isinstance(cmd, list) or not cmd or any(not isinstance(v, str) or not v for v in cmd)
        for cmd in checks
    ):
        raise Stop("At least one validated test command is required")
    endpoint = urlsplit(cfg.get("ollama_url", "http://127.0.0.1:11434/api/generate"))
    if endpoint.scheme != "http" or endpoint.hostname not in {"127.0.0.1", "localhost", "::1"} or endpoint.path != "/api/generate":
        raise Stop("Ollama must use the loopback HTTP endpoint")
    return cfg

def parts_of(name):
    if not isinstance(name, str) or not name or "\\" in name:
        raise Stop("Invalid path")
    rel = PurePosixPath(name)
    if rel.is_absolute() or any(p in ("..", "") for p in rel.parts):
        raise Stop("Path escape rejected")
    return rel

def contained(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False

def safe_path(name, cfg):
    rel = parts_of(name)
    if any(p.startswith(".") or p in BLOCKED_PARTS for p in rel.parts):
        raise Stop("Hidden/protected path")
    path = (ROOT / Path(*rel.parts)).resolve()
    if not contained(path, ROOT.resolve()):
        raise Stop("Path outside project")
    for denied in cfg.get("deny_paths", []):
        blocked = (ROOT / Path(*parts_of(denied).parts)).resolve()
        if path == blocked or contained(path, blocked):
            raise Stop("Target explicitly denied")
    if not any(contained(path, (ROOT / Path(*parts_of(base).parts)).resolve())
               for base in cfg["allow_paths"]):
        raise Stop("Target outside allowed directories")
    if path.suffix not in cfg.get("extensions", [".py"]):
        raise Stop("Unsupported file extension")
    cur = ROOT
    for part in rel.parts:
        cur = cur / part
        if cur.is_symlink():
            raise Stop("Symlink paths are forbidden")
    return path

def load_task(task_file, cfg):
    task = json.loads(Path(task_file).read_text(encoding="utf-8"))
    if not isinstance(task, dict) or task.get("kind") not in KINDS:
        raise Stop("Unsupported task type")
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{2,50}", str(task.get("task_id", ""))):
        raise Stop("Invalid task ID")
    for field in ("objective", "expected_behavior"):
        value = task.get(field)
        if not isinstance(value, str) or not value.strip() or len(value) > 1600:
            raise Stop(f"Missing or excessive {field}")
    if task["kind"] == "bugfix" and not str(task.get("reproducer", "")).strip():
        raise Stop("Bugfix requires reproduction evidence")
    if task.get("cross_subsystem") or task.get("requires_visual_judgment"):
        raise Stop("Escalate multi-subsystem/visual tasks to Codex")
    scope = task.get("scope", "generic")
    if scope not in SCOPES:
        raise Stop("Unknown task scope")
    target = safe_path(task.get("target"), cfg)
    if task["kind"] == "new_tool":
        if target.exists() or not target.name.startswith("qwen_"):
            raise Stop("New tools must be unused qwen_*.py files")
    elif not target.is_file():
        raise Stop("Target missing")
    if scope == "character_specific":
        if task["kind"] != "new_tool" or not target.name.startswith("qwen_character_"):
            raise Stop("Character-specific changes must be a separate new qwen_character_*.py adapter")
        if not isinstance(task.get("character_id"), str) or not task["character_id"].strip():
            raise Stop("Character-specific task requires character_id")
        if not isinstance(task.get("character_requirements"), str) or not task["character_requirements"].strip():
            raise Stop("Character-specific task needs observed requirements from the run profile")
        if not isinstance(task.get("generic_baseline"), str) or not task["generic_baseline"].strip():
            raise Stop("Describe what generic behavior must remain unchanged")
    elif any(task.get(k) for k in ("character_id", "character_requirements")):
        raise Stop("Character-specific information requires explicit character_specific scope")
    refs = task.get("references", [])
    limits = cfg.get("limits", {})
    if not isinstance(refs, list) or len(refs) > limits.get("max_references", 1):
        raise Stop("Too many reference files")
    sources = []
    for p in [target] + [safe_path(ref, cfg) for ref in refs]:
        if p.exists():
            if not p.is_file() or p.stat().st_size > limits.get("max_file_bytes", 5500):
                raise Stop("Input file too large")
            sources.append({"path": p.relative_to(ROOT).as_posix(), "content": p.read_text(encoding="utf-8")})
        elif p != target:
            raise Stop("Missing reference file")
    if len(json.dumps({"task": task, "sources": sources})) > limits.get("max_input_chars", 9200):
        raise Stop("Input context too large")
    return task, target, sources

def load_task_data(task, cfg):
    """Validate a planned task without modifying the worktree."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "task.json"
        path.write_text(json.dumps(task), encoding="utf-8")
        return load_task(path, cfg)

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None

def propose(args):
    # Prevent new delegation if reviewed Qwen results cross the configured >10% threshold.
    gate = subprocess.run([sys.executable, str(HELPER / "review.py"), "--fail-over-threshold"],
                          cwd=ROOT, capture_output=True, text=True, timeout=15)
    if gate.returncode:
        raise Stop("Review ledger invalid or correction rate above 10%; stop delegating. " + (gate.stdout + gate.stderr)[-1000:])
    cfg = read_config()
    task, target, sources = load_task(args.task, cfg)
    model_name = resolve_model(task, cfg)
    message = ("You support a GENERAL PMX-to-native-Blender Cycles-only pipeline. "
               "Write exactly one complete Python source file for this isolated maintenance task. "
               "Preserve correct behavior for other characters; never hardcode character-specific constants "
               "into generic tools. Character-specific tools are separate opt-in adapters only. "
               "Do not alter shaders, geometry, rigs, physics, approvals, accepted artifacts, "
               "secrets, permissions, or architecture. "
               "Answer JSON with target, code, explanation. If uncertain return empty code. "
               "No markdown.\n" + json.dumps({"task": task, "sources": sources}, ensure_ascii=False))
    limits = cfg.get("limits", {})
    req = Request(cfg.get("ollama_url", "http://127.0.0.1:11434/api/generate"),
        data=json.dumps({"model": model_name, "prompt": message, "stream": False, "format": "json",
                         "options": {"num_ctx": limits.get("context_tokens", 4096),
                                     "num_predict": limits.get("output_tokens", 1536),
                                     "temperature": 0.1}}).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    with urlopen(req, timeout=180) as response:
        proposal = json.loads(json.loads(response.read().decode("utf-8"))["response"])
    code = proposal.get("code") if isinstance(proposal, dict) else None
    if not isinstance(proposal, dict) or proposal.get("target") != task["target"] or not isinstance(code, str) or not code.strip():
        raise Stop("Qwen did not return a valid one-file proposal")
    if len(code.encode("utf-8")) > limits.get("max_output_bytes", 6500):
        raise Stop("Proposed file exceeds limit")
    if target.suffix == ".py":
        compile(code, str(target), "exec")
    OUTBOX.mkdir(exist_ok=True)
    output = OUTBOX / (task["task_id"] + ".json")
    if output.exists():
        raise Stop("Task ID already proposed; keep original evidence")
    output.write_text(json.dumps({"task": task, "model": model_name,
                  "base_sha256": digest(target), "proposal": proposal}, indent=2) + "\n", encoding="utf-8")
    print("PROPOSED (not executed):", output)

def apply(args):
    if not args.reviewed:
        raise Stop("Explicit --reviewed required: inspect full generated code before execution")
    cfg = read_config()
    task, target, _ = load_task(args.task, cfg)
    model_name = resolve_model(task, cfg)
    record = json.loads(Path(args.proposal).read_text(encoding="utf-8"))
    if record.get("task") != task or record.get("model") != model_name or record.get("base_sha256") != digest(target):
        raise Stop("Stale submission, different model, or changed task")
    proposal = record.get("proposal", {})
    code = proposal.get("code")
    if proposal.get("target") != task["target"] or not isinstance(code, str) or not code.strip():
        raise Stop("Invalid patch")
    if len(code.encode("utf-8")) > cfg.get("limits", {}).get("max_output_bytes", 6500):
        raise Stop("Output too large")
    if target.suffix == ".py":
        compile(code, str(target), "exec")
    # Refuse any pre-existing local edit to the target. Never discard existing human work.
    git = subprocess.run(["git", "status", "--porcelain", "--", task["target"]],
                         cwd=ROOT, capture_output=True, text=True, timeout=15)
    if git.returncode or git.stdout.strip():
        raise Stop("Target is dirty or git status unavailable; use a clean disposable worktree")
    before = target.read_bytes() if target.exists() else None
    target.parent.mkdir(parents=True, exist_ok=True)
    logs, success = [], False
    target.write_text(code, encoding="utf-8")
    try:
        for cmd in cfg["checks"]:
            result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True,
                                    timeout=cfg.get("limits", {}).get("test_timeout_seconds", 180),
                                    shell=False)
            logs.append({"command": cmd, "exit_code": result.returncode,
                         "output": (result.stdout + "\n" + result.stderr)[-12000:]})
            if result.returncode:
                raise Stop("Check failed: proposal reverted")
        success = True
    finally:
        if not success:
            if before is None:
                target.unlink(missing_ok=True)
            else:
                target.write_bytes(before)
        Path(args.proposal).with_suffix(".validation.json").write_text(json.dumps(
            {"task_id": task["task_id"], "passed": success, "checks": logs,
             "note": "Passing generic checks does not replace task-specific acceptance testing."}, indent=2) + "\n")
    print("Checks passed; inspect diff, run task-specific reproducer and record human/Codex review.")

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    commands = p.add_subparsers(dest="command", required=True)
    x = commands.add_parser("propose"); x.add_argument("--task", required=True)
    x = commands.add_parser("apply"); x.add_argument("--task", required=True)
    x.add_argument("--proposal", required=True); x.add_argument("--reviewed", action="store_true")
    args = p.parse_args(argv)
    try:
        {"propose": propose, "apply": apply}[args.command](args)
    except (ValueError, OSError, KeyError, TimeoutError, subprocess.TimeoutExpired) as e:
        print("HARD STOP / CODEX ESCALATION:", e, file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
