# IBM Granite 4.2 8B Q4_K_M — Stage03 Final Report v2.1

_Generated from ledger head `79c3d9e19ddd2aca` (410 events). Measures come only from validated events; narrative text is separately attributed._

## 1. Experiment Summary

| Field | Value |
|---|---|
| Experiment | granite42-8b-stage03 |
| Model digest(s) | f586c02fdecdf151b65 |
| Model tag(s) | granite4.2:8b |
| Task(s) / stage(s) | geometry_weight_normalize / 03 |
| Laps recorded | 10 |
| Attempts recorded | 200 |
| Decoding | T=0.0 ctx=4096 seed=None reasoning=explicit_think_false_no_thinking_observed; T=0.0 ctx=4096 seed=None reasoning=server_default_no_thinking_observed; T=0.15 ctx=4096 seed=None reasoning=explicit_think_false_no_thinking_observed |
| Native template hash | recorded |
| Environment (lap-declared; public allowlist) | Blender 5.2.2 LTS; Python 3.13.5; local hardened Blender runtime. OS, machine and paths withheld; per-lap controller identities retained in analysis-data.json. |
| Readiness (evidence-derived) | 2 verified synthetic observations (development-only) |


**Interpretation:** (author: Benchmark operator; sanitized public interpretation) Ten sequential synthetic development laps, one model/stage, no training or adapter updates. All measurements below derive from the validated ledger. Dates and redacted environment are documented in analysis-data.json. No real-character trial or qualification is established. Lap1 has incomplete model-response coverage due to an HTTP error plus a harness indexing cascade; do not treat its fourteen locally blocked requests as bad model answers.

## 2. Performance, Quality and Benchmark Results

Rate = verified passes / ALL first-try attempts in the group (blocked, not_run and no_verdict count against). Repair attempts (attempt_no > 1) are reported separately and never counted as first-try. Rates are exploratory; correlated families make intervals optimistic.

| Lap | Task | Split | Role | First-try pass | Rate | Wilson 95% | Cases | Families | Fail | Not run | Blocked | No verdict | Severe | Repair pass/tries (offline) | p50/p95 model+oracle s | Model+oracle passes/min (not end-to-end) | Tokens in/out |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lap-01 | geometry_weight_normalize | dev | target | 0/20 | 0% | 0-16% | 20 | 5 | 0 | 15 | 5 | 0 | 0 | 0/0 | 48.4 / 61.4 | not measured (timing incomplete) | 1508 / 5099 |
| lap-02 | geometry_weight_normalize | dev | target | 0/20 | 0% | 0-16% | 20 | 5 | 0 | 4 | 16 | 0 | 0 | 0/0 | 43.8 / 71.1 | not measured (timing incomplete) | 5421 / 19267 |
| lap-03 | geometry_weight_normalize | dev | target | 12/20 | 60% | 39-78% | 20 | 5 | 0 | 2 | 6 | 0 | 0 | 0/0 | 30.4 / 56.8 | not measured (timing incomplete) | 13197 / 12168 |
| lap-04 | geometry_weight_normalize | dev | target | 14/20 | 70% | 48-85% | 20 | 5 | 1 | 0 | 5 | 0 | 0 | 0/0 | 34.5 / 42.5 | 1.16 | 21864 / 14249 |
| lap-05 | geometry_weight_normalize | dev | target | 13/20 | 65% | 43-82% | 20 | 5 | 1 | 5 | 1 | 0 | 0 | 0/0 | 39.5 / 107.6 | not measured (timing incomplete) | 16504 / 12952 |
| lap-06 | geometry_weight_normalize | dev | target | 11/20 | 55% | 34-74% | 20 | 5 | 7 | 1 | 1 | 0 | 0 | 0/0 | 52.9 / 112.8 | not measured (timing incomplete) | 23469 / 18222 |
| lap-07 | geometry_weight_normalize | dev | target | 5/20 | 25% | 11-47% | 20 | 5 | 9 | 2 | 4 | 0 | 0 | 0/0 | 37.7 / 121.3 | not measured (timing incomplete) | 24685 / 19009 |
| lap-08 | geometry_weight_normalize | dev | target | 13/20 | 65% | 43-82% | 20 | 5 | 3 | 0 | 4 | 0 | 0 | 0/0 | 55.2 / 78.7 | 0.70 | 21864 / 21958 |
| lap-09 | geometry_weight_normalize | dev | target | 4/20 | 20% | 8-42% | 20 | 5 | 2 | 0 | 14 | 0 | 0 | 0/0 | 54.6 / 92.7 | 0.21 | 21864 / 22726 |
| lap-10 | geometry_weight_normalize | dev | target | 11/20 | 55% | 34-74% | 20 | 5 | 1 | 0 | 8 | 0 | 0 | 0/0 | 72.9 / 111.5 | 0.43 | 40064 / 28812 |


**Exploratory gates:**

