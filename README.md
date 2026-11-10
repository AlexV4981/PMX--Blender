# PMX to native Blender skills — version 3

Eleven skills for PMX anime character conversion with a lightweight, human-reviewed Cycles-only workflow. The ten stage handoffs remain. Each stage uses essential checks and a short Cycles demonstration, expanding diagnosis or mathematical fitting only for an observed or uncertain fault.

## Explore the project by workstream

The `main` branch contains the shared **11-skill, human-reviewed Cycles pipeline**. The branches below hold separate experiments and optimizations; their features and results are **not automatically part of `main`**. This index is a snapshot of the workstreams as of **2026-11-10**. Follow each link for its current state.

| Branch / workstream | What's being developed or evaluated | Start with |
| --- | --- | --- |
| **[`main`](https://github.com/AlexV4981/PMX--Blender/tree/main)** — baseline pipeline | Staged PMX-to-native-Blender workflow, verification gates, Cycles-only evidence, and audit/delivery checks. | [Stage skills](skills/) · [Workflow comparison](WORKFLOW_COMPARISON.md) |
| **[`Multi-Model-PMX-Benchmark`](https://github.com/AlexV4981/PMX--Blender/tree/Multi-Model-PMX-Benchmark)** — local AI model experiments | Stage 03 model evaluations covering **Qwen3.5 9B, Ministral 3 8B, Phi4 14B, Gemma4 12B, and Granite 4.2 8B**; prompts, per-model reports, synthetic vs. real-test evidence, errors, and fallback decisions. Later-stage specialist work is experimental. | [Five model report packages](https://github.com/AlexV4981/PMX--Blender/tree/Multi-Model-PMX-Benchmark/final_reports_stage03) · [Evaluation/reporting standard](https://github.com/AlexV4981/PMX--Blender/blob/Multi-Model-PMX-Benchmark/MODEL_REPORT_STANDARD.md) · [Workflow](https://github.com/AlexV4981/PMX--Blender/blob/Multi-Model-PMX-Benchmark/MULTI_MODEL_WORKFLOW.md) |
| **[`Pipeline-Optimization`](https://github.com/AlexV4981/PMX--Blender/tree/Pipeline-Optimization)** — tool-first conversion | Simplifies **fully human** character construction using MMD Tools and Rigify before custom Blender solutions. Updates the stage skills while retaining human approval and quality gates. Animal/kemonomimi features and live-asset qualification remain outside the demonstrated scope. | [Construction route](https://github.com/AlexV4981/PMX--Blender/blob/Pipeline-Optimization/skills/anime-blender-pipeline/references/construction.md) · [Branch README](https://github.com/AlexV4981/PMX--Blender/blob/Pipeline-Optimization/README.md) |
| **[`Qwen-Local-Helper`](https://github.com/AlexV4981/PMX--Blender/tree/Qwen-Local-Helper)** — earlier local specialist workbench | Local Qwen coding-helper experiments, Stage 03–06 synthetic pilot fixtures and Blender oracles, bounded task routing, training-workbench scaffolding, and Codex fallback. Pilot work is **not** evidence of a production-qualified specialist. | [Local model lab](https://github.com/AlexV4981/PMX--Blender/blob/Qwen-Local-Helper/astra-qwen-weight-lab/README.md) · [Training workbench](https://github.com/AlexV4981/PMX--Blender/blob/Qwen-Local-Helper/qwen-helper/training-workbench/README.md) |

**Historical reference branches:** [`archive/Qwen-Local-Helper-2026-11-05`](https://github.com/AlexV4981/PMX--Blender/tree/archive/Qwen-Local-Helper-2026-11-05) preserves the earlier local-helper work (currently the same revision as `Qwen-Local-Helper`); [`codex/blender-diagnostic-rewrite-v2`](https://github.com/AlexV4981/PMX--Blender/tree/codex/blender-diagnostic-rewrite-v2) is an older pipeline revision now superseded by `main`.

### AI engineering evidence: quickest route for reviewers

1. **What was evaluated?** [Stage 03 candidate reports and reproducibility attachments](https://github.com/AlexV4981/PMX--Blender/tree/Multi-Model-PMX-Benchmark/final_reports_stage03) include individual model results and prompt/analysis artifacts.
2. **How were results judged?** The [reporting standard](https://github.com/AlexV4981/PMX--Blender/blob/Multi-Model-PMX-Benchmark/MODEL_REPORT_STANDARD.md) requires first-try vs. repaired outcomes, synthetic vs. independent real tests, regressions, failure analysis, and explicit evidence gaps.
3. **How are changes controlled?** The [pipeline optimization branch](https://github.com/AlexV4981/PMX--Blender/tree/Pipeline-Optimization) and the [baseline review process](WORKFLOW_COMPARISON.md) retain staged acceptance checks and human decisions rather than treating model output as approved automatically.

**Scope and attribution:** This is an AI-assisted, human-directed engineering and evaluation project. Coding agents help produce implementation and proposals; specifications, tests, review gates, and measured outcomes determine whether work is accepted. Experimental fixtures, reported test passes, and model comparisons do **not** establish an end-to-end conversion success or production readiness. Branches may differ in status and dependencies; do not combine their claims into a single deployed system.

## What changed

Reuse accepted camera/environment/color definitions while their dependencies match. Share one motion/face suite and rerun affected cases. Use a no-change integrity report when geometry needs no repair. Keep regional Delta E 00 measurements, explicit limits and human artistic critique.

Stage 09 now has two decisions: audit plus selected plan/disposition; final re-audit plus delivery and stage acceptance. The CLI applies final acceptance in the delivery operation, with current checks and submitted-bundle validation. No third approval question follows.

## Cycles-only scope

Use Cycles for all final renders, comparisons, review images and animation previews. Use the Cycles Rendered viewport (CYCLES / RENDERED), not Material Preview, for viewport evidence. No alternate-engine graph or external rendering path is built unless the user explicitly requests it. Pin viewport samples, denoising, device and resolution; freshly qualify the desired FPS goals rather than transferring an old preview-engine timing pass.

## Installation and version boundary

Copy all eleven directories inside skills/ into your Codex skills location as siblings, replacing matching older copies. The historical version-1 ZIP is not the current source. Keep originals and accepted checkpoints immutable.

Version 3 changes approval semantics and renderer requirements. Start a new run with explicit lineage; preserve version 1/2 runs and their original tools. Never edit a historical policy/version or copy its approvals. A correct earlier imported blend can be a new source with fresh affected review; another import is not automatically required.

## Maps and validation

[WORKFLOW_COMPARISON.md](WORKFLOW_COMPARISON.md) preserves the historical hierarchy and shows the active lighter hierarchy. [AUDIT.md](AUDIT.md) records the previous diagnosis and subsequent changes.

All eleven skills validate. Fifty-one utility tests pass, including 20 published CIEDE2000 cases and stage-09 CLI acceptance/stale-evidence checks. No live Blender/model/target-laptop qualification is claimed. Documented camera/IK/ARAP/PSD/preference/inverse-simulation solvers remain procedures or external options, not bundled Blender implementations. Numerical helpers require NumPy; the texture auditor additionally requires Pillow.

```sh
python3 -m unittest discover -s skills/anime-blender-pipeline/scripts/tests -v
python3 skills/anime-blender-pipeline/scripts/blender_tools.py validate-seeds
```
