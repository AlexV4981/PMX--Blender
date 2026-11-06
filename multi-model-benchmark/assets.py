#!/usr/bin/env python3
"""Download public premade test motions without installing AI models.

Source URLs are preserved in the manifest; downloads require internet access on the
operator's machine. This script does NOT assert the motions have been retargeted or
qualified on any character. No third-party executable code is run.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import ssl
import tempfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data' / 'animation-assets'
CATALOG = {
  'quaternius-ual1': {
    'method':'manual-zip',
    'page':'https://quaternius.itch.io/universal-animation-library',
    'endpoint':None,
    'filename':'quaternius-ual1-standard.zip',
    'sha256':None,
    'license':'CC0-1.0', 'track':'blender-native',
    'notes':'Download free Standard pack from publisher; manually check source/license before importing.'},
  'quaternius-ual2': {
    'method':'manual-zip',
    'page':'https://quaternius.itch.io/universal-animation-library-2',
    'endpoint':None,
    'filename':'quaternius-ual2-standard.zip',
    'sha256':None,
    'license':'CC0-1.0','track':'blender-native',
    'notes':'Download free Standard pack from publisher; manually check source/license before importing.'},
  'mmd-tools-vmd-smoke': {
    'method':'github-raw',
    'page':'https://github.com/MMD-Blender/blender_mmd_tools/blob/main/samples/vmd/test.vmd',
    'endpoint':'https://raw.githubusercontent.com/MMD-Blender/blender_mmd_tools/main/samples/vmd/test.vmd',
    'filename':'mmd-tools-test.vmd', 'sha256': None, 'license':'check-upstream-repository',
    'track':'pmx-vmd',
    'notes':'Upstream VMD test fixture, format/parser smoke only. NOT full-body qualification; verify sample terms.'}
}

MAX_DOWNLOAD = 60 * 1024 * 1024  # Small direct VMD downloads only
MAX_IMPORT = 1024 * 1024 * 1024  # Operator-supplied ZIPs may be large
MAX_UNPACK = 2 * 1024 * 1024 * 1024
ALLOWED_SUFFIXES = {'.glb', '.fbx', '.bvh'}


def digest_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def _read_url(url, limit=MAX_DOWNLOAD):
    if not url.startswith('https://'):
        raise ValueError('HTTPS required')
    req = urllib.request.Request(url, headers={'User-Agent':'PMX-Blender-Fixture-Downloader/1.0'})
    with urllib.request.urlopen(req, timeout=45, context=ssl.create_default_context()) as response:
        if not response.geturl().startswith('https://'):
            raise ValueError('insecure redirect')
        raw = response.read(limit + 1)
        if len(raw) > limit:
            raise ValueError('oversized download')
        return raw



def extract_motion_zip(archive, destination):
    """Extract *only* motion formats, without traversal, symlinks or zip bombs."""
    results = []
    total = 0
    with zipfile.ZipFile(archive) as z:
        infos = z.infolist()
        if len(infos) > 1000:
            raise ValueError('too many archive entries')
        approved = []
        for info in infos:
            name = info.filename.replace('\\', '/')
            path = PurePosixPath(name)
            if info.is_dir() or path.suffix.lower() not in ALLOWED_SUFFIXES:
                continue
            if path.is_absolute() or '..' in path.parts or any(not x or x == '.' for x in path.parts):
                raise ValueError('unsafe archive path')
            if ((info.external_attr >> 16) & 0o170000) == 0o120000:
                raise ValueError('archive symlink not allowed')
            total += info.file_size
            if info.file_size > MAX_UNPACK or total > MAX_UNPACK:
                raise ValueError('archive unpack limit exceeded')
            approved.append((info, path))
        if not approved:
            raise ValueError('no supported Blender motion files in archive')
        for info, relative in approved:
            dest = destination.joinpath(*relative.parts)
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists():
                raise ValueError('refusing to overwrite extracted motion')
            with z.open(info) as source, open(dest, 'xb') as output:
                shutil.copyfileobj(source, output, length=1024*1024)
            results.append({'path':str(dest.relative_to(DATA)), 'sha256':digest_file(dest), 'bytes':dest.stat().st_size})
    return results


def fetch(name, local_file=None):
    """Fetch an upstream direct file or import manually downloaded publisher ZIP.

    First acquisition records the actual digest; subsequent calls verify it.
    An unpinned first download is NOT a reproducible frozen benchmark until
    the receipt/hash is committed to a separate approved experiment manifest.
    """
    entry = CATALOG[name]
    raw_dir = DATA / 'downloads'
    raw_dir.mkdir(parents=True, exist_ok=True)
    target = raw_dir / entry['filename']
    if not target.exists():
        if local_file is not None:
            source = Path(local_file).resolve()
            if not source.is_file() or source.is_symlink():
                raise ValueError('local source file must be a regular non-symlink')
            if source.stat().st_size > MAX_IMPORT:
                raise ValueError('oversized manually supplied package')
            with target.open('xb') as out, source.open('rb') as src:
                shutil.copyfileobj(src,out)
        elif entry['method']=='github-raw':
            data = _read_url(entry['endpoint'])
            with target.open('xb') as out:
                out.write(data)
        else:
            raise ValueError('Download free Standard ZIP from publisher page, then run: '
                             'python multi-model-benchmark/assets.py import --asset '
                             + name + ' --file /path/to/download.zip')
    actual = digest_file(target)
    if entry['sha256'] and actual != entry['sha256']:
        raise ValueError('download differs from pinned source SHA256: ' + str(target))
    if entry['method']=='github-raw':
        with target.open('rb') as f:
            if not f.read(40).startswith(b'Vocaloid Motion Data'):
                raise ValueError('invalid VMD signature')
    elif not zipfile.is_zipfile(target):
        raise ValueError('expected ZIP archive: ' + str(target))
    receipts_dir = DATA / 'receipts'
    receipts_dir.mkdir(parents=True, exist_ok=True)
    receipt = receipts_dir / (name + '.json')
    if receipt.exists():
        old = json.loads(receipt.read_text())
        if old.get('sha256') != actual:
            raise ValueError('asset receipt changed; review required')
        return old
    outputs=[]
    if entry['method']=='manual-zip':
        destination = DATA / entry['track'] / name
        destination.mkdir(parents=True, exist_ok=True)
        outputs=extract_motion_zip(target, destination)
    else:
        destination = DATA / entry['track']
        destination.mkdir(parents=True, exist_ok=True)
        export=destination / entry['filename']
        if not export.exists():
            shutil.copyfile(target, export)
        if digest_file(export)!=actual:
            raise ValueError('existing VMD differs from download')
        outputs=[{'path':str(export.relative_to(DATA)), 'sha256':actual, 'bytes':export.stat().st_size}]
    record={'asset_id':name,'publisher_page':entry['page'],'source':entry['endpoint'],
            'license':entry['license'],'license_review_required':entry['license']=='check-upstream-repository',
            'original_path':str(target.relative_to(DATA)),'sha256':actual,
            'bytes':target.stat().st_size,'files':outputs,'scope':entry['notes'],
            'acquisition':'operator_source_verified_by_hash' if entry['method']=='manual-zip' else 'upstream_download_unpinned_first_fetch'}
    receipt.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return record

def verify(name):
    receipt = DATA / 'receipts' / (name + '.json')
    if not receipt.is_file():
        return False, 'not downloaded'
    data = json.loads(receipt.read_text())
    origin = DATA / data['original_path']
    if not origin.is_file() or digest_file(origin) != data['sha256']:
        return False, 'source file checksum mismatch'
    for item in data['files']:
        target = DATA / item['path']
        if not target.is_file() or digest_file(target) != item['sha256']:
            return False, 'extracted file checksum mismatch: ' + item['path']
    return True, 'valid ' + str(len(data['files'])) + ' motion files'


def import_inbox(selected=None):
    """Import manually supplied files without accessing the network."""
    inbox = DATA / 'manual-inbox'
    names = [selected] if selected else list(CATALOG)
    errors = 0
    for name in names:
        extension = '.vmd' if name == 'mmd-tools-vmd-smoke' else '.zip'
        folder = inbox / name
        candidates = sorted(p for p in folder.iterdir()
                            if p.is_file() and not p.is_symlink() and
                            p.suffix.lower() == extension) if folder.is_dir() else []
        if not candidates:
            print('WAITING', name, '— place one', extension, 'file in', folder)
            continue
        if len(candidates) != 1:
            print('FAIL', name, '— expected one', extension, 'file; found', len(candidates))
            errors += 1
            continue
        try:
            receipt = fetch(name, candidates[0])
            print('IMPORTED', name, 'sha256:', receipt['sha256'], 'files:', len(receipt['files']))
        except (OSError, ValueError, KeyError, zipfile.BadZipFile) as exc:
            print('FAIL', name, str(exc))
            errors += 1
    return 2 if errors else 0


def main():
    p = argparse.ArgumentParser(description=__doc__)
    s=p.add_subparsers(dest='cmd',required=True)
    b=s.add_parser('import-inbox', help='Import operator-supplied files; no network')
    b.add_argument('--asset', choices=sorted(CATALOG))
    s.add_parser('list')
    f=s.add_parser('fetch')
    f.add_argument('--asset',choices=sorted(CATALOG),required=True)
    i=s.add_parser('import')
    i.add_argument('--asset',choices=sorted(CATALOG),required=True)
    i.add_argument('--file',type=Path,required=True)
    v=s.add_parser('verify')
    v.add_argument('--asset',choices=sorted(CATALOG))
    a=p.parse_args()
    if a.cmd=='import-inbox':
        return import_inbox(a.asset)
    if a.cmd=='list':
        for name,entry in CATALOG.items():
            ok,why=verify(name)
            print(f'{name:22s} {"OK" if ok else "MISSING"}: {why}\n  {entry["page"]}')
        return 0
    if a.cmd=='verify':
        selected=[a.asset] if a.asset else list(CATALOG)
        results=[(name,*verify(name)) for name in selected]
        for name,ok,why in results:print(name,'OK' if ok else 'FAIL',why)
        return 0 if all(x[1] for x in results) else 2
    try:
        rec=fetch(a.asset,a.file if a.cmd=='import' else None)
        print('OK',a.asset,rec['sha256'],'files:',len(rec['files']))
        return 0
    except (OSError,ValueError,KeyError,zipfile.BadZipFile) as e:
        print('FAIL',a.asset,str(e),'Publisher:',CATALOG[a.asset]['page'])
        return 2

if __name__=='__main__':
    raise SystemExit(main())
