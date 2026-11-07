# Ministral 3 8B — final Stage03 benchmark report

**Canonical alignment:** [MODEL_REPORT_STANDARD.md](../../MODEL_REPORT_STANDARD.md), version 1 (2026-11-05). Operator-authored, sanitized public evidence report. The report describes one model only, not a cross-model ranking. **Observed**, **inferred**, and **not measured** are distinguished; no new tests were run to update report formatting.

## 1. Experiment summary

| Field | Value / evidence status |
|---|---|
| Experiment ID / date | `Stage03-ministral-3-8b-Q4_K_M`; published **2026-11-07**, individual run dates **not publicly recorded** |
| Family / exact Ollama tag / pinned digest | Ministral 3, `ministral-3:8b`, `1922accd5827ebe6829e536369195db25eaf664528dc66206d646ea3bb386b71` |
| Parameter count / quantization | **8,918,026,240**, GGUF Q4_K_M |
| Source base / adapter / checkpoint | Pinned model digest; base upstream revision **not recorded**; **no weight fine-tuning claimed**; real source checkpoint held privately |
| Stage / objective | **03 geometry**; synthesize valid deform-weight normalization code; separate real repair of hair self-shadow preserving protected data |
| Inference/training approach | Local Ollama inference with prompt/decoder specialization and existing Blender verifier; **no trained adapter** |
| Blender, Python, add-ons, hardware, RAM/VRAM | Installed Blender **5.2.2 LTS**; exact Python, add-on inventory, machine, RAM/VRAM and per-lap Ollama version **not measured/disclosed** |
| Number of laps | **10 authorized laps**: six synthetic development laps and four real proposals on **one** unique real character |
| Overall result | Development synthetic reached **20/20** on reused cases; **real primary 0/1**, no subsequent verified real success; real task **failed**, production qualification **blocked** |
| Action | Retain synthetic evidence; retest independently after targeted output/API fixes; use existing Codex fallback pending human gate |

**Executive summary:** This model generated valid Blender scripts for all 20 reused development normalization fixtures after prompt adjustments, but it never delivered a verifiably successful real self-shadow repair. The first real proposal was truncated; later proposals progressed from basic formatting to runtime API failures and did not complete the real builder/verifier. Six synthetic laps are not six independent data splits, and four real trials on one character are not four unique cases.

## 2. Stage performance and quality

| Canonical metric | Observed result | Evidence / sample size |
|---|---|---|
| Synthetic Blender-oracle first-try passes | Laps 04, 05 and 06 each **20/20**; across lap attempts **72/120** | 20 unique **reused** synthetic fixtures in five families; [per-case data](analysis-data.json) |
| Independent real PMX/Blender passes | **0/1** primary attempt; 0 verified successful repairs across 4 proposals | One unique character; real fresh verifier **never reached** |
| First-try pass rate | Best **100%** development lap; **0%** real primary | Distinct tasks; never pool synthetic and real scores |
| Offline feedback-retry success | **0/3** subsequent real proposals achieved a verified repair | Same one real character, later prompt/decoder interventions; not new independent cases |
| Severe regressions | **0** flagged across 120 synthetic records; model/source integrity verified through real trials | Narrow regression flag; a blocked proposal is not a safe/useful outcome |
| Quality vs original Codex workflow | **Not measured** under matched conditions | Existing Codex effort and fidelity baselines unavailable |
| Runtime per successful task, wall time | Synthetic successful-case p50/p95 shown below; real verified success **none** | Excludes human review and Codex time; not end-to-end qualification |
| Inference tokens, RAM/VRAM | Per-lap tokens below; RAM/VRAM and hardware/cache effects **not measured** | Request/response metadata |
| Codex fallback frequency | **Not recorded** for these trials | No fallback-run count invented |
| Sol Light and human stage decision | **No completed independent Sol Light review; no human artistic acceptance** | Do not infer a human review from a machine field |
| Motion/face ROM coverage | **Not tested** | Outside this Stage 03 geometry specialization |

