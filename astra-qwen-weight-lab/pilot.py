#!/usr/bin/env python3
"""7B baseline-versus-stage-Modelfile pilot; never executes generated code."""
import argparse
import ast
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
DATA=HERE/"data"
CFG=HERE/"config.json"
STAGES={"03","04","05","06"}
DISALLOWED={"subprocess","socket","requests","urllib","ftplib","paramiko"}

class PilotError(ValueError):
    pass

def require_branch():
    result=subprocess.run(["git","branch","--show-current"],cwd=ROOT,
        text=True,capture_output=True,timeout=10,check=True)
    if result.stdout.strip()!="Qwen-Local-Helper":
        raise PilotError("Only Qwen-Local-Helper; never main")

def config():
    p=json.loads(CFG.read_text(encoding="utf-8"))
    if p.get("schema_version")!=2:
        raise PilotError("Active Qwen 7B configuration required")
    return p

def models_installed():
    with urlopen("http://127.0.0.1:11434/api/tags",timeout=6) as r:
        data=json.load(r)
    return {m["name"]:m["digest"] for m in data.get("models",[])
            if isinstance(m,dict) and m.get("name") and m.get("digest")}

def load_cases(path,stage):
    if path.is_symlink() or not path.is_file():
        raise PilotError("Missing/symlinked fixture cases")
    cases=[]
    ids=set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():continue
        c=json.loads(raw)
        if c.get("stage")!=stage:continue
        if (c.get("case_id") in ids or c.get("stage") not in STAGES or
            not isinstance(c.get("fixture_family"),str) or
            not isinstance(c.get("prompt"),str) or not isinstance(c.get("params"),dict)):
            raise PilotError("Malformed/duplicate fixture")
        ids.add(c["case_id"]);cases.append(c)
    if len(cases)!=20:
        raise PilotError("Expect exactly 20 parametric cases per selected stage; found "+str(len(cases)))
    return cases

def syntax(code):
    if not isinstance(code,str) or not code.strip() or len(code.encode("utf-8"))>24000:
        return {"valid":False,"warnings":["missing/oversized code"]}
    try:
        tree=ast.parse(code)
    except SyntaxError as e:
        return {"valid":False,"warnings":["syntax: "+e.msg]}
    warnings=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Import):
            warnings.extend("disallowed import: "+x.name for x in node.names if x.name.split(".")[0] in DISALLOWED)
        elif isinstance(node,ast.ImportFrom):
            if (node.module or "").split(".")[0] in DISALLOWED:
                warnings.append("disallowed import: "+str(node.module))
        elif isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in ("eval","exec","__import__"):
            warnings.append("dynamic eval/import: "+node.func.id)
    if not any(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name=="solve" for n in tree.body):
        warnings.append("missing solve(scene) function")
    return {"valid":True,"warnings":sorted(set(warnings))}

def prompt_for(case,retry_feedback=None):
    fixed=(
        "Create exactly ONE Python Blender bpy script for a disposable SYNTHETIC PMX fixture. "
        "Declare def solve(scene): and return an observed summary dict. "
        "The human/Blender oracle will execute it separately in a no-network disposable Blender sandbox. "
        "Never access real PMX files, source or accepted .blend assets, credentials, network, shell, "
        "global filesystem, or alter anything outside the passed synthetic scene. "
        "Do not invent Blender API properties, character morph meanings, or rig transforms. "
        "Return only a JSON object with keys code and explanation. Empty code if uncertain. "
        "Stage 04 is LEFT ARM PILOT ONLY and MUST NOT add poles or claim full rig qualification. "
        "No model output itself counts as stage acceptance.\n"
    )
    body=f"STAGE {case['stage']}\nTASK: {case['prompt']}\nEXPECTED: {case['expected_behavior']}"
    if retry_feedback:
        body+="\nOFFLINE RESEARCH RETRY ONLY. Independent Blender oracle failed with: "+retry_feedback[:2000]
    return fixed+body

def execute_inference(model,case,profile,thinking,feedback=None):
    opts={k:profile[k] for k in ("temperature","num_ctx","num_predict")}
    request_data={"model":model,"prompt":prompt_for(case,feedback),
                  "stream":False,"format":"json","options":opts,
                  "think":thinking}
    req=Request("http://127.0.0.1:11434/api/generate",
                data=json.dumps(request_data).encode("utf-8"),
                headers={"Content-Type":"application/json"})
    start=time.monotonic()
    try:
        with urlopen(req,timeout=300) as resp:
            answer=json.load(resp)
    except HTTPError as exc:
        if thinking and exc.code in (400,422):
            return {"status":"thinking_unsupported","http_status":exc.code,
                    "elapsed_seconds":round(time.monotonic()-start,2)}
        raise
    elapsed=round(time.monotonic()-start,2)
    raw=answer.get("response","")
    try:
        obj=json.loads(raw)
    except (ValueError,TypeError):
        obj=None
    code=obj.get("code") if isinstance(obj,dict) else None
    return {"status":"produced","response_json_valid":isinstance(obj,dict),
            "code":code if isinstance(code,str) else "",
            "explanation":str(obj.get("explanation",""))[:1000] if isinstance(obj,dict) else "",
            "syntax":syntax(code),"elapsed_seconds":elapsed,
            "prompt_tokens":answer.get("prompt_eval_count"),"output_tokens":answer.get("eval_count"),
            "done_reason":answer.get("done_reason"),
            "hit_cap":answer.get("eval_count",0)>=profile["num_predict"] if isinstance(answer.get("eval_count"),int) else None,
            "thinking_accepted_by_api":thinking,
            "note":"API accepted think flag does not prove model truly supports reasoning mode."}

