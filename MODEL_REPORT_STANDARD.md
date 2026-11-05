# Standard: Individual PMX-to-Blender Model Evaluation Report

**Status:** Canonical report template for one model at a time on `Qwen-Local-Helper`. Version 1, 2026-11-05.

## Purpose and scope
Use this template for **every model family**, **each eligible stage (03–06)**, and **every lap**, including unsuccessful or abandoned laps. Produce a separate report for each individual model and specialization. **Do not add a cross-model comparison section**: that will be a separate, later analysis. A same-model untuned-versus-specialized comparison is required.

This is a reporting standard, **not** a change to the stage workflow, automated score logic, acceptance criteria, or historical approvals. Stage 00 remains Codex-only; 01/02/07/08/09 remain Codex-led. Use only disposable derivatives for experimental code. Original human gates, Cycles-only render evidence, independent Sol Light review and Codex fallback remain mandatory. Keep Stage 04 limited to the authorized left-arm pilot until pole placement is resolved.

Create one report per model/stage experiment, then append every lap. Do not overwrite past measurements. For each claim distinguish **observed**, **inferred**, and **not measured**.

## 1. Experiment summary

| Field | Value |
|---|---|
| Experiment ID and date | |
| Model family, exact Ollama tag, digest | |
| Parameter size / quantization | |
| Source base revision / adapter / checkpoint identity (if applicable) | |
| Stage (03 geometry / 04 rig / 05 ready / 06 motion tests) | |
| Narrow specialization objective | |
| Inference or training approach | |
| Blender version, Python, add-ons, machine, RAM/VRAM | |
| Number of laps attempted | |
| Overall result (pass / fail / inconclusive / blocked) | |
| Action (keep / improve / retest / reject / Codex fallback) | |

**Executive summary:** Describe actual task, observed output, strengths, failures, relevance to the intended stage, and status. Never equate a synthetic fixture result with a completed PMX conversion.

## 2. Stage performance and quality

| Metric | Observed result | Evidence / sample size |
|---|---|---|
| Synthetic Blender-oracle first-try passes / total | | |
| Independent real PMX/Blender passes / total | | |
| First-try pass rate | | |
| Separately labeled offline feedback-retry success (if permitted) | | |
| Severe regressions | | |
| Quality vs the **original Codex workflow** on comparable tasks | | |
| Runtime per successful task, wall time | | |
| Inference tokens, RAM and VRAM | | |
| Codex fallback frequency | | |
| Sol Light review; human stage decision (separate) | | |
| Motion/face ROM coverage and unsupported controls (when applicable) | | |

**Test quality:** State the oracle and checks, exact fixture families, keyed/interpolated frames, metrics and failures.

**Real application quality:** Describe actual Blender execution and PMX source-family held-out tests, evaluated deformation and rig functionality, with Cycles render evidence as required by stage.

**Synthetic-to-real gap:** Record cases passing synthetic evaluation but failing real motion, deformation, retargeting, clean-process or human usability tests. **Unknown** is not pass.

## 3. Lap-by-lap failure analysis

### Lap N — objective and configuration

| Field | Finding |
|---|---|
| Lap ID, date, attempt number and status | |
| Model tag/digest; prompt/Modelfile and settings | |
| Dataset/source-family split and exact test IDs | |
| Change vs previous lap and intended mechanism | |
| First-try passes / total; independent real tests | |
| Severe regressions; repair/fallback | |
| Compute, time, memory and cost | |

| Failed case/frame | Expected vs actual | Failure category | Confirmed cause or hypothesis | Severity | Reproduction / evidence |
|---|---|---|---|---|---|
| | | | | | |

**Failure explanation:** Identify where and why, separating confirmed root cause from plausible hypothesis (incorrect bpy/API calls; rig-space math; IK/FK; pole orientation; retarget axes; deformation; context loss; invalid JSON; tool/environment; evaluator flaw; dataset quality; quantization; resource limit).

**Adjustments:** Record *each* prompt, context, dataset, decoder, code, verifier, LoRA or other change; **why** it was made; what was frozen; and whether it was reverted.

**Measured before/after:** On comparable frozen tests, show delta for first-try quality, real applicability, severity, runtime and memory. State when the evidence is insufficient to claim an improvement.

**Lap decision:** Continue / revert / stop / blocked, with explanation. Preserve failed and abandoned laps in the chronology.

## 4. Specialization effectiveness (within the same model)

| Metric | Untuned baseline | Lap N | Absolute / relative change | Comparable? |
|---|---|---|---|---|
| Synthetic first-try pass | | | | |
| Real-workflow success | | | | |
| Severe regressions | | | | |
| Repairs / fallback rate | | | | |
| Time per verified success | | | | |
| RAM / VRAM | | | | |

Describe target stage skill, what improved, what regressed outside the intended scope, signs of memorization or synthetic overfitting, and whether additional specialization cost is justified. Do not report post-retry success as first-try performance.

## 5. Workflow integration and safety

Record **separately**: proposal generation; sandboxed/credential-free Blender execution on disposable input; deterministic oracle checks; real Sol Light review; Codex fallback; explicit human gate decision and immutable checkpoint identities. Check unauthorized file changes, network access, crashes, untrusted Python, external dependencies, clean stock Blender and Cycles-only evidence. Never infer actual review from a JSON flag. Document exact gate pass/fail/not-run.

Current lab **exploratory** go/no-go per stage: >=75% first-try verified passes on 20 seeded pilot cases, zero severe regressions, and local+review work <=35% of the original Codex effort. These 80 synthetic cases are **not** diverse production evidence. Production specialist qualification separately requires >=300 independent held-out examples **per stage**, zero observed failures, actual independent review and existing human gates. The project review ledger also escalates if repair/rejection rate is >10%. No benchmark creates an unconditional quality guarantee.

## 6. Miscellaneous findings and future analysis

| Finding category | Notes and evidence |
|---|---|
| Unexpected successes and failures | |
| Prompt/template sensitivity | |
| Quantization and reasoning-mode behavior | |
| Blender API/version incompatibilities | |
| PMX/VMD bone names and retarget maps | |
| Stage 04 pole/IK unknowns | |
| Training data coverage, licenses and source-family leakage | |
| Deformation, geometry, motion/face edge cases | |
| Hardware/cache/runtime bottlenecks | |
| Repeatability and evaluator weaknesses | |
| Potential future experiments / transferable learnings | |

Reproducibility attachment manifest: model + GGUF + adapter digests, commits, prompts, temperature/context/token limits, stage reference version, data licenses/provenance/split hashes, fixtures/seed, scripts, raw responses, Blender logs, oracle outcomes, frame IDs, contact sheets/renders, reviewer evidence and exact commands. Keep proprietary/large raw assets out of public Git and never fabricate unavailable evidence.

## 7. Final verdict

- **Readiness:** qualified / experimental / rejected / blocked.
- **Within-model quality:** current lap vs untouched same-model baseline and original workflow (not another candidate-model ranking).
- **Best lap:** configuration, supporting evidence, limitations.
- **Remaining faults:** severity, observed reproduction and owner-stage routing.
- **Next action:** retain / retest / specialize / revert / Codex fallback.
- **Evidence confidence:** n tested, real independent families, untested situations and confidence caveats.
- **Human decision:** exact observed decision or **not yet obtained**.

**Non-negotiable reporting rule:** For every lap, answer: *what changed, why, where did it fail, did the change measurably improve this stage, and what should future model analysis learn?*
