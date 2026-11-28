import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

scripts=Path(__file__).resolve().parents[1]
def module(name):
    spec=importlib.util.spec_from_file_location(name,scripts/(name+".py"))
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m
a=module("stage_archive")
p=module("pipeline")

class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        base=Path(self.tmp.name)
        self.root=base/"run"
        self.root.mkdir()
        self.store=a.Store(self.root,local=base/"remote")
        self.run={"created":"fixture","policy_sha256":"fixture","sources":[],
                  "stages":{"02":{"approved":"A","candidates":{"A":{"artifacts":[{"path":"work/02/approved.blend"}]}}}}}
        self.rel="work/02/retired.blend"
        self.file=self.root/self.rel
        self.file.parent.mkdir(parents=True)
        self.file.write_bytes(b"old-model"*100)
        (self.root/"work/02/approved.blend").write_bytes(b"approved")
    def tearDown(self):
        self.tmp.cleanup()
    def bundle(self):
        res=a.archive(self.root,self.store,self.run,"02",{"paths":["work/02"]})
        return a.get_manifest(self.root,self.store,res["manifest"],self.run)
    def plan(self,paths=None,keep=None):
        return {"retired":paths or [self.rel],"keep":keep or [],"dependencies_reviewed":True,"reason":"test only"}
    def test_roundtrip_and_no_overwrite(self):
        m,entries=self.bundle()
        content=self.file.read_bytes()
        self.assertTrue(self.file.exists())
        a.evict(self.root,self.store,self.run,m,entries,self.plan())
        self.assertFalse(self.file.exists())
        self.assertEqual(a.restore(self.root,self.store,entries[self.rel]),"restored")
        self.assertEqual(self.file.read_bytes(),content)
        self.file.write_bytes(b"new")
        with self.assertRaises(ValueError):
            a.restore(self.root,self.store,entries[self.rel])
    def test_protected_and_dependency(self):
        m,e=self.bundle()
        for plan in (self.plan(["work/02/approved.blend"]),self.plan(keep=["work/02"])):
            with self.assertRaises(ValueError):
                a.evict(self.root,self.store,self.run,m,e,plan)
        self.assertTrue(self.file.exists())
    def test_corrupt_remote(self):
        m,e=self.bundle()
        self.store.target(a.object_key(e[self.rel]["sha256"])).write_bytes(b"bad")
        with self.assertRaises((OSError,ValueError,EOFError)):
            a.evict(self.root,self.store,self.run,m,e,self.plan())
        self.assertTrue(self.file.exists())
    def test_changed_local(self):
        m,e=self.bundle()
        self.file.write_bytes(b"changed")
        with self.assertRaises(ValueError):
            a.evict(self.root,self.store,self.run,m,e,self.plan())
        self.assertEqual(self.file.read_bytes(),b"changed")
    def test_path_and_wrong_run(self):
        for name in ("../outside","work/../run.json","/work/02/a","work//02/a"):
            with self.assertRaises(ValueError):
                a.safe_path(self.root,name)
        self.run["stages"]["02"]["approved"]=None
        with self.assertRaises(ValueError):
            self.bundle()
    def test_relative_and_legacy_sources(self):
        self.assertEqual(p.source_path(self.root,{"path":self.rel}),self.file)
        self.assertEqual(p.source_path(self.root,{"path":str(self.file)}),self.file)
        with self.assertRaises(p.PipelineError):
            p.source_path(self.root,{"path":"../outside"})
    def test_recover_manifest(self):
        res=a.archive(self.root,self.store,self.run,"02",{"paths":[self.rel]})
        (self.root/a.INDEX/(res["manifest"]+".json")).unlink()
        _,e=a.get_manifest(self.root,self.store,res["manifest"],self.run)
        self.assertIn(self.rel,e)
        self.run["created"]="different"
        with self.assertRaises(ValueError):
            a.get_manifest(self.root,self.store,res["manifest"],self.run)

if __name__=="__main__":
    unittest.main()
