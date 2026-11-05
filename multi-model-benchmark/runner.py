#!/usr/bin/env python3
"""Inert, one-model-at-a-time Ollama proposal recorder. NEVER executes generated code."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
REGISTRY = HERE / "models.json"
STAGES = {"03", "04", "05", "06"}
TAG = re.compile(r"[A-Za-z0-9_.-]+(?::[A-Za-z0-9_.-]+)?\Z")
DANGEROUS = {"subprocess", "socket", "requests", "urllib", "ftplib", "paramiko"}

class Stop(ValueError):
    pass

def branch_check():
    r = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, capture_output=True,
                       text=True, timeout=10, check=True)
    if r.stdout.strip() != "Multi-Model-PMX-Benchmark":
        raise Stop("Run only on Multi-Model-PMX-Benchmark branch")

def sha(data):
    return hashlib.sha256(data).hexdigest()

def installed():
    with urlopen("http://127.0.0.1:11434/api/tags", timeout=10) as r:
        d = json.load(r)
    return {m["name"]: m for m in d.get("models", []) if m.get("name") and m.get("digest")}

def load_cases(path, stage):
    if path.is_symlink() or not path.is_file():
        raise Stop("Fixture file absent or symlinked")
    cases = []
    ids = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        c = json.loads(line)
        if c.get("stage") != stage:
            continue
        if not isinstance(c.get("case_id"), str) or c["case_id"] in ids or not isinstance(c.get("prompt"), str) or not isinstance(c.get("params"), dict):
            raise Stop("Malformed/duplicate fixture")
        ids.add(c["case_id"])
        cases.append(c)
    if len(cases) != 20:
        raise Stop("Require 20 synthetic cases per stage; found " + str(len(cases)))
    return cases

def syntax(code):
    if not isinstance(code, str) or not code or len(code.encode()) > 24000:
        return {"valid": False, "warnings": ["missing or oversized code"]}
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {"valid": False, "warnings": ["syntax: " + e.msg]}
    warnings = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            warnings.extend("disallowed import: " + x.name for x in n.names if x.name.split(".")[0] in DANGEROUS)
        if isinstance(n, ast.ImportFrom) and (n.module or "").split(".")[0] in DANGEROUS:
            warnings.append("disallowed import: " + str(n.module))
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in ("eval", "exec", "__import__"):
            warnings.append("dynamic call: " + n.func.id)
    if not any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == "solve" for n in tree.body):
        warnings.append("missing solve(scene)")
    return {"valid": True, "warnings": sorted(set(warnings)), "blender_executed": False}

def prompt(case, stage, specialization):
    instructions = (
        "You are <model>, a narrowly scoped local PMX-to-Blender script PROPOSAL generator. "
        "Your code will be reviewed and executed ONLY by an independent trusted Blender oracle in a disposable no-network environment. "
        "Do not run tools, use shell/network/filesystem, modify originals, approve stage gates, or invent PMX bone semantics. "
        "Return JSON with keys code and explanation. The code must define solve(scene). "
        "If uncertain, return empty code. "
        "Stage 04 is LEFT-ARM PILOT ONLY; do not create pole targets or claim full rig completion. "
        "Stage 06 must NEVER modify the accepted rig. "
    )
    if specialization:
        p = ROOT / "skills" / ("anime-blender-" + stage + {"03":"-geometry","04":"-rig","05":"-ready","06":"-tests"}[stage]) / "references" / "stage.md"
        if not p.is_file() or p.is_symlink():
            raise Stop("Missing stage authority")
        instructions += "\nAuthoritative stage reference:\n" + p.read_text(encoding="utf-8")[:16000]
    return instructions + "\nSTAGE " + stage + "\nTASK " + case["prompt"] + "\nEXPECTED " + str(case.get("expected_behavior", ""))

def infer(model, text, temperature, ctx, output_tokens):
    body = {"model": model, "prompt": text, "stream": False, "format": "json",
            "options": {"temperature": temperature, "num_ctx": ctx, "num_predict": output_tokens}}
    req = Request("http://127.0.0.1:11434/api/generate",
                  data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    start = time.monotonic()
    with urlopen(req, timeout=600) as r:
        answer = json.load(r)
    elapsed = round(time.monotonic() - start, 3)
    try:
        obj = json.loads(answer.get("response", ""))
    except (ValueError, TypeError):
        obj = None
    code = obj.get("code", "") if isinstance(obj, dict) else ""
    return {"status": "produced", "response_json_valid": isinstance(obj, dict),
            "code": code if isinstance(code, str) else "",
            "explanation": str(obj.get("explanation", ""))[:1000] if isinstance(obj, dict) else "",
            "syntax": syntax(code), "elapsed_seconds": elapsed,
            "prompt_tokens": answer.get("prompt_eval_count"), "output_tokens": answer.get("eval_count"),
            "blender_executed": False, "blender_pass": None}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    i = sub.add_parser("inspect")
    i.add_argument("--model", required=True)
    p = sub.add_parser("run")
    p.add_argument("--model", required=True)
    p.add_argument("--stage", required=True, choices=sorted(STAGES))
    p.add_argument("--cases", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--specialized", action="store_true")
    p.add_argument("--temperature", type=float, default=0.0)
    p.add_argument("--ctx", type=int, default=4096)
    p.add_argument("--output-tokens", type=int, default=1536)
    args = parser.parse_args()
    branch_check()
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if args.command == "list":
        print(json.dumps(registry, indent=2))
        return 0
    if not TAG.fullmatch(args.model):
        raise Stop("Unsafe/invalid model tag")
    models = installed()
    if args.model not in models:
        raise Stop("Exact Ollama tag not installed: " + args.model + " (no automatic pull)")
    entry = models[args.model]
    if args.command == "inspect":
        print(json.dumps({"name": args.model, "digest": entry["digest"], "details": entry.get("details")}, indent=2))
        return 0
    if not (0 <= args.temperature <= 2 and 1024 <= args.ctx <= 32768 and 128 <= args.output_tokens <= 4096):
        raise Stop("Invalid decoding bounds")
    cases = load_cases(args.cases, args.stage)
    target = args.out.resolve()
    if args.out.is_symlink() or not target.is_relative_to(DATA.resolve()) or target.exists():
        raise Stop("Output must be a NEW file under ignored multi-model-benchmark/data/")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf-8") as f:
        for c in cases:
            ptext = prompt(c, args.stage, args.specialized)
            rec = {"stage": args.stage, "lap": "prompt_specialized" if args.specialized else "untuned",
                   "attempt": 1, "case_id": c["case_id"], "fixture_family": c.get("fixture_family"),
                   "model": args.model, "model_digest": entry["digest"],
                   "fixture_sha256": sha(json.dumps(c, sort_keys=True).encode()),
                   "prompt_sha256": sha(ptext.encode()),
                   "decoding": {"temperature": args.temperature, "num_ctx": args.ctx, "num_predict": args.output_tokens},
                   "expected_behavior": c.get("expected_behavior"),
                   "blender_executed": False, "blender_pass": None}
            try:
                rec["result"] = infer(args.model, ptext, args.temperature, args.ctx, args.output_tokens)
            except Exception as exc:
                rec["result"] = {"status": "inference_error", "error": type(exc).__name__ + ": " + str(exc)[:300],
                                 "blender_executed": False, "blender_pass": None}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            print(args.stage, args.model, c["case_id"], rec["result"]["status"], flush=True)
    print("INERT PROPOSALS ONLY. NO BLENDER EXECUTION OR VERIFIED PASS.")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except (Stop, OSError, ValueError, KeyError, subprocess.CalledProcessError) as e:
        print("STOP:", str(e), file=sys.stderr)
        sys.exit(2)
