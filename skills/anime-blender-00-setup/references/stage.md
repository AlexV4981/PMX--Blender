# Stage 00 implementation checklist

Read this with the live shared contract. Treat the research excerpt below as technical rationale, not a claim of implementation or authority over newer user rules.

## Execute and verify

1. Inventory original PMX package, texture files, source terms and reference images; hash each original before copying.
2. Pin exact Blender build and construction add-on commits; record OS, GPU, drivers and dependency hashes.
3. Record Nitro V Ryzen 5 7535HS, 16 GB RAM, 6 GB VRAM baseline and actual device differences.
4. Measure approved character height; propose Z-up, -Y-forward, meters; record landmark-based scale conversion.
5. Separate confirmed in-game references from inferred details; capture professional rig references as capability evidence.
6. Create fixed neutral Cycles, lighting sweep, showcase and Material Preview fixtures with recorded cameras and color management.
7. Propose numerical tolerance pilot and character-specific pose ranges; leave unmeasured thresholds pending human calibration.
8. Save environment lock, intake manifest, reference board, run.json recipe skeleton and acceptance proposal.

## Binding policy updates

- Execute through Codex. Use Sol 6.1 High for orchestration and difficult implementation, Sol 6.1 Light for routine work, and Astra when High produces no usable candidate.
- Keep at most three active candidates; prepare only the one to three needed. Ask the user to select or critique each exact submission.
- Allow third-party add-ons and embedded Python during construction. Deliver addon-free core behavior except a hyperspecific runtime add-on exception supported by ten distinct documented failed alternatives and explicit human approval of the exact exception; stop early when an alternative works.
- Disclose and review embedded Python; keep basic native posing independent of unapproved runtime add-ons. Inspect required script behavior separately from add-on installation.
- Keep source and approved checkpoints immutable; use descendants and invalidate dependent approvals after changes.
- Give fidelity priority over animation, realism, performance and convenience, in that order. Optimize only in stage 09.
- Mark missing models, references, hardware, fixtures or Blender execution as blocked/assumed; never infer qualification from documentation.

## Research technical rationale

## 00 — Setup, intake and reference specification

**What it does:** Establishes the exact environment, character identity, source inventory, comparison scenes and acceptance rules before any conversion.

**How it does it:** Use stock Blender 4.5 LTS as the proposed initial qualification branch, with one exact patch/build and checksum frozen after fixture testing. Pin a matching MMD Tools release or commit; do not use a moving “latest” dependency. Blender 4.5 LTS is a stable starting branch, not a claim that a specific patch/add-on combination has already passed testing. Record all build-time extensions separately from final-file dependencies. [1,2]

Collect the PMX package, original textures, source terms/readmes, in-game front/side/back/face references and professional rig examples. Label unknown character features and camera/lighting uncertainties instead of inventing them. Define character height from an approved anatomical measurement or user-approved estimate; do not make every character the same height. Use a documented Blender coordinate convention, proposed as Z-up and -Y-forward, and one Blender unit per meter. Record every conversion transform. If scaling by height, scale_factor = approved_height / measured_import_height; document the measurement landmarks and transform geometry, armature and later collision construction consistently.

Create fixed Cycles neutral-light, lighting-sweep and showcase scenes, plus a Material Preview animation scene. Pin camera, resolution, color management, light/world assets, sample count, seed, denoising and render device. A color-diagnostic preset can use Standard, while the approved showcase preset is separately fixed. Never compare images made with different view transforms and call the difference a shader error. AgX and Standard are display transforms with different behavior. [3]

**Gate output:** environment lock, intake inventory, reference board, character recipe skeleton, rig capability checklist, test scene settings, proposed per-model tolerances and approved scope.

| Action | Allowed? | Condition |
| --- | --- | --- |
| Inventory, hash, inspect and create comparison scenes | YES | No mutation of source assets |
| Select scale, style assumptions, rig requirements or references | REVIEW | Record uncertainty and the chosen evidence |
| Upgrade a pinned tool during an existing run | NO | Requalify a new pack version |
| Guess unavailable visual details and mark them confirmed | NO | Record a reconstruction proposal instead |