- lap-01 / geometry_weight_normalize: exploratory pilot gate (>=20 first-try, >=75% pass, 0 severe): not met (n=20, pass=0, severe=0); cost gate (<=35% of Codex effort): NOT MEASURED, so the gate is INCOMPLETE.
- lap-02 / geometry_weight_normalize: exploratory pilot gate (>=20 first-try, >=75% pass, 0 severe): not met (n=20, pass=0, severe=0); cost gate (<=35% of Codex effort): NOT MEASURED, so the gate is INCOMPLETE.
- lap-03 / geometry_weight_normalize: exploratory pilot gate (>=20 first-try, >=75% pass, 0 severe): not met (n=20, pass=12, severe=0); cost gate (<=35% of Codex effort): NOT MEASURED, so the gate is INCOMPLETE.
- lap-04 / geometry_weight_normalize: exploratory pilot gate (>=20 first-try, >=75% pass, 0 severe): not met (n=20, pass=14, severe=0); cost gate (<=35% of Codex effort): NOT MEASURED, so the gate is INCOMPLETE.
- lap-05 / geometry_weight_normalize: exploratory pilot gate (>=20 first-try, >=75% pass, 0 severe): not met (n=20, pass=13, severe=0); cost gate (<=35% of Codex effort): NOT MEASURED, so the gate is INCOMPLETE.
- lap-06 / geometry_weight_normalize: exploratory pilot gate (>=20 first-try, >=75% pass, 0 severe): not met (n=20, pass=11, severe=0); cost gate (<=35% of Codex effort): NOT MEASURED, so the gate is INCOMPLETE.
- lap-07 / geometry_weight_normalize: exploratory pilot gate (>=20 first-try, >=75% pass, 0 severe): not met (n=20, pass=5, severe=0); cost gate (<=35% of Codex effort): NOT MEASURED, so the gate is INCOMPLETE.
- lap-08 / geometry_weight_normalize: exploratory pilot gate (>=20 first-try, >=75% pass, 0 severe): not met (n=20, pass=13, severe=0); cost gate (<=35% of Codex effort): NOT MEASURED, so the gate is INCOMPLETE.
- lap-09 / geometry_weight_normalize: exploratory pilot gate (>=20 first-try, >=75% pass, 0 severe): not met (n=20, pass=4, severe=0); cost gate (<=35% of Codex effort): NOT MEASURED, so the gate is INCOMPLETE.
- lap-10 / geometry_weight_normalize: exploratory pilot gate (>=20 first-try, >=75% pass, 0 severe): not met (n=20, pass=11, severe=0); cost gate (<=35% of Codex effort): NOT MEASURED, so the gate is INCOMPLETE.

**Real-use gap:** real PMX/VMD and native Blender fixtures evaluated: 0 attempt(s). Unknown is not pass.

**Compromised holdout cases:** stage03-synthetic-000 (consulted_for_change in lap-02), stage03-synthetic-001 (consulted_for_change in lap-02), stage03-synthetic-002 (consulted_for_change in lap-02), stage03-synthetic-003 (consulted_for_change in lap-02), stage03-synthetic-004 (consulted_for_change in lap-02), stage03-synthetic-005 (consulted_for_change in lap-02), stage03-synthetic-006 (consulted_for_change in lap-02), stage03-synthetic-007 (consulted_for_change in lap-02), stage03-synthetic-008 (consulted_for_change in lap-02), stage03-synthetic-009 (consulted_for_change in lap-02), stage03-synthetic-010 (consulted_for_change in lap-02), stage03-synthetic-011 (consulted_for_change in lap-02), stage03-synthetic-012 (consulted_for_change in lap-02), stage03-synthetic-013 (consulted_for_change in lap-02), stage03-synthetic-014 (consulted_for_change in lap-02), stage03-synthetic-015 (consulted_for_change in lap-02), stage03-synthetic-016 (consulted_for_change in lap-02), stage03-synthetic-017 (consulted_for_change in lap-02), stage03-synthetic-018 (consulted_for_change in lap-02), stage03-synthetic-019 (consulted_for_change in lap-02)


**Interpretation:** (author: Benchmark operator; sanitized public interpretation) Twenty reused development cases in five correlated families per lap, not two hundred independent fixtures. Highest observed development score is lap4 14/20 (70%); final lap10 is11/20 (55%). No lap meets the75% exploratory pilot threshold, and the <=35% effort gate is unmeasured. Real workflow quality, independent artistic review and human acceptance are not measured. Recorded token usage omits unavailable usage from aborted requests.

## 3. Lap-by-Lap Failure and Adjustment Analysis

### lap-01 (parent: none)

- Change reason (controller-declared): New-model baseline: original Qwen lap-1 prompts and explicit decoding controls; model tag/native template differ; no retries
- Selection rule hash: `22f2e5f309e7557d`; split manifest hash: `a9d9dd7d997f76c8`
- Cases consulted for this change: none
- Target first-try: 0/20 pass; severe regressions: 0

