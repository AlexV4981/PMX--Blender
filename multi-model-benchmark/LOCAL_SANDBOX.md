# Local Blender sandbox v3

This is the user-authorized existing-Blender alternative to the repository's Docker adapter. No Docker image is downloaded. The old ignored `run_local_smoke.py` launcher is disabled because it failed adversarial review. No Qwen proposal has been executed during hardening.

## Execution boundary

`evidence/local_sandbox.py` launches a uniquely named transient systemd **user** service. Before it launches Bubblewrap, an ExecStartPre process reads the actual cgroup `memory.max`, `memory.swap.max`, `pids.max`, `cpu.max` and NoNewPrivs state, failing closed on disagreement. Normal limits are 2 GiB aggregate RAM, zero swap, 64 tasks, one CPU of aggregate quota, a 65-second service runtime and one-second stop grace. The Blender child additionally has hard virtual-address, descriptor, CPU-time and file-size limits. Tests use smaller explicit RAM caps.

Bubblewrap provides separate user/PID/network/IPC/UTS namespaces, disables additional user namespaces, drops capabilities, clears the environment, and exposes a read-only root. Personal home/project directories, host sockets, cgroups, GPUs and `/usr/local` are absent. Mounted runtime consists of installed Blender, system libraries, Python and library-resolution metadata. Readable mounted files are cryptographically inventoried; operator-unreadable files have permissions/ownership recorded instead. The same unprivileged UID cannot read those files inside the sandbox. Runtime inventory does not authenticate a compromised host or another trusted host process changing files during a lap.

A libseccomp filter blocks sockets, fork/vfork, process clones, namespace changes, tracing/process-memory APIs, keyring/BPF/perf/io_uring and privileged kernel interfaces. Thread creation remains possible but is bounded by the cgroup. clone3 returns ENOSYS for normal thread-library fallback. This is a denylist, not a claim that every remaining syscall is harmless.

There are **no writable host mounts**. Temporary files and candidate/verifier outputs reside on separate size-limited tmpfs mounts (128 MiB, 64 MiB and 4 MiB). Inode allocations are covered by aggregate cgroup memory accounting; no separate explicit inode-count quota is claimed. Killing the service destroys the private filesystems. A live controller pipe terminates the namespace promptly if the controller crashes. Normal, exception, quota and timeout paths explicitly stop the owned unit and check that it is inactive with no populated cgroup before accepting outputs.

The transport parent is non-dumpable. Fresh stdio descriptors are used; child inherits no host directory/socket descriptors. Only bounded regular files with fixed names are exported. Symlinks, FIFOs, hardlinks, oversized artifacts, duplicate JSON keys, nonfinite numbers and unexpected filenames are rejected. Host pipes have hard byte quotas; retained child logs are limited to a 64 KiB tail. Exported candidate data remains untrusted.

The fresh verifier runs under the same restrictions, sees only explicitly exported candidate files, opens Blender with autoexec disabled, and never executes the candidate script. It additionally rejects nonfinite reported values and Blender geometry/weights/transforms, fixing observed NaN false passes. A hostile `.blend` still exercises Blender's native parser: unknown Blender or kernel vulnerabilities remain a trust assumption. The hash chain cannot authenticate evidence against the host owner.

## Reproduce and use

From the repository root:

```sh
python3 -m unittest discover -s multi-model-benchmark/tests -v
python3 multi-model-benchmark/data/local-runtime/adversarial_checks.py
python3 multi-model-benchmark/data/local-runtime/controller_death_check.py
python3 multi-model-benchmark/data/local-runtime/verifier_attack_checks.py
python3 multi-model-benchmark/data/local-runtime/run_hardened_smoke.py
```

These audit scripts are local ignored artifacts, retained in this setup. They run only authored probes/disposable synthetic fixtures, never an accepted Lynae file. Host access to the user service manager is necessary. Do not run generated code directly when a sandbox command fails. Do not replace cgroup enforcement with per-process limits.

Before a model lap, call `evidence.local_sandbox.install_bridge()` with its default gate enabled. It requires `data/local-runtime/HARDENED-READY.json`, exact policy/source hashes, and rechecks the pinned runtime inventory. Missing or stale evidence blocks the lap. `audit=True` is reserved for rerunning the authored audit, not for bypassing a failed model-execution gate. Runtime identity binds the complete sandbox/verifier policy and pinned runtime manifest, so results from older verifier versions have a different identity. Proposal inference and Blender verification remain separate sequential phases.

## Evidence and limitations

See `data/reports/SANDBOX-HARDENING-2026-11-06.md` and `data/local-runtime/*results.json`. The 85-test suite, controlled security probes and positive/negative smoke verify specific observed behavior; they do not prove an unbreakable sandbox. A disposable VM or separate machine with no valuable mounts/accounts provides a separate kernel boundary for deliberately hostile native code. No exploit attempt against the host kernel or real user files is part of this audit.

Implementation references: [Bubblewrap documentation](https://github.com/containers/bubblewrap/blob/main/bwrap.xml), [systemd resource controls](https://www.freedesktop.org/software/systemd/man/261/systemd.resource-control.html).


## Intruder follow-up — 2026-11-06

An explicitly requested adversarial subagent reproduced two fresh-verifier false passes, not host escapes: deleted mesh faces at Stage03 and disabled/muted IK at Stage04. The independent verifier now compares protected topology, coordinates, keys, UVs, material/group names, object transforms and armature rest matrices/parenting. It requires enabled full-influence IK and independently moves its target to measure an actual response before restoring it.

The same subagent reran five regression scenarios: deleted faces, disabled IK, moved mesh and reversed winding were rejected; enabled full-influence IK passed. Before/after sources, verdicts and cgroup/cleanup evidence are in data/local-runtime/intruder/. Readiness additionally validates the recorded security-receipt hashes rather than merely storing them. See data/reports/INTRUDER-ROUND-2026-11-06.md.
