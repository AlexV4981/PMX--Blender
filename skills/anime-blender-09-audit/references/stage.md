# 09 — Audit and delivery: working procedure

## 1. Audit and one plan decision

Read PACK/references/workflow.md. Reuse the accepted camera/color recipe and shared motion/face fixture identities; inspect actual changed systems and critical final Cycles face/full-body views, switches, expressions, cold physics/reset/toggles and dependencies. Keep unresolved faults visible. Present the actual audit plus the concrete optimization plan or 'not needed' disposition together. One observed human decision is recorded as review --gate audit. Do all audit preparation before asking; do not ask separately whether to prepare it.

## 2. Measure the actual Cycles workload

Use Cycles Rendered viewport (scene.render.engine='CYCLES', shading.type='RENDERED') with actual scene materials/lights/world. Material Preview is a different engine and is outside scope unless explicitly requested. Pin Cycles viewport samples, denoising, device, viewport pixels/UI scaling and shader/scene state. Record exact CPU/GPU/RAM/VRAM, Blender/driver/OS, power and thermal state. Retain the approved 24 FPS project timebase, proposed 240 measured frames and three repetitions, or the human-approved fixture. Desired goals remain >=24 FPS physics-off and approximately 12 FPS fresh active physics, with severe sustained stalls unacceptable; they require fresh Cycles qualification and cannot inherit prior preview-engine results.

Count completed viewport frame evaluations/redraws at the pinned sampling policy and elapsed wall time (FPS=N/t). Do not count progressive sampling updates as new animation frames. Compile shaders first; report initialization and pre-roll separately. Use no frame dropping. A playback cap cannot prove spare throughput; a qualified uncapped UI harness must retain the simulation timebase and fixed sampling policy. No tested UI recorder is bundled. Report this limitation and block a throughput claim if measurement is unavailable; never substitute headless frame_set timing or an alternate engine.

Separate physics-off, cleared-cache sequential cold physics and cached playback. Report repetitions, frame-time distributions/long stalls, memory and actual enabled categories. Keep fidelity and functional conditions separate from timing; do not hide objects, alter masks, lower render/physics quality or disable collisions to force a pass.

## 3. Apply selected work and re-audit affected systems

Perform only the combined audit decision's selected plan. Prioritize measured duplicate evaluation/dead dependencies, proxy/collision scope and control overhead. Changes to quality or visible assets require the already specified comparisons and owner-stage requalification; a changed tradeoff/scope requires a fresh combined audit decision. If no work is needed, record that disposition and continue to package tests. Reuse passing unchanged-component evidence with explicit dependency identity/rationale, and rerun affected fixtures plus the critical final checks. Keep source and accepted checkpoints immutable.

## 4. Test the actual package and one final delivery decision

Package local rig/material data and packed/relative required textures. Save neutral animation state, separate audit actions and embedded guide; clear simulation bakes while preserving editable solvers. Open the relocated package in fresh stock Blender without construction add-ons and core automatic Python execution. Test native controls/shape keys, Cycles graph output, reset/short simulation and dependencies; run approved optional helpers separately. Keep user-specific paths/modules/driver namespace/handlers/reference links disclosed and resolved.

Register the final file/assets, record required checks and submit the exact bundle. Present the final Cycles result, changed-system re-audit, package tests and timing evidence together. One observed human delivery decision covers re-audit, delivery and final stage acceptance. The orchestrator records review --gate delivery; the CLI validates the exact submitted bundle and approves stage 09 atomically. Do not ask another final-approval question or run approve a second time. Workers cannot grant either decision.

## Evidence

Retain the eight canonical names: final-quality, physics-off-fps, cold-physics-fps, frame-time-and-memory, regression-tests, relocated-clean-open, dependency-disposition, delivery-guide-and-recipe. Use one compact report with references or separate evidence files as appropriate; each ledger check binds actual evidence to the current bundle. A failed/blocked check remains failed/blocked despite a flattering image. Do not transplant old approvals into version 3 runs.

## Mathematical support

Use PACK/references/mathematics.md section 09 for residual/uncertainty and constrained tradeoff principles. Keep quality/function/dependency/performance separate; the two human decisions are audit and delivery. No scalar similarity score or timing average can silently waive a fault.

## Technical references

Consult PACK/references/sources.md for primary Blender documentation and PACK/references/workflow.md for the active lightweight procedure.
