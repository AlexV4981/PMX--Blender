# Local Specialist Proof of Concept: Simple PMX Character Curriculum

> **Status: PLANNED — NOT EXECUTED**  
> **Branch:** `Pipeline-Optimization`  
> **First priority:** Test the newly revised, graded/gated-out **version 3 lightweight Cycles workflow** on a real Blender character before starting this synthetic-character experiment. Passing utility tests is not live Blender qualification.

## Purpose

Create a large pool of **simple, appealing, original anime-style characters** to use as inexpensive PMX-to-Blender test cases. The purpose is **not** to train a text/image-to-3D generator from scratch or to replace the existing pipeline. The proof of concept is whether **local small language model (SLM) specialists** can carry out bounded PMX-to-Blender operations well enough to **reduce Codex usage**, first on simple characters, then on existing, more elaborate game-derived models that the user is authorized to use.

The local image model can learn the user's aesthetic preferences and produce varied concepts and modeling references. That is an **upstream design tool**, not the specialist training target. The PMX-to-Blender specialists learn from **actual Blender tasks, validated tool actions, failures, corrections, evidence and accepted outputs**.

## Important: unfinished prerequisite

- [ ] **TEST THE NEW VERSION 3 PLAN FIRST.** Rehearse the active `WORKFLOW_COMPARISON.md` Map B / `skills/anime-blender-pipeline/references/workflow.md` on an actual PMX and pinned Blender install. The user has **not** yet tested the revised lightweight, gate-driven workflow.
- [ ] Run the existing 51-test utility suite and seed validation on the current branch; record the actual results of this execution. Earlier reported results are not a substitute.
- [ ] Pin Blender, MMD Tools, Rigify/bridge, Cycles viewport settings and environment; verify basic import, materials, rig, morph and cold physics fixtures in Blender.
- [ ] Confirm that **every human G00–G09 handoff** still works. Stage 09 has two decisions: `audit` and `delivery`; do not add a third approval, copy earlier approvals or skip reviews.
- [ ] Test a real character and capture a baseline of fidelity, regressions, local resources, time and Codex calls; preserve the last correct source/import/checkpoint.
- [ ] Clearly label each qualification level: utility-tested, Blender-fixture qualified, character-qualified, cross-machine replay-qualified, or feature-family qualified. **No claim of live qualification without evidence.**

**Dependencies:** [Workflow comparison](WORKFLOW_COMPARISON.md) · [Active workflow](skills/anime-blender-pipeline/references/workflow.md) · [Qualification](skills/anime-blender-pipeline/references/qualification.md) · [Shared contract](skills/anime-blender-pipeline/references/contract.md) · [Role dispatch](skills/anime-blender-pipeline/references/roles.md).

## Working architecture

```text
Local image generator + preference ratings (optional concept art)
                        |
                        v
Simple original characters / variant reference sheets
                        |
                        v
Known-good reusable 3D base, simple Blender procedural variations,
or permissively licensed PMX assets + actual cleanup/rigging
                        |
                        v
Verified source PMX + textures + reference/baseline manifest
                        |
                        v
EXISTING v3 PMX -> native Cycles Blender pipeline (stages 00–09)
                        |
                        +--> bounded local specialist task (pilot)
                        |        |
                        |        +--> scripts / Blender operations / draft .blend
                        |                    |
                        |               deterministic tests
                        |                    |
                        +--> Codex for failures, novel decisions, or escalation
                        |
                        v
Human stage gate + accepted candidate + evidence
                        |
                        v
Curated task / execution / correction / outcome dataset
```

**Do not conflate a pretty image sheet with a valid PMX.** AI image-to-3D is optional research, not a dependency of the proof of concept. For volume, prefer a few proven bases and scripted hairstyle, clothing, texture and accessory variants that produce *real, inspectable PMX files*. Keep a distinct held-out set of models that the specialist has never seen.

## Phased rollout

### Phase 0 — Finish the pending version 3 workflow test

Run a real, end-to-end Cycles-only conversion under the *current* lightweight plan, with human approvals, actual Blender checks and measured resource behavior. Log anything that is broken before modifying dispatch. **Exit:** one character with verified stage outcomes and known limitations; no assumption that all stages passed.

### Phase 1 — Simple appealing PMX batch (generation only)

Start with 5–10 small, fully human original anime characters using a limited set of clean base meshes. Favor different but manageable hairstyles, palettes, facial looks and straightforward outfits; avoid generating endless near-duplicates. After the initial batch, expand toward 20–50 *only when the construction/export and validation path is reliable*. For each character:

- Save design reference(s), licensing/provenance, source .blend if applicable, exported .pmx, textures, rig/morph inventory and hashes.
- Verify the **actual exported PMX**, its bones/weights, UVs, texture paths and morphs by reimporting it. Flag missing features rather than silently repairing them.
- Assign a difficulty label and the variation knobs used (geometry count, materials, alpha, morphs, accessories, hair, cloth/physics).
- Keep **simple** cases really simple. Do not introduce elaborate layered sheer skirts or game-specific shaders as the first fixture.
- Separate test data from training data by character/base lineage to avoid measuring memorization of the same underlying asset.

