"""Offline regression suite for Claude-patch qualification and trust-boundary bugs.

These are MOCK tests. They DO NOT prove Docker/Blender operation or sandbox isolation.
"""
import json
from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from evidence import bridge, report
from evidence.ledger import LedgerError
from test_evidence import Env, IMAGE, GOOD_PROBE


def pure_attempt(case="c1", model="model:one", lap="lap1", trial="t1", stage="03"):
    return {"attempt_id": lap+":"+trial+":"+case, "lap_id":lap, "trial_id":trial,
            "case_id":case, "task_id":"geometry_weight_normalize", "stage":stage,
            "model_digest":model, "attempt_no":1, "split":"holdout", "role":"target",
            "fixture_kind":"real", "license_record_sha256":"f"*64,
            "asset_track":"pmx_vmd", "source_family":"family1",
            "final_eval_selection_rule_sha256":"a"*64, "inference_seconds":1,
            "input_tokens":10,"output_tokens":20}


class MockDocker:
    """The two synthetic containers are simulated; no untrusted code is executed."""
    def __init__(self, *, pass_result=True, builder_exit=0, verifier_exit=0):
        self.calls=[]
        self.pass_result=pass_result
        self.builder_exit=builder_exit
        self.verifier_exit=verifier_exit

    def __call__(self, cmd, timeout):
        self.calls.append(cmd)
        mounts = {}
        for item in cmd:
            if item.startswith("type=bind,"):
                fields = dict(part.split("=",1) for part in item.split(",") if "=" in part)
                mounts[fields["dst"]] = Path(fields["src"])
        if "/lab/builder.py" in cmd:
            assert "/trusted_out" not in mounts
            assert "/candidate_out" in mounts
            if self.builder_exit == 0:
                (mounts["/candidate_out"] / "candidate.blend").write_bytes(b"mock blend, not an actual Blender file")
                (mounts["/candidate_out"] / "result.json").write_text("{}")
                (mounts["/candidate_out"] / "oracle.json").write_text('{"blender_pass":true}')  # forgery ignored
            return self.builder_exit, "builder", "", False, 0.2
        assert "/lab/verifier.py" in cmd
        assert "/trusted_out" in mounts
        assert "/candidate_out" not in mounts
        case = json.loads(mounts["/lab/case.json"].read_text())
        from evidence.ledger import fixture_hash, sha256_bytes
        result = {"verifier_phase":"fresh_process_no_candidate_exec", "blender_executed":True,
                  "blender_pass": self.pass_result,
                  "source_sha256":sha256_bytes(mounts["/lab/candidate.py"].read_bytes()),
                  "fixture_sha256": fixture_hash(case),
                  "oracle_sha256":sha256_bytes(mounts["/lab/oracle.py"].read_bytes()),
                  "case_id":case["case_id"], "stage":case["stage"],
                  "oracle_detail":"synthetic fake result"}
        (mounts["/trusted_out"] / "oracle.json").write_text(json.dumps(result))
        return self.verifier_exit, "verifier", "", False, 0.1


