# Microsoft Phi4 14B Q4_K_M — Stage03 Final Report v2.1

_Generated from ledger head `727086d4da4954be` (123 events). Measures come only from validated events; narrative text is separately attributed._

## 1. Experiment Summary

| Field | Value |
|---|---|
| Experiment | phi4-14b-stage03 |
| Model digest(s) | ac896e5b8b34a1f4efa |
| Model tag(s) | phi4:14b |
| Task(s) / stage(s) | geometry_weight_normalize / 03 |
| Laps recorded | 3 in synthetic ledger;10 total including7 real trials recorded separately |
| Attempts recorded | 60 |
| Decoding | T=0.0 ctx=4096 seed=None reasoning=server_default_no_thinking_observed |
| Native template hash | recorded |
| Environment (public allowlist) | Blender5.2.2 LTS; Python3.13.5; hardened local runtime. Machine/OS identity withheld. |
| Readiness (evidence-derived) | 2 verified synthetic observations (development-only) |


**Interpretation:** (author: Benchmark operator; sanitized interpretation) Microsoft Phi4, Ollama phi4:14b,14.7B Q4_K_M. Ten sequential Stage03 laps:3 synthetic development laps and7 real-character trials on one input. Two extra feedback repairs were separate, not additional laps. Model weights unchanged; no training/adapters. Blender5.2.2 LTS/Python3.13.5; hardware identity withheld.

## 2. Performance, Quality and Benchmark Results

Rate = verified passes / ALL first-try attempts in the group (blocked, not_run and no_verdict count against). Repair attempts (attempt_no > 1) are reported separately and never counted as first-try. Rates are exploratory; correlated families make intervals optimistic.

| Lap | Task | Split | Role | First-try pass | Rate | Wilson 95% | Cases | Families | Fail | Not run | Blocked | No verdict | Severe | Repair pass/tries (offline) | p50/p95 model+oracle s | Model+oracle passes/min (not end-to-end) | Tokens in/out |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lap-01 | geometry_weight_normalize | dev | target | 17/20 | 85% | 64-95% | 20 | 5 | 0 | 0 | 3 | 0 | 0 | 0/0 | 75.9 / 79.5 | 0.66 | 5704 / 11914 |
| lap-02 | geometry_weight_normalize | dev | target | 20/20 | 100% | 84-100% | 20 | 5 | 0 | 0 | 0 | 0 | 0 | 0/0 | 66.0 / 71.1 | 0.89 | 15004 / 9968 |
| lap-03 | geometry_weight_normalize | dev | target | 20/20 | 100% | 84-100% | 20 | 5 | 0 | 0 | 0 | 0 | 0 | 0/0 | 66.0 / 70.4 | 0.89 | 15004 / 9968 |


The offline-repair column above covers the synthetic ledger only (no synthetic retries). Two additional real repairs are in repair-analysis.json; neither passed.

**Exploratory gates:**

- lap-01 / geometry_weight_normalize: exploratory pilot gate (>=20 first-try, >=75% pass, 0 severe): numerically met; cost gate (<=35% of Codex effort): NOT MEASURED, so the gate is INCOMPLETE.
- lap-02 / geometry_weight_normalize: exploratory pilot gate (>=20 first-try, >=75% pass, 0 severe): numerically met; cost gate (<=35% of Codex effort): NOT MEASURED, so the gate is INCOMPLETE.
- lap-03 / geometry_weight_normalize: exploratory pilot gate (>=20 first-try, >=75% pass, 0 severe): numerically met; cost gate (<=35% of Codex effort): NOT MEASURED, so the gate is INCOMPLETE.

**Real-use gap:** No real attempts in this synthetic ledger. Separate real evidence records7 first trials (0 passes) and2 unsuccessful feedback repairs on one character; fresh geometry verifier reached in04/09/10. Unknown is not pass.

