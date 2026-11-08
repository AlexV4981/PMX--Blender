# Gemma4 12B Q4_K_M — Stage03 Final Report v2.1

_Generated from ledger head `de162125549140a5` (246 events). Measures come only from validated events; narrative text is separately attributed._

## 1. Experiment Summary

| Field | Value |
|---|---|
| Experiment | gemma4-12b-stage03 |
| Model digest(s) | 6114515d63c17436a7c |
| Model tag(s) | gemma4:12b |
| Task(s) / stage(s) | geometry_weight_normalize / 03 |
| Laps recorded | 6 in synthetic first-attempt ledger; 10 total (4 real trials recorded separately below) |
| Attempts recorded | 120 |
| Decoding | T=0.0 ctx=4096 seed=None reasoning=explicit_think_false_no_thinking_observed; T=0.0 ctx=4096 seed=None reasoning=server_default_observed_thinking |
| Native template hash | recorded |
| Environment (public allowlist) | Blender5.2.2 LTS; Python3.13.5; hardened local runtime. Machine/OS identity withheld. |
| Readiness (evidence-derived) | 2 verified synthetic observations (development-only) |


**Interpretation:** (author: Benchmark operator; sanitized interpretation) Gemma4 12B Q4_K_M, ten sequential Stage03 laps: six synthetic development laps and four repeated real-character trials. No model training or adapter changes. All synthetic first-attempt data derive from a verified ledger; real results are separate status/request/API evidence and never pooled with synthetic counts.

## 2. Performance, Quality and Benchmark Results

Rate = verified passes / ALL first-try attempts in the group (blocked, not_run and no_verdict count against). Repair attempts (attempt_no > 1) are reported separately and never counted as first-try. Rates are exploratory; correlated families make intervals optimistic.

| Lap | Task | Split | Role | First-try pass | Rate | Wilson 95% | Cases | Families | Fail | Not run | Blocked | No verdict | Severe | Repair pass/tries (offline) | p50/p95 model+oracle s | Model+oracle passes/min (not end-to-end) | Tokens in/out |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lap-01 | geometry_weight_normalize | dev | target | 0/20 | 0% | 0-16% | 20 | 5 | 0 | 20 | 0 | 0 | 0 | 0/0 | 94.9 / 98.0 | 0.00 | 6444 / 30720 |
| lap-02 | geometry_weight_normalize | dev | target | 0/20 | 0% | 0-16% | 20 | 5 | 4 | 1 | 15 | 0 | 0 | 0/0 | 42.0 / 72.0 | 0.00 | 6384 / 14659 |
| lap-03 | geometry_weight_normalize | dev | target | 18/20 | 90% | 70-97% | 20 | 5 | 0 | 0 | 2 | 0 | 0 | 0/0 | 30.3 / 43.4 | 1.67 | 15004 / 9582 |
| lap-04 | geometry_weight_normalize | dev | target | 17/20 | 85% | 64-95% | 20 | 5 | 0 | 0 | 3 | 0 | 0 | 0/0 | 41.9 / 53.7 | 1.16 | 21904 / 12484 |
| lap-05 | geometry_weight_normalize | dev | target | 19/20 | 95% | 76-99% | 20 | 5 | 0 | 0 | 1 | 0 | 0 | 0/0 | 45.3 / 69.8 | 1.13 | 23064 / 13773 |
| lap-06 | geometry_weight_normalize | dev | target | 19/20 | 95% | 76-99% | 20 | 5 | 0 | 0 | 1 | 0 | 0 | 0/0 | 45.5 / 64.5 | 1.20 | 23064 / 13773 |


The offline repair column is zero because this table covers the original first-attempt ledger only. Lap06's one separately recorded repair passed; its assisted score is20/20, while the first-try score remains19/20. See repair-analysis.json.

**Exploratory gates:**