| Attempt | Case | Status | Category | Severity | Evaluator note (not a root-cause analysis; may echo candidate-influenced text) | Evidence |
|---|---|---|---|---|---|---|
| granite42-8b-stage03:lap-01:t1:stage03-synthetic-000:1 | stage03-synthetic-000 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-01:t1:stage03-synthetic-001:1 | stage03-synthetic-001 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-01:t1:stage03-synthetic-002:1 | stage03-synthetic-002 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-01:t1:stage03-synthetic-003:1 | stage03-synthetic-003 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-01:t1:stage03-synthetic-004:1 | stage03-synthetic-004 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-01:t1:stage03-synthetic-005:1 | stage03-synthetic-005 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-01:t1:stage03-synthetic-006:1 | stage03-synthetic-006 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-01:t1:stage03-synthetic-007:1 | stage03-synthetic-007 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-01:t1:stage03-synthetic-008:1 | stage03-synthetic-008 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-01:t1:stage03-synthetic-009:1 | stage03-synthetic-009 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-01:t1:stage03-synthetic-010:1 | stage03-synthetic-010 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-01:t1:stage03-synthetic-011:1 | stage03-synthetic-011 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-01:t1:stage03-synthetic-012:1 | stage03-synthetic-012 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-01:t1:stage03-synthetic-013:1 | stage03-synthetic-013 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-01:t1:stage03-synthetic-014:1 | stage03-synthetic-014 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-01:t1:stage03-synthetic-015:1 | stage03-synthetic-015 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-01:t1:stage03-synthetic-016:1 | stage03-synthetic-016 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-01:t1:stage03-synthetic-017:1 | stage03-synthetic-017 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-01:t1:stage03-synthetic-018:1 | stage03-synthetic-018 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-01:t1:stage03-synthetic-019:1 | stage03-synthetic-019 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |

Root cause: **unknown** unless attributed narrative below states otherwise.

### lap-02 (parent: lap-01)

- Change reason (controller-declared): Lap 2: unchanged Qwen lap-1 baseline prompts and decoding; capture-v2 harness fixes request-index advancement after transport errors and preserves bounded HTTP error bodies; lap 1 incomplete due to HTTP 500 plus capture-index cascade; no retries or sandbox-policy changes.
- Selection rule hash: `22f2e5f309e7557d`; split manifest hash: `a9d9dd7d997f76c8`
- Cases consulted for this change: stage03-synthetic-000, stage03-synthetic-001, stage03-synthetic-002, stage03-synthetic-003, stage03-synthetic-004, stage03-synthetic-005, stage03-synthetic-006, stage03-synthetic-007, stage03-synthetic-008, stage03-synthetic-009, stage03-synthetic-010, stage03-synthetic-011, stage03-synthetic-012, stage03-synthetic-013, stage03-synthetic-014, stage03-synthetic-015, stage03-synthetic-016, stage03-synthetic-017, stage03-synthetic-018, stage03-synthetic-019
- Target first-try: 0/20 pass; severe regressions: 0

| Attempt | Case | Status | Category | Severity | Evaluator note (not a root-cause analysis; may echo candidate-influenced text) | Evidence |
|---|---|---|---|---|---|---|
| granite42-8b-stage03:lap-02:t1:stage03-synthetic-000:1 | stage03-synthetic-000 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-02:t1:stage03-synthetic-001:1 | stage03-synthetic-001 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-02:t1:stage03-synthetic-002:1 | stage03-synthetic-002 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-02:t1:stage03-synthetic-003:1 | stage03-synthetic-003 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-02:t1:stage03-synthetic-004:1 | stage03-synthetic-004 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-02:t1:stage03-synthetic-005:1 | stage03-synthetic-005 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-02:t1:stage03-synthetic-006:1 | stage03-synthetic-006 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-02:t1:stage03-synthetic-007:1 | stage03-synthetic-007 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-02:t1:stage03-synthetic-008:1 | stage03-synthetic-008 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-02:t1:stage03-synthetic-009:1 | stage03-synthetic-009 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-02:t1:stage03-synthetic-010:1 | stage03-synthetic-010 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-02:t1:stage03-synthetic-011:1 | stage03-synthetic-011 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-02:t1:stage03-synthetic-012:1 | stage03-synthetic-012 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-02:t1:stage03-synthetic-013:1 | stage03-synthetic-013 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-02:t1:stage03-synthetic-014:1 | stage03-synthetic-014 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-02:t1:stage03-synthetic-015:1 | stage03-synthetic-015 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-02:t1:stage03-synthetic-016:1 | stage03-synthetic-016 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-02:t1:stage03-synthetic-017:1 | stage03-synthetic-017 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-02:t1:stage03-synthetic-018:1 | stage03-synthetic-018 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-02:t1:stage03-synthetic-019:1 | stage03-synthetic-019 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |

Root cause: **unknown** unless attributed narrative below states otherwise.

### lap-03 (parent: lap-02)

