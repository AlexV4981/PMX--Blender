#!/usr/bin/env python3
"""Read-only measurements, not a shader optimizer or stage acceptance tool.
NumPy required. Color input must explicitly declare matched display-sRGB samples.
"""
import argparse
import json
from pathlib import Path
import numpy as np


def vectors(value, width=3):
    a=np.asarray(value,dtype=float)
    if a.ndim<1 or a.shape[-1]!=width or not np.all(np.isfinite(a)):
        raise ValueError(f'Expected finite vectors with last dimension {width}')
    return a


def srgb_to_lab(rgb):
    """Display sRGB [0,1] -> XYZ D65 -> Lab D65; no ICC/OCIO/adaptation."""
    rgb=vectors(rgb)
    if np.any((rgb<0)|(rgb>1)):raise ValueError('sRGB samples must be within [0,1]')
    linear=np.where(rgb<=0.04045,rgb/12.92,((rgb+0.055)/1.055)**2.4)
    matrix=np.array([[.4124564,.3575761,.1804375],[.2126729,.7151522,.0721750],[.0193339,.1191920,.9503041]])
    xyz=(linear@matrix.T)/np.array([.95047,1.,1.08883])
    delta=6/29
    f=np.where(xyz>delta**3,np.cbrt(xyz),xyz/(3*delta**2)+4/29)
    return np.stack([116*f[...,1]-16,500*(f[...,0]-f[...,1]),200*(f[...,1]-f[...,2])],axis=-1)


def ciede2000(lab1,lab2):
    """Sharma/Wu/Dalal CIEDE2000; kL=kC=kH=1, broadcasting allowed."""
    a,b=np.broadcast_arrays(vectors(lab1),vectors(lab2))
    L1,a1,b1=np.moveaxis(a,-1,0);L2,a2,b2=np.moveaxis(b,-1,0)
    C1=np.hypot(a1,b1);C2=np.hypot(a2,b2);Cbar=(C1+C2)/2
    G=.5*(1-np.sqrt(Cbar**7/(Cbar**7+25.**7)))
    ap1=(1+G)*a1;ap2=(1+G)*a2
    cp1=np.hypot(ap1,b1);cp2=np.hypot(ap2,b2)
    hp1=np.mod(np.degrees(np.arctan2(b1,ap1)),360.)
    hp2=np.mod(np.degrees(np.arctan2(b2,ap2)),360.)
    hp1=np.where(cp1==0,0.,hp1);hp2=np.where(cp2==0,0.,hp2)
    dL=L2-L1;dC=cp2-cp1;dh=hp2-hp1;zero=(cp1*cp2==0)
    dh=np.where(zero,0.,np.where(dh>180,dh-360,np.where(dh < -180,dh+360,dh)))
    dH=2*np.sqrt(cp1*cp2)*np.sin(np.radians(dh)/2)
    lbar=(L1+L2)/2;cbar=(cp1+cp2)/2
    hsum=hp1+hp2;hdiff=np.abs(hp1-hp2)
    hbar=np.where(zero,hsum,np.where(hdiff<=180,hsum/2,np.where(hsum<360,(hsum+360)/2,(hsum-360)/2)))
    T=1-.17*np.cos(np.radians(hbar-30))+.24*np.cos(np.radians(2*hbar))+.32*np.cos(np.radians(3*hbar+6))-.20*np.cos(np.radians(4*hbar-63))
    SL=1+.015*(lbar-50)**2/np.sqrt(20+(lbar-50)**2)
    SC=1+.045*cbar;SH=1+.015*cbar*T
    RT=-2*np.sqrt(cbar**7/(cbar**7+25.**7))*np.sin(np.radians(60*np.exp(-((hbar-275)/25)**2)))
    x=dL/SL;y=dC/SC;z=dH/SH
    return np.sqrt(np.maximum(0.,x*x+y*y+z*z+RT*y*z))


def summarize(values,threshold=None):
    a=np.asarray(values,dtype=float).ravel()
    if a.size==0 or not np.all(np.isfinite(a)):raise ValueError('Need nonempty finite measurements')
    r={'count':int(a.size),'median':float(np.median(a)),'p95':float(np.percentile(a,95)),
       'maximum':float(np.max(a)),'rms':float(np.sqrt(np.mean(a*a)))}
    if threshold is not None:
        if not np.isfinite(threshold) or threshold<=0:raise ValueError('Threshold must be positive and finite')
        r.update(threshold=float(threshold),fraction_at_or_above_threshold=float(np.mean(a>=threshold)),
                 proposed_p95_target_met=bool(r['p95']<threshold))
    return r


