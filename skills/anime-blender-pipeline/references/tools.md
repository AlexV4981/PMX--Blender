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


## Version 2 diagnostic utilities

Run explicit image files only (Pillow required):

    python3 "$PACK/scripts/texture_audit.py" /source/face.png /source/hair.png --output "$RUN/audit/channels-001"

Output must be a new directory. Inspect texture-report.json and the channel sheets. Exit 3 means some inputs are blocked/unsupported. Sheets/statistics represent encoded file channels without ICC/OCIO transformation; synthetic opaque alpha may be added for RGB input. No roles are inferred, source pixels are not rewritten, and high-depth/HDR/multiframe inputs require separate inspection.

Copy assets/material-plan.template.json into the run; populate it with actual paths, map roles, hashes, evidence and limitations. Evidence and texture paths resolve relative to the plan file; absolute paths are also supported. Then run:

    python3 "$PACK/scripts/material_plan.py" "$RUN/work/material-plan.json"

A valid plan is a record, not visual acceptance. Required unknown maps block the material and remain unconnected. Empty templates fail intentionally. Record all actual Blender graph and image-setting changes in the recipe and inspect the renders. Neither utility repairs shaders automatically.

Version 2 pipeline.py rejects old pack-version ledgers. Do not edit an old policy or run.json to bypass that rejection. Preserve the original run and use fresh lineage/review for a version 2 run.

## Mathematical measurements (revision 1)

Read mathematics.md for assumptions and stage-specific methods. math_tools.py requires NumPy; it is a read-only measurement utility, not an optimizer or acceptance tool. No new dependency is required to open/animate the final blend.

    python3 "$PACK/scripts/math_tools.py" colors "$RUN/audit/color-samples.json" --output "$RUN/audit/color-result-001.json"
    python3 "$PACK/scripts/math_tools.py" align "$RUN/audit/corresponding-points.json" --output "$RUN/audit/alignment-001.json"

Colors input: encoding='display-srgb', matched_conditions_evidence=[paths], regions=[{name,reference_rgb:[[r,g,b],...],candidate_rgb:[[r,g,b],...]}]. Use JSON double quotes. Values are corresponding display-referred sRGB samples in [0,1]; evidence paths resolve relative to the input file. No ICC/OCIO conversion is performed. Report per-region CIEDE2000 median/p95/max and fraction >=3; the provisional p95<3 result is not stage acceptance. Unknown lighting/registration remains a diagnostic limit.

Align input: source and target equal N-by-3 arrays with known correspondence, after documented axis and scale conversion. Proper SVD rigid alignment rejects collinear data, never allows reflection/scale, and reports residuals. CLI outputs refuse overwrite. Python APIs also expose quaternion_angle and summarize; see their docstrings for units.

Camera/IK/ARAP/PSD/preference/inverse-simulation solvers are procedures or external options, not implemented by this utility. Record actual method/code/version/results before claiming execution. Store a copy of assets/mathematical-profile.template.json with each actual fit; fill relevant fields only and preserve evidence. Existing ledger check names and gates remain unchanged.
