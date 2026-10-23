# Executable tools

## Ledger CLI (Python standard library)

Set PACK to this skill's absolute directory and RUN to the conversion workspace. Run scripts/pipeline.py --help or a subcommand's --help for exact arguments.

    python3 "$PACK/scripts/pipeline.py" init "$RUN" --source /source/character.pmx --source /source/texture.png
    python3 "$PACK/scripts/pipeline.py" status "$RUN"
    python3 "$PACK/scripts/pipeline.py" validate "$RUN"
    python3 "$PACK/scripts/pipeline.py" candidate "$RUN" 00 A --file work/setup.json --asset work/character-profile.json
    python3 "$PACK/scripts/pipeline.py" check "$RUN" 00 A --name source-inventory --status pass --evidence audit/source-inventory.json
    python3 "$PACK/scripts/pipeline.py" submit "$RUN" 00 A

Repeat check for every canonical required_check in assets/stage-policy.json. Status can be pass, fail or blocked. Evidence must be a separate nonempty file inside the workspace. Do not pass missing prerequisites, guesses or fictional results. When a requirement is legitimately not applicable, explain why in the evidence and obtain the stage's human review; never misrepresent an unperformed required test.

Only after an actual human decision:

    python3 "$PACK/scripts/pipeline.py" approve "$RUN" 00 A --actor HUMAN --statement 'Exact observed human acceptance of candidate A'
    python3 "$PACK/scripts/pipeline.py" feedback "$RUN" 00 B --statement 'Exact observed human critique'

These examples are not advance authorization or authentic approval statements. Never execute them as a worker. Submitted status is a stop condition, not approval. Feedback preserves snapshot history and clears checks for revision. Register the changed bundle again, rerun checks and resubmit. Approved stages cannot be reopened in place; branch a new run with explicit lineage and requalified gates.

Stage 09 internal human reviews:

    python3 "$PACK/scripts/pipeline.py" review "$RUN" 09 A --gate audit --actor HUMAN --statement 'Observed decision' --evidence audit/09-audit.md

Use audit, optimization, reaudit and delivery in that order. Record optimization as not needed when appropriate. Reaudit/delivery must identify the final current bundle. Final approve still follows submit and all checks. Do not run review because a model thinks the user would agree.

Dependency alternatives:

    python3 "$PACK/scripts/pipeline.py" attempts "$RUN" specific-addon --method 'Actual distinct alternative' --outcome failed --evidence audit/alternative-01.json

Stop early when succeeded. Ten failed alternatives only make a hyperspecific exception eligible for human consideration. Distinct descriptions do not prove distinct technical approaches; the orchestrator must examine actual evidence.

## PMX inventory (read-only)

    python3 "$PACK/scripts/pmx_inventory.py" /source/model.pmx --output "$RUN/audit/pmx-inventory.json"

Exit 0: structurally consumed inventory; not proof every PMX effect is supported. Exit 3: partial inventory, including nonzero PMX 2.1 soft-body payload or unknown trailing bytes. Exit 2: malformed/unsupported input. Never suppress partial status and claim full support. PMX 2.0 sections and deformation-type counts are parsed without changing the source. Preserve source data and validate against the actual importer. This tool does not replace the source-to-import comparison or inspect every numeric/index invariant.

## Blender tools (live qualification required)

Run the actual Blender executable. Do not claim normal Python has bpy. Probe first:

    blender --background --factory-startup --disable-autoexec --python "$PACK/scripts/blender_tools.py" -- probe --output "$RUN/audit/environment.json"

Inspect a working derivative read-only:

    blender --background --factory-startup --disable-autoexec "$RUN/work/character.blend" --python "$PACK/scripts/blender_tools.py" -- inspect --output "$RUN/audit/scene-inspection.json"

Inspection emits base geometry/UV/normal/shape-key hashes, rig/weight/node/driver records, dependencies and diagnostics. It is an inspection seed, not a complete semantic fingerprint of every Blender feature. Use raw registered asset hashes for approval integrity; extend and qualify the semantic snapshot where a character uses unsupported data. A zero-length/invalid-target report can include intentional cases: diagnose and document rather than deleting bones blindly. Log-based lint does not prove every possible dependency cycle absent.

Validate declarative shader seeds without Blender:

    python3 "$PACK/scripts/blender_tools.py" validate-seeds

Build a NEW seed library in factory startup, with no production file loaded:

    blender --background --factory-startup --disable-autoexec --python "$PACK/scripts/blender_tools.py" -- build-seeds --output "$RUN/work/shader-seeds.blend"

The native Toon and Surface seed groups are starting graphs with fixed interfaces, not approved Wuthering Waves materials, complete face/eye systems or measured physics presets. Verify sockets and render fixtures in the pinned Blender build before appending them. Qualify approved game/character-specific groups and record their hashes. Do not claim an unbuilt library exists or replace missing reference assets with these neutral seeds.

## Capability limitations

No UI FPS recorder is bundled or claimed tested. Implement and qualify a UI redraw-driven measurement harness in stage 00/09 before reporting actual viewport throughput. Do not substitute inspect, a background frame loop or a cached playback pass. The pack's templates/rules define the required benchmark, not a fabricated measurement tool.

Blender-dependent paths were syntax/pure-data checked when authored without Blender available. Run live fixture tests before marking them qualified. Do not report that building the seed library qualifies the full pipeline.
