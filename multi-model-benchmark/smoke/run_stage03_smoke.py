#!/usr/bin/env python3
"""Run authored-correct and authored-wrong Stage 03 fixtures in *real* isolated Blender.

Requires a locally installed Docker image pinned by digest. Never downloads a model.
Produces a fresh ignored smoke ledger; deliberately cannot count as a model result.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

BENCH = Path(__file__).resolve().parents[1]
ROOT = BENCH.parent
sys.path.insert(0, str(BENCH))
from evidence import bridge, ingest, ledger as L, report

SAMPLES = {'correct': 'stage03_correct.py', 'wrong': 'stage03_wrong.py'}


def run(image, cases_path):
    branch = subprocess.run(['git', 'branch', '--show-current'], cwd=ROOT,
                            check=True, text=True, capture_output=True, timeout=10).stdout.strip()
    if branch != 'Multi-Model-PMX-Benchmark':
        raise L.LedgerError('Only run smoke on Multi-Model-PMX-Benchmark')
    samples = [json.loads(s) for s in cases_path.read_text(encoding='utf-8').splitlines()
               if s.strip() and json.loads(s).get('stage') == '03']
    if len(samples) != 20:
        raise L.LedgerError('Need 20 generated Stage 03 synthetic cases first')
    now = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    name = 'stage03-smoke-' + now
    base = BENCH / 'data' / name
    if base.exists():
        raise L.LedgerError('Smoke directory already exists')
    ledger = L.Ledger(base / 'ledger.jsonl')
    store = L.ArtifactStore(base / 'artifacts')
    exp = 'AUTHORED-SMOKE-ONLY'
    manifest = {'schema_version': 1, 'cases': [{'case_id': c['case_id'],
        'source_family': c['fixture_family'], 'split': 'dev'} for c in samples]}
    manifest_hash = store.put('split_manifests', (json.dumps(manifest, sort_keys=True)+'\n').encode(), '.json')
    ledger.append('lap', 'controller', exp, {'lap_id':'authored-smoke-lap', 'parent_lap_id':None,
        'task_id':'geometry_weight_normalize', 'change_reason':'Two hand-authored smoke fixtures; not model evaluation',
        'selection_rule_sha256':L.sha256_bytes(report.SELECTION_RULE.encode()),
        'split_manifest_sha256':manifest_hash,'cases_consulted_for_change':[]}, artifacts=store)
    attempts=[]
    for i,(kind,file) in enumerate(SAMPLES.items()):
        c=samples[i]
        raw=(Path(__file__).resolve().parent / file).read_bytes()
        fx=L.fixture_hash(c)
        cand=store.put('candidates', raw, '.py')
        store.put('fixtures',ingest.fixture_bytes(c),'.json')
        raw_sha=store.put('raw_outputs',raw,'.txt')
        att_id=f'{exp}:authored-smoke-lap:{kind}:{c["case_id"]}:1'
        fields={'attempt_id':att_id,'lap_id':'authored-smoke-lap','trial_id':kind,'attempt_no':1,
          'task_id':'geometry_weight_normalize','stage':'03','case_id':c['case_id'],
          'source_family':c['fixture_family'],'split':'dev','role':'target','fixture_kind':'synthetic',
          'fixture_sha256':fx,'model_digest':'AUTHORED-NOT-A-MODEL',
          'prompt_sha256':L.sha256_bytes(b'fixed authored smoke script, not an LLM'),
          'template_sha256':None,'raw_output_sha256':raw_sha,'candidate_sha256':cand,
          'generation_status':'produced','seed':None,'temperature':0.0,'num_ctx':0,
          'reasoning_mode':'not-applicable','input_tokens':None,'output_tokens':None,
          'inference_seconds':None}
        ledger.append('attempt','orchestrator',exp,fields,artifacts=store)
        attempts.append((kind,att_id))
    probe=bridge.run_probe(image,forbidden_dirs=[base])
    if not probe.verified:
        raise L.LedgerError('Docker/Blender isolation probe failed. No smoke results accepted: '+str(probe.details))
    outcome={}
    for kind,aid in attempts:
        v=bridge.evaluate_attempt(ledger,store,exp,aid,image=image,probe=probe)
        outcome[kind]=v['result']
        print(kind.upper(), v['result'], v.get('reason',''))
    errors=ledger.verify(store)
    if errors:
        raise L.LedgerError('Smoke ledger failed: '+ '; '.join(errors))
    print('Evidence:',base)
    if outcome != {'correct':'pass','wrong':'fail'}:
        raise L.LedgerError('Expected correct=pass AND wrong=fail, observed '+str(outcome))
    print('SMOKE PASSED: true Blender isolation + positive/negative discrimination; NOT model qualification')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--image',required=True,help='Already installed and pinned Blender image name@sha256:64hex')
    p.add_argument('--cases',type=Path,default=ROOT/'astra-qwen-weight-lab'/'data'/'fixtures'/'cases.jsonl')
    a=p.parse_args()
    try:
        run(a.image,a.cases)
        return 0
    except (OSError,ValueError,subprocess.CalledProcessError) as e:
        print('SMOKE STOP:',e,file=sys.stderr)
        return 2

if __name__=='__main__':
    raise SystemExit(main())
