#!/usr/bin/env python3
"""Apply reviewed scalar/sparse tensor deltas to a COPIED HF safetensors checkpoint.

No model downloads, autonomous weight search, unpickling, GGUF editing, or source changes.
Requires torch + safetensors in isolated env. Manifest author must inspect tensor layout.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
DATA=HERE/"data"
MAX_FILES=200
MAX_ELEMENTS=500000

class PatchError(ValueError):
    pass

def hash_file(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk=f.read(1024*1024)
            if not chunk:break
            h.update(chunk)
    return h.hexdigest()

def safe_name(s):
    if not isinstance(s,str) or not s or "\\" in s or "/" in s or s in {".",".."}:
        raise PatchError("Invalid tensor file name")
    return s

def load_spec(path):
    item=json.loads(path.read_text(encoding="utf-8"))
    if item.get("schema_version")!=1 or not isinstance(item.get("operations"),list):
        raise PatchError("Invalid patch spec")
    if not item["operations"] or len(item["operations"])>64:
        raise PatchError("Patch must contain 1-64 bounded operations")
    for op in item["operations"]:
        if not isinstance(op,dict) or op.get("method")!="sparse_add":
            raise PatchError("Only auditable sparse_add operations allowed")
        safe_name(op.get("file"))
        if not isinstance(op.get("tensor"),str) or not op["tensor"]:
            raise PatchError("Tensor missing")
        cells=op.get("cells")
        if not isinstance(cells,list) or not cells or len(cells)>2048:
            raise PatchError("Operation must contain 1-2048 sparse cells")
        for cell in cells:
            if not isinstance(cell,dict) or not isinstance(cell.get("index"),list):
                raise PatchError("Cell index must be a list")
            if not cell["index"] or any(type(idx)!=int or idx<0 for idx in cell["index"]):
                raise PatchError("Invalid nonnegative multi-index")
            if type(cell.get("delta")) not in (int,float) or not (-1e3<float(cell["delta"])<1e3):
                raise PatchError("Invalid delta value")
    return item

def inside(path,root):
    return path.resolve().is_relative_to(root.resolve())

def check_roots(source,output):
    if not source.is_dir() or source.is_symlink():
        raise PatchError("Source must be existing local Hugging Face checkpoint folder")
    if not inside(source,DATA) or not inside(output,DATA):
        raise PatchError("Source/output must live in ignored lab data/")
    if source.resolve()==output.resolve() or output.exists() or output.is_symlink():
        raise PatchError("Output must be a new destination distinct from source")
    if any(p.is_symlink() for p in source.rglob("*")):
        raise PatchError("Symlinks prohibited in source checkpoint")
    if len([p for p in source.rglob("*") if p.is_file()])>MAX_FILES:
        raise PatchError("Checkpoint directory exceeds file safety count")

def apply(source,output,spec_file,global_fraction=0.0002,regional_norm=0.05):
    from safetensors.torch import load_file,save_file
    import torch
    check_roots(source,output)
    spec=load_spec(spec_file)
    if not 0<global_fraction<=0.001 or not 0<regional_norm<=0.1:
        raise PatchError("Safety caps exceeded")
    safes=list(source.glob("*.safetensors"))
    if not safes:
        raise PatchError("No safetensors files present; quantized GGUF not supported")
    if (source/"model.safetensors.index.json").exists():
        try:
            index=json.loads((source/"model.safetensors.index.json").read_text(encoding="utf-8"))
            if not isinstance(index.get("weight_map"),dict):
                raise PatchError("Malformed weight map")
        except (ValueError,OSError) as exc:
            raise PatchError("Invalid index JSON") from exc
    by_file={}
    for op in spec["operations"]:
        if not (source/op["file"]).is_file() or not op["file"].endswith(".safetensors"):
            raise PatchError("Patch file missing from checkpoint")
        by_file.setdefault(op["file"],[]).append(op)
    before={p.name:hash_file(p) for p in safes}
    size_total=0
    # Count every floating-point parameter in the checkpoint: global edit budget.
    for file in safes:
        tensors=load_file(str(file),device="cpu")
        size_total+=sum(t.numel() for t in tensors.values() if t.is_floating_point())
        del tensors
    if size_total<=0:
        raise PatchError("No floating point tensors")
    touched=set()
    actual={}
    # Plan and validate before creating any destination.
    for name,ops in by_file.items():
        tensor_map=load_file(str(source/name),device="cpu")
        for op in ops:
            key=op["tensor"]
            if key not in tensor_map:
                raise PatchError("Tensor does not exist: "+key)
            value=tensor_map[key]
            if not value.is_floating_point():
                raise PatchError("Only floating point tensors supported")
            indices=[tuple(x["index"]) for x in op["cells"]]
            if len(indices)!=len(set(indices)):
                raise PatchError("Duplicate cells within operation")
            for index in indices:
                if len(index)!=value.ndim or any(i>=d for i,d in zip(index,value.shape)):
                    raise PatchError("Index out of bounds")
                marker=(name,key,index)
                if marker in touched:raise PatchError("Repeated edit to same weight")
                touched.add(marker)
            delta2=sum(float(c["delta"])**2 for c in op["cells"])
            old2=sum(float(value[tuple(c["index"])].item())**2 for c in op["cells"])
            if delta2**0.5>regional_norm*max(old2**0.5,1e-6):
                raise PatchError("Sparse patch norm exceeds local relative cap")
        del tensor_map
    if len(touched)>int(global_fraction*size_total):
        raise PatchError("Too many weight scalars changed")
    output.mkdir(parents=True,exist_ok=False)
    try:
        for file in source.iterdir():
            target=output/file.name
            if file.is_dir():
                raise PatchError("Unexpected subdirectory; cannot safely clone")
            if file.name in by_file:
                data=load_file(str(file),device="cpu")
                for op in by_file[file.name]:
                    value=data[op["tensor"]]
                    value=value.clone()
                    for cell in op["cells"]:
                        index=tuple(cell["index"])
                        value[index]+=float(cell["delta"])
                    data[op["tensor"]]=value
                save_file(data,str(target))
            else:
                shutil.copy2(file,target)
        after={p.name:hash_file(p) for p in output.glob("*.safetensors")}
        # Validate unmodified originals remain bit-identical.
        if before!={p.name:hash_file(p) for p in safes}:
            raise PatchError("Source weights unexpectedly changed")
        report={"schema_version":1,"source_sha256":before,"patched_sha256":after,
            "patch_sha256":hash_file(spec_file),"modified_scalar_weights":len(touched),
            "total_float_parameters":size_total,"modified_fraction":len(touched)/size_total,
            "limits":{"max_fraction":global_fraction,"max_relative_l2_per_region":regional_norm},
            "status":"EXPERIMENTAL, NOT QUALIFIED; requires independent held-out comparison"}
        (output/"patch-manifest.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
        return report
    except Exception:
        shutil.rmtree(output)
        raise

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--spec",type=Path,required=True)
    args=p.parse_args(argv)
    try:
        import subprocess
        current=subprocess.run(["git","branch","--show-current"],cwd=ROOT,check=True,
            capture_output=True,text=True,timeout=10).stdout.strip()
        if current!="Qwen-Local-Helper":
            raise PatchError("Only Qwen-Local-Helper branch permitted")
        limits=json.loads((HERE/"config.json").read_text(encoding="utf-8"))["patch_safety"]
        result=apply(args.source,args.output,args.spec,
            limits["max_fraction_of_parameters"],limits["max_relative_l2_per_region"])
        print(json.dumps(result,indent=2))
        return 0
    except (PatchError,OSError,ValueError,KeyError,ImportError) as exc:
        print("PATCH STOP:",exc,file=sys.stderr)
        return 2
if __name__=="__main__":
    raise SystemExit(main())
