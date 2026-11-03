#!/usr/bin/env python3
"""Isolated script proposal path for stages 03–06; no unreviewed Blender execution."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.request import Request, urlopen

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DATA=HERE/"data"
REGISTRY=ROOT/"qwen-helper"/"specialists.json"
TRACKS=HERE/"tracks.json"
TASK_ID=re.compile(r"[a-z0-9][a-z0-9_-]{2,50}\Z")
STAGES={"03","04","05","06"}

class Stop(ValueError):
    pass

def config():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))

def read_runtime():
    path=DATA/"runtime.json"
    if path.is_symlink() or not path.is_file():
        raise Stop("Run training-workbench/install.py using your existing Ollama model")
    cfg=json.loads(path.read_text(encoding="utf-8"))
    if cfg.get("schema_version")!=1 or not cfg.get("model") or not cfg.get("digest"):
        raise Stop("Invalid existing Ollama runtime pin")
    return cfg

def verify_branch():
    result=subprocess.run(["git","branch","--show-current"],cwd=ROOT,
                          capture_output=True,text=True,timeout=10,check=True)
    if result.stdout.strip()!="Qwen-Local-Helper":
        raise Stop("Stage worker forbidden outside Qwen-Local-Helper branch")

def read_task(path):
    task=json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(task,dict):
        raise Stop("Invalid task object")
    return task

def qualify_task(task, *, demo=False):
    if not TASK_ID.fullmatch(str(task.get("task_id",""))):
        raise Stop("Invalid task ID")
    stage=task.get("stage")
    if stage not in STAGES:
        raise Stop("Only stages 03–06 can run Qwen main workers. Stage 00 is Codex-only.")
    tracks=json.loads(TRACKS.read_text(encoding="utf-8"))["stages"]
    mapping=next((s for s in tracks if s["stage"]==stage),None)
    if not mapping or mapping["specialist"]!=task.get("specialist"):
        raise Stop("Specialist/stage mismatch")
    reg=config()
    spec=reg["specialists"].get(task["specialist"])
    if not spec or spec.get("kind")!="stage_candidate" or spec.get("stage")!=stage:
        raise Stop("Not a registered stage candidate specialist")
    if task.get("kind")!="stage_candidate" or task.get("scope")!="character_specific":
        raise Stop("Wrong task kind/scope")
    for field in ("objective","expected_behavior","constraints","character_profile_summary"):
        v=task.get(field)
        if not isinstance(v,str) or not v.strip() or len(v)>2400:
            raise Stop("Missing/oversized "+field)
    stem=task["task_id"]
    expected=f"qwen-helper/training-workbench/data/candidates/{stem}/candidate.py"
    if task.get("target")!=expected:
        raise Stop("Output must remain a private candidate script under workbench/data")
    if not task.get("fixture_only") and demo:
        raise Stop("Demo requires fixture_only=true")
    if demo:
        if not task.get("fixture_only") or task.get("accepted_input_path") or task.get("accepted_input_sha256"):
            raise Stop("Demo must use synthetic fixtures only, no production assets")
    else:
        if task.get("fixture_only"):
            raise Stop("Fixture-only demo cannot enter production")
        for key in ("accepted_input_path","accepted_input_sha256","accepted_predecessor_evidence"):
            if not isinstance(task.get(key),str) or not task[key].strip():
                raise Stop("Production stage requires approved input and predecessor evidence")
        path=Path(task["accepted_input_path"])
        if path.is_absolute() or ".." in path.parts:
            raise Stop("Approved input must have a safe project-relative path")
        full=(ROOT/path).resolve()
        inputs=(DATA/"inputs").resolve()
        if not full.is_relative_to(inputs) or not full.is_file() or full.is_symlink():
            raise Stop("Production input must be private local copy in workbench/data/inputs")
        if hashlib.sha256(full.read_bytes()).hexdigest()!=task["accepted_input_sha256"]:
            raise Stop("Accepted input copy hash mismatch")
        evidence=Path(task["accepted_predecessor_evidence"])
        if evidence.is_absolute() or ".." in evidence.parts or not (ROOT/evidence).is_file():
            raise Stop("Approved predecessor evidence missing")
        import specialists
        specialists.verify_served_model({"specialist":task["specialist"],"stage":stage,
                                         "kind":"stage_candidate","scope":"character_specific",
                                         "target":task["target"]})
    return spec

def plan(task, demo=False):
    try:
        verify_branch()
        spec=qualify_task(task,demo=demo)
        if not demo:
            gate=subprocess.run([sys.executable,str(ROOT/"qwen-helper"/"review.py"),
                                 "--fail-over-threshold"],cwd=ROOT,text=True,capture_output=True,timeout=10)
            if gate.returncode:raise Stop("10% production review gate blocked Qwen")
        model=read_runtime()["model"] if demo else spec["model"]
        return {"route":"local_qwen_one_attempt","stage":task["stage"],
                "specialist":task["specialist"],"model":model,
                "mode":"synthetic_proposal_only" if demo else "qualified_stage_candidate",
                "on_failure":"original_codex_pipeline"}
    except (ValueError,OSError,KeyError,TypeError,subprocess.CalledProcessError,
            subprocess.TimeoutExpired,json.JSONDecodeError) as exc:
        return {"route":"original_codex_pipeline","reason":str(exc),
                "local_attempts_remaining":0}

def generate(task, demo=False):
    decision=plan(task,demo=demo)
    if decision["route"]!="local_qwen_one_attempt":
        return decision
    model=decision["model"]
    local=read_runtime()
    if demo:
        # Demo must use exactly the installed/pinned local tag, and never signal a production queue.
        if model!=local["model"]:
            return {"route":"original_codex_pipeline","reason":"Demo runtime mismatch"}
    else:
        if model==local["model"] and not config()["specialists"][task["specialist"]]["qualified"]:
            return {"route":"original_codex_pipeline","reason":"Unqualified specialist"}
    out=ROOT/task["target"]
    if out.exists() or out.is_symlink():
        return {"route":"original_codex_pipeline","reason":"Candidate already exists; no retry"}
    task_json=json.dumps({key:task[key] for key in
        ("stage","specialist","objective","expected_behavior","constraints","character_profile_summary","fixture_only") if key in task})
    prompt=(
        "You are a narrow PMX to native Blender Python construction specialist. "
        "Output only a JSON object with target, code and explanation. "
        "Your code is inert until independently reviewed by Codex; do not request executions. "
        "Code must use Blender bpy, preserve source, create or test only a PRIVATE derivative, "
        "never delete/overwrite input or approved objects, never approve gates or use network. "
        "Stages 03 geometry, 04 controls, 05 facial/animation usability, 06 animation tests. "
        "Never infer character semantics, rest spaces or artwork. "
        "On insufficient evidence return an empty code string. Task: "+task_json+
        " Target: "+task["target"])
    request=Request(local["api"],data=json.dumps({
        "model":model,"prompt":prompt,"stream":False,"format":"json",
        "options":{"temperature":0.0,"num_ctx":4096,"num_predict":1800}}).encode(),
        headers={"Content-Type":"application/json"})
    try:
        with urlopen(request,timeout=180) as response:
            obj=json.loads(json.loads(response.read().decode("utf-8"))["response"])
        code=obj.get("code")
        if obj.get("target")!=task["target"] or not isinstance(code,str) or not code.strip():
            raise Stop("Empty or mismatched Qwen candidate")
        if len(code.encode("utf-8"))>12000:
            raise Stop("Stage candidate exceeds 12 KB")
        compile(code,task["target"],"exec")  # syntax only; never execute here
        path=DATA/"candidates"/task["task_id"]
        path.mkdir(parents=True,exist_ok=False)
        record={"task":task,"model":model,"base_sha256":None,
                "proposal":{"target":task["target"],"code":code,
                            "explanation":str(obj.get("explanation",""))[:2000]}}
        proposal=path/"proposal.json"
        proposal.write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
        (path/"candidate.py").write_text(code,encoding="utf-8")
        # The watcher reads an identical JSON outbox entry for qualified production only.
        if not demo:
            outbox=ROOT/"qwen-helper"/"outbox"
            outbox.mkdir(parents=True,exist_ok=True)
            handoff=outbox/(task["task_id"]+".json")
            handoff.write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
            import done
            done.emit(task["specialist"],task["task_id"])
        return {"route":"pending_codex_review" if not demo else "synthetic_proposal_only",
                "proposal":str(proposal.relative_to(ROOT)),
                "never_executed":True,"requires_human_stage_gate":True}
    except (Stop,OSError,ValueError,KeyError,TimeoutError,SyntaxError,
            json.JSONDecodeError) as exc:
        return {"route":"original_codex_pipeline","reason":str(exc),
                "local_attempts_remaining":0}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=("plan","propose","demo"))
    parser.add_argument("--task",required=True)
    args=parser.parse_args()
    try:
        task=read_task(args.task)
        output=plan(task,False) if args.command=="plan" else generate(task,demo=args.command=="demo")
    except (ValueError,OSError,KeyError,TypeError,json.JSONDecodeError) as exc:
        output={"route":"original_codex_pipeline","reason":str(exc)}
    print(json.dumps(output,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