- lap-01 / geometry_weight_normalize: exploratory pilot gate (>=20 first-try, >=75% pass, 0 severe): not met (n=20, pass=0, severe=0); cost gate (<=35% of Codex effort): NOT MEASURED, so the gate is INCOMPLETE.
- lap-02 / geometry_weight_normalize: exploratory pilot gate (>=20 first-try, >=75% pass, 0 severe): not met (n=20, pass=0, severe=0); cost gate (<=35% of Codex effort): NOT MEASURED, so the gate is INCOMPLETE.
- lap-03 / geometry_weight_normalize: exploratory pilot gate (>=20 first-try, >=75% pass, 0 severe): numerically met; cost gate (<=35% of Codex effort): NOT MEASURED, so the gate is INCOMPLETE.
- lap-04 / geometry_weight_normalize: exploratory pilot gate (>=20 first-try, >=75% pass, 0 severe): numerically met; cost gate (<=35% of Codex effort): NOT MEASURED, so the gate is INCOMPLETE.
- lap-05 / geometry_weight_normalize: exploratory pilot gate (>=20 first-try, >=75% pass, 0 severe): numerically met; cost gate (<=35% of Codex effort): NOT MEASURED, so the gate is INCOMPLETE.
- lap-06 / geometry_weight_normalize: exploratory pilot gate (>=20 first-try, >=75% pass, 0 severe): numerically met; cost gate (<=35% of Codex effort): NOT MEASURED, so the gate is INCOMPLETE.

**Real-use gap:** This synthetic ledger contains no real attempts. Separately recorded real laps07–10 produced0/4 passes on one character; none reached fresh geometry verification. See real-trial-results.json. Unknown is not pass.

**Consulted/exposed cases (generator legacy label: compromised holdout):** These are reused development cases, not a held-out split.  stage03-synthetic-000 (consulted_for_change in lap-02), stage03-synthetic-001 (consulted_for_change in lap-02), stage03-synthetic-002 (consulted_for_change in lap-02), stage03-synthetic-003 (consulted_for_change in lap-02), stage03-synthetic-004 (consulted_for_change in lap-02), stage03-synthetic-005 (consulted_for_change in lap-02), stage03-synthetic-006 (consulted_for_change in lap-02), stage03-synthetic-007 (consulted_for_change in lap-02), stage03-synthetic-008 (consulted_for_change in lap-02), stage03-synthetic-009 (consulted_for_change in lap-02), stage03-synthetic-010 (consulted_for_change in lap-02), stage03-synthetic-011 (consulted_for_change in lap-02), stage03-synthetic-012 (consulted_for_change in lap-02), stage03-synthetic-013 (consulted_for_change in lap-02), stage03-synthetic-014 (consulted_for_change in lap-02), stage03-synthetic-015 (consulted_for_change in lap-02), stage03-synthetic-016 (consulted_for_change in lap-02), stage03-synthetic-017 (consulted_for_change in lap-02), stage03-synthetic-018 (consulted_for_change in lap-02), stage03-synthetic-019 (consulted_for_change in lap-02)


**Interpretation:** (author: Benchmark operator; sanitized interpretation) Highest observed synthetic first-try result:19/20 (95%) in laps05 and06. Lap06 separately reached20/20 after one syntax-feedback repair. Real trials07–10:0/4 passes on one reused real character; none reached the fresh geometry verifier. Synthetic pilot numerical threshold is met, but cost <=35% of original workflow is unmeasured, no real successful qualification or human artistic gate exists.

## 3. Lap-by-Lap Failure and Adjustment Analysis

### lap-01 (parent: none)

- Change reason (controller-declared): New-model baseline: original Qwen lap-1 prompts and explicit decoding controls; model tag/native template differ; no retries
- Selection rule hash: `22f2e5f309e7557d`; split manifest hash: `a9d9dd7d997f76c8`
- Cases consulted for this change: none
- Target first-try: 0/20 pass; severe regressions: 0