- Change reason (controller-declared): Lap 3: output limit raised from 1536 to 4096 tokens; append exact original Qwen synthetic lap-3 VERIFIED API REFERENCE verbatim. Context remains 4096; all other explicit decoding controls and base prompt unchanged. Two factors change together; no isolated causal attribution. Capture-v2 error bookkeeping retained; trusted controller now reads prepared budgets.
- Selection rule hash: `22f2e5f309e7557d`; split manifest hash: `a9d9dd7d997f76c8`
- Cases consulted for this change: stage03-synthetic-000, stage03-synthetic-001, stage03-synthetic-002, stage03-synthetic-003, stage03-synthetic-004, stage03-synthetic-005, stage03-synthetic-006, stage03-synthetic-007, stage03-synthetic-008, stage03-synthetic-009, stage03-synthetic-010, stage03-synthetic-011, stage03-synthetic-012, stage03-synthetic-013, stage03-synthetic-014, stage03-synthetic-015, stage03-synthetic-016, stage03-synthetic-017, stage03-synthetic-018, stage03-synthetic-019
- Target first-try: 12/20 pass; severe regressions: 0

| Attempt | Case | Status | Category | Severity | Evaluator note (not a root-cause analysis; may echo candidate-influenced text) | Evidence |
|---|---|---|---|---|---|---|
| granite42-8b-stage03:lap-03:t1:stage03-synthetic-001:1 | stage03-synthetic-001 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-03:t1:stage03-synthetic-002:1 | stage03-synthetic-002 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-03:t1:stage03-synthetic-005:1 | stage03-synthetic-005 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-03:t1:stage03-synthetic-007:1 | stage03-synthetic-007 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-03:t1:stage03-synthetic-010:1 | stage03-synthetic-010 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-03:t1:stage03-synthetic-011:1 | stage03-synthetic-011 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-03:t1:stage03-synthetic-015:1 | stage03-synthetic-015 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-03:t1:stage03-synthetic-018:1 | stage03-synthetic-018 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |

Root cause: **unknown** unless attributed narrative below states otherwise.

### lap-04 (parent: lap-03)

- Change reason (controller-declared): Lap 4: append sandbox-verified general vertex-group and typed-collection clarification. Retain temperature 0, context/output 4096/4096 and prior API appendix. Change transport to stream=true with bounded private NDJSON capture to diagnose repetition; completed responses reconstructed without changing text; aborted streams remain errors, never rescued. No weight changes or retries.
- Selection rule hash: `22f2e5f309e7557d`; split manifest hash: `a9d9dd7d997f76c8`
- Cases consulted for this change: stage03-synthetic-000, stage03-synthetic-001, stage03-synthetic-002, stage03-synthetic-003, stage03-synthetic-004, stage03-synthetic-005, stage03-synthetic-006, stage03-synthetic-007, stage03-synthetic-008, stage03-synthetic-009, stage03-synthetic-010, stage03-synthetic-011, stage03-synthetic-012, stage03-synthetic-013, stage03-synthetic-014, stage03-synthetic-015, stage03-synthetic-016, stage03-synthetic-017, stage03-synthetic-018, stage03-synthetic-019
- Target first-try: 14/20 pass; severe regressions: 0

| Attempt | Case | Status | Category | Severity | Evaluator note (not a root-cause analysis; may echo candidate-influenced text) | Evidence |
|---|---|---|---|---|---|---|
| granite42-8b-stage03:lap-04:t1:stage03-synthetic-001:1 | stage03-synthetic-001 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-04:t1:stage03-synthetic-004:1 | stage03-synthetic-004 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-04:t1:stage03-synthetic-005:1 | stage03-synthetic-005 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-04:t1:stage03-synthetic-009:1 | stage03-synthetic-009 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-04:t1:stage03-synthetic-013:1 | stage03-synthetic-013 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-04:t1:stage03-synthetic-019:1 | stage03-synthetic-019 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |

Root cause: **unknown** unless attributed narrative below states otherwise.

### lap-05 (parent: lap-04)

- Change reason (controller-declared): Lap 5 preparation: one semantically equivalent goal-sentence permutation only. Preserve all API guidance, temperature 0, context/output 4096/4096, stream=true and no-retry rule. Preparation alone did not start inference; a subsequent user instruction authorized launch.
- Selection rule hash: `22f2e5f309e7557d`; split manifest hash: `a9d9dd7d997f76c8`
- Cases consulted for this change: stage03-synthetic-000, stage03-synthetic-001, stage03-synthetic-002, stage03-synthetic-003, stage03-synthetic-004, stage03-synthetic-005, stage03-synthetic-006, stage03-synthetic-007, stage03-synthetic-008, stage03-synthetic-009, stage03-synthetic-010, stage03-synthetic-011, stage03-synthetic-012, stage03-synthetic-013, stage03-synthetic-014, stage03-synthetic-015, stage03-synthetic-016, stage03-synthetic-017, stage03-synthetic-018, stage03-synthetic-019
- Target first-try: 13/20 pass; severe regressions: 0

