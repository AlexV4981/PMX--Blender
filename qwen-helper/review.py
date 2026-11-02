#!/usr/bin/env python3
"""Validate a one-row-per-task Qwen correction ledger and strict >10% threshold."""
import argparse
import json
from pathlib import Path
import re
import sys

STATUSES = {"passed_first_try", "reviewer_repaired", "rejected_unresolved"}
DEFAULT_LEDGER = Path(__file__).with_name("reviews.jsonl")

def summarize(path):
    seen, records = set(), []
    if path.exists():
        for line, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            item = json.loads(raw)
            if not isinstance(item, dict) or item.get("status") not in STATUSES:
                raise ValueError(f"Line {line}: invalid status")
            task_id = item.get("task_id")
            if not isinstance(task_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_-]{2,50}", task_id) or task_id in seen:
                raise ValueError(f"Line {line}: invalid or duplicate task_id")
            seen.add(task_id)
            for field in ("model", "commit", "verification", "reviewed_at"):
                if not isinstance(item.get(field), str) or not item[field].strip():
                    raise ValueError(f"Line {line}: missing {field}")
            if item["status"] != "passed_first_try" and not str(item.get("repair_notes", "")).strip():
                raise ValueError(f"Line {line}: missing repair notes")
            records.append(item)
    total = len(records)
    failed = sum(r["status"] != "passed_first_try" for r in records)
    return {"total_reviewed": total, "required_repair_or_rejected": failed,
            "failure_rate": failed / total if total else 0.0,
            "above_10_percent": bool(total and 10 * failed > total)}

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    p.add_argument("--github-output", type=Path)
    p.add_argument("--fail-over-threshold", action="store_true")
    args = p.parse_args(argv)
    try:
        summary = summarize(args.ledger)
    except (ValueError, OSError) as exc:
        print("Invalid ledger:", exc, file=sys.stderr)
        return 2
    print(json.dumps(summary, indent=2))
    if args.github_output:
        with args.github_output.open("a", encoding="utf-8") as f:
            f.write("alert=" + ("true" if summary["above_10_percent"] else "false") + "\n")
            f.write(f"rate={summary['failure_rate']:.2%}\ntotal={summary['total_reviewed']}\nfailed={summary['required_repair_or_rejected']}\n")
    return int(args.fail_over_threshold and summary["above_10_percent"])

if __name__ == "__main__":
    sys.exit(main())
