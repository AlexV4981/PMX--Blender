#!/usr/bin/env python3
"""Exact duplicate storage sharing; never unlink or replace a project artifact."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import struct
import sys

# Linux FIDEDUPERANGE: kernel compares bytes and shares extents copy-on-write.
# Unsupported filesystems, permission failures and partial results are retained.
CHUNK = 1024 * 1024
IOCTL = 0xc0189436
EXCLUDED = {".git", ".artifact-store", "__pycache__"}

def identity(s):
    return (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)

def hash_file(path):
    with path.open("rb") as f:
        a = os.fstat(f.fileno())
        h = hashlib.sha256()
        for data in iter(lambda: f.read(CHUNK), b""):
            h.update(data)
        if identity(a) != identity(os.fstat(f.fileno())):
            raise OSError("File changed while hashing")
    if identity(a) != identity(path.lstat()):
        raise OSError("Path changed while hashing")
    return h.hexdigest()

def equal(a,b):
    with a.open("rb") as x,b.open("rb") as y:
        while True:
            u,v=x.read(CHUNK),y.read(CHUNK)
            if u != v: return False
            if not u: return True

def kernel_share(a,b,size):
    import fcntl
    flags = os.O_NOFOLLOW | os.O_CLOEXEC
    with os.fdopen(os.open(a, os.O_RDONLY | flags), "rb") as src:
        with os.fdopen(os.open(b, os.O_RDWR | flags), "rb+") as dst:
            sa,sb=os.fstat(src.fileno()),os.fstat(dst.fileno())
            if not stat.S_ISREG(sa.st_mode) or not stat.S_ISREG(sb.st_mode) or sa.st_size!=size or sb.st_size!=size:
                raise OSError("File changed before dedupe")
            if sa.st_dev != sb.st_dev or sa.st_ino == sb.st_ino:
                return 0,"already-linked-or-other-device"
            # Header 24 bytes; destination info 32 bytes. Kernel verifies equality.
            buf=bytearray(struct.pack("=QQHHIqQQiI",0,size,1,0,0,dst.fileno(),0,0,0,0))
            fcntl.ioctl(src.fileno(),IOCTL,buf,True)
            _,_,_,_,_,_,_,shared,status,_=struct.unpack("=QQHHIqQQiI",buf)
            return shared, "shared" if status==0 else "kernel-status-"+str(status)

def run(root, scopes, apply=False, min_bytes=65536, share=kernel_share):
    root=Path(root).resolve(strict=True)
    if not root.is_dir() or min_bytes<1 or not scopes:
        raise ValueError("Directory, explicit scopes and positive minimum size required")
    bysize={}; seen=set(); errors=[]; skipped=0
    for raw in scopes:
        rel=Path(raw)
        if rel.is_absolute() or ".." in rel.parts or not rel.parts or any(x in EXCLUDED for x in rel.parts):
            raise ValueError("Unsafe scope: "+str(raw))
        scope=root/rel
        if not scope.exists(): continue
        if scope.resolve()!=scope or not scope.is_dir():
            raise ValueError("Scope must be a real directory: "+str(raw))
        for directory,dirs,files in os.walk(scope,followlinks=False,onerror=lambda e: errors.append(str(e))):
            dirs[:]=sorted(d for d in dirs if d not in EXCLUDED and not (Path(directory)/d).is_symlink())
            for name in sorted(files):
                p=Path(directory)/name
                if p in seen: continue
                seen.add(p)
                try:
                    s=p.lstat()
                    if not stat.S_ISREG(s.st_mode) or s.st_size<min_bytes:
                        skipped+=1; continue
                    bysize.setdefault(s.st_size,[]).append(p)
                except OSError as e: errors.append(str(e))
    groups=[]; logical=0; shared_total=0
    for size,paths in sorted(bysize.items()):
        if len(paths)<2: continue
        byhash={}
        for p in paths:
            try: byhash.setdefault(hash_file(p),[]).append(p)
            except OSError as e: errors.append(str(e))
        for h,ps in sorted(byhash.items()):
            if len(ps)<2: continue
            ps=sorted(ps); source=ps[0]; entries=[]
            for p in ps[1:]:
                row={"path":str(p.relative_to(root)), "status":"planned", "kernel_shared_bytes":0}
                try:
                    if os.path.samefile(source,p):
                        row["status"]="already-linked"
                    elif not equal(source,p):
                        row["status"]="not-byte-identical"
                        errors.append("Hash match but unequal bytes: "+row["path"])
                    else:
                        logical+=size
                        if apply:
                            try:
                                n,status=share(source,p,size)
                                row.update(status=status,kernel_shared_bytes=n)
                            except (OSError,ImportError,AttributeError) as e:
                                row.update(status="retained-unsupported",reason=str(e))
                            # Verify all original bytes remain present after attempt.
                            if hash_file(source)!=h or hash_file(p)!=h:
                                raise OSError("Post-operation content verification failed")
                            shared_total+=row["kernel_shared_bytes"]
                except OSError as e:
                    errors.append(str(e));row["status"]="blocked"
                entries.append(row)
            groups.append({"sha256":h,"bytes_per_file":size,"source":str(source.relative_to(root)),"copies":entries})
    return {"schema":1,"mode":"apply" if apply else "plan","scopes":list(scopes),
            "min_bytes":min_bytes,"scanned_paths":len(seen),"skipped":skipped,
            "logical_duplicate_bytes":logical,"kernel_reported_shared_bytes":shared_total,
            "groups":groups,"errors":errors,"status":"blocked" if errors else "complete",
            "notice":"Kernel shared bytes are not verified free-space recovery; all paths retained; unsupported copies retained."}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("root",type=Path)
    p.add_argument("--scope",action="append",required=True)
    p.add_argument("--min-bytes",type=int,default=65536)
    p.add_argument("--apply",action="store_true")
    p.add_argument("--quiescent",action="store_true")
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args(argv)
    if a.apply and not a.quiescent:
        p.error("Apply requires exclusive, quiescent workspace; close Blender and all writers")
    try:
        # Exclusive report creation; no historical report overwrite.
        with a.output.open("x",encoding="utf-8") as f:
            result=run(a.root,a.scope,a.apply,a.min_bytes)
            json.dump(result,f,indent=2,sort_keys=True);f.write("\n")
            f.flush();os.fsync(f.fileno())
        print(json.dumps({k:v for k,v in result.items() if k!="groups"}))
        return 2 if result["errors"] else 0
    except (ValueError,OSError) as e:
        print(str(e),file=sys.stderr);return 2

if __name__=="__main__":
    raise SystemExit(main())
