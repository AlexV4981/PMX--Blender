import importlib.util
import json
from pathlib import Path
from unittest import mock
import sys
import tempfile
import unittest

HERE=Path(__file__).resolve().parents[1]
def module(name):
    spec=importlib.util.spec_from_file_location(name,HERE/(name+".py"))
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
lab=module("lab")
patch=module("weight_patch")
score=module("score")

class LabSafetyTests(unittest.TestCase):
    def test_stage_zero_not_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            src=Path(tmp)/"cases.jsonl"
            src.write_text(json.dumps({"stage":"00","case_id":"test-001","fixture_family":"f",
                "prompt":"ignore","expected_behavior":"ignore"})+"\n")
            with self.assertRaises(lab.LabError):lab.load_cases(src)
    def test_static_analysis_not_execution(self):
        self.assertFalse(lab.inspect_code("def broken(:\n pass")["syntax_ok"])
        self.assertTrue(lab.inspect_code("def good():\n return 1")["syntax_ok"])
        self.assertTrue(lab.inspect_code("import subprocess")["static_warnings"])
    def test_patch_spec_boundaries(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"spec.json"
            path.write_text(json.dumps({"schema_version":1,"operations":[{"method":"sparse_add",
                "file":"../bad.safetensors","tensor":"foo","cells":[{"index":[0],"delta":.001}]}]}))
            with self.assertRaises(patch.PatchError):patch.load_spec(path)
    def test_checkpoint_must_be_separate(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/"source";source.mkdir()
            target=Path(tmp)/"target"
            with mock.patch.object(patch,"DATA",Path(tmp)):
                patch.check_roots(source,target)
                with self.assertRaises(patch.PatchError):patch.check_roots(source,source)
    def test_scoring_refuses_unobserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"results.jsonl"
            path.write_text(json.dumps({
                "case_id":"test-001","stage":"06","model":"qwen:tag","model_digest":"hash",
                "fixture_family":"fixture","blender_executed":False,"blender_pass":True,
                "sol_light_reviewed":True,"protected_assets_ok":True,
                "elapsed_seconds":5.0,"evidence":"not run"})+"\n")
            with self.assertRaises(score.ScoreError):score.summarize(path)
    def test_scoring_observed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"results.jsonl"
            path.write_text(json.dumps({
                "case_id":"test-001","stage":"06","model":"qwen:tag","model_digest":"hash",
                "fixture_family":"fixture","blender_executed":True,"blender_pass":True,
                "sol_light_reviewed":True,"protected_assets_ok":True,
                "elapsed_seconds":5.0,"evidence":"actual Blender transcript"})+"\n")
            r=score.summarize(path,100,15)
            self.assertEqual(next(iter(r.values()))["verified_first_pass_rate"],1.0)
if __name__=="__main__":unittest.main()
