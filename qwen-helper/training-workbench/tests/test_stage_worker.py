import importlib.util
import json
from pathlib import Path
from unittest import mock
import tempfile
import unittest
import sys

HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
import install
import stage_worker

def stage_task(stage="03",specialist="geometry_builder",demo=True):
    key="geometry-synthetic-001"
    return {"task_id":key,"stage":stage,"specialist":specialist,
            "kind":"stage_candidate","scope":"character_specific",
            "fixture_only":demo,
            "objective":"Check synthetic morphology",
            "expected_behavior":"One safe standalone Blender script",
            "constraints":"No production assets",
            "character_profile_summary":"Synthetic fixtures only",
            "accepted_input_path":None,"accepted_input_sha256":None,
            "target":f"qwen-helper/training-workbench/data/candidates/{key}/candidate.py"}

class SetupTests(unittest.TestCase):
    def test_existing_tag_selection(self):
        models={"qwen2.5-coder:7b":"abc","other:latest":"def"}
        self.assertEqual(install.choose(models,preferred="qwen2.5-coder:7b"),"qwen2.5-coder:7b")
        self.assertEqual(install.choose(models),"qwen2.5-coder:7b")
    def test_ambiguous_or_uninstalled_model(self):
        models={"qwen-coder:a":"1","qwen-coder:b":"2"}
        with self.assertRaises(install.InstallError):install.choose(models)
        with self.assertRaises(install.InstallError):install.choose(models,explicit="missing")
    def test_stage00_unconditionally_blocked(self):
        with self.assertRaises(stage_worker.Stop):
            stage_worker.qualify_task(stage_task("00","geometry_builder"),demo=True)
    def test_stage_mapping_boundaries(self):
        t=stage_task("04","geometry_builder")
        with self.assertRaises(stage_worker.Stop):
            stage_worker.qualify_task(t,demo=True)
        for stage,name in [("03","geometry_builder"),("04","rig_builder"),
                           ("05","animator_builder"),("06","animation_qualifier")]:
            self.assertEqual(stage_worker.qualify_task(stage_task(stage,name),demo=True)["stage"],stage)
    def test_demo_never_approves_production(self):
        t=stage_task()
        with self.assertRaises(stage_worker.Stop):stage_worker.qualify_task(t,demo=False)
        result=stage_worker.plan(t,demo=True)
        self.assertIn(result["route"],("local_qwen_one_attempt","original_codex_pipeline"))
        if result["route"]=="local_qwen_one_attempt":
            self.assertEqual(result["mode"],"synthetic_proposal_only")
    def test_qualified_stage_gates_remain_off(self):
        from pathlib import Path
        import json
        reg=json.loads((stage_worker.ROOT/"qwen-helper"/"specialists.json").read_text())
        for key in ("geometry_builder","rig_builder","animator_builder","animation_qualifier"):
            self.assertFalse(reg["specialists"][key]["qualified"])
    def test_wrong_branch_falls_back(self):
        with mock.patch.object(stage_worker,"verify_branch",side_effect=stage_worker.Stop("main forbidden")):
            self.assertEqual(stage_worker.plan(stage_task(),demo=True)["route"],"original_codex_pipeline")
    def test_runtime_file_pin(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"runtime.json"
            path.write_text(json.dumps({"schema_version":1,"model":"qwen:existing","digest":"sha"}))
            with mock.patch.object(stage_worker,"DATA",Path(tmp)):
                self.assertEqual(stage_worker.read_runtime()["model"],"qwen:existing")

if __name__=="__main__":unittest.main()
