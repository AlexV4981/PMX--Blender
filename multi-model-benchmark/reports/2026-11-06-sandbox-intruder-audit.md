# Intruder subagent follow-up — 2026-11-06

User explicitly requested a subagent adversary and fixes for reproducible failures. The sandbox_intruder subagent ran two bounded rounds through the existing resource-controlled sandbox. No host escape was observed. Qwen remains unrun.

## Findings and fixes

1. Stage03 false pass: after normalizing weights, deleting every polygon still passed the legacy geometry snapshot. Added independent protected topology, vertex/key coordinate, UV, material/group, object-transform/modifier/constraint and armature-rest snapshots to the fresh verifier.
2. Stage04 false pass: a muted zero-influence IK constraint met the legacy structural test. Fresh verification now requires an enabled full-influence constraint and independently moves its target inward to measure endpoint motion, then restores it.
3. Parent audit also found that readiness stored security-receipt hashes without checking them. Missing or changed receipt files now block readiness. Runtime identity additionally binds the whole verifier/sandbox policy and runtime manifest rather than only the Blender executable.

## Independent re-test

The same adversary confirmed all five expectations: disabled IK, deleted faces, translated mesh and reversed face winding rejected; enabled full-influence IK accepted. Ten builder/verifier processes recorded effective cgroup enforcement and successful cleanup. Sources, verdicts and runtime records are preserved in ../data/local-runtime/intruder/semantic-before-fixes.json and semantic-after-fixes.json. No further concrete gap was identified in that bounded review.

Full suite: 85 unit tests passed. Existing NaN and forged-verdict probes still rejected. Final Stage03 smoke: correct PASS, deliberately wrong FAIL; fresh verification and evidence ledger passed. Final smoke evidence: ../data/stage03-smoke-20261106T175925Z/.

Hardened runtime policy version is v3. The execution gate and full runtime inventory are revalidated before another lap. Earlier v2 evidence remains historical and has a different runtime identity. The previous 15 controlled resource/boundary/forgery scenarios remain preserved, with five additional intruder regression scenarios recorded here. Prior readiness/evidence receipts were copied to ../data/local-runtime/before-intruder-round/ before this round.

No Docker image downloaded, software installed, host kernel exploitation attempted, or approved Lynae file mounted. No sandbox is proven unbreakable by these probes; host-kernel and Blender-native-parser vulnerabilities remain residual risks. The implementation and this summary are published on the benchmark branch. Raw host-specific evidence, assets and runtime inventories remain in ignored local data directories.
