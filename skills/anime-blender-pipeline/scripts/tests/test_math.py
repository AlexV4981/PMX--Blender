"""Numerical/reference tests, not live Blender/character qualification."""
import importlib.util
import math
from pathlib import Path
import tempfile
import unittest
import numpy as np

spec=importlib.util.spec_from_file_location('math_tools',Path(__file__).resolve().parents[1]/'math_tools.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

# Selected published cases: Sharma/Wu/Dalal (2005), including difficult hue/zero-chroma cases.
# Source: https://hajim.rochester.edu/ece/sites/gsharma/ciede2000/dataNprograms/ciede2000testdata.txt
CASES='''50 2.6772 -79.7751 50 0 -82.7485 2.0425
50 3.1571 -77.2803 50 0 -82.7485 2.8615
50 2.8361 -74.0200 50 0 -82.7485 3.4412
50 -1.3802 -84.2814 50 0 -82.7485 1.0000
50 -1.1848 -84.8006 50 0 -82.7485 1.0000
50 -.9009 -85.5211 50 0 -82.7485 1.0000
50 0 0 50 -1 2 2.3669
50 -1 2 50 0 0 2.3669
50 2.49 -.001 50 -2.49 .0009 7.1792
50 2.49 -.001 50 -2.49 .0010 7.1792
50 2.49 -.001 50 -2.49 .0011 7.2195
50 2.49 -.001 50 -2.49 .0012 7.2195
50 -.001 2.49 50 .0009 -2.49 4.8045
50 -.001 2.49 50 .001 -2.49 4.8045
50 -.001 2.49 50 .0011 -2.49 4.7461
50 2.5 0 50 0 -2.5 4.3065
60.2574 -34.0099 36.2677 60.4626 -34.1751 39.4387 1.2644
63.0109 -31.0961 -5.8663 62.8187 -29.7946 -4.0864 1.2630
61.2901 3.7196 -5.3901 61.4292 2.2480 -4.9620 1.8731
35.0831 -44.1164 3.7933 35.0232 -40.0716 1.5901 1.8645'''

class MathTests(unittest.TestCase):
    def test_published_twenty_cases(self):
        for row in CASES.splitlines():
            v=list(map(float,row.split()))
            with self.subTest(case=row):self.assertAlmostEqual(float(m.ciede2000(v[:3],v[3:6])),v[6],delta=.000051)
    def test_identity_and_symmetry(self):
        a=np.array([[50,0,0],[20,1,2],[80,-30,50]],float);b=a+np.array([2,-1,3])
        np.testing.assert_allclose(m.ciede2000(a,a),0)
        np.testing.assert_allclose(m.ciede2000(a,b),m.ciede2000(b,a))
    def test_srgb_known_black_white_red(self):
        np.testing.assert_allclose(m.srgb_to_lab([0,0,0]),[0,0,0],atol=1e-6)
        np.testing.assert_allclose(m.srgb_to_lab([1,1,1]),[100,0,0],atol=3e-5)
        np.testing.assert_allclose(m.srgb_to_lab([1,0,0]),[53.2408,80.0925,67.2032],atol=.0002)
    def test_bad_inputs(self):
        for a in [[float('nan'),0,0],[2,0,0],[-1,0,0]]:
            with self.assertRaises(ValueError):m.srgb_to_lab(a)
        with self.assertRaises(ValueError):m.summarize([])
        with self.assertRaises(ValueError):m.summarize([float('inf')])
    def test_strict_threshold_and_tail(self):
        self.assertFalse(m.summarize([3,3],3)['proposed_p95_target_met'])
        r=m.summarize([0]*99+[20],3)
        self.assertTrue(r['proposed_p95_target_met']);self.assertEqual(r['maximum'],20)
        self.assertEqual(r['fraction_at_or_above_threshold'],.01)
    def test_rigid_fit(self):
        p=np.array([[0,0,0],[1,0,0],[0,1,0],[0,0,1]],float)
        R=np.array([[0,-1,0],[1,0,0],[0,0,1]],float);t=np.array([3,5,7])
        out=m.rigid_alignment(p,p@R.T+t)
        np.testing.assert_allclose(out['rotation'],R,atol=1e-12)
        np.testing.assert_allclose(out['translation'],t,atol=1e-12)
        self.assertLess(out['summary']['maximum'],1e-12)
    def test_reflection_not_hidden(self):
        p=np.array([[0,0,0],[1,0,0],[0,1,0],[0,0,1]],float)
        q=p*np.array([-1,1,1]);out=m.rigid_alignment(p,q)
        self.assertAlmostEqual(out['determinant'],1)
        self.assertGreater(out['summary']['maximum'],.1)
    def test_collinear_rejected(self):
        with self.assertRaises(ValueError):m.rigid_alignment([[0,0,0],[1,0,0],[2,0,0]],[[0,0,0],[1,0,0],[2,0,0]])
    def test_quaternion_sign_and_rotation(self):
        self.assertAlmostEqual(float(m.quaternion_angle([1,0,0,0],[-2,0,0,0])),0)
        self.assertAlmostEqual(float(m.quaternion_angle([1,0,0,0],[math.sqrt(.5),0,0,math.sqrt(.5)])),math.pi/2)
        with self.assertRaises(ValueError):m.quaternion_angle([0,0,0,0],[1,0,0,0])
    def test_color_report_conditions_and_separate_regions(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'fixture.txt').write_text('Synthetic fixture only')
            data={'encoding':'display-srgb','matched_conditions_evidence':['fixture.txt'],
                  'regions':[{'name':'skin','reference_rgb':[[.5,.5,.5]],'candidate_rgb':[[.5,.5,.5]]},
                             {'name':'iris','reference_rgb':[[1,0,0]],'candidate_rgb':[[0,0,1]]}]}
            out=m.color_report(data,p);self.assertEqual(len(out['regions']),2)
            self.assertTrue(out['regions'][0]['proposed_p95_target_met'])
            self.assertFalse(out['regions'][1]['proposed_p95_target_met'])
            data['encoding']='scene-linear'
            with self.assertRaises(ValueError):m.color_report(data,p)
    def test_missing_evidence_rejected(self):
        with self.assertRaises(ValueError):m.color_report({'encoding':'display-srgb','matched_conditions_evidence':['missing']},Path('/tmp'))

if __name__=='__main__':unittest.main()
