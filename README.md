# PMX to native Blender skills — version 2

Eleven Codex skills for source-preserving PMX anime character conversion to a native Cycles animation asset. All stage entrypoints and working procedures have been rewritten around diagnosis, isolated experiments and actual evidence. See [AUDIT.md](AUDIT.md) for the failure analysis, per-stage changes and validation limits.

## Use the rewritten source

Copy the eleven directories inside `skills/` into the skills directory used by your Codex installation. Keep them as siblings, with each SKILL.md directly inside its folder. Replace the corresponding old skills; avoid duplicate named copies. The version 1 ZIP under `downloads/` is historical and does **not** contain the rewrite. Use the current repository source for version 2.

A skill cannot control Blender on your laptop unless the running Codex environment actually has access to it. Provide the exact PMX, texture package, last correct import, failed derivative if available, reference images and Blender executable. Preserve originals. No game models/textures, approved character shaders or completed character recipes are included.

Suggested restart prompt:

> Use $anime-blender-pipeline version 2. Preserve my last correct import and original textures. Inspect the failed shader result and diagnose one face material, one hair material and an alpha edge with the stage 02 ladder. Show actual diagnostic renders before propagating any fix. Keep missing map roles unknown. Stop at the existing human review gates.

Choose the parent model in the client. The pack retains the Sol High/Light routine-work/Astra escalation preference where supported; prose role names do not configure an unavailable model. Use bounded workers for proven operations, not unfamiliar shader or rig design.

## Version compatibility

Version 2 uses fresh ledger runs. Do not change the policy/version in a version 1 ledger, copy old approvals or overwrite accepted files. Keep historical runs with their historical tools. Reuse a correct imported blend as an explicit source artifact with recorded lineage and fresh affected review; another import is not automatically necessary.

The product priorities remain fidelity > animation > realism > performance > convenience. Each stage has a human candidate gate. Final core posing should be native and independent of construction add-ons. The exception process for a hyperspecific required runtime add-on remains unchanged.

## Tools and validation

```sh
python3 -m unittest discover -s skills/anime-blender-pipeline/scripts/tests -v
python3 skills/anime-blender-pipeline/scripts/blender_tools.py validate-seeds
python3 skills/anime-blender-pipeline/scripts/texture_audit.py /path/map.png --output /path/new-audit-dir
python3 skills/anime-blender-pipeline/scripts/material_plan.py /path/material-plan.json
```

The texture auditor requires Pillow; other pure-Python utilities use the standard library. Channel sheets are observations, not role inference. Material plans validate evidence structure, not visual truth. Generic Toon/Principled seeds remain experimental fixture graphs, not Wuthering Waves material presets.

Forty-one utility tests passed. Blender is unavailable in this authoring environment. Live Blender execution, original-model fidelity, actual laptop FPS and cross-machine replay remain unqualified. Read [qualification.md](skills/anime-blender-pipeline/references/qualification.md) before claiming those results. The target remains a Cycles blend with usable animation preview, editable unbaked physics and verified portability; no timing claim is implied by these documents.

## Mathematical integration

All eleven skills now link to stage-specific fitting/measurement procedures, with a tested CIEDE2000 helper and provisional regional Delta E <3 target. External camera/IK/ARAP/PSD/preference/inverse-simulation solvers are documented methods, not bundled Blender implementations. See [WORKFLOW_COMPARISON.md](WORKFLOW_COMPARISON.md) for the active hierarchy and an unapplied simplification proposal. The ten stages, ledger checks and gates remain unchanged.
