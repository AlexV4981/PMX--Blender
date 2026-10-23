# Stage 01 implementation checklist

Read this with the live shared contract. Treat the research excerpt below as technical rationale, not a claim of implementation or authority over newer user rules.

## Execute and verify

1. Extract a working copy with recorded archive utility and encoding; preserve original archive unchanged.
2. Inventory PMX elements before import, including stable IDs, deform types, morph types and extra UVs.
3. Import using pinned tool and fully recorded options; disable destructive cleanup where possible.
4. Resolve textures using hash-backed path mappings; present ambiguous matches rather than guessing.
5. Compare vertices, faces, UVs, normals, materials, bones, axes, grants, IK, weights, morphs and edge attributes.
6. Record SDEF and QDEF separately; test pinned importer behavior rather than equating them.
7. Inventory rigid bodies, joints, collision masks and importer changes; classify preserved, transformed, approximated, lost.
8. Save baseline .blend, correspondence map, texture manifest, loss report and matched diagnostic images.

## Binding policy updates

- Execute through Codex. Use Sol 6.1 High for orchestration and difficult implementation, Sol 6.1 Light for routine work, and Astra when High produces no usable candidate.
- Keep at most three active candidates; prepare only the one to three needed. Ask the user to select or critique each exact submission.
- Allow third-party add-ons and embedded Python during construction. Deliver addon-free core behavior except a hyperspecific runtime add-on exception supported by ten distinct documented failed alternatives and explicit human approval of the exact exception; stop early when an alternative works.
- Disclose and review embedded Python; keep basic native posing independent of unapproved runtime add-ons. Inspect required script behavior separately from add-on installation.
- Keep source and approved checkpoints immutable; use descendants and invalidate dependent approvals after changes.
- Give fidelity priority over animation, realism, performance and convenience, in that order. Optimize only in stage 09.
- Mark missing models, references, hardware, fixtures or Blender execution as blocked/assumed; never infer qualification from documentation.

## Research technical rationale

## 01 — PMX import and loss inventory

**What it does:** Creates a traceable Blender import and records what was preserved, transformed, approximated or lost.

**How it does it:** Extract a copy with an explicitly recorded archive utility and filename handling. Preserve the original archive. Resolve texture paths with a mapping file; do not assume filename encoding is the only reason for pink materials. Use an explicit import preset with every relevant option recorded. Disable automatic destructive cleanup for the first baseline wherever the pinned importer permits it; document unavoidable importer changes.

Compare pre-import PMX inventory with the resulting Blender data: vertices/faces/material assignment, UV and additional-UV data, source normals, deform types, weights, morph types and names, bone hierarchy/local axes/grants/IK, edge attributes, rigid bodies, joints and collision masks. Use stable source IDs in addition to names. Capture missing texture dependencies and all lossy import behavior. PMX-specific data can remain in the intermediate recipe even though it will not be an active final-file dependency.

Do not collapse SDEF and QDEF into one unsupported category or assume both have been converted correctly. MMD Tools has documented SDEF support, while actual behavior must be tested in the pinned build. This stage preserves evidence; stages 03–05 decide how to replace dependency-bound deformation. The current MMD Tools project also documents IK and physics differences from MMD, so exact native-MMD motion parity is not an import acceptance requirement for this project. [2,4]

**Gate output:** untouched Blender import checkpoint, feature/loss report, texture manifest, source-to-Blender correspondence and diagnostic renders.

| Action | Allowed? | Condition |
| --- | --- | --- |
| Import, inventory and relink an unambiguous matching texture | YES | Log the source file/hash and resolved path |
| Resolve ambiguous maps or importer cleanup choices | REVIEW | Show the alternatives and consequences |
| Weld, decimate, globally recalculate normals or rebuild the rig | NO | Owned by later stages |
| Omit missing features and declare import complete | NO | Unresolved loss remains a blocker or explicit scoped exception |


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
