# Sprawling Instructor — Lynae-informed pilot

Evidence from the November 27 Lynae audit: 466 distinct recorded jobs, 15.52 cumulative subprocess hours, 734 working Python scripts, roughly 500 KB of active instruction/handoff files, six r36–r41 batches without a retained model change, eight final checks still blocked. These are engineering workload measurements, not Codex usage telemetry. The lessons are generic: persistent limits, causal evidence, progressive verification, context separation and explicit escalation.

This is a new, optional skill; Graphify Pipeline remains unchanged. It can use Graphify's existing read-only navigator without renaming or modifying it. No installation, automatic process interception, model switching or approval authority is implied.

Example (from the skill directory):

    python3 scripts/budget.py init /path/to/run/budget.json --run 20 --stage 8 --issue 4
    python3 scripts/budget.py reserve /path/to/run/budget.json --issue reset-stability --stage physics --kind implementation --evidence evidence/hypothesis-1.json
    python3 scripts/budget.py finish /path/to/run/budget.json --attempt 1 --outcome rejected --evidence evidence/result-1.json
    python3 scripts/budget.py status /path/to/run/budget.json
    python3 scripts/budget.py context /path/to/run/AGENTS.md /path/to/run/RESUME-HERE.md

The limits are examples, not universal defaults. Use an immutable evidence reference (ideally content hash + relative path); the CLI verifies uniqueness of the supplied string, not its content. An attempt is charged before work; a pending attempt blocks new reservations to avoid concurrent work. After two non-improving implementations, a diagnosis must be reserved and finished with outcome diagnosis and new evidence before another implementation. Three non-improvements block the issue. A diagnosis does not reset counters. A changed stage charges its own stage cap while the issue cap follows the ID. Keep the journal under project control; direct execution and manual edits are not intercepted. No budget extension command is offered in this pilot. Use a recorded human decision before introducing a future extension mechanism.

Tests: `python3 -m unittest discover -s tests -v` from this skill directory. Historical replay and live usage comparison remain required before production adoption.

### Review revision 2

`finish` optionally accepts `--seconds`, `--tokens` and `--usage-source measured|estimated`. `report` returns coverage counts, outcome counts and remaining run/stage/issue limits. Unknown telemetry stays unknown; estimates and actual tokens are never combined. A failed renewed diagnosis after two non-improving implementations cannot be repeated under the same issue ID. A recorded evidence reference remains a trust boundary, not a proof of causality or artifact integrity. The journal is an opt-in gate, not a sandbox or a Codex quota meter.

Historical replay targets: r37/r38 rejected -> renewed diagnosis -> r39 rejected -> stop same issue; r41 failed precheck -> no blind arithmetic retry; neutral motion fixture and placeholder measurements -> blocked rather than pass; context >20 KB -> explicit compaction. These are replay scenarios, not reproduced Blender results.
