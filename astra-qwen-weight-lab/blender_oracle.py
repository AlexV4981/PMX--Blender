#!/usr/bin/env python3
"""Deterministic Blender oracle for one synthetic Qwen candidate.

MUST be executed INSIDE a disposable no-network sandbox, not on the host.
bpy is imported at runtime; this file is also importable for pure-Python tests.
"""
import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time
import traceback

def assert_safe_environment():
    if os.environ.get("PMX_QWEN_ISOLATED_BLENDER")!="I_ACKNOWLEDGE_NO_NETWORK_SANDBOX":
        raise RuntimeError("Untrusted Qwen code requires external isolated sandbox with no network, mounts/limits")

def setup_stage(scene,case):
    import bpy
    from mathutils import Vector
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    p=case["params"];stage=case["stage"]
    if stage in ("03","05"):
        offset=p.get("vertex_offset",0.03)
        verts=[(0,0,0),(1+offset,0,0),(1,1,0),(0,1,0)]
        mesh=bpy.data.meshes.new("SyntheticMeshData")
        mesh.from_pydata(verts,[],[(0,1,2),(0,2,3)])
        mesh.update()
        name="RepairMesh" if stage=="03" else "FaceMesh"
        obj=bpy.data.objects.new(name,mesh);scene.collection.objects.link(obj)
        bpy.context.view_layer.objects.active=obj
        obj.select_set(True)
        obj.shape_key_add(name="Basis",from_mix=False)
        if stage=="03":
            obj.shape_key_add(name="smile",from_mix=False)
            keys={name:obj.vertex_groups.new(name=name) for name in ("DEF_A","DEF_B","MASK")}
            for idx,(a,b) in enumerate(p["weights"]):
                keys["DEF_A"].add([idx],a,"REPLACE")
                keys["DEF_B"].add([idx],b,"REPLACE")
                keys["MASK"].add([idx],p["mask"],"REPLACE")
        else:
            for name in p["keys"]:
                obj.shape_key_add(name=name,from_mix=False)
        return obj
    if stage in ("04","06"):
        arm=bpy.data.armatures.new("SyntheticArmatureData")
        name="ArmaturePilot" if stage=="04" else "MotionArm"
        obj=bpy.data.objects.new(name,arm);scene.collection.objects.link(obj)
        bpy.context.view_layer.objects.active=obj
        obj.select_set(True)
        bpy.ops.object.mode_set(mode="EDIT")
        if stage=="04":
            upper=arm.edit_bones.new("UpperArm_L");upper.head=(0,0,0)
            upper.tail=(p["bend"],0,p["upper"])
            lower=arm.edit_bones.new("Forearm_L");lower.parent=upper;lower.use_connect=True
            lower.head=upper.tail;lower.tail=(p["bend"]*2,0,p["upper"]+p["lower"])
        else:
            b=arm.edit_bones.new("TestBone");b.head=(0,0,0);b.tail=(0,p["length"],0)
        bpy.ops.object.mode_set(mode="OBJECT")
        return obj
    raise RuntimeError("Unsupported stage")

def snapshot(stage,obj,case):
    if stage=="03":
        return {
          "positions":[tuple(v.co) for v in obj.data.vertices],
          "keys":{k.name:[tuple(x.co) for x in k.data]
                  for k in obj.data.shape_keys.key_blocks},
          "mask":[obj.vertex_groups["MASK"].weight(i) for i in range(len(obj.data.vertices))]}
    if stage=="04":
        return {name:(tuple(obj.data.bones[name].head_local),tuple(obj.data.bones[name].tail_local))
                for name in ("UpperArm_L","Forearm_L")}
    if stage=="05":
        return list(obj.data.shape_keys.key_blocks.keys())
    if stage=="06":
        return tuple(obj.pose.bones["TestBone"].rotation_euler)
    raise RuntimeError("Unsupported snapshot")