class TwoProcessBridge(unittest.TestCase):
    def _evaluate(self, *, passed=True, builder_exit=0, verifier_exit=0):
        with tempfile.TemporaryDirectory() as td:
            e=Env(td)
            e.lap()
            att=e.attempt(case_id="c0")
            oracle=Path(td)/"trusted_oracle.py"
            oracle.write_text("# oracle stub for mocked bridge\n")
            fake=MockDocker(pass_result=passed,builder_exit=builder_exit,verifier_exit=verifier_exit)
            with patch.object(bridge,"ORACLE",oracle):
                v=bridge.evaluate_attempt(e.ledger,e.store,e.exp,att["attempt_id"],
                    image=IMAGE,probe=GOOD_PROBE,executor=fake,scratch_root=e.root)
            self.assertEqual(e.ledger.verify(e.store),[])
            return v, fake.calls

    def test_separate_process_mock_pass_and_identity(self):
        v,commands=self._evaluate()
        self.assertEqual(v["result"],"pass")
        self.assertEqual(len(commands),2)
        self.assertTrue(all("--disable-autoexec" in c for c in commands))
        self.assertTrue(all("--network" in c and "none" in c for c in commands))
        self.assertTrue(all("--user" in c for c in commands))
        self.assertFalse(any("/lab/candidate.py" == commands[1][i+1] for i,t in enumerate(commands[1][:-1]) if t == "--python"))

    def test_fresh_verifier_rejects_wrong_solution_despite_builder_forgery(self):
        v,_=self._evaluate(passed=False)
        self.assertEqual(v["result"],"fail")

    def test_builder_nonzero_cannot_pass(self):
        v,_=self._evaluate(builder_exit=137)
        self.assertEqual(v["result"],"blocked")

    def test_verifier_nonzero_cannot_pass(self):
        v,_=self._evaluate(verifier_exit=7)
        self.assertEqual(v["result"],"blocked")

    def test_old_same_process_oracle_is_not_a_valid_witness(self):
        att={"attempt_id":"a", "candidate_sha256":"b"*64,
             "fixture_sha256":"f"*64,"case_id":"case","stage":"03"}
        with tempfile.TemporaryDirectory() as td:
            f=Path(td)/"oracle.py";f.write_text("stub\n")
            with patch.object(bridge,"ORACLE",f):
                x=bridge.derive_verdict(att,oracle_result={"blender_executed":True,
                    "blender_pass":True,"source_sha256": "b"*64,
                    "case_id":"case","stage":"03"},
                    exit_code=0,builder_exit_code=0,timed_out=False,
                    candidate_sha="b"*64,fixture_sha="f"*64,probe=GOOD_PROBE,
                    trusted_oracle_sha=bridge.sha256_bytes(f.read_bytes()),wall=1)
            self.assertEqual(x["result"],"blocked")

    def test_probe_nonzero_is_not_verified(self):
        def fake(cmd, **kw):
            text='ISOLATION_PROBE_RESULT '+json.dumps({"network_blocked":True,
                "root_readonly":True,"forbidden_paths_present":[],"secret_env_keys":[],
                "blender_version":"4.2"})+'\n'
            return SimpleNamespace(stdout=text,returncode=7)
        self.assertFalse(bridge.run_probe(IMAGE,runner=fake).verified)


class EvidenceAndQualification(unittest.TestCase):
    def test_trial_reset_in_next_lap(self):
        with tempfile.TemporaryDirectory() as td:
            e=Env(td)
            e.lap()
            e.attempt(case_id="c0",trial="seed1",lap_id="lap-00")
            e.lap(lap_id="lap-01",parent="lap-00")
            e.attempt(case_id="c0",trial="seed1",lap_id="lap-01",no=1)
            self.assertEqual(e.ledger.verify(e.store),[])

    def test_seven_section_report_refuses_mixed_models(self):
        with tempfile.TemporaryDirectory() as td:
            e=Env(td);e.lap()
            e.attempt(case_id="a",model_digest="model:first")
            e.attempt(case_id="b",model_digest="model:second")
            with self.assertRaises(report.ReportBlocked):
                report.generate(e.ledger.path,e.store.root,e.exp)

    def test_300_repeated_cases_not_300_holdouts(self):
        exp="exp-unique"
        lap={"event_type":"lap", "experiment_id":exp, "lap_id":"lap1",
             "task_id":"geometry_weight_normalize", "selection_rule_sha256":"a"*64,
             "cases_consulted_for_change":[],"parent_lap_id":None}
        final={"event_type":"lap","experiment_id":exp,"lap_id":"final", "parent_lap_id":"lap1",
               "task_id":"geometry_weight_normalize","selection_rule_sha256":"a"*64,
               "cases_consulted_for_change":[],"holdout_final_eval":True}
        atts=[pure_attempt(case="h0", lap="final",trial="t%d"%i) for i in range(300)]
        # Additional validation selects the lap before the holdout.
        val=pure_attempt(case="v0", lap="lap1",trial="val")
        val["split"]="validation"
        events=[lap,final]+[{"event_type":"attempt", "experiment_id":exp, **a} for a in atts+[val]]
        for a in atts+[val]:
            events.append({"event_type":"verdict", "experiment_id":exp,
                "attempt_id":a["attempt_id"],"result":"pass", "isolation_verified":True, "severe_regression":False, "wall_seconds":1})
        m=report.Model(events,exp)
        level,unmet=report.readiness(m)
        self.assertNotIn("production-qualified", level)
        self.assertTrue(any("distinct untouched" in u and "1 unique cases" in u for u in unmet),unmet)

    def test_300_unique_cases_one_family_insufficient(self):
        exp="exp-family"
        lap={"event_type":"lap", "experiment_id":exp, "lap_id":"lap1",
             "task_id":"geometry_weight_normalize", "selection_rule_sha256":"a"*64,
             "cases_consulted_for_change":[],"parent_lap_id":None}
        final={"event_type":"lap","experiment_id":exp,"lap_id":"final", "parent_lap_id":"lap1",
               "task_id":"geometry_weight_normalize","selection_rule_sha256":"a"*64,
               "cases_consulted_for_change":[],"holdout_final_eval":True}
        atts=[pure_attempt(case="c%d"%i,lap="final",trial="t%d"%i) for i in range(300)]
        val=pure_attempt(case="v0",lap="lap1",trial="val"); val["split"]="validation"
        events=[lap,final]+[{"event_type":"attempt", "experiment_id":exp, **a} for a in atts+[val]]
        events += [{"event_type":"verdict","experiment_id":exp,"attempt_id":a["attempt_id"],
                    "result":"pass","isolation_verified":True,"severe_regression":False,"wall_seconds":1} for a in atts+[val]]
        level,unmet=report.readiness(report.Model(events,exp))
        self.assertNotIn("production-qualified",level)
        self.assertTrue(any("source families" in u for u in unmet))

    def test_hash_chain_does_not_accept_fake_pass_receipt(self):
        with tempfile.TemporaryDirectory() as td:
            e=Env(td);e.lap();a=e.attempt()
            # Explicit old-style written-by-hand evidence must not pass.
            sha=e.store.put("evidence",b"{}",".json")
            with self.assertRaises(LedgerError):
                e.verdict(a,evidence_sha256=sha)

    def test_blocked_reasons_are_counted_not_deduplicated(self):
        with tempfile.TemporaryDirectory() as td:
            e=Env(td);e.lap()
            for i in range(3):
                a=e.attempt(case_id="c%d"%i)
                e.verdict(a,result="blocked",failure_category="sandbox",severity="none",
                          isolation_verified=False, blocked_reason="isolation_unverified")
            md,_=report.generate(e.ledger.path,e.store.root,e.exp)
            self.assertIn('"isolation_unverified": 3',md)


