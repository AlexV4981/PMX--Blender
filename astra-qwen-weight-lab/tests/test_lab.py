"""CPU-only unit tests: no Ollama, Blender, GPU or internet required."""
import importlib.util
import json
from pathlib import Path
from unittest import mock
import tempfile
import unittest

HERE=Path(__file__).resolve().parents[1]

def load(name):
    spec=importlib.util.spec_from_file_location("active_"+name,HERE/(name+".py"))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

fixtures=load("fixtures")
pilot=load("pilot")
modelfiles=load("modelfiles")
oracle=load("blender_oracle")
score=load("score")
sandbox=load("sandbox")
training=load("train_7b")

class Active7BTests(unittest.TestCase):
    def test_exactly_20_per_stage(self):
        rows=fixtures.cases()
        self.assertEqual(len(rows),80)
        self.assertEqual({s:sum(x["stage"]==s for x in rows) for s in ("03","04","05","06")},
                         {s:20 for s in ("03","04","05","06")})
        self.assertEqual(len({x["case_id"] for x in rows}),80)
        self.assertEqual(len({x["fixture_family"] for x in rows}),20)

    def test_stage04_only_arm_and_no_pole(self):
        self.assertTrue(all("UNSET" in x["prompt"] and "LEFT ARM" in x["prompt"] and
                          "pole" in x["prompt"].lower() for x in fixtures.cases()
                          if x["stage"]=="04"))
        self.assertNotIn("00",pilot.STAGES)

    def test_modelfile_embeds_actual_reference(self):
        txt=modelfiles.render("04","qwen2.5-coder:7b-instruct-q4_K_M","SOME VERIFIED REST SPACE DOC")
        self.assertIn("SOME VERIFIED REST SPACE DOC",txt)
        self.assertIn("No pole-target placement",txt)
        self.assertIn("FROM qwen2.5-coder:7b-instruct-q4_K_M",txt)

    def test_syntax_only_not_execution(self):
        self.assertFalse(pilot.syntax("def bad(: pass")["valid"])
        self.assertIn("missing solve(scene) function",pilot.syntax("pass")["warnings"])
        self.assertTrue(pilot.syntax("def solve(scene): return {}")["valid"])

    def test_blender_requires_external_sandbox(self):
        with mock.patch.dict("os.environ",{},clear=True):
            with self.assertRaises(RuntimeError):oracle.assert_safe_environment()

    def test_score_blocks_fake_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            f=Path(tmp)/"response.json";o=Path(tmp)/"oracle.json"
            f.write_text(json.dumps({"case_id":"stage03-synthetic-001","stage":"03",
                 "result":{"code":"def solve(scene): return {}"}}))
            o.write_text(json.dumps({"case_id":"stage03-synthetic-001","stage":"03",
                 "blender_executed":False}))
            with mock.patch.object(score,"DATA",Path(tmp)):
                args=type("A",(),{"response":f,"oracle":o,"out":Path(tmp)/"v.json"})()
                with self.assertRaises(score.ScoreError):score.bind(args)

    def test_unpinned_sandbox_image_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            home=Path(tmp);case=home/"case.json";src=home/"candidate.py"
            case.write_text(json.dumps({"stage":"06","synthetic":True}))
            src.write_text("def solve(scene):return {}")
            args=type("A",(),{"case":case,"source":src,"out":home/"verdict.json","image":"blender:latest"})()
            with mock.patch.object(sandbox,"DATA",home):
                with self.assertRaises(sandbox.SandboxError):sandbox.build(args)

    def test_lora_refuses_unsupported_checkpoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)
            (base/"config.json").write_text(json.dumps({
                "model_type":"qwen2","hidden_size":1536,"num_hidden_layers":28}))
            (base/"model.safetensors").write_bytes(b"fixture-only")
            with self.assertRaises(training.TrainError):
                training.local_base(base)

    def test_training_split_must_be_disjoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            data={"case_id":"row-001","group_id":"family-a","prompt":"test",
                  "completion":"verified","source_type":"synthetic","verified_by":"oracle"}
            for name in ("train","validation","holdout"):
                (root/(name+".jsonl")).write_text(json.dumps(data)+"\n")
            with mock.patch.object(training,"DATA",root):
                with self.assertRaises(training.TrainError):
                    training.validate(*(root/(n+".jsonl") for n in ("train","validation","holdout")))

    def test_no_08b_model_as_active_base(self):
        cfg=json.loads((HERE/"config.json").read_text())
        self.assertEqual(cfg["base_ollama_tag"],"qwen2.5-coder:7b-instruct-q4_K_M")
        self.assertFalse(cfg["pilot"]["retry"]["production_enabled"])
        self.assertFalse(cfg["qualification"]["qualified"])

if __name__=="__main__":unittest.main()
