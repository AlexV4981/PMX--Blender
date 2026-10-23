# Stage 04 implementation checklist

Read this with the live shared contract. Treat the research excerpt below as technical rationale, not a claim of implementation or authority over newer user rules.

## Execute and verify

1. Map source bones to anatomical roles and native deform bones; document unsupported source mechanics.
2. Build control-to-mechanism-to-deform dependency direction with tested exceptions and no hidden runtime callbacks.
3. Implement world/root/COG, hips/spine/chest, head/neck and arm/leg IK/FK controls.
4. Add poles, foot roll/toes, fingers and needed accessory/tail/ear controls; default stretch off.
5. Define stable naming, bone collections, side colors, control shapes, rotation modes, scale inheritance and reset values.
6. Test grants/twist/follow in explicit transform spaces, combined rotations and relevant negative ratios.
7. Use construction tools such as Rigify only with pinned versions; inventory generated embedded Python separately.
8. Save rig maps, capability matrix, reset and switch demonstrations, runtime dependency report.

## Binding policy updates

- Execute through Codex. Use Sol 6.1 High for orchestration and difficult implementation, Sol 6.1 Light for routine work, and Astra when High produces no usable candidate.
- Keep at most three active candidates; prepare only the one to three needed. Ask the user to select or critique each exact submission.
- Allow third-party add-ons and embedded Python during construction. Deliver addon-free core behavior except a hyperspecific runtime add-on exception supported by ten distinct documented failed alternatives and explicit human approval of the exact exception; stop early when an alternative works.
- Disclose and review embedded Python; keep basic native posing independent of unapproved runtime add-ons. Inspect required script behavior separately from add-on installation.
- Keep source and approved checkpoints immutable; use descendants and invalidate dependent approvals after changes.
- Give fidelity priority over animation, realism, performance and convenience, in that order. Optimize only in stage 09.
- Mark missing models, references, hardware, fixtures or Blender execution as blocked/assumed; never infer qualification from documentation.

## Research technical rationale

## 04 — Native Blender control rig

**What it does:** Replaces PMX-oriented rig mechanisms with a coherent Blender animation rig. It does not recreate MMD evaluation order as a final requirement.

**How it does it:** Map source bones to approved anatomical roles and final deform bones. Implement one explicit control → mechanism → deformation dependency direction, with documented exceptions. Reproduce needed twist, follow, volume and corrective functions using native constraints, bones and drivers. Do not assume a PMX grant ratio directly equals a Copy Rotation influence in every space or rotation case. Test translations, rotations, negative ratios and combined poses wherever those source features matter.

Define collections, stable naming, side labels/colors, control shapes, rotation modes, scale inheritance and reset values. Include world/root/COG, hips/spine/chest, head/neck, arm and leg IK/FK, pole controls, foot roll/toes, finger controls and appropriate accessory/tail/ear controls. Stretch defaults off unless the user approves a stylized option. Match professional reference rig capabilities after analyzing their suitability, without copying proprietary rig assets into a distributable pack without permission.

A pinned Rigify build may be used as a construction tool if its generated result meets the specification. Generated rigs can function without the recipient installing Rigify, but snapping, parent-switch UI and other helper functionality can involve generated Python. Do not equate absence of an add-on installation with absence of script dependence. Rigify's generated features document IK/FK and parent-switch behavior; these must be individually tested in the delivered file. [14,15]

**Gate output:** native rig, mapping tables, required-function checklist, reset-pose and switching demonstrations, plus an explicit runtime dependency list.

| Action | Allowed? | Condition |
| --- | --- | --- |
| Build native controls, constraints, drivers and mechanisms | YES | Within the approved rig specification |
| Change deformation behavior or choose a different rig architecture | REVIEW | Demonstrate consequences in the same test poses |
| Retain required MMD/Rigify add-on callbacks without an approved exception | NO | Remove/replace or satisfy the ten-distinct-failed-alternative and explicit human approval rule |
| Change approved mesh proportions to make rigging easier | NO | Return to stage 03 |


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