| Synthetic lap | First-try pass | Blocked | Not run | Successful-case model+oracle p50/p95 s | Total lap wall s | Input/output tokens |
|---|---:|---:|---:|---:|---:|---:|
| lap-01 | 0/20 | 0 | 20 | —/— | 1162.3 | 17284/19982 |
| lap-02 | 0/20 | 20 | 0 | —/— | 681.8 | 17984/11118 |
| lap-03 | 12/20 | 8 | 0 | 32.8/37.5 | 747.2 | 26164/11445 |
| lap-04 | 20/20 | 0 | 0 | 34.0/37.4 | 743.1 | 28124/10645 |
| lap-05 | 20/20 | 0 | 0 | 31.4/33.5 | 693.4 | 28104/10548 |
| lap-06 | 20/20 | 0 | 0 | 31.4/33.4 | 693.0 | 28104/10548 |

These timings are observed generation plus oracle measurements for synthetic successes only; they exclude independent review. Total lap wall time includes failed and not-run cases. Neither indicates qualified production throughput.

| Real trial | Independent/assisted | Proposal result | Input/output tokens | Trial elapsed s | Fresh real verifier |
|---|---|---|---:|---:|---|
| lap-07 | Independent primary | Truncated JSON; no execution | 1605/1536 | 104.5 | **Not reached** |
| lap-08 | Same-fixture development | Invalid GEOMETRY modifier; builder error | 1605/2051 | 157.9 | **Not reached** |
| lap-09 | Same-fixture development | Missing explanation; invalid syntax; not executed | 1865/1880 | 146.0 | **Not reached** |
| lap-10 | Same-fixture development | GeometryNodesTree typo; builder error | 2174/1776 | 142.9 | **Not reached** |

**Test quality:** The trusted synthetic oracle checked deform-weight normalization and protected geometry, topology, transforms, shape keys and MASK data. Returned modified-count accuracy was **not independently scored**. Five correlated fixture families and the same 20 cases were reused; there was no untouched validation split. Per-case ID, category, severity, hash and timing evidence is in [analysis-data.json](analysis-data.json).

**Real application quality:** The single protected real source was assessed through the local Blender isolation environment, but no candidate completed the real repair and fresh verification, with no accepted Cycles render or human signoff. This is a **synthetic-to-real gap**. Rig deformation, motion frames, retarget maps, clean stock Blender and independent source-family fidelity are **not measured**.

## 3. Lap-by-lap failure analysis

Every lap below preserves its original outcome rather than retroactively treating a retry as a first attempt. Individual run dates, exact private source identifiers and raw tracebacks remain withheld or unavailable in the public export. Each lap uses its own [frozen prompt archive](prompts/README.md); weights were not trained. Ledger category `evaluator` for blocked builder outcomes is retained, even where the diagnosed *candidate* API misuse is the probable cause.

### Synthetic lap 01 — Baseline prompt and JSON-output contract with 4096/1536 limits

| Field | Recorded finding |
|---|---|
| Lap ID / date / attempt / status | `lap-01`; individual date not published; one first attempt per each of 20 fixtures; **0/20** pass |
| Model / prompt / decoding | `ministral-3:8b`, digest `1922accd5827ebe6829e536369195db25eaf664528dc66206d646ea3bb386b71`; [archived prompt](prompts/lap-01-prompts.json); JSON, temperature 0, context 4096, output 1536; other optional controls not explicitly set |
| Data/split | Cases 000–019 in five synthetic families; reused **development fixtures**; no untouched holdout |
| Change / mechanism | Baseline prompt and JSON-output contract with 4096/1536 limits |
| First-try / real tests | **0/20** synthetic; independent real **not run** |
| Failures / severe / repair / fallback | 20 × not_run / invalid_output / none; severe regression flags **0**; no within-case repair; Codex fallback **not recorded** |
| Time / compute / cost | Total lap elapsed **1162.3 s**; input/output **17284/19982** tokens; RAM/VRAM, human effort, monetary cost **not measured** |

| Failed case/frame | Expected vs actual | Failure category | Cause status | Severity | Evidence |
|---|---|---|---|---|---|
| `000, 001, 002, 003, 004, 005, 006, 007, 008, 009, 010, 011, 012, 013, 014, 015, 016, 017, 018, 019` | Expected valid Blender code and normalized deform weights; observed: All 20 returned code of object type rather than required string; no script executed | 20 × not_run / invalid_output / none | Observed output type mismatch; other causal inference unproven | Ledger labels `none` for blocked/not-run; unusable outcome is still a failure | [Case records](analysis-data.json); [prompt](prompts/lap-01-prompts.json) |

