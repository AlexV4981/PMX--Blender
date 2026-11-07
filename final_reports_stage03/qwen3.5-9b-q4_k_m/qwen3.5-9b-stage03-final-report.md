# Qwen3.5 9B — final Stage03 evaluation report

Finalized 2026-11-07. Sanitized public edition. Narrative interpretation is by the benchmark operator; numerical synthetic results were regenerated from verified saved events. This report follows [MODEL_REPORT_STANDARD.md](../../MODEL_REPORT_STANDARD.md) for one model only. [Prompts are archived by lap and trial](prompts/README.md).

## 1. Experiment Summary

| Field | Value / evidence status |
|---|---|
| Experiment ID / date | `Stage03-qwen3.5-9b-Q4_K_M`; report finalized **2026-11-07**; individual run timestamps not published |
| Model / exact tag / digest | Qwen3.5, `qwen3.5:9b`, `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90` |
| Size / quantization | 8,953,803,264 parameters; GGUF `Q4_K_M` |
| Base revision / adapter / checkpoint | Saved model digest above; source-base commit **not recorded**; **no trained adapter or model-weight fine-tuning**; private asset checkpoint withheld |
| Stage / narrow task | Stage 03 geometry; synthetic deform-weight normalization; distinct independent real hair self-shadow repair |
| Approach | Prompt and decoder specialization, Ollama with Blender oracle; no training |
| Environment | Blender 5.2.2; Python/add-ons build, machine, RAM/VRAM and per-run Ollama version **not disclosed / not measured** |
| Laps attempted | 8 synthetic development laps, 1 primary real trial, 1 separately assisted real retry; **no synthetic laps 9–10** |
| Overall result | Development synthetic **20/20** best reused lap; independent real **0/1**; overall **fail for demonstrated real repair**, production qualification blocked |
| Next action | Retain evidence, retest on untouched real families and repair controls; default to existing Codex workflow pending approval |

**Claim discipline:** Numerical metrics below are **observed** in retained evidence; model-specific causal diagnoses are labeled **inferred** unless supported by an actual traceback; omitted hardware and review fields are **not measured**, not zero.


Qwen3.5 9B Q4_K_M (`qwen3.5:9b`) completed eight synthetic development laps, followed by one primary real-character attempt and one explicitly assisted final retry. These are ten recorded evaluation phases, not ten interchangeable synthetic laps. No synthetic laps 9 or 10 were run. Weights were not trained or fine-tuned; adjustments changed prompts or inference settings.

Model digest: `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`.

The synthetic task normalized deform weights on the same 20 development fixtures from five synthetic families each lap. It produced 160 first-try attempts across eight laps, representing 20 reused cases. The real task asked for repair of a hair self-shadow artifact from a pre-repair Stage02 checkpoint while preserving source geometry, shape keys, materials, eyes, rig and animation behavior. Its accepted Stage03 reference remained private. This is a different repair operation, so the two task scores are not pooled.

Blender 5.2.2 was used. Synthetic lap 1 used temperature 0, context 4,096, output limit 1,536 and server-default thinking. Lap 2 used context 8,192, output limit 4,096 and explicit thinking disabled. Lap 3 also set presence penalty to 0 and added API guidance; laps 4-8 kept those generation settings. Synthetic seeds were not specified. Both real attempts used temperature 0, context 8,192, output limit 4,096, thinking disabled, seed 0, presence penalty 0, repeat penalty 1 and JSON output.

## 2. Performance, Quality and Benchmark Results

| Canonical metric | Observed result | Sample and evidence |
|---|---|---|
| Synthetic Blender-oracle first-try passes | **20/20 (100%) at development lap 08**; cumulative 98/160 across 8 distinct lap executions | Only **20 unique reused synthetic fixtures**, five correlated families; [all-case data](analysis-data.json) |
| Independent real PMX/Blender passes | **0/1** primary real-character repair | One unique real character; no verified repair; private real evidence |
| First-try pass rate | Development lap 08: 100%; distinct real primary: 0% | Separate tasks/denominators; no pooled rate |
| Offline feedback-retry success | **0/1**; incomplete output, not executed | Assisted attempt on **same** real case, excluded from first-try |
| Severe regressions | **0** flagged in 160 synthetic verdict records; integrity verified for real originals | Narrow recorded checks only, not a global safety guarantee |
| Quality vs original Codex workflow | **Not measured** on matched independent tasks | Codex accepted workflow baseline not quantified; real attempted repair failed |
| Runtime per successful task | **Not established** end-to-end; lap 08 all-case model+oracle p50/p95 30.9/37.7 s | Synthetic only; excludes Sol Light/human and Codex effort |
| Inference tokens, RAM/VRAM | Lap 08 17,944 input / 9,870 output across 20 requests; RAM/VRAM **not measured** | Request/output metadata; runtime hardware not in public data |
| Codex fallback frequency | **Not recorded** | Existing fallback remains required if unqualified |
| Sol Light review and human gate | **No completed independent Sol Light review; human artistic decision not obtained** | A generated JSON flag is not review; render evidence does not imply signoff |
| Motion / face ROM coverage | **Not tested** | Stage 03 geometry scope; no Stage 06 qualification |

**Test quality:** Synthetic oracle checked deform-weight normalization while protecting scene invariants; twenty seeded development fixtures in five families were reused over eight laps. Per-case results and prompt hashes are in [analysis-data.json](analysis-data.json) and [prompts](prompts/README.md). No independent held-out geometry split is shown. Frame-by-frame deformation or motion coverage was not measured.

