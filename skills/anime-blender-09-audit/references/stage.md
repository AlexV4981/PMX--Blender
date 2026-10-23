# Stage 09 implementation checklist

Read this with the live shared contract. Treat the research excerpt below as technical rationale, not a claim of implementation or authority over newer user rules.

## Execute and verify

1. Run 09A audit and obtain explicit human acceptance of exact report/checkpoint before optimization decisions.
2. Calibrate pilot stall/tolerance limits with human; retain physics-off >=24 FPS and cold-physics approximately 12 FPS targets.
3. Measure UI redraw-completed frames in Material Preview using Play Every Frame, fixed viewport and scene 24 FPS.
4. Run three repeats on stated laptop/power setup; separate cold physics, pre-roll, warm/off and cached statistics.
5. Obtain 09B human approval of exact optimization plan/candidate if needed; optimize only measured costs and disclose quality tradeoffs.
6. Run 09C re-audit of every affected visual, deformation, physics, portability and performance check; require human gate.
7. Relocate package, open fresh stock Blender without construction add-ons; test basic posing with automatic Python disabled.
8. Run 09D clean-package review; deliver editable .blend, relative dependencies, embedded guide, cleared caches and exact approved recipe.

## Binding policy updates

- Execute through Codex. Use Sol 6.1 High for orchestration and difficult implementation, Sol 6.1 Light for routine work, and Astra when High produces no usable candidate.
- Keep at most three active candidates; prepare only the one to three needed. Ask the user to select or critique each exact submission.
- Allow third-party add-ons and embedded Python during construction. Deliver addon-free core behavior except a hyperspecific runtime add-on exception supported by ten distinct documented failed alternatives and explicit human approval of the exact exception; stop early when an alternative works.
- Disclose and review embedded Python; keep basic native posing independent of unapproved runtime add-ons. Inspect required script behavior separately from add-on installation.
- Keep source and approved checkpoints immutable; use descendants and invalidate dependent approvals after changes.
- Give fidelity priority over animation, realism, performance and convenience, in that order. Optimize only in stage 09.
- Mark missing models, references, hardware, fixtures or Blender execution as blocked/assumed; never infer qualification from documentation.

## Research technical rationale

## 09 — Final audit, approved optimization and delivery

**What it does:** Demonstrates quality and laptop usability, allows reviewed optimization, then proves the package is independent of the build environment.

**How it does it:** Treat the stage as four explicit human gates: 09A audit → 09B approve optimization plan/candidate if needed → 09C re-audit → 09D approve delivery. If no optimization is necessary, omit the optimization work, not the final clean-package test or human acceptance.

**09A benchmark proposal:** One full character with all intended visible pieces, a fixed floor/prop test scene, Material Preview, fixed 1920×1080 viewport area or an explicitly approved measured substitute, fixed HDRI/lighting/overlays and 24 FPS project timebase. Record the exact viewport pixel area and UI scaling. Use wall-clock timing of actually evaluated/displayed frames with Play Every Frame, not frame dropping or a background-only frame_set loop. Blender's timeline can drop frames to maintain time, which would invalidate a naive displayed-FPS claim. [27]

Use an approved 240-frame motion fixture, plus recorded pre-roll for the physics-on run. Proposed qualification protocol: three repetitions, laptop plugged in, performance/power state recorded, shaders compiled before measurement. Physics-off runs can be warmed; physics-on runs must begin from a cleared simulation cache and run sequentially. Report initialization/pre-roll separately. A cached second pass is a separate statistic, never the active-calculation result. Preserve the simulation timebase: the scene remains 24 FPS even if wall-clock computation averages 12 FPS. Normal playback at a 24 FPS cap cannot measure throughput above that cap. Qualify an additional UI redraw-driven, uncapped stepping harness that retains the 24 FPS scene timebase, counts only completed viewport updates, and is checked against observed UI playback. Do not raise scene FPS to make the benchmark uncapped, because that changes simulation timing. This measurement harness remains an implementation task, not a tested tool supplied with this report.

Average FPS = counted completed frames / elapsed seconds. Also report frame-time percentiles, longest stall, segment-level averages, peak RAM/VRAM and thermal/power context. Report every repetition, with aggregate/minimum as well as average. Physics-off acceptance is ≥24 FPS over the agreed test; physics-on is approximately 12 FPS target with severe sustained stalls explicitly flagged. Precise stall-duration and tolerance limits are calibrated in the pilot and approved by the human; the research does not invent validated values.

**09B optimization:** Diagnose measured costs before changing the character. Candidate order: remove confirmed duplicate work/dead dependencies; improve simulation/collision proxies and unnecessary interactions; evaluate control/constraint overhead; introduce explicitly labeled viewport-only simplification while retaining final Cycles quality; change visible geometry/textures/physics quality only as an individually reviewed tradeoff. Preview simplification must not conceal an unmeasured lower-quality configuration. No decimation, texture reduction, deleted soft tissue, disabled collisions or downgraded fidelity can silently produce a performance “pass.”

**09C re-audit:** Repeat every affected visual, deformation, physics, portability and performance test, not just the fastest FPS clip. If a change alters topology, correspondence or simulation bindings, return to the owning stage and rebuild downstream approvals as required. If the laptop target and approved quality cannot both be met, report the conflict; do not quietly reverse the user's priority order.

