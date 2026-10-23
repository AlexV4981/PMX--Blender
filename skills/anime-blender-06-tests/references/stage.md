# Stage 06 implementation checklist

Read this with the live shared contract. Treat the research excerpt below as technical rationale, not a claim of implementation or authority over newer user rules.

## Execute and verify

1. Create a dedicated test derivative with versioned, stored control-space motion inputs.
2. Test approved shoulder/hip ranges, elbow/knee flexion, wrist/forearm twist and neck/spine turns.
3. Run crouch, walk/run, planted turn, jump/landing, floor contact, hand poses and object grip.
4. Exercise facial extremes/combinations, mirror behavior, each retarget profile and root/in-place modes.
5. Measure IK/FK and parent-switch pose jumps and neutral reset before/after fixtures.
6. Lint invalid drivers/targets, zero-length bones, nonuniform scale, nonfinite values, stale bindings and broken paths.
7. Combine dependency inspection and evaluated fixture diagnostics; open clean stock Blender without construction add-ons.
8. Save pass/fail/blocked matrix, close-up clips, numerical deviations and owner-routed issues without silently repairing them.

## Binding policy updates

- Execute through Codex. Use Sol 6.1 High for orchestration and difficult implementation, Sol 6.1 Light for routine work, and Astra when High produces no usable candidate.
- Keep at most three active candidates; prepare only the one to three needed. Ask the user to select or critique each exact submission.
- Allow third-party add-ons and embedded Python during construction. Deliver addon-free core behavior except a hyperspecific runtime add-on exception supported by ten distinct documented failed alternatives and explicit human approval of the exact exception; stop early when an alternative works.
- Disclose and review embedded Python; keep basic native posing independent of unapproved runtime add-ons. Inspect required script behavior separately from add-on installation.
- Keep source and approved checkpoints immutable; use descendants and invalidate dependent approvals after changes.
- Give fidelity priority over animation, realism, performance and convenience, in that order. Optimize only in stage 09.
- Mark missing models, references, hardware, fixtures or Blender execution as blocked/assumed; never infer qualification from documentation.

## Research technical rationale

## 06 — Animation and deformation qualification

**What it does:** Proves that the character can be animated before final appearance and physics work.

**How it does it:** Run versioned fixtures in a dedicated test derivative: shoulder/hip ranges, elbow/knee flexion, wrist/forearm twists, neck/spine turns, crouch, walk/run, planted-foot turn, jump/landing, floor contact, hand poses, object grip, facial extremes and expression combinations. Use the same control-space inputs and stored poses for repeat runs of a given character. Avoid requiring every stylized body to satisfy an identical anatomical range; approve character-specific ranges at intake.

Test IK/FK and parent switches for positional/rotational jumps, root-motion/in-place behavior, mirrored controls, facial combinations and each supported retarget profile. Check neutral reset before and after tests. Capture face/hand/foot close-ups, silhouette comparisons and mesh strain/collapse indicators. Numeric metrics supplement the human's assessment of appeal and usable deformation.

Run integrity lint: invalid drivers, missing targets, unintended zero-length bones, unexpected non-uniform scale, nonfinite values, stale bindings, duplicate evaluations, broken paths and dependency-cycle diagnostics. Logs alone do not prove all possible cycles absent; combine reference inspection with evaluation of the required fixtures. Core rig and deformation must still work in a clean stock-Blender process without construction add-ons.

**Gate output:** pass/fail/blocked matrix, test clips, measured deviations, issue ownership and a human-reviewed animation-ready checkpoint. Formal laptop FPS acceptance remains in stage 09.

| Action | Allowed? | Condition |
| --- | --- | --- |
| Animate test derivatives, measure, lint and report | YES | Do not overwrite production actions or the approved rig |
| Propose a repair and route it to its owner stage | YES | Invalidate and repeat affected checks after changes |
| Silently modify geometry, shading or rig behavior during testing | NO | Testing does not grant editing authority |
| Mark an untested or skipped capability as passed | NO | Use blocked or not applicable with a reason |


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
