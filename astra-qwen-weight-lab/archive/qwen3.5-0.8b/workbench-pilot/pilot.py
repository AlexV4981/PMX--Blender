#!/usr/bin/env python3
"""Opt-in, read-only-inference comparison of local Ollama models for PMX stages 03–06.

This does NOT run or accept generated code. No model downloads, fine-tuning,
candidate .blend changes, or automatic specialist qualification.
"""
import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
DATA = ROOT / "qwen-helper" / "training-workbench" / "data"
STAGES = {"03": "geometry", "04": "rig", "05": "animator controls", "06": "animation and deformation tests"}
BLOCKED_MODULES = {"subprocess", "socket", "requests", "urllib", "http", "ftplib", "paramiko"}
BLOCKED_CALLS = {"eval", "exec", "compile", "__import__"}
MAX_SOURCE_BYTES = 15000

class PilotError(ValueError):
    pass

def read_branch():
    return subprocess.run(["git", "branch", "--show-current"], cwd=ROOT,
        check=True, text=True, capture_output=True, timeout=10).stdout.strip()

def require_branch():
    if read_branch() != "Qwen-Local-Helper":
        raise PilotError("Pilot is restricted to Qwen-Local-Helper; never use main")

def installed():
    with urlopen("http://127.0.0.1:11434/api/tags", timeout=6) as resp:
        payload = json.load(resp)
    return {m["name"]: m["digest"] for m in payload.get("models", [])
            if isinstance(m, dict) and m.get("name") and m.get("digest")}

def read_cases(path):
    if path.is_symlink() or not path.is_file():
        raise PilotError("Missing/unsafe cases JSONL")
    rows = []
    ids = set()
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        case = json.loads(line)
        if not isinstance(case, dict) or case.get("stage") not in STAGES:
            raise PilotError(f"Bad stage in case line {line_no}")
        cid=case.get("case_id")
        if not isinstance(cid, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_-]{2,60}", cid) or cid in ids:
            raise PilotError(f"Bad/duplicate case_id in line {line_no}")
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip() or len(case["prompt"]) > 5000:
            raise PilotError(f"Bad/oversized prompt in line {line_no}")
        if not isinstance(case.get("expected_behavior"), str) or not case["expected_behavior"].strip():
            raise PilotError(f"Missing expected_behavior in line {line_no}")
        if not isinstance(case.get("fixture_family"), str) or not case["fixture_family"].strip():
            raise PilotError(f"Missing fixture_family in line {line_no}")
        ids.add(cid)
        rows.append(case)
    if not rows or len(rows) > 200:
        raise PilotError("Need 1–200 independent synthetic or approved fixture tasks")
    return rows

def validate_code(text):
    if not isinstance(text, str) or not text.strip() or len(text.encode("utf-8")) > MAX_SOURCE_BYTES:
        return {"syntax_valid":False,"static_warnings":["Empty/oversized source"]}
    try:
        tree=ast.parse(text)
    except SyntaxError as exc:
        return {"syntax_valid":False,"static_warnings":[f"SyntaxError: {exc.msg}"]}
    warnings=[]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in BLOCKED_MODULES:
                    warnings.append("Blocked import: "+alias.name)
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] in BLOCKED_MODULES:
                warnings.append("Blocked from-import: "+str(node.module))
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in BLOCKED_CALLS:
                warnings.append("Dynamic execution call: "+node.func.id)
    return {"syntax_valid":True,"static_warnings":sorted(set(warnings))}

def build_prompt(case):
    return (
       f"Write one small, self-contained Blender Python bpy script for STAGE {case['stage']} "
       f"({STAGES[case['stage']]}). Your task is constrained and uses ONLY synthetic or "
       "explicitly approved fixture data. Never open original PMX files, modify accepted "
       ".blend files, access credentials/network, run shell commands, or declare stage approval. "
       "Produce JSON with 'code' and 'explanation'. If uncertain, return empty code.\n"
       "Task: "+case["prompt"]+"\nAcceptance behavior: "+case["expected_behavior"]+
       "\nNo code is executed by this benchmark."
    )

