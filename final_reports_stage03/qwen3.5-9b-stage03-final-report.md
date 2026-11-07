# Qwen3.5 9B — final Stage03 evaluation report

Finalized 2026-11-07. Sanitized public edition. Narrative interpretation is by the benchmark operator; numerical synthetic results were regenerated from verified saved events. This report covers one model only. [Prompts are archived by lap and trial](prompts/README.md).

## 1. Experiment Summary

Qwen3.5 9B Q4_K_M (`qwen3.5:9b`) completed eight synthetic development laps, followed by one primary real-character attempt and one explicitly assisted final retry. These are ten recorded evaluation phases, not ten interchangeable synthetic laps. No synthetic laps 9 or 10 were run. Weights were not trained or fine-tuned; adjustments changed prompts or inference settings.

Model digest: `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90`.

The synthetic task normalized deform weights on the same 20 development fixtures from five synthetic families each lap. It produced 160 first-try attempts across eight laps, representing 20 reused cases. The real task asked for repair of a hair self-shadow artifact from a pre-repair Stage02 checkpoint while preserving source geometry, shape keys, materials, eyes, rig and animation behavior. Its accepted Stage03 reference remained private. This is a different repair operation, so the two task scores are not pooled.

Blender 5.2.2 was used. Synthetic lap 1 used temperature 0, context 4,096, output limit 1,536 and server-default thinking. Lap 2 used context 8,192, output limit 4,096 and explicit thinking disabled. Lap 3 also set presence penalty to 0 and added API guidance; laps 4-8 kept those generation settings. Synthetic seeds were not specified. Both real attempts used temperature 0, context 8,192, output limit 4,096, thinking disabled, seed 0, presence penalty 0, repeat penalty 1 and JSON output.

## 2. Performance, Quality and Benchmark Results

All first attempts remain in each denominator. Blocked, not-run and missing verdicts never count as passes. No within-case synthetic repair attempts were recorded. Severe regression flags were zero in all eight laps; this is a recorded metric, not a general safety guarantee.

| Synthetic lap | First-try pass | Rate | Wilson 95% | Fail | Blocked | Not run | No verdict |
|---|---:|---:|---|---:|---:|---:|---:|
| 1 | 0/20 | 0% | 0-16% | 0 | 0 | 20 | 0 |
| 2 | 0/20 | 0% | 0-16% | 1 | 17 | 2 | 0 |
| 3 | 19/20 | 95% | 76-99% | 0 | 1 | 0 | 0 |
| 4 | 19/20 | 95% | 76-99% | 0 | 1 | 0 | 0 |
| 5 | 19/20 | 95% | 76-99% | 0 | 1 | 0 | 0 |
| 6 | 7/20 | 35% | 18-57% | 0 | 13 | 0 | 0 |
| 7 | 14/20 | 70% | 48-85% | 1 | 5 | 0 | 0 |
| 8 | 20/20 | 100% | 84-100% | 0 | 0 | 0 | 0 |

These exploratory intervals assume more independence than reused, correlated development fixtures provide. They do not estimate production reliability.

| Synthetic lap | p50 / p95 model + oracle seconds | Model + oracle passes/min | Input / output tokens |
|---|---:|---:|---:|
| 1 | 87.9 / 90.6 | 0.00 | 6,084 / 30,720 |
| 2 | 41.2 / 57.3 | 0.00 | 6,124 / 13,384 |
| 3 | 31.0 / 43.5 | 1.69 | 14,064 / 10,661 |
| 4 | 30.5 / 43.0 | 1.71 | 14,064 / 10,661 |
| 5 | 30.4 / 42.3 | 1.73 | 14,064 / 10,661 |
| 6 | 32.0 / 70.6 | 0.56 | 16,784 / 11,906 |
| 7 | 33.7 / 49.0 | 1.18 | 15,844 / 11,288 |
| 8 | 30.9 / 37.7 | 1.90 | 17,944 / 9,870 |

Timing and throughput above exclude human review and are not end-to-end workflow measurements. Cost and operator effort relative to the accepted workflow were not measured.

| Real-character trial | Primary score contribution | Observed result | Input / output tokens | Inference / total seconds |
|---|---|---|---:|---:|
| Unassisted first attempt | 0/1 | Valid saved derivative; repair absent; fresh verifier rejected it | 980 / 1,391 | 92.94 / 178.73 |
| Assisted final retry | Separate; does not replace primary score | Incomplete JSON at output limit; no candidate execution or Blender verdict | 1,009 / 4,096 | 272.38 / 285.08 |

Both real submissions were unsuccessful. Only the first produced a Blender artifact and reached structural verification. There is one unique real character, not two independent real cases.

