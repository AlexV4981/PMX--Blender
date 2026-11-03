#!/usr/bin/env python3
"""Stage-mapped, fail-closed local Qwen training workbench.

No auto downloads, no automatic qualification, no promotion to production.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import random
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HELPER = ROOT / "qwen-helper"
DATA = HERE / "data"
CATALOG = HERE / "tracks.json"
STAGE_ID = re.compile(r"[0-9]{2}\Z")
CASE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{2,127}\Z")
SPLITS = ("train", "validation", "holdout")
REQUIRED = ("case_id", "group_id", "source_type", "provenance", "verified_by",
            "verification", "prompt", "completion")

class Stop(ValueError):
    pass

def check_branch():
    p = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT,
                       text=True, capture_output=True, timeout=10, check=True)
    if p.stdout.strip() != "Qwen-Local-Helper":
        raise Stop("Work is restricted to Qwen-Local-Helper; no main changes allowed")

def catalog():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise Stop("Unsupported curriculum version")
    return data

def tracks():
    stages = catalog()["stages"]
    if sorted(x["stage"] for x in stages) != [f"{i:02d}" for i in range(10)]:
        raise Stop("Curriculum must cover original stages 00–09 exactly")
    return stages

def lookup(name):
    for stage in tracks():
        if stage["specialist"] == name:
            if stage["eligibility"] != "training_ready":
                raise Stop("Not eligible for local specialization")
            return stage
    raise Stop("Unknown or Codex-only training track")

def registry():
    cfg = json.loads((HELPER / "specialists.json").read_text(encoding="utf-8"))
    if cfg.get("version") != 1:
        raise Stop("Unsupported specialist registry")
    for stage in tracks():
        name = stage["specialist"]
        if name and name not in cfg["specialists"]:
            raise Stop("Unregistered specialist " + name)
    return cfg

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def print_map():
    registry()
    print("00→09 original order; Qwen assists only with narrow reports/fixtures.")
    for stage in tracks():
        print(f'{stage["stage"]} {stage["skill"]:<30} -> {stage["specialist"] or "CODEX ONLY"}')

def bootstrap():
    check_branch()
    registry()
    for name in ("raw", "splits", "adapters", "evaluations", "logs"):
        (DATA / name).mkdir(parents=True, exist_ok=True)
    print("Bootstrapped ignored local workspace:", DATA)
    print("Supply independently verified raw/<specialist>.jsonl examples before prepare.")

def load_raw(path):
    if not path.is_file() or path.is_symlink():
        raise Stop("Missing or symlinked raw dataset: " + str(path))
    rows=[]
    seen=set()
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row=json.loads(raw)
        except json.JSONDecodeError as exc:
            raise Stop(f"Invalid JSON line {n}: {exc}") from exc
        if not isinstance(row, dict):
            raise Stop(f"Expected object at line {n}")
        for field in REQUIRED:
            if not isinstance(row.get(field), str) or not row[field].strip():
                raise Stop(f"Line {n} missing independently verified field: {field}")
        if any(row[key].startswith("FILL_") for key in REQUIRED):
            raise Stop(f"Line {n} still contains a placeholder")
        if not CASE_ID.fullmatch(row["case_id"]):
            raise Stop(f"Invalid case_id on line {n}")
        if row["case_id"] in seen:
            raise Stop(f"Duplicate case ID: {row['case_id']}")
        seen.add(row["case_id"])
        if len(row["prompt"]) > 12000 or len(row["completion"]) > 20000:
            raise Stop(f"Oversize example on line {n}")
        rows.append(row)
    if not rows:
        raise Stop("No verified examples")
    return rows

def group_partition(rows, seed=271828):
    """Entire source families remain in exactly one split."""
    groups=defaultdict(list)
    for row in rows:
        groups[row["group_id"]].append(row)
    if len(groups) < 5:
        raise Stop("At least five independent source families required for split")
    labels=sorted(groups)
    random.Random(seed).shuffle(labels)
    n=len(labels)
    n_hold=max(1,round(n*0.2))
    n_val=max(1,round(n*0.1))
    if n-n_hold-n_val < 2:
        raise Stop("Insufficient independent training groups")
    assignments={"holdout":labels[:n_hold],
                 "validation":labels[n_hold:n_hold+n_val],
                 "train":labels[n_hold+n_val:]}
    return {split:[r for g in keys for r in groups[g]] for split,keys in assignments.items()}

def output_for(track):
    return DATA / "splits" / track

def prepare(name):
    check_branch()
    lookup(name)
    registry()
    raw=DATA / "raw" / f"{name}.jsonl"
    rows=load_raw(raw)
    parts=group_partition(rows)
    dest=output_for(name)
    if dest.exists() and any(dest.iterdir()):
        raise Stop("Frozen split exists; refuse overwrite. Archive and explicitly remove it before regenerating.")
    dest.mkdir(parents=True,exist_ok=True)
    hashes={}
    for split in SPLITS:
        p=dest / f"{split}.jsonl"
        with p.open("x",encoding="utf-8") as f:
            for row in parts[split]:
                f.write(json.dumps(row,ensure_ascii=False,sort_keys=True)+"\n")
        hashes[split]=sha(p)
    manifest={"schema_version":1,"specialist":name,"source_sha256":sha(raw),
              "seed":271828,"split_sha256":hashes,
              "counts":{key:len(parts[key]) for key in SPLITS},
              "group_counts":{key:len({r["group_id"] for r in parts[key]}) for key in SPLITS},
              "note":"Frozen group-split datasets, NOT a model qualification."}
    (dest / "manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2))

def validate_splits(name):
    dest=output_for(name)
    manifest=json.loads((dest/"manifest.json").read_text(encoding="utf-8"))
    if manifest.get("specialist") != name:
        raise Stop("Split manifest for another specialist")
    raw=DATA/"raw"/f"{name}.jsonl"
    if sha(raw)!=manifest["source_sha256"]:
        raise Stop("Raw source changed since frozen splits")
    parts={}
    for split in SPLITS:
        p=dest/f"{split}.jsonl"
        if sha(p)!=manifest["split_sha256"][split]:
            raise Stop("Frozen split mutated")
        parts[split]=load_raw(p)
    ids=[{r["case_id"] for r in parts[s]} for s in SPLITS]
    groups=[{r["group_id"] for r in parts[s]} for s in SPLITS]
    for a in range(3):
        for b in range(a+1,3):
            if ids[a]&ids[b] or groups[a]&groups[b]:
                raise Stop("Cross-split leakage detected")
    return manifest

def status(name=None):
    registry()
    items=[lookup(name)] if name else tracks()
    for t in items:
        key=t["specialist"]
        if not key:
            print(t["stage"],"CODEX ONLY",t["title"])
            continue
        raw=DATA/"raw"/f"{key}.jsonl"
        frozen=output_for(key)/"manifest.json"
        spec=registry()["specialists"][key]
        desc="missing verified data"
        if raw.is_file():
            try:
                rows=load_raw(raw)
                desc=f'{len(rows)} verified examples / {len(set(r["group_id"] for r in rows))} groups'
            except (Stop,OSError) as e:
                desc="invalid raw data: "+str(e)
        if frozen.is_file():
            try:
                validate_splits(key)
                desc+="; frozen clean group splits"
            except (Stop,OSError,KeyError,ValueError) as e:
                desc+="; INVALID SPLITS: "+str(e)
        print(f'{t["stage"]} {key}: {desc}; qualified={spec["qualified"]}')

def train(name, epochs=2, max_length=1024, base_model=None, allow_download=False):
    check_branch()
    lookup(name)
    registry()
    validate_splits(name)
    # Explicitly require an existing environment; do not silently install packages/models.
    model=HELPER/"train_specialist.py"
    train_path=output_for(name)/"train.jsonl"
    out=DATA/"adapters"/name
    if out.exists():
        raise Stop("Adapter directory exists; refuse silent overwrite")
    cmd=[sys.executable,str(model),"--specialist",name,"--train",str(train_path),
         "--output",str(out),"--epochs",str(epochs),"--max-length",str(max_length)]
    if base_model:
        cmd.extend(["--base-model",base_model])
    if allow_download:
        cmd.append("--allow-download")
    print("Training local candidate, NOT qualified:",name,flush=True)
    subprocess.run(cmd,cwd=ROOT,check=True)

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest="action",required=True)
    sub.add_parser("map")
    sub.add_parser("bootstrap")
    st=sub.add_parser("status");st.add_argument("--track")
    pr=sub.add_parser("prepare");pr.add_argument("--track",required=True)
    tr=sub.add_parser("train");tr.add_argument("--track",required=True)
    tr.add_argument("--epochs",type=int,default=2);tr.add_argument("--max-length",type=int,default=1024)
    tr.add_argument("--base-model",help="Existing full-weight Hugging Face checkpoint directory")
    tr.add_argument("--allow-download",action="store_true",help="Allow HF model download explicitly")
    args=parser.parse_args(argv)
    try:
        if args.action=="map":print_map()
        elif args.action=="bootstrap":bootstrap()
        elif args.action=="status":status(args.track)
        elif args.action=="prepare":prepare(args.track)
        else:train(args.track,args.epochs,args.max_length,args.base_model,args.allow_download)
    except (Stop,ValueError,OSError,KeyError,subprocess.CalledProcessError,
            subprocess.TimeoutExpired,json.JSONDecodeError) as exc:
        print("WORKBENCH STOP:",exc,file=sys.stderr)
        return 2
    return 0
if __name__=="__main__":
    sys.exit(main())
