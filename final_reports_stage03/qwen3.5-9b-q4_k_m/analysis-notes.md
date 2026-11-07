# Additional details for future Stage03 analysis

This supplement adds information absent from the aggregate [final report](qwen3.5-9b-stage03-final-report.md). Measurements come from the saved synthetic ledger, outgoing requests, raw API metadata and selected real-trial records. Interpretations below are by the benchmark operator. No new model test was run to prepare this package.

## Native defaults versus requested settings

Saved model metadata declares 8,953,803,264 parameters, GGUF Q4_K_M, the qwen35 family and a llamacpp backend label. It advertises a 262,144-token context; the benchmark tested only 4,096 and 8,192. The advertised value is not a measured capacity or quality claim. A shared native-template hash and the small architecture metadata subset are in analysis-data.json; the full Modelfile is excluded because it can contain local storage paths.

The saved native parameters list presence_penalty=1.5, temperature=1, top_k=20 and top_p=0.95. Every recorded benchmark request explicitly used temperature=0. Synthetic laps 1-2 did not explicitly override presence_penalty; laps 3-8 did set it to 0. Both real trials explicitly set presence_penalty=0, repeat_penalty=1 and seed=0. Consult each archived request for exact explicit fields. No full engine-level resolved-options dump was recorded, so omitted options must not be invented. The Ollama version at measurement time was not captured here.

The lap-03 API-reference addition and presence-penalty override happened together. Their individual contributions were not isolated. This is a reason to use separate controlled interventions in later development, not evidence that a particular parameter caused a specific coding error.

## Completion, parsing and execution are distinct

All 20 synthetic lap-01 responses ended with done_reason=length and contained a nonempty thinking field, with no usable final code. All 140 responses in synthetic laps 2-8 ended with done_reason=stop and no nonempty thinking field. Lap 2 nevertheless had only 16 syntactically valid code submissions: a normal stop and valid outer JSON are not evidence of correct code.

The per-case dataset adds JSON validity, code presence, syntax validity, stop reason, token/cache counts, API timing components and trusted builder/verifier exit codes. It preserves every case, including passes. The JSON case table pairs each row with the ordered `columns` list; no fields are dropped by that compact encoding. No model-authored success field is substituted for a trusted verdict. Null exit codes and static syntax success must be interpreted using the field notes, not treated as proof of execution or repair.

## Evidence that repeated laps did not self-correct

For both lap 3→4 and lap 4→5, all 20 paired cases had identical prompt hashes, identical generated code bytes and identical final response text bytes. The same collection-length mistake on case 007 therefore repeated with an unchanged submission, not merely the same aggregate score. This is an observed result in these runs; it is not a general guarantee of deterministic inference on other runtimes or hardware. Repeating an unchanged request does not provide the model with feedback or update its weights.

## What remains unproven in the real repair

The first real submission's zero return was accurate, but occurred before its repair body ran. A subsequent read-only context/API inspection diagnosed that guard; it was not a second execution of the generated repair. Incomplete or unreachable code can contain additional issues without establishing an observed second runtime failure.

The assisted final response contained 16,368 characters, including nine occurrences of one identical planning comment, and stopped mid-string at 4,096 output tokens. Its malformed JSON was not completed or repaired by the operator. No candidate script or Blender result was created. More output allowance alone has not been shown to produce a valid algorithm. These observations support studying completion and repetition separately from geometry correctness; they do not prove a mechanism inside the model weights.

## How to extend this record

Keep the frozen primary real result and this finalized snapshot distinct from future prompt-assisted development. New runs need their own lap/trial identifiers, exact requests and provenance. Use new independent fixtures before claiming transfer; development-case repetitions and the single real character do not provide independent case coverage. Treat object selection, valid output, API execution and actual geometric repair as separate failure stages.

Check the [public package checksums](SHA256SUMS) before analyzing these files. They detect changed public bytes, not independent authenticity or correctness. The raw evidence stays local, so this public package supports inspection of the published measurements rather than full reproduction against private assets.