**Where/why:** All 20 returned code of object type rather than required string; no script executed. **Adjustments/frozen:** Baseline prompt and JSON-output contract with 4096/1536 limits; base synthetic task and same twenty cases held fixed, model weights unchanged. **Measured before/after:** Not comparable to independent holdout; baseline 0/20. **Decision:** Stop and clarify required JSON value types.

### Synthetic lap 02 — Explicitly require code and explanation as JSON strings

| Field | Recorded finding |
|---|---|
| Lap ID / date / attempt / status | `lap-02`; individual date not published; one first attempt per each of 20 fixtures; **0/20** pass |
| Model / prompt / decoding | `ministral-3:8b`, digest `1922accd5827ebe6829e536369195db25eaf664528dc66206d646ea3bb386b71`; [archived prompt](prompts/lap-02-prompts.json); JSON, temperature 0, context 4096, output 1536; other optional controls not explicitly set |
| Data/split | Cases 000–019 in five synthetic families; reused **development fixtures**; no untouched holdout |
| Change / mechanism | Explicitly require code and explanation as JSON strings |
| First-try / real tests | **0/20** synthetic; independent real **not run** |
| Failures / severe / repair / fallback | 20 × blocked / evaluator / none; severe regression flags **0**; no within-case repair; Codex fallback **not recorded** |
| Time / compute / cost | Total lap elapsed **681.8 s**; input/output **17984/11118** tokens; RAM/VRAM, human effort, monetary cost **not measured** |

| Failed case/frame | Expected vs actual | Failure category | Cause status | Severity | Evidence |
|---|---|---|---|---|---|
| `000, 001, 002, 003, 004, 005, 006, 007, 008, 009, 010, 011, 012, 013, 014, 015, 016, 017, 018, 019` | Expected valid Blender code and normalized deform weights; observed: 20 Blender builder failures: eight Mesh.vertex_groups, ten from_edit_mesh mode, one BMVert.groups, one BMesh lookup-table error | 20 × blocked / evaluator / none | Observed Blender exception patterns; other causal inference unproven | Ledger labels `none` for blocked/not-run; unusable outcome is still a failure | [Case records](analysis-data.json); [prompt](prompts/lap-02-prompts.json) |

**Where/why:** 20 Blender builder failures: eight Mesh.vertex_groups, ten from_edit_mesh mode, one BMVert.groups, one BMesh lookup-table error. **Adjustments/frozen:** Explicitly require code and explanation as JSON strings; base synthetic task and same twenty cases held fixed, model weights unchanged. **Measured before/after:** 0/20 → 0/20 verified (+0 pp); format improved, API calls did not. **Decision:** Continue with Blender API guidance.

### Synthetic lap 03 — Add loading-mesh sentence and verified Blender API guidance

| Field | Recorded finding |
|---|---|
| Lap ID / date / attempt / status | `lap-03`; individual date not published; one first attempt per each of 20 fixtures; **12/20** pass |
| Model / prompt / decoding | `ministral-3:8b`, digest `1922accd5827ebe6829e536369195db25eaf664528dc66206d646ea3bb386b71`; [archived prompt](prompts/lap-03-prompts.json); JSON, temperature 0, context 4096, output 1536; other optional controls not explicitly set |
| Data/split | Cases 000–019 in five synthetic families; reused **development fixtures**; no untouched holdout |
| Change / mechanism | Add loading-mesh sentence and verified Blender API guidance |
| First-try / real tests | **12/20** synthetic; independent real **not run** |
| Failures / severe / repair / fallback | 8 × blocked / evaluator / none; severe regression flags **0**; no within-case repair; Codex fallback **not recorded** |
| Time / compute / cost | Total lap elapsed **747.2 s**; input/output **26164/11445** tokens; RAM/VRAM, human effort, monetary cost **not measured** |

| Failed case/frame | Expected vs actual | Failure category | Cause status | Severity | Evidence |
|---|---|---|---|---|---|
| `001, 004, 006, 009, 011, 013, 015, 019` | Expected valid Blender code and normalized deform weights; observed: Cases 001/004/006/009/011/013/015/019: unsupported VertexGroup.remove kwargs (six ok_if_not_assigned, two ok_if_empty) | 8 × blocked / evaluator / none | Observed unsupported keyword arguments; other causal inference unproven | Ledger labels `none` for blocked/not-run; unusable outcome is still a failure | [Case records](analysis-data.json); [prompt](prompts/lap-03-prompts.json) |