| Attempt | Case | Status | Category | Severity | Evaluator note (not a root-cause analysis; may echo candidate-influenced text) | Evidence |
|---|---|---|---|---|---|---|
| gemma4-12b-stage03:lap-01:t1:stage03-synthetic-000:1 | stage03-synthetic-000 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-01:t1:stage03-synthetic-001:1 | stage03-synthetic-001 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-01:t1:stage03-synthetic-002:1 | stage03-synthetic-002 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-01:t1:stage03-synthetic-003:1 | stage03-synthetic-003 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-01:t1:stage03-synthetic-004:1 | stage03-synthetic-004 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-01:t1:stage03-synthetic-005:1 | stage03-synthetic-005 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-01:t1:stage03-synthetic-006:1 | stage03-synthetic-006 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-01:t1:stage03-synthetic-007:1 | stage03-synthetic-007 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-01:t1:stage03-synthetic-008:1 | stage03-synthetic-008 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-01:t1:stage03-synthetic-009:1 | stage03-synthetic-009 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-01:t1:stage03-synthetic-010:1 | stage03-synthetic-010 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-01:t1:stage03-synthetic-011:1 | stage03-synthetic-011 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-01:t1:stage03-synthetic-012:1 | stage03-synthetic-012 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-01:t1:stage03-synthetic-013:1 | stage03-synthetic-013 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-01:t1:stage03-synthetic-014:1 | stage03-synthetic-014 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-01:t1:stage03-synthetic-015:1 | stage03-synthetic-015 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-01:t1:stage03-synthetic-016:1 | stage03-synthetic-016 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-01:t1:stage03-synthetic-017:1 | stage03-synthetic-017 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-01:t1:stage03-synthetic-018:1 | stage03-synthetic-018 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-01:t1:stage03-synthetic-019:1 | stage03-synthetic-019 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case results](case-results.json) |

Root cause: **unknown** unless attributed narrative below states otherwise.

### lap-02 (parent: lap-01)

- Change reason (controller-declared): Lap 2: set only explicit top-level think=false. Keep all original baseline prompts and other request controls unchanged: temperature0, context4096, output1536, JSON format, stream=false. Lap1 exhausted output budget in native thinking without any final code; this tests direct-answer behavior. No retries, extracted reasoning, candidate repair or weight changes.
- Selection rule hash: `22f2e5f309e7557d`; split manifest hash: `a9d9dd7d997f76c8`
- Cases consulted for this change: stage03-synthetic-000, stage03-synthetic-001, stage03-synthetic-002, stage03-synthetic-003, stage03-synthetic-004, stage03-synthetic-005, stage03-synthetic-006, stage03-synthetic-007, stage03-synthetic-008, stage03-synthetic-009, stage03-synthetic-010, stage03-synthetic-011, stage03-synthetic-012, stage03-synthetic-013, stage03-synthetic-014, stage03-synthetic-015, stage03-synthetic-016, stage03-synthetic-017, stage03-synthetic-018, stage03-synthetic-019
- Target first-try: 0/20 pass; severe regressions: 0

| Attempt | Case | Status | Category | Severity | Evaluator note (not a root-cause analysis; may echo candidate-influenced text) | Evidence |
|---|---|---|---|---|---|---|
| gemma4-12b-stage03:lap-02:t1:stage03-synthetic-000:1 | stage03-synthetic-000 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-02:t1:stage03-synthetic-001:1 | stage03-synthetic-001 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-02:t1:stage03-synthetic-002:1 | stage03-synthetic-002 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-02:t1:stage03-synthetic-003:1 | stage03-synthetic-003 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-02:t1:stage03-synthetic-004:1 | stage03-synthetic-004 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-02:t1:stage03-synthetic-005:1 | stage03-synthetic-005 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-02:t1:stage03-synthetic-006:1 | stage03-synthetic-006 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-02:t1:stage03-synthetic-007:1 | stage03-synthetic-007 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-02:t1:stage03-synthetic-008:1 | stage03-synthetic-008 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-02:t1:stage03-synthetic-009:1 | stage03-synthetic-009 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-02:t1:stage03-synthetic-010:1 | stage03-synthetic-010 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-02:t1:stage03-synthetic-011:1 | stage03-synthetic-011 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-02:t1:stage03-synthetic-012:1 | stage03-synthetic-012 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-02:t1:stage03-synthetic-013:1 | stage03-synthetic-013 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-02:t1:stage03-synthetic-014:1 | stage03-synthetic-014 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-02:t1:stage03-synthetic-015:1 | stage03-synthetic-015 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-02:t1:stage03-synthetic-016:1 | stage03-synthetic-016 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-02:t1:stage03-synthetic-017:1 | stage03-synthetic-017 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-02:t1:stage03-synthetic-018:1 | stage03-synthetic-018 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-02:t1:stage03-synthetic-019:1 | stage03-synthetic-019 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case results](case-results.json) |

