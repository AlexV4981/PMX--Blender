---
name: anime-blender-07-look
description: Execute stage 07, final in-game appearance, for a Codex PMX anime-humanoid to native Blender pipeline. Use for look work on Wuthering Waves-style game characters after the pipeline stage prerequisites are approved; preserve explicit human candidate gates and source identity.
---

# Stage 07: Final in-game appearance

## Load the execution contract

1. Set STAGE_SKILL to this loaded skill's absolute resource directory. Resolve PACK with `python3 "$STAGE_SKILL/scripts/locate_pipeline.py"`; installed folder IDs may differ from skill names.
2. Read PACK/references/contract.md and PACK/references/schemas.md before stage work or gate records.
3. Read PACK/references/roles.md, then [stage implementation checklist](references/stage.md) for procedures and primary sources.
4. Block execution if the shared pack cannot be uniquely located. If skills are exposed only through a catalogue, resolve the exact anime-blender-pipeline package there and use its resource paths; do not invent sibling paths.
5. Inspect `python3 "$PACK/scripts/pipeline.py" --help`; use only supported forms.
6. Follow explicit user instructions over research-era policy wording.

## Scope and priorities

- Execute through Codex; let Sol 6.1 High orchestrate and handle difficult implementation.
- Assign routine implementation to Sol 6.1 Light (low effort where exposed); escalate to Astra if High yields no usable candidate.
- Verify actual role/model availability; never claim requested prose labels configured or ran a model.
- Keep one writer per live .blend and one laptop Blender workload; use private worker assets.
- Preserve fidelity before animation quality, realism, performance and convenience.
- Support only tested PMX anime-humanoid feature profiles; do not advertise universal game support.
- Keep original sources and every approved checkpoint immutable.
- Prepare descendants from the exact approved predecessor; never edit an archived checkpoint in place.
- Keep at most three candidate IDs per stage and create only the one to three needed.
- Revise an existing ID only after recorded human critique; do not evade the cap by archiving IDs.
- Obtain explicit human selection or critique at this stage even if replaying an accepted recipe.
- Record assumptions where character, visual, rig or hardware references are missing.
- Treat Blender execution, character fidelity and hardware qualification as unverified until measured.

## Inputs and preflight

1. Locate the run workspace, `run.json`, source manifest and approved predecessor identity.
2. Check recorded hashes against actual source and approved checkpoint files.
3. Check stage-order and invalidation state using the common pipeline validator.
4. Confirm pinned Blender build, construction tool versions and relevant fixture revisions.
5. Load character-specific scope, allowed edits, reference confidence and calibrated tolerances.
6. Stop if prerequisites are unapproved, stale or incompatible; report the concrete blocker.
7. Use `audit/` for reports and evidence; use `candidates/` for working derivatives.
8. Keep exact assets and deterministic edits needed for replay rather than prose-only artistic instructions.

## Perform the ordered stage work

1. Load approved style sheet and in-game evidence; preserve approved anatomy and face identity.
2. Match cameras and display transform, then refine palette, shadow bands, highlights and surface response.
3. Record exact ramp values, masks/channels, node versions, normals, eye settings and lighting assumptions.
4. Compare face/eye readability, hair detail, emission and alpha from front/profile/three-quarter and motion views.
5. Evaluate only needed outline methods such as reviewed shell or Freestyle with explicit editing and animation tradeoffs.
6. Test outline width across camera distance and resolution; do not promise fixed pixel width from world-space thickness.
7. Test hair-over-eye and ray-dependent tricks under camera and light movement, reflections and shadows.
8. Save accepted material/texture assets, style specification, Cycles showcase and preview comparison for critique.

## Preserve runtime portability

- Allow pinned third-party construction add-ons and construction-time embedded Python.
- Inventory every runtime add-on, module, handler, driver namespace and embedded text dependency.
- Disclose exact embedded Python, behavior and execution requirements for human review.
- Keep core native posing independent of unapproved runtime add-ons.
- Require an addon-free final file unless the exact hyperspecific exception has ten distinct documented failed alternatives and explicit human approval.
- Record up to ten distinct alternatives per dependency with method, outcome and evidence; stop early if one succeeds.
- Escalate incapable routine retries to High/Astra; ten failures permit requesting an exception, never granting it.
- Keep native constraints, controls and editable data; do not substitute screenshots or videos for assets.