## Sources

Primary documentation consulted; source pages describe Blender/MMD capabilities, while pipeline choices and approval rules above are proposed for this project.

1. [Blender 4.5 LTS release/support](https://www.blender.org/releases/4-5/)
2. [Maintained MMD Tools repository: compatibility and known IK/physics limitations](https://github.com/MMD-Blender/blender_mmd_tools)
3. [Blender color management](https://docs.blender.org/manual/en/4.4/render/color_management.html)
4. [Upstream MMD Tools feature documentation, including SDEF](https://github.com/powroupi/blender_mmd_tools/wiki/MMD_TOOLS-LIST-OF-FEATURES-AND-BRIEF-TUTORIAL-INFORMATION-FOR-FEATURES)
5. [Toon BSDF, Blender 4.5](https://docs.blender.org/manual/pt/4.5/render/shader_nodes/shader/toon.html)
6. [Shader to RGB limitations](https://docs.blender.org/manual/id/4.0/render/shader_nodes/converter/shader_to_rgb.html)
7. [Blender developer documentation: Material Preview uses Eevee](https://archive.blender.org/developer/differential/0005/0005612/index.html)
8. [Blender 4.5 API: Material Output renderer targets](https://docs.blender.org/api/4.5/bpy.types.ShaderNodeOutputMaterial.html)
9. [Shape-key introduction and topology guidance](https://docs.blender.org/manual/nl/4.5/animation/shape_keys/introduction.html)
10. [Data Transfer topology/index mapping](https://docs.blender.org/UATEST/manual/en/4.5/modeling/modifiers/modify/data_transfer.html)
11. [Armature modifier and Preserve Volume](https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/armature.html)
12. [Corrective Smooth](https://docs.blender.org/manual/es/4.5/modeling/modifiers/deform/corrective_smooth.html)
13. [Driver workflow and corrective shape keys](https://docs.blender.org/manual/id/4.5/animation/drivers/workflow_examples.html)
14. [Rigify distribution/runtime statement](https://docs.blender.org/manual/en/2.81/addons/rigging/rigify.html)
15. [Rigify generated rig features](https://docs.blender.org/manual/en/4.5/addons/rigging/rigify/rig_features.html)
16. [Driver execution restrictions](https://docs.blender.org/manual/nl/4.5/animation/drivers/troubleshooting.html)
17. [Drivers panel and variables](https://docs.blender.org/manual/ar/4.5/animation/drivers/drivers_panel.html)
18. [Solidify thickness and vertex groups](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/solidify.html)
19. [Freestyle introduction](https://docs.blender.org/manual/en/4.5/render/freestyle/introduction.html)
20. [Surface Deform proxy workflow](https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/surface_deform.html)
21. [Cloth pin groups](https://docs.blender.org/manual/id/4.5/physics/cloth/settings/shape.html)
22. [Soft-body goals](https://docs.blender.org/UATEST/manual/en/4.5/physics/soft_body/settings/goal.html)
23. [Generic spring constraints](https://docs.blender.org/manual/uk/4.5/physics/rigid_body/constraints/types/generic_spring.html)
24. [Rigid Body World settings](https://docs.blender.org/manual/en/latest/physics/rigid_body/world.html)
25. [Cloth collisions and quality](https://docs.blender.org/manual/nl/4.5/physics/cloth/settings/collisions.html)
26. [Simulation caching/baking](https://docs.blender.org/manual/en/5.0/physics/baking.html)
27. [Blender 4.5 timeline playback modes](https://docs.blender.org/manual/en/4.5/editors/timeline.html)
28. [Packed data, relative paths and missing-file tools](https://docs.blender.org/manual/fi/4.5/interface/window_system/topbar.html)
