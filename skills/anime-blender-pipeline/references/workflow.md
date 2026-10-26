# Lightweight stage execution — version 3

## Default renderer

Use Cycles for all production materials, reference comparisons, review renders, animation previews and performance evidence. Set scene.render.engine='CYCLES'; use 3D viewport shading.type='RENDERED' with the scene lights/world and the recorded Cycles settings. Blender's Material Preview uses another engine even in a Cycles project: do not select it or build compatibility graphs unless the user explicitly requests it. Do not substitute another engine, an external differentiable renderer or a preview material to meet timing or color targets. Solid/wireframe inspection is permissible for topology/control diagnosis; it is not appearance or benchmark evidence. Record any explicit user-requested engine exception and its scope; keep Cycles final evaluation unless that request changes it.

## Routine path

1. Load the current stage, accepted input and one shared recipe/fixture record. Verify identities and changed dependencies. Re-probe environment facts only after an actual environment change or inconsistent evidence; do not regenerate unchanged inventories.
2. Perform the stage's essential integrity/safety checks and a short relevant Cycles visual or motion demonstration. Keep regional Delta E 00 measurements in materials/final look. Use the accepted camera, masks, color conditions and material roles while their dependencies remain unchanged.
3. If the result is sound, present the compact demonstration at the existing stage gate: 'Does this look/behave right?' Include candidate ID, meaningful deltas, required-check results and limitations. Ask selection or critique, with 'neither' allowed. Do not ask separate permission for each reversible parameter adjustment.
4. Expand only an observed or uncertain fault into the stage's full diagnostic ladder or bounded mathematical search. Stop after two non-improving experiments and restore the best draft. Human feedback guides the repair; it never fabricates a numerical pass.
5. Register the exact final candidate and required assets, record canonical checks and preserve the actual human decision. Keep all ten stage handoffs and the three-candidate cap.

## Reuse evidence without misrepresenting it

Maintain one versioned camera/color recipe and one motion/face fixture suite. Stages 04/05 use local smoke tests; 06 performs full motion qualification; 07/08/09 repeat only affected cases plus the critical final checks. A reused result needs the original passing evidence, matching relevant component/fixture/environment hashes, and a new compact current-candidate report explaining why the checked behavior is unaffected. A changed whole-file hash does not alone prove a component changed or remained equal. Use semantic fingerprints/explicit dependency records for that decision.

Never copy old approvals or relabel old evidence as a new execution. New evidence must bind the current bundle through the ledger; stale identities, changed masks/camera/lighting/graph/geometry/rig/timebase/dependencies invalidate the related results. If unchanged behavior cannot be established, run its test. Source/approved artifact hash verification remains mandatory and is not a costly environment probe to skip.

## Stage-specific reductions

- 00: confirm camera/scope once and preserve the recipe; re-fit only changed references, framing, pose or geometry dependencies.
- 01: preserve a correct import; verify correspondence/losses, show the short import review and retain its inventory.
- 02: use verified existing maps/graph, regional color checks and a Cycles review first. Run the complete diagnostic ladder for faults or uncertain roles, not every correct material. Keep alpha/eye/shadow checks distinct.
- 03: if no geometry change is needed, produce a no-change integrity/correspondence report and the existing gate; do not manufacture a repair or reweighting task.
- 04/05: build/test the actual changed controls/face combinations with the shared fixtures. Do not duplicate the entire 06 qualification suite here.
- 06: run the shared qualification suite, including held-out cases, evaluated deformation and clean native runtime.
- 07: reuse accepted camera/maps/color definitions. Check changed look regions and critical face/eye/silhouette regressions; expand new faults rather than repeat all material discovery.
- 08: show a short cold-reset/settle/turn/landing demonstration and receive motion critique before expensive inverse fitting. Still prove collision/stretch/stability, real category suspension and manual fallback.
- 09: run actual audit and changed-system regressions; use the two decisions below. Portability and final target-machine evidence remain actual checks, not inherited aesthetic judgments.

## Two stage-09 decisions

1. **audit**: present audit results plus the concrete optimization plan or 'not needed' disposition together. Record one observed human decision with `review --gate audit`. This allows the selected bounded work, not arbitrary future redesign. Preserve this historical decision across revisions; if scope/quality tradeoffs change, obtain a fresh audit decision and invalidate delivery.
2. **delivery**: after any work, repeat affected tests and the final clean-package/Cycles/performance checks, register the final bundle and submit it. Present the exact final result for one human decision covering re-audit, delivery and stage-09 acceptance. `review --gate delivery` records that decision and atomically approves stage 09 after verifying checks, current bundle and submission snapshot. Do not ask a third final-approval question or run approve again.

Do not record either decision on worker authority or infer it from the current request to update skills. This request authorizes skill changes, not approval of a future character. A failed/blocked required check remains visible; an explicit scoped requirement change must be recorded separately and cannot silently rewrite frozen policy.

## Version boundary

Version 3 changes stage-09 approval semantics and the benchmark renderer. Start new v3 runs with explicit lineage; retain v1/v2 runs and their tools unchanged. Never modify a historical run's version/policy or import its approvals. A correct earlier imported blend may be used as a source in the new run with fresh affected review; another import is not automatically required. New Cycles Rendered viewport timings cannot inherit an old Material Preview performance pass. Keep 24 FPS off / approximately 12 FPS cold active as desired goals, pin actual samples/denoising/device/viewport and qualify anew; do not promise they are met.
