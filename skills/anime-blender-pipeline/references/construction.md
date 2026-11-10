# Existing construction tools first

## Scope and tool boundary

The active target is a fully human PMX anime character. Animal ears, tails and kemonomimi conversion/physics are deferred. Preserve such source data if encountered and report the scope mismatch at 00; do not delete it, redesign the character or claim it qualified. This scope does not defer human ears, hair, garments, accessories or applicable soft tissue. If animal features are added in a future scope, apply the same tool-first rule: bespoke work only for a demonstrated requirement that compatible existing tools cannot meet.

Prefer maintained MMD Tools (`mmd_tools`) for import and Rigify for human body control generation. Inspect a compatible existing MMD-to-Rigify bridge before implementing equivalent conversion code. These are construction helpers, not a promise of automatic native conversion. Keep all stages 00–09 and their existing checks/decisions; put tool evidence into those checks rather than adding a tool approval gate.

| Stage | Reuse first | Character-specific work that remains |
| --- | --- | --- |
| 00 | Upstream compatibility information and local capability probe | Exact version lock, source scope, pilot/resource plan |
| 01 | MMD Tools import and source metadata | Correspondence, actual losses, texture/morph/deformation audit |
| 02 | Correct imported image links and usable Cycles nodes | Diagnose actual graph, alpha and reference fidelity |
| 03 | Preserved source topology, weights and shape keys | Only demonstrated local faults; no automatic cleanup |
| 04 | Rigify human metarig/generator; compatible bridge if proven | Anatomical mapping, bind-space verification, grants/twists/accessories |
| 05–06 | Generated controls and inspected optional UI | Full source expression mapping, usability and clean-runtime qualification |
| 07–09 | Accepted shaders, fixtures and native solver facilities | Look review, editable physics, measured performance and portability |

## Lock a combination, not a compatibility slogan

Record exact Blender build, MMD Tools package version/commit, Rigify package/build identity, bridge version/commit if used, install source and import/generation options in the existing environment-lock evidence. Preserve downloadable packages or hashes where permitted. A declared minimum version is only a starting point; operator names and generated data can change. Reuse a working pinned environment rather than upgrading it during conversion.

Upstream reviewed 2026-11-09 (America/Chicago): MMD Tools describes v4.x for Blender 4.2–5.2, but explicitly excludes direct Rigify integration from its core scope. MMD Tools Append documents Blender >=4.2 and MMD Tools >=4.2.1, with an Add Metarig -> Rigify Generate Rig -> Integrate Armatures workflow. Those ranges do not qualify every combination. Use the primary links in sources.md and the actual installed help/source. Rigify generation creates a complete rig, not merely decorative control shapes.

At 00 verify import availability and Rigify generation on a tiny disposable fixture; inspect bridge availability/options if proposing it. This is an environment smoke test, not construction of the character's stage-04 rig before preceding approvals. At 04 test the approved character's arm/leg pilot, rest geometry, controls and dependency behavior before expansion. Keep one Blender workload and bounded pilot renders. Treat the user ceiling of 5 GB RAM and 60% VRAM as planning limits: record the memory metric and device capacity, monitor peak use, and stop/resize the diagnostic workload before crossing them. Do not silently reduce delivered fidelity to fit the budget; report a conflict at the existing gate. If a tool is incompatible, preserve the working import, diagnose the exact failure and try the smallest supported route; do not install every competing tool or rebuild the pipeline.

## Rig construction route

1. Retain the raw import and accepted stage-03 derivative, source bone IDs, weights, shape keys and rest matrices. Keep the metarig and generation settings in the private construction bundle for repeatable regeneration.
2. Prefer a supported bridge that can integrate generated Rigify controls with the proven imported deformation skeleton. Validate anatomical mapping from positions/hierarchy/influences; names alone do not prove it. Inspect integration edits to bones, constraints, drivers and morph targets. Model-specific cleanup options remain off unless the observed model needs them.
3. If evidence shows compatible existing tools cannot meet a specific required integration behavior, record that failure and use a fitted Rigify human metarig with only the smallest explicit native control-to-existing-deform mapping needed for that gap. Preserve bind transforms and existing vertex groups. Do not parent with automatic weights, remesh, delete shape keys or replace the deform skeleton as a default. A replacement needs a demonstrated need, source mapping and affected-stage review.
4. Use generated IK/FK, poles, foot roll and fingers where the configured rig supplies them. Reuse generated switching helpers only after inspecting/testing their execution requirements. Bespoke controls or scripts address a measured missing capability only when demonstrated evidence shows compatible existing tools cannot meet that requirement, not a parallel implementation of all Rigify features.
5. Compare neutral evaluated mesh, bent/twisted limb, mirrored side, switch/reset and source morph combinations. Integration success is a candidate, not acceptance. Preserve imported grants, SDEF/QDEF and morph behavior until a tested native equivalent exists; an add-on callback cannot silently survive as core runtime.

## Native output and helper separation

Generation and integration may use add-ons; core playback, posing and rendering must work in stock Blender with construction add-ons unavailable and auto execution disabled. Inventory generated drivers, handlers, text blocks and custom properties. Retain native constraints/controls and portable drivers that pass the clean test. Rigify's generated UI/snapping Python is a separately disclosed optional helper, not proof that core behavior needs Rigify installed. If a required switch/reset function exists only in the helper, supply and test a native/manual procedure or resolve the dependency before claiming readiness. Do not remove control bones with a de-rigger: the delivered asset is an animation rig.

MMD Tools material/physics output is an inspected starting point. It does not establish Cycles fidelity, grant equivalence, independent simulation suspension or laptop performance. Reuse correct native bodies/joints only when the requested behavior tests pass; add native proxies/solvers for demonstrated gaps. Final runtime checks still belong to 06 and relocated delivery checks to 09. No automatic reweighting, engine substitution, baked-only physics or hidden resource tradeoff follows from choosing these helpers.