**Real application quality and synthetic-to-real gap:** The real task differed from synthetic weight normalization: a protected hair self-shadow repair was needed on a private character. The first real script executed but made no repair; assisted output was invalid JSON and was never executed. The fresh structural verifier rejected the first, and neither reached human Cycles approval. Unknown motion/retarget/clean-stock behavior is **not** a pass.


All first attempts remain in each denominator. Blocked, not-run and missing verdicts never count as passes. No within-case synthetic repair attempts were recorded. Severe regression flags were zero in all eight laps; this is a recorded metric, not a general safety guarantee.

| Synthetic lap | First-try pass | Rate | Wilson 95% | Fail | Blocked | Not run | No verdict |
|---|---:|---:|---|---:|---:|---:|---:|
| 1 | 0/20 | 0% | 0-16% | 0 | 0 | 20 | 0 |
| 2 | 0/20 | 0% | 0-16% | 1 | 17 | 2 | 0 |
| 3 | 19/20 | 95% | 76-99% | 0 | 1 | 0 | 0 |
| 4 | 19/20 | 95% | 76-99% | 0 | 1 | 0 | 0 |
| 5 | 19/20 | 95% | 76-99% | 0 | 1 | 0 | 0 |
| 6 | 7/20 | 35% | 18-57% | 0 | 13 | 0 | 0 |
| 7 | 14/20 | 70% | 48-85% | 1 | 5 | 0 | 0 |
| 8 | 20/20 | 100% | 84-100% | 0 | 0 | 0 | 0 |

These exploratory intervals assume more independence than reused, correlated development fixtures provide. They do not estimate production reliability.

| Synthetic lap | p50 / p95 model + oracle seconds | Model + oracle passes/min | Input / output tokens |
|---|---:|---:|---:|
| 1 | 87.9 / 90.6 | 0.00 | 6,084 / 30,720 |
| 2 | 41.2 / 57.3 | 0.00 | 6,124 / 13,384 |
| 3 | 31.0 / 43.5 | 1.69 | 14,064 / 10,661 |
| 4 | 30.5 / 43.0 | 1.71 | 14,064 / 10,661 |
| 5 | 30.4 / 42.3 | 1.73 | 14,064 / 10,661 |
| 6 | 32.0 / 70.6 | 0.56 | 16,784 / 11,906 |
| 7 | 33.7 / 49.0 | 1.18 | 15,844 / 11,288 |
| 8 | 30.9 / 37.7 | 1.90 | 17,944 / 9,870 |

Timing and throughput above exclude human review and are not end-to-end workflow measurements. Cost and operator effort relative to the accepted workflow were not measured.

| Real-character trial | Primary score contribution | Observed result | Input / output tokens | Inference / total seconds |
|---|---|---|---:|---:|
| Unassisted first attempt | 0/1 | Valid saved derivative; repair absent; fresh verifier rejected it | 980 / 1,391 | 92.94 / 178.73 |
| Assisted final retry | Separate; does not replace primary score | Incomplete JSON at output limit; no candidate execution or Blender verdict | 1,009 / 4,096 | 272.38 / 285.08 |

Both real submissions were unsuccessful. Only the first produced a Blender artifact and reached structural verification. There is one unique real character, not two independent real cases.

## 3. Lap-by-Lap Failure and Adjustment Analysis

The following diagnoses are operator interpretations of retained evidence. Generic ledger categories are preserved separately below rather than silently relabeled.

| Phase | Adjustment and observed failure |
|---|---|
| Synthetic 1 | Initial configuration yielded no usable code in all 20 cases. Recorded diagnosis identified output budget consumed by thinking. |
| Synthetic 2 | Increased context/output and disabled thinking. Object-versus-Mesh ownership, weight-method calls and membership errors persisted, with two syntax errors, two unusable proposals and one normalization failure. |
| Synthetic 3 | Added verified Blender API guidance and set presence penalty to zero. Nineteen cases passed; case 007 used an unsupported collection length attribute. Multiple settings changed together; individual causal contribution was not isolated. |
| Synthetic 4 | Unchanged repeat of lap 3; the same case failed at the builder stage. |
| Synthetic 5 | Unchanged repeat; the same case failed again. Retained builder evidence confirmed the unsupported length attribute. Repeating the same prompt and deterministic settings did not fix that API assumption. |
| Synthetic 6 | Added guidance about collection length, sparse assignments and returned modification counts. Result fell to 7/20: thirteen builder failures involved integer membership tests on Blender collections or a vertex-group object. All proposals were syntactically valid; generation ended normally. No controlled ablation identifies which wording caused the regression. |
| Synthetic 7 | Removed unrelated stage guidance and replaced the length warning with a plain Python explanation. Result recovered to 14/20. Remaining errors included group-versus-vertex ID confusion, integer containment, treating assignment objects as tuples and an invented API attribute. |
| Synthetic 8 | Added a simple explanation of vertex IDs, group IDs and membership assignments. All 20 reused cases passed. This is development-set success after feedback, not an untouched holdout result. |
| Real first attempt | Code relied on the active object, which was an EMPTY model root. A guard returned zero before reaching the repair logic. The actual named mesh was already present in the input summary. Fresh evaluation confirmed no repair; protected source data remained intact. Static problems in the unreached body were not counted as additional observed crashes. |
| Real final retry | Added only the instruction to select the named mesh explicitly. The partial text reflected that instruction, then repeatedly discussed possible modifiers without completing an implementation. It used all 4,096 output tokens and ended inside a JSON string. Strict parsing rejected it; no attempt was made to complete or execute the partial response. |

The final retry used identical input, weights, decoding, sandbox, evaluator and resource limits. Its feedback-assisted prompt is separate from the primary common prompt; future primary entrants retain the original conditions.

Every synthetic non-pass is retained below. Case numbers are generic synthetic fixture IDs. The recorded severity `none` is not an assertion that a failed submission was useful or safe.

