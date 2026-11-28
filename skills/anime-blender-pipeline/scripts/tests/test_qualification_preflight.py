import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location("preflight",Path(__file__).parents[1]/"qualification_preflight.py")
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)

class PreflightTests(unittest.TestCase):
    def test_screen(self):
        self.assertTrue(p.screen(.01,2)["screened_out"])
        self.assertFalse(p.screen(.1,2)["screened_out"])
        with self.assertRaises(ValueError): p.screen(float("nan"),2)
    def test_coverage(self):
        self.assertEqual(p.coverage(25,list(range(1,25)),["normals"],{"normals":True})["status"],"blocked")
        self.assertEqual(p.coverage(25,[25],["normals"],{"normals":False})["status"],"blocked")
        self.assertEqual(p.coverage(25,[25],["normals"],{"normals":True})["status"],"eligible")
    def test_dependencies(self):
        self.assertFalse(p.reusable({}, {}, ["fixture"]))
        self.assertFalse(p.reusable({"fixture":"a"*64},{"fixture":"b"*64},["fixture"]))
        self.assertTrue(p.reusable({"fixture":"a"*64},{"fixture":"a"*64},["fixture"]))
