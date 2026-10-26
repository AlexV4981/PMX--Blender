# 04 — Native control rig: working procedure

## 1. Preserve the proven deform skeleton

Map anatomical roles using rest positions, hierarchy and influence regions; Japanese/English bone names are hints. Keep the imported deform skeleton/rest bind where it works. Build separate control/mechanism bones rather than rebuilding and reweighting everything. Inventory grants, twist, IK, SDEF callbacks and morph dependencies before removal.

Write a directed dependency graph: controls -> mechanisms -> deform bones -> mesh. No mechanism may depend on the mesh it drives. Declare coordinate/constraint spaces, parent inverses, rotation modes, scale inheritance and reset values. Maintain source-to-final correspondence and compare evaluated rest geometry before animation.

## 2. Solve spaces mathematically

A bone's rest world matrix is armature.matrix_world @ bone.matrix_local. A world target converted to armature space uses armature.matrix_world.inverted() @ target_world; constraint evaluation additionally depends on pose/parent/rest spaces. Do not copy matrix_basis or Euler angles between unrelated spaces. Verify each conversion with a single-axis test before combined rotations. PMX grant ratios, local grants and negative rotation ratios are not generally identical to Copy Rotation influence. Use measured native equivalents and document approximations.

For a limb with shoulder/hip A, elbow/knee B and hand/ankle C, project B onto line AC: D=A+dot(B-A,C-A)/dot(C-A,C-A)*(C-A). Pole direction is normalize(B-D). If the limb is nearly straight the direction is unstable; use an approved rest-plane fallback. Determine pole angle from bone axes by fixture, not an assumed +/-90 degrees. Guard zero-length limbs and target distances. Stretch defaults off.

## 3. Build and prove the interface

Provide root/world/COG, spine/head, limbs with IK/FK, poles, foot roll/toes, fingers and applicable accessories. Start with one arm and one leg. Test the mirrored side independently because roll and local axes differ. Add remaining controls only after pilot switching and reset work.

For IK/FK switching, sample evaluated world matrices before switching, solve destination controls in their spaces, switch, then compare endpoints and intermediate joints. Test at several bent/twisted poses and keyed frames. Parent/space switching must preserve world pose. Report translation normalized by height and quaternion angle 2*acos(clamp(abs(dot(q0,q1)),0,1)). Never conceal a switch pop by changing the test pose.

Rigify may construct a rig, but generated Python UI and snapping are separate dependencies. Core posing must pass in stock Blender with auto execution disabled. Do not delete the original rig until all affected functions pass.

## Evidence

| Check | Minimum actual evidence |
| --- | --- |
| control-capabilities | Tested checklist, control selection/reset, one-arm/leg pilot and full rig |
| rig-integrity | Rest/evaluated mesh comparison, space/dependency map, target/driver/cycle diagnostics |
| switching-demonstrations | Actual pre/post matrices and rendered/keyed IK/FK and space switch fixtures |
| runtime-dependencies | Exact add-on/driver/text/handler dependencies and clean native posing test |

## Technical references

Consult PACK/references/sources.md for primary documentation matched to the pinned Blender build. Treat formulas and proposed methods here as engineering guidance, not evidence that the character has been qualified.