| Lap | Case IDs | Result | Recorded category / severity | Sanitized evaluator note |
|---|---|---|---|---|
| 1 | 000, 001, 002, 003, 004, 005, 006, 007, 008, 009, 010, 011, 012, 013, 014, 015, 016, 017, 018, 019 | not_run | invalid_output / none | No usable proposal code; candidate not executed. |
| 2 | 000, 001, 002, 003, 004, 005, 006, 007, 008, 009, 010, 011, 015, 016, 017, 018, 019 | blocked | evaluator / none | Builder exited before a usable fresh verification result; see the attributed diagnosis in this section. |
| 2 | 012 | fail | deformation / major | Verifier rejected deform-weight normalization. |
| 2 | 013, 014 | not_run | invalid_output / none | No usable proposal code; candidate not executed. |
| 3 | 007 | blocked | evaluator / none | Builder exited before a usable fresh verification result; see the attributed diagnosis in this section. |
| 4 | 007 | blocked | evaluator / none | Builder exited before a usable fresh verification result; see the attributed diagnosis in this section. |
| 5 | 007 | blocked | evaluator / none | Builder exited before a usable fresh verification result; see the attributed diagnosis in this section. |
| 6 | 000, 004, 005, 006, 007, 008, 011, 012, 013, 015, 017, 018, 019 | blocked | evaluator / none | Builder exited before a usable fresh verification result; see the attributed diagnosis in this section. |
| 7 | 005 | fail | deformation / major | Verifier rejected deform-weight normalization. |
| 7 | 008, 010, 012, 018, 019 | blocked | evaluator / none | Builder exited before a usable fresh verification result; see the attributed diagnosis in this section. |

There are no non-pass cases in synthetic lap 8. Private raw artifacts remain with the operator; this public summary is not a substitute for their full verification bundle.


### Synthetic lap 01 — Initial untuned prompt/decoder configuration; test initial code generation.

| Field | Recorded finding |
|---|---|
| ID / date / attempt / status | `lap-01`; individual run date not published; attempt 1 per case; 0/20 pass |
| Model, prompt and decoding | `qwen3.5:9b` / `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`; [archived prompt](prompts/lap-01-prompts.json); 4096 context, 1536 output, temperature 0, thinking server-default, presence penalty not explicitly overridden |
| Dataset / held-out status | Synthetic cases 000–019; five correlated families; **same reused development fixtures**, not held out |
| Objective / change / why | Initial untuned prompt/decoder configuration; test initial code generation. |
| First-try synthetic; real | **0/20**; independent real **not run** in this lap |
| Severe regression / repair / fallback | Ledger severe flag: **0**; no within-case synthetic repair; Codex fallback **not recorded** |
| Runtime, compute and cost | Model+oracle p50/p95 **87.9/90.6 s across all cases**; tokens input/output **6084/30720**; RAM, VRAM, monetary cost and human effort **not measured** |

| Failed case/frame | Expected vs actual | Recorded failure category | Cause status | Severity | Reproduction/evidence |
|---|---|---|---|---|---|
| `000, 001, 002, 003, 004, 005, 006, 007, 008, 009, 010, 011, 012, 013, 014, 015, 016, 017, 018, 019` | Expected a valid deform-weight normalization preserving protected data; observed `not_run`: No usable proposal code; candidate not executed. | `invalid_output / none` (original recorded category/severity) | See diagnosis; where causality is not independently verified, treat as operator hypothesis | none (ledger label) | [Lap 01 prompt](prompts/lap-01-prompts.json); [per-case data](analysis-data.json) |

**Explanation:** All 20 had no usable code; output budget consumed by thinking; no execution. **Adjustment:** Initial untuned prompt/decoder configuration; test initial code generation. Frozen original source and synthetic evaluator; no weight training. **Measured before/after:** Initial baseline; no improvement claim. Runtime differences are descriptive, not controlled effort comparisons. **Decision:** Stop and change inference constraints; no usable baseline.

### Synthetic lap 02 — Increase context/output limits and disable thinking to obtain executable code.

| Field | Recorded finding |
|---|---|
| ID / date / attempt / status | `lap-02`; individual run date not published; attempt 1 per case; 0/20 pass |
| Model, prompt and decoding | `qwen3.5:9b` / `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`; [archived prompt](prompts/lap-02-prompts.json); 8192 context, 4096 output, temperature 0, thinking off, presence penalty not explicitly overridden |
| Dataset / held-out status | Synthetic cases 000–019; five correlated families; **same reused development fixtures**, not held out |
| Objective / change / why | Increase context/output limits and disable thinking to obtain executable code. |
| First-try synthetic; real | **0/20**; independent real **not run** in this lap |
| Severe regression / repair / fallback | Ledger severe flag: **0**; no within-case synthetic repair; Codex fallback **not recorded** |
| Runtime, compute and cost | Model+oracle p50/p95 **41.2/57.3 s across all cases**; tokens input/output **6124/13384**; RAM, VRAM, monetary cost and human effort **not measured** |