**Where/why:** Cases 001/004/006/009/011/013/015/019: unsupported VertexGroup.remove kwargs (six ok_if_not_assigned, two ok_if_empty). **Adjustments/frozen:** Add loading-mesh sentence and verified Blender API guidance; base synthetic task and same twenty cases held fixed, model weights unchanged. **Measured before/after:** 0/20 → 12/20 (+60 pp); two changes confounded. **Decision:** Clarify documented remove signature and test again.

### Synthetic lap 04 — Clarify VertexGroup.remove arguments and change 'concise' to 'succinct'

| Field | Recorded finding |
|---|---|
| Lap ID / date / attempt / status | `lap-04`; individual date not published; one first attempt per each of 20 fixtures; **20/20** pass |
| Model / prompt / decoding | `ministral-3:8b`, digest `1922accd5827ebe6829e536369195db25eaf664528dc66206d646ea3bb386b71`; [archived prompt](prompts/lap-04-prompts.json); JSON, temperature 0, context 4096, output 1536; other optional controls not explicitly set |
| Data/split | Cases 000–019 in five synthetic families; reused **development fixtures**; no untouched holdout |
| Change / mechanism | Clarify VertexGroup.remove arguments and change 'concise' to 'succinct' |
| First-try / real tests | **20/20** synthetic; independent real **not run** |
| Failures / severe / repair / fallback | no non-pass rows; severe regression flags **0**; no within-case repair; Codex fallback **not recorded** |
| Time / compute / cost | Total lap elapsed **743.1 s**; input/output **28124/10645** tokens; RAM/VRAM, human effort, monetary cost **not measured** |

| Failed case/frame | Expected vs actual | Failure category | Cause status | Severity | Evidence |
|---|---|---|---|---|---|
| None | Expected valid Blender code and normalized deform weights; observed: No failed synthetic cases; one-word change not isolated | no non-pass rows | Not applicable; no failing case; other causal inference unproven | None flagged | [Case records](analysis-data.json); [prompt](prompts/lap-04-prompts.json) |

**Where/why:** No failed synthetic cases; one-word change not isolated. **Adjustments/frozen:** Clarify VertexGroup.remove arguments and change 'concise' to 'succinct'; base synthetic task and same twenty cases held fixed, model weights unchanged. **Measured before/after:** 12/20 → 20/20 (+40 pp); not independent holdout. **Decision:** Revert stylistic wording next lap, retain signature correction.

### Synthetic lap 05 — Revert 'succinct' to 'concise', retain remove signature clarification

| Field | Recorded finding |
|---|---|
| Lap ID / date / attempt / status | `lap-05`; individual date not published; one first attempt per each of 20 fixtures; **20/20** pass |
| Model / prompt / decoding | `ministral-3:8b`, digest `1922accd5827ebe6829e536369195db25eaf664528dc66206d646ea3bb386b71`; [archived prompt](prompts/lap-05-prompts.json); JSON, temperature 0, context 4096, output 1536; other optional controls not explicitly set |
| Data/split | Cases 000–019 in five synthetic families; reused **development fixtures**; no untouched holdout |
| Change / mechanism | Revert 'succinct' to 'concise', retain remove signature clarification |
| First-try / real tests | **20/20** synthetic; independent real **not run** |
| Failures / severe / repair / fallback | no non-pass rows; severe regression flags **0**; no within-case repair; Codex fallback **not recorded** |
| Time / compute / cost | Total lap elapsed **693.4 s**; input/output **28104/10548** tokens; RAM/VRAM, human effort, monetary cost **not measured** |

| Failed case/frame | Expected vs actual | Failure category | Cause status | Severity | Evidence |
|---|---|---|---|---|---|
| None | Expected valid Blender code and normalized deform weights; observed: No synthetic failures | no non-pass rows | Not applicable; no failing case; other causal inference unproven | None flagged | [Case records](analysis-data.json); [prompt](prompts/lap-05-prompts.json) |

**Where/why:** No synthetic failures. **Adjustments/frozen:** Revert 'succinct' to 'concise', retain remove signature clarification; base synthetic task and same twenty cases held fixed, model weights unchanged. **Measured before/after:** 20/20 → 20/20 (+0 pp), signature fix retained. **Decision:** Repeat unchanged to check deterministic replay.

