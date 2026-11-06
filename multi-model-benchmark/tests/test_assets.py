"""Offline checks for fixture downloader; no internet or Blender required."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile

MOD = Path(__file__).resolve().parents[1] / 'assets.py'
spec = importlib.util.spec_from_file_location('motion_assets', MOD)
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

class MotionAssetTests(unittest.TestCase):
    def test_all_automated_assets_have_real_source_pages(self):
        self.assertEqual(set(a.CATALOG), {'quaternius-ual1','quaternius-ual2','mmd-tools-vmd-smoke'})
        for item in a.CATALOG.values():
            self.assertTrue(item['page'].startswith('https://'))
            self.assertTrue(item['endpoint'] is None or item['endpoint'].startswith('https://'))

    def test_extract_only_motion_files(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            z=root/'source.zip'
            with zipfile.ZipFile(z,'w') as w:
                w.writestr('Unreal-Godot/Walk.glb', b'glb sample')
                w.writestr('Unity/Jump.fbx', b'fbx sample')
                w.writestr('README.sh', b'bad executable')
            old=a.DATA
            try:
                a.DATA=root
                out=a.extract_motion_zip(z,root/'unpacked')
            finally:
                a.DATA=old
            self.assertEqual(len(out),2)
            self.assertFalse((root/'unpacked'/'README.sh').exists())

    def test_archive_traversal_refused(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            z=root/'bad.zip'
            with zipfile.ZipFile(z,'w') as w:w.writestr('../escape.glb',b'no')
            with self.assertRaises(ValueError):a.extract_motion_zip(z,root/'out')

    def test_empty_or_non_motion_archive_refused(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            z=root/'empty.zip'
            with zipfile.ZipFile(z,'w') as w:w.writestr('README.txt','hi')
            with self.assertRaises(ValueError):a.extract_motion_zip(z,root/'out')

    def test_inbox_empty_does_not_download(self):
        with tempfile.TemporaryDirectory() as td:
            old = a.DATA
            try:
                a.DATA = Path(td)
                self.assertEqual(a.import_inbox(), 0)
                self.assertFalse((a.DATA / 'downloads').exists())
            finally:
                a.DATA = old

    def test_user_supplied_vmd_import_is_repeatable(self):
        with tempfile.TemporaryDirectory() as td:
            old = a.DATA
            try:
                a.DATA = Path(td)
                folder = a.DATA / 'manual-inbox/mmd-tools-vmd-smoke'
                folder.mkdir(parents=True)
                (folder / 'test.vmd').write_bytes(b'Vocaloid Motion Data 0002' + b'0' * 75)
                self.assertEqual(a.import_inbox('mmd-tools-vmd-smoke'), 0)
                self.assertTrue(a.verify('mmd-tools-vmd-smoke')[0])
                self.assertEqual(a.import_inbox('mmd-tools-vmd-smoke'), 0)
            finally:
                a.DATA = old

    def test_ambiguous_downloads_refused(self):
        with tempfile.TemporaryDirectory() as td:
            old = a.DATA
            try:
                a.DATA = Path(td)
                folder = a.DATA / 'manual-inbox/mmd-tools-vmd-smoke'
                folder.mkdir(parents=True)
                (folder / 'first.vmd').write_bytes(b'Vocaloid Motion Data 0002')
                (folder / 'second.vmd').write_bytes(b'Vocaloid Motion Data 0002')
                self.assertEqual(a.import_inbox('mmd-tools-vmd-smoke'), 2)
                self.assertFalse((a.DATA / 'downloads').exists())
            finally:
                a.DATA = old


if __name__=='__main__':unittest.main()
