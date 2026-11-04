#!/usr/bin/env python3
"""Independent local Ollama inference pilot. NEVER executes generated Python."""
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import time
from urllib.request import Request, urlopen

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
DATA=HERE/"data"
CONFIG=HERE/"config.json"
STAGES={"03","04","05","06"}
RESTRICTED_IMPORTS={"subprocess","socket","requests","urllib","ftplib","paramiko"}

class LabError(ValueError):
    pass

def git_branch():
    return subprocess.run(
        ["git","branch","--show-current"], cwd=ROOT, check=True,
        capture_output=True,text=True,timeout=12
    ).stdout.strip()

def require_branch():
    if git_branch()!="Qwen-Local-Helper":
        raise LabError("Must use Qwen-Local-Helper, NEVER main")

def load_config():
    cfg=json.loads(CONFIG.read_text(encoding="utf-8"))
    if cfg.get("schema_version")!=1:
        raise LabError("Unrecognized configuration")
    return cfg

def local_models():
    with urlopen("http://127.0.0.1:11434/api/tags",timeout=5) as r:
        payload=json.load(r)
    return {m["name"]:m["digest"] for m in payload.get("models",[])
            if isinstance(m,dict) and m.get("name") and m.get("digest")}

def load_cases(path):
    if not path.is_file() or path.is_symlink():
        raise LabError("Cases missing or symlink")
    seen=set()
    cases=[]
    for n,line in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not line.strip():
            continue
        row=json.loads(line)
        if not isinstance(row,dict) or row.get("stage") not in STAGES:
            raise LabError(f"Case {n} is not a permitted stage 03-06 task")
        cid=row.get("case_id")
        if (not isinstance(cid,str) or not re.fullmatch(r"[a-z0-9][a-z0-9_-]{2,70}",cid)
            or cid in seen):
            raise LabError(f"Invalid or repeated case id in line {n}")
        for field in ("fixture_family","prompt","expected_behavior"):
            if not isinstance(row.get(field),str) or not row[field].strip():
                raise LabError(f"Missing {field} on line {n}")
        if len(row["prompt"])>8000:
            raise LabError("Prompt too long")
        seen.add(cid)
        cases.append(row)
    if not cases or len(cases)>4000:
        raise LabError("Expected 1-4000 cases")
    return cases

