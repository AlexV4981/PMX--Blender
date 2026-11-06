# Model Evaluation Report v2.1: demo-001

_Generated from ledger head `4cfab03479d16e47` (7 events). Measures come only from validated events; narrative text is separately attributed._

## 1. Experiment Summary

| Field | Value |
|---|---|
| Experiment | demo-001 |
| Model digest(s) | AUTHORED-NOT-A-MODE |
| Model tag(s) | authored-demo |
| Task(s) / stage(s) | geometry_weight_normalize / 03 |
| Laps recorded | 1 |
| Attempts recorded | 3 |
| Decoding | T=0.0 ctx=4096 seed=None reasoning=not_recorded |
| Native template hash | NOT RECORDED for 3 attempt(s) |
| Environment (lap-declared) | {"note": "no-docker-no-blender", "os": "linux-container"} |
| Readiness (evidence-derived) | 1 proposal-only |


**Interpretation:** _none authored_

## 2. Performance, Quality and Benchmark Results

Rate = verified passes / ALL first-try attempts in the group (blocked, not_run and no_verdict count against). Repair attempts (attempt_no > 1) are reported separately and never counted as first-try. Rates are exploratory; correlated families make intervals optimistic.

| Lap | Task | Split | Role | First-try pass | Rate | Wilson 95% | Cases | Families | Fail | Not run | Blocked | No verdict | Severe | Repair pass/tries (offline) | p50/p95 verified s | Verified passes/min | Tokens in/out |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lap-00 | geometry_weight_normalize | dev | target | 0/3 | 0% | 0-56% | 3 | 1 | 0 | 0 | 3 | 0 | 0 | 0/0 | not measured | not measured (timing incomplete) | n/m / n/m |


**Exploratory gates:**

- lap-00 / geometry_weight_normalize: exploratory pilot gate (>=20 first-try, >=75% pass, 0 severe): not met (n=3, pass=0, severe=0); cost gate (<=35% of Codex effort): NOT MEASURED, so the gate is INCOMPLETE.

**Real-use gap:** real PMX/VMD and native Blender fixtures evaluated: 0 attempt(s). Unknown is not pass.

**Compromised holdout cases:** none recorded


**Interpretation:** _none authored_

## 3. Lap-by-Lap Failure and Adjustment Analysis

### lap-00 (parent: none)

- Change reason (controller-declared): plumbing demo baseline
- Selection rule hash: `22f2e5f309e7557d`; split manifest hash: `1585ae43f640d125`
- Cases consulted for this change: none
- Target first-try: 0/3 pass; severe regressions: 0

| Attempt | Case | Status | Category | Severity | Evaluator note (not a root-cause analysis; may echo candidate-influenced text) | Evidence |
|---|---|---|---|---|---|---|
| demo-001:lap-00:t1:stage03-synthetic-000:1 | stage03-synthetic-000 | blocked | sandbox | none | evaluator note: sandbox isolation not verified | evidence/b5cd04cd0af61864d523bb47e383875b053c1137570d8db7c3a20fa3c3b88477.json |
| demo-001:lap-00:t1:stage03-synthetic-001:1 | stage03-synthetic-001 | blocked | sandbox | none | evaluator note: sandbox isolation not verified | evidence/b5cd04cd0af61864d523bb47e383875b053c1137570d8db7c3a20fa3c3b88477.json |
| demo-001:lap-00:t1:stage03-synthetic-002:1 | stage03-synthetic-002 | blocked | sandbox | none | evaluator note: sandbox isolation not verified | evidence/b5cd04cd0af61864d523bb47e383875b053c1137570d8db7c3a20fa3c3b88477.json |

Root cause: **unknown** unless attributed narrative below states otherwise.


**Interpretation:** _none authored_

## 4. Specialization Effectiveness

Untuned baseline = a lap with no parent. Comparison uses only cases attempted first-try in both laps. Lap IDs reference Section 2; numbers here are deltas only.

_No rows._

Canary rows are out-of-scope regression checks; absence of canary rows means **not measured**, not no regression.


**Interpretation:** _none authored_

## 5. Workflow Integration, Reliability and Safety

| Item | Observed |
|---|---|
| Verdicts by result | {"blocked": 3} |
| Verdicts with isolation verified | 0 of 3 |
| Evaluator runtime identities | unavailable |
| Attempts with no verdict | 0 |
| Blocked/not_run reasons | {"isolation_unverified": 1} |
| Codex fallback frequency | not measured (no fallback event type in this schema) |
| Recorded decisions | none obtained |

**Evaluator limitations carried by verdicts:**

- candidate_executes_in_oracle_process: candidate code can alter oracle state or write the result file
- fixture_hash_is_host_computed: the oracle does not hash the case file it loads

Hash chain detects casual mutation only; it is not tamper-proof against the operator. A model never supplies result, severity, isolation or approval fields.


**Interpretation:** _none authored_

## 6. Miscellaneous Findings and Future Model Analysis

**Reproducibility manifest (from events):**

| Item | Value |
|---|---|
| Ledger head hash | 4cfab03479d16e475fcb87dd785f441aafb9f25974342243768fe85846471816 |
| Oracle versions | oracle_sha256:290319ec1fb1f9a8a7b17b0fecfed9e3f636a1c60c21c2ba3f446fe884d73697;repo_commit:9ac4ea4ce77d55e0499960a57b2e61182f968895 |
| Selection-rule hashes | 22f2e5f309e7557d |
| Split-manifest hashes | 1585ae43f640d125 |
| Fixture hashes | 3 |
| Candidate hashes | 2 |
| Attempts without raw-output hash | 3 |


**Interpretation:** _none authored_

## 7. Final Verdict

**Readiness:** 1 proposal-only

**Unmet requirements for the next level:**

- a trusted, isolation-verified Blender verdict for at least one attempt

**Capability rows (machine-readable):**

```json
[
  {
    "best_lap_id": null,
    "dev_only_first_try_by_lap": {
      "lap-00": [
        0,
        3
      ]
    },
    "evidence_ref": "4cfab03479d16e475fcb87dd785f441aafb9f25974342243768fe85846471816",
    "first_try_pass_count": null,
    "model_digest": "AUTHORED-NOT-A-MODEL",
    "n": null,
    "readiness": "1 proposal-only",
    "selection_rule": "max validation-split first-try pass rate; ties -> lower mean verified seconds",
    "split_basis": "none",
    "task_id": "geometry_weight_normalize",
    "trusted_scope": "development-only synthetic smoke; not a production scope",
    "uncertainty": null
  }
]
```

**Human decision:** none obtained


**Interpretation:** _none authored_