## 3. Lap-by-Lap Failure and Adjustment Analysis

The following diagnoses are operator interpretations of retained evidence. Generic ledger categories are preserved separately below rather than silently relabeled.

| Phase | Adjustment and observed failure |
|---|---|
| Synthetic 1 | Initial configuration yielded no usable code in all 20 cases. Recorded diagnosis identified output budget consumed by thinking. |
| Synthetic 2 | Increased context/output and disabled thinking. Object-versus-Mesh ownership, weight-method calls and membership errors persisted, with two syntax errors, two unusable proposals and one normalization failure. |
| Synthetic 3 | Added verified Blender API guidance and set presence penalty to zero. Nineteen cases passed; case 007 used an unsupported collection length attribute. Multiple settings changed together; individual causal contribution was not isolated. |
| Synthetic 4 | Unchanged repeat of lap 3; the same case failed at the builder stage. |
| Synthetic 5 | Unchanged repeat; the same case failed again. Retained builder evidence confirmed the unsupported length attribute. Repeating the same prompt and deterministic settings did not fix that API assumption. |
| Synthetic 6 | Added guidance about collection length, sparse assignments and returned modification counts. Result fell to 7/20: thirteen builder failures involved integer membership tests on Blender collections or a vertex-group object. All proposals were syntactically valid; generation ended normally. No controlled ablation identifies which wording caused the regression. |
| Synthetic 7 | Removed unrelated stage guidance and replaced the length warning with a plain Python explanation. Result recovered to 14/20. Remaining errors included group-versus-vertex ID confusion, integer containment, treating assignment objects as tuples and an invented API attribute. |
| Synthetic 8 | Added a simple explanation of vertex IDs, group IDs and membership assignments. All 20 reused cases passed. This is development-set success after feedback, not an untouched holdout result. |
| Real first attempt | Code relied on the active object, which was an EMPTY model root. A guard returned zero before reaching the repair logic. The actual named mesh was already present in the input summary. Fresh evaluation confirmed no repair; protected source data remained intact. Static problems in the unreached body were not counted as additional observed crashes. |
| Real final retry | Added only the instruction to select the named mesh explicitly. The partial text reflected that instruction, then repeatedly discussed possible modifiers without completing an implementation. It used all 4,096 output tokens and ended inside a JSON string. Strict parsing rejected it; no attempt was made to complete or execute the partial response. |

The final retry used identical input, weights, decoding, sandbox, evaluator and resource limits. Its feedback-assisted prompt is separate from the primary common prompt; future primary entrants retain the original conditions.

Every synthetic non-pass is retained below. Case numbers are generic synthetic fixture IDs. The recorded severity `none` is not an assertion that a failed submission was useful or safe.

| Lap | Case IDs | Result | Recorded category / severity | Sanitized evaluator note |
|---|---|---|---|---|
| 1 | 000, 001, 002, 003, 004, 005, 006, 007, 008, 009, 010, 011, 012, 013, 014, 015, 016, 017, 018, 019 | not_run | invalid_output / none | No usable proposal code; candidate not executed. |
| 2 | 000, 001, 002, 003, 004, 005, 006, 007, 008, 009, 010, 011, 015, 016, 017, 018, 019 | blocked | evaluator / none | Builder exited before a usable fresh verification result; see the attributed diagnosis in this section. |
| 2 | 012 | fail | deformation / major | Verifier rejected deform-weight normalization. |
| 2 | 013, 014 | not_run | invalid_output / none | No usable proposal code; candidate not executed. |
| 3 | 007 | blocked | evaluator / none | Builder exited before a usable fresh verification result; see the attributed diagnosis in this section. |
| 4 | 007 | blocked | evaluator / none | Builder exited before a usable fresh verification result; see the attributed diagnosis in this section. |
| 5 | 007 | blocked | evaluator / none | Builder exited before a usable fresh verification result; see the attributed diagnosis in this section. |
| 6 | 000, 004, 005, 006, 007, 008, 011, 012, 013, 015, 017, 018, 019 | blocked | evaluator / none | Builder exited before a usable fresh verification result; see the attributed diagnosis in this section. |
| 7 | 005 | fail | deformation / major | Verifier rejected deform-weight normalization. |
| 7 | 008, 010, 012, 018, 019 | blocked | evaluator / none | Builder exited before a usable fresh verification result; see the attributed diagnosis in this section. |

There are no non-pass cases in synthetic lap 8. Private raw artifacts remain with the operator; this public summary is not a substitute for their full verification bundle.

## 4. Specialization Effectiveness

