# 09 — Audit and delivery: working procedure

## 1. Audit before optimizing (09A)

Load accepted visual, rig and physics evidence and inventory unresolved assumptions. Repeat representative Cycles face/full-body views, switches, expressions, physics reset/toggles and dependency checks on the exact final candidate. Obtain human review of the actual audit and proposed tradeoffs. This is a model acceptance gate, not permission to prepare the audit.

## 2. Measure the intended machine and workload

Record exact CPU/GPU/VRAM/RAM, Blender/driver/OS, power and thermal state, viewport pixel dimensions, UI scaling, lighting, overlays and enabled visible/physics categories. Use the approved full-character fixture, 24 FPS project timebase, proposed 240 measured frames and three repetitions. Compile shaders before timing and report initialization separately.

Count completed UI redraw/evaluation frames and elapsed wall time; FPS=N/t. Play Every Frame avoids dropping frames, but capped playback cannot prove spare throughput above its cap. Use an independently qualified redraw-driven uncapped UI harness retaining the same scene timebase, and cross-check observed playback. No such recorder is bundled as a tested tool. If unavailable, report the measurement limitation and block the throughput claim; do not substitute a background frame_set timer.

Measure physics-off, fresh active physics and cached playback separately. Clear caches and run sequentially with documented pre-roll for each cold repetition. Report each repeat, aggregate, percentiles/longest frame stalls, memory peaks and actual categories. Physics-off target is >=24 FPS; active physics aims near 12 FPS with sustained near-1-FPS stalls unacceptable. Use approved pilot stall/tolerance limits, not a fabricated threshold.

## 3. Optimize measured cost only (09B), then re-audit (09C)

Prepare a concrete plan and obtain its required human gate before quality tradeoffs. Prioritize duplicate evaluation/dead dependencies, proxy and collision scope, then control overhead. Any viewport-only simplification needs an explicitly labeled measured configuration and preserved final render quality. Visible geometry/texture/physics changes require individual comparisons and owner-stage requalification. Do not silently hide objects, drop frames, downsample textures or disable collisions to pass.

If no optimization is needed, record that disposition at the optimization review; do not manufacture changes. Repeat affected visual/motion/dependency and timing checks on the final bundle. Preserve fidelity priority if hardware cannot meet the goal; report the conflict.

## 4. Test the actual package (09D)

Make needed material/rig data local or package linked dependencies intentionally. Pack eligible assets or use verified relative texture paths. Save neutral animation state, isolated audit actions and embedded guide. Clear simulation bakes while preserving editable settings. Reopen from a new directory in a fresh stock Blender profile, with construction add-ons unavailable and automatic Python disabled. Replay core controls, shape keys, graph outputs and short simulation reset. Test any approved optional embedded helpers separately.

Check required external modules, Python driver namespace functions, handlers, user-specific paths and reference-model links. An inspection report inventories possible dependencies; only replay demonstrates whether they are required. Preserve exact recipe/settings, source correspondence and qualified limitations. Deliver the blend and necessary textures; keep audit artifacts separate from production animation.

## Evidence

Use all eight canonical names in frozen stage policy: final-quality, physics-off-fps, cold-physics-fps, frame-time-and-memory, regression-tests, relocated-clean-open, dependency-disposition, delivery-guide-and-recipe. Attach actual images, timings, clean-process results and exact package manifests respectively. Record the audit, optimization, reaudit and delivery human subgates through pipeline.py only after the corresponding observed decision. A blocked hardware/runtime check cannot become pass merely because the document is complete.

## Apply mathematical support

Keep quality/function/dependency/performance as separate acceptance conditions and report measurement variation. Use constrained tradeoff selection; retain all existing 09 subgates. This integration does not apply workflow or asset optimization.

Read PACK/references/mathematics.md for the 09 procedure, equations, assumptions, evidence fields and primary references. Use only methods relevant to this fault; preserve the ordered work above. Bundled measurements do not imply the optional solvers were implemented or that a human approved the result.

## Technical references

Consult PACK/references/sources.md for primary documentation matched to the pinned Blender build. Treat formulas and proposed methods here as engineering guidance, not evidence that the character has been qualified.