if __name__ == "__main__":
    unittest.main()

class FrozenSplits(unittest.TestCase):
    def test_family_split_cannot_leak(self):
        from evidence.splits import parse_manifest
        manifest = {"schema_version":1,"cases":[
            {"case_id":"a","source_family":"same","split":"dev"},
            {"case_id":"b","source_family":"same","split":"holdout"}]}
        with self.assertRaises(LedgerError):
            parse_manifest(json.dumps(manifest).encode())

    def test_split_membership_enforced(self):
        from evidence.splits import parse_manifest, enforce_case_split
        manifest={"schema_version":1,"cases":[
            {"case_id":"a","source_family":"fa","split":"dev"},
            {"case_id":"b","source_family":"fb","split":"holdout"}]}
        labels=parse_manifest(json.dumps(manifest).encode())
        enforce_case_split([{"case_id":"a","fixture_family":"fa"}],labels,"dev")
        with self.assertRaises(LedgerError):
            enforce_case_split([{"case_id":"b","fixture_family":"fb"}],labels,"dev")

    def test_selection_rule_cannot_change_across_laps(self):
        with tempfile.TemporaryDirectory() as td:
            e=Env(td)
            e.lap()
            with self.assertRaises(LedgerError):
                e.lap(lap_id="lap-next",parent="lap-00",selection_rule_sha256="a"*64)

    def test_invalid_final_parent_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            e=Env(td)
            with self.assertRaises(LedgerError):
                e.lap(holdout_final_eval=True)

    def test_raw_response_is_content_addressed_and_integrity_checked(self):
        from evidence import ingest
        from evidence.ledger import fixture_hash
        with tempfile.TemporaryDirectory() as td:
            e=Env(td);e.lap()
            c={"case_id":"x","stage":"03","synthetic":True,"params":{},"prompt":"p","fixture_family":"f"}
            raw='{"code":"def solve(scene): return {}","explanation":""}'
            rec={"case_id":"x", "stage":"03","fixture_sha256":fixture_hash(c),
                 "fixture_family":"f","model_digest":"model:digest","prompt_sha256":"a"*64,
                 "decoding":{"temperature":0,"num_ctx":4096},
                 "attempt":1,"result":{"status":"produced","code":"def solve(scene): return {}",
                                       "raw_response_text":raw,"raw_response_sha256":e.store.put("raw_outputs",raw.encode(),".txt")}}
            runner=Path(td)/"runner.jsonl";runner.write_text(json.dumps(rec)+"\n")
            ingested=ingest.ingest_runner_jsonl(e.ledger,e.store,runner,{"x":c},experiment_id=e.exp,
                                                 lap_id="lap-00",trial_id="t1")
            self.assertEqual(len(ingested),1)
            self.assertEqual(e.ledger.verify(e.store),[])
            p=e.store._path("raw_outputs",rec["result"]["raw_response_sha256"],".txt")
            p.chmod(0o644);p.write_text("tampered")
            self.assertTrue(any("raw model output" in err for err in e.ledger.verify(e.store)))
