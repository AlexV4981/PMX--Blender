---
name: graphify-pipeline
description: "Build and query source-linked graphs of existing PMX-to-Blender skill folders, requested model roles, stages, exact checks, human approval gates and evidence-based failure/backtrack routes. Navigation only, not authority to change any gate."
---

# Graphify Pipeline

From the repository root, generate the self-contained indexed graph:

    python3 skills/graphify-pipeline/scripts/graphify.py build

Then ask for only the slice needed:

    python3 skills/graphify-pipeline/scripts/graphify.py stage 04
    python3 skills/graphify-pipeline/scripts/graphify.py fault "limb flips"
    python3 skills/graphify-pipeline/scripts/graphify.py models
    python3 skills/graphify-pipeline/scripts/graphify.py verify

Outputs: generated/graph.json, generated/graph.html and generated/context.md, all underneath this skill. The graph is a read-only navigation and provenance cache. It does not edit conversion files, ledgers, the eleven-skill manifest or any gate policy.

## Agent operating rules

1. Verify freshness before trusting a generated graph. If stale, rebuild from current checkout; never trust an older branch's gate index.
2. The graph's exact required check IDs are extracted from the active stage-policy.json. The original contract, workflow, stage procedure, frozen run policy and ledger remain authoritative. Read only contract.md, workflow.md, active stage SKILL.md and stage.md before ordinary execution, plus other specialized references as needed.
3. Follow the normal stage gate: actual passing required checks, current candidate bundle, and observed explicit human approval. At 09 retain two decisions: audit and delivery, with delivery serving as final acceptance. A graph edge does not mean a check passed or a human approved.
4. Diagnose failures with actual evidence and route only verified repairs to the owning stage. Late geometry changes return to 03 and requalify affected dependent work. After two non-improving experiments revert and re-diagnose. A failure label is a starting hypothesis, not proof.
5. Model-role nodes represent requested selections/config files, never guaranteed running model availability. Verify actual Codex/client capabilities before delegation.
6. Keep all existing constraints: fidelity above animation above realism above performance above convenience; fully human current scope; MMD Tools and Rigify first; Cycles/Rendered by default; native clean Blender behavior; at most three submitted candidate IDs; independent human approval per handoff; no invented consent.
7. Do not install dependencies, launch Blender, run acceptance, copy old approvals or rewrite source policy to make the graph work. Graphify is intentionally excluded from the original pack-manifest.json.

See README.md for CLI options and source-of-truth boundaries.

## Detailed action-and-repair graph

The default build also generates action_graph.json, action_graph.html and actions_context.md under generated/. The detailed graph uses numbered headings from each original stage.md as task nodes. After each task is a local verification checkpoint (not an additional formal gate). PASS routes to the next task. FAIL routes through diagnosis, reversible repair, retest and back to the exact interrupted check. Two consecutive non-improving experiments route to restoration of the best checkpoint and renewed diagnosis or escalation. Diagnoses and repair choices must be grounded in actual model evidence; this navigator never guesses that a particular fix succeeded.

Exact mandatory check names still come from stage-policy.json, and human decisions remain at their existing positions. Stage 09 includes audit before further measurement/work and delivery as final acceptance. Navigation buttons cannot record evidence or human approval.

Open generated/action_graph.html to explore or run:

    python3 skills/graphify-pipeline/scripts/action_graph.py stage 04

A graph is an index, not a replacement for authoritative original task instructions or the real run ledger.