**Consulted/exposed development cases (legacy generator label: compromised holdout):** These fixtures were development data, not an untouched held-out split.  stage03-synthetic-000 (consulted_for_change in lap-02), stage03-synthetic-001 (consulted_for_change in lap-02), stage03-synthetic-002 (consulted_for_change in lap-02), stage03-synthetic-003 (consulted_for_change in lap-02), stage03-synthetic-004 (consulted_for_change in lap-02), stage03-synthetic-005 (consulted_for_change in lap-02), stage03-synthetic-006 (consulted_for_change in lap-02), stage03-synthetic-007 (consulted_for_change in lap-02), stage03-synthetic-008 (consulted_for_change in lap-02), stage03-synthetic-009 (consulted_for_change in lap-02), stage03-synthetic-010 (consulted_for_change in lap-02), stage03-synthetic-011 (consulted_for_change in lap-02), stage03-synthetic-012 (consulted_for_change in lap-02), stage03-synthetic-013 (consulted_for_change in lap-02), stage03-synthetic-014 (consulted_for_change in lap-02), stage03-synthetic-015 (consulted_for_change in lap-02), stage03-synthetic-016 (consulted_for_change in lap-02), stage03-synthetic-017 (consulted_for_change in lap-02), stage03-synthetic-018 (consulted_for_change in lap-02), stage03-synthetic-019 (consulted_for_change in lap-02)


**Interpretation:** (author: Benchmark operator; sanitized interpretation) Synthetic first tries17/20,20/20,20/20. Exact repeat02/03 produced20 identical answer texts. Real first tries0/7 and extra repairs0/2. Real fresh verifier ran in04,09,10 and rejected them; other first attempts failed runtime before geometry evaluation. No synthetic/real pooling. Numerical75% synthetic pilot bar met; <=35% original-workflow effort gate unmeasured. No real success or artistic qualification.

## 3. Lap-by-Lap Failure and Adjustment Analysis

### lap-01 (parent: none)

- Change reason (controller-declared): New-model baseline: original Qwen lap-1 prompts and explicit decoding controls; model tag/native template differ; no retries
- Selection rule hash: `22f2e5f309e7557d`; split manifest hash: `a9d9dd7d997f76c8`
- Cases consulted for this change: none
- Target first-try: 17/20 pass; severe regressions: 0

| Attempt | Case | Status | Category | Severity | Evaluator note (not a root-cause analysis; may echo candidate-influenced text) | Evidence |
|---|---|---|---|---|---|---|
| phi4-14b-stage03:lap-01:t1:stage03-synthetic-011:1 | stage03-synthetic-011 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public synthetic outcomes](case-results.json) |
| phi4-14b-stage03:lap-01:t1:stage03-synthetic-012:1 | stage03-synthetic-012 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public synthetic outcomes](case-results.json) |
| phi4-14b-stage03:lap-01:t1:stage03-synthetic-018:1 | stage03-synthetic-018 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public synthetic outcomes](case-results.json) |

Root cause: **unknown** unless attributed narrative below states otherwise.

### lap-02 (parent: lap-01)

- Change reason (controller-declared): Append original Qwen lap03 Blender API helper, relabeled for Phi, plus explicit scalar-float weight versus index-sequence clarification for VertexGroup.add. Keep baseline inference controls unchanged; no repair attempts.
- Selection rule hash: `22f2e5f309e7557d`; split manifest hash: `a9d9dd7d997f76c8`
- Cases consulted for this change: stage03-synthetic-000, stage03-synthetic-001, stage03-synthetic-002, stage03-synthetic-003, stage03-synthetic-004, stage03-synthetic-005, stage03-synthetic-006, stage03-synthetic-007, stage03-synthetic-008, stage03-synthetic-009, stage03-synthetic-010, stage03-synthetic-011, stage03-synthetic-012, stage03-synthetic-013, stage03-synthetic-014, stage03-synthetic-015, stage03-synthetic-016, stage03-synthetic-017, stage03-synthetic-018, stage03-synthetic-019
- Target first-try: 20/20 pass; severe regressions: 0

_No rows._

Root cause: **unknown** unless attributed narrative below states otherwise.

### lap-03 (parent: lap-02)

- Change reason (controller-declared): Exact unchanged repeat of lap02 to measure consistency; no prompt, decoding, transport or retry-policy changes.
- Selection rule hash: `22f2e5f309e7557d`; split manifest hash: `a9d9dd7d997f76c8`
- Cases consulted for this change: stage03-synthetic-000, stage03-synthetic-001, stage03-synthetic-002, stage03-synthetic-003, stage03-synthetic-004, stage03-synthetic-005, stage03-synthetic-006, stage03-synthetic-007, stage03-synthetic-008, stage03-synthetic-009, stage03-synthetic-010, stage03-synthetic-011, stage03-synthetic-012, stage03-synthetic-013, stage03-synthetic-014, stage03-synthetic-015, stage03-synthetic-016, stage03-synthetic-017, stage03-synthetic-018, stage03-synthetic-019
- Target first-try: 20/20 pass; severe regressions: 0

