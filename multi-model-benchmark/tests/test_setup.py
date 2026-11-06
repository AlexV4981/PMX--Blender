"""Offline checks for the shared manual/agent setup."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

FILE = Path(__file__).resolve().parents[1] / 'setup.py'
spec = importlib.util.spec_from_file_location('benchmark_setup', FILE)
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)

class SetupTests(unittest.TestCase):
    def test_init_creates_manual_handoff(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paths = setup.init_folders(root)
            self.assertEqual(len(paths), len(setup.FOLDERS))
            self.assertTrue(all(path.is_dir() for path in paths))
            inbox = root / 'animation-assets/manual-inbox'
            self.assertIn('MANUAL DOWNLOADS ONLY', (inbox / 'README.txt').read_text())
            self.assertTrue((inbox / 'mmd-tools-vmd-smoke').is_dir())

    def test_init_keeps_existing_user_notes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            setup.init_folders(root)
            guide = root / 'animation-assets/manual-inbox/README.txt'
            guide.write_text('my notes')
            setup.init_folders(root)
            self.assertEqual(guide.read_text(), 'my notes')

    def test_prepare_does_not_download(self):
        import inspect
        src = inspect.getsource(setup.prepare)
        self.assertNotIn('urllib', src)
        self.assertNotIn('assets.py', src)
        self.assertIn('fixtures.py', src)

if __name__ == '__main__':
    unittest.main()