The synthetic baseline had 0/20 usable passes; lap 8 reached 20/20 on the same cases after prompt and settings changes. Laps 3-5 repeated 19/20, lap 6 regressed, and lap 7 partly recovered. This demonstrates sensitivity to API guidance and wording within this development set. It does not demonstrate learning in the weights, independent generalization, or stable real-character competence.

The real first attempt failed on object context. The assisted retry reflected the mesh-selection instruction in incomplete text but failed to produce an executable repair. Thus the synthetic gate did not establish readiness for the distinct real hair-repair task. Other tasks, canaries, independent validation and untouched holdouts were not measured here. No cross-model conclusion is made.

## 5. Workflow Integration, Reliability and Safety

Generated scripts were never executed directly on the host. The primary real candidate ran in the existing isolated local Blender sandbox; it was not run in a Blender Docker image. Input assets were read-only, the private reference was unavailable to candidate code, and snapshot/verifier processes were separate from candidate execution. The final retry was rejected before any sandbox execution.

Original assets and qualified model blobs verified unchanged after both real trials. The final retry preserved the original first-attempt result, common prompt and frozen contract. The controller finished, Qwen was unloaded and no further attempt was automatically scheduled.

The retained setup evidence records 103 passing tests, stable repeated reference snapshots, two accepted positive controls, seven rejected negative scene controls and seven passing boundary/artifact/lifecycle probes. These bounded checks do not prove immunity to unknown application or operating-system vulnerabilities. An independent subagent implementation/review did not complete because of usage limits; no completed independent review is claimed. Human artistic acceptance and production approval were not obtained.

This sanitized report and the separately labeled per-lap prompt archive are published. Local usernames, absolute filesystem paths, machine/network identifiers, source-character identifiers, asset fingerprints, checkpoints, textures, renders, private manifests, raw outputs, logs and operational sandbox details are excluded from this report. The accompanying archive publishes exact synthetic prompts and redacted real-character prompts. The private original reports and evidence are retained locally.

## 6. Miscellaneous Findings and Future Model Analysis

Synthetic evidence was reverified before export: 328 hash-chained events, 160 attempts and 160 recorded verdicts. The eight saved status summaries agree with freshly computed counts. Each lap has 20 generic synthetic cases and five families. Verdict records mark isolation verified, including not-run records; that field does not imply every proposal reached Blender. No decision events were recorded.

The real adapter stores separate controller, builder, fresh-snapshot and verifier evidence; its trials were not added to the synthetic ledger. Their values here come from the retained real-trial records. The final retry records `done_reason: length`, exactly 4,096 output tokens and zero sandbox execution records. Both before/after model-integrity records match. The primary prompt/contract/status hashes also remained unchanged.

Exact synthetic prompt text and request settings are available in the accompanying archive. Real-character reproducibility remains limited because identifying prompt details are redacted and private assets, manifests and raw evidence are withheld. No independent public reproduction or cryptographic attestation is claimed. The hash chain detects inconsistencies in saved data but is not a tamper-proof audit system. A finalized report does not imply an accepted model result.

## 7. Final Verdict

**Development-only evidence; real-character repair unsuccessful; not production qualified.** The retained synthetic observations meet the numerical pilot pass threshold in laps 3-5 and 8. The distinct real primary score remains 0/1, and the final assisted trial is separately unsuccessful at proposal validation.

The synthetic ledger's readiness remains level 2 (verified synthetic observations). Separate unsuccessful real-asset evidence now exists; it does not automatically advance the ledger's readiness or grant production status. Validation-based model selection, sufficient independent real cases and source families, both animation tracks, exact-scope independent review, human acceptance and a measured cost/effort baseline remain unmet or unmeasured. Reused development cases cannot satisfy those requirements.

Capability rows below are sanitized summaries, not approval certificates. `best_lap_id` remains null because there was no validation split. Lap 8 is an observed development result only. The assisted retry is excluded from the primary capability row.

```json
[
  {
    "task_id": "geometry_weight_normalize",
    "model_digest": "56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90",
    "best_lap_id": null,
    "development_observation_lap": "lap-08",
    "first_try_pass_count": 20,
    "n": 20,
    "uncertainty": "Wilson 95%: 84-100%; reused development cases",
    "trusted_scope": "synthetic development only",
    "evidence_ref": "#2-performance-quality-and-benchmark-results"
  },
  {
    "task_id": "real_character_hair_repair",
    "model_digest": "56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90",
    "best_lap_id": null,
    "first_try_pass_count": 0,
    "n": 1,
    "uncertainty": "one character; generalization not established",
    "trusted_scope": "unsuccessful primary real-asset attempt",
    "evidence_ref": "#3-lap-by-lap-failure-and-adjustment-analysis"
  }
]
```

No model candidate was promoted over an approved checkpoint. No further lap is running or scheduled.
