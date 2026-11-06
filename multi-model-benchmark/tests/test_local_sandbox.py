import base64
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evidence import local_sandbox as s

class HostBoundaryTests(unittest.TestCase):
    def test_duplicate_keys_and_nonfinite_refused(self):
        for raw in ('{"exit_code":0,"exit_code":1,"files":{},"log":""}', '{"exit_code":NaN,"files":{},"log":""}'):
            with self.assertRaises(ValueError): s.decode_packet(raw.encode(), set())
    def test_unexpected_paths_and_bad_encoding_refused(self):
        for files in ({'../escape':'AA=='}, {'candidate.blend':'!'}, {'candidate.blend':[] }):
            with self.assertRaises(ValueError): s.decode_packet(json.dumps({'exit_code':0,'files':files,'log':''}).encode(), {'candidate.blend'})
    def test_only_fixed_bounded_files_are_decoded(self):
        data=s.decode_packet(json.dumps({'exit_code':0,'files':{'result.json':base64.b64encode(b'{}').decode()},'log':''}).encode(), {'result.json'})
        self.assertEqual(data['files'], {'result.json':b'{}'})
    def test_no_host_output_mounts(self):
        cmd=s.bwrap_command([], '/lab/probe.py', 'probe')
        self.assertNotIn('--bind',cmd)
        self.assertIn('--disable-userns',cmd)
        self.assertIn('--unshare-user',cmd)
    def test_environment_and_hard_limits_required(self):
        cmd=s.service_command(['true'],'pmx-test',10,256*1024*1024)
        for value in ('NoNewPrivileges=yes','MemorySwapMax=0','TasksMax=64','KillMode=control-group'):
            self.assertIn(value,cmd)


class VerifierFiniteTests(unittest.TestCase):
    def test_nonfinite_and_duplicate_result_json_refused(self):
        from evidence.trusted_verifier import strict_result_json
        for text in ('{"x":NaN}', '{"x":Infinity}', '{"x":1e999}', '{"x":1,"x":2}'):
            with self.assertRaises(ValueError): strict_result_json(text)
    def test_stage06_nonfinite_numeric_strings_refused(self):
        from evidence.trusted_verifier import validate_motion_samples
        for value in ('NaN','Infinity',float('nan'),True):
            with self.assertRaises(ValueError):
                validate_motion_samples({'samples':[{'angle_deg':value,'tip':[0,0,0]}]})


class ReadinessTests(unittest.TestCase):
    def test_missing_readiness_receipt_blocks_execution(self):
        import tempfile
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp, patch.object(s, 'READY', Path(tmp)/'absent'):
            with self.assertRaisesRegex(RuntimeError, 'readiness receipt'):
                s.require_ready()

    def test_stale_policy_blocks_execution(self):
        import tempfile
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            receipt=Path(tmp)/'ready.json';receipt.write_text('{"policy_sha256":"old"}')
            with patch.object(s,'READY',receipt), patch.object(s,'policy_fingerprint',return_value='new'):
                with self.assertRaisesRegex(RuntimeError,'stale'):
                    s.require_ready()


class EvidenceReceiptTests(unittest.TestCase):
    def test_changed_security_evidence_blocks_readiness(self):
        import tempfile
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); receipt={'evidence_sha256':{name:'0'*64 for name in s.EVIDENCE_FILES}}
            for name in s.EVIDENCE_FILES:(root/name).write_text('changed')
            with patch.object(s,'READY',root/'ready.json'):
                with self.assertRaisesRegex(RuntimeError,'evidence'):
                    s.verify_receipts(receipt)
    def test_missing_required_security_receipts_block_readiness(self):
        with self.assertRaisesRegex(RuntimeError,'evidence'):
            s.verify_receipts({'evidence_sha256':{}})


class RuntimeIdentityTests(unittest.TestCase):
    def test_identity_binds_verifier_policy_not_only_blender_binary(self):
        from unittest.mock import patch
        with patch.object(s,'policy_fingerprint',return_value='a'*64):
            self.assertEqual(s.runtime_identity(),'local-blender-bwrap-v3@sha256:'+'a'*64)

if __name__=='__main__':unittest.main()