_No rows._

Root cause: **unknown** unless attributed narrative below states otherwise.


**Interpretation:** (author: Benchmark operator; sanitized interpretation) Complete ten-lap chronology and all real/repair failures appear below and in analysis attachments. Qwen-derived API appendix plus scalar-weight clarification removed the observed list-weight error in synthetic02. Real failures include no-op semantic selection, BMFace/vertex confusion, invented BMesh operator, protected-source change and wrong count metadata. Lap07 feedback extractor supplied only a generic footer; fixed before08. Specific feedback in08 did not change candidate code.


### Complete ten-lap chronology (separate scopes)

| Lap | Scope | First try | Additional repair | Wall minutes | Change and finding |
|---|---|---|---|---|---|
| 01 | Synthetic dev | 17/20 | None | 26.66 | Original baseline prompts and explicit decoding controls; only model tag differs. 17/20; three candidates passed a list as VertexGroup.add weight, which requires one scalar float. |
| 02 | Synthetic dev | 20/20 | None | 23.64 | Append original Qwen-derived general Blender API helper, relabel heading, add scalar-float weight versus index-sequence clarification. 20/20 first try; no weight-list errors. Full helper and targeted clarification added together, so individual effects cannot be isolated. |
| 03 | Synthetic dev | 20/20 | None | 23.59 | Exact repeat of lap02; no request changes. 20/20; all20 final answer texts identical to02. Consistent observed pair, not universal reproducibility or generalization. |
| 04 | Repeated real case | 0/1 | None | 3.98 | First real exam: frozen common prompt/input/evaluator and original real decoding controls. No extra synthetic appendix or repair. Code ran but fresh snapshot exactly matched input. Material label treated as vertex-group name and early no-op return. |
| 05 | Repeated real case | 0/1 | None | 1.92 | Append general identification guidance: distinguish object/material/group names and inspect measured regions. Runtime failure: BMFace.co while iterating vertex.link_faces; no fresh verifier. |
| 06 | Repeated real case | 0/1 | None | 2.80 | Append general BMesh element, adjacency, coordinate and lifecycle guidance. Runtime failure: nonexistent bmesh.ops.bound_box; no fresh verifier. |
| 07 | Repeated real case | 0/1 | 1 failed repair; feedback limited | 7.05 | Same first request as06; allow one syntax/runtime feedback repair. Feedback extractor defect documented. First/repair both failed on bound_box. Repair received generic Blender script-failed footer, not specific exception: harness limitation. |
| 08 | Repeated real case | 0/1 | 1 failed repair | 7.15 | Same first request; repair helper corrected to send the specific exception instead of generic footer. Specific AttributeError delivered. Repair code hash identical to first attempt; same bound_box runtime failure. |
| 09 | Repeated real case | 0/1 | None | 3.26 | Append brief API-review instruction; native thinking remains off. Repair policy unchanged. Builder completed; verifier rejected protected-object change, reference surfaces and count metadata. Reported125942 removed versus actual0. |
| 10 | Repeated real case | 0/1 | None | 3.53 | Only temperature0 to0.2; prompt and repair policy unchanged. Final speculative sampling trial. Builder completed; snapshot exactly matched input, actual reduction0, reference surfaces still wrong. Different code but no task success. |

## 4. Specialization Effectiveness

Untuned baseline = a lap with no parent. Comparison uses only cases attempted first-try in both laps. Lap IDs reference Section 2; numbers here are deltas only.

| Lap | Task | Role | Split | Baseline | Lap | Abs change | Rel change | Comparable? |
|---|---|---|---|---|---|---|---|---|
| lap-02 | geometry_weight_normalize | target | dev | 17/20 | 20/20 | +3 | +15 pts | yes (frozen matched cases) |
| lap-03 | geometry_weight_normalize | target | dev | 17/20 | 20/20 | +3 | +15 pts | yes (frozen matched cases) |

Canary rows are out-of-scope regression checks; absence of canary rows means **not measured**, not no regression.


**Interpretation:** (author: Benchmark operator; sanitized interpretation) Within-model baseline17/20 (85%) to20/20 (100%) is a15-percentage-point development improvement with unchanged decoding. General API reference and targeted clarification were added together, so their effects are not isolated. Synthetic repeat is stable in this pair. Real brief-review instruction09 yielded runtime completion but incorrect output; temperature0.2 in10 yielded different code and a no-op. No canary or independent held-out success. Native low-thinking mode is unavailable in recorded metadata.

