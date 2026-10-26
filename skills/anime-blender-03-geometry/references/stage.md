# 03 — Geometry and deformation foundation: working procedure

## 1. Diagnose without cleanup

Inspect deliberate disconnected layers, open garment boundaries, mirrored UVs, coincident seam vertices, custom split normals, vertex order, shape keys and deform/utility groups. Nonmanifold does not mean broken for game characters. Render neutral diffuse and normal diagnostics to distinguish shading-normal faults from topology faults. Preserve stylized facial normals unless a specific edit is justified by matched evidence.

Test the isolated offending pose before editing. Record source IDs, vertex/loop correspondence, affected groups and material/UV ownership. Measure a deformation problem on the evaluated mesh, not only the undeformed datablock.

## 2. Repair the correct cause

For linear skinning p'=sum_i(w_i M_i p), M_i must include the correct bind/rest transform into a common space. Check armature object transforms, parent inverse, bone rest matrices and duplicate Armature modifiers before changing weights. Normalize only actual deform groups: w'_i=w_i/sum(w_deform). For an unweighted vertex (sum=0), identify the intended bone; do not divide by epsilon and invent a binding. Preserve cloth pins, masks, outline weights and selection groups.

Compare ordinary Armature, Preserve Volume and localized corrective solutions for SDEF/QDEF replacement; none is automatically equivalent. Test twist and bends before choosing. Keep nondeforming regions unchanged. A smoothing modifier can conceal bad weights while changing the silhouette; require an isolated comparison.

For relative shape keys evaluate p=p_basis+sum_k(v_k*(p_k-p_relative(k))) under the actual relative-key chain. Topology edits must preserve index correspondence across all keys or reconstruct and test an explicit transfer. Never discard keys to allow merge/subdivision/apply. Verify Basis and every imported expression individually plus relevant combinations.

## 3. Handle artistic changes as individual proposals

For thickness, proportions, eyes or hidden surfaces, show one isolated delta with wireframe, silhouette and deformed views. Add thickness after the appropriate deformation stage and check self-intersection; do not inflate eyelashes or layered face shells. Preserve source UVs and custom normals. Defer stylistic redesign and global simplification.

## Evidence

| Check | Minimum actual evidence |
| --- | --- |
| geometry-change-comparisons | Scoped vertex/normal/UV/topology deltas, wireframes and matched visual comparisons |
| morph-integrity | Key names/counts, correspondence, basis reset and individual/combined extremes |
| deformation-tests | Original versus repaired isolated poses, evaluated displacement/collapse and silhouette checks |
| correspondence-map | Exact source/import/final indices or tested transfer with failures disclosed |

## Technical references

Consult PACK/references/sources.md for primary documentation matched to the pinned Blender build. Treat formulas and proposed methods here as engineering guidance, not evidence that the character has been qualified.
