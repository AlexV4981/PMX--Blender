"""Sandbox-side transport. Every byte returned by this process is UNTRUSTED."""
import base64
import ctypes
import errno
import json
import os
from pathlib import Path
import resource
import select
import stat
import subprocess
import sys
import threading

MAX_FILE = 32 * 1024 * 1024


def install_seccomp():
    lib = ctypes.CDLL('libseccomp.so.2', use_errno=True)
    lib.seccomp_init.argtypes = [ctypes.c_uint32]
    lib.seccomp_init.restype = ctypes.c_void_p
    lib.seccomp_syscall_resolve_name.argtypes = [ctypes.c_char_p]
    lib.seccomp_syscall_resolve_name.restype = ctypes.c_int
    lib.seccomp_rule_add.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int, ctypes.c_uint]
    lib.seccomp_load.argtypes = [ctypes.c_void_p]
    lib.seccomp_release.argtypes = [ctypes.c_void_p]
    ctx = lib.seccomp_init(0x7fff0000)  # SCMP_ACT_ALLOW, native arch only; other arch killed.
    if not ctx:
        raise RuntimeError('seccomp_init failed')
    try:
        denied = ('socket socketpair ptrace process_vm_readv process_vm_writev pidfd_getfd '
                  'bpf perf_event_open userfaultfd keyctl add_key request_key mount umount2 '
                  'pivot_root chroot setns unshare open_by_handle_at name_to_handle_at '
                  'kexec_load kexec_file_load init_module finit_module delete_module reboot '
                  'swapon swapoff syslog quotactl io_uring_setup ioperm iopl fanotify_init '
                  'fork vfork').split()
        for name in denied + ['clone3']:
            nr = lib.seccomp_syscall_resolve_name(name.encode())
            if nr < 0:
                continue
            action = 0x00050000 | (errno.ENOSYS if name == 'clone3' else errno.EPERM)
            if lib.seccomp_rule_add(ctx, action, nr, 0) != 0:
                raise RuntimeError('seccomp rule failed: ' + name)
        class Comparison(ctypes.Structure):
            _fields_ = [('arg', ctypes.c_uint), ('op', ctypes.c_int),
                        ('datum_a', ctypes.c_uint64), ('datum_b', ctypes.c_uint64)]
        # clone is only allowed for threads, never a new process/namespace.
        nr = lib.seccomp_syscall_resolve_name(b'clone')
        cmp = Comparison(0, 7, 0x10000, 0)  # MASKED_EQ(CLONE_THREAD, 0)
        lib.seccomp_rule_add_array.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int,
                                              ctypes.c_uint, ctypes.POINTER(Comparison)]
        if lib.seccomp_rule_add_array(ctx, 0x00050000 | errno.EPERM, nr, 1, ctypes.byref(cmp)):
            raise RuntimeError('clone filter failed')
        if lib.seccomp_load(ctx):
            raise RuntimeError('seccomp_load failed')
    finally:
        lib.seccomp_release(ctx)


def child_setup():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_FSIZE, (256 * 1024 * 1024, 256 * 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_NOFILE, (128, 128))
    resource.setrlimit(resource.RLIMIT_CPU, (50, 50))
    install_seccomp()


def read_regular(folder, name):
    directory = os.open(folder, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
        try:
            st = os.fstat(fd)
            if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1 or not 0 < st.st_size <= MAX_FILE:
                raise ValueError('invalid output artifact')
            data = bytearray()
            while len(data) <= MAX_FILE:
                chunk = os.read(fd, min(1024 * 1024, MAX_FILE + 1 - len(data)))
                if not chunk:
                    break
                data.extend(chunk)
            if len(data) > MAX_FILE:
                raise ValueError('oversized output')
            return base64.b64encode(data).decode('ascii')
        finally:
            os.close(fd)
    finally:
        os.close(directory)


def main():
    # Child must not open its transport parent's /proc/PID/{mem,fd/*}.
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(4, 0, 0, 0, 0) != 0:  # PR_SET_DUMPABLE=0
        raise RuntimeError('cannot protect transport parent')
    mode, script = sys.argv[1:3]
    program = ['/opt/blender/blender', '--background', '--factory-startup', '--disable-autoexec',
               '--threads', '2', '--python-exit-code', '1', '--python', script]
    if mode.startswith('python'):
        program = ['/usr/bin/python3', script]
    # These files live exclusively on a bounded, private tmpfs.
    with open('/tmp/process.log', 'w+b') as log:
        child = subprocess.Popen(program, stdin=subprocess.DEVNULL, stdout=log, stderr=log,
                                 close_fds=True, preexec_fn=child_setup)
        def watch_controller():
            while True:
                if select.select([0], [], [], 0.2)[0] and os.read(0, 1) == b'':
                    # Exiting the namespace leader tears down all candidate threads.
                    os._exit(125)
        threading.Thread(target=watch_controller, daemon=True).start()
        returncode = child.wait(timeout=55)
        # Retain the descriptor; candidate may replace the pathname with a FIFO/symlink.
        log.seek(0, 2)
        log.seek(max(0, log.tell() - 65536))
        tail = log.read(65536).decode('utf-8', errors='replace')
    files = {}
    names = {'builder':('/candidate_out', ('candidate.blend', 'result.json')),
             'verifier':('/trusted_out', ('oracle.json',))}.get(mode)
    if returncode == 0 and names:
        for name in names[1]:
            files[name] = read_regular(names[0], name)
    print(json.dumps({'exit_code':returncode, 'files':files, 'log':tail}, allow_nan=False))


if __name__ == '__main__':
    main()
