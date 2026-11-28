import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("budget", Path(__file__).parents[1] / "scripts/budget.py")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)

class BudgetTests(unittest.TestCase):
    def setUp(self):
        self.data = b.initial(10, 8, 5)

    def attempt(self, issue="x", stage="08", kind="implementation", outcome="rejected"):
        n = len(self.data["attempts"]) + 1
        a = b.reserve(self.data, issue, stage, kind, "h"+str(n))
        b.finish(self.data, a["id"], outcome, "r"+str(n))

    def test_rejected_loop(self):
        self.attempt()
        self.attempt()
        with self.assertRaises(ValueError):
            b.reserve(self.data, "x", "09", "implementation", "h3")
        self.attempt(stage="09", kind="diagnosis", outcome="diagnosis")
        self.attempt(stage="09")
        with self.assertRaises(ValueError):
            b.reserve(self.data, "x", "08", "diagnosis", "h5")

    def test_issue_budget_follows_stage(self):
        self.data = b.initial(9, 9, 1)
        self.attempt(outcome="improved")
        with self.assertRaises(ValueError):
            b.reserve(self.data, "x", "09", "implementation", "new")

    def test_stage_and_run_budget(self):
        self.data = b.initial(2, 1, 3)
        self.attempt()
        with self.assertRaises(ValueError):
            b.reserve(self.data, "y", "08", "implementation", "new")
        self.attempt(issue="y", stage="09")
        with self.assertRaises(ValueError):
            b.reserve(self.data, "z", "07", "implementation", "new")

    def test_pending_and_duplicate(self):
        b.reserve(self.data, "x", "08", "implementation", "h1")
        with self.assertRaises(ValueError):
            b.reserve(self.data, "y", "09", "implementation", "h2")
        b.finish(self.data, 1, "harness-failure", "r1")
        with self.assertRaises(ValueError):
            b.reserve(self.data, "y", "09", "implementation", "h1")

    def test_disk_persistence(self):
        with tempfile.TemporaryDirectory() as d:
            path = str(Path(d)/"budget.json")
            self.assertEqual(b.main(["init", path, "--run", "2", "--stage", "2", "--issue", "2"]), 0)
            self.assertEqual(b.main(["reserve", path, "--issue", "x", "--stage", "08", "--kind", "implementation", "--evidence", "h1"]), 0)
            self.assertEqual(b.main(["init", path, "--run", "2", "--stage", "2", "--issue", "2"]), 2)
            self.assertEqual(b.main(["reserve", path, "--issue", "y", "--stage", "09", "--kind", "implementation", "--evidence", "h2"]), 2)
            self.assertEqual(b.main(["finish", path, "--attempt", "1", "--outcome", "rejected", "--evidence", "r1"]), 0)

    def test_failed_diagnosis_cannot_repeat(self):
        self.attempt()
        self.attempt()
        self.attempt(kind="diagnosis", outcome="inconclusive")
        for kind in ("diagnosis", "implementation"):
            with self.assertRaises(ValueError):
                b.reserve(self.data, "x", "08", kind, "new")

    def test_telemetry_kept_separate(self):
        a = b.reserve(self.data, "x", "08", "implementation", "h1")
        with self.assertRaises(ValueError):
            b.finish(self.data, a["id"], "rejected", "r1", tokens=42)
        b.finish(self.data, a["id"], "rejected", "r1", seconds=10, tokens=42, usage_source="estimated")
        a = b.reserve(self.data, "y", "09", "implementation", "h2")
        b.finish(self.data, a["id"], "improved", "r2", tokens=20, usage_source="measured")
        r = b.report(self.data)
        self.assertEqual(r["run"]["estimated_tokens"], 42)
        self.assertEqual(r["run"]["measured_tokens"], 20)
        self.assertEqual(r["run"]["seconds_coverage"], 1)
        self.assertEqual(r["remaining_run"], 8)

    def test_context_limits(self):
        with tempfile.TemporaryDirectory() as d:
            a, r = Path(d)/"a", Path(d)/"r"
            a.write_bytes(b"x"*8000)
            r.write_bytes(b"x"*12000)
            self.assertTrue(b.context(a,r)["within_budget"])
            a.write_bytes(b"x"*8001)
            self.assertFalse(b.context(a,r)["within_budget"])

if __name__ == "__main__":
    unittest.main()
