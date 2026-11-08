# Additional analysis and interpretation

These are operator interpretations alongside the immutable measurements in the seven-section report. Observed, inferred and unmeasured claims remain distinct.

## Per-lap interpretation

### lap-01

Change: Original frozen baseline; five captured responses, HTTP 500 on the sixth request, then fourteen local request-index guard failures.

Observed: 0/20 verified first-try passes; 6.16 minutes. Incomplete as a twenty-response model-quality measure. The fourteen unsent cases are harness failures, not demonstrated bad model answers.

### lap-02

Change: Prompts/settings unchanged. Capture-v2 reserves identities before transport and saves bounded HTTP errors; two token-repeat aborts.

Observed: 0/20 verified first-try passes; 17.45 minutes. Capture repair worked; a failed request no longer blocked later request identities. API hallucinations persist.

### lap-03

Change: Append exact original project Blender API appendix and raise output cap 1536 to4096. Two factors changed together.

Observed: 12/20 verified first-try passes; 12.53 minutes. 12/20 passes; remaining failures combine runtime API errors and repetition aborts. Guidance and budget effects cannot be isolated.

### lap-04

Change: Append sandbox-verified general vertex-group/collection guidance; switch stream=false to stream=true for partial-output capture.

Observed: 14/20 verified first-try passes; 12.99 minutes. Highest observed development score 14/20, below75% threshold. No repetition aborts; still API mistakes and an unfinished program.

### lap-05

Change: Permute one goal sentence only; all other request fields unchanged.

Observed: 13/20 verified first-try passes; 14.90 minutes. 13/20; five aborts localized to whitespace after prematurely closed code values. A one-run change is not a population estimate.

### lap-06

Change: Append direct-output/JSON-completion clarification targeting quoted-comment whitespace loops.

Observed: 11/20 verified first-try passes; 17.23 minutes. 11/20; aborts decreased to one but seven unfinished programs failed independent state checks. Not a complete loop remedy.

### lap-07

Change: Append comment-free executable implementation requirement; other controls unchanged.

Observed: 5/20 verified first-try passes; 18.82 minutes. 5/20; new restrictions frequently ignored. Nine unfinished programs, four API errors and two same-mechanism aborts.

### lap-08

Change: Restore lap-4 prompts verbatim and add only explicit top-level think=false relative to lap4. Sequential parent is lap7.

Observed: 13/20 verified first-try passes; 19.38 minutes. 13/20 with zero aborts, versus lap4 14/20 also with zero aborts. Explicit flag was transmitted but is not a demonstrated universal cure.

### lap-09

Change: Retain lap-8 prompts; change temperature0 to0.15 and explicitly set repeat_penalty1.20 together.

Observed: 4/20 verified first-try passes; 19.88 minutes. 4/20; no aborts, but twelve API runtime errors and two syntax errors. Combined sampling change did not improve measured correctness.

### lap-10

Change: Append a general API/formula/convention sheet verified in the installed Blender sandbox; preserve lap9 sampling settings.

Observed: 11/20 verified first-try passes; 26.70 minutes. 11/20; reference guidance helped relative to lap9, but generic Python/type mistakes, ID/object confusion and one unfinished program remain. Ten-lap sequence finished.

## Confirmed failure details

Lap1's five captured responses failed on invented VertexGroup.weights (two), get_weight (one), collection.index (one), and null bytes (one). Its sixth API request returned HTTP500. The capture wrapper indexed the expected frozen request by successful response count; after failure it still expected the old case and rejected fourteen later requests before transport. The original error body was not captured, so its server cause is unknown. Lap2's saved error bodies identified two token-repeat aborts; sixteen proposals failed API/source checks and two other responses hit the output cap and returned invalid JSON.

Lap3's six runtime failures comprise two missing bpy imports, three invented get_weight calls, and one numeric group ID passed to sparse assignment .find; two other requests aborted on repetition. Lap4's five runtime errors were four scalar IDs passed to VertexGroup.add and one attempted write via VertexGroup.weight. Its one independent state failure contained an unfinished implementation.

Lap5's five stream aborts exposed the whitespace mechanism described below; one other proposal had scalar-add misuse and one unfinished normalization. Lap6 reduced aborts to one, but seven unfinished programs failed the verifier and one scalar-add call crashed. Lap7 had nine unfinished programs, three scalar-add errors, one multiargument weight call, and two aborts despite the comment-free instruction. These programs were not rescued by removing comments or supplying missing code.

Lap8 had two scalar-add errors, one multiargument weight call and one .add call on an integer group ID. Its three state failures were one unfinished program and two implementations that lost/misassigned original paired weights before computing values. A normalization check failure is not always proof that the sum differs from one: required normalized component values must also be correct.