| Failed case/frame | Expected vs actual | Recorded failure category | Cause status | Severity | Reproduction/evidence |
|---|---|---|---|---|---|
| `000, 001, 002, 003, 004, 005, 006, 007, 008, 009, 010, 011, 015, 016, 017, 018, 019` | Expected a valid deform-weight normalization preserving protected data; observed `blocked`: Builder exited before a usable fresh verification result; see the attributed diagnosis in this section. | `evaluator / none` (original recorded category/severity) | See diagnosis; where causality is not independently verified, treat as operator hypothesis | none (ledger label) | [Lap 02 prompt](prompts/lap-02-prompts.json); [per-case data](analysis-data.json) |
| `012` | Expected a valid deform-weight normalization preserving protected data; observed `fail`: Verifier rejected deform-weight normalization. | `deformation / major` (original recorded category/severity) | See diagnosis; where causality is not independently verified, treat as operator hypothesis | major (ledger label) | [Lap 02 prompt](prompts/lap-02-prompts.json); [per-case data](analysis-data.json) |
| `013, 014` | Expected a valid deform-weight normalization preserving protected data; observed `not_run`: No usable proposal code; candidate not executed. | `invalid_output / none` (original recorded category/severity) | See diagnosis; where causality is not independently verified, treat as operator hypothesis | none (ledger label) | [Lap 02 prompt](prompts/lap-02-prompts.json); [per-case data](analysis-data.json) |

**Explanation:** Object/Mesh ownership, Blender weight-method and membership mistakes; two no-code outputs, one normalization failure. **Adjustment:** Increase context/output limits and disable thinking to obtain executable code. Frozen original source and synthetic evaluator; no weight training. **Measured before/after:** 0/20 → 0/20; format improved, pass count unchanged. Runtime differences are descriptive, not controlled effort comparisons. **Decision:** Continue with documented API guidance.

### Synthetic lap 03 — Add documented Blender API guidance and set presence_penalty=0 to correct API misuse.

| Field | Recorded finding |
|---|---|
| ID / date / attempt / status | `lap-03`; individual run date not published; attempt 1 per case; 19/20 pass |
| Model, prompt and decoding | `qwen3.5:9b` / `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`; [archived prompt](prompts/lap-03-prompts.json); 8192 context, 4096 output, temperature 0, thinking off, presence penalty 0 |
| Dataset / held-out status | Synthetic cases 000–019; five correlated families; **same reused development fixtures**, not held out |
| Objective / change / why | Add documented Blender API guidance and set presence_penalty=0 to correct API misuse. |
| First-try synthetic; real | **19/20**; independent real **not run** in this lap |
| Severe regression / repair / fallback | Ledger severe flag: **0**; no within-case synthetic repair; Codex fallback **not recorded** |
| Runtime, compute and cost | Model+oracle p50/p95 **31.0/43.5 s across all cases**; tokens input/output **14064/10661**; RAM, VRAM, monetary cost and human effort **not measured** |

| Failed case/frame | Expected vs actual | Recorded failure category | Cause status | Severity | Reproduction/evidence |
|---|---|---|---|---|---|
| `007` | Expected a valid deform-weight normalization preserving protected data; observed `blocked`: Builder exited before a usable fresh verification result; see the attributed diagnosis in this section. | `evaluator / none` (original recorded category/severity) | See diagnosis; where causality is not independently verified, treat as operator hypothesis | none (ledger label) | [Lap 03 prompt](prompts/lap-03-prompts.json); [per-case data](analysis-data.json) |

**Explanation:** Case 007: unsupported collection-length attribute; 19 other cases passed. **Adjustment:** Add documented Blender API guidance and set presence_penalty=0 to correct API misuse. Frozen original source and synthetic evaluator; no weight training. **Measured before/after:** 0/20 → 19/20 (+95 percentage points), multiple variables changed. Runtime differences are descriptive, not controlled effort comparisons. **Decision:** Retain as development candidate; attribution not isolated.

### Synthetic lap 04 — Repeat identical prompt and settings to test stability.

| Field | Recorded finding |
|---|---|
| ID / date / attempt / status | `lap-04`; individual run date not published; attempt 1 per case; 19/20 pass |
| Model, prompt and decoding | `qwen3.5:9b` / `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`; [archived prompt](prompts/lap-04-prompts.json); 8192 context, 4096 output, temperature 0, thinking off, presence penalty 0 |
| Dataset / held-out status | Synthetic cases 000–019; five correlated families; **same reused development fixtures**, not held out |
| Objective / change / why | Repeat identical prompt and settings to test stability. |
| First-try synthetic; real | **19/20**; independent real **not run** in this lap |
| Severe regression / repair / fallback | Ledger severe flag: **0**; no within-case synthetic repair; Codex fallback **not recorded** |
| Runtime, compute and cost | Model+oracle p50/p95 **30.5/43.0 s across all cases**; tokens input/output **14064/10661**; RAM, VRAM, monetary cost and human effort **not measured** |

| Failed case/frame | Expected vs actual | Recorded failure category | Cause status | Severity | Reproduction/evidence |
|---|---|---|---|---|---|
| `007` | Expected a valid deform-weight normalization preserving protected data; observed `blocked`: Builder exited before a usable fresh verification result; see the attributed diagnosis in this section. | `evaluator / none` (original recorded category/severity) | See diagnosis; where causality is not independently verified, treat as operator hypothesis | none (ledger label) | [Lap 04 prompt](prompts/lap-04-prompts.json); [per-case data](analysis-data.json) |

**Explanation:** Case 007 repeated the unchanged builder-stage failure. **Adjustment:** Repeat identical prompt and settings to test stability. Frozen original source and synthetic evaluator; no weight training. **Measured before/after:** 19/20 → 19/20 (0 pp); all 20 outputs matched. Runtime differences are descriptive, not controlled effort comparisons. **Decision:** Repeat for reproducibility, not as independent validation.

### Synthetic lap 05 — Repeat identical prompt and settings to confirm repeated failure.