| Attempt | Case | Status | Category | Severity | Evaluator note (not a root-cause analysis; may echo candidate-influenced text) | Evidence |
|---|---|---|---|---|---|---|
| granite42-8b-stage03:lap-05:t1:stage03-synthetic-000:1 | stage03-synthetic-000 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-05:t1:stage03-synthetic-001:1 | stage03-synthetic-001 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-05:t1:stage03-synthetic-003:1 | stage03-synthetic-003 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-05:t1:stage03-synthetic-005:1 | stage03-synthetic-005 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-05:t1:stage03-synthetic-006:1 | stage03-synthetic-006 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-05:t1:stage03-synthetic-013:1 | stage03-synthetic-013 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-05:t1:stage03-synthetic-016:1 | stage03-synthetic-016 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |

Root cause: **unknown** unless attributed narrative below states otherwise.

### lap-06 (parent: lap-05)

- Change reason (controller-declared): Lap 6: targeted output-completion clarification for observed code-string quotation boundary followed by whitespace repetition. Do not quote/restating instructions inside comments; complete JSON fields and outer object. All existing goal/API text and decoding/stream controls unchanged. No model-weight edits, retries, partial-answer rescue or guard disabling; live streams inspected for recurrence.
- Selection rule hash: `22f2e5f309e7557d`; split manifest hash: `a9d9dd7d997f76c8`
- Cases consulted for this change: stage03-synthetic-000, stage03-synthetic-001, stage03-synthetic-002, stage03-synthetic-003, stage03-synthetic-004, stage03-synthetic-005, stage03-synthetic-006, stage03-synthetic-007, stage03-synthetic-008, stage03-synthetic-009, stage03-synthetic-010, stage03-synthetic-011, stage03-synthetic-012, stage03-synthetic-013, stage03-synthetic-014, stage03-synthetic-015, stage03-synthetic-016, stage03-synthetic-017, stage03-synthetic-018, stage03-synthetic-019
- Target first-try: 11/20 pass; severe regressions: 0

| Attempt | Case | Status | Category | Severity | Evaluator note (not a root-cause analysis; may echo candidate-influenced text) | Evidence |
|---|---|---|---|---|---|---|
| granite42-8b-stage03:lap-06:t1:stage03-synthetic-003:1 | stage03-synthetic-003 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-06:t1:stage03-synthetic-005:1 | stage03-synthetic-005 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-06:t1:stage03-synthetic-007:1 | stage03-synthetic-007 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-06:t1:stage03-synthetic-008:1 | stage03-synthetic-008 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-06:t1:stage03-synthetic-012:1 | stage03-synthetic-012 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-06:t1:stage03-synthetic-013:1 | stage03-synthetic-013 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-06:t1:stage03-synthetic-016:1 | stage03-synthetic-016 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-06:t1:stage03-synthetic-017:1 | stage03-synthetic-017 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-06:t1:stage03-synthetic-019:1 | stage03-synthetic-019 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |

Root cause: **unknown** unless attributed narrative below states otherwise.

### lap-07 (parent: lap-06)

- Change reason (controller-declared): Lap 7: prompt-level loop intervention requiring comment-free executable implementation, with description only in explanation and no planning/instruction quotations. Targets repeated quoted-comment JSON boundary and unfinished outlines. All prior prompt text, model weights, temperature 0, context/output 4096/4096, JSON format, streaming, repetition guard and no-retry rule unchanged. No claim of a proven fix.
- Selection rule hash: `22f2e5f309e7557d`; split manifest hash: `a9d9dd7d997f76c8`
- Cases consulted for this change: stage03-synthetic-000, stage03-synthetic-001, stage03-synthetic-002, stage03-synthetic-003, stage03-synthetic-004, stage03-synthetic-005, stage03-synthetic-006, stage03-synthetic-007, stage03-synthetic-008, stage03-synthetic-009, stage03-synthetic-010, stage03-synthetic-011, stage03-synthetic-012, stage03-synthetic-013, stage03-synthetic-014, stage03-synthetic-015, stage03-synthetic-016, stage03-synthetic-017, stage03-synthetic-018, stage03-synthetic-019
- Target first-try: 5/20 pass; severe regressions: 0

| Attempt | Case | Status | Category | Severity | Evaluator note (not a root-cause analysis; may echo candidate-influenced text) | Evidence |
|---|---|---|---|---|---|---|
| granite42-8b-stage03:lap-07:t1:stage03-synthetic-000:1 | stage03-synthetic-000 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-07:t1:stage03-synthetic-002:1 | stage03-synthetic-002 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-07:t1:stage03-synthetic-003:1 | stage03-synthetic-003 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-07:t1:stage03-synthetic-005:1 | stage03-synthetic-005 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-07:t1:stage03-synthetic-006:1 | stage03-synthetic-006 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-07:t1:stage03-synthetic-007:1 | stage03-synthetic-007 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-07:t1:stage03-synthetic-009:1 | stage03-synthetic-009 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-07:t1:stage03-synthetic-010:1 | stage03-synthetic-010 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-07:t1:stage03-synthetic-011:1 | stage03-synthetic-011 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-07:t1:stage03-synthetic-012:1 | stage03-synthetic-012 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-07:t1:stage03-synthetic-013:1 | stage03-synthetic-013 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-07:t1:stage03-synthetic-014:1 | stage03-synthetic-014 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-07:t1:stage03-synthetic-015:1 | stage03-synthetic-015 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-07:t1:stage03-synthetic-016:1 | stage03-synthetic-016 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-07:t1:stage03-synthetic-018:1 | stage03-synthetic-018 | not_run | invalid_output | none | evaluator note: model produced no usable candidate code | [public case verdicts](case-results.json) |

