#!/usr/bin/env python3
"""Validate explicit material decisions/evidence, never infer roles or edit Blender.
A successful result proves plan structure and referenced evidence presence only.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

ROLES={'base-color','normal-tangent','normal-object','roughness','metallic','occlusion',
       'opacity','emission-color','emission-mask','toon-lookup','sphere-map','face-sdf',
       'light-map','packed-data','unknown'}
DATA=ROLES-{'base-color','emission-color','sphere-map','toon-lookup','unknown'}


def validate(plan,base):
    base=Path(base);errors=[]
    def need(condition,message):
        if not condition:errors.append(message)
    def evidence(value,label):
        need(isinstance(value,list) and bool(value),label+': actual evidence files required')
        for item in value if isinstance(value,list) else []:
            if not isinstance(item,str):errors.append(label+': invalid evidence path');continue
            f=base/item
            need(f.is_file() and f.stat().st_size>0,label+': missing/empty evidence '+item)
    def text(value):return isinstance(value,str) and bool(value.strip())
    need(plan.get('schema_version')==1,'schema_version must be 1')
    need(plan.get('qualification')=='plan_only_not_visual_acceptance','qualification label required')
    evidence(plan.get('baseline_evidence'),'baseline')
    materials=plan.get('materials');need(isinstance(materials,list) and bool(materials),'materials required')
    seen=set()
    for m in materials if isinstance(materials,list) else []:
        if not isinstance(m,dict):errors.append('material record must be object');continue
        label=str(m.get('id','<missing>'))
        need(text(m.get('id')) and label not in seen,label+': unique id required');seen.add(label)
        need(text(m.get('owner')),label+': mesh/slot ownership required')
        need(m.get('status') in {'preserve','proposed','blocked'},label+': status required')
        evidence(m.get('diagnostic_evidence'),label)
        need(text(m.get('output_method')),label+': output method/limits required')
        maps=m.get('maps');need(isinstance(maps,list),label+': maps list required')
        for x in maps if isinstance(maps,list) else []:
            if not isinstance(x,dict):errors.append(label+': map must be object');continue
            role=x.get('role');need(role in ROLES,label+': invalid role')
            need(type(x.get('required_for_fidelity')) is bool,label+': explicit required_for_fidelity boolean required')
            need(text(x.get('uv_map')),label+': uv_map or explicit not-applicable rationale required')
            need(text(x.get('image_datablock')),label+': explicit image datablock required')
            if role=='unknown':
                need(text(x.get('unknown_reason')),label+': unknown_reason required')
                need(x.get('connection')=='unconnected',label+': unknown map must stay unconnected')
                need(not x.get('required_for_fidelity') or m.get('status')=='blocked',label+': required unknown map must block material')
            else:
                evidence(x.get('role_evidence'),label+'/'+str(role))
                need(text(x.get('color_space')) and text(x.get('color_space_rationale')),label+': color-space decision/rationale required')
                if role in DATA:
                    need(x.get('color_space')=='Non-Color' or bool(x.get('encoding_exception_evidence')),
                         label+': data map needs Non-Color or evidenced encoding exception')
                    if x.get('color_space')!='Non-Color' and x.get('encoding_exception_evidence'):
                        evidence(x['encoding_exception_evidence'],label+'/encoding')
                if role=='packed-data':
                    channels=x.get('channel_roles',{})
                    need(isinstance(channels,dict) and set(channels)==set('RGBA'),label+': packed RGBA roles required (unused explicit)')
                    if isinstance(channels,dict):need(all(text(v) for v in channels.values()),label+': empty packed channel role')
                if role=='opacity':need(x.get('alpha_association') in {'STRAIGHT','PREMUL','CHANNEL_PACKED','NONE'},label+': alpha association required')
            image=x.get('file');f=base/image if isinstance(image,str) and image else None
            need(f is not None and f.is_file(),label+': exact map file required')
            if f and f.is_file():
                h=hashlib.sha256(f.read_bytes()).hexdigest();need(x.get('sha256')==h,label+': map hash mismatch')
        evidence(m.get('regression_evidence'),label+'/regression')
    return errors


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan');a=p.parse_args()
    try:
        path=Path(a.plan);plan=json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(plan,dict):raise ValueError('Plan must be an object')
        errors=validate(plan,path.parent)
        print(json.dumps({'valid':not errors,'qualification':'plan_only_not_visual_acceptance','errors':errors},indent=2))
        return 2 if errors else 0
    except (OSError,ValueError,TypeError) as e:p.exit(2,str(e)+'\n')

if __name__=='__main__':raise SystemExit(main())
