import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[1]
def load(name):
    spec = importlib.util.spec_from_file_location(name, BASE / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

worker = load("local_worker")
review = load("review")

class HelperTests(unittest.TestCase):
    def test_threshold(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "reviews"
            def row(i):
                return {"task_id": f"task-{i:03}", "status": "reviewer_repaired" if i == 0 else "passed_first_try",
                        "model": "qwen", "commit": "abc", "verification": "tests",
                        "reviewed_at": "2026-11-01", "repair_notes": "fixed"}
            self.assertFalse(review.summarize(p)["above_10_percent"])
            p.write_text("\n".join(json.dumps(row(i)) for i in range(10)))
            self.assertFalse(review.summarize(p)["above_10_percent"])
            p.write_text("\n".join(json.dumps(row(i)) for i in range(9)))
            self.assertTrue(review.summarize(p)["above_10_percent"])

    def test_protected_paths(self):
        for path in ("../../outside.py", "README.md", "skills/anime-blender-pipeline/scripts/pipeline.py"):
            with self.assertRaises(worker.Stop):
                worker.safe_path(path)

if __name__ == "__main__":
    unittest.main()
