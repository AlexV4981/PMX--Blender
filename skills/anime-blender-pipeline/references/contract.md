# Shared production contract

## Product and priorities

- Produce a native Blender Cycles animation character. PMX export compatibility is not required at delivery.
- Focus on PMX anime humanoids resembling Wuthering Waves characters. Verify actual feature support instead of guaranteeing every game.
- Match supplied in-game references. Professional rigs inform functionality/quality, not automatic body, face or style redesign.
- Rank conflicts: fidelity > animation > realism > performance > convenience.
- Keep originals and accepted checkpoints immutable; use private derivative bundles and human approval at every stage.
- Submit topology, thickness, proportions, replacement eyes and hidden surfaces as individually compared proposals. Finalize substantial geometry before final rig/morph construction. Return late geometry work to 03 and invalidate downstream bindings/tests/approvals.
- Deliver editable native hair, clothing, accessory, tail, ear and soft-tissue simulations where applicable, with separate toggles. Do not deliver baked-only physics. Temporary calculation caches are normal; clear final simulation bakes.

## Candidates and human decisions

Produce one to three candidates, only as needed. Ask the human which to continue with or what to critique. Three is a cap, not a quota. The ledger limits candidate IDs per stage; revisions retain prior snapshots. Never evade the cap with extra folders or new runs that conceal additional options.

Read-only inspection, testing and candidate preparation within stage scope are allowed. Accepting visual, quality, texture, shader, geometry or redesign decisions requires explicit human review. Every stage handoff needs approval of its exact candidate even for technical-only work. Never infer consent from silence, elapsed time, another agent, a similar model or an earlier recipe.

Provide matched before/after views, individual change descriptions, relevant motion evidence, metrics, dependencies, assumptions and blocked checks. Clarify ambiguous selection. Explicit exception acceptance amends the requirement; it does not make a failed test pass.

| In scope | Contract violation | Checks pass | Human approval | Artifact unchanged | Advance? |
| --- | --- | --- | --- | --- | --- |
| No | Any | Any | Any | Any | No |
| Yes | Yes | Any | Any | Any | No |
| Yes | No | No | Any | Any | No |
| Yes | No | Yes | No | Any | No |
| Yes | No | Yes | Yes | No | No |
| Yes | No | Yes | Yes | Yes | Yes |

## Execution and models

Run in Codex with actual access to Blender/project files. Use Sol 6.1 High orchestration, Sol 6.1 Light routine work, High difficult implementation and genuine Astra escalation if no usable candidate can be produced. Keep one writer per .blend and one laptop Blender workload by default. Do not claim that prose model names configure a client: inspect real capabilities and disclose unavailable roles.

## Construction and final dependencies

Allow third-party build tools and inspected embedded Python. Aim for no required final add-on. A hyperspecific exception requires ten distinct documented failed alternatives and explicit human acceptance. Stop early if an alternative works. Escalate hard problems rather than exhausting incapable Light retries. Ten attempts are the dependency-removal budget, not permission for ten model candidates.

Keep core posing usable without construction add-ons. Disclose embedded helper execution requirements separately. Test features with a clean profile; an apparently native rig can still contain dependent drivers/handlers/buttons. Preserve needed imported effects until their native replacements pass tests.

## Laptop performance

Baseline: Acer Nitro V, Ryzen 5 7535HS, 16 GB RAM, 6 GB VRAM. Record exact GPU, OS, driver and power state. Average Material Preview physics-off >=24 FPS. Cold active simulation target approximately 12 FPS, with persistent near-1-FPS behavior unacceptable. Calibrate exact stall limits in the pilot.

Measure real UI viewport updates, not headless frame stepping or cached physics. Keep simulation timebase fixed; separate calculation throughput from capped playback. Report frame-time spikes, RAM/VRAM and cold/warm results. Never hide objects, drop frames, silently lower fidelity or alter tests for a pass.

Optimize at 09 after the human reviews the audit/plan. Resource safety checks earlier may prevent a crash but do not authorize premature simplification. If quality and performance conflict, report that conflict rather than reversing priorities.

## Reproducibility and uncertainty

Require source hashes, pinned tools, approved exact assets/edits, material parameters, rest rig/weights, simulation settings/reset/preroll, fixtures and showcase scene. Save manual mesh/paint edits as actual assets or deterministic operations. Verify correspondence before indexed patches.

Treat screenshot lighting/camera uncertainty explicitly. Compare replay outputs under the same approved scene and use direct numerical tolerances rather than rounded hashes. Label unsupported losses, assumptions and uncalibrated metrics. A script's success exit code does not prove model quality.


## Diagnostic execution (version 2)

Read diagnosis.md for failed attempts. Preserve working imports/materials. Require evidence-led map interpretation and isolated pilots before broad changes. Two consecutive non-improving experiments trigger rollback and renewed diagnosis, not another blind fix. Keep generic seeds distinct from approved character shaders. Never compensate across lighting, albedo, normals, bind spaces or solver attachment faults. Stage procedures own the concrete evidence requirements; existing ledger check names remain stable. Version 2 runs do not inherit version 1 approvals.
