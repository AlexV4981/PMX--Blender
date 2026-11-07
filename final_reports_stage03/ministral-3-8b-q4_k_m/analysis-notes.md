# Additional analysis and interpretation

## Model and decoding

The pinned model digest, architecture, parameter count, quantization, native template hash and selected metadata appear in analysis-data.json. The model advertises completion, vision and tools; no thinking capability was advertised and no nonempty thinking output was observed. Native parameter metadata lists temperature 0.15; actual benchmark requests explicitly override temperature to 0. Do not equate metadata defaults with fully resolved per-request controls.

Synthetic requests use format=json, stream=false, num_ctx=4096 and num_predict=1536. Seed, think, presence penalty and repeat penalty are omitted. Real lap 7 retains that budget; laps 8–10 use 8192/4096. These numbers are tokens, not GB or guaranteed RAM/VRAM allocations. Engine version was not independently captured per lap; no per-lap version is asserted.

## Prompt changes and causal limits

Lap 1 reused Qwen's first synthetic prompt and explicit settings except model tag. Lap 2 requires code and explanation to be JSON strings. Lap 3 adds the literal loading-mesh sentence and the same original Blender API guidance Qwen received in its synthetic lap 3. Both additions occurred together, so their effects cannot be isolated.

Lap 4 changes concise to succinct and adds documented VertexGroup.remove argument clarification. Lap 5 restores concise while retaining the API clarification. Lap 6 repeats lap 5 unchanged. All twenty actual and frozen request bodies, generated response texts and Python code bytes match between laps 5 and 6. API envelope timings and timestamps are excluded. This is one observed repeat pair, not proof that temperature zero guarantees identical outputs on all engines or hardware.

The generic manual controller first used for lap 5 parameterized the parent/model experiment metadata; its generation, capture, unload, evaluation and scoring blocks were checked against the preceding controller. This operational change should be retained when analyzing provenance.

## Failure details

Lap 1 returned objects rather than strings for code: nineteen contained nested Python strings and one a structured function representation. None was rescued or executed. Lap 2's first runtime errors comprise eight Mesh.vertex_groups ownership errors, ten from_edit_mesh mode errors, one BMVert.groups error and one BMesh lookup-table error. Lap 3's eight failures all used unsupported VertexGroup.remove keyword arguments: six ok_if_not_assigned and two ok_if_empty. The remaining twelve passed independently.

The real base exam uses the same frozen input, accepted reference, task and evaluator as Qwen. Lap 7 has the smaller Ministral budget; lap 8 changes only context/output limits. Lap 9 appends general modifier API guidance; lap 10 appends mandatory explanation and no unsupported assumptions. Qwen's original real request explicitly set think=false, seed=0, presence_penalty=0 and repeat_penalty=1, while Ministral leaves those controls omitted. Equal assets and base task therefore do not imply identical full decoding conditions.

Real lap 7 hit the 1536 output cap and produced an unterminated JSON string. Input plus output tokens were below num_ctx; the immediate limit was output length. Lap 8 stopped normally but explanation was an object; the real collector permitted that type and executed syntax-valid code, which failed on modifier type GEOMETRY. Lap 9 stopped normally but omitted explanation and was rejected before execution; separate static inspection found an unmatched closing brace in the code string. It made untested assumptions including a percentage reduction. Lap 10 returned both required strings and valid Python, but execution failed on GeometryNodesTree instead of GeometryNodeTree. Placeholder implementation and unsupported assumptions remained.

Real source status candidate_executed=false is a builder-completion flag. The traceback proves execution in laps 8 and 10; neither completed the builder, exported a verified derivative, reached the fresh verifier or reached render acceptance. Do not interpret normal generation stop, valid JSON or valid Python as task completion.

## Evidence and limitations

All 120 synthetic attempts and verdicts are ledger/artifact verified. The final two synthetic successes remain preserved. Results cover twenty reused cases in five correlated families, not 120 independent fixtures. The synthetic state oracle checks deform-weight normalization and protected geometry, topology, transforms, shape keys and MASK data. Returned modified-count accuracy is not independently scored. Numerical pilot thresholds do not establish real-character qualification; production cost and human artistic acceptance are unmeasured.

Four unsuccessful proposals concern one unique real fixture, with feedback in later trials. No real domain failure score from a completed verifier exists. Model-layer/source integrity checks are recorded separately from task success. Runtime isolation used installed Blender 5.2.2 LTS with bubblewrap, systemd/cgroup and seccomp restrictions, not a Blender Docker image. Isolation checks do not prove the absence of every possible escape or protect evidence against a host administrator.

Some historical ledger boilerplate says container/runtime isolation was not verified in that release; specific run verdicts record isolation_verified=true and the local runtime identity. This package retains that distinction rather than representing the runs as Docker tests. Raw diagnostic logs remain private.
