import importlib.util
from pathlib import Path
import tempfile
import unittest
import os

spec=importlib.util.spec_from_file_location("dedup",Path(__file__).parents[1]/"scripts/artifact_dedup.py")
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)

class DedupTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.scope=self.root/"audit";self.scope.mkdir()
        for name,data in (("a",b"abc"),("b",b"abc"),("c",b"abd")):
            (self.scope/name).write_bytes(data)
    def tearDown(self): self.tmp.cleanup()
    def test_plan_exact_only(self):
        r=d.run(self.root,["audit"],min_bytes=1)
        self.assertEqual(r["logical_duplicate_bytes"],3)
        self.assertEqual(r["kernel_reported_shared_bytes"],0)
        self.assertEqual(len(r["groups"]),1)
    def test_apply_preserves_paths_and_bytes(self):
        r=d.run(self.root,["audit"],True,1,share=lambda a,b,n:(n,"shared"))
        self.assertEqual(r["kernel_reported_shared_bytes"],3)
        self.assertEqual((self.scope/"b").read_bytes(),b"abc")
        self.assertEqual((self.scope/"c").read_bytes(),b"abd")
    def test_unsupported_keeps_copy(self):
        def unsupported(*a): raise OSError("unsupported")
        r=d.run(self.root,["audit"],True,1,share=unsupported)
        self.assertEqual(r["groups"][0]["copies"][0]["status"],"retained-unsupported")
        self.assertTrue((self.scope/"b").exists())
    def test_hardlinks_not_counted_twice(self):
        os.link(self.scope/"b",self.scope/"z")
        r=d.run(self.root,["audit"],min_bytes=1)
        self.assertEqual(r["logical_duplicate_bytes"],3)
    def test_symlinks_and_outside_scope(self):
        (self.root/"outside").write_bytes(b"abc")
        (self.scope/"link").symlink_to(self.root/"outside")
        r=d.run(self.root,["audit"],min_bytes=1)
        self.assertEqual(r["logical_duplicate_bytes"],3)
        with self.assertRaises(ValueError): d.run(self.root,["../"],min_bytes=1)
    def test_mutation_blocks(self):
        def bad(a,b,n): b.write_bytes(b"xxx");return n,"shared"
        r=d.run(self.root,["audit"],True,1,share=bad)
        self.assertEqual(r["status"],"blocked")

if __name__=="__main__": unittest.main()
