# 05 — Face controls and animation usability: working procedure

## Routine path

Use the shared face fixture for changed expression combinations, reset/keying and a short human demo. Reserve full qualification for 06; retain actual retarget tests when required. Use PACK/references/workflow.md; retain Cycles-only evidence unless the user explicitly requests another engine. The technical sections below are the focused procedures for the work actually needed, not a requirement to redo unchanged systems.

## 1. Preserve the expression vocabulary

Map source vertex, group, bone, UV and material morphs to native controls explicitly. Shape keys only represent compatible vertex deformations. Record original ranges and intentional asymmetry; do not rename away the source mapping. Preserve neutral Basis and relative-key relationships.

Create independent left/right blink, eye aim, brows, jaw, mouth and approved viseme controls, plus source-specific expressions. Probe 0, midpoint and full range and restore after each test. Check blink+eye aim, smile+jaw, phoneme+blink and brow combinations for eye penetration, tooth/lip intersections and overdriving. Correctives require scoped evidence and the correct owner-stage requalification.

Use simple portable driver variables/expressions for core behavior. Resolve actual data paths and IDs; do not assume duplicate names address the correct shape-key block. Preserve animator overrides. Evaluate controls in a clean process with auto execution disabled. Optional embedded snapping/UI helpers must be disclosed and tested separately.

## 2. Make animation usable

Provide selectable control shapes, collections, lock conventions, keying sets, neutral reset and supported root-motion/in-place behavior. Test reset by comparing evaluated bone/mesh state with the stored neutral state; pressing Alt-G/R/S does not reset custom properties. Ensure test actions and NLA strips are not silently active in the deliverable.

Retarget only named, supplied source skeleton profiles. Record rest pose, units, root scale, bone map and axis corrections. Run a short real clip, foot contact and arm reach checks; a bone-name table alone is not a tested retarget pipeline. If no source profile is requested, document that scoped absence rather than claiming universal support.

Embed a concise animator guide in the blend: entry controls, property ranges, switching, keying, resets, physics handoff and helper requirements. Lip-sync readiness is editable mouth/viseme controls; it does not imply speech recognition.

## Evidence

| Check | Minimum actual evidence |
| --- | --- |
| face-and-visemes | Source/native morph map, neutral/isolated/combined contact sheet and tested control ranges |
| animation-usability | Selection/key/reset/switch tests, root conventions and production-action state |
| retarget-profiles | Requested profile and actual clip results, or explicit approved absence |
| animator-guide | Actual embedded text plus guide procedure replay on the candidate |

## Apply mathematical support

Use bounded shape-delta fitting for known targets and pose-space correctives for reviewed combination faults. Preserve native portable controls; do not treat 2D observations as corresponding 3D vertices or assume independent shape weights sum to one.

Read PACK/references/mathematics.md for the 05 procedure, equations, assumptions, evidence fields and primary references. Use only methods relevant to this fault; preserve the ordered work above. Bundled measurements do not imply the optional solvers were implemented or that a human approved the result.

## Technical references

Consult PACK/references/sources.md for primary documentation matched to the pinned Blender build. Treat formulas and proposed methods here as engineering guidance, not evidence that the character has been qualified.