**Exit:** a small validated PMX fixture library whose source and expected behavior are known.

### Phase 2 — Local specialist proof of concept

Start with **one bounded stage task**, ideally stage 03 *only when there is a real, scoped geometry problem*. Stage 03 with no actual geometry repair should produce the required **no-change integrity report**, not an invented edit. Other suitable early pilots are evidence gathering, correspondence checks or replaying a proven materials recipe. Keep the existing production orchestrator and human gates unchanged.

For each task:

1. Codex (or current orchestrator) prepares a bounded `worker-task.template.json` with inputs, exact allowed mutations, forbidden edits, expected evidence and rollback.
2. A local candidate model proposes a script/plan or makes changes to a **private draft**, never the accepted source or live shared .blend.
3. Run the prescribed deterministic checks and a short Cycles review; have the human inspect meaningful visual/behavior changes at the existing gate.
4. Record local-first pass, repaired pass, failure, timeout, or **Codex escalation**. Stop a non-improving loop and do not auto-approve.
5. For training, save only traceable examples with verified outcome, corrections and provenance. A failed attempt may be labeled as a failure; it must not be treated as ground-truth success.

**Evaluation:** compare against a Codex-only baseline on matched inputs and identical checks. Track first-pass success, pass-after-repair, actual stage acceptance, regressions, Codex calls/tokens, local inference time, human review time, memory/VRAM and total effort. Count cost reduction **only when quality and required gates remain intact**. Hold out some models and tasks for a genuine unseen-case test.

**Exit:** reproducible results showing whether a local specialist handles the selected task family reliably; if it cannot, do not expand scope merely because many simple characters exist.

### Phase 3 — Expand task families, then character complexity

Only after the Phase 2 pilot shows value, evaluate local workers for other *proven and bounded* operations. Unfamiliar shader logic, bind/rest-space changes, solver design and hidden feature failures continue to receive capable orchestration/Codex escalation. Keep one writer per .blend, no unauthorized stage jumps, and at most three user-facing candidate IDs per gate.

Character complexity ladder:

1. Basic originals: uncomplicated skin, hair, dress/shirt, stockings, simple morphs.
2. Original variants: multiple accessories, extra hair parts, alpha/transparent fabrics, modest rig and cloth demands.
3. **Existing Genshin Impact and Wuthering Waves character models**, only with documented permission/provenance and a usable PMX/converted source.
4. **Existing Silver Palace models**, if a lawful usable asset source is actually available; do not assume asset availability or format.
5. Full ornate, physics-heavy showcase characters only after the feature-family tests justify it.

Games are **later test fixtures**, not a requirement to train a general 3D model from scratch. Model provenance, redistribution and training rights must be assessed individually.

## Dataset record — minimum per task

- `case_id`, `character_id`, `base_lineage`, `difficulty`, `license_provenance`
- `source_pmx_hash`, texture hashes, Blender/add-on/driver versions and environment
- `stage`, `task_type`, objective, constraints, allowed mutations, input checkpoint hash
- Local model/checkpoint/quantization/parameters, exact prompt and tool/script calls
- Draft artifact hashes, errors, logs, evidence paths and measured resource use
- Deterministic check results and **separately recorded human feedback/approval**
- If escalated: Codex intervention, correction diff, validated final artifact and failure cause
- Train/validation/test split and explicit status: **unreviewed / rejected / verified**

Do not label generated reference images, synthetic guesses or successful process exit codes as ground-truth Blender conversions.

## Invariants / non-goals

- **Do not edit or merge `main`.** This is a roadmap on `Pipeline-Optimization`, not authorization to change production workflow/skills or begin conversion.
- Priorities remain **fidelity > animation > realism > performance > convenience**.
- Preserve original PMX, working import and approved Blender checkpoints; no silent redesign or destructive rewrite.
- Maintain the active **Cycles-only** render/review/benchmark contract, stage 00–09 gating, human acceptance, and stage-09 `audit`/`delivery` decisions.
- Use MMD Tools + Rigify/compatible bridge where justified. Local LLM workers are **experimental**; today's Codex role dispatch remains the active contract until separately proposed, tested and approved.
- Optimize for the available dedicated compute where possible (Nitro V 6 GB VRAM or future machine); never assume a local model fits. Respect the current per-workload resource ceilings and keep Blender/LLM contention measurable.
- Do not fine-tune from scratch or generate thousands of models before confirming the first conversion and specialist task actually work.

## Next session checklist

- [ ] **FIRST: Test the revised lightweight/gated v3 plan in actual Blender.**
- [ ] Review its failure notes and establish a Codex-only baseline.
- [ ] Choose the first simple base character and build/export/reimport one real PMX.
- [ ] Define one specialist task and a held-out case.
- [ ] Test one local model versus Codex under identical gates; record outcome.
- [ ] Only then scale the character batch and consider fine-tuning.

**Success definition:** reliably accepted PMX-to-Blender work on progressively harder models **with fewer Codex interventions, without sacrificing fidelity, tests, or human decisions**.