### Synthetic lap 06 — Repeat lap 05 exactly, no new feedback or code change

| Field | Recorded finding |
|---|---|
| Lap ID / date / attempt / status | `lap-06`; individual date not published; one first attempt per each of 20 fixtures; **20/20** pass |
| Model / prompt / decoding | `ministral-3:8b`, digest `1922accd5827ebe6829e536369195db25eaf664528dc66206d646ea3bb386b71`; [archived prompt](prompts/lap-06-prompts.json); JSON, temperature 0, context 4096, output 1536; other optional controls not explicitly set |
| Data/split | Cases 000–019 in five synthetic families; reused **development fixtures**; no untouched holdout |
| Change / mechanism | Repeat lap 05 exactly, no new feedback or code change |
| First-try / real tests | **20/20** synthetic; independent real **not run** |
| Failures / severe / repair / fallback | no non-pass rows; severe regression flags **0**; no within-case repair; Codex fallback **not recorded** |
| Time / compute / cost | Total lap elapsed **693.0 s**; input/output **28104/10548** tokens; RAM/VRAM, human effort, monetary cost **not measured** |

| Failed case/frame | Expected vs actual | Failure category | Cause status | Severity | Evidence |
|---|---|---|---|---|---|
| None | Expected valid Blender code and normalized deform weights; observed: No synthetic failures; all 20 saved response texts and code bytes match lap 05 | no non-pass rows | Not applicable; no failing case; other causal inference unproven | None flagged | [Case records](analysis-data.json); [prompt](prompts/lap-06-prompts.json) |

**Where/why:** No synthetic failures; all 20 saved response texts and code bytes match lap 05. **Adjustments/frozen:** Repeat lap 05 exactly, no new feedback or code change; base synthetic task and same twenty cases held fixed, model weights unchanged. **Measured before/after:** 20/20 → 20/20 (+0 pp); repeat is not a new independent fixture. **Decision:** Stop synthetic development; attempt separate real task.

### Real lap 07 — independent primary

| Field | Recorded finding |
|---|---|
| Lap ID / date / status | `lap-07`; run date not published; **failed** real proposal; one unique shared real character across laps 07–10 |
| Model / prompt / settings | `ministral-3:8b` / `1922accd5827ebe6829e536369195db25eaf664528dc66206d646ea3bb386b71`; [redacted archived prompt](prompts/real-lap07-prompt.txt); JSON, temp 0, context 4096, output 1536; optional seed/think/presence/repeat omitted |
| Data and split | One private pre-repair Stage 02 character; not an independent holdout on later laps; source identifiers redacted |
| Change / reason | Primary, unassisted real-character prompt; transfer the synthetic coding skill to hair self-shadow repair. |
| First-try verified real score | **0/1 primary**; independently verified real **0/1** |
| Execution / severe / fallback | Candidate execution not observed; builder completed **no**, fresh verifier **not reached**, protected sources and model blobs unchanged; Codex fallback not recorded |
| Time / tokens / cost | 104.5 s controller elapsed; **1605/1536** input/output tokens; RAM/VRAM and monetary/human costs not measured |

| Failed case/frame | Expected vs actual | Failure category | Confirmed vs inferred | Severity | Reproduction/evidence |
|---|---|---|---|---|---|
| Same private real fixture | Expected completed shadow repair with protected-source preservation; actual: Output truncated at 1,536 tokens, invalid JSON, no script. | Invalid output / output-budget exhaustion | Observed `done_reason=length`; under context limit; output budget exhausted | Unusable proposal; no source damage observed | [Lap 07 prompt](prompts/real-lap07-prompt.txt); [trial metrics](analysis-data.json); private logs withheld |

**Measured before/after:** not applicable (primary); no independent verified real success in this trial. The output-format/API progression cannot be counted as a pass or validation improvement. **Decision:** Continue with larger context/output budget while preserving primary failure.

### Real lap 08 — feedback-assisted development

