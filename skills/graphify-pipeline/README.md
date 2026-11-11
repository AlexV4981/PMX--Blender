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