Lap9 had nine scalar-index add errors, two list-valued weight arguments, one multiargument weight call, two Python syntax errors and two incomplete programs. Lap10 had three .add calls on integer IDs, a tuple mutation, a string passed to abs, unpacking a scalar float, two syntax errors, and one unfinished normalization. General API guidance did not eliminate ordinary Python/type errors.

## Repetition evidence and limits

Five lap5 failures, one lap6 failure and two lap7 failures emitted instruction-quoting comments inside the code value, closed that JSON string, then emitted only whitespace before the server token-repeat abort. The public loop attachment records parsed boundaries, suffix lengths and repeated chunk counts without publishing generated code or internal reasoning. Empty terminal error events are excluded: the diagnostic count is101 nonempty public response chunks for the reproduced loops. Events need not correspond one-to-one with internal raw tokens.

The [Ollama v0.40.15 guard source](https://github.com/ollama/ollama/blob/v0.40.15/llm/llama_server.go#L1717-L1727) compares whitespace-trimmed output content and aborts above100 repeats. This explains the reference guard condition, not why a model/backend prefers whitespace. Version0.40.15 is recorded by the local installation receipt; a resolved engine version was not separately captured for every lap. Interaction among deterministic sampling, JSON grammar, prompt/template behavior and quotation handling is plausible but unisolated. No individual defective weight or VRAM-exhaustion cause is demonstrated. Laps8–10 had no aborts, but lap4 also had none without explicit think=false, so a universal fix is not established.

## Native thinking and sampling controls

The installed GGUF template defaults enable_thinking to true; earlier requests omitted think. No nonempty separate thinking field appeared in captured responses, and the saved model-show snapshot has no top-level thinking-default metadata. These facts do not independently establish effective internal thinking state. Lap8 explicitly sends top-level think=false in every actual request and records that flag accurately. Template contents are not silently patched, and native model weights remain unchanged.

The installed native parameters list temperature1 and top_p0.95, while the initial benchmark explicitly overrides temperature0. Lap9 changes temperature to0.15 and repeat_penalty to1.20 together; their individual effects cannot be isolated. repeat_last_n and seed remain omitted. Higher repeat penalty did not demonstrate coding improvement; both lap8 and9 already had no aborts. Source distribution, tokenizer, backend, sampling and quantization causality require separate controlled tests.

## Harness and execution provenance

The original capture template, capture-v2 repair, prepared output-budget support, stream-capture support, explicit thinking support and sampling forwarding revisions were archived locally. Per-lap controller hashes and actual request settings are in analysis-data.json. Regression tests reproduced failure before repair and passed afterward: sixteen focused plus85 benchmark tests for the first capture repair, then further targeted capture/forwarding tests as capabilities were added. Latest controller changes passed22 focused and85 benchmark tests. No extra model lap was consumed for those mock/unit tests.

Streaming began at lap4 as an explicit transport change. Complete response text was concatenated in order and final metrics preserved. Incomplete streams, HTTP errors and malformed bodies remain failures; partial source is never accepted as a completed candidate. Resource observation adds no inference, does not modify weights and stops after the run. Model residency observations showed partial RAM offloading; detailed hardware identity and resource traces remain private. Integrity hashes establish unchanged files, not neural-weight causal attribution.

General API notes were checked by operator-authored probes in the installed Blender sandbox. The final sheet covers group signatures, scalar-versus-sequence arguments, integer IDs versus objects, sparse assignments, generic unit-sum identities and separate numeric storage. Those are API/mathematical references, not a finished task solution. Probe summaries are exported; executable probe source and full logs remain private.

## Oracle, selection and reporting caveats

The independent state oracle checks required normalized values and protected geometry/topology/transforms/shape-key/MASK data. Returned modified-count accuracy is not independently scored. A builder exit code can reflect compilation failure before solve runs. A shared successful isolation probe is not evidence that each candidate executed or that every conceivable escape is impossible. The report retains legacy evaluator caveats and explicitly identifies the actual local runtime rather than presenting it as Docker.

There is no independent validation split, so formal best_lap_id remains null in capability rows. Lap4 is only the highest observed development score. No identical-repeat pair, independent hardware reproduction, real-character test, artistic review or human acceptance gate was measured. The canonical same-model baseline table is preserved, but lap1's harness defect prevents interpreting the entire numerical improvement from0% as model specialization. Confidence intervals are exploratory and optimistic for correlated reused families.

The75% pilot pass threshold was never met. The <=35% original-workflow effort gate is unmeasured. Production criteria require independent real held-out coverage and existing review/human gates; this archive does not establish them. These are scope limits, not missing values to fill with assumed passes.
