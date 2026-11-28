#!/usr/bin/env python3
"""Opt-in, verified stage archive. No gate changes; no automatic deletion."""
import argparse
from contextlib import contextmanager
import gzip
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile

CHUNK = 1024 * 1024
AREAS = {"work", "audit", "candidates", "checkpoints"}
HEX = re.compile(r"^[0-9a-f]{64}$")
INDEX = ".stage-archive"
STAGES = {f"{i:02d}" for i in range(9)} | {"08P", "09"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def safe_path(root, name):
    require(isinstance(name, str) and name and "\\" not in name and ":" not in name, "Use a relative POSIX path")
    rel = PurePosixPath(name)
    require(not rel.is_absolute() and str(rel) == name and ".." not in rel.parts and len(rel.parts) >= 2 and rel.parts[0] in AREAS, "Unsafe archive path: " + name)
    p = root
    for part in rel.parts:
        p = p / part
        require(not p.is_symlink(), "Symlink refused: " + name)
    require(p.resolve().is_relative_to(root), "Path escaped workspace")
    return p


def regular(p):
    return stat.S_ISREG(p.lstat().st_mode)


def identity(p):
    s = p.lstat()
    require(stat.S_ISREG(s.st_mode), "Not a regular file: " + str(p))
    return (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)


def digest_stream(f, out=None, limit=None):
    h = hashlib.sha256()
    n = 0
    for chunk in iter(lambda: f.read(CHUNK), b""):
        n += len(chunk)
        require(limit is None or n <= limit, "Archive exceeds expected length")
        h.update(chunk)
        if out is not None:
            out.write(chunk)
    return h.hexdigest(), n


def digest_file(p):
    before = identity(p)
    with p.open("rb") as f:
        result = digest_stream(f)
    require(before == identity(p), "File changed while reading: " + str(p))
    return result


def canonical(data):
    return (json.dumps(data, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def index_dir(root):
    d = root / INDEX
    require(not d.is_symlink(), "Unsafe archive index")
    d.mkdir(exist_ok=True)
    return d


class Store:
    """An external local test store or preconfigured rclone remote. No credentials handled."""
    def __init__(self, root, local=None, remote=None):
        require(bool(local) != bool(remote), "Choose exactly one store")
        self.remote = remote
        if remote:
            require(re.fullmatch(r"[A-Za-z0-9_-]+:[A-Za-z0-9_./ -]+", remote) is not None and ".." not in remote.split(":",1)[1].split("/") and not remote.endswith(":"), "Use a named rclone remote with a dedicated folder")
            require(shutil.which("rclone") is not None, "rclone not installed")
            self.base = remote.rstrip("/")
        else:
            self.base = Path(local).resolve()
            require(not self.base.is_relative_to(root) and not root.is_relative_to(self.base), "Archive store must be separate from workspace")
            self.base.mkdir(parents=True, exist_ok=True)

    def target(self, key):
        require(re.fullmatch(r"(objects/[0-9a-f]{64}\.gz|manifests/[0-9a-f]{64}\.json)", key) is not None, "Invalid store key")
        return self.base + "/" + key if self.remote else self.base / key

    def put(self, src, key):
        target = self.target(key)
        if self.remote:
            subprocess.run(["rclone", "copyto", "--immutable", str(src), target], check=True)
        else:
            target.parent.mkdir(exist_ok=True)
            if target.exists():
                require(digest_file(target) == digest_file(src), "Immutable object collision")
                return
            with target.open("xb") as dst, src.open("rb") as f:
                shutil.copyfileobj(f, dst, CHUNK)

    @contextmanager
    def read(self, key):
        target = self.target(key)
        if self.remote:
            with subprocess.Popen(["rclone", "cat", target], stdout=subprocess.PIPE) as proc:
                try:
                    yield proc.stdout
                    require(proc.wait() == 0, "Remote read failed")
                finally:
                    if proc.poll() is None:
                        proc.kill()
        else:
            with target.open("rb") as f:
                yield f


def object_key(sha):
    require(isinstance(sha,str) and HEX.fullmatch(sha), "Invalid SHA-256")
    return "objects/" + sha + ".gz"


def verify_object(store, entry, out=None):
    size = entry["bytes"]
    require(type(size) is int and size >= 0, "Invalid length")
    with store.read(object_key(entry["sha256"])) as raw:
        with gzip.GzipFile(fileobj=raw, mode="rb") as f:
            actual = digest_stream(f, out, size)
    require(actual == (entry["sha256"], size), "Remote content mismatch: " + entry["path"])


def protected_paths(root, run):
    """Conservatively protect every stamped or path-valued ledger record, even rejected candidates."""
    found = set()
    def walk(node):
        if isinstance(node, dict):
            for k,v in node.items():
                if k == "path" and isinstance(v,str):
                    p = Path(v)
                    p = p.resolve() if p.is_absolute() else (root/p).resolve()
                    if p.is_relative_to(root):
                        found.add(p.relative_to(root).as_posix())
                walk(v)
        elif isinstance(node,list):
            for v in node:
                walk(v)
    walk(run)
    return found


def plan_files(root, paths):
    require(isinstance(paths,list) and paths, "Explicit paths required")
    result = set()
    for name in paths:
        p = safe_path(root,name)
        if p.is_dir():
            for d, dirs, files in os.walk(p, followlinks=False):
                dirs[:] = sorted(x for x in dirs if not (Path(d)/x).is_symlink())
                for x in files:
                    f = Path(d)/x
                    if not f.is_symlink() and regular(f):
                        result.add(f.relative_to(root).as_posix())
        else:
            require(regular(p), "Not a regular file: " + name)
            result.add(name)
    require(result, "No eligible files")
    return sorted(result)


def run_identity(run):
    return hashlib.sha256(canonical({k:run[k] for k in ("created","policy_sha256","sources")})).hexdigest()


def archive(root, store, run, stage, plan):
    require(stage in STAGES and run["stages"][stage]["approved"], "Archive only after actual stage approval")
    paths = plan_files(root,plan["paths"])
    protected = protected_paths(root,run)
    entries = []
    d = index_dir(root)
    for name in paths:
        p = safe_path(root,name)
        before = identity(p)
        sha,size = digest_file(p)
        entry = {"path":name,"sha256":sha,"bytes":size,"mode":stat.S_IMODE(p.stat().st_mode),
                 "ledger_protected_at_archive":name in protected or name.startswith("checkpoints/")}
        # A complete remote read is necessary; a prior upload may be reused only if verified.
        try:
            verify_object(store,entry)
        except (OSError,ValueError,EOFError,subprocess.CalledProcessError):
            require(shutil.disk_usage(d).free > size + max(1048576, size//100), "Insufficient temporary headroom for single-file compression")
            with tempfile.TemporaryDirectory(dir=d) as t:
                compressed = Path(t)/"object.gz"
                with compressed.open("wb") as raw, gzip.GzipFile(filename="",fileobj=raw,mode="wb",mtime=0,compresslevel=6) as f, p.open("rb") as src:
                    require(digest_stream(src,f) == (sha,size), "Source changed during compression")
                store.put(compressed,object_key(sha))
            verify_object(store,entry)
        require(before == identity(p), "Source changed during archive")
        entries.append(entry)
    manifest = {"schema":1,"run_identity":run_identity(run),"stage":stage,"entries":entries}
    body = canonical(manifest)
    mid = hashlib.sha256(body).hexdigest()
    path = d/(mid+".json")
    with tempfile.TemporaryDirectory(dir=d) as t:
        tmp = Path(t)/"manifest.json"
        tmp.write_bytes(body)
        store.put(tmp,"manifests/"+mid+".json")
    with store.read("manifests/"+mid+".json") as f:
        require(f.read(len(body)+1)==body, "Remote manifest mismatch")
    if path.exists():
        require(path.read_bytes()==body,"Local manifest collision")
    else:
        with path.open("xb") as f:
            f.write(body)
            f.flush()
            os.fsync(f.fileno())
    return {"manifest":mid,"files":len(entries),"raw_bytes":sum(e["bytes"] for e in entries),"local_files_removed":0}


def get_manifest(root,store,mid,run):
    require(isinstance(mid,str) and HEX.fullmatch(mid),"Invalid manifest ID")
    # Read back the remote index, not just a local receipt.
    with store.read("manifests/"+mid+".json") as f:
        body=f.read(64*1024*1024+1)
    require(len(body)<=64*1024*1024 and hashlib.sha256(body).hexdigest()==mid,"Remote manifest hash mismatch")
    m=json.loads(body)
    require(m["schema"]==1 and m["run_identity"]==run_identity(run),"Manifest belongs to another run")
    require(m["stage"] in STAGES and run["stages"][m["stage"]]["approved"],"Stage is not approved")
    entries={}
    for e in m["entries"]:
        safe_path(root,e["path"])
        require(e["path"] not in entries,"Duplicate manifest path")
        object_key(e["sha256"])
        require(type(e["bytes"]) is int and e["bytes"]>=0,"Invalid entry length")
        entries[e["path"]]=e
    d=index_dir(root)
    local=d/(mid+".json")
    if local.exists():
        require(local.read_bytes()==body,"Local manifest changed")
    else:
        with local.open("xb") as f:
            f.write(body)
    return m,entries


def restore(root,store,entry):
    p=safe_path(root,entry["path"])
    if p.exists():
        require(digest_file(p)==(entry["sha256"],entry["bytes"]),"Refusing to overwrite different local content")
        return "already-present"
    p.parent.mkdir(parents=True,exist_ok=True)
    require(shutil.disk_usage(p.parent).free >= entry["bytes"],"Insufficient restore space")
    fd,tmp=tempfile.mkstemp(prefix=".restore-",dir=p.parent)
    try:
        with os.fdopen(fd,"wb") as f:
            verify_object(store,entry,f)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp,entry["mode"] & 0o777)
        # Atomic no-overwrite installation; temporary name is immediately removed.
        os.link(tmp,p)
        return "restored"
    finally:
        os.unlink(tmp)


def evict(root,store,run,manifest,entries,plan):
    """Explicit, fail-closed opt-in; only retired unregistered files, never a checkpoint."""
    require(plan.get("dependencies_reviewed") is True and isinstance(plan.get("reason"),str) and plan["reason"].strip(),"Explicit dependency review and retirement reason required")
    retired=plan.get("retired")
    keep=plan.get("keep")
    require(isinstance(retired,list) and retired and len(set(retired))==len(retired) and isinstance(keep,list),"Explicit retired and keep lists required")
    require(all(isinstance(x,str) for x in keep),"Invalid keep list")
    for name in keep:
        safe_path(root,name)
    protected=protected_paths(root,run)
    stage=manifest["stage"]
    verified=[]
    for name in retired:
        p=safe_path(root,name)
        require(name in entries,"Not in verified manifest: "+name)
        parts=PurePosixPath(name).parts
        require(len(parts)>=3 and parts[0] in {"audit","work","candidates"} and parts[1]==stage,"Only retired files of the archived stage may be evicted")
        require(name not in protected and not entries[name]["ledger_protected_at_archive"],"Ledger-referenced file must remain local: "+name)
        require(not any(name==k or name.startswith(k.rstrip("/")+"/") for k in keep),"Active dependency must remain local: "+name)
        before=identity(p)
        require(digest_file(p)==(entries[name]["sha256"],entries[name]["bytes"]),"Local bytes changed: "+name)
        verify_object(store,entries[name])
        require(before==identity(p),"Local file changed: "+name)
        verified.append((p,before))
    # All checks precede the first removal; quiescent workspace is a caller requirement.
    for p,before in verified:
        require(before==identity(p),"File changed before eviction")
    for p,before in verified:
        require(before==identity(p),"File changed before eviction")
        p.unlink()
    return {"evicted":len(verified),"notice":"Logical file removal; actual free-space recovery depends on filesystem sharing."}


def main(argv=None):
    import pipeline
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace",type=Path)
    parser.add_argument("command",choices=("archive","list","restore","evict"))
    store=parser.add_mutually_exclusive_group(required=True)
    store.add_argument("--remote")
    store.add_argument("--local-store",type=Path)
    parser.add_argument("--stage")
    parser.add_argument("--plan",type=Path)
    parser.add_argument("--manifest")
    parser.add_argument("--path",action="append")
    parser.add_argument("--quiescent",action="store_true")
    args=parser.parse_args(argv)
    try:
        root=args.workspace.resolve(strict=True)
        require(args.quiescent or args.command=="list","Stop Blender and all workspace writers first; use --quiescent")
        backend=Store(root,args.local_store,args.remote)
        with pipeline.lock(root):
            run=pipeline.load(root)
            if args.command=="archive":
                require(args.plan is not None,"Archive requires a plan")
                result=archive(root,backend,run,args.stage,json.loads(args.plan.read_text(encoding="utf-8")))
            else:
                m,entries=get_manifest(root,backend,args.manifest,run)
                if args.command=="list":
                    result={"stage":m["stage"],"entries":list(entries.values())}
                elif args.command=="restore":
                    require(args.path,"Specify exact paths to restore")
                    result={name:restore(root,backend,entries[name]) for name in args.path}
                else:
                    require(args.plan is not None,"Eviction requires a plan")
                    # Validate every registered candidate, including drafts, before and after.
                    for stage in run["stages"].values():
                        for c in stage["candidates"].values():
                            require(pipeline.live_bundle(root,c)==c["bundle_sha256"],"Registered candidate changed; do not evict")
                    result=evict(root,backend,run,m,entries,json.loads(args.plan.read_text(encoding="utf-8")))
                    pipeline.load(root)
                    for stage in run["stages"].values():
                        for c in stage["candidates"].values():
                            require(pipeline.live_bundle(root,c)==c["bundle_sha256"],"Registered candidate changed; restore and stop")
        print(json.dumps(result,indent=2))
        return 0
    except (ValueError,OSError,KeyError,TypeError,EOFError,subprocess.CalledProcessError,pipeline.PipelineError) as exc:
        print(json.dumps({"error":str(exc)}),file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
