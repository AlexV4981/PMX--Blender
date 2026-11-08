# Additional analysis

All findings below are operator interpretations; machine-readable measurements are separate.

## lap-01

Change: Original frozen baseline; thinking control omitted, native thinking default enabled.

Observed: All20 responses exhausted the1536-token cap with thinking and empty final response. Budget/configuration failure, not demonstrated Blender runtime failures. Wall time:33.48 minutes.

## lap-02

Change: Only think=false added.

Observed: Thinking off enabled final answers, but API hallucinations, syntax mistakes, incomplete repairs and one truncated response remained. Wall time:17.29 minutes.

## lap-03

Change: Append the exact original general Blender API appendix used in the initial project benchmark.

Observed: 18/20; two attempts treated sparse VertexGroupElement objects as unpackable pairs. Wall time:11.91 minutes.

## lap-04

Change: Append general vertex-group ownership, sparse membership and collection clarification.

Observed: 17/20; three double-escaped newline syntax failures. No tuple-unpacking errors among executable candidates. Wall time:15.75 minutes.

## lap-05

Change: Append JSON encode-once and newline-separator clarification.

Observed: 19/20; one double-escaped newline remained. Wall time:17.87 minutes.

## lap-06

Change: Same first-attempt prompts/settings as lap05; allow one syntax-feedback repair, separately scored.

Observed: 19/20 first try; the single syntax-feedback repair passed, yielding20/20 assisted. Operator bookkeeping recovery described separately. Wall time:17.46 minutes.

## lap-07

Change: First real-character exam: frozen common task and original decoding profile, no retry.

Observed: Valid JSON/Python reached solve; invalid GeometryNodes enum stopped the builder. No fresh geometry verdict. Wall time:1.58 minutes.

## lap-08

Change: Append general Geometry Nodes API guidance only.

Observed: Explanation prose emitted as a key with literal value explanation. Contract rejected response before execution. Wall time:1.84 minutes.

## lap-09

Change: Exact repeat of lap08 prompt and settings.

Observed: Request and final response text exactly matched lap08; same response-schema failure. Wall time:1.88 minutes.

## lap-10

Change: Only enable thinking; retain lap09 prompt and all other controls.

Observed: Thinking consumed4096 output tokens; empty final response. No candidate or Blender execution. Wall time:5.17 minutes.

## Failure details and implications

Lap02 had12 runtime API failures,3 syntax failures,4 fresh-state normalization failures and1 truncated final response. Runtime errors included Mesh.vertex_groups, invented MeshVertex.data/VertexGroup.data, scalar indices or incorrect mode/argument counts in VertexGroup.add. Four state failures included placeholder work and copying unnormalized reference values. The input's expected-state data is not an acceptable substitute for measuring and modifying current state.

Lap03's two blocked candidates tried to unpack VertexGroupElement assignments as pairs. Lap04's three source errors and lap05/06's one source error were literal backslash-n statement separators after JSON decoding, not sandbox-specific indentation problems. No global unescaping was used because legitimate Python string escapes must remain intact. The separately generated lap06 syntax repair succeeded.

Lap06's controller incorrectly used global submission number2 as attempt_no2 in a new isolated repair ledger. Its monotonic rule required local attempt1. Original frozen controller, stopped status and raw repair were preserved; a new normalization derivative retained model_submission_number2. The saved repair was sandbox-evaluated without another model call. The first-attempt ledger was not changed. New regression coverage exercises the actual ingester/ledger, not only a callback mock. Original run duration excludes later recovery and operator time.

Lap07 used GeometryNodes where node_groups.new requires GeometryNodeTree. Candidate execution began but builder did not complete; the legacy candidate_executed=false field must not be read as proof of no execution. Laps08/09 corrected that type in generated text but inverted explanation key/value, failing the strict two-key response contract. Code was not extracted or run. Exact repetition yielded identical final response text in the observed pair. It does not establish universal determinism.

Lap10 enabled thinking only. It used all4096 output tokens, returned thinking but no final response, and stopped for length. The resulting JSONDecodeError was downstream of empty output. There is no evidence that the8192-token context window was exhausted. This boolean thinking setting is not a bounded low-thinking level.

## Qualification and cost limits

Twenty reused synthetic cases in five correlated families support development observations. Six repetitions are not120 independent fixtures. Four real trials used one character, no held-out successful geometry comparison or Cycles acceptance. The numerical75% synthetic pilot bar was reached, but the <=35% original-workflow effort gate is unmeasured. No300 independent held-out production examples, multiple source families, independent reviewer approval or human stage acceptance exists. Returned synthetic count accuracy is not independently scored. No cross-model ranking is made.