## 5. Workflow Integration, Reliability and Safety

| Item | Observed |
|---|---|
| Verdicts by result | {"blocked": 3, "pass": 57} |
| Verdicts with isolation verified | 60 of 60 |
| Evaluator runtime identities | local-blender-bwrap-v3@sha256:6f9288264bb6fe7eb09e5bff0148e7b728918c79369a292d8a4490e8a361df86 |
| Attempts with no verdict | 0 |
| Blocked/not_run reasons | {"nonzero_execution_exit": 3} |
| Codex fallback frequency | not measured (no fallback event type in this schema) |
| Recorded decisions | none obtained |

**Evaluator limitations carried by verdicts:**

- fresh-process synthetic oracle; Blender runtime and container isolation not verified in this release
- sandbox cannot prevent an operator who controls the host from replacing trusted evidence

Hash chain detects casual mutation only; it is not tamper-proof against the operator. A model never supplies result, severity, isolation or approval fields.


**Interpretation:** (author: Benchmark operator; sanitized interpretation) Existing local Blender bubblewrap/systemd/cgroup/seccomp isolation, not Docker. Candidate never sees reference or credentials; model unloaded before Blender. Real originals/model hashes verified after every trial. Changes in09 were confined to disposable candidate data and rejected by fresh verifier. Independent verifier completion is distinct from builder execution. No artistic/human gate approval or recorded actual fallback event.

## 6. Miscellaneous Findings and Future Model Analysis

**Reproducibility manifest (from events):**

| Item | Value |
|---|---|
| Ledger head hash | 727086d4da4954be2624c4ca4c0fa31d6eaec004d373414f1038c0a916f737b7 |
| Oracle versions | oracle_sha256:290319ec1fb1f9a8a7b17b0fecfed9e3f636a1c60c21c2ba3f446fe884d73697;repo_commit:d70c1f7c38df697251193594368a13c8dbb14d1d |
| Selection-rule hashes | 22f2e5f309e7557d |
| Split-manifest hashes | a9d9dd7d997f76c8 |
| Fixture hashes | 20 |
| Candidate hashes | 20 |
| Attempts without raw-output hash | 0 |


**Interpretation:** (author: Benchmark operator; sanitized interpretation) Attachments preserve ten lap-linked prompts/settings,60 synthetic outcome rows,7 real first-attempt summaries,2 separate repairs, repeatability and extractor-limitation evidence, code/controller/model identities without code content. Exact synthetic prompts public; real identifiers redacted with established placeholders. Repair prompts contain generated source and remain private; public templates describe them. Raw code/reasoning/logs/assets/local paths/private reference fingerprints excluded.

## 7. Final Verdict

**Readiness:** 2 verified synthetic observations (development-only)

**Unmet requirements for the next level:**

- real licensed PMX/VMD and Blender assets not evaluated

**Capability rows (machine-readable):**

```json
[
  {
    "best_lap_id": null,
    "dev_only_first_try_by_lap": {
      "lap-01": [
        17,
        20
      ],
      "lap-02": [
        20,
        20
      ],
      "lap-03": [
        20,
        20
      ]
    },
    "evidence_ref": "727086d4da4954be2624c4ca4c0fa31d6eaec004d373414f1038c0a916f737b7",
    "first_try_pass_count": null,
    "model_digest": "ac896e5b8b34a1f4efa7b14d7520725140d5512484457fab45d2a4ea14c69dba",
    "n": null,
    "readiness": "2 verified synthetic observations (development-only)",
    "selection_rule": "max validation-split first-try pass rate; ties -> lower mean verified seconds",
    "split_basis": "none",
    "task_id": "geometry_weight_normalize",
    "trusted_scope": "development-only synthetic smoke; not a production scope",
    "uncertainty": null
  }
]
```

**Human decision:** none obtained


**Interpretation:** (author: Benchmark operator; sanitized interpretation) Ten-lap evaluation finished. Experimental synthetic capability only; not qualified for unattended real-character Stage03 repair. Descriptive best synthetic20/20 in02/03, formal best_lap_id null without validation split. Real0/7 plus unsuccessful repairs. >=300 independent held-out examples, multiple source families, independent reviewer/human gates and comparable effort baseline absent. No next inference starts automatically.


Attachments: [analysis](analysis-notes.md), [data](analysis-data.json), [real outcomes](real-trial-results.json), [repairs](repair-analysis.json), [prompts](prompts/README.md), [privacy](privacy-and-provenance.md).