Root cause: **unknown** unless attributed narrative below states otherwise.

### lap-03 (parent: lap-02)

- Change reason (controller-declared): Lap 3: append exact original Qwen synthetic lap-3 Blender API reference, including ownership, weight signatures, sparse assignments and live data vs reference tuples. Keep explicit think=false and all lap-2 controls unchanged: temperature0, context4096, output1536, JSON format, stream=false. Prompt guidance only; no retries, candidate repair or weight changes.
- Selection rule hash: `22f2e5f309e7557d`; split manifest hash: `a9d9dd7d997f76c8`
- Cases consulted for this change: stage03-synthetic-000, stage03-synthetic-001, stage03-synthetic-002, stage03-synthetic-003, stage03-synthetic-004, stage03-synthetic-005, stage03-synthetic-006, stage03-synthetic-007, stage03-synthetic-008, stage03-synthetic-009, stage03-synthetic-010, stage03-synthetic-011, stage03-synthetic-012, stage03-synthetic-013, stage03-synthetic-014, stage03-synthetic-015, stage03-synthetic-016, stage03-synthetic-017, stage03-synthetic-018, stage03-synthetic-019
- Target first-try: 18/20 pass; severe regressions: 0

| Attempt | Case | Status | Category | Severity | Evaluator note (not a root-cause analysis; may echo candidate-influenced text) | Evidence |
|---|---|---|---|---|---|---|
| gemma4-12b-stage03:lap-03:t1:stage03-synthetic-007:1 | stage03-synthetic-007 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-03:t1:stage03-synthetic-016:1 | stage03-synthetic-016 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case results](case-results.json) |

Root cause: **unknown** unless attributed narrative below states otherwise.

### lap-04 (parent: lap-03)

- Change reason (controller-declared): Lap 4: append general vertex-group/VertexGroupElement object-versus-tuple and sparse-ID clarification. Targets two observed tuple-unpacking failures without providing a completed solution. Preserve original API appendix and all lap-3 controls: think=false, temperature0, context4096, output1536, JSON, stream=false. No retries, repaired answers, weight changes or sandbox-policy changes.
- Selection rule hash: `22f2e5f309e7557d`; split manifest hash: `a9d9dd7d997f76c8`
- Cases consulted for this change: stage03-synthetic-000, stage03-synthetic-001, stage03-synthetic-002, stage03-synthetic-003, stage03-synthetic-004, stage03-synthetic-005, stage03-synthetic-006, stage03-synthetic-007, stage03-synthetic-008, stage03-synthetic-009, stage03-synthetic-010, stage03-synthetic-011, stage03-synthetic-012, stage03-synthetic-013, stage03-synthetic-014, stage03-synthetic-015, stage03-synthetic-016, stage03-synthetic-017, stage03-synthetic-018, stage03-synthetic-019
- Target first-try: 17/20 pass; severe regressions: 0

