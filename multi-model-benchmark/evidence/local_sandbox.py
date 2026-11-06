"""Existing-Blender sandbox v3. Fail closed; no Docker fallback or host execution."""
import base64
import hashlib
import json
import math
import os
from pathlib import Path
import selectors
import stat
import subprocess
import time
import uuid

HERE = Path(__file__).resolve().parent
BLENDER = Path('/home/rootuser/Documents/BlenderWork/software/blender-5.2.2-linux-x64')
MAX_FILE = 32 * 1024 * 1024
MAX_PACKET = 92 * 1024 * 1024
RECORDS = []
READY = HERE.parent / 'data/local-runtime/HARDENED-READY.json'
MANIFEST = READY.with_name('runtime-files.json')
EVIDENCE_FILES = frozenset(('adversarial-results.json', 'verifier-attack-results.json',
                           'controller-death-result.json', 'hardened-smoke-runtime.json'))


def file_hash(path):
    with open(path, 'rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def runtime_inventory():
    """Pin mounted runtime bytes, not only the Blender executable."""
    roots = [BLENDER, Path('/usr/lib'), Path('/usr/lib64'), Path('/etc/alternatives'),
             Path('/etc/ld.so.cache'), Path('/usr/bin/python3.13'),
             Path('/usr/bin/bwrap'), Path('/usr/bin/systemd-run'), Path('/usr/bin/prlimit')]
    records = []
    for root in roots:
        paths = [root]
        if root.is_dir() and not root.is_symlink():
            paths += sorted(root.rglob('*'))
        for path in paths:
            info = path.lstat()
            record = {'path':str(path), 'mode':stat.S_IMODE(info.st_mode),
                      'uid':info.st_uid, 'gid':info.st_gid}
            if path.is_symlink():
                record['symlink'] = os.readlink(path)
            elif path.is_file():
                record['bytes'] = info.st_size
                try:
                    record['sha256'] = file_hash(path)
                except PermissionError:
                    # Same unprivileged UID is unable to read this in the sandbox.
                    record['unreadable_by_operator'] = True
            elif path.is_dir():
                record['directory'] = True
            else:
                raise RuntimeError('unexpected special file in runtime: '+str(path))
            records.append(record)
    return records


def policy_fingerprint():
    files = [Path(__file__), HERE/'local_worker.py', HERE/'trusted_verifier.py',
             HERE/'trusted_builder.py', HERE/'bridge.py', HERE/'isolation_probe.py',
             HERE.parents[1]/'astra-qwen-weight-lab/blender_oracle.py', MANIFEST]
    return hashlib.sha256(json.dumps({str(p):file_hash(p) for p in files},sort_keys=True).encode()).hexdigest()


def runtime_identity():
    # Distinguish verifier fixes even when the Blender executable is unchanged.
    return 'local-blender-bwrap-v3@sha256:' + policy_fingerprint()


def require_ready():
    try:
        receipt = strict_json(READY.read_bytes())
    except (OSError, ValueError) as exc:
        raise RuntimeError('hardened sandbox has no valid readiness receipt') from exc
    if receipt.get('policy_sha256') != policy_fingerprint():
        raise RuntimeError('hardened sandbox evidence is stale; rerun audit')
    verify_receipts(receipt)
    if strict_json(MANIFEST.read_bytes()) != runtime_inventory():
        raise RuntimeError('mounted runtime changed; rerun audit')


def verify_receipts(receipt):
    hashes = receipt.get('evidence_sha256')
    if not isinstance(hashes, dict) or set(hashes) != EVIDENCE_FILES:
        raise RuntimeError('required sandbox evidence receipts are missing')
    for name, expected in hashes.items():
        path = READY.with_name(name)
        if path.is_symlink() or not path.is_file() or file_hash(path) != expected:
            raise RuntimeError('sandbox evidence changed: '+name)


def no_duplicates(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError('duplicate JSON key')
        obj[key] = value
    return obj


def strict_json(text):
    def bad(value):
        raise ValueError('nonfinite JSON constant')
    def number(value):
        result = float(value)
        if not math.isfinite(result):
            bad(value)
        return result
    return json.loads(text, object_pairs_hook=no_duplicates, parse_constant=bad, parse_float=number)


def decode_packet(raw, allowed):
    if len(raw) > MAX_PACKET:
        raise ValueError('output quota exceeded')
    packet = strict_json(raw)
    if not isinstance(packet, dict) or set(packet) != {'exit_code', 'files', 'log'}:
        raise ValueError('invalid transport packet')
    if type(packet['exit_code']) is not int or not isinstance(packet['log'], str) or len(packet['log']) > 131072:
        raise ValueError('invalid transport metadata')
    if not isinstance(packet['files'], dict) or not set(packet['files']) <= allowed:
        raise ValueError('unexpected artifact name')
    decoded = {}
    for name, text in packet['files'].items():
        if not isinstance(text, str) or len(text) > 4*((MAX_FILE+2)//3):
            raise ValueError('invalid artifact encoding')
        try:
            data = base64.b64decode(text, validate=True)
        except Exception as exc:
            raise ValueError('invalid artifact encoding') from exc
        if not 0 < len(data) <= MAX_FILE:
            raise ValueError('artifact size invalid')
        decoded[name] = data
    packet['files'] = decoded
    return packet


def bwrap_command(mounts, script, mode):
    cmd = ['/usr/bin/bwrap', '--unshare-all', '--unshare-user', '--disable-userns',
           '--assert-userns-disabled', '--new-session', '--die-with-parent', '--cap-drop', 'ALL',
           '--clearenv', '--chdir', '/', '--hostname', 'pmx-disposable',
           '--ro-bind', '/usr/lib', '/usr/lib', '--symlink', 'usr/lib', '/lib',
           '--ro-bind', '/usr/lib64', '/usr/lib64', '--symlink', 'usr/lib64', '/lib64',
           '--ro-bind', '/usr/bin/python3.13', '/usr/bin/python3',
           '--ro-bind', '/etc/alternatives', '/etc/alternatives',
           '--ro-bind', '/etc/ld.so.cache', '/etc/ld.so.cache',
           '--ro-bind', str(BLENDER), '/opt/blender',
           '--proc', '/proc', '--remount-ro', '/proc', '--dev', '/dev',
           '--size', '134217728', '--tmpfs', '/tmp',
           '--size', '67108864', '--tmpfs', '/candidate_out',
           '--size', '4194304', '--tmpfs', '/trusted_out',
           '--dir', '/home', '--dir', '/lab',
           '--setenv', 'HOME', '/tmp', '--setenv', 'PATH', '/usr/bin',
           '--setenv', 'XDG_CONFIG_HOME', '/tmp/.config',
           '--setenv', 'XDG_CACHE_HOME', '/tmp/.cache',
           '--setenv', 'PMX_QWEN_ISOLATED_BLENDER', 'I_ACKNOWLEDGE_NO_NETWORK_SANDBOX',
           '--setenv', 'OMP_NUM_THREADS', '2', '--setenv', 'OPENBLAS_NUM_THREADS', '2',
           '--ro-bind', str(HERE/'local_worker.py'), '/lab/transport.py']
    for src, dst, ro in mounts:
        if not ro:
            raise ValueError('writable host mounts forbidden')
        path = Path(src)
        if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_FILE:
            raise ValueError('only bounded regular input files may be mounted')
        if not (dst.startswith('/lab/') or dst.startswith('/candidate_artifacts/')) or '..' in Path(dst).parts:
            raise ValueError('invalid mount destination')
        cmd += ['--ro-bind', str(path.resolve()), dst]
    return cmd + ['--remount-ro', '/', '/usr/bin/python3', '/lab/transport.py', mode, script]


def service_command(command, unit, seconds=65, memory=2147483648):
    return ['/usr/bin/systemd-run', '--user', '--quiet', '--wait', '--pipe', '--unit', unit,
            '-p', 'NoNewPrivileges=yes', '-p', f'MemoryMax={memory}', '-p', f'MemoryHigh={memory}',
            '-p', 'MemorySwapMax=0', '-p', 'TasksMax=64', '-p', 'CPUQuota=100%',
            '-p', f'RuntimeMaxSec={seconds}s', '-p', 'TimeoutStopSec=1s',
            '-p', 'KillMode=control-group', '-p', 'SendSIGKILL=yes',
            '-p', 'OOMPolicy=kill', '-p', 'LimitCORE=0', '-p', 'UMask=0077',
            '-p', f'ExecStartPre=/usr/bin/python3 {HERE / "local_sandbox.py"} preflight {unit} {memory}',
            '/usr/bin/prlimit', '--as=5368709120', '--core=0', '--nofile=128', '--'] + command


def stop_unit(unit):
    r = subprocess.run(['/usr/bin/systemctl', '--user', 'stop', unit], stdin=subprocess.DEVNULL,
                       capture_output=True, timeout=8, close_fds=True)
    check = subprocess.run(['/usr/bin/systemctl', '--user', 'show', unit,
                            '-p', 'ActiveState', '-p', 'SubState', '-p', 'ControlGroup',
                            '-p', 'Result', '-p', 'MemoryPeak', '-p', 'TasksMax', '-p', 'MemoryMax',
                            '-p', 'MemorySwapMax'], capture_output=True, text=True, timeout=5)
    details = dict(line.split('=',1) for line in check.stdout.splitlines() if '=' in line)
    if details.get('ActiveState') not in ('inactive', 'failed'):
        raise RuntimeError('sandbox unit did not terminate')
    group = details.get('ControlGroup')
    if group:
        events = Path('/sys/fs/cgroup') / group.lstrip('/') / 'cgroup.events'
        if events.exists() and 'populated 1' in events.read_text():
            raise RuntimeError('sandbox cgroup remains populated')
    subprocess.run(['/usr/bin/systemctl','--user','reset-failed',unit],capture_output=True,timeout=5)
    return details


def preflight(unit, memory):
    # Runs within the transient service, BEFORE any sandbox/candidate launch.
    cg = Path('/sys/fs/cgroup') / Path('/proc/self/cgroup').read_text().strip().split('::',1)[1].lstrip('/')
    expected = {'memory.max':str(memory), 'memory.swap.max':'0', 'pids.max':'64'}
    actual = {key:(cg/key).read_text().strip() for key in expected}
    if actual != expected or cg.name != unit:
        raise RuntimeError('effective cgroup limits do not match requested limits')
    quota, period = (cg/'cpu.max').read_text().split()
    if quota == 'max' or int(quota) > int(period):
        raise RuntimeError('CPU quota not effective')
    status = Path('/proc/self/status').read_text()
    if 'NoNewPrivs:\t1' not in status:
        raise RuntimeError('no-new-privileges missing')
    print('CGROUP_PREFLIGHT '+json.dumps(actual,sort_keys=True),file=__import__('sys').stderr,flush=True)


def run(mode, script, mounts, *, seconds=65, memory=2147483648):
    unit = 'pmx-sandbox-' + uuid.uuid4().hex + '.service'
    cmd = service_command(bwrap_command(mounts, script, mode), unit, seconds, memory)
    started = time.monotonic()
    # Only this controller owns the write end. Its death produces EOF in the worker.
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            close_fds=True, start_new_session=True)
    selector = selectors.DefaultSelector()
    selector.register(proc.stdout, selectors.EVENT_READ, 'stdout')
    selector.register(proc.stderr, selectors.EVENT_READ, 'stderr')
    output, errors = bytearray(), bytearray()
    details = {}
    try:
        while selector.get_map():
            if time.monotonic() - started > seconds + 10:
                raise TimeoutError('sandbox wall timeout')
            for key, _ in selector.select(0.2):
                chunk = os.read(key.fileobj.fileno(), 65536)
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                if key.data == 'stdout':
                    output.extend(chunk)
                    if len(output) > MAX_PACKET:
                        raise ValueError('sandbox transport quota exceeded')
                else:
                    errors.extend(chunk)
                    if len(errors) > 131072:
                        raise ValueError('sandbox stderr quota exceeded')
        rc = proc.wait(timeout=5)
    finally:
        selector.close()
        try:
            details = stop_unit(unit)
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait(timeout=5)
            proc.stdin.close(); proc.stdout.close(); proc.stderr.close()
        RECORDS.append({'unit':unit,'mode':mode,'seconds':round(time.monotonic()-started,3),
                        'service':details,'command':cmd})
    if rc:
        raise RuntimeError('sandbox failed: ' + errors[-2000:].decode(errors='replace') + output[-1000:].decode(errors='replace'))
    allowed = {'builder':{'candidate.blend','result.json'}, 'verifier':{'oracle.json'}}.get(mode,set())
    packet = decode_packet(bytes(output), allowed)
    if b'CGROUP_PREFLIGHT ' not in errors:
        raise RuntimeError('missing effective resource-limit witness')
    RECORDS[-1]['preflight'] = errors.decode(errors='replace')
    if packet['exit_code']:
        raise RuntimeError('isolated process failed: '+str(packet['exit_code'])+' '+packet['log'][-1000:])
    if allowed != set(packet['files']):
        raise ValueError('missing output artifact')
    return packet


def install_bridge(*, audit=False):
    """Explicit adapter; tracked Docker path is unchanged. Host output is never mounted."""
    from . import bridge
    if not audit:
        require_ready()
    expected_identity = runtime_identity()
    def flags(identity, mounts, **kwargs):
        if identity != expected_identity:
            raise ValueError('local runtime identity mismatch')
        return ['LOCAL_SANDBOX_V2', json.dumps({'mounts':[(str(a),b,c) for a,b,c in mounts]})]
    def executor(cmd, timeout):
        try:
            requested = json.loads(cmd[1])['mounts']
            script = cmd[cmd.index('--python')+1]
            mode = 'builder' if script.endswith('builder.py') else 'verifier' if script.endswith('verifier.py') else 'probe'
            mounts, output = [], None
            for src,dst,ro in requested:
                if ro and dst == '/candidate_artifacts':
                    for name in ('candidate.blend','result.json'):
                        mounts.append((Path(src)/name,dst+'/'+name,True))
                elif ro:
                    mounts.append((src,dst,True))
                else:
                    if dst not in ('/candidate_out','/trusted_out') or output is not None:
                        raise ValueError('unexpected host output request')
                    output=Path(src)
            packet = run(mode, script, mounts)
            if output:
                for name,data in packet['files'].items():
                    fd=os.open(output/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o400)
                    with os.fdopen(fd,'wb') as f:f.write(data)
            return 0,packet['log'],'',False,0
        except Exception as exc:
            return 1,'',type(exc).__name__+': '+str(exc),isinstance(exc,TimeoutError),0
    def probe(identity, **kwargs):
        if identity != expected_identity:
            raise ValueError('local runtime identity mismatch')
        packet=run('probe','/lab/probe.py',[(bridge.PROBE,'/lab/probe.py',True)])
        parsed=bridge.parse_probe(packet['log'])
        return bridge.ProbeResult(parsed['verified'],identity,parsed)
    bridge.sandbox_flags=flags
    bridge.run_probe=probe
    original=bridge.evaluate_attempt
    def evaluate(*args,**kwargs):
        kwargs['executor']=executor
        return original(*args,**kwargs)
    bridge.evaluate_attempt=evaluate


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 4 and sys.argv[1] == 'preflight':
        preflight(sys.argv[2], int(sys.argv[3]))
    else:
        raise SystemExit('This module is only launched by the trusted controller.')
