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
