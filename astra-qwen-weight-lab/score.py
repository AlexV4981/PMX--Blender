#!/usr/bin/env python3
"""Bind observed Blender oracles to exact first-try responses and score 7B pilots.

No inference, Blender execution, model promotion, or manufactured observations.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys

HERE=Path(__file__).resolve().parent
DATA=HERE/"data"
CFG=HERE/"config.json"

class ScoreError(ValueError):
    pass

def read_json(path):
    if path.is_symlink() or not path.is_file():
        raise ScoreError("Missing/unsafe evidence file: "+str(path))
    return json.loads(path.read_text(encoding="utf-8"))

def inside_data(path):
    if not path.resolve().is_relative_to(DATA.resolve()) or path.is_symlink():
        raise ScoreError("All outputs/input evidence must live inside ignored lab/data/")

def read_pilot(path):
    inside_data(path)
    results=[]
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip():
            item=json.loads(raw)
            if not isinstance(item,dict):raise ScoreError("Bad pilot record")
            results.append(item)
    return results

def extract(args):
    records=read_pilot(args.pilot)
    matches=[r for r in records if r.get("case_id")==args.case_id and r.get("model")==args.model
             and r.get("profile")==args.profile and r.get("thinking_requested")==args.thinking]
    if len(matches)!=1:
        raise ScoreError("Need exactly one matching pilot result")
    response=matches[0]
    if response.get("result",{}).get("status")!="produced":
        raise ScoreError("Candidate not produced")
    code=response["result"]["code"]
    if not isinstance(code,str) or not code.strip():
        raise ScoreError("Empty candidate")
    fixture=next((json.loads(s) for s in args.cases.read_text(encoding="utf-8").splitlines()
                  if s.strip() and json.loads(s).get("case_id")==args.case_id),None)
    if fixture is None or fixture.get("stage")!=response["stage"] or not fixture.get("synthetic"):
        raise ScoreError("Cannot associate response with exact synthetic fixture")
    output=args.outdir
    if not output.resolve().is_relative_to(DATA.resolve()) or output.is_symlink() or output.exists():
        raise ScoreError("Candidate output dir must be new and ignored")
    output.mkdir(parents=True,exist_ok=False)
    (output/"candidate.py").write_text(code,encoding="utf-8")
    (output/"case.json").write_text(json.dumps(fixture,indent=2)+"\n",encoding="utf-8")
    (output/"response.json").write_text(json.dumps(response,indent=2)+"\n",encoding="utf-8")
    print("INERT files written; must use isolated sandbox.py for Blender validation:",output)

def bind(args):
    inside_data(args.response);inside_data(args.oracle);inside_data(args.out)
    if args.out.exists():
        raise ScoreError("Never overwrite an existing verdict")
    response=read_json(args.response);oracle=read_json(args.oracle)
    if (oracle.get("case_id")!=response.get("case_id") or oracle.get("stage")!=response.get("stage")
            or oracle.get("blender_executed") is not True):
        raise ScoreError("Oracle must be actually executed on exact same stage/case")
    result=response.get("result",{})
    code=result.get("code")
    digest=hashlib.sha256(code.encode("utf-8")).hexdigest() if isinstance(code,str) else None
    if not digest or oracle.get("source_sha256")!=digest:
        raise ScoreError("Exact executed script SHA-256 mismatch")
    if type(oracle.get("blender_pass")) is not bool or type(oracle.get("protected_assets_ok")) is not bool:
        raise ScoreError("Unobserved Blender result fields")
    if type(oracle.get("severe_regression")) is not bool:
        raise ScoreError("No observed severe regression field")
    record={
        "case_id":response["case_id"],"stage":response["stage"],
        "fixture_family":response["fixture_family"],"model":response["model"],
        "model_digest":response["model_digest"],"profile":response["profile"],
        "thinking_requested":response["thinking_requested"],"attempt":response["attempt"],
        "blender_executed":True,"blender_pass":oracle["blender_pass"],
        "protected_assets_ok":oracle["protected_assets_ok"],
        "severe_regression":oracle["severe_regression"],
        "repair_needed":not (oracle["blender_pass"] and oracle["protected_assets_ok"]),
        "astra_fallback_used":False,"sol_light_reviewed":False,
        "error_feedback":oracle.get("error_feedback",""),
        "inference_seconds":result.get("elapsed_seconds"),
        "blender_seconds":oracle.get("elapsed_seconds"),
        "evidence":{"response":str(args.response.relative_to(DATA)),
                    "oracle":str(args.oracle.relative_to(DATA)),
                    "executed_source_sha256":digest},
        "qualified":False}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(record,indent=2))

def export_failures(args):
    inside_data(args.verdict_dir);inside_data(args.out)
    if args.out.exists():raise ScoreError("No overwriting failure exports")
    failures=[]
    for path in sorted(args.verdict_dir.glob("*.json")):
        v=read_json(path)
        if v.get("attempt")!=1 or v.get("blender_executed") is not True:
            continue
        if v.get("blender_pass") is True and v.get("protected_assets_ok") is True:
            continue
        if not isinstance(v.get("error_feedback"),str) or not v["error_feedback"].strip():
            raise ScoreError("Cannot retry without observed failure feedback")
        failures.append(v)
    if not failures:raise ScoreError("No observed failed first attempts")
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text("".join(json.dumps(v)+"\n" for v in failures),encoding="utf-8")
    print("Exported offline feedback retry inputs:",len(failures),"to",args.out)

def summarize(args):
    inside_data(args.verdict_dir)
    if not args.verdict_dir.is_dir():
        raise ScoreError("Verdict directory missing")
    config=json.loads(CFG.read_text(encoding="utf-8"))
    gate=config["pilot"]["go_no_go"]
    groups=defaultdict(list)
    seen=set()
    for path in sorted(args.verdict_dir.glob("*.json")):
        v=read_json(path)
        if v.get("attempt") not in (1,2) or v.get("stage") not in ("03","04","05","06"):
            raise ScoreError("Invalid stage/attempt")
        if not v.get("model_digest") or not v.get("profile") or not v.get("fixture_family"):
            raise ScoreError("Incomplete exact model and fixture identity")
        if (v.get("blender_executed") is not True or type(v.get("blender_pass")) is not bool
            or type(v.get("protected_assets_ok")) is not bool or type(v.get("severe_regression")) is not bool):
            raise ScoreError("Refuse unobserved or self-reported passes")
        key=(v["model"],v["model_digest"],v["stage"],v["profile"],v["thinking_requested"],
             v["attempt"],v["case_id"])
        if key in seen:raise ScoreError("Duplicate attempt verdict")
        seen.add(key)
        groups[key[:6]].append(v)
    results={}
    for key,rows in sorted(groups.items()):
        model,digest,stage,profile,thinking,attempt=key
        successes=sum(r["blender_pass"] and r["protected_assets_ok"] and not r["severe_regression"]
                      for r in rows)
        severe=sum(bool(r["severe_regression"] or not r["protected_assets_ok"]) for r in rows)
        full=len(rows)==20 and len({r["case_id"] for r in rows})==20
        first=attempt==1
        # Measured cost gate unavailable unless independently supplied by assessor.
        cost_gate="not_measured"
        if args.local_review_cost is not None and args.codex_cost is not None:
            cost_gate="pass" if args.local_review_cost/args.codex_cost<=gate["local_review_relative_cost_limit"] else "fail"
        technical=(full and first and successes/len(rows)>=gate["first_try_pass_rate_min"]
                   and severe<=gate["max_severe_regressions"])
        outcome="ready_for_independent_review" if technical and cost_gate=="pass" else "HOLD"
        results["/".join(map(str,key))]={
          "stage":stage,"model":model,"digest":digest,"profile":profile,
          "thinking_requested":thinking,"attempt":attempt,
          "cases":len(rows),"fixture_families":len({r["fixture_family"] for r in rows}),
          "first_try_verified_passes":successes if first else None,
          "first_try_pass_rate":round(successes/len(rows),4) if first else None,
          "experimental_retry_pass_rate":round(successes/len(rows),4) if not first else None,
          "repairs_needed":sum(bool(r["repair_needed"]) for r in rows),
          "severe_regressions":severe,
          "mean_inference_seconds":round(sum(float(r.get("inference_seconds") or 0) for r in rows)/len(rows),3),
          "mean_blender_seconds":round(sum(float(r.get("blender_seconds") or 0) for r in rows)/len(rows),3),
          "first_try_gate":technical,"cost_gate":cost_gate,"decision":outcome,
          "qualified":False,"note":"20 parametric cases are not production qualification"}
    print(json.dumps(results,indent=2))
    if args.out:
        inside_data(args.out)
        if args.out.exists():raise ScoreError("No overwriting reports")
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(json.dumps(results,indent=2)+"\n",encoding="utf-8")

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    actions=parser.add_subparsers(dest="action",required=True)
    a=actions.add_parser("extract")
    a.add_argument("--pilot",type=Path,required=True)
    a.add_argument("--cases",type=Path,default=DATA/"fixtures"/"cases.jsonl")
    a.add_argument("--case-id",required=True);a.add_argument("--model",required=True)
    a.add_argument("--profile",required=True)
    a.add_argument("--thinking",action="store_true");a.add_argument("--outdir",type=Path,required=True)
    b=actions.add_parser("bind")
    b.add_argument("--response",type=Path,required=True)
    b.add_argument("--oracle",type=Path,required=True)
    b.add_argument("--out",type=Path,required=True)
    d=actions.add_parser("export-failures")
    d.add_argument("--verdict-dir",type=Path,required=True)
    d.add_argument("--out",type=Path,required=True)
    c=actions.add_parser("summarize")
    c.add_argument("--verdict-dir",type=Path,required=True)
    c.add_argument("--codex-cost",type=float);c.add_argument("--local-review-cost",type=float)
    c.add_argument("--out",type=Path)
    args=parser.parse_args()
    try:
        if args.action=="extract":extract(args)
        elif args.action=="bind":bind(args)
        elif args.action=="export-failures":export_failures(args)
        else:summarize(args)
        return 0
    except (ScoreError,OSError,ValueError,KeyError,TypeError,ZeroDivisionError,json.JSONDecodeError) as exc:
        print("SCORE STOP:",exc,file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
