#!/usr/bin/env python3
"""Small opt-in persistent attempt journal. No project approval authority."""
import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import sys
import tempfile

OUTCOMES = ("improved", "rejected", "inconclusive", "harness-failure", "environment-failure", "diagnosis")

@contextmanager
def locked(path):
    lock = path.with_name(path.name + ".lock")
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        os.close(fd)
        yield
    finally:
        lock.unlink()

def save(path, data):
    fd, tmp = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=True)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

def initial(run, stage, issue):
    limits = dict(run=run, stage=stage, issue=issue)
    if any(type(v) is not int or v <= 0 for v in limits.values()):
        raise ValueError("All limits must be positive integers")
    return {"schema": 1, "limits": limits, "attempts": []}

def reserve(data, issue, stage, kind, evidence):
    if not all(isinstance(v, str) and v.strip() for v in (issue, stage, evidence)):
        raise ValueError("Issue, stage and evidence must be nonempty")
    if kind not in ("implementation", "diagnosis"):
        raise ValueError("Unknown attempt kind")
    attempts = data["attempts"]
    if any(a["outcome"] is None for a in attempts):
        raise ValueError("Resolve the pending reservation first")
    if any(evidence in (a["hypothesis"], a.get("result")) for a in attempts):
        raise ValueError("New distinguishing evidence required")
    prior = [a for a in attempts if a["issue"] == issue]
    counts = (len(attempts), sum(a["stage"] == stage for a in attempts), len(prior))
    for key, count in zip(("run", "stage", "issue"), counts):
        if count >= data["limits"][key]:
            raise ValueError(key + " budget exhausted; escalate")
    failures = 0
    last_failure = -1
    for i, a in enumerate(prior):
        if a["kind"] == "implementation":
            if a["outcome"] == "improved":
                failures = 0
                last_failure = -1
            else:
                failures += 1
                last_failure = i
    if failures >= 3:
        raise ValueError("Three non-improvements; escalate")
    if kind == "implementation" and failures >= 2 and not any(
        a["kind"] == "diagnosis" and a["outcome"] == "diagnosis" for a in prior[last_failure+1:]
    ):
        raise ValueError("Rollback and finish renewed diagnosis before implementation")
    entry = dict(id=len(attempts)+1, issue=issue, stage=stage, kind=kind,
                 hypothesis=evidence, outcome=None, result=None)
    attempts.append(entry)
    return entry

def finish(data, attempt, outcome, evidence):
    if not isinstance(evidence, str) or not evidence.strip():
        raise ValueError("Result evidence required")
    if outcome not in OUTCOMES:
        raise ValueError("Unknown outcome")
    a = next((a for a in data["attempts"] if a["id"] == attempt), None)
    if a is None or a["outcome"] is not None:
        raise ValueError("Unknown or already finished reservation")
    if (outcome == "diagnosis") != (a["kind"] == "diagnosis") and outcome not in ("inconclusive", "harness-failure", "environment-failure"):
        raise ValueError("Outcome incompatible with attempt kind")
    if any(evidence in (x["hypothesis"], x.get("result")) for x in data["attempts"]):
        raise ValueError("Distinct result evidence required")
    a.update(outcome=outcome, result=evidence)
    return a

def context(agents, resume):
    sizes = {"agents": Path(agents).stat().st_size, "resume": Path(resume).stat().st_size}
    return {"bytes": sizes, "within_budget": sizes["agents"] <= 8000 and sizes["resume"] <= 12000}

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("init", "reserve", "finish", "status"):
        q = sub.add_parser(name)
        q.add_argument("journal", type=Path)
        if name == "init":
            for key in ("run", "stage", "issue"):
                q.add_argument("--"+key, type=int, required=True)
        elif name == "reserve":
            for key in ("issue", "stage", "evidence"):
                q.add_argument("--"+key, required=True)
            q.add_argument("--kind", choices=("implementation", "diagnosis"), required=True)
        elif name == "finish":
            q.add_argument("--attempt", type=int, required=True)
            q.add_argument("--outcome", choices=OUTCOMES, required=True)
            q.add_argument("--evidence", required=True)
    q = sub.add_parser("context")
    q.add_argument("agents")
    q.add_argument("resume")
    a = p.parse_args(argv)
    try:
        if a.cmd == "context":
            result = context(a.agents, a.resume)
            print(json.dumps(result))
            return 0 if result["within_budget"] else 2
        path = a.journal.resolve()
        with locked(path):
            if a.cmd == "init":
                if path.exists():
                    raise ValueError("Journal already exists; do not reset")
                data = initial(a.run, a.stage, a.issue)
                result = data
            else:
                data = json.loads(path.read_text(encoding="utf-8"))
                if data.get("schema") != 1:
                    raise ValueError("Unsupported journal schema")
                if a.cmd == "reserve":
                    result = reserve(data, a.issue, a.stage, a.kind, a.evidence)
                elif a.cmd == "finish":
                    result = finish(data, a.attempt, a.outcome, a.evidence)
                else:
                    result = data
            if a.cmd != "status":
                save(path, data)
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
