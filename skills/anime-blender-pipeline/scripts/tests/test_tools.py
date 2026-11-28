"""Behavioral tests for ledger invariants and bounded PMX parsing; no Blender claims."""
import argparse
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


p = module("pipeline")
pmx = module("pmx_inventory")


def args(**kw): return argparse.Namespace(**kw)


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.root = self.base / "run"
        self.source = self.base / "source.pmx"
        self.source.write_bytes(b"test ledger source, not a PMX fixture")
        p.init_run(args(source=[str(self.source)]), self.root)
        self.run = p.load(self.root)
        self.evidence = self.root / "audit" / "test.txt"
        self.evidence.write_text("observed test evidence")

    def tearDown(self): self.tmp.cleanup()

    def candidate(self, stage="00", cid="A"):
        f = self.root / "work" / (stage+cid+".json")
        if stage == "09" and self.run["stages"]["08P"]["approved"]:
            prev = self.run["stages"]["08P"]["candidates"][self.run["stages"]["08P"]["approved"]]
            f.write_bytes((self.root / prev["primary"]).read_bytes())
        else:
            f.write_text(json.dumps({"fixture": cid, "stage": stage}))
        p.register(args(stage=stage, candidate=cid, file=str(f), asset=[]), self.root, self.run)
        return f

    def check_all(self, stage="00", cid="A"):
        policy = p.read_json(self.root / "policy.json")["stages"][stage]
        for name in policy.get("pre_review_checks", policy["required_checks"]):
            p.record_check(args(stage=stage, candidate=cid, name=name, status="pass", evidence=str(self.evidence)), self.root, self.run)
        if stage != "09":
            p.direction(args(stage=stage,candidate=cid,actor="fixture-human",statement="Fixture direction"),self.root,self.run)
            for name in policy["post_review_checks"]:
                p.record_check(args(stage=stage, candidate=cid, name=name, status="pass", evidence=str(self.evidence)), self.root, self.run)

    def accept(self, stage="00", cid="A"):
        p.submit(args(stage=stage, candidate=cid), self.root, self.run)
        p.storage(args(stage=stage,candidate=cid,quiescent=True),self.root,self.run)
        p.complete(args(stage=stage, candidate=cid), self.root, self.run)

    def test_previous_stage_gate(self):
        with self.assertRaises(p.PipelineError): self.candidate("01")

    def test_submit_without_checks_fails(self):
        self.candidate()
        with self.assertRaises(p.PipelineError): p.submit(args(stage="00", candidate="A"), self.root, self.run)

    def test_cannot_approve_draft(self):
        self.candidate(); self.check_all()
        with self.assertRaises(p.PipelineError):
            p.approve(args(stage="00", candidate="A", actor="human", statement="yes"), self.root, self.run)

    def test_candidate_cap(self):
        for cid in ("A", "B", "C"): self.candidate(cid=cid)
        with self.assertRaises(p.PipelineError): self.candidate(cid="D")

    def test_stale_artifact_rejected(self):
        f = self.candidate(); self.check_all(); f.write_text("changed")
        with self.assertRaises(p.PipelineError): p.submit(args(stage="00", candidate="A"), self.root, self.run)

    def test_changed_evidence_rejected(self):
        self.candidate(); self.check_all(); self.evidence.write_text("changed evidence")
        with self.assertRaises(p.PipelineError): p.submit(args(stage="00", candidate="A"), self.root, self.run)

    def test_submit_snapshot_and_feedback(self):
        self.candidate(); self.check_all(); p.submit(args(stage="00", candidate="A"), self.root, self.run)
        c = p.get_candidate(self.run, "00", "A")
        snapshot = self.root / c["snapshot"][0]["path"]
        self.assertTrue(snapshot.is_file())
        with self.assertRaises(p.PipelineError): self.candidate()
        p.feedback(args(stage="00", candidate="A", statement="Please revise"), self.root, self.run)
        self.candidate()
        self.assertTrue(snapshot.is_file()); self.assertEqual(c["revision"], 1)
        self.assertEqual(p.get_candidate(self.run, "00", "A")["revision"], 2)
        self.assertEqual(p.get_candidate(self.run, "00", "A")["checks"], {})

    def test_approved_sources_and_evidence_are_immutable(self):
        self.candidate(); self.check_all(); self.accept()
        p.atomic_json(self.root / "run.json", self.run)
        self.assertTrue(p.load(self.root))
        self.evidence.write_text("tampered")
        with self.assertRaises(p.PipelineError): p.load(self.root)

    def test_source_changed_blocks_work(self):
        self.source.write_bytes(b"changed")
        with self.assertRaises(p.PipelineError): p.load(self.root)

    def test_policy_change_is_not_a_bypass(self):
        (self.root / "policy.json").write_text("{}")
        with self.assertRaises(p.PipelineError): p.load(self.root)

    def test_path_escape_rejected(self):
        with self.assertRaises(p.PipelineError): p.stamp(self.root, self.source)

    def test_shared_mutable_assets_rejected(self):
        f = self.candidate()
        with self.assertRaises(p.PipelineError):
            p.register(args(stage="00", candidate="B", file=str(f), asset=[]), self.root, self.run)

    def stage09(self, submitted=True):
        for stage in p.STAGES:
            self.candidate(stage); self.check_all(stage)
            if stage != "09": self.accept(stage)
        if submitted: p.submit(args(stage="09", candidate="A"), self.root, self.run)

    def review09(self, gate):
        return p.review(args(stage="09", candidate="A", gate=gate, actor="fixture-human",
            statement="Observed fixture decision", evidence=str(self.evidence)), self.root, self.run)

    def test_stage09_two_decisions_and_no_third_approval(self):
        self.stage09()
        approval = args(stage="09", candidate="A", actor="fixture-human", statement="Explicit fixture acceptance")
        with self.assertRaises(p.PipelineError): p.approve(approval, self.root, self.run)
        self.review09("audit")
        self.assertIsNone(self.run["stages"]["09"]["approved"])
        result=self.review09("delivery")
        self.assertEqual(result["approved"],"A")
        c=p.get_candidate(self.run,"09","A")
        self.assertEqual(set(c["reviews"]),{"audit","delivery"})
        self.assertEqual(c["approval"]["statement"],c["reviews"]["delivery"]["statement"])
        self.assertEqual(self.run["stages"]["09"]["approved"],"A")
        with self.assertRaises(p.PipelineError): p.approve(approval,self.root,self.run)

    def test_stage09_delivery_without_audit_rejected(self):
        self.stage09()
        with self.assertRaises(p.PipelineError):self.review09("delivery")
        self.assertNotIn("delivery",p.get_candidate(self.run,"09","A")["reviews"])

    def test_stage09_delivery_on_draft_rejected(self):
        self.stage09(submitted=False);self.review09("audit")
        with self.assertRaises(p.PipelineError):self.review09("delivery")

    def test_stage09_stale_final_bundle_rejected(self):
        self.stage09();self.review09("audit")
        c=p.get_candidate(self.run,"09","A");(self.root/c["primary"]).write_text("changed")
        with self.assertRaises(p.PipelineError):self.review09("delivery")
        self.assertIsNone(self.run["stages"]["09"]["approved"])

    def test_stage09_stale_snapshot_rejected(self):
        self.stage09();self.review09("audit")
        c=p.get_candidate(self.run,"09","A");(self.root/c["snapshot"][0]["path"]).write_text("changed")
        with self.assertRaises(p.PipelineError):self.review09("delivery")

    def test_stage09_stale_audit_evidence_rejected(self):
        self.stage09();self.review09("audit");self.evidence.write_text("tampered")
        with self.assertRaises(p.PipelineError):self.review09("delivery")

    def test_stage09_revisions_keep_audit_but_need_new_delivery(self):
        self.stage09();self.review09("audit")
        p.feedback(args(stage="09",candidate="A",statement="Observed fixture critique"),self.root,self.run)
        self.candidate("09");self.check_all("09")
        c=p.get_candidate(self.run,"09","A")
        self.assertEqual(set(c["reviews"]),{"audit"})
        p.submit(args(stage="09",candidate="A"),self.root,self.run)
        p.storage(args(stage="09",candidate="A",quiescent=True),self.root,self.run)
        self.review09("delivery")
        self.assertEqual(c["approval"]["bundle_sha256"],c["bundle_sha256"])

    def test_delivery_cli_persists_acceptance_in_one_operation(self):
        import contextlib,io
        self.stage09();self.review09("audit")
        p.atomic_json(self.root/"run.json",self.run)
        with contextlib.redirect_stdout(io.StringIO()):
            code=p.main(["review",str(self.root),"09","A","--gate","delivery",
                         "--actor","fixture-human","--statement","Deliver this fixture", "--evidence",str(self.evidence)])
        self.assertEqual(code,0)
        saved=p.load(self.root);c=p.get_candidate(saved,"09","A")
        self.assertEqual(c["status"],"approved")
        self.assertEqual(c["approval"]["statement"],"Deliver this fixture")
        self.assertEqual(c["reviews"]["delivery"]["bundle_sha256"],c["bundle_sha256"])

    def test_legacy_stage09_gates_rejected(self):
        self.stage09()
        for gate in ("optimization","reaudit"):
            with self.assertRaises(p.PipelineError):self.review09(gate)

    def test_08p_is_real_predecessor(self):
        self.assertEqual(p.STAGES[-3:], ("08", "08P", "09"))
        for stage in p.STAGES[:-2]:
            self.candidate(stage); self.check_all(stage); self.accept(stage)
        with self.assertRaises(p.PipelineError):
            self.candidate("09")
        self.candidate("08P"); self.check_all("08P")
        p.submit(args(stage="08P",candidate="A"),self.root,self.run)
        p.storage(args(stage="08P",candidate="A",quiescent=True),self.root,self.run)
        result=p.complete(args(stage="08P",candidate="A"),self.root,self.run)
        self.assertEqual(result["next_stage"],"09")
        self.candidate("09")

    def test_debt_added_during_performance_blocks_submission(self):
        for stage in p.STAGES[:-2]:
            self.candidate(stage); self.check_all(stage); self.accept(stage)
        self.candidate("08P"); self.check_all("08P")
        p.debt(args(operation="add",id="reset",evidence=str(self.evidence),owner="08",source_stage="08",
                    severity="major",description="reset unstable"),self.root,self.run)
        with self.assertRaises(p.PipelineError):
            p.submit(args(stage="08P",candidate="A"),self.root,self.run)

    def test_final_audit_cannot_edit_model(self):
        self.stage09(submitted=False)
        f = self.root / "work/09A.json"
        f.write_text("not the 08P package")
        with self.assertRaises(p.PipelineError):
            p.register(args(stage="09",candidate="A",file=str(f),asset=[]),self.root,self.run)

    def test_debt_blocks_audit_without_rewriting_checks(self):
        self.stage09(submitted=False)
        p.debt(args(operation="add",id="reset",evidence=str(self.evidence),owner="08",source_stage="08",
                    severity="major",description="reset unstable"),self.root,self.run)
        with self.assertRaises(p.PipelineError):
            p.submit(args(stage="09",candidate="A"),self.root,self.run)
        p.debt(args(operation="accept",id="reset",evidence=str(self.evidence),actor="fixture-human",
                    statement="Scoped fixture exception"),self.root,self.run)
        p.record_check(args(stage="09",candidate="A",name="regression-tests",status="fail",evidence=str(self.evidence)),self.root,self.run)
        with self.assertRaises(p.PipelineError):
            p.submit(args(stage="09",candidate="A"),self.root,self.run)

    def test_direction_does_not_advance(self):
        self.candidate()
        policy=p.read_json(self.root/"policy.json")["stages"]["00"]
        for name in policy["pre_review_checks"]:
            p.record_check(args(stage="00",candidate="A",name=name,status="pass",evidence=str(self.evidence)),self.root,self.run)
        name=policy["post_review_checks"][0]
        with self.assertRaises(p.PipelineError):
            p.record_check(args(stage="00",candidate="A",name=name,status="pass",evidence=str(self.evidence)),self.root,self.run)
        p.direction(args(stage="00",candidate="A",actor="fixture-human",statement="fixture"),self.root,self.run)
        self.assertIsNone(self.run["stages"]["00"]["approved"])
        with self.assertRaises(p.PipelineError): self.candidate("01")
        with self.assertRaises(p.PipelineError): p.submit(args(stage="00",candidate="A"),self.root,self.run)
        self.check_all()
        self.accept()
        self.assertEqual(self.run["stages"]["00"]["approved"],"A")

    def test_revision_invalidates_direction(self):
        self.candidate(); self.check_all()
        self.candidate()
        c=p.get_candidate(self.run,"00","A")
        self.assertNotIn("direction",c)
        self.assertTrue(p.direction_errors(self.root,self.run,"00",c))

    def test_post_review_debt_blocks_early_stage(self):
        self.candidate(); self.check_all()
        p.debt(args(operation="add",id="fault",evidence=str(self.evidence),owner="00",source_stage="00",
                    severity="major",description="fixture defect"),self.root,self.run)
        with self.assertRaises(p.PipelineError): p.submit(args(stage="00",candidate="A"),self.root,self.run)

    def test_storage_subgate_required(self):
        self.candidate(); self.check_all()
        p.submit(args(stage="00",candidate="A"),self.root,self.run)
        with self.assertRaises(p.PipelineError):
            p.complete(args(stage="00",candidate="A"),self.root,self.run)
        with self.assertRaises(p.PipelineError):
            p.storage(args(stage="00",candidate="A",quiescent=False),self.root,self.run)
        p.storage(args(stage="00",candidate="A",quiescent=True),self.root,self.run)
        p.complete(args(stage="00",candidate="A"),self.root,self.run)

    def test_storage_report_tamper_blocks(self):
        self.candidate(); self.check_all()
        p.submit(args(stage="00",candidate="A"),self.root,self.run)
        p.storage(args(stage="00",candidate="A",quiescent=True),self.root,self.run)
        c=p.get_candidate(self.run,"00","A")
        (self.root/c["storage_subgate"]["evidence"]["path"]).write_text("changed")
        with self.assertRaises(p.PipelineError):
            p.complete(args(stage="00",candidate="A"),self.root,self.run)

    def test_old_version_is_not_silently_migrated(self):
        self.run["pack_version"]="2.0.0";p.atomic_json(self.root/"run.json",self.run)
        with self.assertRaises(p.PipelineError):p.load(self.root)

    def test_cycles_profile_and_policy_defaults(self):
        profile=p.read_json(p.PACK/"assets"/"character-profile.template.json")
        policy=p.read_json(p.PACK/"assets"/"stage-policy.json")
        self.assertEqual(profile["render"]["engine"],"CYCLES")
        self.assertEqual(profile["render"]["viewport_shading"],"RENDERED")
        self.assertEqual(profile["benchmark"]["engine"],"CYCLES")
        self.assertEqual(profile["benchmark"]["mode"],"RENDERED")
        self.assertEqual(policy["stage09_human_reviews"],list(p.REVIEW_GATES))

    def test_dependency_budget_no_duplicate_or_automatic_exception(self):
        for i in range(10):
            result = p.attempt(args(dependency="example-addon", method=f"alternative {i}", outcome="failed", evidence=str(self.evidence)), self.root, self.run)
        self.assertTrue(result["exception_eligible_for_review"])
        self.assertFalse(self.run["stages"]["09"]["approved"])
        with self.assertRaises(p.PipelineError):
            p.attempt(args(dependency="example-addon", method="extra", outcome="failed", evidence=str(self.evidence)), self.root, self.run)