def validate(scene,obj,case,before,result):
    import bpy
    stage=case["stage"];p=case["params"]
    if stage=="03":
        after=snapshot(stage,obj,case)
        if after!=before:
            return False,"Geometry, MASK, or shape keys changed"
        for i,(a,b) in enumerate(p["weights"]):
            aa=obj.vertex_groups["DEF_A"].weight(i)
            bb=obj.vertex_groups["DEF_B"].weight(i)
            if abs(aa+bb-1)>1e-5 or abs(aa-a/(a+b))>1e-5:
                return False,f"Deform weights not normalized at vertex {i}"
        return True,"All DEF weights normalized; source geometry/morph/MASK intact"
    if stage=="04":
        if snapshot(stage,obj,case)!=before:
            return False,"Accepted armature rest data changed"
        lower=obj.pose.bones["Forearm_L"]
        constraints=[c for c in lower.constraints if c.type=="IK"]
        if len(constraints)!=1:
            return False,"Exactly one pilot IK constraint required"
        c=constraints[0]
        if c.chain_count!=2 or not c.target or c.target.name!="IKTarget":
            return False,"IK target/chain mismatch"
        if c.pole_target is not None:
            return False,"Pole placement unresolved: do not create poles"
        if getattr(c,"use_stretch",False):
            return False,"IK stretch must be disabled"
        expected=tuple(obj.data.bones["Forearm_L"].tail_local)
        if (c.target.matrix_world.translation - __import__("mathutils").Vector(expected)).length>1e-4:
            return False,"IK target not at source arm tip"
        return True,"Source arm preserved; left-arm no-pole IK pilot established"
    if stage=="05":
        if snapshot(stage,obj,case)!=before:
            return False,"Shape key topology changed"
        controller=bpy.data.objects.get("CTRL_Face")
        if not controller or controller.type!="EMPTY":
            return False,"Missing native controller empty"
        keys=obj.data.shape_keys.key_blocks
        deps=bpy.context.evaluated_depsgraph_get()
        for name in p["keys"]:
            if name not in controller:
                return False,"Missing custom property for "+name
            ad=obj.data.shape_keys.animation_data
            if ad is None or ad.drivers is None:
                return False,"Shape-key driver missing"
            path='key_blocks["'+name+'"].value'
            drivers=[f for f in ad.drivers if f.data_path==path]
            if len(drivers)!=1:
                return False,"Shape-key FCurve missing for "+name
            for v in (0.0,0.5,1.0):
                controller[name]=v
                bpy.context.view_layer.update()
                measured=obj.evaluated_get(deps).data.shape_keys.key_blocks[name].value
                if abs(measured-v)>2e-4:
                    return False,f"Driver mismatch {name}: expected {v}, observed {measured}"
            controller[name]=0.0
        bpy.context.view_layer.update()
        for name in p["keys"]:
            if abs(obj.evaluated_get(deps).data.shape_keys.key_blocks[name].value)>1e-4:
                return False,"Neutral not restored"
        return True,"All three native shape key drivers measured and reset"
    if stage=="06":
        if not isinstance(result,dict) or not isinstance(result.get("samples"),list):
            return False,"Expected return dict with samples"
        if len(result["samples"])!=len(p["angles"]):
            return False,"Wrong sample count"
        bone=obj.pose.bones["TestBone"]
        if tuple(bone.rotation_euler)!=before:
            return False,"Neutral pose not restored"
        for expected_angle,sample in zip(p["angles"],result["samples"]):
            if not isinstance(sample,dict) or abs(float(sample.get("angle_deg",1e6))-expected_angle)>1e-4:
                return False,"Unexpected angle sample"
            tip=sample.get("tip")
            if not isinstance(tip,(list,tuple)) or len(tip)!=3:
                return False,"Missing evaluated tip"
            import mathutils
            bone.rotation_mode="XYZ"
            bone.rotation_euler[2]=math.radians(expected_angle)
            bpy.context.view_layer.update()
            measured=tuple(obj.matrix_world @ bone.tail)
            if any(abs(float(a)-b)>2e-4 for a,b in zip(tip,measured)):
                return False,"Tip location incorrect compared with independent Blender evaluation"
        bone.rotation_euler=(0,0,0)
        bpy.context.view_layer.update()
        return True,"Pose samples independently compared; neutral restored"
    return False,"Unsupported stage"

def execute(case,source):
    import bpy
    started=time.monotonic()
    scene=bpy.context.scene
    obj=setup_stage(scene,case)
    before=snapshot(case["stage"],obj,case)
    clean_source=source.read_text(encoding="utf-8")
    mod={"__builtins__":__builtins__,"__name__":"__qwen_candidate__"}
    marker={"case_id":case["case_id"],"stage":case["stage"],"blender_executed":True,
        "blender_pass":False,"sol_light_reviewed":False,"protected_assets_ok":False,
        "severe_regression":False,"elapsed_seconds":0,"evidence":"actual isolated Blender oracle",
        "source_sha256":hashlib.sha256(clean_source.encode()).hexdigest()}
    try:
        exec(compile(clean_source,str(source),"exec"),mod)
        solve=mod.get("solve")
        if not callable(solve):
            raise RuntimeError("Script must expose callable solve(scene)")
        outcome=solve(scene)
        good,reason=validate(scene,obj,case,before,outcome)
        marker["blender_pass"]=bool(good)
        marker["protected_assets_ok"]=bool(good)
        marker["error_feedback"]="" if good else reason
        marker["oracle_detail"]=reason
    except Exception as exc:
        marker["error_feedback"]=str(exc)[:2000]
        marker["oracle_detail"]=traceback.format_exc()[-3000:]
    marker["elapsed_seconds"]=round(time.monotonic()-started,3)
    return marker

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--case",required=True,type=Path)
    p.add_argument("--source",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    args=p.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else None)
    try:
        assert_safe_environment()
        case=json.loads(args.case.read_text(encoding="utf-8"))
        if case.get("stage") not in ("03","04","05","06"):
            raise RuntimeError("Stage 00 and unrelated tasks forbidden")
        if args.out.exists():
            raise RuntimeError("Refusing to overwrite result")
        result=execute(case,args.source)
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
        print(json.dumps(result))
        return 0 if result["blender_pass"] else 1
    except Exception as exc:
        print("ORACLE STOP:",exc,file=sys.stderr)
        return 2

if __name__=="__main__":
    sys.exit(main())