def safe_output(path):
    if path.is_symlink() or not path.resolve().is_relative_to(DATA.resolve()) or path.exists():
        raise PilotError("Output must be NEW and under ignored experiment data/")
    path.parent.mkdir(parents=True,exist_ok=True)

def run(args):
    require_branch()
    if args.stage not in STAGES:
        raise PilotError("Only stages 03–06; Stage 00 always Codex")
    cfg=config()
    cases=load_cases(args.cases,args.stage)
    tags=[x.strip() for x in args.models.split(",")]
    valid={cfg["base_ollama_tag"],cfg["stage_models"][args.stage]}
    if len(tags)!=2 or set(tags)!=valid:
        raise PilotError("Exactly two candidates required: installed 7B base and matching stage Modelfile tag")
    installed=models_installed()
    if any(t not in installed for t in tags):
        raise PilotError("Missing installed Ollama tag; no automatic download")
    profiles=[p for p in cfg["pilot"]["decoding_profiles"] if not args.profile or p["name"]==args.profile]
    if not profiles:
        raise PilotError("Unknown A/B decoding profile")
    safe_output(args.out)
    with args.out.open("x",encoding="utf-8") as f:
        for model in tags:
            for profile in profiles:
                # Qwen2.5-Coder-Instruct does NOT have a native thinking-mode contract.
                modes=[False]
                if args.thinking=="both":
                    modes=[False,True]
                elif args.thinking=="on":modes=[True]
                for thinking in modes:
                    for case in cases:
                        record={"attempt":1,"stage":args.stage,"case_id":case["case_id"],
                            "fixture_family":case["fixture_family"],"model":model,
                            "model_digest":installed[model],"profile":profile["name"],
                            "thinking_requested":thinking,"expected_behavior":case["expected_behavior"],
                            "case_params":case["params"]}
                        try:
                            record["result"]=execute_inference(model,case,profile,thinking)
                        except (OSError,HTTPError,URLError,TimeoutError,ValueError,KeyError) as exc:
                            record["result"]={"status":"inference_error","error":str(exc)}
                        f.write(json.dumps(record,ensure_ascii=False)+"\n")
                        f.flush()
                        print(args.stage,model,profile["name"],"think="+str(thinking),
                              case["case_id"],record["result"]["status"],flush=True)
    print("INERT RESPONSES ONLY:",args.out)
    print("Execute only through separately trusted, no-network Blender container and oracle.")

def retry(args):
    require_branch()
    cases={x["case_id"]:x for x in load_cases(args.cases,args.stage)}
    cfg=config();installed=models_installed()
    allowed={cfg["base_ollama_tag"],cfg["stage_models"][args.stage]}
    verified=[]
    for line in args.failures.read_text(encoding="utf-8").splitlines():
        if not line.strip():continue
        f=json.loads(line)
        if (f.get("stage")!=args.stage or f.get("case_id") not in cases
            or f.get("model") not in allowed or f.get("model_digest")!=installed.get(f.get("model"))
            or f.get("attempt")!=1 or f.get("blender_executed") is not True
            or f.get("blender_pass") is not False or not isinstance(f.get("error_feedback"),str)
            or not f["error_feedback"].strip()):
            raise PilotError("Retry requires a real failed first-try Blender verdict with correct exact model digest")
        verified.append(f)
    if not verified:
        raise PilotError("No observed first-attempt failures")
    safe_output(args.out)
    profile=next(p for p in cfg["pilot"]["decoding_profiles"] if p["name"]=="sampled_7b")
    with args.out.open("x",encoding="utf-8") as dest:
        for fail in verified:
            case=cases[fail["case_id"]]
            record={"attempt":2,"offline_retry_only":True,"case_id":case["case_id"],
                    "stage":args.stage,"model":fail["model"],"model_digest":fail["model_digest"],
                    "profile":profile["name"],"thinking_requested":False,
                    "parent_evidence":fail.get("evidence"),"fixture_family":case["fixture_family"]}
            record["result"]=execute_inference(fail["model"],case,profile,False,fail["error_feedback"])
            dest.write(json.dumps(record,ensure_ascii=False)+"\n")
    print("Offline experimental retry only; production one-shot remains unchanged.")

def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest="command",required=True)
    a=sub.add_parser("run");a.add_argument("--stage",required=True,choices=sorted(STAGES))
    a.add_argument("--cases",type=Path,default=DATA/"fixtures"/"cases.jsonl")
    a.add_argument("--models",required=True)
    a.add_argument("--profile",choices=["greedy_legacy","sampled_7b"])
    a.add_argument("--thinking",choices=["off","on","both"],default="off")
    a.add_argument("--out",type=Path,required=True)
    b=sub.add_parser("retry");b.add_argument("--stage",choices=sorted(STAGES),required=True)
    b.add_argument("--cases",type=Path,default=DATA/"fixtures"/"cases.jsonl")
    b.add_argument("--failures",type=Path,required=True)
    b.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    try:
        if args.command=="run":run(args)
        else:retry(args)
        return 0
    except (PilotError,OSError,ValueError,TypeError,KeyError,subprocess.CalledProcessError,
            subprocess.TimeoutExpired,StopIteration,json.JSONDecodeError) as exc:
        print("PILOT STOP:",exc,file=sys.stderr)
        return 2

if __name__=="__main__":
    sys.exit(main())
