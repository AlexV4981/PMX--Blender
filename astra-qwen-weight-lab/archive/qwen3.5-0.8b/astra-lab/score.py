#!/usr/bin/env python3
"""Summarize independently OBSERVED Blender verdicts and cost; never infer from syntax."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
DATA=ROOT/"data"

class ScoreError(ValueError):
    pass

def summarize(path,codex_baseline_cost=None,review_cost=None):
    if not path.is_file() or path.is_symlink():
        raise ScoreError("Verdict JSONL missing/unsafe")
    bins=defaultdict(list)
    seen=set()
    for line,raw in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not raw.strip():continue
        r=json.loads(raw)
        for field in ("case_id","stage","model","model_digest","fixture_family"):
            if not isinstance(r.get(field),str) or not r[field]:
                raise ScoreError(f"Line {line}: missing {field}")
        if r["stage"] not in ("03","04","05","06"):
            raise ScoreError(f"Line {line}: stage excluded")
        for field in ("blender_executed","blender_pass","sol_light_reviewed","protected_assets_ok"):
            if type(r.get(field)) is not bool:
                raise ScoreError(f"Line {line}: missing observed boolean {field}")
        if (not r["blender_executed"]) and r["blender_pass"]:
            raise ScoreError("Cannot pass without actual Blender execution")
        if type(r.get("elapsed_seconds")) not in (int,float) or r["elapsed_seconds"]<0:
            raise ScoreError("Time must be measured")
        if not isinstance(r.get("evidence"),str) or not r["evidence"]:
            raise ScoreError("Missing command/fixture evidence")
        k=(r["model"],r["model_digest"],r["stage"],r["case_id"])
        if k in seen:raise ScoreError("Duplicate model/case verdict")
        seen.add(k)
        bins[(r["model"],r["model_digest"],r["stage"])].append(r)
    summary={}
    for key,rows in sorted(bins.items()):
        total=len(rows)
        clean=sum(bool(x["blender_executed"] and x["blender_pass"] and x["protected_assets_ok"] and
                       x["sol_light_reviewed"]) for x in rows)
        families=len({r["fixture_family"] for r in rows})
        group="/".join(key)
        report={"tasks":total,"independent_families":families,"verified_first_pass":clean,
                "verified_first_pass_rate":clean/total,
                "mean_elapsed_seconds":sum(r["elapsed_seconds"] for r in rows)/total,
                "unqualified": True}
        if codex_baseline_cost is not None and review_cost is not None:
            # Baseline and fallback must have comparable units.
            report["assumed_relative_work"]=round(review_cost+(1-clean/total)*codex_baseline_cost,4)
            report["normal_codex_work"]=codex_baseline_cost
        summary[group]=report
    if not summary:raise ScoreError("No verdicts")
    return summary

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--verdicts",required=True,type=Path)
    p.add_argument("--normal-codex-cost",type=float)
    p.add_argument("--local-plus-review-cost",type=float)
    p.add_argument("--out",type=Path)
    a=p.parse_args(argv)
    try:
        if not a.verdicts.resolve().is_relative_to(DATA.resolve()):
            raise ScoreError("Verdicts must remain under ignored lab data")
        if (a.normal_codex_cost is None)!=(a.local_plus_review_cost is None):
            raise ScoreError("Both cost terms are required together")
        if a.normal_codex_cost is not None and (a.normal_codex_cost<=0 or a.local_plus_review_cost<0):
            raise ScoreError("Invalid cost values")
        results=summarize(a.verdicts,a.normal_codex_cost,a.local_plus_review_cost)
        rendered=json.dumps(results,indent=2)
        print(rendered)
        if a.out:
            if not a.out.resolve().is_relative_to(DATA.resolve()) or a.out.exists():
                raise ScoreError("Output must be a new ignored data path")
            a.out.parent.mkdir(parents=True,exist_ok=True)
            a.out.write_text(rendered+"\n",encoding="utf-8")
        return 0
    except (ScoreError,OSError,ValueError,TypeError,KeyError,json.JSONDecodeError) as exc:
        print("SCORE STOP:",exc,file=sys.stderr)
        return 2
if __name__=="__main__":
    raise SystemExit(main())
