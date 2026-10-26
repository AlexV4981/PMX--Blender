---
name: anime-blender-03-geometry
description: "Repair demonstrated mesh and deformation faults while preserving deliberate anime topology, normals, UVs, silhouettes and morph correspondence. Use for stage 03 of the human-reviewed PMX to native Blender pipeline, including diagnosis or resuming that stage."
---

# 03 — Geometry and deformation foundation

## Load the actual procedure

1. Resolve this skill's absolute directory as STAGE_SKILL. Run `python3 "$STAGE_SKILL/scripts/locate_pipeline.py"` to resolve PACK; never assume installed folder names match skill names.
2. Read PACK/references/contract.md, PACK/references/workflow.md and [stage.md](references/stage.md). Read PACK/references/diagnosis.md when a previous attempt failed. Read PACK/references/tools.md and schemas.md before ledger operations; roles.md only when delegating.
3. Check the pinned version, source hashes and exact approved predecessor. Stage 00 has source input instead of a predecessor. Work on a private derivative; leave source and accepted files unchanged.
4. Locate Blender and inspect its actual API before writing version-sensitive code. If tools, model or references are unavailable, complete independent preparation and report what remains untested.

## Execute with a bounded change

Use the routine path in workflow.md first; expand relevant diagnosis in stage.md only for an observed or uncertain fault. State the observed fault, evidence, competing causes, distinguishing test, proposed edit and rollback file before editing. Run the distinguishing test first. Preserve a correct imported subsystem; never rebuild it simply because a template exists.

Change one causal variable per experiment and render/measure the affected region before expanding to the character. Treat failed experiments as reversible drafts within a candidate, not as new candidate designs. Stop and restore the best draft after two consecutive experiments without measurable improvement; diagnose or escalate before another edit. Keep at most three user-facing candidate IDs and request human critique before revising a submitted candidate.

Do not compensate for a fault in another subsystem: do not fix lighting with albedo, shader faults with normals, a rest-space error with weights, or attachment faults with excessive damping. Route cross-stage changes to their owner and requalify affected downstream work.

## Lightweight Cycles workflow

Use Cycles renders and Cycles Rendered viewport evidence by default; another engine requires an explicit user request. When no geometry change is needed, submit a no-change integrity/correspondence report at the existing gate. Do not manufacture geometric work. Reuse evidence only with the matching-dependency report required by workflow.md.

## Mathematical support

Read the 03 section and shared rules in PACK/references/mathematics.md when applying a fit or numerical comparison. Use ARAP only for an approved geometric correction, compare skinning models only for an observed deformation fault, and preserve all shape/UV/normal correspondence. Measure evaluated displacement; human accepts the form/motion delta. Record methods/results under the existing checks; add no new human gate.

## Evidence and handoff

Required check names from the frozen run policy:
- `geometry-change-comparisons` — use the evidence specified in stage.md.
- `morph-integrity` — use the evidence specified in stage.md.
- `deformation-tests` — use the evidence specified in stage.md.
- `correspondence-map` — use the evidence specified in stage.md.

Record pass, fail or blocked honestly. A file hash proves identity; a command exit proves execution; neither proves visual correctness. Inspect actual renders, including face/hair/eye close-ups, and name regressions. If image inspection is unavailable, do not claim visual acceptance.

```bash
python3 "$PACK/scripts/pipeline.py" validate "$RUN"
python3 "$PACK/scripts/pipeline.py" candidate "$RUN" 03 A --file "$BLEND" --asset "$ASSET"
python3 "$PACK/scripts/pipeline.py" check "$RUN" 03 A --name CHECK_NAME --status pass --evidence "$EVIDENCE"
python3 "$PACK/scripts/pipeline.py" submit "$RUN" 03 A
```

Use the actual candidate ID and paths. Repeat --asset for all mutable dependencies; omit it only for a self-contained file. Stage 00 may register a setup document as primary. Register after final saving; any subsequent mutation requires new registration and checks. Read command help rather than guessing switches. Present failed/blocked drafts for critique without falsely submitting them as passing.

Present before/after evidence, exact edits, remaining faults and candidate identity for human selection at the stage gate. Do all authorized candidate preparation before asking. Never record approval yourself as a worker; return the actual observed human decision to the orchestrator. Preserve fidelity > animation > realism > performance > convenience. Allow construction add-ons; keep final core behavior native and test dependencies under the shared contract.