| Attempt | Case | Status | Category | Severity | Evaluator note (not a root-cause analysis; may echo candidate-influenced text) | Evidence |
|---|---|---|---|---|---|---|
| gemma4-12b-stage03:lap-04:t1:stage03-synthetic-001:1 | stage03-synthetic-001 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-04:t1:stage03-synthetic-018:1 | stage03-synthetic-018 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case results](case-results.json) |
| gemma4-12b-stage03:lap-04:t1:stage03-synthetic-019:1 | stage03-synthetic-019 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case results](case-results.json) |

Root cause: **unknown** unless attributed narrative below states otherwise.

### lap-05 (parent: lap-04)

- Change reason (controller-declared): Lap 5: append the user-approved exact JSON encoding clarification: encode once, decoded statement separators are actual line breaks, preserve indentation and intentional Python-string escapes. Target prior double-escaped newline syntax failures. All earlier goal/API guidance and controls unchanged: think=false, temperature0, context4096, output1536, JSON string contract, stream=false. No automatic unescaping, candidate repair, retries or weight changes.
- Selection rule hash: `22f2e5f309e7557d`; split manifest hash: `a9d9dd7d997f76c8`
- Cases consulted for this change: stage03-synthetic-000, stage03-synthetic-001, stage03-synthetic-002, stage03-synthetic-003, stage03-synthetic-004, stage03-synthetic-005, stage03-synthetic-006, stage03-synthetic-007, stage03-synthetic-008, stage03-synthetic-009, stage03-synthetic-010, stage03-synthetic-011, stage03-synthetic-012, stage03-synthetic-013, stage03-synthetic-014, stage03-synthetic-015, stage03-synthetic-016, stage03-synthetic-017, stage03-synthetic-018, stage03-synthetic-019
- Target first-try: 19/20 pass; severe regressions: 0

| Attempt | Case | Status | Category | Severity | Evaluator note (not a root-cause analysis; may echo candidate-influenced text) | Evidence |
|---|---|---|---|---|---|---|
| gemma4-12b-stage03:lap-05:t1:stage03-synthetic-000:1 | stage03-synthetic-000 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case results](case-results.json) |

Root cause: **unknown** unless attributed narrative below states otherwise.

### lap-06 (parent: lap-05)

- Change reason (controller-declared): Keep lap05 first-attempt prompts and settings unchanged; allow exactly one syntax-feedback repair for syntactically invalid Python, record repair requests and separate sandbox verdicts without replacing first-attempt scores.
- Selection rule hash: `22f2e5f309e7557d`; split manifest hash: `a9d9dd7d997f76c8`
- Cases consulted for this change: stage03-synthetic-000, stage03-synthetic-001, stage03-synthetic-002, stage03-synthetic-003, stage03-synthetic-004, stage03-synthetic-005, stage03-synthetic-006, stage03-synthetic-007, stage03-synthetic-008, stage03-synthetic-009, stage03-synthetic-010, stage03-synthetic-011, stage03-synthetic-012, stage03-synthetic-013, stage03-synthetic-014, stage03-synthetic-015, stage03-synthetic-016, stage03-synthetic-017, stage03-synthetic-018, stage03-synthetic-019
- Target first-try: 19/20 pass; severe regressions: 0

| Attempt | Case | Status | Category | Severity | Evaluator note (not a root-cause analysis; may echo candidate-influenced text) | Evidence |
|---|---|---|---|---|---|---|
| gemma4-12b-stage03:lap-06:t1:stage03-synthetic-000:1 | stage03-synthetic-000 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case results](case-results.json) |

Root cause: **unknown** unless attributed narrative below states otherwise.


**Interpretation:** (author: Benchmark operator; sanitized interpretation) See the ten-lap chronology in analysis-notes.md and real-trial-results.json. Lap01 and10 exhausted output during thinking. Lap02 exposed API/source/state errors. API guidance improved synthetic performance, but JSON escaping remained. The one repair was generated once and evaluated after an operator separate-ledger numbering defect was corrected without new inference. Real lap07 failed on node-tree enum, laps08/09 on reversed explanation key/value, final lap10 on empty final output after thinking.


### Complete ten-lap chronology (separate scopes)

