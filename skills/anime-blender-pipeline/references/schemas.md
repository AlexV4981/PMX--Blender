# Artifacts and ledger

## Workspace files

- run.json: schema_version 1, pack_version, source identities, policy hash, stage/candidate state, dependency attempts and events. Manage through scripts/pipeline.py, not manual approval edits.
- policy.json: frozen assets/stage-policy.json. Its required_checks names are canonical; changing policy in an existing run is rejected.
- character-profile.json: copy assets/character-profile.template.json. Null means unknown. Populate facts/tolerances from observed data and pilot tests.
- work/ and candidates/: private derivative bundles. Register primary .blend and every linked texture/config asset. No shared writable assets between candidates.
- audit/: actual comparisons, clips, inventory, lint, fixture outputs and review reports. Distinguish pass/fail/blocked and justified not-applicable.
- checkpoints/submissions/STAGE/CANDIDATE/rNNNN/: snapshots of registered bundles. Preserve previous submissions and accepted history.

Source entries contain absolute path, bytes and SHA-256. Work/evidence entries contain workspace-relative path, bytes and SHA-256. Bundle identity hashes a canonical sorted manifest. Enumerate all dependencies; the ledger cannot discover unregistered external assets.

## Candidate lifecycle

draft -> awaiting_review -> approved. Observed human critique returns an unapproved submission to draft; register it after edits to create a revision and clear checks. One accepted candidate per stage, at most three IDs. Revise existing IDs after critique. Accepted stages remain immutable. Branch a new run to revisit accepted work, then revalidate/obtain affected approvals; do not copy approval records to a new run.

Candidate fields: ID/revision/status, primary path, artifact manifest, preceding input digest, bundle digest, checks, internal reviews and snapshots. Stage 00 input identifies sources; later inputs identify the preceding accepted bundle. Checks bind current bundle and independent nonempty evidence. Submission is not consent.

approve/review record externally observed human statements. The CLI cannot authenticate people or prevent fabricated consent; the conversation/UI is authoritative. Workers must never call these commands on their own authority. Every received approval must identify the actual candidate or be clarified.

## Stage 09

Record audit then delivery. Audit covers audit plus selected plan/not-needed disposition and remains historical across revisions within that scope. If scope changes, obtain a fresh audit decision. Delivery must identify the current submitted bundle and passing checks; it covers re-audit/delivery/final acceptance and approves stage 09 atomically. Re-submit after edits and repeat affected checks. The ledger cannot semantically prove every edit followed the selected plan.

## Recipe contents

Store source revision/hashes; scale/axes; environment lock; game-family/template versions; texture channels/color spaces; exact approved mesh/paint edits; bone correspondence/rest/weights; control conventions; expression/viseme and retarget mappings; solver settings/collision scope; toggles/reset/preroll; fixtures; cameras/world/lights/color management; assumptions and approved decisions.

Save manual edits as data or deterministic operations, not directives to make something look better. Validate source correspondence before replay. Separate build tools, embedded helpers and final runtime requirements. Include model-specific assets only under their applicable usage terms. The pack contains no game character or third-party professional model assets.

## Dependencies and escalation

Record up to ten distinct alternatives per final dependency, each with failed/succeeded outcome and nonempty evidence. Ten failures permit requesting a hyperspecific exception; they do not grant it. Record actual Astra role/session and resulting artifacts when used. If unavailable, record that fact and remaining choices, not manufactured escalation evidence.


## Diagnostic records

Use assets/material-plan.template.json. Record baseline evidence and each material's source ID, mesh/slot owner, disposition (preserve/proposed/blocked), output method/limits, PMX semantics, map hashes, image datablocks, UVs, role evidence, color-space rationale and regression evidence. Packed maps name all RGBA channels, including unused. Unknown roles stay unconnected; required unknowns block the material. Paths resolve relative to the plan file. Validator success is only structural evidence.

Do not add plan fields to run.json or manually mutate the frozen ledger policy. Register the plan as a candidate dependency and store its validation report separately. Maintain map/graph/fixture/recipe identity across changes. Version 3 uses pack_version 3.0.0; historical version 1/2 approvals remain in their original runs.

## Renderer and reused evidence

New profiles use CYCLES and RENDERED viewport with samples/denoising/device explicit. Other engines require a recorded explicit user request. Legacy preview check labels now mean Cycles Rendered viewport. A reused unchanged-component result is accompanied by a fresh current-bundle evidence report identifying original evidence, matching component/fixture/environment hashes and rationale. No copied approvals or invented test execution is permitted.
