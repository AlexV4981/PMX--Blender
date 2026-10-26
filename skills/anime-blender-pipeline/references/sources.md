# Primary technical references

Use documentation for the exact pinned build, not a moving latest version. These sources describe capabilities; project procedures, formulas, acceptance gates and character-specific choices are engineering guidance. A documentation link is not evidence a graph or solver was run. If a versioned page is unavailable, inspect the actual Blender API/help and record the limitation rather than inventing properties.

## Material diagnosis (02 and 07)

- [Image Texture](https://docs.blender.org/manual/en/4.5/render/shader_nodes/textures/image.html): projection, color/data interpretation and image sampling.
- [Image settings](https://docs.blender.org/manual/en/4.5/editors/image/image_settings.html): image-datablock color space and alpha interpretation.
- [Color management](https://docs.blender.org/manual/en/4.5/render/color_management.html): scene-linear processing and view transforms.
- [Normal Map](https://docs.blender.org/manual/en/4.5/render/shader_nodes/vector/normal_map.html): tangent/object/world normal conventions and UV basis.
- [Toon BSDF](https://docs.blender.org/manual/en/4.5/render/shader_nodes/shader/toon.html): Cycles-only shader; not a general game shader replica.
- [Shader to RGB](https://docs.blender.org/manual/en/4.5/render/shader_nodes/converter/shader_to_rgb.html): Eevee-only lighting conversion; cannot supply Cycles shading.
- [Material Output API](https://docs.blender.org/api/4.5/bpy.types.ShaderNodeOutputMaterial.html): actual target/output properties.
- [Solidify](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/solidify.html) and [Freestyle](https://docs.blender.org/manual/en/4.5/render/freestyle/introduction.html): different outline construction/render methods.

## Import, geometry, rig and controls (00–06)

- [Maintained MMD Tools](https://github.com/MMD-Blender/blender_mmd_tools): pin an actual compatible release/commit; inspect documented limitations and source behavior.
- [Blender shape keys](https://docs.blender.org/manual/en/4.5/animation/shape_keys/introduction.html): relative keys and topology assumptions.
- [Armature modifier](https://docs.blender.org/manual/en/4.5/modeling/modifiers/deform/armature.html): vertex groups and Preserve Volume; not evidence of SDEF/QDEF equivalence.
- [Corrective Smooth](https://docs.blender.org/manual/en/4.5/modeling/modifiers/deform/corrective_smooth.html): targeted correction with bind/rest considerations.
- [PoseBone API](https://docs.blender.org/api/4.5/bpy.types.PoseBone.html), [Bone API](https://docs.blender.org/api/4.5/bpy.types.Bone.html) and [Object.convert_space](https://docs.blender.org/api/4.5/bpy.types.Object.html#bpy.types.Object.convert_space): distinguish rest, pose, local and world transforms.
- [Driver troubleshooting](https://docs.blender.org/manual/en/4.5/animation/drivers/troubleshooting.html): driver execution/dependency limitations.

## Native physics and delivery (08–09)

- [Surface Deform](https://docs.blender.org/manual/en/4.5/modeling/modifiers/deform/surface_deform.html): transfer binding constraints and deformation.
- [Cloth shape/pins](https://docs.blender.org/manual/en/4.5/physics/cloth/settings/shape.html) and [collisions](https://docs.blender.org/manual/en/4.5/physics/cloth/settings/collisions.html): attachment and solver settings are specific to cloth.
- [Soft-body goals](https://docs.blender.org/manual/en/4.5/physics/soft_body/settings/goal.html): goal weights/behavior are not cloth stiffness values.
- [Generic spring](https://docs.blender.org/manual/en/4.5/physics/rigid_body/constraints/types/generic_spring.html) and [Rigid Body World](https://docs.blender.org/manual/en/4.5/physics/rigid_body/world.html): constraints, collections and shared-world behavior.
- [Timeline playback](https://docs.blender.org/manual/en/4.5/editors/timeline.html): synchronization/frame-dropping settings must be included in performance evidence.
- [Packed data](https://docs.blender.org/manual/en/4.5/files/blend/packed_data.html): asset packing does not replace relocated clean-open tests.

During this rewrite, official indexed documentation confirmed the Toon/Cycles and Shader-to-RGB/Eevee distinction and image color/alpha concepts. Some direct versioned manual fetches were unavailable. No API or Blender behavior was qualified by a live run here. Test every required feature in the actual pinned Blender build.

## Mathematical methods

See [mathematics.md](mathematics.md) for stage mapping, assumptions and the primary references for robust fitting, CIEDE2000, rigid alignment, ARAP, skinning, expression fitting, inverse simulation and human preference models. The documented external solvers are not bundled Blender implementations.

## Cycles viewport scope

- [Blender viewport shading](https://docs.blender.org/manual/en/4.4/editors/3dview/display/shading.html): Rendered mode uses the scene engine; Material Preview is not a Cycles substitute.
- [Blender Eevee developer documentation](https://developer.blender.org/docs/features/eevee/): Material Preview uses Eevee even for a Cycles project. The default workflow therefore uses Cycles Rendered viewport and builds no alternate-engine graph.