| Field | Recorded finding |
|---|---|
| Lap ID / date / status | `lap-08`; run date not published; **failed** real proposal; one unique shared real character across laps 07–10 |
| Model / prompt / settings | `ministral-3:8b` / `1922accd5827ebe6829e536369195db25eaf664528dc66206d646ea3bb386b71`; [redacted archived prompt](prompts/real-lap08-prompt.txt); JSON, temp 0, context 8192, output 4096; optional seed/think/presence/repeat omitted |
| Data and split | One private pre-repair Stage 02 character; not an independent holdout on later laps; source identifiers redacted |
| Change / reason | Increase context/output limits to 8192/4096; keep same base real prompt. |
| First-try verified real score | **not a new primary case; 0/1 remains primary**; independently verified real **0/1** |
| Execution / severe / fallback | Candidate execution observed in traceback; builder completed **no**, fresh verifier **not reached**, protected sources and model blobs unchanged; Codex fallback not recorded |
| Time / tokens / cost | 157.9 s controller elapsed; **1605/2051** input/output tokens; RAM/VRAM and monetary/human costs not measured |

| Failed case/frame | Expected vs actual | Failure category | Confirmed vs inferred | Severity | Reproduction/evidence |
|---|---|---|---|---|---|
| Same private real fixture | Expected completed shadow repair with protected-source preservation; actual: Valid response but Blender raised invalid GEOMETRY modifier type. | Blender API misuse | Observed runtime exception for unsupported modifier type; builder did not complete | Blocking execution failure; not a verified source regression | [Lap 08 prompt](prompts/real-lap08-prompt.txt); [trial metrics](analysis-data.json); private logs withheld |

**Measured before/after:** real lap 07: failed; no independent verified real success in this trial. The output-format/API progression cannot be counted as a pass or validation improvement. **Decision:** Add general modifier API reference next lap.

### Real lap 09 — feedback-assisted development

| Field | Recorded finding |
|---|---|
| Lap ID / date / status | `lap-09`; run date not published; **failed** real proposal; one unique shared real character across laps 07–10 |
| Model / prompt / settings | `ministral-3:8b` / `1922accd5827ebe6829e536369195db25eaf664528dc66206d646ea3bb386b71`; [redacted archived prompt](prompts/real-lap09-prompt.txt); JSON, temp 0, context 8192, output 4096; optional seed/think/presence/repeat omitted |
| Data and split | One private pre-repair Stage 02 character; not an independent holdout on later laps; source identifiers redacted |
| Change / reason | Append general modifier API guidance, retaining raised token limits. |
| First-try verified real score | **not a new primary case; 0/1 remains primary**; independently verified real **0/1** |
| Execution / severe / fallback | Candidate execution not observed; builder completed **no**, fresh verifier **not reached**, protected sources and model blobs unchanged; Codex fallback not recorded |
| Time / tokens / cost | 146.0 s controller elapsed; **1865/1880** input/output tokens; RAM/VRAM and monetary/human costs not measured |

| Failed case/frame | Expected vs actual | Failure category | Confirmed vs inferred | Severity | Reproduction/evidence |
|---|---|---|---|---|---|
| Same private real fixture | Expected completed shadow repair with protected-source preservation; actual: Missing explanation key; code had unmatched closing brace on static inspection; no execution. | Output-contract violation and Python syntax error | Observed missing required key, static invalid Python; unsupported reduction assumptions untested | Unusable proposal before execution | [Lap 09 prompt](prompts/real-lap09-prompt.txt); [trial metrics](analysis-data.json); private logs withheld |

**Measured before/after:** real lap 08: failed; no independent verified real success in this trial. The output-format/API progression cannot be counted as a pass or validation improvement. **Decision:** Clarify required explanation and prohibit unsupported assumptions.

### Real lap 10 — feedback-assisted development

| Field | Recorded finding |
|---|---|
| Lap ID / date / status | `lap-10`; run date not published; **failed** real proposal; one unique shared real character across laps 07–10 |
| Model / prompt / settings | `ministral-3:8b` / `1922accd5827ebe6829e536369195db25eaf664528dc66206d646ea3bb386b71`; [redacted archived prompt](prompts/real-lap10-prompt.txt); JSON, temp 0, context 8192, output 4096; optional seed/think/presence/repeat omitted |
| Data and split | One private pre-repair Stage 02 character; not an independent holdout on later laps; source identifiers redacted |
| Change / reason | Require explanation string and no unsupported assumptions. |
| First-try verified real score | **not a new primary case; 0/1 remains primary**; independently verified real **0/1** |
| Execution / severe / fallback | Candidate execution observed in traceback; builder completed **no**, fresh verifier **not reached**, protected sources and model blobs unchanged; Codex fallback not recorded |
| Time / tokens / cost | 142.9 s controller elapsed; **2174/1776** input/output tokens; RAM/VRAM and monetary/human costs not measured |