| Field | Recorded finding |
|---|---|
| ID / date / attempt / status | `lap-05`; individual run date not published; attempt 1 per case; 19/20 pass |
| Model, prompt and decoding | `qwen3.5:9b` / `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`; [archived prompt](prompts/lap-05-prompts.json); 8192 context, 4096 output, temperature 0, thinking off, presence penalty 0 |
| Dataset / held-out status | Synthetic cases 000–019; five correlated families; **same reused development fixtures**, not held out |
| Objective / change / why | Repeat identical prompt and settings to confirm repeated failure. |
| First-try synthetic; real | **19/20**; independent real **not run** in this lap |
| Severe regression / repair / fallback | Ledger severe flag: **0**; no within-case synthetic repair; Codex fallback **not recorded** |
| Runtime, compute and cost | Model+oracle p50/p95 **30.4/42.3 s across all cases**; tokens input/output **14064/10661**; RAM, VRAM, monetary cost and human effort **not measured** |

| Failed case/frame | Expected vs actual | Recorded failure category | Cause status | Severity | Reproduction/evidence |
|---|---|---|---|---|---|
| `007` | Expected a valid deform-weight normalization preserving protected data; observed `blocked`: Builder exited before a usable fresh verification result; see the attributed diagnosis in this section. | `evaluator / none` (original recorded category/severity) | See diagnosis; where causality is not independently verified, treat as operator hypothesis | none (ledger label) | [Lap 05 prompt](prompts/lap-05-prompts.json); [per-case data](analysis-data.json) |

**Explanation:** Case 007 still invoked unsupported collection-length attribute. **Adjustment:** Repeat identical prompt and settings to confirm repeated failure. Frozen original source and synthetic evaluator; no weight training. **Measured before/after:** 19/20 → 19/20 (0 pp); all 20 outputs matched. Runtime differences are descriptive, not controlled effort comparisons. **Decision:** Change targeted guidance on next lap.

### Synthetic lap 06 — Add collection-length, sparse-assignment and modified-count guidance.

| Field | Recorded finding |
|---|---|
| ID / date / attempt / status | `lap-06`; individual run date not published; attempt 1 per case; 7/20 pass |
| Model, prompt and decoding | `qwen3.5:9b` / `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`; [archived prompt](prompts/lap-06-prompts.json); 8192 context, 4096 output, temperature 0, thinking off, presence penalty 0 |
| Dataset / held-out status | Synthetic cases 000–019; five correlated families; **same reused development fixtures**, not held out |
| Objective / change / why | Add collection-length, sparse-assignment and modified-count guidance. |
| First-try synthetic; real | **7/20**; independent real **not run** in this lap |
| Severe regression / repair / fallback | Ledger severe flag: **0**; no within-case synthetic repair; Codex fallback **not recorded** |
| Runtime, compute and cost | Model+oracle p50/p95 **32.0/70.6 s across all cases**; tokens input/output **16784/11906**; RAM, VRAM, monetary cost and human effort **not measured** |

| Failed case/frame | Expected vs actual | Recorded failure category | Cause status | Severity | Reproduction/evidence |
|---|---|---|---|---|---|
| `000, 004, 005, 006, 007, 008, 011, 012, 013, 015, 017, 018, 019` | Expected a valid deform-weight normalization preserving protected data; observed `blocked`: Builder exited before a usable fresh verification result; see the attributed diagnosis in this section. | `evaluator / none` (original recorded category/severity) | See diagnosis; where causality is not independently verified, treat as operator hypothesis | none (ledger label) | [Lap 06 prompt](prompts/lap-06-prompts.json); [per-case data](analysis-data.json) |

**Explanation:** Thirteen builder failures from integer-membership and vertex-group confusion. **Adjustment:** Add collection-length, sparse-assignment and modified-count guidance. Frozen original source and synthetic evaluator; no weight training. **Measured before/after:** 19/20 → 7/20 (−60 pp); no causal ablation. Runtime differences are descriptive, not controlled effort comparisons. **Decision:** Revise/revert wording; this intervention regressed.

### Synthetic lap 07 — Remove unrelated guidance; simplify length advice to plain Python.

| Field | Recorded finding |
|---|---|
| ID / date / attempt / status | `lap-07`; individual run date not published; attempt 1 per case; 14/20 pass |
| Model, prompt and decoding | `qwen3.5:9b` / `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`; [archived prompt](prompts/lap-07-prompts.json); 8192 context, 4096 output, temperature 0, thinking off, presence penalty 0 |
| Dataset / held-out status | Synthetic cases 000–019; five correlated families; **same reused development fixtures**, not held out |
| Objective / change / why | Remove unrelated guidance; simplify length advice to plain Python. |
| First-try synthetic; real | **14/20**; independent real **not run** in this lap |
| Severe regression / repair / fallback | Ledger severe flag: **0**; no within-case synthetic repair; Codex fallback **not recorded** |
| Runtime, compute and cost | Model+oracle p50/p95 **33.7/49.0 s across all cases**; tokens input/output **15844/11288**; RAM, VRAM, monetary cost and human effort **not measured** |

| Failed case/frame | Expected vs actual | Recorded failure category | Cause status | Severity | Reproduction/evidence |
|---|---|---|---|---|---|
| `005` | Expected a valid deform-weight normalization preserving protected data; observed `fail`: Verifier rejected deform-weight normalization. | `deformation / major` (original recorded category/severity) | See diagnosis; where causality is not independently verified, treat as operator hypothesis | major (ledger label) | [Lap 07 prompt](prompts/lap-07-prompts.json); [per-case data](analysis-data.json) |
| `008, 010, 012, 018, 019` | Expected a valid deform-weight normalization preserving protected data; observed `blocked`: Builder exited before a usable fresh verification result; see the attributed diagnosis in this section. | `evaluator / none` (original recorded category/severity) | See diagnosis; where causality is not independently verified, treat as operator hypothesis | none (ledger label) | [Lap 07 prompt](prompts/lap-07-prompts.json); [per-case data](analysis-data.json) |

