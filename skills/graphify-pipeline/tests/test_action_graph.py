"""Action graph routing, frozen checks and stale source detection."""
import importlib.util
import pathlib
import sys
import tempfile
import unittest

DIR = pathlib.Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(DIR))
import action_graph

spec = importlib.util.spec_from_file_location(
    "base_graphify_tests", pathlib.Path(__file__).with_name("test_graphify.py"))
fixture_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture_module)


def setup(root):
    fixture_module.GraphifyTests().fixture(root)
    for i in range(10):
        path = root / "skills" / f"anime-blender-{i:02d}-fixture" / "references/stage.md"
        path.write_text("## 1. Perform source-derived task\n\nInspect actual evidence.\n"
                        "## Evidence\n\nOriginal exact requirements.\n", encoding="utf-8")
    path = root / "skills/anime-blender-pipeline/references/diagnosis.md"
    rows = [
        "| Symptom | Plausible causes | First useful tests | Unjustified compensation |",
        "| --- | --- | --- | --- |",
    ]
    rows += [f"| Fault {i} | Unconfirmed cause | Isolated test {i} | Blind fix |"
             for i in range(9)]
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


class ActionTests(unittest.TestCase):
    def test_action_and_return(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            setup(root)
            data = action_graph.make_graph(root)
            self.assertEqual(len(data["stages"]), 10)
            self.assertTrue(all(s["tasks"] for s in data["stages"]))
            self.assertEqual(data["stages"][9]["sequence"][1], "gate:09:audit")
            self.assertEqual(data["stages"][9]["sequence"][-1], "gate:09:delivery")
            self.assertIn("required:04:check-04", data["stages"][4]["sequence"])
            edges = data["edges"]
            self.assertTrue(any(e["source"] == "retest1:task:04:1" and
                                e["target"] == "qc:task:04:1" for e in edges))
            self.assertTrue(any(e["source"] == "retest2:task:04:1" and
                                e["target"] == "qc:task:04:1" for e in edges))
            self.assertTrue(any(e["condition"] == "two_consecutive_non_improving_attempts"
                                for e in edges))

    def test_stale_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            setup(root)
            out = root / "generated"
            action_graph.build_files(root, out)
            self.assertTrue(action_graph.verify_files(root, out))
            path = root / "skills/anime-blender-04-fixture/references/stage.md"
            path.write_text("## 1. Updated task\n\nNew information.\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Stale"):
                action_graph.verify_files(root, out)


if __name__ == "__main__":
    unittest.main()
