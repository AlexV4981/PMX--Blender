"""Plumbing tests for the evidence ledger, bridge and report generator.

NOT Blender evidence: the container runtime is replaced by an injected fake executor, so these
tests prove the binding/refusal logic only. No test here runs Blender, Docker or a model.
"""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
BENCH = HERE.parent
sys.path.insert(0, str(BENCH))
from evidence import bridge, ingest, ledger as L, report  # noqa: E402

CLOCK_N = [0]


def clock():
    CLOCK_N[0] += 1
    return "2026-11-06T00:00:%02d.%06dZ" % (CLOCK_N[0] // 1000000 % 60, CLOCK_N[0] % 1000000)


def sha(s):
    return L.sha256_bytes(s.encode())


def load_fixture_cases():
    spec = importlib.util.spec_from_file_location("fx", BENCH.parent / "astra-qwen-weight-lab" / "fixtures.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.cases()


class Env:
    def __init__(self, td):
        self.root = Path(td)
        self.ledger = L.Ledger(self.root / "ledger" / "events.jsonl", clock=clock)
        self.store = L.ArtifactStore(self.root / "artifacts")
        self.exp = "exp-001"

    def lap(self, lap_id="lap-00", parent=None, task="geometry_weight_normalize", consulted=(), **kw):
        f = {"lap_id": lap_id, "parent_lap_id": parent, "task_id": task, "change_reason": "untuned baseline",
             "selection_rule_sha256": sha(report.SELECTION_RULE), "split_manifest_sha256": sha("split-v1"),
             "cases_consulted_for_change": list(consulted)}
        f.update(kw)
        return self.ledger.append("lap", "controller", self.exp, f)

    def attempt(self, case_id="c0", lap_id="lap-00", trial="t1", no=1, task="geometry_weight_normalize", stage="03",
                family="fam-0", split="dev", role="target", code="def solve(scene):\n    return {}\n", fixture_kind="synthetic",
                fixture_sha=None, **kw):
        cand = self.store.put("candidates", code.encode(), ".py") if code else None
        case = {"case_id": case_id, "stage": stage, "synthetic": True, "params": {}, "prompt": "p"}
        fx = L.fixture_hash(case)
        self.store.put("fixtures", ingest.fixture_bytes(case), ".json")
        f = {"attempt_id": "%s:%s:%s:%d" % (lap_id, trial, case_id, no), "lap_id": lap_id, "trial_id": trial,
             "attempt_no": no, "task_id": task, "stage": stage, "case_id": case_id, "source_family": family,
             "split": split, "role": role, "fixture_kind": fixture_kind, "fixture_sha256": fixture_sha or fx,
             "model_digest": "sha256:abc", "prompt_sha256": sha("prompt"), "template_sha256": None,
             "raw_output_sha256": None, "candidate_sha256": cand,
             "generation_status": "produced" if code else "inference_error", "seed": None, "temperature": 0,
             "num_ctx": 4096, "reasoning_mode": "off", "input_tokens": 100, "output_tokens": 50, "inference_seconds": 2.0}
        f.update(kw)
        return self.ledger.append("attempt", "orchestrator", self.exp, f, artifacts=self.store)

    def verdict(self, att, result="pass", **kw):
        # Unit tests use an explicit FAKE two-process receipt. This is not proof
        # that Docker/Blender executed; the live bridge must supply real receipts.
        oracle_sha = "c" * 64
        witness = {"verifier_phase": "fresh_process_no_candidate_exec",
                   "blender_executed": True, "blender_pass": result == "pass",
                   "source_sha256": att["candidate_sha256"],
                   "fixture_sha256": att["fixture_sha256"],
                   "oracle_sha256": oracle_sha,
                   "case_id": att["case_id"], "stage": att["stage"]}
        receipt = {"trusted_verifier_result": witness, "builder_exit_code": 0,
                   "verifier_exit_code": 0, "timed_out": False}
        f = {"attempt_id": att["attempt_id"], "candidate_sha256": att["candidate_sha256"],
             "fixture_sha256": att["fixture_sha256"], "oracle_version": "oracle_sha256:" + oracle_sha, "runtime_identity": "img@sha256:" + "a" * 64,
             "result": result, "failure_category": "none" if result == "pass" else "deformation",
             "severity": "none" if result == "pass" else "major", "severe_regression": False,
             "evidence_sha256": self.store.put("evidence", json.dumps(receipt).encode(), ".json"), "evidence_path": "evidence/x.json",
             "wall_seconds": 3.0, "isolation_verified": True, "evaluator_limitations": [], "reason": "", "reevaluation_of": None}
        f.update(kw)
        return self.ledger.append("verdict", "trusted_evaluator", self.exp, f, artifacts=self.store)


def with_env(fn):
    def wrapper(self):
        with tempfile.TemporaryDirectory() as td:
            fn(self, Env(td))
    return wrapper


class SchemaAndChain(unittest.TestCase):
    @with_env
    def test_valid_chain_and_null_stage(self, e):
        e.lap(task="pmx_name_translate")
        e.attempt(task="pmx_name_translate", stage=None, code="x")
        self.assertEqual(e.ledger.verify(e.store), [])

    @with_env
    def test_rejections(self, e):
        e.lap()
        a = e.attempt()
        with self.assertRaises(L.LedgerError):  # missing required field
            e.ledger.append("lap", "controller", e.exp, {"lap_id": "x"})
        with self.assertRaises(L.LedgerError):  # wrong role for event type
            e.ledger.append("verdict", "orchestrator", e.exp, {})
        with self.assertRaises(L.LedgerError):  # self-declared first_try
            e.attempt(case_id="c1", first_try=True)
        with self.assertRaises(L.LedgerError):  # result field smuggled into attempt
            e.attempt(case_id="c2", result="pass")
        with self.assertRaises(L.LedgerError):  # unknown field
            e.attempt(case_id="c3", bogus=1)
        with self.assertRaises(L.LedgerError):  # duplicate attempt id
            e.attempt()
        with self.assertRaises(L.LedgerError):  # non-monotonic attempt_no
            e.attempt(case_id="c0", no=3)
        with self.assertRaises(L.LedgerError):  # conflicting stage for task
            e.attempt(case_id="c9", stage="04")
        self.assertEqual(e.ledger.verify(e.store), [])

    @with_env
    def test_case_identity_conflict(self, e):
        e.lap()
        e.attempt(case_id="c0", trial="t1")
        with self.assertRaises(L.LedgerError):
            e.attempt(case_id="c0", trial="t2", split="validation")

    @with_env
    def test_verdict_binding_rules(self, e):
        e.lap()
        a = e.attempt()
        with self.assertRaises(L.LedgerError):  # orphan
            e.verdict(dict(a, attempt_id="nope"))
        with self.assertRaises(L.LedgerError):  # wrong candidate hash
            e.verdict(a, candidate_sha256=sha("other"))
        with self.assertRaises(L.LedgerError):  # wrong fixture hash
            e.verdict(a, fixture_sha256=sha("other"))
        with self.assertRaises(L.LedgerError):  # pass without verified isolation
            e.verdict(a, isolation_verified=False)
        with self.assertRaises(L.LedgerError):  # invalid result
            e.verdict(a, result="great")
        v1 = e.verdict(a)
        with self.assertRaises(L.LedgerError):  # second verdict without re-evaluation identity
            e.verdict(a)
        e.verdict(a, result="fail", reevaluation_of=v1["event_id"])
        self.assertEqual(e.ledger.verify(e.store), [])

    @with_env
    def test_edits_break_chain(self, e):
        e.lap()
        e.attempt()
        text = e.ledger.path.read_text()
        e.ledger.path.write_text(text.replace('"temperature":0', '"temperature":1') if '"temperature":0' in text else text.replace('"temperature": 0', '"temperature": 1'))
        self.assertTrue(any("event_hash" in x or "chain" in x for x in e.ledger.verify(e.store)))
        with self.assertRaises(L.LedgerError):
            e.attempt(case_id="c5")  # refuses to append to an invalid ledger

    @with_env
    def test_deleted_event_breaks_chain(self, e):
        e.lap()
        e.attempt()
        e.attempt(case_id="c1")
        lines = e.ledger.path.read_text().splitlines()
        e.ledger.path.write_text("\n".join([lines[0], lines[2]]) + "\n")
        self.assertTrue(e.ledger.verify(e.store))

    @with_env
    def test_holdout_exposure_marked_compromised(self, e):
        e.lap(consulted=["h1"])
        e.attempt(case_id="h1", split="holdout")
        e.attempt(case_id="h2", split="holdout")
        comp = L.compromised_holdout_cases(e.ledger.read())
        self.assertIn("h1", comp)
        self.assertIn("h2", comp)  # no final-eval authorization

    @with_env
    def test_final_eval_authorization_is_not_compromised(self, e):
        e.lap()
        e.lap(lap_id="lap-final", parent="lap-00", holdout_final_eval=True)
        e.attempt(case_id="h3", lap_id="lap-final", split="holdout",
                  final_eval_selection_rule_sha256=sha(report.SELECTION_RULE))
        self.assertEqual(L.compromised_holdout_cases(e.ledger.read()), {})

    @with_env
    def test_fake_reviewer_approval_rejected(self, e):
        e.lap()
        base = {"decision_kind": "human_gate", "outcome": "approved", "reviewer_id": "r1",
                "review_evidence_sha256": sha("a review that was never stored"), "scope": "stage03"}
        with self.assertRaises(L.LedgerError):  # evidence file does not exist
            e.ledger.append("decision", "reviewer", e.exp, base, artifacts=e.store)
        with self.assertRaises(L.LedgerError):  # wrong role cannot write approvals
            e.ledger.append("decision", "controller", e.exp, base, artifacts=e.store)
        with self.assertRaises(L.LedgerError):  # model-style approval flag
            e.ledger.append("decision", "reviewer", e.exp, dict(base, human_approved=True), artifacts=e.store)
        real = e.store.put("reviews", b"signed review record", "")
        e.ledger.append("decision", "reviewer", e.exp, dict(base, review_evidence_sha256=real), artifacts=e.store)

    def test_fixture_hash_matches_runner(self):
        spec = importlib.util.spec_from_file_location("r", BENCH / "runner.py")
        r = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(r)
        case = {"b": 1, "a": [1, 2], "case_id": "x"}
        self.assertEqual(L.fixture_hash(case), r.sha(json.dumps(case, sort_keys=True).encode()))

    def test_canonical_hash_ignores_event_hash_and_key_order(self):
        a = {"x": 1, "y": [1, 2], "event_hash": "zz"}
        b = {"y": [1, 2], "x": 1}
        self.assertEqual(L.event_hash(a), L.event_hash(b))
        with self.assertRaises(ValueError):
            L.canonical({"x": float("nan")})


class FakeRuntime:
    """TWO-PHASE MOCK, not evidence of actual Blender or Docker execution."""
    def __init__(self, result=None, exit_code=0, timed_out=False):
        self.result, self.exit_code, self.timed_out, self.calls = result, exit_code, timed_out, []

    def __call__(self, cmd, timeout):
        self.calls.append(cmd)
        mounts = {}
        for part in cmd:
            if part.startswith("type=bind,"):
                f = dict(kv.split("=", 1) for kv in part.split(",") if "=" in kv)
                mounts[f["dst"]] = Path(f["src"])
        if "/lab/builder.py" in cmd:
            if self.result is not None:
                (mounts["/candidate_out"] / "candidate.blend").write_bytes(b"mock-only")
                (mounts["/candidate_out"] / "result.json").write_text("{}")
            return self.exit_code, "out", "err", self.timed_out, 0.5
        assert "/lab/verifier.py" in cmd
        if self.result is not None:
            (mounts["/trusted_out"] / "oracle.json").write_text(json.dumps(self.result))
        return self.exit_code, "out", "err", self.timed_out, 0.5


IMAGE = "blender@sha256:" + "b" * 64
GOOD_PROBE = bridge.ProbeResult(True, IMAGE + ";blender:4.2.0", {"verified": True})
BAD_PROBE = bridge.ProbeResult(False, "unavailable", {"why": "docker missing"})


def oracle_ok(att, **kw):
    r = {"case_id": att["case_id"], "stage": att["stage"],
         "verifier_phase": "fresh_process_no_candidate_exec",
         "blender_executed": True, "blender_pass": True,
         "source_sha256": att["candidate_sha256"],
         "fixture_sha256": att["fixture_sha256"],
         "oracle_sha256": L.sha256_bytes(bridge.ORACLE.read_bytes()),
         "oracle_detail": "ok", "error_feedback": ""}
    r.update(kw)
    return r


class BridgeTests(unittest.TestCase):
    def evaluate(self, e, att, rt, probe=GOOD_PROBE):
        return bridge.evaluate_attempt(e.ledger, e.store, e.exp, att["attempt_id"], image=IMAGE, probe=probe,
                                       executor=rt, scratch_root=e.root)

    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.e = Env(self.td.name)
        self.e.lap()
        self.att = self.e.attempt()

    def tearDown(self):
        self.td.cleanup()

    def test_pass_requires_matching_oracle_binding(self):
        v = self.evaluate(self.e, self.att, FakeRuntime(oracle_ok(self.att)))
        self.assertEqual((v["result"], v["isolation_verified"]), ("pass", True))
        self.assertTrue(v["evaluator_limitations"])  # remaining honest sandbox limitations are recorded
        self.assertEqual(self.e.ledger.verify(self.e.store), [])

    def test_oracle_result_for_other_candidate_is_blocked_not_pass(self):
        v = self.evaluate(self.e, self.att, FakeRuntime(oracle_ok(self.att, source_sha256=sha("forged"))))
        self.assertEqual((v["result"], v["failure_category"]), ("blocked", "integrity"))

    def test_wrong_case_or_unexecuted_result_blocked(self):
        for bad in ({"case_id": "other"}, {"blender_executed": False}, {"blender_pass": "yes"}, {"stage": "04"}):
            with tempfile.TemporaryDirectory() as td:
                e = Env(td)
                e.lap()
                a = e.attempt()
                v = self.evaluate(e, a, FakeRuntime(oracle_ok(a, **bad)))
                self.assertEqual(v["result"], "blocked", bad)

    def test_unverified_sandbox_never_executes(self):
        rt = FakeRuntime(oracle_ok(self.att))
        v = self.evaluate(self.e, self.att, rt, BAD_PROBE)
        self.assertEqual((v["result"], v["failure_category"]), ("blocked", "sandbox"))
        self.assertEqual(rt.calls, [])

    def test_timeout_crash_and_missing_result_are_blocked(self):
        for rt in (FakeRuntime(None, None, True), FakeRuntime(None, 137), FakeRuntime(None, 2)):
            with tempfile.TemporaryDirectory() as td:
                e = Env(td)
                e.lap()
                a = e.attempt()
                self.assertEqual(self.evaluate(e, a, rt)["result"], "blocked")

    def test_failure_and_critical_severity(self):
        v = self.evaluate(self.e, self.att, FakeRuntime(oracle_ok(self.att, blender_pass=False,
                          error_feedback="Geometry, MASK, or shape keys changed", oracle_detail="Geometry, MASK, or shape keys changed")))
        self.assertEqual((v["result"], v["severity"], v["severe_regression"], v["failure_category"]), ("fail", "critical", True, "deformation"))

    def test_exception_is_blender_api_major(self):
        v = self.evaluate(self.e, self.att, FakeRuntime(oracle_ok(self.att, blender_pass=False, error_feedback="boom",
                          oracle_detail="Traceback (most recent call last):\n boom")))
        self.assertEqual((v["result"], v["severity"], v["failure_category"]), ("fail", "major", "blender_api"))

    def test_no_candidate_is_not_run(self):
        with tempfile.TemporaryDirectory() as td:
            e = Env(td)
            e.lap()
            a = e.attempt(code=None)
            rt = FakeRuntime(None)
            v = self.evaluate(e, a, rt)
            self.assertEqual((v["result"], v["failure_category"]), ("not_run", "invalid_output"))
            self.assertEqual(rt.calls, [])

    def test_tampered_candidate_artifact_blocked(self):
        p = self.e.store._path("candidates", self.att["candidate_sha256"], ".py")
        p.chmod(0o644)
        p.write_text("def solve(scene):\n    return {'evil': 1}\n")
        rt = FakeRuntime(oracle_ok(self.att))
        v = self.evaluate(self.e, self.att, rt)
        self.assertEqual((v["result"], v["failure_category"]), ("blocked", "integrity"))
        self.assertEqual(rt.calls, [])

    def test_command_hardening_and_mount_rules(self):
        cmd = bridge.sandbox_flags(IMAGE, [(self.td.name, "/results", False)])
        for flag in ("--network", "none", "--read-only", "--cap-drop", "ALL", "no-new-privileges"):
            self.assertIn(flag, cmd)
        with self.assertRaises(L.LedgerError):
            bridge.sandbox_flags("blender:latest", [])
        with self.assertRaises(L.LedgerError):
            bridge.assert_mounts_exclude([(self.e.ledger.path.parent, "/x", False)], [self.e.ledger.path.parent])
        rt = FakeRuntime(oracle_ok(self.att))
        self.evaluate(self.e, self.att, rt)
        self.assertIn("--name", rt.calls[0])  # named so a timeout can docker-kill it (kill path itself is untested here)
        joined = " ".join(rt.calls[0])
        self.assertNotIn(str(self.e.ledger.path.parent), joined)
        self.assertNotIn("docker.sock", joined)

    def test_probe_parsing(self):
        good = {"network_blocked": True, "root_readonly": True, "forbidden_paths_present": [], "secret_env_keys": [], "blender_version": "4.2.0"}
        self.assertTrue(bridge.parse_probe("x\nISOLATION_PROBE_RESULT " + json.dumps(good))["verified"])
        for k, v in (("network_blocked", False), ("root_readonly", False), ("secret_env_keys", ["X_TOKEN"]),
                     ("forbidden_paths_present", ["/var/run/docker.sock"]), ("blender_version", None)):
            self.assertFalse(bridge.parse_probe("ISOLATION_PROBE_RESULT " + json.dumps(dict(good, **{k: v})))["verified"], k)
        self.assertFalse(bridge.parse_probe("")["verified"])

    def test_run_probe_without_docker_is_unverified(self):
        def boom(*a, **k):
            raise FileNotFoundError("docker")
        self.assertFalse(bridge.run_probe(IMAGE, runner=boom).verified)

    def test_non_executable_inputs_refused(self):
        a2 = self.e.attempt(case_id="real1", fixture_kind="real")
        with self.assertRaises(L.LedgerError):
            self.evaluate(self.e, a2, FakeRuntime(None))


class IngestTests(unittest.TestCase):
    def test_runner_records_become_attempts_without_runner_verdict_fields(self):
        cases = [c for c in load_fixture_cases() if c["stage"] == "03"]
        with tempfile.TemporaryDirectory() as td:
            e = Env(td)
            e.lap()
            runner_file = Path(td) / "runner.jsonl"
            recs = []
            for c in cases[:3]:
                recs.append({"stage": "03", "lap": "untuned", "attempt": 1, "case_id": c["case_id"],
                             "fixture_family": c["fixture_family"], "model": "q", "model_digest": "sha256:d",
                             "fixture_sha256": L.fixture_hash(c), "prompt_sha256": sha("p"),
                             "decoding": {"temperature": 0.0, "num_ctx": 4096, "num_predict": 1536},
                             "blender_executed": True, "blender_pass": True,  # must be ignored
                             "result": {"status": "produced", "code": "def solve(scene):\n    return {}\n", "prompt_tokens": 10,
                                        "output_tokens": 5, "elapsed_seconds": 1.5, "blender_executed": True, "blender_pass": True}})
            recs.append(dict(recs[0], case_id=cases[3]["case_id"], fixture_family=cases[3]["fixture_family"],
                             fixture_sha256=L.fixture_hash(cases[3]), result={"status": "inference_error", "error": "x"}))
            runner_file.write_text("\n".join(json.dumps(r) for r in recs) + "\n")
            ev = ingest.ingest_runner_jsonl(e.ledger, e.store, runner_file, {c["case_id"]: c for c in cases},
                                            experiment_id=e.exp, lap_id="lap-00", trial_id="t1")
            self.assertEqual(len(ev), 4)
            self.assertTrue(all("blender_pass" not in x and "result" not in x for x in ev))
            self.assertIsNone(ev[3]["candidate_sha256"])
            self.assertEqual(ev[3]["generation_status"], "inference_error")
            with self.assertRaises(L.LedgerError):  # replay of the same file = duplicate attempts
                ingest.ingest_runner_jsonl(e.ledger, e.store, runner_file, {c["case_id"]: c for c in cases},
                                           experiment_id=e.exp, lap_id="lap-00", trial_id="t1")
            bad = dict(recs[0], fixture_sha256=sha("tampered"))
            runner_file2 = Path(td) / "bad.jsonl"
            runner_file2.write_text(json.dumps(bad) + "\n")
            with self.assertRaises(L.LedgerError):
                ingest.ingest_runner_jsonl(e.ledger, e.store, runner_file2, {c["case_id"]: c for c in cases},
                                           experiment_id=e.exp, lap_id="lap-00", trial_id="t9")


class ReportTests(unittest.TestCase):
    def build_pilot(self, e, passes=15, n=20):
        e.lap()
        for i in range(n):
            a = e.attempt(case_id="c%02d" % i, family="fam-%d" % (i // 4))
            e.verdict(a, "pass" if i < passes else "fail")

    def gen(self, e, **kw):
        return report.generate(e.ledger.path, e.store.root, e.exp, **kw)

    @with_env
    def test_seven_headings_and_exploratory_75_percent(self, e):
        self.build_pilot(e)
        md, caps = self.gen(e)
        heads = [l for l in md.splitlines() if l.startswith("## ")]
        self.assertEqual(heads, ["## " + s for s in report.SECTIONS])
        self.assertIn("15/20", md)
        self.assertIn("75%", md)
        self.assertIn("53-89%", md)
        self.assertIn("numerically met", md)
        self.assertIn("INCOMPLETE", md)  # cost gate not measured
        self.assertIn("2 verified synthetic observations (development-only)", md)
        self.assertIsNone(caps[0]["best_lap_id"])  # dev-only: no validation split, rule cannot select
        self.assertEqual(caps[0]["dev_only_first_try_by_lap"], {"lap-00": [15, 20]})

    @with_env
    def test_deterministic_replay(self, e):
        self.build_pilot(e, 3, 5)
        self.assertEqual(self.gen(e), self.gen(e))

    @with_env
    def test_missing_blocked_and_not_run_never_count_as_pass(self, e):
        e.lap()
        a1 = e.attempt(case_id="a")
        e.verdict(a1)
        e.attempt(case_id="b")  # no verdict
        a3 = e.attempt(case_id="c")
        e.verdict(a3, "blocked", failure_category="sandbox", severity="none", isolation_verified=False)
        a4 = e.attempt(case_id="d", code=None)
        e.verdict(a4, "not_run", failure_category="invalid_output", severity="none", candidate_sha256=None, evidence_sha256=None, isolation_verified=False)
        md, _ = self.gen(e)
        self.assertIn("| 1/4 | 25% |", md)
        self.assertIn("1/4", md)

    @with_env
    def test_repairs_not_counted_as_first_try(self, e):
        e.lap()
        a = e.attempt(case_id="a")
        e.verdict(a, "fail")
        r = e.attempt(case_id="a", no=2, code="def solve(scene):\n    return {'v': 2}\n")
        e.verdict(r, "pass")
        md, _ = self.gen(e)
        self.assertIn("| 0/1 | 0% |", md)
        self.assertIn("1/1", md)  # repair pass/tries reported separately

    @with_env
    def test_specialization_and_canary_deltas(self, e):
        e.lap()
        for i in range(4):
            a = e.attempt(case_id="t%d" % i)
            e.verdict(a, "pass" if i < 1 else "fail")
        ca = e.attempt(case_id="k0", task="left_arm_ik", stage="04", role="canary")
        e.verdict(ca)
        e.lap("lap-01", parent="lap-00", change_reason="prompt change")
        for i in range(4):
            a = e.attempt(case_id="t%d" % i, lap_id="lap-01", trial="t2")
            e.verdict(a, "pass" if i < 3 else "fail")
        cb = e.attempt(case_id="k0", lap_id="lap-01", trial="t2", task="left_arm_ik", stage="04", role="canary")
        e.verdict(cb, "fail")
        md, _ = self.gen(e)
        sec4 = md.split("## 4.")[1].split("## 5.")[0]
        self.assertIn("| lap-01 | geometry_weight_normalize | target | dev | 1/4 | 3/4 | +2 |", sec4)
        self.assertIn("| lap-01 | left_arm_ik | canary | dev | 1/1 | 0/1 | -1 |", sec4)

    @with_env
    def test_validation_split_selects_best_lap(self, e):
        e.lap()
        for lap_id, passes in (("lap-00", 1), ("lap-01", 3)):
            if lap_id != "lap-00":
                e.lap(lap_id, parent="lap-00")
            for i in range(4):
                a = e.attempt(case_id="v%d" % i, lap_id=lap_id, trial=lap_id, split="validation")
                e.verdict(a, "pass" if i < passes else "fail")
        _, caps = self.gen(e)
        self.assertEqual((caps[0]["best_lap_id"], caps[0]["first_try_pass_count"], caps[0]["n"]), ("lap-01", 3, 4))

    @with_env
    def test_proposal_only_has_no_verified_level(self, e):
        e.lap()
        e.attempt()
        md, _ = self.gen(e)
        self.assertIn("1 proposal-only", md)

    @with_env
    def test_tampered_ledger_blocks_report(self, e):
        self.build_pilot(e, 2, 3)
        text = e.ledger.path.read_text()
        e.ledger.path.write_text(text.replace('"result": "fail"', '"result": "pass"'))
        with self.assertRaises(report.ReportBlocked):
            self.gen(e)

    @with_env
    def test_missing_evidence_artifact_blocks_report(self, e):
        e.lap()
        a = e.attempt()
        v = e.verdict(a)
        p = e.store._path("evidence", v["evidence_sha256"], ".json")
        p.chmod(0o644)
        p.unlink()
        with self.assertRaises(report.ReportBlocked):
            self.gen(e)

    @with_env
    def test_non_blender_task_uses_same_core_schema_and_headings(self, e):
        e.lap(task="pmx_name_translate")
        for i in range(3):
            a = e.attempt(case_id="n%d" % i, task="pmx_name_translate", stage=None, code="translated %d" % i)
            e.verdict(a, "pass" if i else "fail")
        md, _ = self.gen(e, narrative={"3": {"author": "operator", "text": "terminology errors only"}})
        self.assertEqual([l for l in md.splitlines() if l.startswith("## ")], ["## " + s for s in report.SECTIONS])
        self.assertIn("(author: operator) terminology errors only", md)

    @with_env
    def test_codex_cost_gate_never_reported_as_pass(self, e):
        self.build_pilot(e, 20, 20)
        md, _ = self.gen(e)
        self.assertIn("NOT MEASURED", md)

    def test_wilson_and_percentiles(self):
        lo, hi = report.wilson(15, 20)
        self.assertAlmostEqual(lo, 0.531, places=3)
        self.assertAlmostEqual(hi, 0.888, places=3)
        self.assertEqual(report.nearest_rank([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], .5), 5)
        self.assertEqual(report.nearest_rank([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], .95), 10)

    @with_env
    def test_timing_denominator_excludes_incomplete_rows(self, e):
        e.lap()
        a = e.attempt(case_id="a", inference_seconds=60.0)
        e.verdict(a, wall_seconds=0.0)
        b = e.attempt(case_id="b", inference_seconds=None)
        e.verdict(b, "fail")
        md, _ = self.gen(e)
        self.assertIn("not measured (timing incomplete)", md)


class LegacyOracleDefect(unittest.TestCase):
    """Reproduces the structural weakness recorded as LEGACY_ORACLE_LIMITATIONS.

    astra-qwen-weight-lab/blender_oracle.py exec()s candidate code in the same process that later
    calls validate(). With bpy and stage setup stubbed, a candidate can replace validate(). This
    reproduces the structure only; it is not a Blender run.
    """

    def test_candidate_can_override_validator_in_same_process(self):
        import types
        spec = importlib.util.spec_from_file_location("oracle_under_test", BENCH.parent / "astra-qwen-weight-lab" / "blender_oracle.py")
        oracle = importlib.util.module_from_spec(spec)
        sys.modules["oracle_under_test"] = oracle
        spec.loader.exec_module(oracle)
        fake_bpy = types.ModuleType("bpy")
        fake_bpy.context = types.SimpleNamespace(scene=object())
        sys.modules["bpy"] = fake_bpy
        try:
            oracle.setup_stage = lambda scene, case: object()
            oracle.snapshot = lambda *a, **k: {}
            oracle.validate = lambda *a, **k: (False, "honest validator rejects")
            with tempfile.TemporaryDirectory() as td:
                honest = Path(td) / "honest.py"
                honest.write_text("def solve(scene):\n    return {}\n")
                forged = Path(td) / "forged.py"
                forged.write_text("import sys\ndef solve(scene):\n    sys.modules['oracle_under_test'].validate = lambda *a, **k: (True, 'forged')\n    return {}\n")
                case = {"case_id": "c", "stage": "03", "params": {}}
                self.assertFalse(oracle.execute(case, honest)["blender_pass"])
                oracle.validate = lambda *a, **k: (False, "honest validator rejects")
                self.assertTrue(oracle.execute(case, forged)["blender_pass"])  # DEFECT: forged pass
        finally:
            sys.modules.pop("bpy", None)
            sys.modules.pop("oracle_under_test", None)


if __name__ == "__main__":
    unittest.main()