**Explanation:** Case 005 normalization fail; 008/010/012/018/019 blocked by API/membership errors. **Adjustment:** Remove unrelated guidance; simplify length advice to plain Python. Frozen original source and synthetic evaluator; no weight training. **Measured before/after:** 7/20 → 14/20 (+35 pp) on reused cases. Runtime differences are descriptive, not controlled effort comparisons. **Decision:** Refine vertex/group/assignment explanation.

### Synthetic lap 08 — Explicitly distinguish vertex IDs, group IDs and vertex-group membership assignments.

| Field | Recorded finding |
|---|---|
| ID / date / attempt / status | `lap-08`; individual run date not published; attempt 1 per case; 20/20 pass |
| Model, prompt and decoding | `qwen3.5:9b` / `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`; [archived prompt](prompts/lap-08-prompts.json); 8192 context, 4096 output, temperature 0, thinking off, presence penalty 0 |
| Dataset / held-out status | Synthetic cases 000–019; five correlated families; **same reused development fixtures**, not held out |
| Objective / change / why | Explicitly distinguish vertex IDs, group IDs and vertex-group membership assignments. |
| First-try synthetic; real | **20/20**; independent real **not run** in this lap |
| Severe regression / repair / fallback | Ledger severe flag: **0**; no within-case synthetic repair; Codex fallback **not recorded** |
| Runtime, compute and cost | Model+oracle p50/p95 **30.9/37.7 s across all cases**; tokens input/output **17944/9870**; RAM, VRAM, monetary cost and human effort **not measured** |

| Failed case/frame | Expected vs actual | Recorded failure category | Cause status | Severity | Reproduction/evidence |
|---|---|---|---|---|---|
| None | 20/20 development fixtures verified under synthetic oracle | None observed | Not applicable | None observed in this lap | [Per-case data](analysis-data.json) |

**Explanation:** No synthetic failure; transfer to distinct real hair repair not established. **Adjustment:** Explicitly distinguish vertex IDs, group IDs and vertex-group membership assignments. Frozen original source and synthetic evaluator; no weight training. **Measured before/after:** 14/20 → 20/20 (+30 pp) on reused cases. Runtime differences are descriptive, not controlled effort comparisons. **Decision:** Retain as development observation only; test on independent real fixtures.

### Real trial 01 — independent first attempt

| Field | Recorded finding |
|---|---|
| ID / date / status | `real-primary-01`; run date not published; independent first attempt **failed** |
| Model / prompt / settings | `qwen3.5:9b` / `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`; [frozen primary prompt](prompts/real-first-attempt-prompt.txt); temperature 0, context 8192, output 4096, thinking off, seed 0, presence_penalty 0, repeat_penalty 1, JSON |
| Dataset / IDs | One private source character and pre-repair Stage02 checkpoint; identifiers redacted publicly; **not a new synthetic fixture** |
| Change and intended mechanism | Transfer successful development-set API prompting to independent repair of hair self-shadow while preserving protected character content |
| First-try passes | **0/1** real; synthetic comparison **not applicable** |
| Severe regressions / fallback | Protected original remained unchanged; no additional verified repair; Codex fallback execution **not recorded** |
| Compute and time | 980 input / 1,391 output tokens; 92.94 s inference / 178.73 s total; RAM/VRAM, full Codex effort baseline **not measured** |

| Failed case/frame | Expected vs actual | Failure category | Confirmed cause or hypothesis | Severity | Evidence |
|---|---|---|---|---|---|
| One private real source | Expected actual self-shadow repair and preservation; valid derivative had **no repair**, verifier rejected it | Context-selection and functional failure | **Observed:** active root was EMPTY; guard returned zero before repair body. Possible faults in unreached code are not observed crashes | Material task failure, not a verified protected-source regression | [Redacted prompt](prompts/real-first-attempt-prompt.txt); [analysis](analysis-notes.md); private verifier/logs withheld |

**Decision:** Real transfer failed; do not promote candidate or count review renders as a human approval.

### Real trial 02 — explicitly feedback-assisted final retry

| Field | Recorded finding |
|---|---|
| ID / date / status | `real-assisted-final-02`; date not published; **failed proposal validation**, not a fresh independent case |
| Model / prompt / settings | Same model/digest and decoding as trial 01; [assisted prompt](prompts/real-final-assisted-prompt.txt) |
| Dataset / change / why | **Same** private real character. Added explicit instruction to target named mesh rather than active EMPTY to address confirmed context failure |
| First-try score; offline retry | Independent first-try denominator **unchanged at 0/1**; separately recorded retry **0/1** |
| Execution, regressions and fallback | JSON was incomplete; **zero candidate executions**, hence no Blender verifier or render acceptance for retry; source/model integrity unchanged; Codex fallback not recorded |
| Compute and time | 1,009 input / 4,096 output tokens; 272.38 s inference / 285.08 s total; RAM/VRAM and cost unavailable |

| Failed case/frame | Expected vs actual | Failure category | Confirmed cause or hypothesis | Severity | Evidence |
|---|---|---|---|---|---|
| Same private real source | Expected valid repair script, got truncated JSON string at output limit | Invalid output / output-budget exhaustion | **Observed:** `done_reason=length`, 4,096 output tokens, repeated planning comments; why the model failed to finish is not established beyond length exhaustion | Unusable proposal; Blender not run | [Assisted prompt](prompts/real-final-assisted-prompt.txt); [analysis](analysis-notes.md) |

**Measured before/after:** The mesh targeting instruction appeared in partial text, but usable real results remained **0/1 → 0/1**. **Decision:** Stop, retain frozen primary score, and require new independent cases for further qualification.

