"""Tests for frozen, group-disjoint training splits without any GPU requirements."""
import importlib.util
import json
from pathlib import Path
import tempfile
from unittest import mock
import unittest

SOURCE=Path(__file__).resolve().parents[1]/"workbench.py"
SPEC=importlib.util.spec_from_file_location("workbench",SOURCE)
workbench=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(workbench)

def row(i, group):
    return {"case_id":f"example-{i:03}","group_id":group,
            "source_type":"deterministic_fixture","provenance":"synthetic test",
            "verified_by":"deterministic unit test","verification":"unit test result",
            "prompt":"Count checked input items","completion":"return 1"}

class WorkbenchTests(unittest.TestCase):
    def test_stage_order(self):
        s=workbench.tracks()
        self.assertEqual([x["stage"] for x in s],[f"{i:02d}" for i in range(10)])
        self.assertEqual(s[8]["specialist"],None)
        self.assertEqual(s[9]["specialist"],None)
    def test_group_isolation(self):
        examples=[row(i,f"family-{i//4}") for i in range(60)]
        output=workbench.group_partition(examples)
        self.assertEqual(sum(map(len,output.values())),len(examples))
        a=[{r["group_id"] for r in output[k]} for k in workbench.SPLITS]
        self.assertFalse(a[0]&a[1] or a[0]&a[2] or a[1]&a[2])
    def test_small_groups_blocked(self):
        with self.assertRaises(workbench.Stop):
            workbench.group_partition([row(i,"same-family") for i in range(60)])
    def test_fake_verification_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"bad.jsonl"
            x=row(0,"family");x["verification"]="FILL_WITH_TEST"
            p.write_text(json.dumps(x)+"\n")
            with self.assertRaises(workbench.Stop):workbench.load_raw(p)
    def test_prepare_freezes_and_detects_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            home=Path(tmp);(home/"raw").mkdir()
            records=[row(i,f"family-{i//3}") for i in range(75)]
            (home/"raw"/"inventory_summary.jsonl").write_text(
                "".join(json.dumps(r)+"\n" for r in records))
            with mock.patch.object(workbench,"DATA",home), mock.patch.object(workbench,"check_branch"):
                workbench.prepare("inventory_summary")
                self.assertEqual(workbench.validate_splits("inventory_summary")["counts"]["train"]>0,True)
                with self.assertRaises(workbench.Stop):workbench.prepare("inventory_summary")
                train=home/"splits"/"inventory_summary"/"train.jsonl"
                train.write_text(train.read_text()+"\n")
                with self.assertRaises(workbench.Stop):workbench.validate_splits("inventory_summary")
    def test_main_branch_refused(self):
        with mock.patch.object(workbench,"subprocess") as run:
            run.run.return_value.stdout="main\n"
            with self.assertRaises(workbench.Stop):workbench.check_branch()
if __name__=="__main__":unittest.main()
