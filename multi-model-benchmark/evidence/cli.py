"""Command line for the evidence pipeline. Run from multi-model-benchmark/:  python3 -m evidence.cli <cmd> ...

Data lives under the ignored multi-model-benchmark/data/<name>/ (ledger.jsonl + artifacts/).
Nothing here downloads or installs a model, image or asset.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys

from . import bridge, ingest, report, splits
from .ledger import ArtifactStore, Ledger, LedgerError, sha256_bytes

HERE = Path(__file__).resolve().parent
BENCH = HERE.parent
DATA = BENCH / "data"


def paths(name):
    base = (DATA / name).resolve()
    if not base.is_relative_to(DATA.resolve()) or name in ("", ".", ".."):
        raise LedgerError("data name must be a directory under multi-model-benchmark/data/")
    return Ledger(base / "ledger.jsonl"), ArtifactStore(base / "artifacts"), base


def branch_check():
    r = subprocess.run(["git", "branch", "--show-current"], cwd=BENCH, capture_output=True, text=True, timeout=10, check=True)
    if r.stdout.strip() != "Multi-Model-PMX-Benchmark":
        raise LedgerError("run only on the Multi-Model-PMX-Benchmark branch")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("lap", "ingest", "probe", "evaluate", "verify", "report", "decision"):
        s = sub.add_parser(name)
        s.add_argument("--data", required=True)
        if name in ("lap", "ingest", "evaluate", "report", "decision"):
            s.add_argument("--experiment", required=True)
        if name == "lap":
            s.add_argument("--lap-id", required=True)
            s.add_argument("--parent")
            s.add_argument("--task", required=True)
            s.add_argument("--reason", required=True)
            s.add_argument("--split-manifest", type=Path, required=True, help="file whose bytes are hashed into the lap")
            s.add_argument("--selection-rule", default=report.SELECTION_RULE)
            s.add_argument("--consulted", nargs="*", default=[])
            s.add_argument("--final-eval", action="store_true", help="final holdout child of selected validation lap")
            s.add_argument("--env", nargs="*", default=[], help="key=value pairs (os, ollama_version, ram_gb, ...)")
        if name == "ingest":
            s.add_argument("--lap-id", required=True)
            s.add_argument("--trial-id", required=True)
            s.add_argument("--runner-jsonl", type=Path, required=True)
            s.add_argument("--cases", type=Path, required=True)
            s.add_argument("--split", default="dev", choices=("dev", "validation", "holdout"))
            s.add_argument("--role", default="target", choices=("target", "canary"))
            s.add_argument("--model-tag")
            s.add_argument("--final", action="store_true", help="explicit final holdout release; requires final-eval child lap")
        if name in ("probe", "evaluate"):
            s.add_argument("--image", required=True, help="locally installed image pinned as name@sha256:...")
        if name == "evaluate":
            s.add_argument("--attempt-id")
        if name == "decision":
            s.add_argument("--kind", required=True, choices=("sol_light_review", "human_gate"))
            s.add_argument("--outcome", required=True, choices=("approved", "rejected", "changes_requested"))
            s.add_argument("--reviewer", required=True)
            s.add_argument("--scope", required=True, help="experiment|model_digest|task_id|selected_lap")
            s.add_argument("--review-file", type=Path, required=True)
        if name == "report":
            s.add_argument("--narrative", type=Path)
            s.add_argument("--out", type=Path, required=True)
            s.add_argument("--capability-out", type=Path)
    a = p.parse_args(argv)
    try:
        branch_check()
        ledger, store, base = paths(a.data)
        if a.cmd == "lap":
            env = dict(kv.split("=", 1) for kv in a.env)
            if a.final_eval and not a.parent:
                raise LedgerError("final holdout lap must identify an independently selected parent lap")
            raw_manifest = a.split_manifest.read_bytes()
            splits.parse_manifest(raw_manifest)  # validates family grouping before freezing
            pinned_manifest = store.put("split_manifests", raw_manifest, ".json")
            fields = {"lap_id": a.lap_id, "parent_lap_id": a.parent, "task_id": a.task, "change_reason": a.reason,
                      "selection_rule_sha256": sha256_bytes(a.selection_rule.encode()),
                      "split_manifest_sha256": pinned_manifest,
                      "cases_consulted_for_change": a.consulted, "selection_rule_id": "frozen-at-lap-0"}
            if env:
                fields["environment"] = env
            if a.final_eval:
                fields["holdout_final_eval"] = True
            print(json.dumps(ledger.append("lap", "controller", a.experiment, fields, artifacts=store)))
        elif a.cmd == "ingest":
            events = ledger.read()
            lap = next((x for x in events if x["event_type"] == "lap" and x["experiment_id"] == a.experiment
                        and x["lap_id"] == a.lap_id), None)
            if lap is None:
                raise LedgerError("unknown lap in experiment")
            labels = splits.parse_manifest(store.get("split_manifests", lap["split_manifest_sha256"], ".json"))
            if a.split == "holdout":
                if not a.final or not lap.get("holdout_final_eval") or not lap["parent_lap_id"]:
                    raise LedgerError("holdout requires --final and an explicit final-eval child lap")
                if not any(x["event_type"] == "attempt" and x["experiment_id"] == a.experiment
                           and x["lap_id"] == lap["parent_lap_id"] and x["split"] == "validation"
                           for x in events):
                    raise LedgerError("final holdout not authorized before parent validation evidence")
            elif a.final:
                raise LedgerError("--final is only applicable to holdout split")
            ev = ingest.ingest_runner_jsonl(ledger, store, a.runner_jsonl, ingest.load_cases(a.cases), experiment_id=a.experiment,
                                            lap_id=a.lap_id, trial_id=a.trial_id, split=a.split, role=a.role,
                                            model_tag=a.model_tag, split_labels=labels,
                                            final_selection_sha=lap["selection_rule_sha256"] if a.final else None)
            print("appended %d attempt events" % len(ev))
        elif a.cmd == "probe":
            pr = bridge.run_probe(a.image, forbidden_dirs=[base])
            print(json.dumps({"verified": pr.verified, "runtime_identity": pr.runtime_identity, "details": pr.details}, indent=2))
            return 0 if pr.verified else 3
        elif a.cmd == "evaluate":
            pr = bridge.run_probe(a.image, forbidden_dirs=[base])
            if not pr.verified:
                print("Sandbox isolation NOT verified; verdicts will be blocked. Details:", json.dumps(pr.details)[:300], file=sys.stderr)
            events = ledger.read()
            done = {e["attempt_id"] for e in events if e["event_type"] == "verdict"}
            todo = [e["attempt_id"] for e in events if e["event_type"] == "attempt" and e["experiment_id"] == a.experiment
                    and e["attempt_id"] not in done and (not a.attempt_id or e["attempt_id"] == a.attempt_id)]
            for aid in todo:
                v = bridge.evaluate_attempt(ledger, store, a.experiment, aid, image=a.image, probe=pr)
                print(aid, v["result"], v["failure_category"], v["severity"])
        elif a.cmd == "verify":
            errs = ledger.verify(store)
            print("VALID" if not errs else "INVALID:\n" + "\n".join(errs))
            return 0 if not errs else 2
        elif a.cmd == "decision":
            if not a.review_file.is_file() or a.review_file.is_symlink():
                raise LedgerError("review evidence must be an existing regular file")
            if len(a.scope.split("|")) != 4 or not a.scope.startswith(a.experiment + "|"):
                raise LedgerError("review scope must bind experiment, model digest, task, selected lap")
            evidence_bytes = a.review_file.read_bytes()
            if not evidence_bytes or len(evidence_bytes) > 2_000_000:
                raise LedgerError("review evidence empty or oversized")
            review_hash = store.put("reviews", evidence_bytes)
            fields = {"decision_kind": a.kind, "outcome": a.outcome,
                      "reviewer_id": a.reviewer, "review_evidence_sha256": review_hash,
                      "scope": a.scope}
            print(json.dumps(ledger.append("decision", "reviewer", a.experiment, fields, artifacts=store)))
        elif a.cmd == "report":
            narrative = json.loads(a.narrative.read_text(encoding="utf-8")) if a.narrative else None
            md, caps = report.generate(ledger.path, store.root, a.experiment, narrative)
            with a.out.open("x", encoding="utf-8") as f:
                f.write(md)
            if a.capability_out:
                with a.capability_out.open("x", encoding="utf-8") as f:
                    json.dump(caps, f, indent=2, sort_keys=True)
    except (LedgerError, report.ReportBlocked, OSError, ValueError, subprocess.CalledProcessError) as exc:
        print("STOP:", exc, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
