#!/usr/bin/env python3
"""Evidence-based gate. Never promote a specialist from self-reported accuracy."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import specialists

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def validate(name, report):
    reg = specialists.registry()
    if name not in reg["specialists"]:
        raise ValueError("Unknown specialist")
    spec = reg["specialists"][name]
    policy = reg["qualification"]
    cases = report.get("cases")
    if not isinstance(cases, list) or len(cases) < policy["minimum_independent_holdout"]:
        raise ValueError("Too few independent held-out cases")
    ids = [case.get("case_id") for case in cases if isinstance(case, dict)]
    if len(ids) != len(cases) or any(not isinstance(i,str) or not i for i in ids) or len(set(ids)) != len(ids):
        raise ValueError("Invalid or repeated case IDs")
    failures = [c for c in cases if c.get("deterministic_pass") is not True or c.get("sol_light_pass") is not True]
    if len(failures) > policy["max_holdout_failures"]:
        raise ValueError("Holdout failures exceed threshold")
    if report.get("specialist") != name or report.get("model") != spec["model"]:
        raise ValueError("Mismatched model/specialist")
    if not report.get("independent_evaluator") or not report.get("reviewer_identity"):
        raise ValueError("Missing independent evaluation attribution")
    if not report.get("evaluation_commands") or not report.get("model_digest"):
        raise ValueError("Missing executed commands/model identity")
    train_path = Path(report["training_set"])
    holdout_path = Path(report["holdout_set"])
    if not train_path.is_file() or not holdout_path.is_file():
        raise ValueError("Training/holdout files not found")
    t_hash,h_hash=sha(train_path),sha(holdout_path)
    if t_hash == h_hash:
        raise ValueError("Holdout cannot equal training data")
    # Dataset separation requires matching content IDs, not merely unequal file hashes.
    def ids_from_jsonl(path):
        return {json.loads(line).get("case_id") for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}
    train_ids,holdout_ids=ids_from_jsonl(train_path),ids_from_jsonl(holdout_path)
    if None in train_ids or None in holdout_ids or train_ids & holdout_ids:
        raise ValueError("Train/evaluation examples overlap or have missing IDs")
    if set(ids) != holdout_ids:
        raise ValueError("Holdout report case IDs do not match held-out dataset")
    return {"specialist":name,"model":spec["model"],"passed_cases":len(cases),"failed_cases":0,
            "sol_light_reviewed":True,"model_digest":report["model_digest"],
            "training_set_sha256":t_hash,"holdout_set_sha256":h_hash,
            "evaluator":report["independent_evaluator"],
            "reviewer":report["reviewer_identity"],
            "note":"Evidence is self-contained but needs independent audit before marking qualified."}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--specialist",required=True)
    p.add_argument("--report",type=Path,required=True)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    try:
        result=validate(args.specialist,json.loads(args.report.read_text(encoding="utf-8")))
        # Deliberately does not set qualified=true. An agent must audit and
        # explicitly promote the exact model digest after an independent review.
        print(json.dumps(result,indent=2))
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=True)
            args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    except (ValueError,OSError,KeyError,TypeError,json.JSONDecodeError) as exc:
        print("NOT QUALIFIED:",exc,file=sys.stderr)
        return 2
    return 0

if __name__=="__main__":
    raise SystemExit(main())
