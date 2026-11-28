---
name: anime-blender-09-audit
description: "Read-only audit of an exact approved 08P Blender package, including fresh relocated clean-open tests and final delivery. Use for stage 09 of the human-reviewed PMX to native Blender pipeline, including diagnosis or resuming that stage."
---

# 09 — Audit and delivery

## Load the actual procedure

1. Resolve this skill's absolute directory as STAGE_SKILL. Run `python3 "$STAGE_SKILL/scripts/locate_pipeline.py"` to resolve PACK; never assume installed folder names match skill names.
2. Read PACK/references/contract.md, PACK/references/workflow.md and [stage.md](references/stage.md). Read PACK/references/diagnosis.md when a previous attempt failed. Read PACK/references/tools.md and schemas.md before ledger operations; roles.md only when delegating.
3. Check the pinned version, source hashes and exact approved predecessor. Stage 00 has source input instead of a predecessor. Work on a private derivative; leave source and accepted files unchanged.
4. Locate Blender and inspect its actual API before writing version-sensitive code. If tools, model or references are unavailable, complete independent preparation and report what remains untested.

Deliver the native animation rig with required controls intact. Keep construction metarig/settings in the recipe bundle; test the relocated result without MMD Tools, Rigify or bridge add-ons and disclose optional generated UI helpers.

## Read-only execution

Require byte-identical approved 08P model and registered assets; only relocate copies and write independent audit evidence. Do not repair or optimize here. Register newly found faults as debt and route to the owner; stop if a blocker remains. No approved checkpoint mutation or approval fabrication.

## Lightweight Cycles workflow

Use Cycles renders and Cycles Rendered viewport evidence by default; another engine requires an explicit user request. Combine audit plus existing performance disposition into one human decision, then re-audit plus final delivery/acceptance into one exact final decision. Use only audit and delivery CLI gates. Reuse evidence only with the matching-dependency report required by workflow.md.

## Mathematical support

Read the 09 section and shared rules in PACK/references/mathematics.md when applying a fit or numerical comparison. Keep quality/function/dependency/performance as separate acceptance conditions and report measurement variation. Use constrained tradeoff selection; use the two 09 decisions defined in workflow.md. Asset quality tradeoffs require an earlier explicit owner-stage decision; audit cannot authorize model edits. Record methods/results under the existing checks; add no new human gate.

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
- `debt-clear` — verify actual register and dispositions; failed checks remain failed.

Record pass, fail or blocked honestly. A file hash proves identity; a command exit proves execution; neither proves visual correctness. Inspect actual renders, including face/hair/eye close-ups, and name regressions. If image inspection is unavailable, do not claim visual acceptance.

```bash
python3 "$PACK/scripts/pipeline.py" validate "$RUN"
python3 "$PACK/scripts/pipeline.py" candidate "$RUN" 09 A --file "$BLEND" --asset "$ASSET"
python3 "$PACK/scripts/pipeline.py" check "$RUN" 09 A --name CHECK_NAME --status pass --evidence "$EVIDENCE"
python3 "$PACK/scripts/pipeline.py" submit "$RUN" 09 A
```

Use the actual candidate ID and paths. Repeat --asset for all mutable dependencies; omit it only for a self-contained file. Stage 00 may register a setup document as primary. Register after final saving; any subsequent mutation requires new registration and checks. Read command help rather than guessing switches. Present failed/blocked drafts for critique without falsely submitting them as passing.

Present before/after evidence, exact edits, remaining faults and candidate identity for human selection at the stage gate. Do all authorized candidate preparation before asking. Never record approval yourself as a worker; return the actual observed human decision to the orchestrator. Preserve fidelity > animation > realism > performance > convenience. Allow construction add-ons; keep final core behavior native and test dependencies under the shared contract.
