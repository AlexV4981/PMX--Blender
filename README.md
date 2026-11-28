# PMX to native Blender skills — V4.1 bounded-execution pilot

Review branch only, not a production release. Preserves Cycles-only, native editable controls/physics, immutable source and human decisions. Adds 08P before read-only 09, debt tracking, progressive testing and explicit budgets. See [V4 execution controls](skills/anime-blender-pipeline/references/bounded-execution.md) and [current-run handoff](CURRENT-AUDIT-HANDOFF.md). Install all twelve anime-blender skills as siblings for a NEW V4 run, plus separately reviewed Sprawling Instructor or equivalent persistent journal. Do not install over a pinned historical run. Historical ZIP/manifest remain V3 artifacts and are not V4 release assets. No live Blender, hardware, full historical replay or packaged release qualification is claimed. Utility tests are included; verify before adoption.

## Construction simplification

Use MMD Tools import and Rigify body controls for fully human characters; animal ears/tails/kemonomimi are deferred. The [construction route](skills/anime-blender-pipeline/references/construction.md) covers compatible bridges, version probes, source preservation and native runtime limits. Bespoke work requires demonstrated inability of compatible existing tools to meet the requirement. All stages and human gates remain; live asset qualification is still required.


## Validation

    python3 -m unittest discover -s skills/anime-blender-pipeline/scripts/tests -v

Review the new stage ordering, exact package identity, debt checks and preflight tests. Current CLI does not enforce journal reservations on arbitrary shell commands, authenticate human decisions, reopen approved stages in-place, or amend a frozen performance requirement. These remain explicit limitations, not production-ready functionality.

V4.1 adds mandatory [post-review technical subgates](skills/anime-blender-pipeline/references/post-review-subgates.md). Human direction no longer advances 00–08P; the existing required checks are split into preliminary and post-review groups and a technical completion command gates progression. 09 retains its audit/delivery reviews. No V3/V4.0 migration.

## V4.2 mandatory storage subgate

After submit and before complete (or 09 delivery review), run `python3 "$PACK/scripts/pipeline.py" storage "$RUN" STAGE CANDIDATE --quiescent` with all writers stopped. This runs the bundled exact-duplicate utility on work, audit, candidates and checkpoints; preserves original paths and independent writes; records a revision-bound report. No additional human approval. Unsupported sharing retains copies and reports limitations, never unlinks files. Scan or verification errors block completion. See the shared artifact-dedup procedure. New runs only; do not change frozen V3/V4.1 policy.
