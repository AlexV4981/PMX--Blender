# Optional Graphify Pipeline skill

A compact, offline source-linked graph of the Pipeline-Optimization branch. Existing ten stages, all frozen required check names, and the eleventh orchestrator skill are untouched. The graph is NOT a rewritten specification.

Run from repository root:

    python3 skills/graphify-pipeline/scripts/graphify.py build
    python3 skills/graphify-pipeline/scripts/graphify.py verify
    python3 skills/graphify-pipeline/scripts/graphify.py stage 09
    python3 skills/graphify-pipeline/scripts/graphify.py fault "pink material"
    python3 skills/graphify-pipeline/scripts/graphify.py models
    python3 skills/graphify-pipeline/scripts/graphify.py impact skills/anime-blender-04-rig/references/stage.md

Use --root /repo to target another checkout and --out /dir to change the output directory. Python 3.10+ standard library; no network, Blender, pip packages, graph service or cloud credentials.

The generated directory contains graph.json (nodes/typed edges, exact policy check names, model roles, failure routes, SHA-256 source fingerprints), graph.html (clickable offline stage/gate/check source explorer), and context.md (compact router). All source paths are relative to repository root. HTML source links assume the default generated directory; use --out only when those relative links are not needed.

An agent should read the graph/index first, then load the relevant original stage procedure and original shared contract/workflow. Never substitute a short stage title or graph check name for its full evidence definition in stage.md and the actual run ledger. Human approvals are not machine actions. Stage 09 has audit and delivery decisions, not a fabricated third one.

The diagnostic fault mapping is provisional and derived from the existing diagnosis ownership map; a distinguishing test must establish cause. Any change to source files makes verification fail until rebuilt. Graphify does not change the pack manifest, conversion stage policy, source model, renderer or delivery requirements.

Local tests:

    python3 -m unittest discover -s skills/graphify-pipeline/tests -v

## Task-level graph with recovery paths

The main build command now also creates generated/action_graph.json,
generated/action_graph.html and generated/actions_context.md. Open
action_graph.html in a browser. It includes numbered source task nodes with
references, local task checks, exact stage-policy checks and human decision
nodes. Each unsuccessful check has a diagnosis → first bounded solution →
retest → second bounded solution if needed → retest → rollback and re-diagnosis
route. After a verified repair the navigator returns to the same interrupted
check, then continues to the next action only if the check actually passes.

The source tasks are indexed by their original numbered sections, not rewritten
into invented specification requirements. Consult the original text for all
step-level details. HTML PASS/FAIL controls are interactive navigation only:
they do not inspect Blender, execute fixes, record ledger checks, grant approval
or persist completed work. The graph identifies the correct next instruction,
not a proven completed instruction.

Run action_graph.py stage 04 to print one detailed route or
action_graph.py verify to detect stale source fingerprints. Stage 09 retains
the source audit and delivery decisions; all other stage handoffs still require
their original explicit human approval.

This optional graph skill is not included in the frozen original
pack-manifest.json. It does not alter the conversion pipeline, original
skill procedures, acceptance rules or historical runs.
