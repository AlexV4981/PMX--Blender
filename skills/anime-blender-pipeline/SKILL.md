---
name: anime-blender-pipeline
description: Coordinate a human-reviewed PMX anime game character conversion into a native Cycles Blender animation asset, especially Wuthering Waves-style humanoids. Use for the complete ten-stage pipeline, resuming a conversion, reproducing a showcased character recipe, dispatching stage skills, enforcing candidate and approval gates, or handling difficult Blender/MMD conversion failures. Do not claim model or laptop qualification without actual tests.
---

# Anime Blender Pipeline

## Load only the relevant instructions

Read [contract.md](references/contract.md) before conversion, [schemas.md](references/schemas.md) before ledger operations, and [roles.md](references/roles.md) before delegation. Load only the current stage and its references. Use [tools.md](references/tools.md) for commands, [qualification.md](references/qualification.md) for evidence and [sources.md](references/sources.md) for version-sensitive technical verification.

## Establish actual capability

Locate the user's project and Blender binary. Probe the exact build/add-on versions. If Blender, model sources, references or a required model role are unavailable, report precisely what is blocked and continue only independent preparation. Never claim local workstation access from an unrelated cloud workspace or substitute a random downloaded character.

Treat this pack as workflow and verification implementation. Qualify bundled shader seed definitions and Blender-dependent tools in live Blender before use. They are not approved character presets. A new character has no proven showcase recipe until it completes the pipeline.

## Coordinate roles

Use GPT-6.1 Sol High (gpt-6.1-sol, high) as orchestrator, GPT-6.1 Sol Light (gpt-6.1-sol, low where exposed) for bounded routine work, High for unfamiliar implementation and actual Astra escalation when no usable candidate can be produced. Report unavailable models honestly. Keep one writer/workload per Blender project by default. Review compact reports at task boundaries rather than repeating worker actions.

## Initialize or resume

Set PACK to this skill directory and RUN to the chosen absolute project workspace. Consult scripts/pipeline.py --help for canonical arguments.

    python3 "$PACK/scripts/pipeline.py" init "$RUN" --source /absolute/source/model.pmx --source /absolute/source/texture.png
    python3 "$PACK/scripts/pipeline.py" status "$RUN"
    python3 "$PACK/scripts/pipeline.py" validate "$RUN"

Register every authoritative source file. Init hashes files and never modifies originals. For an archive, register the archive and independently extracted authoritative files. Place mutable derivatives/evidence inside RUN; preserve submitted snapshots under checkpoints. Give each candidate private asset copies. A valid ledger proves integrity, not visual quality.

Copy assets/character-profile.template.json into the run and fill observed facts. Leave unknowns null. Do not invent GPU, height, texture channels, accepted tolerances or version hashes. Save manual edits as exact assets or deterministic operations. Distinguish adapting a new character from replaying a known recipe.

## Dispatch stages

| Stage | Skill | Responsibility |
| --- | --- | --- |
| 00 | $anime-blender-00-setup | Environment, references and scope |
| 01 | $anime-blender-01-import | Import baseline and loss inventory |
| 02 | $anime-blender-02-materials | Cycles restoration and preview |
| 03 | $anime-blender-03-geometry | Approved geometry/deformation foundation |
| 04 | $anime-blender-04-rig | Native Blender controls |
| 05 | $anime-blender-05-ready | Face, usability and retarget profiles |
| 06 | $anime-blender-06-tests | Motion, deformation and integrity tests |
| 07 | $anime-blender-07-look | Final in-game appearance |
| 08 | $anime-blender-08-physics | Editable native secondary motion |
| 09 | $anime-blender-09-audit | Audit, approved optimization and delivery |

Require the preceding accepted checkpoint before constructing the next stage. Stop at every human gate. Produce one to three candidates as needed and ask which to continue with or what to critique. Never select a winner or fill a quota. Revise existing IDs after critique rather than evading the cap.

## Bind decisions to artifacts

Register the primary file and every required asset with candidate --file and repeated --asset arguments. Log required checks with separate nonempty evidence. Submit only after required checks pass. Use assets/gate-report.template.md and list each substantive visual/geometry change separately under matched comparison conditions.

After explicit human selection/approval, record the actual actor and observed statement with approve. The CLI records a trust assertion, not authenticated consent. Workers must not approve themselves. Artifact edits invalidate checks and approvals. Never modify an approved checkpoint; branch a new run for retrospective revisions and requalify affected stages.

Use feedback to record observed human critique and unlock a submitted candidate for revision. Retain earlier snapshots. At stage 09, record audit, optimization, reaudit and delivery human subgates with review. Explicitly record optimization as not needed when appropriate; still perform clean-package tests.

## Handle difficult problems and dependencies

Allow third-party construction tools and reviewed embedded Python. Aim for an addon-independent final character. For a hyperspecific required runtime add-on, log up to ten genuinely distinct alternative methods with attempts and evidence; stop early if one succeeds. After ten failures, ask the human to accept or reject the exact dependency/version and limitations. This budget does not permit ten model candidates.

Escalate inability to produce a candidate to Astra with failed approaches and artifacts. If Astra also fails or is unavailable, leave actionable avenues for the human. Do not impersonate escalation. Label assumptions when references are missing rather than claiming reconstructed details as facts.

## Finish truthfully

Deliver a relocated, clean-open-tested Cycles .blend, editable unbaked simulations, relative texture assets, dependency disclosures, recipe, animator guide and evidence. Require >=24 average Material Preview FPS with physics off; target approximately 12 during fresh active calculation and disclose severe stalls. Optimize only at stage 09 and rerun affected checks. Never claim hardware qualification, recipe reproducibility or addon independence without actual evidence.
