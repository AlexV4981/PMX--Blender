import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
BASE = Path(__file__).resolve().parents[1]
def load(name):
    spec=importlib.util.spec_from_file_location(name,BASE/(name+".py"))
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
worker=load("local_worker")
review=load("review")
setup=load("setup")
class HelperTests(unittest.TestCase):
    def test_threshold(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"ledger"
            def record(i):
                return {"task_id":f"task-{i:03}","status":"reviewer_repaired" if i==0 else "passed_first_try","model":"qwen","commit":"abc","verification":"tests","reviewed_at":"2026-11-02","repair_notes":"fixed"}
            self.assertFalse(review.summarize(path)["above_10_percent"])
            path.write_text("\n".join(json.dumps(record(i)) for i in range(10)))
            self.assertFalse(review.summarize(path)["above_10_percent"])
            path.write_text("\n".join(json.dumps(record(i)) for i in range(9)))
            self.assertTrue(review.summarize(path)["above_10_percent"])
    def test_gate(self):
        cfg={"allow_paths":["skills/anime-blender-pipeline/scripts"],"extensions":[".py"],"deny_paths":["skills/anime-blender-pipeline/scripts/pipeline.py"]}
        for path in ("../../outside.py",".github/anything.py","qwen-helper/local_worker.py","skills/anime-blender-pipeline/scripts/pipeline.py"):
            with self.assertRaises(worker.Stop):worker.safe_path(path,cfg)
        self.assertTrue(worker.safe_path("skills/anime-blender-pipeline/scripts/texture_audit.py",cfg).is_file())
    def test_detection(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(setup.detect_checks(Path(d)),[])
            (Path(d)/"go.mod").write_text("module example")
            self.assertEqual(setup.detect_checks(Path(d)),[["go","test","./..."]])
if __name__=="__main__":unittest.main()
