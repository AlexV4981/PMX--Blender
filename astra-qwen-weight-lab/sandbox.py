#!/usr/bin/env python3
"""Run ONE inert Qwen candidate in a locally installed Docker Blender image.

No image pulls. Qwen code is mounted read-only in a no-network, read-only,
no-privileges, resource-capped disposable container. One task at a time.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
DATA=HERE/"data"

class SandboxError(ValueError):
    pass

def inside(path,base):
    if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(base.resolve()):
        raise SandboxError("Input must be an ordinary file under ignored lab/data/")

def build(args):
    if not args.case.is_file():
        raise SandboxError("Case JSON missing")
    inside(args.case,DATA);inside(args.source,DATA)
    if args.out.exists() or args.out.is_symlink() or not args.out.resolve().is_relative_to(DATA.resolve()):
        raise SandboxError("Result must be new and under ignored lab data/")
    d=json.loads(args.case.read_text(encoding="utf-8"))
    if d.get("stage") not in ("03","04","05","06") or not d.get("synthetic"):
        raise SandboxError("Only private synthetic 03–06 fixtures may execute")
    if args.image.count("@sha256:")!=1:
        raise SandboxError("Blender Docker image must be PINNED by local sha256 digest")
    subprocess.run(["docker","image","inspect",args.image],check=True,
                   capture_output=True,timeout=15)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    c=[
      "docker","run","--rm","--network","none","--read-only",
      "--cap-drop","ALL","--security-opt","no-new-privileges",
      "--pids-limit","128","--memory","5g","--cpus","4",
      "--ipc","private",
      "--tmpfs","/tmp:rw,nosuid,size=268435456",
      "--env","PMX_QWEN_ISOLATED_BLENDER=I_ACKNOWLEDGE_NO_NETWORK_SANDBOX",
      "--mount",f"type=bind,src={args.case.resolve()},dst=/lab/case.json,readonly",
      "--mount",f"type=bind,src={args.source.resolve()},dst=/lab/candidate.py,readonly",
      "--mount",f"type=bind,src={(HERE/'blender_oracle.py').resolve()},dst=/lab/oracle.py,readonly",
      "--mount",f"type=bind,src={args.out.parent.resolve()},dst=/results",
      args.image,
      "blender","--background","--factory-startup","--python","/lab/oracle.py",
      "--","--case","/lab/case.json","--source","/lab/candidate.py",
      "--out","/results/"+args.out.name
    ]
    return c

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--case",required=True,type=Path)
    p.add_argument("--source",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--image",required=True,help="Locally installed Blender image ID pinned as name@sha256:...")
    p.add_argument("--execute",action="store_true",help="Run exactly one container; default prints proposed command")
    a=p.parse_args()
    try:
        branch=subprocess.run(["git","branch","--show-current"],cwd=ROOT,
            text=True,capture_output=True,check=True,timeout=10).stdout.strip()
        if branch!="Qwen-Local-Helper":
            raise SandboxError("Refuse outside Qwen-Local-Helper")
        cmd=build(a)
        if not a.execute:
            print("DRY RUN only. To run, pass --execute after inspecting command.")
            print(json.dumps(cmd,indent=2))
            return 0
        result=subprocess.run(cmd,cwd=ROOT,timeout=240,text=True,capture_output=True)
        print(result.stdout[-6000:]);print(result.stderr[-4000:],file=sys.stderr)
        if not a.out.is_file():
            raise SandboxError("No oracle result file; Blender did not produce verifiable evidence")
        return result.returncode
    except (SandboxError,OSError,ValueError,KeyError,subprocess.TimeoutExpired,
            subprocess.CalledProcessError) as exc:
        print("SANDBOX STOP:",exc,file=sys.stderr)
        return 2

if __name__=="__main__":
    sys.exit(main())
