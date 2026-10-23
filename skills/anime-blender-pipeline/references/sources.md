# Primary sources and version verification

Use these as technical references, not proof the pack's implementation has passed. Verify APIs/options in the pinned Blender build before writing model-specific scripts. Record source/retrieval date for new decisions.

- [Blender 4.5 LTS](https://www.blender.org/releases/4-5/): proposed initial qualification branch; pin exact patch/build rather than moving latest.
- [Maintained MMD Tools](https://github.com/MMD-Blender/blender_mmd_tools): importer compatibility, scope and documented MMD IK/physics differences.
- [Upstream MMD feature documentation](https://github.com/powroupi/blender_mmd_tools/wiki/MMD_TOOLS-LIST-OF-FEATURES-AND-BRIEF-TUTORIAL-INFORMATION-FOR-FEATURES): SDEF and historical data preservation; recheck current implementation.
- [Toon BSDF](https://docs.blender.org/manual/pt/4.5/render/shader_nodes/shader/toon.html) and [Shader to RGB](https://docs.blender.org/manual/id/4.0/render/shader_nodes/converter/shader_to_rgb.html): different render-engine support.
- [Renderer-specific material outputs](https://docs.blender.org/api/4.5/bpy.types.ShaderNodeOutputMaterial.html) and [Material Preview design](https://archive.blender.org/developer/differential/0005/0005612/index.html).
- [Color management](https://docs.blender.org/manual/en/4.4/render/color_management.html): view transforms and color interpretation.
- [Shape-key topology guidance](https://docs.blender.org/manual/nl/4.5/animation/shape_keys/introduction.html), [Data Transfer](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/link_transfer/transfer_mesh_data.html), [Corrective Smooth](https://docs.blender.org/manual/es/4.5/modeling/modifiers/deform/corrective_smooth.html).
- [Rigify generated features](https://docs.blender.org/manual/en/4.5/addons/rigging/rigify/rig_features.html), [native constraints](https://docs.blender.org/manual/en/4.5/animation/constraints/introduction.html), [driver execution](https://docs.blender.org/manual/nl/4.5/animation/drivers/troubleshooting.html).
- [Surface Deform](https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/surface_deform.html), [cloth pins](https://docs.blender.org/manual/id/4.5/physics/cloth/settings/shape.html), [soft-body goals](https://docs.blender.org/UATEST/manual/en/4.5/physics/soft_body/settings/goal.html), [spring constraints](https://docs.blender.org/manual/uk/4.5/physics/rigid_body/constraints/types/generic_spring.html).
- [Cloth collisions](https://docs.blender.org/manual/nl/4.5/physics/cloth/settings/collisions.html), [rigid-body world](https://docs.blender.org/manual/en/latest/physics/rigid_body/world.html), [baking/caches](https://docs.blender.org/manual/en/5.0/physics/baking.html).
- [Timeline playback modes](https://docs.blender.org/manual/en/4.5/editors/timeline.html), [relative paths/packing/missing files](https://docs.blender.org/manual/fi/4.5/interface/window_system/topbar.html).
- [Official OpenAI model guidance](https://learn.chatgpt.com/docs/models) and [Codex subagents/custom agent configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents): validate actual model availability and role settings. Skill text alone does not select the current parent model.

Some historical/manual translation pages are retained because they describe a researched behavior. Do not treat historical documentation as an unconditional claim about a different installed version. No upstream game-character, rig, toon-texture or add-on binaries are redistributed in this pack.