def infer(model, case, think=False, timeout=180):
    request=Request("http://127.0.0.1:11434/api/generate",
        data=json.dumps({"model":model,"prompt":build_prompt(case),"stream":False,
            "format":"json","think":think,
            "options":{"temperature":0.0,"num_ctx":4096,"num_predict":2048}}).encode("utf-8"),
        headers={"Content-Type":"application/json"})
    start=time.monotonic()
    with urlopen(request,timeout=timeout) as response:
        result=json.load(response)
    elapsed=time.monotonic()-start
    try:
        parsed=json.loads(result.get("response",""))
    except (json.JSONDecodeError,TypeError):
        parsed=None
    code=parsed.get("code") if isinstance(parsed,dict) else None
    checks=validate_code(code)
    return {"response_json_valid":isinstance(parsed,dict),"syntax_valid":checks["syntax_valid"],
            "static_warnings":checks["static_warnings"],
            "code":code if isinstance(code,str) else "",
            "explanation":str(parsed.get("explanation",""))[:1000] if isinstance(parsed,dict) else "",
            "elapsed_seconds":round(elapsed,2),"prompt_eval_count":result.get("prompt_eval_count"),
            "eval_count":result.get("eval_count"),
            "important":"Syntax/static checks DO NOT establish Blender correctness or safety."}

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases",required=True,type=Path)
    parser.add_argument("--models",required=True,help="Comma-separated exact tags already installed in Ollama")
    parser.add_argument("--out",required=True,type=Path,help="Under qwen-helper/training-workbench/data/")
    parser.add_argument("--think",action="store_true",help="Enable thinking; default is off to avoid 0.8B loops")
    args=parser.parse_args(argv)
    try:
        require_branch()
        cases=read_cases(args.cases)
        tags=[x.strip() for x in args.models.split(",")]
        if not tags or any(not x for x in tags) or len(set(tags)) != len(tags):
            raise PilotError("Supply unique non-empty model tags")
        models=installed()
        unknown=[tag for tag in tags if tag not in models]
        if unknown:
            raise PilotError("Models not installed locally; no downloads attempted: "+", ".join(unknown))
        out=args.out.resolve()
        if not out.is_relative_to(DATA.resolve()) or args.out.is_symlink() or out.exists():
            raise PilotError("Output must be a NEW file beneath ignored workbench/data/")
        out.parent.mkdir(parents=True,exist_ok=True)
        with out.open("x",encoding="utf-8") as dest:
            for model in tags:
                for case in cases:
                    try:
                        result=infer(model,case,think=args.think)
                        record={"case_id":case["case_id"],"stage":case["stage"],
                           "fixture_family":case["fixture_family"],
                           "expected_behavior":case["expected_behavior"],
                           "model":model,"model_digest":models[model],
                           "thinking":args.think,"inference":result}
                    except (OSError,ValueError,KeyError,TimeoutError) as exc:
                        record={"case_id":case["case_id"],"stage":case["stage"],
                           "fixture_family":case["fixture_family"],"model":model,
                           "model_digest":models[model],"error":str(exc)}
                    dest.write(json.dumps(record,ensure_ascii=False)+"\n")
                    dest.flush()
                    print(model,case["case_id"],"syntax:",
                          record.get("inference",{}).get("syntax_valid",False),flush=True)
        print("Saved inert proposals to",out)
        print("NEXT: Codex independently runs approved candidates in an isolated Blender sandbox,")
        print("records actual passes/failures, then uses Astra for failed work. NOT a qualification.")
        return 0
    except (PilotError,OSError,ValueError,KeyError,subprocess.CalledProcessError,
            subprocess.TimeoutExpired,json.JSONDecodeError) as exc:
        print("PILOT STOP:",exc,file=sys.stderr)
        return 2

if __name__=="__main__":
    sys.exit(main())
