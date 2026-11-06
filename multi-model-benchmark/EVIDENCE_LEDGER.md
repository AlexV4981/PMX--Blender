# Evidence ledger, evaluator bridge and report generator

Source of truth for every quantitative claim is `data/<name>/ledger.jsonl` (ignored by git). The Markdown report is generated from it and never edited by hand for numbers.

Run from `multi-model-benchmark/` on branch `Multi-Model-PMX-Benchmark`:

```
python3 -m evidence.cli lap      --data NAME --experiment E --lap-id lap-00 --task TASK --reason "..." --split-manifest FILE
python3 -m evidence.cli ingest   --data NAME --experiment E --lap-id lap-00 --trial-id t1 --runner-jsonl R --cases C
python3 -m evidence.cli probe    --data NAME --image blender@sha256:<local digest>     # sandbox isolation probe
python3 -m evidence.cli evaluate --data NAME --experiment E --image blender@sha256:<local digest>
python3 -m evidence.cli verify   --data NAME
python3 -m evidence.cli report   --data NAME --experiment E --out report.md --capability-out cap.json
python3 -m unittest discover -s tests -p "test_*.py"
```

## Events

| Event | Only appended by | Carries |
|---|---|---|
| `lap` | `controller` | parent lap, change reason, frozen selection-rule hash, split-manifest hash, cases consulted for the change, optional environment |
| `attempt` | `orchestrator` | exact model digest, prompt/template/raw-output/candidate hashes, fixture hash, case/family/split/role, decoding, tokens, inference seconds |
| `verdict` | `trusted_evaluator` | hashes as executed, oracle version, runtime identity, result, failure category, severity, evidence hash, isolation flag, evaluator limitations |
| `decision` | `reviewer` | decision kind, outcome, reviewer id, hash of a stored review artifact |

Every event also has `schema_version`, `event_id`, `event_type`, `experiment_id`, `created_at_utc`, `producer`, `previous_event_hash`, `event_hash`. The hash is SHA-256 of canonical JSON (sorted keys, compact separators, UTF-8, no NaN) with `event_hash` excluded.

Identity: `task_id` (stable slug), `stage` (nullable), `case_id`, `source_family`, `split` (`dev`/`validation`/`holdout`), `lap_id`, `trial_id`, `attempt_no`, `attempt_id`. A new seed or fresh evaluation is a new `trial_id`; a feedback repair inside a trial increments `attempt_no`. `first_try` is derived (`attempt_no == 1`); a stored `first_try` is rejected.

Result vocabulary: `pass`, `fail`, `not_run`, `not_applicable`, `blocked`. Failure categories: `none`, `invalid_output`, `blender_api`, `rig_space`, `deformation`, `morph`, `retarget`, `timeout`, `resource`, `sandbox`, `integrity`, `evaluator`, `unsupported`. Severity: `none`, `minor`, `major`, `critical`.

Definitions used by code:
- **First-try verified success:** attempt 1 of a trial whose exact candidate bytes were executed by the trusted evaluator in a probe-verified sandbox and judged `pass`, with a verdict whose candidate and fixture hashes equal the attempt's.
- **Severe regression:** a verdict with severity `critical`, which the bridge assigns only when the oracle's reason matches a protected invariant (source geometry/MASK/shape keys, armature rest data, shape-key topology, neutral restoration, pole creation). Rubric id `pmx-synth-v1`. This is a coarse text match on the oracle's reason, not a deformation measurement.
- **Rate denominator:** all first-try attempts in the group. `blocked`, `not_run` and missing verdicts count against, never as pass.

## What the code refuses

Appends are refused when the ledger is already invalid. Rejected: missing fields, unknown fields, wrong producer for the event type, model-supplied `result`/`severity`/`blender_*`/`first_try`/`human_approved`/`sol_light_reviewed`/`qualified`, duplicate `event_id` or `attempt_id`, non-monotonic `attempt_no`, conflicting case or task identity, orphan verdicts, verdict hashes that differ from the attempt, a second verdict without `reevaluation_of`, a `pass` without evidence and verified isolation, and decisions whose review artifact is missing or hash-mismatched. The report generator raises `ReportBlocked` on any violation. A holdout case is marked compromised if a lap listed it as consulted or it ran without final-eval authorization.

## Hardening v2 — read first

See [HARDENING_v2_README.md](HARDENING_v2_README.md) for the complete patch, usage examples, tests and limitations. The prior version's single-process legacy oracle vulnerability is now addressed in the **bridge architecture** by running the untrusted candidate and the independent validator in **separate Blender containers** with disjoint output mounts. The trusted validator opens derivative .blend files with `--disable-autoexec` and `use_scripts=False`. This behavior remains untested in a real Blender runtime.

- A pass requires both phase exit codes zero, fresh verifier receipt, matching candidate/fixture/oracle hashes, and a verified sandbox probe. A candidate-written result or original single-process oracle output alone is not accepted.
- Source-family split manifest is frozen and content addressed; holdout evaluation requires the `--final` flow and a final-eval child lap of an already validation-tested lap.
- The 20-case pilot is development-only. Production readiness **cannot** be inferred from 300 repeats of one case or pooled outputs from different model digests. In fact, the 35% cost gate is not yet independently recorded, so this version will never auto-certify production readiness.
- A real reviewer must provide an actual review artifact via `python -m evidence.cli decision`; role names and hash chains alone are not cryptographic signatures or reviewer authentication.
- Docker, Blender, Ollama, PMX/VMD and animation packs have **not** been executed/verified in this patch environment. Offline regression tests are simulations of the two container commands, not runtime security proof.
- Native Windows Python uses a `msvcrt` file lock fallback, but this path still needs testing. WSL2/Linux is the recommended first evaluation environment.