| Lap | Scope | First try | Additional repair | Wall minutes | Change and outcome |
|---|---|---|---|---|---|
| 01 | Synthetic dev | 0/20 | None | 33.48 | Original frozen baseline; thinking control omitted, native thinking default enabled. All20 responses exhausted the1536-token cap with thinking and empty final response. Budget/configuration failure, not demonstrated Blender runtime failures. |
| 02 | Synthetic dev | 0/20 | None | 17.29 | Only think=false added. Thinking off enabled final answers, but API hallucinations, syntax mistakes, incomplete repairs and one truncated response remained. |
| 03 | Synthetic dev | 18/20 | None | 11.91 | Append the exact original general Blender API appendix used in the initial project benchmark. 18/20; two attempts treated sparse VertexGroupElement objects as unpackable pairs. |
| 04 | Synthetic dev | 17/20 | None | 15.75 | Append general vertex-group ownership, sparse membership and collection clarification. 17/20; three double-escaped newline syntax failures. No tuple-unpacking errors among executable candidates. |
| 05 | Synthetic dev | 19/20 | None | 17.87 | Append JSON encode-once and newline-separator clarification. 19/20; one double-escaped newline remained. |
| 06 | Synthetic dev | 19/20 | 1 repair passed; assisted20/20 | 17.46 | Same first-attempt prompts/settings as lap05; allow one syntax-feedback repair, separately scored. 19/20 first try; the single syntax-feedback repair passed, yielding20/20 assisted. Operator bookkeeping recovery described separately. |
| 07 | Real repeated case | 0/1 | None | 1.58 | First real-character exam: frozen common task and original decoding profile, no retry. Valid JSON/Python reached solve; invalid GeometryNodes enum stopped the builder. No fresh geometry verdict. |
| 08 | Real repeated case | 0/1 | None | 1.84 | Append general Geometry Nodes API guidance only. Explanation prose emitted as a key with literal value explanation. Contract rejected response before execution. |
| 09 | Real repeated case | 0/1 | None | 1.88 | Exact repeat of lap08 prompt and settings. Request and final response text exactly matched lap08; same response-schema failure. |
| 10 | Real repeated case | 0/1 | None | 5.17 | Only enable thinking; retain lap09 prompt and all other controls. Thinking consumed4096 output tokens; empty final response. No candidate or Blender execution. |

## 4. Specialization Effectiveness

Untuned baseline = a lap with no parent. Comparison uses only cases attempted first-try in both laps. Lap IDs reference Section 2; numbers here are deltas only.

| Lap | Task | Role | Split | Baseline | Lap | Abs change | Rel change | Comparable? |
|---|---|---|---|---|---|---|---|---|
| lap-02 | geometry_weight_normalize | target | dev | 0/20 | 0/20 | +0 | +0 pts | yes (frozen matched cases) |
| lap-03 | geometry_weight_normalize | target | dev | 0/20 | 18/20 | +18 | +90 pts | yes (frozen matched cases) |
| lap-04 | geometry_weight_normalize | target | dev | 0/20 | 17/20 | +17 | +85 pts | yes (frozen matched cases) |
| lap-05 | geometry_weight_normalize | target | dev | 0/20 | 19/20 | +19 | +95 pts | yes (frozen matched cases) |
| lap-06 | geometry_weight_normalize | target | dev | 0/20 | 19/20 | +19 | +95 pts | yes (frozen matched cases) |

Canary rows are out-of-scope regression checks; absence of canary rows means **not measured**, not no regression.


**Interpretation:** (author: Benchmark operator; sanitized interpretation) Untuned lap01 is0/20 because default thinking exhausted the smaller cap; it is a budget/configuration baseline, not20 demonstrated Blender failures. With thinking disabled and general API/encoding guidance, later synthetic first tries reached95%. Prompt exposure uses reused dev fixtures, so causal attribution and generalization remain limited. Exact real repeat08/09 produced identical response text. Enabling thinking in10 did not produce a final answer within4096 tokens.