**09D delivery:** Make required rig/material data local or package dependencies intentionally. Store external textures under relative paths and run missing-file checks. Open the package from a different directory in a fresh stock-Blender profile with construction add-ons unavailable. Test core posing with automatic Python disabled; document any approved optional embedded helper functionality separately. Check that there are no required external modules, user-specific paths or unresolved linked reference models. Blender provides packing, relative-path and missing-file tools, but the relocated clean-open test is still required. [28]

Deliver the editable character in a neutral, documented animation-ready state, with an embedded guide identifying controls, physics toggles, reset/pre-roll procedure, supported retargeting profiles, known limits and tool/recipe versions. Clear simulation caches; do not delete simulations. Keep test actions/fixtures in the audit package or clearly separated so they do not unexpectedly drive the production character.

**Gate output:** final .blend and relative dependencies; audit evidence; approved recipe and fingerprints; animation/physics guide; final human acceptance.

| Action | Allowed? | Condition |
| --- | --- | --- |
| Audit, benchmark and propose a measured optimization plan | YES | All test settings disclosed |
| Change evaluation structure or viewport/physics/asset quality | REVIEW | Side-by-side evidence and regression tests required |
| Deliver baked-only physics or unapproved required runtime add-ons | NO | Any hyperspecific add-on exception needs ten distinct documented failed alternatives and explicit human approval |
| Hide physics, drop frames or change the benchmark to claim a pass | NO | Report the actual configuration and result |


## Sources

Primary documentation consulted; source pages describe Blender/MMD capabilities, while pipeline choices and approval rules above are proposed for this project.

1. [Blender 4.5 LTS release/support](https://www.blender.org/releases/4-5/)
2. [Maintained MMD Tools repository: compatibility and known IK/physics limitations](https://github.com/MMD-Blender/blender_mmd_tools)
3. [Blender color management](https://docs.blender.org/manual/en/4.4/render/color_management.html)
4. [Upstream MMD Tools feature documentation, including SDEF](https://github.com/powroupi/blender_mmd_tools/wiki/MMD_TOOLS-LIST-OF-FEATURES-AND-BRIEF-TUTORIAL-INFORMATION-FOR-FEATURES)
5. [Toon BSDF, Blender 4.5](https://docs.blender.org/manual/pt/4.5/render/shader_nodes/shader/toon.html)
6. [Shader to RGB limitations](https://docs.blender.org/manual/id/4.0/render/shader_nodes/converter/shader_to_rgb.html)
7. [Blender developer documentation: Material Preview uses Eevee](https://archive.blender.org/developer/differential/0005/0005612/index.html)
8. [Blender 4.5 API: Material Output renderer targets](https://docs.blender.org/api/4.5/bpy.types.ShaderNodeOutputMaterial.html)
9. [Shape-key introduction and topology guidance](https://docs.blender.org/manual/nl/4.5/animation/shape_keys/introduction.html)
10. [Data Transfer topology/index mapping](https://docs.blender.org/UATEST/manual/en/4.5/modeling/modifiers/modify/data_transfer.html)
11. [Armature modifier and Preserve Volume](https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/armature.html)
12. [Corrective Smooth](https://docs.blender.org/manual/es/4.5/modeling/modifiers/deform/corrective_smooth.html)
13. [Driver workflow and corrective shape keys](https://docs.blender.org/manual/id/4.5/animation/drivers/workflow_examples.html)
14. [Rigify distribution/runtime statement](https://docs.blender.org/manual/en/2.81/addons/rigging/rigify.html)
15. [Rigify generated rig features](https://docs.blender.org/manual/en/4.5/addons/rigging/rigify/rig_features.html)
16. [Driver execution restrictions](https://docs.blender.org/manual/nl/4.5/animation/drivers/troubleshooting.html)
17. [Drivers panel and variables](https://docs.blender.org/manual/ar/4.5/animation/drivers/drivers_panel.html)
18. [Solidify thickness and vertex groups](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/solidify.html)
19. [Freestyle introduction](https://docs.blender.org/manual/en/4.5/render/freestyle/introduction.html)
20. [Surface Deform proxy workflow](https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/surface_deform.html)
21. [Cloth pin groups](https://docs.blender.org/manual/id/4.5/physics/cloth/settings/shape.html)
22. [Soft-body goals](https://docs.blender.org/UATEST/manual/en/4.5/physics/soft_body/settings/goal.html)
23. [Generic spring constraints](https://docs.blender.org/manual/uk/4.5/physics/rigid_body/constraints/types/generic_spring.html)
24. [Rigid Body World settings](https://docs.blender.org/manual/en/latest/physics/rigid_body/world.html)
25. [Cloth collisions and quality](https://docs.blender.org/manual/nl/4.5/physics/cloth/settings/collisions.html)
26. [Simulation caching/baking](https://docs.blender.org/manual/en/5.0/physics/baking.html)
27. [Blender 4.5 timeline playback modes](https://docs.blender.org/manual/en/4.5/editors/timeline.html)
28. [Packed data, relative paths and missing-file tools](https://docs.blender.org/manual/fi/4.5/interface/window_system/topbar.html)