def text(value, encoding="utf-8"):
    b = value.encode(encoding); return struct.pack("<i", len(b))+b


def pmx_fixture(version=2.0, deform_types=(), encoding=1, soft=0):
    enc = "utf-8" if encoding else "utf-16-le"
    t = lambda s: text(s, enc)
    data = b"PMX "+struct.pack("<fB", version, 8)+bytes([encoding,0,1,1,1,1,1,1])
    data += t("fixture 日本語")+t("fixture")+t("comment")+t("comment")
    data += struct.pack("<i", len(deform_types))
    for typ in deform_types:
        data += struct.pack("<8fB",0,0,0,0,0,1,0,0,typ)
        if typ == 0: data += struct.pack("<b",-1)
        elif typ in (1,3):
            data += struct.pack("<bbf",-1,-1,0.5)
            if typ == 3: data += struct.pack("<9f",*([0.0]*9))
        else: data += struct.pack("<4b4f",-1,-1,-1,-1,0.25,0.25,0.25,0.25)
        data += struct.pack("<f",1)
    # Faces, textures, materials, bones, morphs, display frames, bodies, joints.
    data += struct.pack("<8i", *([0]*8))
    if version > 2.0: data += struct.pack("<i",soft)+(b"unparsed soft-body fixture" if soft else b"")
    return data


