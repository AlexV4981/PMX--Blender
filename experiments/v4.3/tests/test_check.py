import importlib.util
import json
from pathlib import Path
import unittest

root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("pilot_check",root/"check.py")
check=importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)

class TestPilot(unittest.TestCase):
    def load(self,name):
        return json.loads((root/name).read_text())
    def test_templates(self):
        for kind,name in (("cases","cases.json"),("scenarios","scenarios.json"),("permissions","permissions.template.json")):
            self.assertEqual(check.validate(self.load(name),kind)["qualification"],"not performed")
    def test_duplicate_case(self):
        d=self.load("cases.json")
        d["cases"].append(d["cases"][0])
        with self.assertRaises(ValueError):
            check.validate(d,"cases")
    def test_false_verification(self):
        d=self.load("cases.json")
        d["cases"][0]["status"]="verified"
        with self.assertRaises(ValueError):
            check.validate(d,"cases")
    def test_unknown_training(self):
        d=self.load("permissions.template.json")
        d["assets"][0]["training"]="allowed"
        with self.assertRaises(ValueError):
            check.validate(d,"permissions")
    def test_permission_separation(self):
        d=self.load("permissions.template.json")
        r=d["assets"][0]
        r.update(creator="Example",source="example",modification="allowed",license_evidence=[{"use":"modification","ref":"example"}])
        check.validate(d,"permissions")
        r["training"]="allowed"
        with self.assertRaises(ValueError):
            check.validate(d,"permissions")

if __name__=="__main__":
    unittest.main()
