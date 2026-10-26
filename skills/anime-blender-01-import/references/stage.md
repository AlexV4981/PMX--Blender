# 01 — Import and loss inventory: working procedure

## 1. Preserve the import that works

Run the read-only PMX inventory before Blender import. Read exit status: partial inventory remains partial. Extract a working copy preserving Unicode paths; preserve the original archive. Record every importer option and unavoidable conversion. Import once without merge-by-distance, triangulation changes, decimation, normal recalculation or automatic rig rebuilding.

Save a raw import baseline and inspect its beauty, flat-texture and neutral-gray views in separate test derivatives. Record missing image paths before relinking. Resolve exact PMX relative paths first; basename alone is ambiguous when multiple files share a name. Log source ID, original path, resolved path and content hash. Do not substitute a visually similar texture.

## 2. Build correspondence

Compare material face counts, vertex/loop counts, UV layers, split/custom normals, deform groups, bone hierarchy/local axes, grants, IK, morph types, edge data, bodies and joints. Track stable PMX indices plus Blender object/data/material identifiers; translated names are labels, not unique IDs. If importer duplication or reindexing occurs, document its mapping before any indexed edit.

Test basis and representative morph extremes. Material/UV/group/bone morphs are not all vertex shape keys. Inventory additional UV and material morph dependencies even if not immediately visible. Distinguish SDEF from QDEF; record actual importer support and native-replacement work, without silently converting either to generic skinning.

## 3. Attribute losses accurately

Classify each feature as preserved, transformed, approximate, unsupported or unknown with evidence. Pink can mean missing files, decoding failure or graph/output trouble; it does not automatically mean broken UVs. Separate importer viewport appearance from final Cycles correctness. Do not delete imported helpers or callbacks until their purpose and native replacement are understood.

If the import is already structurally correct, preserve it. Stage 02 begins by diagnosing materials on this exact checkpoint, not reimporting or cleaning the mesh.

## Evidence

| Check | Minimum actual evidence |
| --- | --- |
| import-inventory | Source/import counts and explicit source-to-Blender correspondence |
| feature-loss-report | Feature-by-feature status, morph/deformation exceptions and owner |
| texture-dependencies | Exact resolved image hashes, ambiguity/missing-file list |
| baseline-integrity | Saved raw import, settings and front/side/face diagnostic images |

## Technical references

Consult PACK/references/sources.md for primary documentation matched to the pinned Blender build. Treat formulas and proposed methods here as engineering guidance, not evidence that the character has been qualified.
