"""Convert inert runner.py JSONL records into `attempt` events plus content-addressed artifacts.

The runner's own fields blender_executed / blender_pass are deliberately NOT copied.
"""
import json
from pathlib import Path

from .ledger import LedgerError, fixture_hash, loads_strict, sha256_bytes
from .splits import enforce_case_split

STAGE_TASK = {"03": "geometry_weight_normalize", "04": "left_arm_ik",
              "05": "face_driver_setup", "06": "motion_tip_verify"}


def load_cases(path):
    out = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            c = loads_strict(line)
            out[c["case_id"]] = c
    return out


def fixture_bytes(case):
    """Canonical bytes stored as the fixture artifact; loading + fixture_hash() round-trips."""
    return json.dumps(case, sort_keys=True).encode()


def ingest_runner_jsonl(ledger, store, runner_jsonl, cases, *, experiment_id, lap_id, trial_id,
                        split="dev", role="target", model_tag=None, template_sha256=None,
                        reasoning_mode="not_recorded", seed=None, split_labels=None, final_selection_sha=None):
    """Append one attempt event per runner record. Returns the appended events."""
    appended = []
    for line in Path(runner_jsonl).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = loads_strict(line)
        case = cases.get(rec.get("case_id"))
        if case is None:
            raise LedgerError("runner record for unknown case " + str(rec.get("case_id")))
        if split_labels is not None:
            enforce_case_split([case], split_labels, split)
        fx = fixture_hash(case)
        if fx != rec.get("fixture_sha256"):
            raise LedgerError("fixture hash mismatch for " + case["case_id"])
        if rec.get("stage") not in STAGE_TASK:
            raise LedgerError("unsupported stage in runner record")
        store.put("fixtures", fixture_bytes(case), ".json")
        res = rec.get("result") or {}
        # Preserve exactly what the model emitted, including invalid JSON.
        # The parsed `code` field is not a substitute for raw-response bytes.
        raw_text, declared_hash = res.get("raw_response_text"), res.get("raw_response_sha256")
        if raw_text is not None:
            if not isinstance(raw_text, str) or len(raw_text.encode("utf-8")) > 2_000_000:
                raise LedgerError("invalid/oversized raw model output")
            raw_bytes = raw_text.encode("utf-8")
            if declared_hash != sha256_bytes(raw_bytes):
                raise LedgerError("raw response hash mismatch for " + case["case_id"])
            store.put("raw_outputs", raw_bytes, ".txt")
        elif declared_hash is not None:
            raise LedgerError("raw response hash claimed without the actual response bytes")
        code = res.get("code")
        cand = None
        if res.get("status") == "produced" and isinstance(code, str) and code.strip():
            cand = store.put("candidates", code.encode("utf-8"), ".py")
        dec = rec.get("decoding") or {}
        no = rec.get("attempt", 1)
        fields = {
            "attempt_id": "%s:%s:%s:%s:%d" % (experiment_id, lap_id, trial_id, case["case_id"], no),
            "lap_id": lap_id, "trial_id": trial_id, "attempt_no": no,
            "task_id": STAGE_TASK[rec["stage"]], "stage": rec["stage"], "case_id": case["case_id"],
            "source_family": rec.get("fixture_family") or case.get("fixture_family") or "unknown",
            "split": split, "role": role,
            "fixture_kind": "synthetic" if case.get("synthetic") else "real",
            "fixture_sha256": fx, "model_digest": rec["model_digest"],
            "prompt_sha256": rec["prompt_sha256"], "template_sha256": template_sha256,
            "raw_output_sha256": res.get("raw_response_sha256"), "candidate_sha256": cand,
            "generation_status": "produced" if res.get("status") == "produced" else "inference_error",
            "seed": seed, "temperature": dec.get("temperature", 0), "num_ctx": dec.get("num_ctx", 0),
            "reasoning_mode": reasoning_mode, "input_tokens": res.get("prompt_tokens"),
            "output_tokens": res.get("output_tokens"), "inference_seconds": res.get("elapsed_seconds"),
        }
        if model_tag:
            fields["model_tag"] = model_tag
        if final_selection_sha:
            fields["final_eval_selection_rule_sha256"] = final_selection_sha
        appended.append(ledger.append("attempt", "orchestrator", experiment_id, fields, artifacts=store))
    return appended