Root cause: **unknown** unless attributed narrative below states otherwise.

### lap-08 (parent: lap-07)

- Change reason (controller-declared): Lap 8: restore best synthetic lap-4 prompt verbatim, remove lap-5 goal permutation and lap-6/7 completion restrictions; add explicit top-level think=false. All twenty requests must equal lap 4 except this flag. Compare against lap 4, not as a single-factor delta from lap 7. Retain temperature 0, context/output 4096/4096, JSON format and streaming; no weight edits, retries or guard changes.
- Selection rule hash: `22f2e5f309e7557d`; split manifest hash: `a9d9dd7d997f76c8`
- Cases consulted for this change: stage03-synthetic-000, stage03-synthetic-001, stage03-synthetic-002, stage03-synthetic-003, stage03-synthetic-004, stage03-synthetic-005, stage03-synthetic-006, stage03-synthetic-007, stage03-synthetic-008, stage03-synthetic-009, stage03-synthetic-010, stage03-synthetic-011, stage03-synthetic-012, stage03-synthetic-013, stage03-synthetic-014, stage03-synthetic-015, stage03-synthetic-016, stage03-synthetic-017, stage03-synthetic-018, stage03-synthetic-019
- Target first-try: 13/20 pass; severe regressions: 0

| Attempt | Case | Status | Category | Severity | Evaluator note (not a root-cause analysis; may echo candidate-influenced text) | Evidence |
|---|---|---|---|---|---|---|
| granite42-8b-stage03:lap-08:t1:stage03-synthetic-000:1 | stage03-synthetic-000 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-08:t1:stage03-synthetic-001:1 | stage03-synthetic-001 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-08:t1:stage03-synthetic-002:1 | stage03-synthetic-002 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-08:t1:stage03-synthetic-013:1 | stage03-synthetic-013 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-08:t1:stage03-synthetic-015:1 | stage03-synthetic-015 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-08:t1:stage03-synthetic-016:1 | stage03-synthetic-016 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-08:t1:stage03-synthetic-019:1 | stage03-synthetic-019 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |

Root cause: **unknown** unless attributed narrative below states otherwise.

### lap-09 (parent: lap-08)

- Change reason (controller-declared): Lap 9: sampling-only experiment, temperature 0 to 0.15 and explicit repeat_penalty 1.20. Exact lap-8 prompt, explicit think=false, JSON format, stream=true and context/output 4096/4096 retained. Both sampling controls change together; no isolated attribution to either. No model-weight changes, retries, guard disabling or answer repair.
- Selection rule hash: `22f2e5f309e7557d`; split manifest hash: `a9d9dd7d997f76c8`
- Cases consulted for this change: stage03-synthetic-000, stage03-synthetic-001, stage03-synthetic-002, stage03-synthetic-003, stage03-synthetic-004, stage03-synthetic-005, stage03-synthetic-006, stage03-synthetic-007, stage03-synthetic-008, stage03-synthetic-009, stage03-synthetic-010, stage03-synthetic-011, stage03-synthetic-012, stage03-synthetic-013, stage03-synthetic-014, stage03-synthetic-015, stage03-synthetic-016, stage03-synthetic-017, stage03-synthetic-018, stage03-synthetic-019
- Target first-try: 4/20 pass; severe regressions: 0

| Attempt | Case | Status | Category | Severity | Evaluator note (not a root-cause analysis; may echo candidate-influenced text) | Evidence |
|---|---|---|---|---|---|---|
| granite42-8b-stage03:lap-09:t1:stage03-synthetic-000:1 | stage03-synthetic-000 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-09:t1:stage03-synthetic-001:1 | stage03-synthetic-001 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-09:t1:stage03-synthetic-002:1 | stage03-synthetic-002 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-09:t1:stage03-synthetic-004:1 | stage03-synthetic-004 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-09:t1:stage03-synthetic-005:1 | stage03-synthetic-005 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-09:t1:stage03-synthetic-007:1 | stage03-synthetic-007 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-09:t1:stage03-synthetic-008:1 | stage03-synthetic-008 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-09:t1:stage03-synthetic-009:1 | stage03-synthetic-009 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-09:t1:stage03-synthetic-010:1 | stage03-synthetic-010 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-09:t1:stage03-synthetic-011:1 | stage03-synthetic-011 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-09:t1:stage03-synthetic-012:1 | stage03-synthetic-012 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-09:t1:stage03-synthetic-013:1 | stage03-synthetic-013 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-09:t1:stage03-synthetic-015:1 | stage03-synthetic-015 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-09:t1:stage03-synthetic-016:1 | stage03-synthetic-016 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-09:t1:stage03-synthetic-017:1 | stage03-synthetic-017 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-09:t1:stage03-synthetic-018:1 | stage03-synthetic-018 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |

