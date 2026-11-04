#!/usr/bin/env python3
"""Create 80 parameterized synthetic tasks; never create training labels or touch PMX."""
import argparse
import json
import math
from pathlib import Path
import random
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
DATA=HERE/"data"/"fixtures"

class FixtureError(ValueError):
    pass

def cases():
    rng=random.Random(20261104)
    results=[]
    for stage in ("03","04","05","06"):
        for i in range(20):
            family=f"synthetic-{stage}-family-{i//4}"
            item={"case_id":f"stage{stage}-synthetic-{i:03d}","stage":stage,
                  "fixture_family":family,"synthetic":True,
                  "oracle":"astra-qwen-weight-lab/blender_oracle.py",
                  "case_version":1,"variant":i}
            if stage=="03":
                weights=[(round(rng.uniform(0.1,0.95),4),round(rng.uniform(0.1,0.95),4))
                         for _ in range(4)]
                item["params"]={"weights":weights,"mask":round(rng.uniform(.1,.9),4),
                                 "vertex_offset":round(rng.uniform(.02,.12),4)}
                item["prompt"]=(
                    "Implement def solve(scene) in bpy. The synthetic mesh object is named "
                    "'RepairMesh' with vertex groups DEF_A, DEF_B, MASK and Basis/smile shape keys. "
                    "Normalize only the DEF_A and DEF_B weights at every vertex to sum to 1; "
                    "leave MASK, all vertices and shape keys untouched; return a JSON-serializable "
                    "dictionary with modified vertex count. Never change source .blend files. "
                    f"Reference weights: {weights}."
                )
                item["expected_behavior"]="Deform weights normalized; MASK, geometry and morph indices unchanged."
            elif stage=="04":
                upper=round(rng.uniform(.6,1.3),4)
                lower=round(rng.uniform(.55,1.2),4)
                bend=round(rng.uniform(.1,.4),4)
                item["params"]={"upper":upper,"lower":lower,"bend":bend}
                item["prompt"]=(
                    "Implement def solve(scene) using bpy on synthetic armature ArmaturePilot. "
                    "Its only bones UpperArm_L and Forearm_L form a bent two-bone LEFT ARM with "
                    f"upper length {upper} and lower length {lower} (scene facts are authoritative). "
                    "Create an EMPTY named IKTarget at the existing Forearm_L tail and a native IK "
                    "constraint on Forearm_L targeting it, chain_count=2, stretch OFF, pole_target "
                    "UNSET. Preserve original bones/rest positions and do not invent pole placement. "
                    "Do not modify other rigs. Return a summary dictionary."
                )
                item["expected_behavior"]="Native two-bone IK target on left arm, no stretch or pole; armature rest unchanged."
            elif stage=="05":
                suffix=f"_{i:02d}"
                names=["BlinkLeft"+suffix,"BlinkRight"+suffix,"JawOpen"+suffix]
                item["params"]={"keys":names}
                item["prompt"]=(
                    "Implement def solve(scene) with Blender bpy. Synthetic object FaceMesh has "
                    "shape keys Basis, "+", ".join(names)+". Create a separate EMPTY named CTRL_Face "
                    "with custom float properties matching these exact observed keys, all default 0. "
                    "Drive each shape-key value from the corresponding controller property using "
                    "a valid SINGLE_PROP driver; do not create or delete shape keys. "
                    "Return a summary dictionary and leave all keys at neutral 0."
                )
                item["expected_behavior"]="Three independently driven real shape keys and reliable neutral restoration."
            else:
                angle=round(rng.uniform(8,65),2)
                sign=-1 if i%2 else 1
                angles=[0,sign*angle,-sign*round(angle*.57,2)]
                length=round(rng.uniform(.75,1.8),4)
                item["params"]={"angles":angles,"length":length}
                item["prompt"]=(
                    "Implement def solve(scene) in Blender bpy for synthetic object MotionArm. "
                    "It has one bone named TestBone, length "+str(length)+", rest aligned with +Y. "
                    "Sample its local Z Euler rotation at degrees "+str(angles)+". "
                    "Return a dict {'samples':[{'angle_deg':number,'tip':[x,y,z]},...]} "
                    "where tip is the actual evaluated tip position in world space. "
                    "Restore the bone's original neutral rotation even if measurement fails. "
                    "Do not repair geometry or claim full animation qualification."
                )
                item["expected_behavior"]="Accurate actual evaluated bone tip at all three angles and neutral reset."
            results.append(item)
    return results

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("action",choices=["generate","verify"])
    args=p.parse_args()
    try:
        branch=subprocess.run(["git","branch","--show-current"],cwd=ROOT,
            capture_output=True,text=True,check=True,timeout=10).stdout.strip()
        if branch!="Qwen-Local-Helper":
            raise FixtureError("Refuse outside Qwen-Local-Helper")
        items=cases()
        if len(items)!=80 or any(sum(x["stage"]==s for x in items)!=20 for s in ("03","04","05","06")):
            raise FixtureError("Expected exactly 20 examples per stage")
        path=DATA/"cases.jsonl"
        generated="".join(json.dumps(x,sort_keys=True)+"\n" for x in items)
        if args.action=="generate":
            path.parent.mkdir(parents=True,exist_ok=True)
            if path.exists():
                if path.read_text(encoding="utf-8")!=generated:
                    raise FixtureError("Existing generated dataset differs; preserve instead of overwriting")
            else:
                path.write_text(generated,encoding="utf-8")
        elif not path.is_file() or path.read_text(encoding="utf-8")!=generated:
            raise FixtureError("Generated dataset missing or modified")
        print("Verified:",len(items),"synthetic cases; 20 per stage; 5 parameter families per stage")
        print(path)
        print("These cases are only a parametric pilot, NOT an independent production holdout.")
        return 0
    except (FixtureError,OSError,ValueError,subprocess.CalledProcessError) as exc:
        print("FIXTURE STOP:",exc,file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
