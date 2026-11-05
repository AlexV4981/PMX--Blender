# PMX to native Blender skills — version 3

Eleven skills for PMX anime character conversion with a lightweight, human-reviewed Cycles-only workflow. The ten stage handoffs remain. Each stage uses essential checks and a short Cycles demonstration, expanding diagnosis or mathematical fitting only for an observed or uncertain fault.

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

## Model benchmark reporting and humanoid motion qualification

- **Required individual-model report format:** [MODEL_REPORT_STANDARD.md](MODEL_REPORT_STANDARD.md). Use its seven sections for every model, stage and lap, including failed experiments. Compare a model against its own baseline and the original workflow; reserve cross-model analysis for a separate later report.
- **PMX and native Blender full-motion testing research:** [MOTION_QUALIFICATION_RESOURCES.md](MOTION_QUALIFICATION_RESOURCES.md). Controlled joint-range sweeps plus rights-cleared real human mocap supplement the existing Stage 04–06 checks; the document is a research/fixture plan, not evidence of tested assets.

## Optional local Qwen maintenance assistant

For bounded, **project-specific** coding chores only, see [Qwen Local Helper](qwen-helper/README.md). Codex can configure it on this branch; Qwen never substitutes for the generic PMX conversion workflow or human approval. Keep character-specific exceptions in each run's profile and opt-in adapters, not in the shared default pipeline.

### Experimental local specialist routing (this branch only)

Read [Qwen specialist setup and qualification](qwen-helper/SPECIALISTS.md). Separate QLoRA specialists have fail-closed eligibility and require independent held-out testing plus an actual Sol Light review. Any ineligible or rejected task returns to the unchanged Codex pipeline. Models ship **unqualified**; no performance or installation is assumed. This does not change `main` or human approval gates.

### Stage-ordered local specialist training workbench

A separate [training workbench](qwen-helper/training-workbench/README.md) maps **00 Setup → 01 Import → 02 Materials/Cycles → 03 Geometry → 04 Rig → 05 Animation Ready → 06 Motion Tests → 07 Final Look → 08 Physics → 09 Audit/Delivery** to bounded read-only support jobs. The runnable `workbench.py` can bootstrap ignored training directories and prepare group-separated training/validation/holdout examples; specialists remain unqualified until independently verified. Stages 08–09 remain Codex-only. No change to the main branch, the original stage gates or Cycles requirements.

### Stage 03–06 main-work Qwen specialization (experimental branch only)

Stage 00 stays **Codex-only**. The [one-prompt local installer](qwen-helper/training-workbench/INSTALL_PROMPT.md) reuses an existing installed Ollama model, installs the separate workbench, and begins synthetic tests without touching source assets. Qualified stage-specific workers may construct private geometry/rig/animation scripts for stages 03–06; the original Codex/actual Sol Light checks, Cycles and human gates remain. [Full workbench guide](qwen-helper/training-workbench/README.md).

## Active local Qwen2.5-Coder-7B pilot (branch-only)

The [active Qwen2.5-Coder-7B A/B lab](astra-qwen-weight-lab/README.md) is now the preferred experimental route on `Qwen-Local-Helper`. It uses the existing `qwen2.5-coder:7b-instruct-q4_K_M` tag, 80 parametric Stage 03–06 synthetic fixture definitions with real Blender oracles, four stage-specific Modelfiles, and guarded inference/fallback evaluation. **Stage 00 is always Codex**; Stage 04 only targets the left-arm pilot while pole placement remains unresolved. Original `qwen-helper/` remains separately usable. The historical Qwen3.5-0.8B results and utilities are [preserved for retrospective review](astra-qwen-weight-lab/archive/qwen3.5-0.8b/README.md). No model is production-qualified based on these fixture pilots.
