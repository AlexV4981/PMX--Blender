# PMX to native Blender skills — V4.2 integrated review

One source skill pack: bounded execution, Sprawling Instructor, performance stage 08P, read-only 09, post-direction technical subgates, debt register and exact duplicate storage subgate. This is a review candidate, not a Blender-qualified release. The historical ZIP and pack-manifest.json describe V3; do not install them as V4.2.

## Refresh for a new project

Check out the reviewed commit into a NEW tools directory, not the working directory of an active run. Install/copy the twelve anime-blender skill directories and sprawling-instructor as siblings from that exact checkout; do not mix versions. Run the Python utility test suites before use (NumPy and Pillow for existing tests). The old Graphify skill is unchanged.

    python3 -m unittest discover -s skills/sprawling-instructor/tests -v
    python3 -m unittest discover -s skills/anime-blender-pipeline/scripts/tests -v

Start a fresh V4.2 ledger. Read [shared workflow](skills/anime-blender-pipeline/references/workflow.md), [bounded execution](skills/anime-blender-pipeline/references/bounded-execution.md), [technical subgates](skills/anime-blender-pipeline/references/post-review-subgates.md), and [storage](skills/anime-blender-pipeline/references/artifact-dedup.md). Each stage 00–08P: register, preliminary checks, observed human direction, technical checks, submit, storage, complete. Stage 09: read-only audit and delivery reviews, submit, storage before delivery. Preserve original priority and actual Cycles benchmark requirements.

## Resume an active V3 audit

Do NOT replace the old skill pack, change its policy, or run the V4.2 ledger against it. Use [CURRENT-AUDIT-HANDOFF.md](CURRENT-AUDIT-HANDOFF.md) as the compatibility overlay. Read latest actual local evidence and preserve qualified progress; do not redo the audit from scratch. The current run can test bounded execution and storage intervention, not the new earlier subgates. Record a clean baseline and cutover.

## Validation boundaries

No live Blender/hardware qualification, full historical replay, or measured quota savings is claimed. The budget journal is opt-in, the ledger checks recorded evidence rather than proving test semantics, and frozen requirements cannot be changed through an automated exception command. Unsupported filesystem deduplication keeps files. Run the tests and review CI before adopting this pack.
