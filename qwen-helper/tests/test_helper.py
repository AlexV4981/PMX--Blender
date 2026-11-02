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
    def test_generic_and_character_boundaries(self):
        cfg={"allow_paths":["skills/anime-blender-pipeline/scripts"],
             "extensions":[".py"],"deny_paths":[],"limits":{}}
        valid={"task_id":"generic-001","kind":"new_tool","scope":"generic",
               "objective":"Create a read-only audit summarizer",
               "expected_behavior":"Input lists are summarized with counts",
               "target":"skills/anime-blender-pipeline/scripts/qwen_audit_summary.py",
               "references":[]}
        import unittest.mock
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"task.json"
            p.write_text(json.dumps(valid))
            task,target,_=worker.load_task(p,cfg)
            self.assertEqual(task["scope"],"generic")
            bad=dict(valid,scope="character_specific")
            p.write_text(json.dumps(bad))
            with self.assertRaises(worker.Stop):worker.load_task(p,cfg)
            per_char=dict(bad,target="skills/anime-blender-pipeline/scripts/qwen_character_accessory.py",
                          character_id="sample",character_requirements="Extra accessory uses given map",
                          generic_baseline="All unmodified characters use standard defaults")
            p.write_text(json.dumps(per_char))
            self.assertEqual(worker.load_task(p,cfg)[0]["scope"],"character_specific")
            leaky=dict(valid,character_id="sample")
            p.write_text(json.dumps(leaky))
            with self.assertRaises(worker.Stop):worker.load_task(p,cfg)
            overwrite=dict(valid,target="skills/anime-blender-pipeline/scripts/texture_audit.py")
            p.write_text(json.dumps(overwrite))
            with self.assertRaises(worker.Stop):worker.load_task(p,cfg)

    def test_pmx_specific_setup(self):
        cfg=setup.pmx_defaults()
        self.assertEqual(cfg["project_type"], "pmx-to-native-blender")
        self.assertEqual(cfg["extensions"], [".py"])
        self.assertEqual(cfg["allow_paths"], ["skills/anime-blender-pipeline/scripts"])
        self.assertIn("skills/anime-blender-pipeline/scripts/pipeline.py",cfg["deny_paths"])
        self.assertEqual(len(cfg["checks"]), 2)
        self.assertTrue(setup.is_pmx_project(worker.ROOT))
        with tempfile.TemporaryDirectory() as d:
            self.assertFalse(setup.is_pmx_project(Path(d)))
if __name__=="__main__":unittest.main()
