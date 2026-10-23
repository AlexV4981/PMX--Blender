# Stage 05 implementation checklist

Read this with the live shared contract. Treat the research excerpt below as technical rationale, not a claim of implementation or authority over newer user rules.

## Execute and verify

1. Implement keyable independent/combined blink, gaze, brows, jaw, mouth shapes, visemes and character expressions.
2. Preserve intended facial asymmetry and expression ranges; show combinations that overdrive face deformation.
3. Demonstrate selectable controls, visibility collections, locks, keying sets, reset, foot planting and IK/FK switching.
4. Demonstrate parent/space switching, root-motion and in-place conventions, pose library and mirror behavior.
5. Name each retarget source profile; save source-to-control mappings, rest alignment, root policy and test clips.
6. Use native driver variables and simple supported expressions for core behavior; inspect custom namespaces and handlers.
7. Disclose exact embedded helper code and execution requirements for human review; test basic posing without it.
8. Embed animator guide, face chart, full capability matrix, supported profile list and limits; do not claim automatic speech recognition.

## Binding policy updates

- Execute through Codex. Use Sol 6.1 High for orchestration and difficult implementation, Sol 6.1 Light for routine work, and Astra when High produces no usable candidate.
- Keep at most three active candidates; prepare only the one to three needed. Ask the user to select or critique each exact submission.
- Allow third-party add-ons and embedded Python during construction. Deliver addon-free core behavior except a hyperspecific runtime add-on exception supported by ten distinct documented failed alternatives and explicit human approval of the exact exception; stop early when an alternative works.
- Disclose and review embedded Python; keep basic native posing independent of unapproved runtime add-ons. Inspect required script behavior separately from add-on installation.
- Keep source and approved checkpoints immutable; use descendants and invalidate dependent approvals after changes.
- Give fidelity priority over animation, realism, performance and convenience, in that order. Optimize only in stage 09.
- Mark missing models, references, hardware, fixtures or Blender execution as blocked/assumed; never infer qualification from documentation.

## Research technical rationale

## 05 — Animation readiness, face and usability

**What it does:** Makes the rig practical for learning and progressively more demanding animation.

**How it does it:** Connect the approved expressions and morphs to native shape keys, bones, material properties or supported node setups. Implement independent and combined blink, eye aim, brows, jaw, mouth shapes and editable viseme controls. Preserve character-specific expressions and asymmetry where intentional. Lip-sync readiness means keyable mouth/viseme controls; automatic speech recognition is not implicitly included. Document expression ranges and combinations that can overdrive the face.

Provide selectable controls, clear visibility collections, transform locks, keying conventions, reset instructions, foot planting, IK/FK switching, parent/space switching, root-motion/in-place conventions and an initial pose set. Include explicit mappings and test clips for each supported retargeting source profile; “retargetable” does not mean every animation source works without configuration.

Use native driver variables with built-in functions or simple expressions for core rig behavior. Custom driver namespace functions, hidden frame handlers and imports from external modules cannot be required core dependencies. Allow inspected embedded helper scripts after review, with exact execution requirements disclosed. Preserve native basic posing independent of unapproved runtime add-ons; distinguish optional helper features from core posing. If a required convenience function needs embedded code, disclose that dependency and have the human approve the exact behavior before acceptance. Simple driver expressions and custom Python functions have different execution requirements. [16,17]

**Gate output:** animator guide embedded as text, capability demonstrations, face chart, retargeting profiles, pose/reset assets and approved usability checkpoint.

| Action | Allowed? | Condition |
| --- | --- | --- |
| Add controls, property labels, supported mappings and instructions | YES | Match the approved interface specification |
| Add corrective shapes or embedded helper scripts | REVIEW | Demonstrate the exact effect and script execution requirements |
| Claim every future animation workflow is supported | NO | Claims must name a tested capability/source profile |
| Depend on custom Python to evaluate basic deformation | NO | Replace with portable native behavior |


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