class PmxTests(unittest.TestCase):
    def read(self, data):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/"fixture.pmx"; path.write_bytes(data)
            return pmx.inventory(path)

    def test_all_weight_types_and_unicode(self):
        r = self.read(pmx_fixture(2.1, range(5)))
        self.assertEqual(r["vertices"]["count"],5)
        self.assertEqual(set(r["vertices"]["deform_types"]),{"BDEF1","BDEF2","BDEF4","SDEF","QDEF"})
        self.assertEqual(r["model"]["name_jp"],"fixture 日本語")
        self.assertEqual(r["inventory_status"],"complete")

    def test_utf16(self):
        self.assertEqual(self.read(pmx_fixture(encoding=0))["encoding"],"utf-16-le")

    def test_soft_body_not_silently_supported(self):
        r = self.read(pmx_fixture(2.1, soft=1))
        self.assertEqual(r["inventory_status"],"partial"); self.assertEqual(r["soft_body_count"],1)

    def test_truncation_rejected(self):
        with self.assertRaises(pmx.FormatError): self.read(pmx_fixture()[:-1])

    def test_wrong_signature_rejected(self):
        with self.assertRaises(pmx.FormatError): self.read(b"NOPE"+pmx_fixture()[4:])

    def test_trailing_payload_is_partial(self):
        self.assertEqual(self.read(pmx_fixture()+b"extra")["inventory_status"],"partial")

    def test_invalid_index_width_rejected(self):
        data = bytearray(pmx_fixture()); data[11]=3
        with self.assertRaises(pmx.FormatError): self.read(data)


if __name__ == "__main__": unittest.main()