## Produce reviewable outputs

1. Save style sheet, accepted texture/material assets and Cycles comparisons.
2. Save candidate `.blend` and registered assets inside WORKSPACE without overwriting its approved predecessor.
   Keep original sources outside registered work assets; registration does not copy originals.
3. Record every substantive edit separately with source IDs, parameters and owning-stage rationale.
4. Record comparisons under fixed cameras, lights, display transform and fixture versions.
5. Classify each required check as pass, fail or blocked with an evidence file.
6. Name known omissions and unsupported PMX features explicitly.
7. Match recipe entries to the exact files and hashes actually submitted.
8. Keep test evidence separate from production actions and temporary caches.

## Required check evidence

Read the frozen WORKSPACE `policy.json`; record all these exact required names, each with nonempty actual evidence.
Do not edit run.json or policy to force acceptance; changing policy in an existing run is rejected.

| Required check name | Evidence to produce |
| --- | --- |
| `final-style-spec` | Exact approved palette, ramp, mask, texture, normal and outline values. |
| `cycles-look-comparisons` | Matched Cycles showcase, close-ups and per-change comparisons. |
| `lighting-and-motion` | Light/camera sweep and animation stability, including hair/eye tricks. |
| `preview-limitations` | Material Preview comparison with declared appearance approximations. |

## Register and submit the exact candidate

Resolve PACK by frontmatter using the locator above; do not assume the installed directory name.
Run `python3 "$PACK/scripts/pipeline.py" --help` before relying on this interface.
Use these verified forms; inspect subcommand help again if the installed script changes:

```bash
python3 "$PACK/scripts/pipeline.py" validate WORKSPACE
python3 "$PACK/scripts/pipeline.py" candidate WORKSPACE 07 CANDIDATE --file BLEND --asset ASSET
python3 "$PACK/scripts/pipeline.py" check WORKSPACE 07 CANDIDATE --name NAME --status pass --evidence FILE
python3 "$PACK/scripts/pipeline.py" submit WORKSPACE 07 CANDIDATE
python3 "$PACK/scripts/pipeline.py" status WORKSPACE
```

Repeat `--asset` for every linked texture/config dependency; omit it only for a truly self-contained bundle.
Use `fail` or `blocked` instead of `pass` for checks without passing evidence.
Do not share writable dependency files between candidates; submitted snapshots freeze the registered bundle.
Do not translate a successful command exit into visual or functional acceptance.

## Human gate and rollback

1. Present exact candidate IDs, differences, comparisons, check results and limitations.
2. Ask the user to select a candidate or critique the submission; never select on their behalf.
3. Wait for explicit observed human approval tied to the exact current candidate.
4. Return the observed human statement to the orchestrator; let it record approval only after exact human acceptance.
   Never invoke approve/review on worker authority or fabricate actor/statement/evidence.
5. Re-run validation and preserve the approved result as an immutable checkpoint.
6. After human critique, record feedback through the orchestrator and revise the existing candidate ID as a new file derivative; repeat affected checks and the gate.
7. If a candidate changes after submission, invalidate its old review and submit the new identity.
8. On failure, keep evidence and route repairs to the owner stage. Branch a new run to revisit accepted work;
   revalidate and obtain affected approvals without copying old approval records.
9. Invalidate downstream checks/bindings/approvals when an upstream edit affects them.
10. Report missing Blender, model, references or target laptop as blocked rather than passing by inference.

## Allowed actions

| Action | Permission | Condition |
| --- | --- | --- |
| Paint textures or choose a new outline method | HUMAN GATE | Preserve character identity and show comparisons. |
| Accept substantive edits or choose a winner | HUMAN GATE | Ask selection/critique of the exact candidate. |
| Change another stage-owned system | NO | Route to owner and invalidate dependents. |
| Optimize character quality before stage 09 | NO | Defer measured performance tradeoffs. |
| Claim missing checks passed | NO | Record blocked status and the missing evidence. |

Keep stage ownership and the explicit human gate even for rows marked YES.
