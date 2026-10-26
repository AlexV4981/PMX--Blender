---
name: anime-blender-pipeline
description: "Coordinate and diagnose a human-reviewed PMX anime character conversion to a native Cycles Blender animation asset. Use for the complete pipeline, resuming stages, failed shader repair, source-preserving reconstruction, or replaying an accepted recipe."
---

# PMX to native Blender

## Start with the failure and the actual asset

Read [contract.md](references/contract.md). When a previous attempt failed, read [diagnosis.md](references/diagnosis.md) and inspect the last correct checkpoint, failed derivative, rendered evidence and actual commands/logs. If those artifacts are unavailable, distinguish an instruction defect from an unconfirmed runtime cause. Do not claim to have diagnosed a particular model from the skill text alone.

Locate the Blender binary, exact build, importer and supplied model/references. Probe actual capabilities. Keep the correct import intact. Do not replace every material or reimport to solve an isolated shader fault. Treat the bundled generic shader seeds as diagnostic fixtures, not game-character presets or an original game shader recovery.

Read only the active [stage procedure](#stages), plus [tools.md](references/tools.md), [schemas.md](references/schemas.md) for ledger work and [sources.md](references/sources.md) for version-sensitive Blender behavior. Read [roles.md](references/roles.md) before actual delegation. Missing tools block their dependent work, not independent analysis/preparation.

## Run an evidence-driven pilot

Before editing state the observed fault, competing causes, distinguishing test, bounded edit and rollback. Change one causal variable, inspect the result and neighboring regressions, then expand only a proven fix. After two non-improving experiments restore the best draft and re-diagnose or escalate. Do not give Light unfamiliar shader, rig-space or physics design decisions merely because they occur in a routine stage.

For materials require raw channel inspection -> UV/material ownership -> emission texture-only -> neutral diffuse -> verified alpha -> isolated shading/specular -> full scene. Classify each map by evidence. Keep unknowns unknown; do not infer original game masks or face SDFs from a filename. Stage 02 contains the detailed procedure and material-plan validator.

Use one writer per blend and one laptop Blender workload. Delegate only bounded proven operations with private artifacts. Verify actual model availability; requested role names do not configure a running client. Preserve the existing Sol High orchestration/Light routine-work/Astra escalation preference where actually supported.

## Use mathematical support without changing the workflow

Read [mathematics.md](references/mathematics.md) for the active stage and shared fitting/color rules. Use bounded stage-local fitting, regional CIEDE2000 with provisional target <3, and human preference feedback within the existing gates. Keep unknown inputs/thresholds explicit and protected features as constraints. Copy assets/mathematical-profile.template.json into a mutable run derivative before an actual fit. Distinguish bundled measurements from optional external solvers. Do not implement workflow simplifications merely because a comparison map proposes them.

## Initialize or resume without laundering approvals

Use scripts/pipeline.py --help. Set PACK to this skill directory and RUN to the absolute conversion workspace.

```bash
python3 "$PACK/scripts/pipeline.py" init "$RUN" --source /absolute/source/model.pmx --source /absolute/source/texture.png
python3 "$PACK/scripts/pipeline.py" status "$RUN"
python3 "$PACK/scripts/pipeline.py" validate "$RUN"
```

Register all authoritative sources by hash; keep extracted source files and originals unchanged. Copy assets/character-profile.template.json into the run and fill observed facts, leaving unknowns null. Version 2 uses fresh runs; do not rewrite version 1 policy/ledgers or transplant old approvals. Use a validated version 1 tool to inspect its historical run. An imported checkpoint can be reused as an input artifact in a new run with explicit lineage and fresh affected review, without needlessly importing again.

Keep immutable accepted checkpoints and private candidate dependencies. Hashes identify files; separate numerical/visual tests establish behavior. Record manual edits as exact assets or replayable operations. Read [qualification.md](references/qualification.md) before making a qualification claim.

## Stages

| Stage | Skill | Concrete purpose |
| --- | --- | --- |
| 00 | $anime-blender-00-setup | Pin tools, calibrate references, freeze scope and small pilot |
| 01 | $anime-blender-01-import | Preserve working import and document correspondence/loss |
| 02 | $anime-blender-02-materials | Diagnose maps/UV/color/alpha before bounded Cycles restoration |
| 03 | $anime-blender-03-geometry | Prove scoped geometry/normal/weight/morph repairs |
| 04 | $anime-blender-04-rig | Build controls around verified rest spaces and deformation |
| 05 | $anime-blender-05-ready | Expose/test face and animator workflows |
| 06 | $anime-blender-06-tests | Qualify evaluated motion and clean native runtime |
| 07 | $anime-blender-07-look | Match camera/light before final material calibration |
| 08 | $anime-blender-08-physics | Prove one physical structure, expand with tested toggles |
| 09 | $anime-blender-09-audit | Audit, benchmark, review tradeoffs and relocate/clean-open |

Obtain the exact preceding stage acceptance before constructing the next stage. Prepare one to three user-facing candidates only as needed. Reversible diagnostic drafts are experiments inside a candidate, not extra designs that evade the cap. Present failed drafts for critique honestly; submit as passing only with actual required evidence. Never select a winner for the human or manufacture consent.

## Submit exact work

Register the final saved file plus every required mutable asset. Log each frozen-policy required check with a separate nonempty evidence file. After edits, re-register and rerun affected checks; do not reuse stale evidence. Use assets/gate-report.template.md. Present matched before/after views, individual deltas, checked/blocked features and unresolved assumptions. Complete all authorized preparation before the gate.

After an observed explicit human decision tied to the current candidate, the orchestrator may record approve. Workers return evidence and the observed statement. The ledger is an integrity/trust log, not an authenticated approval system. Preserve stage 09 audit, optimization, reaudit and delivery subgates. Return late geometry changes to 03 and invalidate affected bindings/tests/approvals.

Allow construction add-ons and inspected embedded Python. Keep core final behavior native; disclose helper execution separately. A required hyperspecific runtime add-on exception still needs ten distinct evidenced failed alternatives and exact human acceptance. Stop alternatives early when a native method succeeds; do not confuse this budget with candidate count.

## Deliver with measured limits

Deliver the native Cycles blend, necessary external textures if any, embedded animator/reset guide, editable unbaked physics and accepted recipe/evidence. Test a relocated package in clean stock Blender without construction add-ons and core auto execution. Measure real UI Material Preview behavior on the stated laptop: physics off >=24 average FPS, fresh active physics target near 12 with severe stalls disclosed. A headless loop is not UI FPS. Documentation and utility tests alone do not qualify Blender output, character fidelity or hardware performance.
