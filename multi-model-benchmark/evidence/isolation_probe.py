"""Runs INSIDE the sandbox (under Blender's Python or plain python3). Prints one JSON line.

It reports observed behaviour; the host decides. Passing this probe is evidence about the
container configuration used for the probe run, not a proof about any later run.
"""
import json
import os
import socket
import sys

FORBIDDEN_PATHS = ("/var/run/docker.sock", "/run/docker.sock", "/ledger", "/root/.ssh", "/home")
SECRET_WORDS = ("TOKEN", "SECRET", "PASSWORD", "CREDENTIAL", "API_KEY", "APIKEY")


def network_blocked():
    for host in ("1.1.1.1", "8.8.8.8"):
        try:
            socket.create_connection((host, 53), timeout=2).close()
            return False
        except OSError:
            continue
    return True


def writable(path):
    try:
        with open(os.path.join(path, ".probe_write"), "w") as f:
            f.write("x")
        os.remove(os.path.join(path, ".probe_write"))
        return True
    except OSError:
        return False


def main():
    version = None
    try:
        import bpy
        version = bpy.app.version_string
    except Exception:
        pass
    out = {
        "network_blocked": network_blocked(),
        "root_readonly": not writable("/") and not writable("/lab"),
        "forbidden_paths_present": [p for p in FORBIDDEN_PATHS if os.path.exists(p) and (p != "/home" or os.listdir(p))],
        "secret_env_keys": sorted(k for k in os.environ if any(w in k.upper() for w in SECRET_WORDS)),
        "blender_version": version, "uid": os.getuid(),
    }
    print("ISOLATION_PROBE_RESULT " + json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
