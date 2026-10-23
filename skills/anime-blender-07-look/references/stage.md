# Stage 07 implementation checklist

Read this with the live shared contract. Treat the research excerpt below as technical rationale, not a claim of implementation or authority over newer user rules.

## Execute and verify

1. Load approved style sheet and in-game evidence; preserve approved anatomy and face identity.
2. Match cameras and display transform, then refine palette, shadow bands, highlights and surface response.
3. Record exact ramp values, masks/channels, node versions, normals, eye settings and lighting assumptions.
4. Compare face/eye readability, hair detail, emission and alpha from front/profile/three-quarter and motion views.
5. Evaluate only needed outline methods such as reviewed shell or Freestyle with explicit editing and animation tradeoffs.
6. Test outline width across camera distance and resolution; do not promise fixed pixel width from world-space thickness.
7. Test hair-over-eye and ray-dependent tricks under camera and light movement, reflections and shadows.
8. Save accepted material/texture assets, style specification, Cycles showcase and preview comparison for critique.

## Binding policy updates

- Execute through Codex. Use Sol 6.1 High for orchestration and difficult implementation, Sol 6.1 Light for routine work, and Astra when High produces no usable candidate.
- Keep at most three active candidates; prepare only the one to three needed. Ask the user to select or critique each exact submission.
- Allow third-party add-ons and embedded Python during construction. Deliver addon-free core behavior except a hyperspecific runtime add-on exception supported by ten distinct documented failed alternatives and explicit human approval of the exact exception; stop early when an alternative works.
- Disclose and review embedded Python; keep basic native posing independent of unapproved runtime add-ons. Inspect required script behavior separately from add-on installation.
- Keep source and approved checkpoints immutable; use descendants and invalidate dependent approvals after changes.
- Give fidelity priority over animation, realism, performance and convenience, in that order. Optimize only in stage 09.
- Mark missing models, references, hardware, fixtures or Blender execution as blocked/assumed; never infer qualification from documentation.

## Research technical rationale

## 07 — Final in-game look and approved refinements

**What it does:** Finalizes the character's approved Cycles appearance after deformation is stable. This replaces an unrestricted “new look” stage.

**How it does it:** Match in-game references using the approved scene/camera where possible, then finalize palette, shadow treatment, highlight shape, face/eye readability, hair detail, outlines, surface roughness and emission. Record stylistic departures individually and require explicit approval. Do not convert anime faces into photorealistic skin merely because physics is becoming more realistic.

Use a fixed character style sheet with numeric colors/ramps, mask/channel assignments, node-group versions, normal treatment, eye settings, outline method and lighting assumptions. Palette extraction can suggest initial values, but do not re-cluster reference images on every replay. The accepted values are stored directly.

Native outline candidates include a reviewed geometry shell or Freestyle line rendering; choose according to required appearance, editing behavior and animation stability. Solidify supports thickness groups, while Freestyle is a separate line-rendering approach. Do not promise constant pixel width from a fixed world-space shell: record test resolution, camera and distance, and use the approved comparison. Hair-over-eye tricks and ray-dependent outline shading must be tested under camera motion and varied lighting. [18,19]

**Gate output:** final look specification, exact accepted materials/textures, Cycles showcase renders, animation-preview comparison and approval record.

| Action | Allowed? | Condition |
| --- | --- | --- |
| Prepare look candidates from the approved style specification | YES | One to three, with shared comparison conditions |
| Accept visual changes, texture painting or a new outline method | REVIEW | Human approves each substantive departure |
| Change proportions, eye geometry or topology locally | NO | Return to stage 03 and requalify downstream systems |
| Treat Material Preview as proof of final Cycles fidelity | NO | Cycles is the appearance authority |


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
