# Stage 08 implementation checklist

Read this with the live shared contract. Treat the research excerpt below as technical rationale, not a claim of implementation or authority over newer user rules.

## Execute and verify

1. Map visible hair, garments, accessories, tails, ears and soft tissue against PMX rigid bodies and joints.
2. Choose native solver candidates per physical structure; do not force a universal jiggle-bone system.
3. Build distinct simulation/collision proxies and render surfaces with one-way attachment-to-solver-to-deformation flow.
4. Test modifier order and double-transform/dependency-cycle risks before full-character evaluation.
5. Record solver-specific scale, mass assumptions, stiffness, damping, gravity, masks, collision pairs, quality and timebase.
6. Implement independent category toggles that stop solver work; measure evaluation and demonstrate manual animation with each off.
7. Define reset/rest/pre-roll and cache invalidation; run settle, acceleration/stop, turns, locomotion, crouch, landing and contacts.
8. Measure normalized tip travel, settle time, stretch, penetration and instability; save approved parameter sets and clear final caches.

## Binding policy updates

- Execute through Codex. Use Sol 6.1 High for orchestration and difficult implementation, Sol 6.1 Light for routine work, and Astra when High produces no usable candidate.
- Keep at most three active candidates; prepare only the one to three needed. Ask the user to select or critique each exact submission.
- Allow third-party add-ons and embedded Python during construction. Deliver addon-free core behavior except a hyperspecific runtime add-on exception supported by ten distinct documented failed alternatives and explicit human approval of the exact exception; stop early when an alternative works.
- Disclose and review embedded Python; keep basic native posing independent of unapproved runtime add-ons. Inspect required script behavior separately from add-on installation.
- Keep source and approved checkpoints immutable; use descendants and invalidate dependent approvals after changes.
- Give fidelity priority over animation, realism, performance and convenience, in that order. Optimize only in stage 09.
- Mark missing models, references, hardware, fixtures or Blender execution as blocked/assumed; never infer qualification from documentation.

## Research technical rationale

## 08 — Editable native physics

**What it does:** Replaces the old physics with Blender-native, editable secondary motion while maintaining the approved character design and animation controls.

**How it does it:** Use the PMX rigid-body/joint assignments as evidence of intended movable parts, not as mandatory final solver parameters. Cross-check visible hair, clothing, accessories, tails, ears and soft tissue. Flag visually movable parts with no imported physics and ambiguous body/accessory assignments for human review. Select the method by physical structure instead of forcing a universal jiggle-bone system.

| Part class | Proposed native starting method | Required controls |
| --- | --- | --- |
| Skirts, sleeves, capes, ribbons | Cloth on a separate suitable proxy, driven by the animated attachment/pin regions | Pin groups, collision scope, material stiffness/damping, reset instructions |
| Hair clumps, tails, flexible ears | Reviewed cloth-strip/volume proxy or constrained spring-body mechanism, selected per structure | Stable attachment, limited stretch, collision, manual fallback |
| Rigid ornaments and dangling hardware | Native rigid bodies and constrained spring/hinge relationships | Attachment, collision collection/pairs, limits and damping |
| Soft tissue | Localized soft-body or cloth-with-internal-springs proxy where suitable | Goal/pin mask, damping, amplitude limits, collision and manual fallback |

These are qualification candidates, not universal production-ready presets. Surface Deform is documented for transferring a cloth proxy's movement to a detailed mesh; cloth pin weights and soft-body goal weights provide native attachment control. Rigid-body spring constraints provide a different solver with different parameters. [20,21,22,23]

Keep simulation proxies, collision proxies and rendered surfaces distinct. Establish one-way evaluation from animation rig to attachments/colliders, through simulation, to visible deformation. Avoid a visible mesh feeding its own collision driver through a dependency cycle or receiving both skin and proxy motion twice. Choose and test each modifier order; for example, many proxy stacks use attachment deformation before Cloth and render thickness after simulation, but no universal stack order is imposed on every model.

Record actual solver-specific settings: scale, proxy topology, masses/density assumptions, stiffness/damping, gravity, pin/goal masks, collision distances, collision pairs, rigid-body substeps/iterations or cloth/soft-body solver settings, time scale, FPS, rest frame, pre-roll and reset procedure. There is no honest universal conversion from an abstract “stiffness 0.7” into every Blender solver. Quality/collision settings trade computation time for stability and collision handling. [24,25]

Provide separate category toggles and usable manual animation when each category is off. A disabled category must stop its solver work, not merely hide its output. Switching physics state requires cache invalidation/reset and a documented restart unless seamless switching has actually been implemented and tested. Use native modifier/constraint/world settings where supported and test the actual evaluation cost. Do not count a visibility toggle as proof of disabled calculation.

Test rest/settle, acceleration/stop, turns, walk/run, crouch, jump/landing and contacts using the approved fixture. Measure tip travel relative to part length, settling time, stretch, collision penetration and instability. PMX motion is not the target reference. The human approves plausible behavior within the character's design; exact real-world fabric properties cannot be inferred from a picture alone.

**Gate output:** category method map, editable native simulations, settings/masks/proxies, toggle demonstrations, cold-reset test clips and human-approved motion. No baked simulation cache is included in the deliverable. Blender still uses temporary caches while evaluating; unbaked simulation is not stateless arbitrary-frame playback. [26]

| Action | Allowed? | Condition |
| --- | --- | --- |
| Build native proxies, collisions, masks and scoped solver candidates | YES | Preserve approved visible surfaces and manual rig behavior |
| Choose motion strength, soft-tissue behavior or solver substitutions | REVIEW | Motion comparisons, settings and limitations disclosed |
| Add visible garment thickness or new body surfaces without approval | NO | Return to the geometry owner stage |
| Replace editable simulations with baked-only motion | NO | Temporary QA caches are cleared for delivery |


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
