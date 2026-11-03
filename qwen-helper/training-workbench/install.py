#!/usr/bin/env python3
"""Set up stage 03–06 Qwen workers using an ALREADY installed Ollama model."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.request import urlopen

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HELPER = ROOT / "qwen-helper"
RUNTIME = HERE / "data" / "runtime.json"
PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:/+-]{0,180}\Z")

class InstallError(ValueError):
    pass

def branch():
    result = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT,
                            text=True, capture_output=True, timeout=10, check=True)
    return result.stdout.strip()

def available_models():
    with urlopen("http://127.0.0.1:11434/api/tags", timeout=5) as response:
        models = json.loads(response.read().decode("utf-8")).get("models", [])
    return {m["name"]:m["digest"] for m in models
            if isinstance(m,dict) and isinstance(m.get("name"),str)
            and isinstance(m.get("digest"),str) and m["digest"]}

def choose(models, explicit=None, preferred=None):
    if explicit:
        if not PATTERN.fullmatch(explicit) or explicit not in models:
            raise InstallError("Requested model not installed; no auto pull allowed")
        return explicit
    if preferred in models:
        return preferred
    qwen = [name for name in models if "qwen" in name.lower() and "coder" in name.lower()]
    if len(qwen) == 1:
        return qwen[0]
    if len(qwen) > 1:
        raise InstallError("Multiple Qwen coder tags found: " + ", ".join(sorted(qwen)) +
                           ". Choose one with --model EXISTING_TAG")
    raise InstallError("No installed Qwen coding tag; no download attempted")

def install(model=None):
    if branch() != "Qwen-Local-Helper":
        raise InstallError("Must be checked out on Qwen-Local-Helper, not main")
    if not (ROOT/"skills"/"anime-blender-pipeline"/"SKILL.md").is_file():
        raise InstallError("Missing original PMX pipeline")
    models = available_models()
    desired = json.loads((HELPER/"project.json").read_text(encoding="utf-8")).get("model")
    tag = choose(models, explicit=model, preferred=desired)
    if RUNTIME.is_symlink():
        raise InstallError("Unsafe runtime config symlink")
    RUNTIME.parent.mkdir(parents=True, exist_ok=True)
    expected = {"schema_version":1,"model":tag,"digest":models[tag],"provider":"ollama",
                "api":"http://127.0.0.1:11434/api/generate","production_qualified":False,
                "note":"Local installed base for demos; never a substitute for specialist qualification."}
    if RUNTIME.exists():
        existing = json.loads(RUNTIME.read_text(encoding="utf-8"))
        if existing.get("model") != tag or existing.get("digest") != models[tag]:
            raise InstallError("Local runtime already pinned to a different model/digest; inspect manually")
        print("Preserved existing pinned runtime:",RUNTIME)
    else:
        RUNTIME.write_text(json.dumps(expected,indent=2)+"\n",encoding="utf-8")
        print("Pinned existing Ollama model:",tag)
    for sub in ("raw","splits","adapters","evaluations","logs","candidates","inputs"):
        (HERE/"data"/sub).mkdir(parents=True,exist_ok=True)
    print("Ollama digest:",models[tag])
    print("Stage 00: CODEX ONLY. Stages 03/04/05/06: unqualified until independent evaluation.")
    print("No downloads, fine-tuning, Blender execution, or changes to main.")
    return expected

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--model",help="Exact tag from your existing Ollama installation")
    a=p.parse_args()
    try:
        install(a.model)
        return 0
    except (InstallError,OSError,ValueError,KeyError,subprocess.CalledProcessError,
            subprocess.TimeoutExpired,json.JSONDecodeError) as exc:
        print("INSTALL STOP:",exc,file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