def rigid_alignment(source,target):
    """Known-correspondence proper rigid fit. Return R,t for source @ R.T + t."""
    p=vectors(source);q=vectors(target)
    if p.ndim!=2 or p.shape!=q.shape or len(p)<3:raise ValueError('Need matching N x 3 arrays, N>=3')
    pc=p-p.mean(axis=0);qc=q-q.mean(axis=0)
    if np.linalg.matrix_rank(pc)<2 or np.linalg.matrix_rank(qc)<2:raise ValueError('Collinear/degenerate correspondence')
    U,_,Vt=np.linalg.svd(pc.T@qc)
    V=Vt.T;fix=np.eye(3);fix[-1,-1]=1 if np.linalg.det(V@U.T)>=0 else -1
    R=V@fix@U.T;t=q.mean(axis=0)-R@p.mean(axis=0)
    residual=np.linalg.norm(p@R.T+t-q,axis=1)
    return {'rotation':R.tolist(),'translation':t.tolist(),'determinant':float(np.linalg.det(R)),
            'residuals':residual.tolist(),'summary':summarize(residual),
            'limitations':['Known correspondences required','No scale/reflection/nonrigid fitting','Not import acceptance']}


def quaternion_angle(q0,q1):
    """Radians, shortest orientation distance; both quaternions use same component order."""
    a=vectors(q0,4);b=vectors(q1,4);a,b=np.broadcast_arrays(a,b)
    na=np.linalg.norm(a,axis=-1,keepdims=True);nb=np.linalg.norm(b,axis=-1,keepdims=True)
    if np.any(na==0) or np.any(nb==0):raise ValueError('Zero quaternion')
    return 2*np.arccos(np.clip(np.abs(np.sum((a/na)*(b/nb),axis=-1)),0,1))


def color_report(data,base):
    if not isinstance(data,dict) or data.get('encoding')!='display-srgb':raise ValueError('Declare encoding=display-srgb; no implicit conversion')
    evidence=data.get('matched_conditions_evidence')
    if not isinstance(evidence,list) or not evidence:raise ValueError('Actual matched-condition evidence files required')
    for item in evidence:
        if not isinstance(item,str) or not item:raise ValueError('Invalid evidence path')
        path=Path(base)/item
        if not path.is_file() or path.stat().st_size==0:raise ValueError('Missing or empty comparison-condition evidence')
    regions=data.get('regions');out=[];names=set()
    if not isinstance(regions,list) or not regions:raise ValueError('Regions required')
    for region in regions:
        name=region.get('name')
        if not isinstance(name,str) or not name.strip() or name in names:raise ValueError('Unique nonempty region names required')
        names.add(name);a=vectors(region.get('reference_rgb'));b=vectors(region.get('candidate_rgb'))
        if a.ndim!=2 or a.shape!=b.shape or not len(a):raise ValueError('Each region needs equal nonempty N x 3 corresponding samples')
        delta=ciede2000(srgb_to_lab(a),srgb_to_lab(b))
        out.append({'name':name,**summarize(delta,3.),'sample_errors':delta.tolist()})
    return {'schema_version':1,'qualification':'diagnostic_measurements_not_stage_acceptance',
            'formula':'CIEDE2000','encoding':'display-srgb','white_point':'D65','parameters':{'kL':1,'kC':1,'kH':1},
            'provisional_target':'per-region p95 < 3; requires human calibration',
            'regions':out,'limitations':['No image registration or mask validation','Evidence presence is not proof of matched conditions',
            'No ICC/OCIO/tone mapping or chromatic adaptation','No shader optimization','No human approval or hidden-feature testing']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['colors','align'])
    p.add_argument('input');p.add_argument('--output',required=True);a=p.parse_args()
    try:
        source=Path(a.input);output=Path(a.output)
        if output.exists():raise ValueError('Refuse to overwrite evidence; choose a new output')
        data=json.loads(source.read_text(encoding='utf-8'))
        result=color_report(data,source.parent) if a.command=='colors' else rigid_alignment(data['source'],data['target'])
        output.parent.mkdir(parents=True,exist_ok=True)
        with output.open('x',encoding='utf-8') as f:f.write(json.dumps(result,indent=2,allow_nan=False)+'\n')
        print(json.dumps({'output':str(output),'qualification':'diagnostic_measurements_only'}));return 0
    except (OSError,ValueError,TypeError,KeyError,AttributeError,np.linalg.LinAlgError) as e:p.exit(2,str(e)+'\n')

if __name__=='__main__':raise SystemExit(main())
