#!/usr/bin/env python3
"""Opt-in 7B QLoRA staging only; uses pre-existing trusted helper trainer unmodified.

Requires a local compatible full-weight HF checkpoint, a verified train split,
a disjoint independent validation/holdout, and >=24 GB GPU memory.
No automatic weights download or training without --execute.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
DATA=HERE/"data"
STAGES={"03":"geometry_builder","04":"rig_builder","05":"animator_builder","06":"animation_qualifier"}

class TrainError(ValueError):
    pass

def rows(path):
    if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(DATA.resolve()):
        raise TrainError("Only local ignored JSONL dataset files permitted")
    found=[]
    ids=set()
    for lineno,line in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not line.strip():continue
        item=json.loads(line)
        for field in ("case_id","group_id","prompt","completion","source_type","verified_by"):
            if not isinstance(item.get(field),str) or not item[field].strip() or item[field].startswith("FILL_"):
                raise TrainError(f"Row {lineno} unverified or missing {field}")
        if item["case_id"] in ids:raise TrainError("Duplicate case IDs")
        ids.add(item["case_id"]);found.append(item)
    if not found:raise TrainError("No training/holdout data")
    return found

def validate(train,validation,holdout):
    groups=[];examples=[]
    for path in (train,validation,holdout):
        items=rows(path)
        groups.append({x["group_id"] for x in items})
        examples.append({x["case_id"] for x in items})
    if any(groups[i]&groups[j] or examples[i]&examples[j]
           for i in range(3) for j in range(i+1,3)):
        raise TrainError("Train/validation/holdout source-family leakage")
    if len(groups[0])<5:
        raise TrainError("At least five independently sourced training groups required")
    return {"training_cases":len(examples[0]),"validation_cases":len(examples[1]),
            "holdout_cases":len(examples[2]),"training_families":len(groups[0])}

def local_base(path):
    if not path.is_dir() or path.is_symlink():
        raise TrainError("Require existing full-weight HF model directory; Ollama GGUF not trainable here")
    config=path/"config.json"
    if not config.is_file():raise TrainError("Missing full-weight model config.json")
    cfg=json.loads(config.read_text(encoding="utf-8"))
    # Verify exact architecture; never quietly use the old 1.5B base.
    if cfg.get("model_type") not in ("qwen2","qwen2_moe"):
        raise TrainError("Model is not the expected Qwen2.5 base architecture")
    hidden=cfg.get("hidden_size")
    layers=cfg.get("num_hidden_layers")
    if not isinstance(hidden,int) or hidden<3000 or not isinstance(layers,int) or layers<25:
        raise TrainError("Checkpoint seems too small to be Qwen2.5-Coder-7B")
    if not list(path.glob("*.safetensors")):
        raise TrainError("No safetensors full-weight shards found")
    return {"model_type":cfg["model_type"],"hidden_size":hidden,"num_hidden_layers":layers}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--stage",required=True,choices=sorted(STAGES))
    p.add_argument("--train",type=Path,required=True)
    p.add_argument("--validation",type=Path,required=True)
    p.add_argument("--holdout",type=Path,required=True)
    p.add_argument("--base-model",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--execute",action="store_true")
    args=p.parse_args()
    try:
        branch=subprocess.run(["git","branch","--show-current"],cwd=ROOT,
            capture_output=True,text=True,check=True,timeout=10).stdout.strip()
        if branch!="Qwen-Local-Helper":raise TrainError("Cannot train on main")
        if args.output.exists() or not args.output.resolve().is_relative_to(DATA.resolve()):
            raise TrainError("Adapter output must be NEW and inside lab/data")
        model_meta=local_base(args.base_model)
        split_meta=validate(args.train,args.validation,args.holdout)
        if args.stage=="04":
            print("WARNING: Stage 04 training is limited to left-arm IK pilot, NO pole placement.")
        cmd=[sys.executable,str(ROOT/"qwen-helper"/"train_specialist.py"),
            "--specialist",STAGES[args.stage],"--train",str(args.train),
            "--output",str(args.output),"--base-model",str(args.base_model)]
        print("Dataset:",json.dumps(split_meta))
        print("Full-weight checkpoint:",json.dumps(model_meta))
        print("Training command:",json.dumps(cmd))
        if not args.execute:
            print("DRY RUN only. No GPU used. --execute required.")
            return 0
        import torch
        if not torch.cuda.is_available():
            raise TrainError("No CUDA GPU for actual QLoRA")
        prop=torch.cuda.get_device_properties(0)
        vram=prop.total_memory/(1024**3)
        if vram<23.5:
            raise TrainError(f"Training requires about >=24 GB VRAM; available {vram:.1f} GB")
        env=os.environ.copy()
        env["HF_HUB_OFFLINE"]="1"
        env["TRANSFORMERS_OFFLINE"]="1"
        env["HF_DATASETS_OFFLINE"]="1"
        subprocess.run(cmd,cwd=ROOT,env=env,check=True)
        print("Candidate LoRA only; must merge/quantize, pin Ollama digest, and independently qualify.")
        return 0
    except (TrainError,OSError,ValueError,KeyError,ImportError,subprocess.CalledProcessError,
            subprocess.TimeoutExpired,json.JSONDecodeError) as exc:
        print("TRAIN STOP:",exc,file=sys.stderr)
        return 2
if __name__=="__main__":
    sys.exit(main())
