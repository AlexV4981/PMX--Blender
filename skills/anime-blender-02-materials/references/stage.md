# Stage 02 implementation checklist

Read this with the live shared contract. Treat the research excerpt below as technical rationale, not a claim of implementation or authority over newer user rules.

## Execute and verify

1. Append versioned native shader templates with recorded socket contracts for each actual material class.
2. Inspect packed image channels, alpha association and color-versus-data treatment using image evidence.
3. Map every relevant PMX flag to implemented, approximate, inapplicable or unsupported Cycles behavior.
4. Build Cycles-compatible toon shading; exclude Shader to RGB from required Cycles graphs.
5. Provide a shared compatible preview graph or labeled Eevee approximation with shared palette parameters.
6. Compare skin, eyes, hair-over-eye visibility, alpha, shadows, outlines and normals in fixed views and lighting sweep.
7. Record each color, shading, outline or visibility departure separately for approval.
8. Save material instances, exact textures, flag table, comparisons and preview limitations.

## Binding policy updates

- Execute through Codex. Use Sol 6.1 High for orchestration and difficult implementation, Sol 6.1 Light for routine work, and Astra when High produces no usable candidate.
- Keep at most three active candidates; prepare only the one to three needed. Ask the user to select or critique each exact submission.
- Allow third-party add-ons and embedded Python during construction. Deliver addon-free core behavior except a hyperspecific runtime add-on exception supported by ten distinct documented failed alternatives and explicit human approval of the exact exception; stop early when an alternative works.
- Disclose and review embedded Python; keep basic native posing independent of unapproved runtime add-ons. Inspect required script behavior separately from add-on installation.
- Keep source and approved checkpoints immutable; use descendants and invalidate dependent approvals after changes.
- Give fidelity priority over animation, realism, performance and convenience, in that order. Optimize only in stage 09.
- Mark missing models, references, hardware, fixtures or Blender execution as blocked/assumed; never infer qualification from documentation.

## Research technical rationale

## 02 — Cycles material and texture restoration

**What it does:** Restores the in-game appearance sufficiently to judge the model before changing its geometry or rig.

**How it does it:** Append versioned native node-group templates with fixed interfaces for skin/face, hair, eyes, cloth, metal, emission, transparency and outlines. Classify each image's actual data: color maps normally use their intended color transform; numeric masks, normals and other data maps use data treatment. Verify packed-channel meaning and alpha association rather than inferring all semantics from filenames.

Map each relevant PMX material flag to an implemented, approximated, inapplicable or unsupported Cycles behavior. Double-sided surfaces, alpha, toon/sphere effects, outlines and shadows receive individual decisions. PMX draw order is not assumed to be equivalent to Cycles ray visibility. Face normals, hair-over-eye appearance and eyebrow visibility receive front/profile/three-quarter comparisons and lighting/motion tests.

Cycles supports Toon BSDF, but Shader to RGB is Eevee-only. Proposed methods are Toon BSDF, controlled stylized BSDF combinations and carefully bounded native math/mask techniques, chosen by the approved game/character profile. No single template is claimed to recreate every game's shader. [5,6]

Material Preview uses Eevee, so provide either a shared compatible graph or a deliberately approximate preview branch. Blender supports renderer-specific Material Output targets. Any preview branch shares the character's approved texture/palette parameters and is labeled an approximation; Cycles renders remain the appearance authority. Camera-dependent or ray-dependent tricks require explicit review of their lighting, reflection, shadow and movement limitations. [7,8]

**Gate output:** restored material library instances, source-map assignments, flag handling table, matched comparisons, preview limitations and approved appearance checkpoint.

| Action | Allowed? | Condition |
| --- | --- | --- |
| Relink known assets and instantiate a recorded shader template | YES | Use exact template version and logged parameters |
| Change colors, shading, alpha, outlines, eyes or visibility tricks | REVIEW | Per-change comparisons in Cycles |
| Replace eye geometry or change the character's proportions | NO | Route to stage 03 |
| Use an Eevee-only node as a required final Cycles effect | NO | A preview-only branch is a separate documented case |


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