Root cause: **unknown** unless attributed narrative below states otherwise.

### lap-10 (parent: lap-09)

- Change reason (controller-declared): Final lap 10: append general Blender/Python API reference sheet covering observed ownership, typed arguments, integer IDs vs objects, sparse collection membership, general unit-sum formulas, independent component storage and valid Python/JSON conventions. General sheet verified with installed-Blender sandbox probe; no completed task solution. Retain exact lap-9 prompt otherwise, temperature 0.15, repeat_penalty 1.20, think=false, context/output 4096/4096, JSON and streaming. Prompt-only comparison; no retries, weight edits, answer repair or sandbox-policy change. Final authorized lap; no lap 11.
- Selection rule hash: `22f2e5f309e7557d`; split manifest hash: `a9d9dd7d997f76c8`
- Cases consulted for this change: stage03-synthetic-000, stage03-synthetic-001, stage03-synthetic-002, stage03-synthetic-003, stage03-synthetic-004, stage03-synthetic-005, stage03-synthetic-006, stage03-synthetic-007, stage03-synthetic-008, stage03-synthetic-009, stage03-synthetic-010, stage03-synthetic-011, stage03-synthetic-012, stage03-synthetic-013, stage03-synthetic-014, stage03-synthetic-015, stage03-synthetic-016, stage03-synthetic-017, stage03-synthetic-018, stage03-synthetic-019
- Target first-try: 11/20 pass; severe regressions: 0

| Attempt | Case | Status | Category | Severity | Evaluator note (not a root-cause analysis; may echo candidate-influenced text) | Evidence |
|---|---|---|---|---|---|---|
| granite42-8b-stage03:lap-10:t1:stage03-synthetic-003:1 | stage03-synthetic-003 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-10:t1:stage03-synthetic-006:1 | stage03-synthetic-006 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-10:t1:stage03-synthetic-007:1 | stage03-synthetic-007 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-10:t1:stage03-synthetic-010:1 | stage03-synthetic-010 | fail | deformation | major | evaluator note: Deform weights not normalized at vertex 0 | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-10:t1:stage03-synthetic-011:1 | stage03-synthetic-011 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-10:t1:stage03-synthetic-012:1 | stage03-synthetic-012 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-10:t1:stage03-synthetic-013:1 | stage03-synthetic-013 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-10:t1:stage03-synthetic-014:1 | stage03-synthetic-014 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |
| granite42-8b-stage03:lap-10:t1:stage03-synthetic-018:1 | stage03-synthetic-018 | blocked | evaluator | none | evaluator note: candidate or fresh verifier exited nonzero (builder=1 verifier=None) | [public case verdicts](case-results.json) |

Root cause: **unknown** unless attributed narrative below states otherwise.


**Interpretation:** (author: Benchmark operator; sanitized public interpretation) Operator-confirmed diagnostics and per-lap interpretations are in analysis-notes.md; public allowlisted verdicts are in case-results.json. The request-index cascade in lap1 was fixed before lap2 without retrying or overwriting the old lap. Later JSON whitespace aborts were localized with streamed capture. Evaluator category blocked is preserved; an observed candidate API error is not silently reclassified in the ledger. Every prompt and explicit request setting is archived per lap.

## 4. Specialization Effectiveness

Untuned baseline = a lap with no parent. Comparison uses only cases attempted first-try in both laps. Lap IDs reference Section 2; numbers here are deltas only.

| Lap | Task | Role | Split | Baseline | Lap | Abs change | Rel change | Comparable? |
|---|---|---|---|---|---|---|---|---|
| lap-02 | geometry_weight_normalize | target | dev | 0/20 | 0/20 | +0 | +0 pts | yes (frozen matched cases) |
| lap-03 | geometry_weight_normalize | target | dev | 0/20 | 12/20 | +12 | +60 pts | yes (frozen matched cases) |
| lap-04 | geometry_weight_normalize | target | dev | 0/20 | 14/20 | +14 | +70 pts | yes (frozen matched cases) |
| lap-05 | geometry_weight_normalize | target | dev | 0/20 | 13/20 | +13 | +65 pts | yes (frozen matched cases) |
| lap-06 | geometry_weight_normalize | target | dev | 0/20 | 11/20 | +11 | +55 pts | yes (frozen matched cases) |
| lap-07 | geometry_weight_normalize | target | dev | 0/20 | 5/20 | +5 | +25 pts | yes (frozen matched cases) |
| lap-08 | geometry_weight_normalize | target | dev | 0/20 | 13/20 | +13 | +65 pts | yes (frozen matched cases) |
| lap-09 | geometry_weight_normalize | target | dev | 0/20 | 4/20 | +4 | +20 pts | yes (frozen matched cases) |
| lap-10 | geometry_weight_normalize | target | dev | 0/20 | 11/20 | +11 | +55 pts | yes (frozen matched cases) |

