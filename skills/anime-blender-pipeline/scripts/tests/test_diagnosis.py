"""Check evidence semantics and texture observation using generated tiny fixtures."""
import copy
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

def mod(name):
    s=importlib.util.spec_from_file_location(name,Path(__file__).resolve().parents[1]/(name+'.py'))
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
mp=mod('material_plan');ta=mod('texture_audit')

class PlanTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name)
        (self.base/'e.txt').write_text('synthetic evidence, not actual model acceptance')
        (self.base/'map.png').write_bytes(b'synthetic identity fixture')
        x={'file':'map.png','sha256':hashlib.sha256(b'synthetic identity fixture').hexdigest(),
           'role':'base-color','role_evidence':['e.txt'],'color_space':'sRGB','color_space_rationale':'fixture',
           'image_datablock':'image/color','uv_map':'UVMap','required_for_fidelity':True}
        self.plan={'schema_version':1,'qualification':'plan_only_not_visual_acceptance','baseline_evidence':['e.txt'],
          'materials':[{'id':'m0','owner':'mesh/slot0','status':'proposed','diagnostic_evidence':['e.txt'],
                       'output_method':'fixture only','maps':[x],'regression_evidence':['e.txt']}]}
    def tearDown(self):self.tmp.cleanup()
    def test_valid_structure_only(self):self.assertEqual(mp.validate(self.plan,self.base),[])
    def test_wrong_hash(self):
        self.plan['materials'][0]['maps'][0]['sha256']='bad'
        self.assertTrue(mp.validate(self.plan,self.base))
    def test_no_fabricated_path(self):
        self.plan['baseline_evidence']=['nonexistent.png'];self.assertTrue(mp.validate(self.plan,self.base))
    def test_required_unknown_blocks(self):
        x=self.plan['materials'][0]['maps'][0];x.update(role='unknown',unknown_reason='not identified',connection='unconnected')
        self.assertTrue(mp.validate(self.plan,self.base))
        self.plan['materials'][0]['status']='blocked';self.assertEqual(mp.validate(self.plan,self.base),[])
    def test_data_srgb_requires_actual_exception(self):
        self.plan['materials'][0]['maps'][0]['role']='normal-tangent'
        self.assertTrue(mp.validate(self.plan,self.base))
        self.plan['materials'][0]['maps'][0]['color_space']='Non-Color'
        self.assertEqual(mp.validate(self.plan,self.base),[])
    def test_packed_channels_explicit(self):
        x=self.plan['materials'][0]['maps'][0];x.update(role='packed-data',color_space='Non-Color',channel_roles={'R':'roughness'})
        self.assertTrue(mp.validate(self.plan,self.base))
        x['channel_roles']={'R':'roughness','G':'unused','B':'unused','A':'unused'}
        self.assertEqual(mp.validate(self.plan,self.base),[])

class TextureTests(unittest.TestCase):
    def test_channels_and_source_immutable(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            b=Path(d);f=b/'texture.png';im=Image.new('RGBA',(2,1));im.putdata([(255,0,128,0),(0,255,128,255)]);im.save(f)
            original=f.read_bytes();r=ta.audit([f],b/'out');x=r['images'][0]
            self.assertEqual(f.read_bytes(),original);self.assertEqual(x['channels']['A']['zero_fraction'],.5)
            self.assertEqual(x['channels']['A']['one_fraction'],.5);self.assertEqual(x['channels']['B']['min'],128)
            self.assertTrue((b/'out'/x['sheet']).is_file())
            with self.assertRaises(ValueError):ta.audit([f],b/'out')
    def test_high_depth_is_not_silently_downsampled(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            b=Path(d);f=b/'height.tif';Image.new('I;16',(1,1)).save(f)
            self.assertEqual(ta.audit([f],b/'out')['images'][0]['status'],'unsupported')
    def test_decode_error_is_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            b=Path(d);f=b/'bad.png';f.write_bytes(b'not an image')
            self.assertEqual(ta.audit([f],b/'out')['images'][0]['status'],'blocked')

if __name__=='__main__':unittest.main()
