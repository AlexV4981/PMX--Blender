# V4.3 — Knowledge-driven pipeline (experimental)
 
This branch is based on V4.2 commit `ade76f63633822229c431604c369413de663b843`. It is an opt-in pilot, not a new ledger version or an authorization to migrate existing projects. V4.2 gates, approved models, Cycles final quality, native editable physics and the three-candidate limit remain unchanged. Do not run this on the active historical audit. Test on a fresh run or isolated copy after V4.2 qualification.

## Why this experiment exists

An anonymized production audit recorded hundreds of subprocess jobs and working scripts, oversized active instructions and repeated batches without retained improvement. These are engineering observations, not AI quota telemetry. The goal is to reduce repeated diagnosis and implementation while preserving fidelity, not to maximize feature count.

## First pilot — highest return, lowest scope

1. **Knowledge library:** one short case per verified repair. Search by symptom, feature and applicability before creating a new script. Store source/target fingerprints, failure reproduction, causal test, verified outcome, dependencies and limitations. Never apply a case merely because names or tags match. Use the included case registry checker; initial records remain research candidates, not qualified reusable solutions.
2. **Reset qualification:** extend the existing Stage 08 cold-motion fixture only when reset risk is present. Use fresh A, B, A→B, B→A histories, repeated fresh controls, genuinely moving windows and explicit cache clearing; compare same target preset against its fresh reference. See pilot-protocol.md. Do not run a full new suite on every edit.
3. **Behavior evaluations:** use the included scenario set with Codex in isolated workspaces. Run the same inputs with V4.2 alone and V4.2 plus this pilot; score observed actions, not promises. The checker validates evidence records, not model compliance.
4. **Permissions:** add a small source-use inventory at setup; unknown means unknown. Modification, private use, redistribution, and training are independent. No upload of third-party assets or private evidence to public GitHub.

## Deferred roadmap (not implemented)

| Phase | Feature | Initial effort | Recurring target |
| --- | --- | --- | --- |
| V4.4 | Reusable collision/contact inspector; category-level timing; cancellable jobs | Moderate–high | Replace custom diagnostics as repeated cases justify |
| V4.5 | Original MMD motion comparison; evaluate MMD Tools / MMDBridge behavior | High | Optional reference fixture; no external runtime in delivery |
| V4.6 | Local annotated review UI | High | Reduce human explanation and repeated render requests |
| Incremental | Hair, skirts, coats, accessories and shader solution library | Low per qualified case; high if built all at once | Reuse only when applicable |
| Optional | Layered animation controls | Moderate | Only for demonstrated animator needs |

External research leads, not approved dependencies: [MMD Tools](https://github.com/MMD-Blender/blender_mmd_tools), [MMD Tools Append](https://github.com/MMD-Blender/blender_mmd_tools_append), [Blender-MMD](https://github.com/ptrthomas/blender-mmd), [MK-MMD](https://github.com/verticalrectangle/mk-mmd), [MMD Wallpaper Pipeline](https://github.com/Ginripple/blender-mmd-wallpaper-pipeline). Inspect licenses, provenance and specific code before adoption. No external code or models copied.

## How to test

From repository root:

    python3 -m unittest discover -s experiments/v4.3/tests -v
    python3 experiments/v4.3/check.py cases experiments/v4.3/cases.json
    python3 experiments/v4.3/check.py scenarios experiments/v4.3/scenarios.json

For a live pilot read pilot-protocol.md, create a private experiment directory outside the repository, copy the permissions template and create independent evidence for each scenario. Use the existing V4.2 journal and authorized budget. Record actual available token/usage telemetry, tool calls, subprocess time, repeated scripts, intervention count, protected quality and completion. Do not equate elapsed hours with quota. No claim of savings until paired results exist.

The scripts are structural preflight only. They do not run Blender, inspect geometry, determine permissions, enforce agent behavior, or authorize gate advancement.
