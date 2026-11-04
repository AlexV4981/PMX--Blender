#!/usr/bin/env python3
"""Generate four stage-specific Ollama Modelfiles from the ACTUAL stage.md docs.

Never auto-pull a model. --create is opt-in and uses existing local Ollama.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.request import urlopen

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
DATA=HERE/"data"
CFG=HERE/"config.json"
STAGES={"03":"anime-blender-03-geometry","04":"anime-blender-04-rig","05":"anime-blender-05-ready","06":"anime-blender-06-tests"}

class ModelFileError(ValueError):
    pass

def check_branch():
    p=subprocess.run(["git","branch","--show-current"],cwd=ROOT,
       capture_output=True,text=True,check=True,timeout=10)
    if p.stdout.strip()!="Qwen-Local-Helper":
        raise ModelFileError("Only Qwen-Local-Helper, not main")

def installed():
    with urlopen("http://127.0.0.1:11434/api/tags",timeout=5) as r:
        return {m["name"]:m["digest"] for m in json.load(r).get("models",[])}

def render(stage,base,doc):
    if stage not in STAGES:
        raise ModelFileError("Only 03–06 are eligible")
    if not doc.strip():
        raise ModelFileError("Empty authoritative stage procedure")
    if '"""' in doc:
        raise ModelFileError("Unexpected Modelfile delimiter in stage procedure")
    prefix=(
      "You implement exactly one bounded PMX-to-native-Blender Cycles stage task. "
      "Return strictly JSON containing code and explanation. "
      "Use the supplied approved input mappings and only private disposable candidates. "
      "Never guess unsupported Blender properties, invent semantics, or alter source/accepted data. "
      "If missing evidence, return an empty code string. "
      "The original pipeline, real Sol Light review and human stage gate remain authoritative.\n"
      "The following is authoritative stage technical reference, not a prompt to bypass gates:\n"
    )
    if stage=="04":
        prefix+="CURRENT RESTRICTION: left-arm IK pilot ONLY. No pole-target placement, no full rig or unproven IK/FK claim. Return empty code if pole placement is required.\n"
    if stage=="06":
        prefix+="Do not make repairs during qualification or assert that unexecuted scripts pass.\n"
    content=prefix+doc
    return f'FROM {base}\nPARAMETER temperature 0.6\nPARAMETER num_ctx 8192\nPARAMETER num_predict 4096\nSYSTEM """\n{content}\n"""\n'

def build(create=False):
    check_branch()
    config=json.loads(CFG.read_text(encoding="utf-8"))
    base=config["base_ollama_tag"]
    actual=installed()
    if base not in actual:
        raise ModelFileError("Base tag not installed. No model downloads: "+base)
    outputs={}
    dest=DATA/"modelfiles"
    for stage,skill in STAGES.items():
        src=ROOT/"skills"/skill/"references"/"stage.md"
        body=src.read_text(encoding="utf-8")
        text=render(stage,base,body)
        dest.mkdir(parents=True,exist_ok=True)
        path=dest/f"stage{stage}.Modelfile"
        if path.exists():
            if path.read_text(encoding="utf-8")!=text:
                raise ModelFileError("Previously generated Modelfile differs; inspect before replacing")
        else:
            path.write_text(text,encoding="utf-8")
        tag=config["stage_models"][stage]
        outputs[stage]={"tag":tag,"modelfile":str(path.relative_to(ROOT)),
            "source_sha256":__import__("hashlib").sha256(body.encode()).hexdigest()}
        if create:
            subprocess.run(["ollama","create",tag,"-f",str(path)],cwd=ROOT,check=True)
    (DATA/"modelfiles"/"manifest.json").write_text(json.dumps(outputs,indent=2)+"\n",encoding="utf-8")
    return outputs

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--create",action="store_true",help="Explicitly create the 4 local Ollama tags")
    a=p.parse_args()
    try:
        print(json.dumps(build(a.create),indent=2))
    except (ModelFileError,OSError,ValueError,KeyError,subprocess.CalledProcessError,
            subprocess.TimeoutExpired) as exc:
        print("MODELFILE STOP:",exc,file=sys.stderr)
        return 2
    return 0

if __name__=="__main__":
    sys.exit(main())