## 4. Specialization Effectiveness

| Metric | Untuned lap 01 | Specialized development lap 08 | Absolute / relative change | Comparable? |
|---|---|---|---|---|
| Synthetic first-try pass | 0/20 | 20/20 | **+20 passes; +100 percentage points**; relative percentage undefined (zero baseline) | **Same reused fixtures**, but prompts **and decoding** changed |
| Real-workflow success | Not run | 0/1 primary trial (separate task) | **Cannot calculate** | **No**, different task and split |
| Severe regressions | 0 recorded | 0 recorded | 0 observed | Same narrow synthetic checks only |
| Repairs / fallback | No synthetic repairs logged; fallback unknown | No synthetic repairs logged; real assisted retry failed | Not comparable | No matched controlled fallback measure |
| Time per verified success | Undefined, zero passes | Not measured as true end-to-end; 30.9/37.7 s all-case p50/p95 | No valid delta | No successful baseline |
| RAM / VRAM | Not recorded | Not recorded | Not measured | No |

**Interpretation:** This is inference-time prompt/decoder specialization, **not** weight tuning. The apparent 0/20→20/20 gain is on repeatedly inspected development fixtures with multiple simultaneous changes; it cannot establish causal attribution, independent transfer or absence of overfitting. Development success did not carry over to real repair. The marginal specialization cost versus Codex remains unmeasured.


The synthetic baseline had 0/20 usable passes; lap 8 reached 20/20 on the same cases after prompt and settings changes. Laps 3-5 repeated 19/20, lap 6 regressed, and lap 7 partly recovered. This demonstrates sensitivity to API guidance and wording within this development set. It does not demonstrate learning in the weights, independent generalization, or stable real-character competence.

The real first attempt failed on object context. The assisted retry reflected the mesh-selection instruction in incomplete text but failed to produce an executable repair. Thus the synthetic gate did not establish readiness for the distinct real hair-repair task. Other tasks, canaries, independent validation and untouched holdouts were not measured here. No cross-model conclusion is made.

## 5. Workflow Integration, Reliability and Safety

| Required workflow gate | Actual evidence | Pass/fail/not run |
|---|---|---|
| Proposal generation | 160 synthetic first attempts plus two separate real proposals | Recorded; real assisted proposal malformed |
| Sandboxed credential-free execution on disposable input | Synthetic bounded Blender builder/oracle; real first script ran in bubblewrap-based local isolation; second real script not executed; read-only originals | Observed for executed candidates; **not run** for assisted retry |
| Deterministic oracle checks | Synthetic per-case verdicts, first real fresh structural verifier | Development lap 08 **pass 20/20**; real primary **fail** |
| Independent Sol Light review | Subagent effort did not complete due usage constraints; no review result | **Not run / not obtained** |
| Codex fallback | Required in project workflow; no fallback work logged for these trials | **Not measured / not executed in reported trials** |
| Human stage gate and immutable checkpoint | No reported human artistic approval; originals and model blobs verified unchanged | Human gate **not obtained**; source integrity checked |
| Unauthorized modifications / network / crashes | Sandboxed candidate, read-only sources, no candidate direct host execution; source and model integrity records | Scoped checks passed; not a proof of complete isolation or zero unknown risks |
| Clean stock Blender; external deps; Cycles-only final render acceptance | Current installed Blender used; candidate real views do not constitute accepted Cycles-only independent review | **Not proven / not accepted** |

**Threshold application:** Exploratory synthetic threshold (≥15/20 first-try and zero severe) was met on some development laps; the additional **≤35% Codex effort** condition was **not measured**, so the complete exploratory go/no-go is **not established**. Production specialist qualification (≥300 independent held-out examples per stage, zero observed failures, independent Sol Light and human gates) is **not met**. The review-ledger >10% repair/rejection escalation should be evaluated against an explicitly defined logged denominator; these exploratory results are not a substitute for that ledger.


Generated scripts were never executed directly on the host. The primary real candidate ran in the existing isolated local Blender sandbox; it was not run in a Blender Docker image. Input assets were read-only, the private reference was unavailable to candidate code, and snapshot/verifier processes were separate from candidate execution. The final retry was rejected before any sandbox execution.

Original assets and qualified model blobs verified unchanged after both real trials. The final retry preserved the original first-attempt result, common prompt and frozen contract. The controller finished, Qwen was unloaded and no further attempt was automatically scheduled.

The retained setup evidence records 103 passing tests, stable repeated reference snapshots, two accepted positive controls, seven rejected negative scene controls and seven passing boundary/artifact/lifecycle probes. These bounded checks do not prove immunity to unknown application or operating-system vulnerabilities. An independent subagent implementation/review did not complete because of usage limits; no completed independent review is claimed. Human artistic acceptance and production approval were not obtained.

This sanitized report and the separately labeled per-lap prompt archive are published. Local usernames, absolute filesystem paths, machine/network identifiers, source-character identifiers, asset fingerprints, checkpoints, textures, renders, private manifests, raw outputs, logs and operational sandbox details are excluded from this report. The accompanying archive publishes exact synthetic prompts and redacted real-character prompts. The private original reports and evidence are retained locally.

## 6. Miscellaneous Findings and Future Model Analysis

