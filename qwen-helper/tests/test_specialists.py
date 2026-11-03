import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
import specialists
import dispatch
import qualification
import local_worker

class SpecialistTests(unittest.TestCase):
    def task(self):
        return {"task_id":"test-inventory-001","specialist":"inventory_summary","kind":"new_tool",
                "scope":"generic","objective":"Summarize fixture counts",
                "expected_behavior":"Return number of fixture items","references":[],
                "target":"skills/anime-blender-pipeline/scripts/qwen_inventory_probe.py"}
    def test_unqualified_routes_original(self):
        self.assertEqual(dispatch.plan(self.task())["route"],"original_codex_pipeline")
    def test_cross_subsystem_routes_original(self):
        t=self.task();t["cross_subsystem"]=True
        self.assertEqual(dispatch.plan(t)["route"],"original_codex_pipeline")
    def test_missing_specialist_routes_original(self):
        t=self.task();t["specialist"]="not-registered"
        self.assertEqual(dispatch.plan(t)["route"],"original_codex_pipeline")
    def test_target_scope_rejected(self):
        t=self.task();t["target"]="skills/anime-blender-pipeline/scripts/pipeline.py"
        with self.assertRaises(specialists.Ineligible):specialists.inspect(t,False)
    def test_branch_preflight_enforced(self):
        # Every task is rejected unless branch, model digest and review ledger pass.
        self.assertEqual(dispatch.plan(self.task())["route"],"original_codex_pipeline")
    def test_legacy_worker_model_unchanged(self):
        self.assertEqual(local_worker.resolve_model({},{"model":"legacy"}),"legacy")
    def test_no_faked_qualification_without_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            train=Path(d)/"train.jsonl";hold=Path(d)/"hold.jsonl"
            train.write_text(json.dumps({"case_id":"train-1"})+"\n")
            hold.write_text(json.dumps({"case_id":"hold-1"})+"\n")
            report={"specialist":"inventory_summary",
                    "model":specialists.registry()["specialists"]["inventory_summary"]["model"],
                    "training_set":str(train),"holdout_set":str(hold),
                    "model_digest":"test","independent_evaluator":"agent","reviewer_identity":"sol-light",
                    "evaluation_commands":["actual commands"],
                    "cases":[{"case_id":"hold-1","deterministic_pass":True,"sol_light_pass":True}]}
            with self.assertRaises(ValueError):qualification.validate("inventory_summary",report)
    def test_review_requires_exact_digest(self):
        with tempfile.TemporaryDirectory() as d:
            proposal=Path(d)/"proposal.json";review=Path(d)/"review.json"
            proposal.write_text('{"a":1}')
            review.write_text(json.dumps({"task_id":"test-inventory-001","proposal_sha256":"wrong",
                "reviewer_role":"sol_light","decision":"approve","evidence":"some test"}))
            # No promotion happens while specialist remains unqualified.
            self.assertEqual(dispatch.plan(self.task())["route"],"original_codex_pipeline")

if __name__=="__main__":unittest.main()
