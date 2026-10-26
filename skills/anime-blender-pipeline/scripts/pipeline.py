#!/usr/bin/env python3
"""Local, dependency-free checkpoint and human-review ledger for the skill pack.

The CLI records an externally observed human decision; it cannot authenticate a
human. Agents must never fabricate --actor/--statement or treat a report as consent.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile

PACK = Path(__file__).resolve().parents[1]
VERSION = "3.0.0"
REVIEW_GATES = ("audit", "delivery")
STAGES = tuple(f"{i:02d}" for i in range(10))
ID = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}$")


class PipelineError(Exception):
    pass


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise PipelineError(f"Cannot read {path}: {e}") from e


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=path.parent, prefix=".pipeline-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(value, f, indent=2, sort_keys=True, allow_nan=False)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


@contextmanager
def lock(root):
    path = root / ".pipeline.lock"
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as e:
        raise PipelineError("Workspace locked; inspect the owning process before clearing a stale lock.") from e
    try:
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        yield
    finally:
        path.unlink(missing_ok=True)


def inside(root, path):
    path = Path(path)
    if not path.is_absolute():
        path = root / path
    path = path.resolve()
    if not path.is_relative_to(root):
        raise PipelineError(f"Working artifact must be inside workspace: {path}")
    if not path.is_file():
        raise PipelineError(f"Missing working artifact: {path}")
    if path.is_relative_to(root / "checkpoints"):
        raise PipelineError("Approved/submitted snapshots cannot be registered as mutable artifacts.")
    if path.name == "run.json" or path == root / "policy.json":
        raise PipelineError("Ledger/policy cannot be a candidate artifact.")
    return path


def stamp(root, path):
    p = inside(root, path)
    return {"path": p.relative_to(root).as_posix(), "sha256": digest(p),
            "bytes": p.stat().st_size}


def verify_stamp(root, item):
    try:
        p = (root / item["path"]).resolve()
        return p.is_relative_to(root) and p.is_file() and digest(p) == item["sha256"]
    except (KeyError, OSError, TypeError):
        return False


def load(root):
    run = read_json(root / "run.json")
    if run.get("schema_version") != 1 or run.get("pack_version") != VERSION:
        raise PipelineError("Unsupported ledger/pack version; do not silently migrate approvals.")
    if digest(root / "policy.json") != run.get("policy_sha256"):
        raise PipelineError("Policy changed; start a newly qualified run instead of weakening existing gates.")
    for s in run["sources"]:
        p = Path(s["path"])
        if not p.is_file() or digest(p) != s["sha256"]:
            raise PipelineError(f"Source changed or unavailable: {p}")
    # Validate every accepted checkpoint before allowing any further work.
    for stage in run["stages"].values():
        if stage.get("approved"):
            c = stage["candidates"][stage["approved"]]
            if not all(verify_stamp(root, x) for x in c["artifacts"]):
                raise PipelineError("Approved working bundle changed. Restore it; do not continue from unapproved data.")
            if not all(verify_stamp(root, x) for x in c.get("snapshot", [])):
                raise PipelineError("Approved snapshot changed or is missing.")
            errors = gate_errors(root, run, next(s for s, st in run["stages"].items() if st is stage), c)
            if errors:
                raise PipelineError("Approved checks/review evidence changed: " + "; ".join(errors))
            if c.get("approval", {}).get("bundle_sha256") != c["bundle_sha256"]:
                raise PipelineError("Approval does not identify the current bundle.")
    return run


def get_candidate(run, stage, cid):
    try:
        return run["stages"][stage]["candidates"][cid]
    except KeyError as e:
        raise PipelineError("Unknown stage or candidate") from e


def input_digest(run, stage):
    if stage == "00":
        return canonical(run["sources"])
    previous = run["stages"][f"{int(stage)-1:02d}"]
    cid = previous.get("approved")
    if not cid:
        raise PipelineError("Previous stage needs explicit human approval before work can advance.")
    return previous["candidates"][cid]["bundle_sha256"]


def live_bundle(root, c):
    return canonical([stamp(root, x["path"]) for x in c["artifacts"]])


def require_current(root, run, stage, c):
    if input_digest(run, stage) != c["input_sha256"]:
        raise PipelineError("Input checkpoint changed; downstream candidate is stale.")
    if live_bundle(root, c) != c["bundle_sha256"]:
        raise PipelineError("Candidate changed. Register a new revision and rerun its checks.")


def append_event(run, event, **data):
    run["events"].append({"time": now(), "event": event, **data})


def gate_errors(root, run, stage, c, reviews=True):
    errors = []
    try:
        require_current(root, run, stage, c)
    except PipelineError as e:
        errors.append(str(e))
    policy = read_json(root / "policy.json")
    for name in policy["stages"][stage]["required_checks"]:
        check = c["checks"].get(name)
        if not check or check["status"] != "pass":
            errors.append(f"Check not passed: {name}")
        elif check["bundle_sha256"] != c["bundle_sha256"] or not verify_stamp(root, check["evidence"]):
            errors.append(f"Check/evidence stale: {name}")
    if reviews and stage == "09":
        for name in REVIEW_GATES:
            review = c["reviews"].get(name)
            if not review or not verify_stamp(root, review["evidence"]):
                errors.append(f"Missing/stale explicit human subgate: {name}")
            elif name == "delivery" and review["bundle_sha256"] != c["bundle_sha256"]:
                errors.append(f"Human {name} review refers to an earlier candidate revision")
    return errors


def init_run(args, root):
    root.mkdir(parents=True, exist_ok=True)
    if (root / "run.json").exists():
        raise PipelineError("Run already exists; do not overwrite it.")
    sources = []
    for f in args.source:
        p = Path(f).resolve()
        if not p.is_file():
            raise PipelineError(f"Missing source: {p}")
        sources.append({"path": str(p), "sha256": digest(p), "bytes": p.stat().st_size})
    if len({s["path"] for s in sources}) != len(sources):
        raise PipelineError("Duplicate source paths")
    for name in ["work", "audit", "candidates", "checkpoints"]:
        (root / name).mkdir(exist_ok=True)
    shutil.copyfile(PACK / "assets" / "stage-policy.json", root / "policy.json")
    run = {"schema_version": 1, "pack_version": VERSION, "created": now(),
           "sources": sorted(sources, key=lambda x: x["path"]),
           "policy_sha256": digest(root / "policy.json"),
           "stages": {s: {"approved": None, "candidates": {}} for s in STAGES},
           "dependency_attempts": {}, "events": []}
    append_event(run, "created", source_count=len(sources))
    atomic_json(root / "run.json", run)
    return {"workspace": str(root), "status": "created", "next_stage": "00"}


def register(args, root, run):
    if not ID.fullmatch(args.candidate):
        raise PipelineError("Candidate ID must be 1–64 letters/digits/hyphens/underscores.")
    stage = run["stages"][args.stage]
    if stage["approved"]:
        raise PipelineError("Stage approved and immutable; branch a new run for retrospective changes.")
    inp = input_digest(run, args.stage)
    existing = stage["candidates"].get(args.candidate)
    if not existing and len(stage["candidates"]) >= 3:
        raise PipelineError("Three candidate IDs already used. Revise an existing candidate after critique.")
    if existing and existing["status"] != "draft":
        raise PipelineError("Submitted candidate requires explicit human feedback before revision.")
    paths = [args.file, *args.asset]
    artifacts = sorted([stamp(root, p) for p in paths], key=lambda x: x["path"])
    if len({a["path"] for a in artifacts}) != len(artifacts):
        raise PipelineError("Duplicate candidate artifact paths")
    source_paths = {Path(s["path"]).resolve() for s in run["sources"]}
    protected = {a["path"] for st in run["stages"].values() for c in st["candidates"].values()
                 if c["status"] == "approved" for a in c["artifacts"]}
    other_paths = {a["path"] for st in run["stages"].values() for cid, c in st["candidates"].items()
                   if c is not existing for a in c["artifacts"]}
    for a in artifacts:
        if (root / a["path"]).resolve() in source_paths or a["path"] in protected:
            raise PipelineError("Source/approved artifacts are read-only; create a derivative.")
        if a["path"] in other_paths:
            raise PipelineError("Candidate artifacts overlap another candidate; copy a private bundle.")
    rev = existing["revision"] + 1 if existing else 1
    historical_reviews = {k: v for k, v in (existing or {}).get("reviews", {}).items()
                          if args.stage == "09" and k == "audit"}
    c = {"id": args.candidate, "revision": rev, "status": "draft",
         "primary": stamp(root, args.file)["path"], "artifacts": artifacts,
         "bundle_sha256": canonical(artifacts), "input_sha256": inp,
         "checks": {}, "reviews": historical_reviews, "snapshot": []}
    stage["candidates"][args.candidate] = c
    append_event(run, "candidate_registered", stage=args.stage, candidate=args.candidate,
                 revision=rev, bundle_sha256=c["bundle_sha256"])
    return {"candidate": args.candidate, "revision": rev, "bundle_sha256": c["bundle_sha256"]}


def record_check(args, root, run):
    c = get_candidate(run, args.stage, args.candidate)
    if c["status"] != "draft":
        raise PipelineError("Checks may only change on a draft candidate.")
    require_current(root, run, args.stage, c)
    evidence = stamp(root, args.evidence)
    if evidence["bytes"] == 0 or evidence["path"] in {a["path"] for a in c["artifacts"]}:
        raise PipelineError("Use a separate, non-empty evidence file.")
    c["checks"][args.name] = {"status": args.status, "evidence": evidence,
                             "bundle_sha256": c["bundle_sha256"]}
    append_event(run, "check", stage=args.stage, candidate=args.candidate, name=args.name,
                 status=args.status, evidence=evidence)
    return {"check": args.name, "status": args.status}


def submit(args, root, run):
    c = get_candidate(run, args.stage, args.candidate)
    if c["status"] != "draft":
        raise PipelineError("Only draft candidates may be submitted.")
    errors = gate_errors(root, run, args.stage, c, reviews=False)
    if errors:
        raise PipelineError("; ".join(errors))
    dest = root / "checkpoints" / "submissions" / args.stage / args.candidate / f"r{c['revision']:04d}"
    if dest.exists():
        raise PipelineError("Snapshot already exists; never overwrite it.")
    copied = []
    try:
        for item in c["artifacts"]:
            src = root / item["path"]
            target = dest / item["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, target)
            copied.append({"path": target.relative_to(root).as_posix(), "sha256": digest(target),
                           "bytes": target.stat().st_size})
        if [x["sha256"] for x in copied] != [x["sha256"] for x in c["artifacts"]]:
            raise PipelineError("Artifact changed while snapshotting")
        atomic_json(dest / "submission.json", {"stage": args.stage, "candidate": c})
    except Exception:
        shutil.rmtree(dest, ignore_errors=True)
        raise
    c["snapshot"] = copied
    c["status"] = "awaiting_review"
    append_event(run, "submitted", stage=args.stage, candidate=args.candidate,
                 revision=c["revision"], bundle_sha256=c["bundle_sha256"])
    return {"status": "awaiting_review", "snapshot": str(dest),
            "notice": "Stop and ask the human to select or critique. Submission is not approval."}


def human_fields(args):
    if not args.actor.strip() or not args.statement.strip():
        raise PipelineError("Record the actual human identity and explicit approval statement.")
    return {"actor": args.actor, "statement": args.statement,
            "trust_boundary": "externally_observed_human_decision_not_authenticated_by_cli"}


def review(args, root, run):
    if args.stage != "09":
        raise PipelineError("Named internal reviews belong to stage 09.")
    c = get_candidate(run, args.stage, args.candidate)
    if c["status"] == "approved":
        raise PipelineError("Approved records are immutable.")
    require_current(root, run, args.stage, c)
    order = list(REVIEW_GATES)
    if args.gate not in order:
        raise PipelineError("Stage 09 supports audit and delivery reviews only.")
    if args.gate == "delivery":
        if c["status"] != "awaiting_review":
            raise PipelineError("Final delivery decision requires the submitted exact candidate.")
        errors = gate_errors(root, run, args.stage, c, reviews=False)
        if not c["snapshot"] or not all(verify_stamp(root, x) for x in c["snapshot"]):
            errors.append("Submission snapshot changed or is missing")
        if errors:
            raise PipelineError("; ".join(errors))
    for previous in order[:order.index(args.gate)]:
        if previous not in c["reviews"]:
            raise PipelineError(f"Human subgate required first: {previous}")
        if not verify_stamp(root, c["reviews"][previous]["evidence"]):
            raise PipelineError(f"Human subgate evidence changed: {previous}")
    record = {**human_fields(args), "time": now(), "bundle_sha256": c["bundle_sha256"],
              "revision": c["revision"], "evidence": stamp(root, args.evidence)}
    if not record["evidence"]["bytes"]:
        raise PipelineError("Review evidence is empty")
    c["reviews"][args.gate] = record
    for later in order[order.index(args.gate)+1:]:
        c["reviews"].pop(later, None)
    append_event(run, "human_subgate", stage=args.stage, candidate=args.candidate,
                 gate=args.gate, record=record)
    if args.gate == "delivery":
        # One observed final human decision also accepts stage 09; no extra prompt.
        result = approve(args, root, run)
        return {**result, "recorded": "delivery", "notice": record["trust_boundary"]}
    return {"recorded": args.gate, "notice": record["trust_boundary"]}


def approve(args, root, run):
    c = get_candidate(run, args.stage, args.candidate)
    if c["status"] != "awaiting_review":
        raise PipelineError("Only a submitted, reviewed candidate can be approved.")
    if run["stages"][args.stage]["approved"]:
        raise PipelineError("Stage already has an approved candidate.")
    errors = gate_errors(root, run, args.stage, c)
    if not c["snapshot"] or not all(verify_stamp(root, x) for x in c["snapshot"]):
        errors.append("Submission snapshot changed or is missing")
    if errors:
        raise PipelineError("; ".join(errors))
    c["approval"] = {**human_fields(args), "time": now(), "bundle_sha256": c["bundle_sha256"]}
    c["status"] = "approved"
    run["stages"][args.stage]["approved"] = args.candidate
    append_event(run, "human_approval", stage=args.stage, candidate=args.candidate, record=c["approval"])
    return {"approved": args.candidate, "stage": args.stage,
            "next_stage": f"{int(args.stage)+1:02d}" if args.stage != "09" else None}


def feedback(args, root, run):
    c = get_candidate(run, args.stage, args.candidate)
    if c["status"] == "approved":
        raise PipelineError("Cannot reopen an approved checkpoint; branch a new run.")
    if not args.statement.strip():
        raise PipelineError("Record the actual human critique")
    c["status"] = "draft"
    c["checks"] = {}
    c["reviews"] = {k: v for k, v in c["reviews"].items() if k == "audit"}
    append_event(run, "human_feedback", stage=args.stage, candidate=args.candidate,
                 statement=args.statement)
    return {"status": "draft", "notice": "Revise this candidate ID; keep the submitted snapshot."}


def attempt(args, root, run):
    if not ID.fullmatch(args.dependency):
        raise PipelineError("Use a simple dependency identifier")
    evidence = stamp(root, args.evidence)
    if not evidence["bytes"]:
        raise PipelineError("Attempt evidence is empty")
    attempts = run["dependency_attempts"].setdefault(args.dependency, [])
    if len(attempts) >= 10:
        raise PipelineError("Ten alternatives already recorded; escalate for human decision.")
    if any(a["method"].strip().casefold() == args.method.strip().casefold() for a in attempts):
        raise PipelineError("Duplicate method is not a new alternative attempt.")
    attempts.append({"number": len(attempts)+1, "method": args.method,
                     "outcome": args.outcome, "evidence": evidence, "time": now()})
    append_event(run, "dependency_attempt", dependency=args.dependency, attempt=attempts[-1])
    return {"dependency": args.dependency, "attempts": len(attempts),
            "exception_eligible_for_review": len(attempts) == 10 and all(a["outcome"] == "failed" for a in attempts),
            "notice": "Eligibility is not approval; disclose hyperspecific scope and ask the human."}


def status(root, run):
    return {"pack_version": run["pack_version"], "stages": {
        s: {"approved": st["approved"], "candidates": {
            cid: {"status": c["status"], "revision": c["revision"],
                  "gate_errors": gate_errors(root, run, s, c)} for cid, c in st["candidates"].items()}}
        for s, st in run["stages"].items()}}


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    subs = p.add_subparsers(dest="command", required=True)
    init = subs.add_parser("init", help="Create a run; do not modify source files")
    init.add_argument("workspace"); init.add_argument("--source", action="append", required=True)
    for name in ["status", "validate"]:
        q = subs.add_parser(name); q.add_argument("workspace")
    for name in ["candidate", "check", "submit", "approve", "feedback", "review"]:
        q = subs.add_parser(name)
        q.add_argument("workspace"); q.add_argument("stage", choices=STAGES); q.add_argument("candidate")
        if name == "candidate":
            q.add_argument("--file", required=True); q.add_argument("--asset", action="append", default=[])
        if name == "check":
            q.add_argument("--name", required=True); q.add_argument("--status", choices=["pass", "fail", "blocked"], required=True)
            q.add_argument("--evidence", required=True)
        if name in ("approve", "review"):
            q.add_argument("--actor", required=True); q.add_argument("--statement", required=True)
        if name == "feedback": q.add_argument("--statement", required=True)
        if name == "review":
            q.add_argument("--gate", choices=REVIEW_GATES, required=True)
            q.add_argument("--evidence", required=True)
    a = subs.add_parser("attempts")
    a.add_argument("workspace"); a.add_argument("dependency"); a.add_argument("--method", required=True)
    a.add_argument("--outcome", choices=["failed", "succeeded"], required=True); a.add_argument("--evidence", required=True)
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    root = Path(args.workspace).resolve()
    try:
        if args.command == "init":
            root.mkdir(parents=True, exist_ok=True)
        if not root.is_dir(): raise PipelineError("Workspace does not exist")
        with lock(root):
            if args.command == "init":
                result = init_run(args, root)
            else:
                run = load(root)
                if args.command in ("status", "validate"):
                    result = status(root, run)
                    if args.command == "validate":
                        stale = [f"{s}/{cid}" for s, st in run["stages"].items() for cid, c in st["candidates"].items()
                                 if live_bundle(root, c) != c["bundle_sha256"]]
                        if stale: raise PipelineError("Unregistered candidate changes: " + ", ".join(stale))
                        result = {"valid": True, "notice": "Ledger integrity only; draft/blocked stages are not production passes.", **result}
                else:
                    actions = {"candidate": register, "check": record_check, "submit": submit,
                               "approve": approve, "feedback": feedback, "review": review, "attempts": attempt}
                    result = actions[args.command](args, root, run)
                    atomic_json(root / "run.json", run)
        print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
        return 0
    except (PipelineError, OSError, KeyError, TypeError, ValueError) as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