| Failed case/frame | Expected vs actual | Failure category | Confirmed vs inferred | Severity | Reproduction/evidence |
|---|---|---|---|---|---|
| Same private real fixture | Expected completed shadow repair with protected-source preservation; actual: Valid JSON and Python; Blender errored on GeometryNodesTree instead of GeometryNodeTree; placeholder logic. | Blender API identifier error and incomplete implementation | Observed builder traceback, not task completion; no fresh verifier reached | Blocking execution failure; no verified real repair | [Lap 10 prompt](prompts/real-lap10-prompt.txt); [trial metrics](analysis-data.json); private logs withheld |

**Measured before/after:** real lap 09: failed; no independent verified real success in this trial. The output-format/API progression cannot be counted as a pass or validation improvement. **Decision:** Stop after ten authorized laps; retain 0/1 primary score.


## 4. Specialization effectiveness (within the same model)

| Metric | Untuned baseline (lap 01) | Specialized lap 06 | Absolute / relative change | Comparable? |
|---|---|---|---|---|
| Synthetic first-try pass | **0/20** | **20/20** | **+20 passes, +100 percentage points**; relative % undefined due zero baseline | Same **reused** cases; altered prompt |
| Real-workflow success | Not run | Subsequent real proposals all fail | Cannot compute matched improvement | **No**; distinct task and fixture |
| Severe regressions | 0 flagged | 0 flagged | 0 observed | Only narrow synthetic regression checks |
| Repairs / fallback | No within-case repair; fallback unknown | No within-case repair; real feedback sequence not a new first try | Not comparable | No |
| Time per verified success | Undefined (zero successes) | Successful-case model+oracle p50/p95 **31.4/33.4 s**; no review time | Undefined | No successful baseline |
| RAM / VRAM | Not measured | Not measured | Unknown | No |

**Observed trajectory:** Output-schema clarification (lap 02) did not fix Blender API errors. API context (lap 03) yielded 12/20; clarifying documented remove arguments (lap 04) yielded 20/20. Reverting a stylistic word (lap 05) kept 20/20, and untouched repeat lap 06 produced identical outputs for all twenty cases. The individual contribution of two simultaneous changes in laps 03–04 was **not experimentally isolated**. No LoRA or other model-weight specialization is evidenced, and no independent held-out transfer or outside-scope regression can be claimed. Costs relative to Codex and real usability remain unknown.

## 5. Workflow integration and safety

| Required control | Observed evidence | Exact disposition |
|---|---|---|
| Proposal generation | Six synthetic rounds; four real proposals; lap 07 truncated, lap 09 missing required explanation | **Recorded**; output schema failures preserved |
| Sandboxed Blender execution on disposable input | Installed Blender 5.2.2 LTS in no-network bubblewrap/systemd/cgroup/seccomp isolation; real lap 08 and 10 executed far enough to throw Blender exceptions; 07/09 did not | **Executed only for eligible scripts**; not a Docker Blender image |
| Deterministic oracle / fresh real verification | 120 synthetic trusted outcomes; real builder never completed | Synthetic pass at 04–06; real **not reached**, not pass |
| Actual independent Sol Light review | No completed review evidence in this package | **Not obtained** |
| Codex fallback | Project requires it for unqualified candidates; no fallback-run count here | **Not recorded**, not a model pass |
| Human gate / checkpoint identity | No human Stage03 approval; source/model layers verified unchanged | **Human approval not obtained**; integrity recorded |
| Unauthorized file/network changes, crashes, untrusted Python | Local sandbox, read-only/protected sources, no-network constraints, before/after integrity checks; script exceptions observed | Bounded controls; **not** a universal security certification |
| External dependencies, clean stock Blender, Cycles-only independent acceptance | Installed runtime used, no validated accepted Cycles reference render published | **Not measured / not approved** |

