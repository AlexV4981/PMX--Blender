import importlib.util
import hashlib
import json
from pathlib import Path
from unittest import mock
import sys
import tempfile
import unittest

HELPER = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HELPER))
import done
import specialists

def task(name="inventory_summary", task_id="fixture-001"):
    return {"task_id":task_id,"specialist":name,"kind":"new_tool",
            "scope":"generic", "objective":"Count synthetic records",
            "expected_behavior":"Correct count", "references":[],
            "target":"skills/anime-blender-pipeline/scripts/qwen_inventory_sample.py"}

class DoneTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home=Path(self.tmp.name)
        self.outbox=self.home/"outbox"
        self.outbox.mkdir()
        self.events=self.home/"handoffs"
        self.events.mkdir()
        self.orig=(done.OUTBOX,done.HANDOFFS)
        done.OUTBOX=self.outbox
        done.HANDOFFS=self.events
        self.addCleanup(self.restore)

    def restore(self):
        done.OUTBOX,done.HANDOFFS=self.orig

    def proposal(self, t=None):
        t=t or task()
        p={"task":t,"model":specialists.registry()["specialists"][t["specialist"]]["model"],
           "base_sha256":None,
           "proposal":{"target":t["target"],"code":"def foo():\n    return 1\n"}}
        file=self.outbox/(t["task_id"]+".json")
        file.write_text(json.dumps(p))
        return file

    @mock.patch.object(done,"require_branch")
    def test_signal_no_execution_then_duplicate_fails(self, branch):
        p=self.proposal()
        with mock.patch.object(done,"ROOT",self.home):
            f=done.emit("inventory_summary")
            event=json.loads(f.read_text())
            self.assertEqual(event["proposal_sha256"],hashlib.sha256(p.read_bytes()).hexdigest())
            self.assertEqual(event["task_id"],"fixture-001")
            with self.assertRaises(done.HandoffError):
                done.emit("inventory_summary","fixture-001")

    @mock.patch.object(done,"require_branch")
    def test_mismatch_rejected(self, branch):
        p=self.proposal()
        self.assertEqual(done.candidates("texture_diagnostics"),[])
        with self.assertRaises(done.HandoffError):
            done.emit("texture_diagnostics","fixture-001")

    @mock.patch.object(done,"require_branch")
    def test_tamper_detected(self, branch):
        p=self.proposal()
        with mock.patch.object(done,"ROOT",self.home):
            event_file=done.emit("inventory_summary")
            p.write_text(p.read_text()+" ")
            with self.assertRaises(done.HandoffError):
                done.validate_event(event_file)

    def test_command_is_fixed_and_model_does_not_choose_flags(self):
        event={"task_id":"fixture-001","specialist":"inventory_summary"}
        cmd=done.build_codex_command(event,session="123e4567-e89b-12d3-a456-426614174000")
        self.assertEqual(cmd[:4],["codex","exec","--model","gpt-6.1-sol"])
        self.assertIn("resume",cmd)
        with self.assertRaises(done.HandoffError):
            done.build_codex_command(event,session="--last")

if __name__=="__main__":
    unittest.main()
