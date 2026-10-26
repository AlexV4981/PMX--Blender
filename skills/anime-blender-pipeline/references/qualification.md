# Qualification and evidence

## Qualification levels

1. Skill-format validated: metadata, links and instruction structure pass static checks.
2. Utility-tested: ledger and parser behavioral tests pass on synthetic data. This is not Blender/model qualification.
3. Blender-fixture qualified: pinned Blender/add-on build has actually run native graph, import, morph, rig and physics fixtures.
4. Character-qualified: one real model completed human gates with approved recipe/assets.
5. Cross-machine replay-qualified: same sources/recipe reproduced equivalent results on a second machine within approved tolerances.
6. Feature-family qualified: structurally different characters exercise claimed face, hair, garment, rig and PMX variations.

Report the actual level and individual tools/features tested. Do not advance the label because an agent or user likes the documentation. Version 2 authoring environment lacked Blender and supplied real models; native .blend/shader, complete conversion and laptop performance were not tested there.

## Script checks

    python3 -m unittest discover -s "$PACK/scripts/tests" -v
    python3 "$PACK/scripts/blender_tools.py" validate-seeds

Run the skill creator quick validator on all eleven skills after edits. Check local reference links, UI metadata, exact required-check names and Python syntax. Keep user files and production scenes out of utility tests. Tests of approval logging simulate a human decision; they are not actual project approvals.

## Required Blender fixture work

- Verify pinned importer options, texture paths/color spaces, alpha, shared toon handling, flags, additional UVs and morph interpretation.
- Exercise BDEF/SDEF/QDEF cases and document actual supported behavior and native replacements. Do not assume their equivalence.
- Render native seed groups, face/eye/hair/outline candidates in Cycles. Verify useful Material Preview separately, including renderer-specific outputs when used.
- Test original-to-native deformation correspondence, weights, normals, shape keys, IK/FK and parent switches; diagnose dependent Python.
- Test each native physics method, one-way evaluation, collision scope, real category-disable behavior and reset/preroll. Deliver no baked-only systems.
- Relocate and clean-open the resulting .blend without construction add-ons. Test core controls with automatic Python disabled and approved embedded convenience helpers separately.

## Laptop benchmark

Record exact GPU, Blender build, driver, OS, power/thermal state, UI scaling and viewport pixel dimensions. Baseline: Nitro V Ryzen 5 7535HS, 16 GB RAM, 6 GB VRAM. Use a fixed full-character scene and motion fixture. Proposed initial fixture: 240 measured frames, three repetitions, Material Preview, 24 FPS scene timebase; obtain stage 00 approval of the exact profile.

Use actual completed UI redraw/evaluation timing with Play Every Frame, no dropped frames. Normal 24 FPS capped playback cannot establish throughput above that cap. Qualify an uncapped UI redraw-driven stepping method that keeps scene FPS fixed, and cross-check against observed playback; do not increase scene FPS to uncap a test because this changes simulation timing. A background frame_set loop is not a viewport test.

Compile shaders first and report initialization separately. Clear simulation caches and run sequentially for each cold active-physics repetition; report prereoll/time separately. Distinguish cached playback explicitly. Count completed frames/elapsed wall time. Report aggregate and per-repetition averages, frame-time percentiles, longest stalls/segments, peak RAM/VRAM and evidence of actual enabled categories.

Physics-off average must reach >=24 FPS. Cold active physics targets approximately 12 FPS. Flag sustained near-1-FPS behavior; calibrate precise stall-duration rules using the pilot and obtain human agreement. Do not turn 12 into an invented hard minimum or let a favorable average conceal severe pauses. Preserve the user's priority order when performance conflicts.

## Numerical and visual comparisons

Use exact hashes for source/approved file identity and direct array comparisons with unit-aware tolerances for evaluated geometry/bones/UVs/normals. Hashing rounded floats is not tolerance testing. Normalize geometric displacement by approved character height, record angular differences and compare switching endpoints.

Use matched cameras/lights/world/color management and region masks for silhouette and color metrics. If using Delta E, name the formula, RGB/Lab conversion, white point, masks and statistic. Use the user-requested provisional Delta E 00 <3 target under the conditions in mathematics.md; it is not a universal guarantee against screenshots of unknown rendering conditions. Propose per-region p95, report tails/maximum and calibrate masks/statistic with the human before treating it as acceptance. Keep unknown-condition comparisons diagnostic.

Measure native physics settling time, part-length-normalized travel, stretch, penetration and stability under the exact reset/preroll/motion settings. No baked delivery is necessary to retain audit clips and numeric evidence. Simulation numerical differences across platforms use tolerances, not exact moving-vertex hashes.

## Failure and acceptance

Record pass/fail/blocked per feature, not a single score. Mark assumptions and unsupported losses. For every candidate, provide side-by-side visual/geometry differences and affected motion tests. Ask the human to choose or critique; preserve at most three IDs. Escalate hard inability to produce a candidate to actual Astra, then return unresolved avenues if needed.


## Version 2 instruction and utility validation

Thirty pure-Python tests exercise ledger/PMX behavior and diagnostic records/raw channel observation. Independent task simulations check how the rewritten materials and rig/physics procedures handle ambiguous inputs and unavailable Blender. This is instruction-level evaluation only. No Blender, model, hardware or replay qualification is implied. The material plan validator does not verify artistic truth, graph equivalence, or screenshot fidelity.

## Mathematical integration qualification

The combined utility suite now has 41 tests. CIEDE2000 matches 20 selected published Sharma/Wu/Dalal reference cases within their four-decimal rounding tolerance, including zero-chroma and hue wraparound. Tests also exercise declared sRGB conversion, visible error tails, reflected/degenerate rigid alignment, quaternion sign equivalence and evidence prerequisites. These qualify the numerical helper on those cases, not image registration, camera/rig fitting, external solvers, real Blender scenes or artistic fidelity. Existing Blender/hardware limitations remain.