**Gate interpretation:** The exploratory numeric requirement of ≥75% first-try on 20 seeded fixtures and zero severe flags was satisfied in synthetic laps 04–06. The additional **≤35% of original Codex effort** condition was **not measured**, so complete exploratory go/no-go is unresolved. Production qualification requires **≥300 independent held-out examples per stage**, zero observed failures on that scope, actual Sol Light review and explicit human gates; none of these are met by this package. The independent review ledger's **>10%** repair/rejection escalation remains a separate operational obligation; there is no evidence of approval to bypass it.

## 6. Miscellaneous findings and future analysis

| Finding category | Notes and supporting evidence |
|---|---|
| Unexpected successes/failures | Synthetic 20/20 repeated, yet every real proposal failed before full verification |
| Prompt/template sensitivity | JSON string requirement, supported remove() signature, concise/succinct reversal and exact repeat of lap 05 in 06 |
| Quantization and reasoning mode | GGUF Q4_K_M; native metadata temperature 0.15 versus explicit benchmark temperature 0; thinking capability not advertised/observed |
| Blender API/version incompatibilities | Mesh.vertex_groups, from_edit_mesh mode, VertexGroup.remove kwargs, GEOMETRY modifier and GeometryNodesTree vs GeometryNodeTree |
| PMX/VMD names and retarget maps | **Not measured** for geometry normalization/real repair experiment |
| Stage 04 pole/IK unknowns | **Not tested**; this report supplies no permission to expand beyond authorized left-arm pilot |
| Training data/licenses/source leakage | Reused five synthetic families; one private real source; upstream licenses and held-out family leakage **not publicly verified** |
| Deformation/geometry/motion/face | Protected synthetic invariants checked; returned modified-count oracle missing; no scored independent real deformation/motion/face |
| Hardware, cache, runtime | Timings/tokens captured per lap; physical RAM/VRAM/cache, engine version and Codex baseline **not measured** |
| Repeatability/evaluator weaknesses | All twenty request bodies/responses/code bytes matched laps 05–06; blocked category does not itself distinguish model API bug from evaluator fault |
| Future experiments | Early strict JSON schema, Blender API smoke checks, holdout tasks, independent source families, controlled prompt ablations and successful real verification |

**Reproducibility attachment manifest:** Exact tag `ministral-3:8b`, digest `1922accd5827ebe6829e536369195db25eaf664528dc66206d646ea3bb386b71`, parameter count/quantization, native-template SHA-256 `5b74c26b9e0b6358e73d0a7eb2f955105097e7bd10b45fa0d2a50f0a906e0798`, explicit [lap request prompts](prompts/README.md), [120 case results and four real-trial metadata rows](analysis-data.json), [interpretations](analysis-notes.md), [privacy/provenance](privacy-and-provenance.md), and refreshed [package checksums](SHA256SUMS). Fixture IDs 000–019 span five correlated synthetic families; private real reference, model-generated source, raw logs, private checkpoint SHA, licensing/source split hashes, full render sheets, reviewer signoff, exact private replay commands, GGUF/adapter file hashes and individual execution dates are **withheld or not recorded**. Public hashes detect export changes, not external attestation.

## 7. Final verdict

| Verdict field | Evidence-based disposition |
|---|---|
| Readiness | **Experimental** for synthetic development; **not production-qualified**; real Stage 03 repair **failed** |
| Within-model quality | 0/20 baseline → 20/20 reused development cases, but **0/1** independent real primary; Codex comparison **not measured** |
| Best lap | **Laps 04–06** reached 20/20 development; **lap 06** is final unchanged repeat, **not** validation-selected best; `best_lap_id=null` without independent validation |
| Remaining faults | Real lap 07 truncated JSON, 08 GEOMETRY API exception, 09 missing explanation/invalid syntax, 10 GeometryNodesTree typo and placeholder logic |
| Next action | Preserve existing data, repair schema/API weaknesses, retest on independent real sources; **Codex fallback** for unqualified work |
| Evidence confidence | 120 attempts on just **20 reused** synthetic fixtures; four proposals on **one** real source; no untouched 300-case test, no independent human approval |
| Human decision | **Not yet obtained**; no implicit promotion or checkpoint change |

**Final status:** Ten authorized laps are complete, no new lap has been scheduled or executed by this documentation change. Do not treat synthetic 20/20 as an accepted PMX conversion.

Supporting material: [analysis notes](analysis-notes.md), [machine-readable metrics](analysis-data.json), [lap prompts](prompts/README.md), and [privacy/provenance](privacy-and-provenance.md).