Canary rows are out-of-scope regression checks; absence of canary rows means **not measured**, not no regression.


**Interpretation:** (author: Benchmark operator; sanitized public interpretation) The untouched baseline is lap1, but its harness failure makes the nominal zero-to-later-pass improvement an incomplete measure of model specialization. Use matched development cases and the comparison-specific controls documented in analysis-data.json. Lap8 restores lap4 prompts and adds only explicit think=false relative to lap4. Lap9 changes two sampling controls together. No canary or real held-out results exist. The descriptive highest development result is not a formally selected validation winner.

## 5. Workflow Integration, Reliability and Safety

| Item | Observed |
|---|---|
| Verdicts by result | {"blocked": 64, "fail": 24, "not_run": 29, "pass": 83} |
| Verdicts with isolation verified | 200 of 200 |
| Evaluator runtime identities | local-blender-bwrap-v3@sha256:6f9288264bb6fe7eb09e5bff0148e7b728918c79369a292d8a4490e8a361df86 |
| Attempts with no verdict | 0 |
| Blocked/not_run reasons | {"no_candidate": 29, "nonzero_execution_exit": 64} |
| Codex fallback frequency | not measured (no fallback event type in this schema) |
| Recorded decisions | none obtained |

**Evaluator limitations carried by verdicts:**

- fresh-process synthetic oracle; Blender runtime and container isolation not verified in this release
- sandbox cannot prevent an operator who controls the host from replacing trusted evidence

Hash chain detects casual mutation only; it is not tamper-proof against the operator. A model never supplies result, severity, isolation or approval fields.


**Interpretation:** (author: Benchmark operator; sanitized public interpretation) Candidate execution used installed Blender5.2.2 LTS with the existing no-network bubblewrap/systemd/cgroup/seccomp controls, not a Blender Docker image. Legacy evaluator boilerplate about container verification is retained below; run-specific local preflight receipts and isolation flags are distinct. A shared probe flag is not proof that each candidate executed. Failed/partial replies were never repaired or rescued. Actual independent domain checks followed successful builders. No real review, human gate or Codex fallback event was recorded.

## 6. Miscellaneous Findings and Future Model Analysis

**Reproducibility manifest (from events):**

| Item | Value |
|---|---|
| Ledger head hash | 79c3d9e19ddd2aca6bba23b8bd705ec156100d2ade6e176ab5bf9dde30bbaab7 |
| Oracle versions | oracle_sha256:290319ec1fb1f9a8a7b17b0fecfed9e3f636a1c60c21c2ba3f446fe884d73697;repo_commit:d70c1f7c38df697251193594368a13c8dbb14d1d |
| Selection-rule hashes | 22f2e5f309e7557d |
| Split-manifest hashes | a9d9dd7d997f76c8 |
| Fixture hashes | 20 |
| Candidate hashes | 161 |
| Attempts without raw-output hash | 27 |


**Interpretation:** (author: Benchmark operator; sanitized public interpretation) Additional attachments retain model/template/controller identities, exact synthetic prompts and request settings, all200 public case metrics, capture coverage, loop-boundary counts, and general API-reference verification summaries. Private paths, hardware identity, raw code/reasoning, continuation-token arrays, logs, native Modelfile and assets are excluded. Model files were unchanged before/after all laps. Output degeneration does not identify an individual faulty neural weight; proposed template/grammar/sampling causes remain hypotheses.

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
        12,
        20
      ],
      "lap-04": [
        14,
        20
      ],
      "lap-05": [
        13,
        20
      ],
      "lap-06": [
        11,
        20
      ],
      "lap-07": [
        5,
        20
      ],
      "lap-08": [
        13,
        20
      ],
      "lap-09": [
        4,
        20
      ],
      "lap-10": [
        11,
        20
      ]
    },
    "evidence_ref": "79c3d9e19ddd2aca6bba23b8bd705ec156100d2ade6e176ab5bf9dde30bbaab7",
    "first_try_pass_count": null,
    "model_digest": "f586c02fdecdf151b656207c339aa003997345774a41768bac1fd6d2fb85913b",
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


**Interpretation:** (author: Benchmark operator; sanitized public interpretation) Final outcome: experimental verified synthetic observations only, not qualified for unattended real-character Stage03 repair. All ten authorized laps are finished. Highest development score70%, final55%; no real independent cases and no validation selection. Human stage approval was not obtained. No further inference starts automatically. Standard thresholds and unmeasured requirements are preserved.


Public attachments: [README](README.md), [analysis notes](analysis-notes.md), [analysis data](analysis-data.json), [case verdicts](case-results.json), [loop observations](loop-observations.json), [prompts](prompts/README.md), [privacy/provenance](privacy-and-provenance.md).
