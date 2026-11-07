# Ministral 3 8B — final Stage03 benchmark report

## 1. Experiment summary

Model: ministral-3:8b, Q4_K_M. Ten sequential user-authorized laps: six synthetic development laps, then four real-character proposal trials. Synthetic and real results are not pooled. No real-character pass was established.

## 2. Synthetic development results

| Lap | Verified first-try passes | Main observation |
|---|---:|---|
| 01 | 0/20 | Code value was an object rather than a string |
| 02 | 0/20 | Blender API exceptions |
| 03 | 12/20 | API guidance helped; eight remove-keyword errors remained |
| 04 | 20/20 | Argument clarification plus wording change |
| 05 | 20/20 | Wording reverted; argument clarification retained |
| 06 | 20/20 | Exact unchanged repeat; every generated response matched lap 05 |

The final two synthetic successes, laps 05 and 06, remain preserved and hash-verified. These are twenty reused development cases in five correlated families, not 120 independent cases. The current synthetic oracle does not separately score returned modified-count accuracy.

## 3. Real-character results

| Lap | Context / output limits | Outcome |
|---|---|---|
| 07 | 4096 / 1536 | Output truncated; invalid JSON; no candidate execution |
| 08 | 8192 / 4096 | Valid response; invalid GEOMETRY modifier type during execution |
| 09 | 8192 / 4096 | Missing explanation key; rejected code also had invalid Python syntax |
| 10 | 8192 / 4096 | Valid format/syntax; GeometryNodesTree typo crashed execution; placeholder assumptions remained |

Four unsuccessful proposals on one unique real fixture. None reached a completed independent real-result verification. Later prompts are feedback-assisted; the first attempt is preserved separately.

## 4. Prompt specialization and comparison limits

Synthetic output-schema and API clarifications improved development scores. Changing concise to succinct was not necessary for the observed 20/20 result: lap 05 restored concise, and lap 06 reproduced its outputs exactly. Real-exam guidance improved some API names and final output formatting, but no correct executable repair emerged.

The original real input/reference, base exam prompt and evaluator match the standardized Qwen challenge. Lap 07 deliberately retained Ministral's smaller decoding budget; laps 08–10 raised context/output budgets, and laps 09–10 added general guidance. Other optional decoding controls remained Ministral defaults/omissions. Do not treat all these trials as identical prompt/decoding conditions or independent holdout measurements.

## 5. Safety and integrity

Synthetic ledger/artifacts verify. Recorded model-layer hashes and source assets verified before/after the real trials. Candidate code ran in the existing gated no-network Blender/bubblewrap isolation environment, rather than directly in the host process environment. This was the installed Blender runtime, not a Blender Docker image. The real verifier was not reached for Ministral. No failed answer was extracted, patched or rerun under an old identifier. This public export contains only allowlisted text and metrics.

## 6. Findings and limits

Observed weaknesses include output-contract compliance, Blender identifier/property accuracy, and replacing measured task implementation with conceptual or placeholder logic. Successful JSON and valid Python syntax did not imply Blender API validity. One real fixture is insufficient to generalize failure to all Blender tasks; repeated synthetic success is also insufficient to qualify real use. Production cost and human artistic acceptance are unmeasured.

## 7. Final verdict

Verified synthetic development competence after prompt help; **no demonstrated real-character Stage03 success**. Not qualified for unattended real-character repair on this evidence. The requested ten-lap sequence is finished; no additional lap starts automatically.


Supporting material: [analysis notes](analysis-notes.md), [machine-readable metrics](analysis-data.json), [lap prompts](prompts/README.md), and [privacy/provenance](privacy-and-provenance.md).
