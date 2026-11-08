# Additional analysis

Observed results and operator interpretations; original private evidence remains intact.

## lap-01

Change: Original baseline prompts and explicit decoding controls; only model tag differs.

Observed: 17/20; three candidates passed a list as VertexGroup.add weight, which requires one scalar float. Wall minutes:26.66.

## lap-02

Change: Append original Qwen-derived general Blender API helper, relabel heading, add scalar-float weight versus index-sequence clarification.

Observed: 20/20 first try; no weight-list errors. Full helper and targeted clarification added together, so individual effects cannot be isolated. Wall minutes:23.64.

## lap-03

Change: Exact repeat of lap02; no request changes.

Observed: 20/20; all20 final answer texts identical to02. Consistent observed pair, not universal reproducibility or generalization. Wall minutes:23.59.

## lap-04

Change: First real exam: frozen common prompt/input/evaluator and original real decoding controls. No extra synthetic appendix or repair.

Observed: Code ran but fresh snapshot exactly matched input. Material label treated as vertex-group name and early no-op return. Wall minutes:3.98.

## lap-05

Change: Append general identification guidance: distinguish object/material/group names and inspect measured regions.

Observed: Runtime failure: BMFace.co while iterating vertex.link_faces; no fresh verifier. Wall minutes:1.92.

## lap-06

Change: Append general BMesh element, adjacency, coordinate and lifecycle guidance.

Observed: Runtime failure: nonexistent bmesh.ops.bound_box; no fresh verifier. Wall minutes:2.80.

## lap-07

Change: Same first request as06; allow one syntax/runtime feedback repair. Feedback extractor defect documented.

Observed: First/repair both failed on bound_box. Repair received generic Blender script-failed footer, not specific exception: harness limitation. Wall minutes:7.05.

## lap-08

Change: Same first request; repair helper corrected to send the specific exception instead of generic footer.

Observed: Specific AttributeError delivered. Repair code hash identical to first attempt; same bound_box runtime failure. Wall minutes:7.15.

## lap-09

Change: Append brief API-review instruction; native thinking remains off. Repair policy unchanged.

Observed: Builder completed; verifier rejected protected-object change, reference surfaces and count metadata. Reported125942 removed versus actual0. Wall minutes:3.26.

## lap-10

Change: Only temperature0 to0.2; prompt and repair policy unchanged. Final speculative sampling trial.

Observed: Builder completed; snapshot exactly matched input, actual reduction0, reference surfaces still wrong. Different code but no task success. Wall minutes:3.53.

## Root causes and limits

Synthetic01's failed cases011,012,018 supplied a weight list to VertexGroup.add. Its indices argument is a sequence, but weight is one scalar. API appendix plus targeted clarification yielded20/20 in02 and unchanged repeat03; individual prompt factors cannot be isolated. All synthetic generations stopped normally; no token-cap or observed thinking issues.

Real04 searched for a group using a material label and returned0; all fresh snapshot fields matched input. Real05 accessed BMFace.co from vertex.link_faces. Real06 invented bmesh.ops.bound_box. Real07/08 initial proposals repeated the same nonexistent call;07 repair had defective generic-footer feedback, while08 supplied the precise exception but returned identical candidate code. Do not describe07 as ignoring the specific error it never received.

Real09 ran and reached fresh verifier but changed protected objects, missed target surfaces and returned125942 faces removed versus actual0. It used source-polygon selection counts rather than before/after evaluated geometry. Only the disposable candidate changed; original assets stayed intact. Real10 at temperature0.2 produced different code but all snapshot fields matched input, with0 face reduction. Speculative axis thresholds and untaken edit branches do not establish a repair. For10, unchanged output does not identify exactly which early-return condition was taken.

Repairs were allowed only after syntax or candidate runtime errors. Verifier failures in09/10 therefore did not trigger a repair. This is the declared policy, not a missing invocation. Shared candidate_executed=false means builder did not finish; tracebacks establish that runtime-failing candidates began solve. Socket-denial startup warnings were not fatal causes. No raw thinking/code was extracted to rescue answers.

Seven real trials used one character and an exposed task, not seven independent held-out cases. Three reached the independent geometry verifier and failed. Diagnostic CPU Cycles views are not artistic approval. No native low-thinking control is recorded; brief API review is a prompt change only. No claim of a faulty neural weight, context exhaustion, quantization causation or safe unattended conversion is supported. Original-workflow effort and comparative RAM/VRAM traces were not measured. Synthetic modified-count correctness is not independently scored.
