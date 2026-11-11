"""Checks that graph generation preserves frozen gate names and catches drift."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("graphify", Path(__file__).resolve().parents[1] / "scripts/graphify.py")
graphify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(graphify)


class GraphifyTests(unittest.TestCase):
    def fixture(self, root):
        pack = root / "skills/anime-blender-pipeline"
        stages = {}
        for i in range(10):
            sid = f"{i:02d}"
            stages[sid] = {"required_checks": ["check-" + sid, "evidence-" + sid]}
            stage = root / "skills" / ("anime-blender-" + sid + "-fixture")
            (stage / "references").mkdir(parents=True)
            (stage / "SKILL.md").write_text("# " + sid + " — Sample\n")
            (stage / "references/stage.md").write_text("Evidence definitions\n")
        (pack / "assets").mkdir(parents=True)
        (pack / "references").mkdir(parents=True)
        (pack / "assets/stage-policy.json").write_text(json.dumps({
            "pack_version": "3.0.0", "candidate_limit": 3,
            "stage09_human_reviews": ["audit", "delivery"], "stages": stages
        }))
        for suffix in graphify.SHARED:
            path = pack / suffix
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("Original document\n")
        (pack / "references/roles.md").write_text(
            "| Role | Requested selection | Responsibility |\n"
            "| --- | --- | --- |\n"
            "| Routine worker | gpt-6.1-sol / low | Apply recipes |\n")

    def test_exact_checks_and_stage09(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            graph = graphify.build_graph(root)
            self.assertEqual(len(graph["stages"]), 10)
            self.assertEqual(graph["stages"][2]["required_checks"], ["check-02", "evidence-02"])
            self.assertEqual(graph["stages"][9]["human_gates"], ["audit", "delivery"])
            self.assertEqual(sum(n["type"] == "required_check" for n in graph["nodes"]), 20)
            self.assertTrue(graphify.verify(graph, json.loads(json.dumps(graph))))

    def test_source_change_invalidates_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            old = graphify.build_graph(root)
            (root / old["stages"][4]["procedure"]).write_text("Changed\n")
            with self.assertRaisesRegex(ValueError, "Stale graph"):
                graphify.verify(graphify.build_graph(root), old)


if __name__ == "__main__":
    unittest.main()