## 5. Workflow Integration, Reliability and Safety

| Item | Observed |
|---|---|
| Verdicts by result | {"blocked": 22, "fail": 4, "not_run": 21, "pass": 73} |
| Verdicts with isolation verified | 120 of 120 |
| Evaluator runtime identities | local-blender-bwrap-v3@sha256:6f9288264bb6fe7eb09e5bff0148e7b728918c79369a292d8a4490e8a361df86 |
| Attempts with no verdict | 0 |
| Blocked/not_run reasons | {"no_candidate": 21, "nonzero_execution_exit": 22} |
| Codex fallback frequency | not measured (no fallback event type in this schema) |
| Recorded decisions | none obtained |

**Evaluator limitations carried by verdicts:**

- fresh-process synthetic oracle; Blender runtime and container isolation not verified in this release
- sandbox cannot prevent an operator who controls the host from replacing trusted evidence

Hash chain detects casual mutation only; it is not tamper-proof against the operator. A model never supplies result, severity, isolation or approval fields.


**Interpretation:** (author: Benchmark operator; sanitized interpretation) Generated code, where reached, executed only in the existing local Blender bubblewrap/systemd/cgroup/seccomp sandbox; not Docker. Original assets remained read-only; reference was unavailable to candidate code. Independent fresh verifier passed19 original synthetic candidates in lap06 and its separate repair. No real trial completed the builder, so no real geometry verifier or render ran. Native startup socket-denial messages in lap07 were not the fatal error. No independent artistic review, human gate or actual Codex fallback event was recorded.

## 6. Miscellaneous Findings and Future Model Analysis

**Reproducibility manifest (from events):**

| Item | Value |
|---|---|
| Ledger head hash | de162125549140a54c88b895ec8a072e26c58ca8da7718483b45f76b3ff8b366 |
| Oracle versions | oracle_sha256:290319ec1fb1f9a8a7b17b0fecfed9e3f636a1c60c21c2ba3f446fe884d73697;repo_commit:d70c1f7c38df697251193594368a13c8dbb14d1d |
| Selection-rule hashes | 22f2e5f309e7557d |
| Split-manifest hashes | a9d9dd7d997f76c8 |
| Fixture hashes | 20 |
| Candidate hashes | 74 |
| Attempts without raw-output hash | 0 |


**Interpretation:** (author: Benchmark operator; sanitized interpretation) Attachments retain ten lap-linked prompts/settings,120 allowlisted first-attempt case rows, one separate repair outcome, four real-trial summaries, repeatability checks and general API-probe proof. Real prompt identifiers are sanitized using the established public placeholders; repair request containing generated source remains private. Raw code/reasoning, contexts, logs, local paths, native Modelfile, original assets and private reference fingerprints are excluded.

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
        0,
        20
      ],
      "lap-02": [
        0,
        20
      ],
      "lap-03": [
        18,
        20
      ],
      "lap-04": [
        17,
        20
      ],
      "lap-05": [
        19,
        20
      ],
      "lap-06": [
        19,
        20
      ]
    },
    "evidence_ref": "de162125549140a54c88b895ec8a072e26c58ca8da7718483b45f76b3ff8b366",
    "first_try_pass_count": null,
    "model_digest": "6114515d63c17436a7c0417d82820ac65ad643e2806c5a3c89cb62846436ed0b",
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


**Interpretation:** (author: Benchmark operator; sanitized interpretation) Ten-lap sequence finished. Experimental synthetic capability only; not qualified for unattended real-character Stage03 repair. Best descriptive synthetic first-try score95%; assisted100%; no real pass. Formal best_lap_id remains null without validation split. No production or artistic acceptance, no new lap authorized by this export. Future experiments would be new, separately labeled work.


Attachments: [analysis notes](analysis-notes.md), [analysis data](analysis-data.json), [repair outcome](repair-analysis.json), [real trials](real-trial-results.json), [prompts](prompts/README.md), [privacy](privacy-and-provenance.md).
