---
name: anime-blender-09-audit
description: "Audit appearance, deformation, dependencies and actual viewport performance, then prepare a relocated, clean-open-tested Blender delivery. Use for stage 09 of the human-reviewed PMX to native Blender pipeline, including diagnosis or resuming that stage."
---

# 09 — Audit and delivery

## Load the actual procedure

1. Resolve this skill's absolute directory as STAGE_SKILL. Run `python3 "$STAGE_SKILL/scripts/locate_pipeline.py"` to resolve PACK; never assume installed folder names match skill names.
2. Read PACK/references/contract.md and [stage.md](references/stage.md). Read PACK/references/diagnosis.md when a previous attempt failed. Read PACK/references/tools.md and schemas.md before ledger operations; roles.md only when delegating.
3. Check the pinned version, source hashes and exact approved predecessor. Stage 00 has source input instead of a predecessor. Work on a private derivative; leave source and accepted files unchanged.
4. Locate Blender and inspect its actual API before writing version-sensitive code. If tools, model or references are unavailable, complete independent preparation and report what remains untested.

## Execute with a bounded change

Follow stage.md in order. State the observed fault, evidence, competing causes, distinguishing test, proposed edit and rollback file before editing. Run the distinguishing test first. Preserve a correct imported subsystem; never rebuild it simply because a template exists.

Change one causal variable per experiment and render/measure the affected region before expanding to the character. Treat failed experiments as reversible drafts within a candidate, not as new candidate designs. Stop and restore the best draft after two consecutive experiments without measurable improvement; diagnose or escalate before another edit. Keep at most three user-facing candidate IDs and request human critique before revising a submitted candidate.

Do not compensate for a fault in another subsystem: do not fix lighting with albedo, shader faults with normals, a rest-space error with weights, or attachment faults with excessive damping. Route cross-stage changes to their owner and requalify affected downstream work.

## Mathematical support

Read the 09 section and shared rules in PACK/references/mathematics.md when applying a fit or numerical comparison. Keep quality/function/dependency/performance as separate acceptance conditions and report measurement variation. Use constrained tradeoff selection; retain all existing 09 subgates. This integration does not apply workflow or asset optimization. Record methods/results under the existing checks; add no new human gate.

## Evidence and handoff

Required check names from the frozen run policy:
- `final-quality` — use the evidence specified in stage.md.
- `physics-off-fps` — use the evidence specified in stage.md.
- `cold-physics-fps` — use the evidence specified in stage.md.
- `frame-time-and-memory` — use the evidence specified in stage.md.
- `regression-tests` — use the evidence specified in stage.md.
- `relocated-clean-open` — use the evidence specified in stage.md.
- `dependency-disposition` — use the evidence specified in stage.md.
- `delivery-guide-and-recipe` — use the evidence specified in stage.md.

Record pass, fail or blocked honestly. A file hash proves identity; a command exit proves execution; neither proves visual correctness. Inspect actual renders, including face/hair/eye close-ups, and name regressions. If image inspection is unavailable, do not claim visual acceptance.

```bash
python3 "$PACK/scripts/pipeline.py" validate "$RUN"
python3 "$PACK/scripts/pipeline.py" candidate "$RUN" 09 A --file "$BLEND" --asset "$ASSET"
python3 "$PACK/scripts/pipeline.py" check "$RUN" 09 A --name CHECK_NAME --status pass --evidence "$EVIDENCE"
python3 "$PACK/scripts/pipeline.py" submit "$RUN" 09 A
```

Use the actual candidate ID and paths. Repeat --asset for all mutable dependencies; omit it only for a self-contained file. Stage 00 may register a setup document as primary. Register after final saving; any subsequent mutation requires new registration and checks. Read command help rather than guessing switches. Present failed/blocked drafts for critique without falsely submitting them as passing.

Present before/after evidence, exact edits, remaining faults and candidate identity for human selection at the stage gate. Do all authorized candidate preparation before asking. Never record approval yourself as a worker; return the actual observed human decision to the orchestrator. Preserve fidelity > animation > realism > performance > convenience. Allow construction add-ons; keep final core behavior native and test dependencies under the shared contract.
