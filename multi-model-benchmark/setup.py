#!/usr/bin/env python3
"""Shared manual/agent setup. Does not download models, VMDs, or animations."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys

BENCH = Path(__file__).resolve().parent
ROOT = BENCH.parent
DATA = BENCH / 'data'
INBOX = DATA / 'animation-assets' / 'manual-inbox'
FOLDERS = (
    'animation-assets/manual-inbox/quaternius-ual1',
    'animation-assets/manual-inbox/quaternius-ual2',
    'animation-assets/manual-inbox/mmd-tools-vmd-smoke',
    'animation-assets/manual-inbox/other-vmd',
    'animation-assets/manual-inbox/other-blender',
    'animation-assets/downloads',
    'animation-assets/pmx-vmd',
    'animation-assets/blender-native',
    'animation-assets/retargeted',
    'animation-assets/receipts',
    'runs',
    'reports',
)
INBOX_GUIDE = """MANUAL DOWNLOADS ONLY. No setup/agent downloads these files.

One free Standard ZIP from https://quaternius.itch.io/universal-animation-library
  -> quaternius-ual1/
One free Standard ZIP from https://quaternius.itch.io/universal-animation-library-2
  -> quaternius-ual2/
One raw test.vmd file from https://github.com/MMD-Blender/blender_mmd_tools/blob/main/samples/vmd/test.vmd
  -> mmd-tools-vmd-smoke/

Optional files go into other-vmd/ or other-blender/ for separate review.
After downloading yourself, from repository root run:
  python multi-model-benchmark/assets.py import-inbox
  python multi-model-benchmark/assets.py list
  python multi-model-benchmark/setup.py status

Imported files are copied and checksummed. VMD is a format smoke sample,
not real full-body movement qualification. Retargeting is not automatic.
"""

def init_folders(data=DATA):
    for folder in FOLDERS:
        (data / folder).mkdir(parents=True, exist_ok=True)
    guide = data / 'animation-assets' / 'manual-inbox' / 'README.txt'
    if not guide.exists():
        guide.write_text(INBOX_GUIDE, encoding='utf-8')
    return [data / folder for folder in FOLDERS]

def status():
    print('Repository:', ROOT)
    print('Expected branch: Multi-Model-PMX-Benchmark')
    for program in ('git', 'docker', 'ollama'):
        print(program + ':', shutil.which(program) or 'MISSING (install or authorize agent)')
    print('Python:', sys.version.split()[0])
    print('Your manual download inbox:', INBOX)
    for name, ext in (('quaternius-ual1', '.zip'),
                      ('quaternius-ual2', '.zip'),
                      ('mmd-tools-vmd-smoke', '.vmd')):
        directory = INBOX / name
        found = [p for p in directory.iterdir() if p.is_file() and
                 not p.is_symlink() and p.suffix.lower() == ext] if directory.is_dir() else []
        print(' ', name, ':', str(len(found)) + ' file(s)' if found else 'WAITING FOR USER')
    print('After downloading: python multi-model-benchmark/assets.py import-inbox')
    print('Smoke later: python multi-model-benchmark/smoke/run_stage03_smoke.py --image PINNED_BLENDER_IMAGE')

def prepare():
    init_folders()
    commands = [
        [sys.executable, '-m', 'unittest', 'discover', '-s', 'multi-model-benchmark/tests', '-v'],
        [sys.executable, 'astra-qwen-weight-lab/fixtures.py', 'generate'],
    ]
    for command in commands:
        print('RUN:', ' '.join(command), flush=True)
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode != 0:
            print('STOP: local test/fixture step failed; no readiness claim.', file=sys.stderr)
            return result.returncode
    status()
    print('PREPARE COMPLETE: no animation assets or Blender runtime were downloaded/tested.')
    return 0

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('init', 'prepare', 'status'))
    args = parser.parse_args()
    if sys.version_info < (3, 10):
        parser.error('Python 3.10+ required')
    if args.command == 'init':
        init_folders()
        status()
    elif args.command == 'prepare':
        return prepare()
    else:
        status()
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