def inspect_code(code):
    if not isinstance(code,str) or not code.strip() or len(code.encode("utf-8"))>15000:
        return {"syntax_ok":False,"static_warnings":["Empty or oversized code"]}
    try:
        parsed=ast.parse(code)
    except SyntaxError as exc:
        return {"syntax_ok":False,"static_warnings":["Syntax error: "+exc.msg]}
    warnings=[]
    for node in ast.walk(parsed):
        if isinstance(node,ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in RESTRICTED_IMPORTS:
                    warnings.append("Disallowed network/subprocess import: "+alias.name)
        elif isinstance(node,ast.ImportFrom):
            if (node.module or "").split(".")[0] in RESTRICTED_IMPORTS:
                warnings.append("Disallowed network/subprocess import: "+str(node.module))
        elif isinstance(node,ast.Call) and isinstance(node.func,ast.Name):
            if node.func.id in {"eval","exec","__import__"}:
                warnings.append("Dynamic execution: "+node.func.id)
    return {"syntax_ok":True,"static_warnings":sorted(set(warnings))}

def prompt_for(case):
    return (
        "You are a narrowly specialized PMX to native Cycles Blender assistant. "
        "Return ONLY a JSON object containing code and explanation. "
        "Write ONE bounded Blender bpy Python script for a disposable synthetic or "
        "explicitly approved input; never access network, delete originals, invent "
        "bone/morph semantics, modify frozen checkpoints, or claim human approval. "
        "If uncertain return empty code.\n"
        "Stage: "+case["stage"]+"\nTask: "+case["prompt"]+
        "\nExpected behavior: "+case["expected_behavior"]+
        "\nIMPORTANT: The evaluator does not execute generated code."
    )

def infer(tag,case,thinking=False):
    opt=load_config()["defaults"]
    request=Request("http://127.0.0.1:11434/api/generate",
        data=json.dumps({
            "model":tag,"prompt":prompt_for(case),"stream":False,"format":"json",
            "think":thinking,
            "options":{"temperature":opt["temperature"],
                       "num_ctx":opt["num_ctx"],"num_predict":opt["num_predict"]}
        }).encode("utf-8"),headers={"Content-Type":"application/json"})
    started=time.monotonic()
    with urlopen(request,timeout=240) as r:
        reply=json.load(r)
    elapsed=round(time.monotonic()-started,3)
    try:
        obj=json.loads(reply.get("response",""))
    except (ValueError,TypeError):
        obj=None
    code=obj.get("code") if isinstance(obj,dict) else None
    return {"response_json_ok":isinstance(obj,dict),
            "code":code if isinstance(code,str) else "",
            "explanation":str(obj.get("explanation",""))[:800] if isinstance(obj,dict) else "",
            "static":inspect_code(code),"elapsed_seconds":elapsed,
            "prompt_tokens":reply.get("prompt_eval_count"),
            "output_tokens":reply.get("eval_count"),
            "warning":"Static checks are NOT executable Blender validation."}

def under_data(path):
    real=path.resolve()
    if not real.is_relative_to(DATA.resolve()) or path.is_symlink():
        raise LabError("Output must be under ignored lab/data and cannot be a symlink")
    if path.exists():
        raise LabError("Never overwrite existing evidence")
    return real

def doctor():
    require_branch()
    cfg=load_config()
    print("Repository branch:",git_branch())
    print("Stages 00,01,02,07,08,09: original pipeline")
    print("Experimental specialist stages:",sorted(STAGES))
    print("Python:",sys.version.split()[0])
    for module in ("torch","safetensors","numpy"):
        print(module, bool(importlib.util.find_spec(module)))
    try:
        print("Installed Ollama models (unchanged):",json.dumps(local_models(),indent=2))
    except OSError as exc:
        print("Ollama unavailable:",exc)
    print("Configured model sources:",json.dumps(cfg["base_weights"],indent=2))

def init():
    require_branch()
    for folder in ("models","datasets","responses","verdicts","patches","deltas","reports","exports","logs"):
        (DATA/folder).mkdir(parents=True,exist_ok=True)
    print("Created ignored lab directories; existing Qwen helper files untouched")

def run_pilot(cases,models,output,thinking=False,only_stage=None):
    require_branch()
    model_map=local_models()
    tags=[t.strip() for t in models.split(",")]
    if not tags or any(not x for x in tags) or len(tags)!=len(set(tags)):
        raise LabError("Specify one or more unique installed model tags")
    if any(tag not in model_map for tag in tags):
        raise LabError("Model not installed; no auto-pull: "+str([x for x in tags if x not in model_map]))
    tests=load_cases(cases)
    if only_stage:
        if only_stage not in STAGES:
            raise LabError("Only stage 03,04,05,06 can run pilot")
        tests=[t for t in tests if t["stage"]==only_stage]
        if not tests:
            raise LabError("No cases for requested stage")
    dest=under_data(output)
    dest.parent.mkdir(parents=True,exist_ok=True)
    count=0
    with dest.open("x",encoding="utf-8") as f:
        for tag in tags:
            for case in tests:
                rec={"case_id":case["case_id"],"stage":case["stage"],
                     "fixture_family":case["fixture_family"],
                     "model":tag,"model_digest":model_map[tag],
                     "thinking":bool(thinking),"expected_behavior":case["expected_behavior"]}
                try:
                    rec["inference"]=infer(tag,case,thinking=thinking)
                except (OSError,TimeoutError,ValueError,KeyError) as exc:
                    rec["inference_error"]=str(exc)
                f.write(json.dumps(rec,ensure_ascii=False)+"\n")
                f.flush()
                count+=1
                print("Saved",tag,case["case_id"],flush=True)
    print("Inert responses:",count,"saved:",dest)
    print("Next: independent Codex evaluation in a safe disposable Blender sandbox; no model qualified.")

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest="command",required=True)
    sub.add_parser("doctor")
    sub.add_parser("init")
    run=sub.add_parser("pilot")
    run.add_argument("--cases",type=Path,default=HERE/"cases.example.jsonl")
    run.add_argument("--models",required=True,help="Comma-separated installed Ollama tags")
    run.add_argument("--out",required=True,type=Path)
    run.add_argument("--think",action="store_true")
    run.add_argument("--stage",choices=sorted(STAGES))
    a=p.parse_args(argv)
    try:
        if a.command=="doctor":doctor()
        elif a.command=="init":init()
        else:run_pilot(a.cases,a.models,a.out,a.think,a.stage)
        return 0
    except (LabError,OSError,ValueError,TypeError,KeyError,subprocess.CalledProcessError,
            subprocess.TimeoutExpired) as exc:
        print("LAB STOP:",exc,file=sys.stderr)
        return 2
if __name__=="__main__":
    raise SystemExit(main())
