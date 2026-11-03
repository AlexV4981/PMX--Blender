#!/usr/bin/env python3
"""One-attempt local offload. Fail closed; hand control to the ORIGINAL Codex path."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import local_worker
import specialists

def fallback(reason, task=None):
    return {"route": "original_codex_pipeline", "local_attempts_remaining": 0,
            "reason": str(reason), "task_id": (task or {}).get("task_id"),
            "instruction": "Do not retry Qwen. Continue existing Sol High/Light/Astra and human stage gates."}

def plan(task):
    try:
        branch=subprocess.run(["git","branch","--show-current"],cwd=local_worker.ROOT,
            text=True,capture_output=True,timeout=8,check=True).stdout.strip()
        if branch != "Qwen-Local-Helper":
            raise ValueError("Local specialists are restricted to Qwen-Local-Helper branch")
        gate=subprocess.run([local_worker.sys.executable,str(local_worker.HELPER/"review.py"),"--fail-over-threshold"],
            cwd=local_worker.ROOT,capture_output=True,text=True,timeout=10)
        if gate.returncode:
            raise ValueError("10% production review threshold or invalid ledger; fallback")
        spec = specialists.verify_served_model(task)
        cfg = local_worker.read_config()
        local_worker.load_task_data(task, cfg)
        return {"route": "local_qwen_one_attempt", "specialist": spec["name"],
                "model": spec["model"], "reviewer": "Sol Light (actual available profile)",
                "on_failure": "original_codex_pipeline"}
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        return fallback(exc, task)

def run(args):
    task = json.loads(Path(args.task).read_text(encoding="utf-8"))
    selection = plan(task)
    if args.command == "plan" or selection["route"] != "local_qwen_one_attempt":
        return selection
    if args.command == "propose":
        try:
            # The worker only writes a JSON proposal; it never executes generated code.
            local_worker.propose(SimpleNamespace(task=args.task))
            return {"route": "pending_sol_light_review", "task_id": task["task_id"],
                    "proposal": str(local_worker.OUTBOX / (task["task_id"] + ".json")),
                    "next": "Sol Light independently reviews exact proposal; no automatic approval."}
        except (ValueError, OSError, KeyError, TimeoutError, local_worker.subprocess.TimeoutExpired) as exc:
            return fallback(exc, task)
    proposal_path = local_worker.OUTBOX / (task["task_id"] + ".json")
    try:
        raw = proposal_path.read_bytes()
        att = json.loads(Path(args.review).read_text(encoding="utf-8"))
        if (att.get("task_id") != task["task_id"] or
                att.get("proposal_sha256") != hashlib.sha256(raw).hexdigest() or
                att.get("reviewer_role") != "sol_light" or
                att.get("decision") != "approve" or
                not isinstance(att.get("evidence"), str) or not att["evidence"].strip()):
            raise ValueError("Sol Light review missing, rejected, or not bound to this proposal")
        local_worker.apply(SimpleNamespace(task=args.task, proposal=str(proposal_path), reviewed=True))
        return {"route": "local_result_validated", "task_id": task["task_id"],
                "note": "Only local checks passed; final Blender, fidelity and human gates remain."}
    except (ValueError, OSError, KeyError, TimeoutError) as exc:
        return fallback(exc, task)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=["plan", "propose", "finalize"])
    p.add_argument("--task", required=True)
    p.add_argument("--review", help="Sol Light decision JSON (required for finalize)")
    args = p.parse_args()
    if args.command == "finalize" and not args.review:
        p.error("--review is required for finalize")
    try:
        result = run(args)
    except (ValueError, OSError, KeyError) as exc:
        result = fallback(exc)
    print(json.dumps(result, indent=2))
    # Fallback is a normal routing outcome, not a failed conversion.
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
