"""No-Ollama, no-Blender safety tests for the proposal runner."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

PATH = Path(__file__).resolve().parents[1] / "runner.py"
spec = importlib.util.spec_from_file_location("multi_model_runner", PATH)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

class RunnerSafetyTests(unittest.TestCase):
    def test_python_syntax_does_not_mean_blender_pass(self):
        result = runner.syntax("def solve(scene):\n    return {'ok': True}\n")
        self.assertTrue(result["valid"])
        self.assertFalse(result["blender_executed"])
    def test_disallowed_import_flagged(self):
        result = runner.syntax("import subprocess\ndef solve(scene):\n    return {}\n")
        self.assertIn("disallowed import: subprocess", result["warnings"])
    def test_missing_solve_flagged(self):
        self.assertIn("missing solve(scene)", runner.syntax("x = 1")["warnings"])
    def test_stage04_prompt_explicit(self):
        case = {"prompt":"move arm", "expected_behavior":"pose preserved"}
        text = runner.prompt(case, "04", False)
        self.assertIn("LEFT-ARM PILOT ONLY", text)
        self.assertIn("do not create pole targets", text)
    def test_stage06_no_modify(self):
        case = {"prompt":"test walk", "expected_behavior":"observe only"}
        self.assertIn("NEVER modify the accepted rig", runner.prompt(case, "06", False))
    def test_requires_exactly_twenty_cases(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "cases.jsonl"
            path.write_text(json.dumps({"stage":"03","case_id":"a","prompt":"x","params":{}})+"\n")
            with self.assertRaises(runner.Stop):
                runner.load_cases(path,"03")
    def test_model_tags_restricted(self):
        self.assertFalse(runner.TAG.fullmatch("x;rm -rf"))
        self.assertTrue(runner.TAG.fullmatch("qwen3.5:9b"))

if __name__ == "__main__":
    unittest.main()
