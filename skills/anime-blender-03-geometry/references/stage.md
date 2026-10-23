# Stage 03 implementation checklist

Read this with the live shared contract. Treat the research excerpt below as technical rationale, not a claim of implementation or authority over newer user rules.

## Execute and verify

1. Audit boundaries, split normals, seam vertices, layered surfaces, deform weights and every imported morph.
2. Preserve intentional openings and coincident seams; isolate defects in diagnostic poses before repair.
3. Separate bone deform groups from pin, outline and utility masks before any normalization.
4. Prepare explicit topology, eye, thickness, hidden-surface and proportion proposals with wireframes and silhouette overlays.
5. Finalize substantial topology before final rig; preserve source IDs and new correspondence for every changed element.
6. Compare native weights, Preserve Volume, corrective shapes and targeted Corrective Smooth for SDEF/QDEF replacement.
7. Re-test every affected shape key and deformed pose; record exact approved mesh assets or deterministic deltas.
8. Save geometry specification, morph inventory, correspondence, repairs and downstream invalidation list.

## Binding policy updates

- Execute through Codex. Use Sol 6.1 High for orchestration and difficult implementation, Sol 6.1 Light for routine work, and Astra when High produces no usable candidate.
- Keep at most three active candidates; prepare only the one to three needed. Ask the user to select or critique each exact submission.
- Allow third-party add-ons and embedded Python during construction. Deliver addon-free core behavior except a hyperspecific runtime add-on exception supported by ten distinct documented failed alternatives and explicit human approval of the exact exception; stop early when an alternative works.
- Disclose and review embedded Python; keep basic native posing independent of unapproved runtime add-ons. Inspect required script behavior separately from add-on installation.
- Keep source and approved checkpoints immutable; use descendants and invalidate dependent approvals after changes.
- Give fidelity priority over animation, realism, performance and convenience, in that order. Optimize only in stage 09.
- Mark missing models, references, hardware, fixtures or Blender execution as blocked/assumed; never infer qualification from documentation.

## Research technical rationale

## 03 — Geometry and deformation foundation

**What it does:** Establishes approved geometry, weighting and deformation foundations before building the final control rig.

**How it does it:** Audit mesh boundaries, intentionally layered surfaces, split normals, UV seams, duplicate-looking vertices, weight validity and imported morphs. Do not treat intentional open surfaces or coincident seam vertices as errors by default. Diagnose failures with isolated poses. Normalize only the intended deform-weight set; utility groups for pinning, masks and outlines must not be accidentally normalized with bone weights.

Prepare separate, clearly labeled changes for garment thickness, replacement eyes, proportion corrections, added hidden surfaces or necessary topology work. Provide matched cameras, wireframes, silhouette overlays, face close-ups and representative deformed poses. Finalize substantial topology/proportion changes here. A late request from stage 07 or optimization must return here and invalidate dependent tests, bindings and approvals as appropriate. Blender's shape-key workflow favors stable topology; index-based data transfer also depends on element correspondence. [9,10]

Where imported SDEF/QDEF behavior cannot remain without the importer, compare native Blender deformation candidates rather than silently discarding the difference. Available candidates include ordinary or volume-preserving armature deformation, revised weights, corrective shape keys and targeted Corrective Smooth. Preserve Volume is a Blender option, not a universal proof of SDEF/QDEF equivalence. Corrective Smooth can reduce deformation artifacts but can also alter approved forms. [11,12,13]

**Gate output:** approved geometry and deformation specification, preserved morph inventory, explicit correspondence maps, approved mesh assets/deltas and repair comparisons.

| Action | Allowed? | Condition |
| --- | --- | --- |
| Diagnose geometry and prepare scoped repair candidates | YES | Preserve source and prior approved checkpoint |
| Change topology, weights, normals, eyes, thickness or proportions | REVIEW | Identify each edit and prove affected morph/deformation behavior |
| Delete morphs or merge seams just to simplify conversion | NO | Requires a separately approved scope decision |
| Start broad performance reduction | NO | Optimization belongs in stage 09 |


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