| Standard finding category | Observed finding / limitation |
|---|---|
| Unexpected success/failure | Development lap 08 20/20 but real primary 0/1; unrelated geometry tasks were not interchangeable |
| Prompt/template sensitivity | Laps 03–05 identical case outputs and failure; lap 06 wording regressed to 7/20; lap 08 explanatory clarification recovered 20/20 |
| Quantization / reasoning mode | Q4_K_M observed; lap 01 thinking consumed output budget; disabling thinking improved completion but did not alone produce passes |
| Blender API compatibility | Unsupported collection length, object/Mesh ownership, group membership and active-root assumptions seen; Blender 5.2.2 used |
| Bone names and retarget maps | **Not measured** for this Stage 03 geometry experiment |
| Stage 04 pole/IK | **Not assessed**; no Stage 04 advancement authorized by Stage 03 synthetic score |
| Data coverage, licenses, source-family leakage | 20 reused synthetic cases from five families; unique real character one; private asset license/source split cannot be reproduced publicly |
| Deformation/geometry/motion/face | Synthetic weights checked; real shadow repair failed; motion/face/keyed frames not independently scored |
| Hardware/runtime | 4,096/8,192 tested context, timing and token metadata captured; RAM/VRAM/cache and Codex effort not fully measured |
| Repeatability/evaluator limitations | Repeated identical output on laps 03–05; private real verifier and assets withheld; synthetic oracle covers only a narrow task |
| Transferable future work | New independent source-family fixtures, object-context checks, early JSON validation, clean-stock Blender tests, controlled ablations |

**Reproducibility manifest:** Model tag/digest `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`; native-template SHA-256 `b507b9c2f6ca642bffcd06665ea7c91f235fd32daeefdf875a0f938db05fb315`; quantization GGUF Q4_K_M; stage reference/runner revisions and local private source checkpoint **not publicly pinned**; explicit per-lap requests and safe prompt text [archived](prompts/README.md); 160 per-case synthetic outcomes [retained](analysis-data.json); original public files [checksummed](SHA256SUMS). Synthetic fixture IDs 000–019, five families; exact raw private scene/asset hashes, licensed source provenance, full logs, candidate code, renders, independent reviewer evidence, complete machine details and exact real reproduction commands **withheld or not recorded**. Public redacted prompt hashes do **not** identify private original prompts. GGUF file/adapter digest beyond the pinned model digest **not recorded**. No public attestation of independent replay is claimed.


Synthetic evidence was reverified before export: 328 hash-chained events, 160 attempts and 160 recorded verdicts. The eight saved status summaries agree with freshly computed counts. Each lap has 20 generic synthetic cases and five families. Verdict records mark isolation verified, including not-run records; that field does not imply every proposal reached Blender. No decision events were recorded.

The real adapter stores separate controller, builder, fresh-snapshot and verifier evidence; its trials were not added to the synthetic ledger. Their values here come from the retained real-trial records. The final retry records `done_reason: length`, exactly 4,096 output tokens and zero sandbox execution records. Both before/after model-integrity records match. The primary prompt/contract/status hashes also remained unchanged.

Exact synthetic prompt text and request settings are available in the accompanying archive. Real-character reproducibility remains limited because identifying prompt details are redacted and private assets, manifests and raw evidence are withheld. No independent public reproduction or cryptographic attestation is claimed. The hash chain detects inconsistencies in saved data but is not a tamper-proof audit system. A finalized report does not imply an accepted model result.

## 7. Final Verdict

| Verdict field | Evidence-based disposition |
|---|---|
| Readiness | **Experimental** on Stage 03 synthetic development; **not production-qualified** and failed observed primary real task |
| Within-model quality | 0/20 untuned lap 01 → 20/20 lap 08 on reused synthetic fixtures; real 0/1; Codex comparison **not measured** |
| Best lap | **Lap 08 is the highest observed development result only.** No validation-selected best lap (`best_lap_id=null`) |
| Remaining faults | Real active-object/mesh selection failure (observed); assisted output length/JSON failure (observed); unknown independent transfer and human/Cycles approval |
| Next action | Retain data; **retest** with untouched real sources and valid output controls; do not substitute for Codex or advance stage gate |
| Evidence confidence | 160 repeated synthetic attempts on **20 unique reused fixtures** and one unique real character; no 300+ untouched source families; no production guarantee |
| Human decision | **Not yet obtained**; no implicit approval from report finalization or synthetic 20/20 |


**Development-only evidence; real-character repair unsuccessful; not production qualified.** The retained synthetic observations meet the numerical pilot pass threshold in laps 3-5 and 8. The distinct real primary score remains 0/1, and the final assisted trial is separately unsuccessful at proposal validation.

The synthetic ledger's readiness remains level 2 (verified synthetic observations). Separate unsuccessful real-asset evidence now exists; it does not automatically advance the ledger's readiness or grant production status. Validation-based model selection, sufficient independent real cases and source families, both animation tracks, exact-scope independent review, human acceptance and a measured cost/effort baseline remain unmet or unmeasured. Reused development cases cannot satisfy those requirements.

Capability rows below are sanitized summaries, not approval certificates. `best_lap_id` remains null because there was no validation split. Lap 8 is an observed development result only. The assisted retry is excluded from the primary capability row.

```json
[
  {
    "task_id": "geometry_weight_normalize",
    "model_digest": "56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90",
    "best_lap_id": null,
    "development_observation_lap": "lap-08",
    "first_try_pass_count": 20,
    "n": 20,
    "uncertainty": "Wilson 95%: 84-100%; reused development cases",
    "trusted_scope": "synthetic development only",
    "evidence_ref": "#2-performance-quality-and-benchmark-results"
  },
  {
    "task_id": "real_character_hair_repair",
    "model_digest": "56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90",
    "best_lap_id": null,
    "first_try_pass_count": 0,
    "n": 1,
    "uncertainty": "one character; generalization not established",
    "trusted_scope": "unsuccessful primary real-asset attempt",
    "evidence_ref": "#3-lap-by-lap-failure-and-adjustment-analysis"
  }
]
```

No model candidate was promoted over an approved checkpoint. No further lap is running or scheduled.
