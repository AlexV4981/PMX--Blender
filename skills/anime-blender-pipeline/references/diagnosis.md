# Diagnose before editing

## Use an evidence loop

Record: observed symptom, exact object/material/frame, baseline file, competing explanations, smallest distinguishing test, one proposed variable, expected observable effect, result, rollback and next decision. Read actual pixels and evaluated data. Do not make ten unrelated edits and interpret the final image as confirmation of all ten hypotheses.

Preserve a correct subsystem. Begin shader repair from the working import, not from a new import or a universal material replacement. Keep one .blend writer. Use private drafts with unique saved paths. At two consecutive non-improving experiments restore the best draft and revisit the diagnosis; escalate unfamiliar implementation to the capable role. This is a diagnostic stop rule, not a new human permission gate. Candidate selection gates remain in the contract.

## Distinguishing tests

| Symptom | Plausible causes | First useful tests | Unjustified compensation |
| --- | --- | --- | --- |
| Pink material | Missing path, image decode, wrong node/output | Exact resolved path/hash, open image, active output graph | Repaint or re-UV the model |
| Washed-out/dark color | View transform, duplicate gamma, wrong map/tint, illumination | Fixed display settings, emission texture-only, texture*tint | Global saturation/gamma or brighter light |
| Dirty anime face shadows | Custom normals, normal map/basis, geometry, light placement | Neutral diffuse, isolate maps, light/head rotation | Airbrush shadows into albedo |
| Cutout fringes | Alpha role/association, RGB under alpha, UV/filtering | Channel inspection on light/dark checker, opaque comparison | Hard threshold everywhere |
| Dark/disappearing eyes | Layering, refraction, normals, output, occlusion | Isolate eye layers with same camera/light | Replace eyes or make all hair transparent |
| Rig collapses | Bind/rest spaces, duplicate skinning, weights | Rest comparison, single bone/axis, modifier isolation | Weight paint the whole model |
| Limb flips | Pole degeneracy, roll, constraint space | Bent/rest-plane pole test, one-axis rotation | Random pole angle offsets on every pose |
| Physics explosion | Intersections, scale, pinning, dependencies, solver time | Rest proxy and one-panel cold reset | Extreme damping/quality everywhere |
| Physics toggle does little | Visibility only, shared solver still active | Verify evaluated solver state and actual cost | Declare disabled from a hidden output |

## Change ownership

02 owns material graph/image interpretation and diagnosis; 03 owns mesh/UV/custom-normal/shape topology and weights; 04 owns control/rest/constraint architecture; 05 owns animator interface and face wiring; 06 owns tests; 07 owns final look calibration; 08 owns simulation proxies/attachments; 09 owns audited performance tradeoffs. A cause can cross ownership: prepare the minimal reproduction, route the edit and requalify downstream effects. Stage ownership must not prevent investigating a cause.

## Use evidence with the right strength

A source hash proves bytes. A plan validator proves required fields are present. A successful render proves a render completed. Neither plan nor render proves visual fidelity. An image comparison supports only its camera/light/pose. A reference screenshot with unknown shader inputs cannot uniquely identify a game material. State approximate reconstruction and its limits honestly.

Do not write placeholders as evidence, auto-pass a stage from utility tests, or treat a human's selection of a direction as approval of unresolved defects. Keep missing evidence visible.
