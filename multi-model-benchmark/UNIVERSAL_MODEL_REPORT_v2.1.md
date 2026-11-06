# Universal AI Model Evaluation Report v2.1 (draft)

Exactly seven sections, one model and one specialization per report, every lap retained, no cross-model comparison. Numbers come from validated ledger events (see `EVIDENCE_LEDGER.md`); `python3 -m evidence.cli report` renders them. Human interpretation is added only as attributed narrative.

1. **Experiment Summary:** model digest and tag, task and nullable stage, laps, attempts, decoding, template-hash status, lap-declared environment, evidence-derived readiness.
2. **Performance, Quality and Benchmark Results:** per lap/task/split/role counts, first-try rate with Wilson interval, case and family counts, fail/not_run/blocked/no_verdict, severe regressions, offline repair successes (separate), p50/p95 model+oracle seconds, model+oracle passes per minute (excluding human review), tokens, exploratory gates (cost gate "not measured" unless a baseline exists), compromised holdout cases.
3. **Lap-by-Lap Failure and Adjustment Analysis:** every lap with controller-declared change reason and cases consulted, every non-pass attempt with category, severity, evaluator note and evidence link. Root cause is "unknown" unless narrative says otherwise.
4. **Specialization Effectiveness:** same-model baseline (parentless lap) versus later laps on matched cases, plus canary rows for other tasks. No canary rows means not measured.
5. **Workflow Integration, Reliability and Safety:** verdicts by result, isolation-verified count, runtime identities, attempts without a verdict, blocked reasons, evaluator limitations, recorded decisions.
6. **Miscellaneous Findings and Future Model Analysis:** reproducibility manifest derived from events (ledger head, oracle versions, selection-rule and split hashes, artifact counts).
7. **Final Verdict:** readiness level, unmet requirements for the next level, machine-readable capability rows (`task_id`, `model_digest`, `best_lap_id`, `first_try_pass_count`, `n`, `uncertainty`, `trusted_scope`, `evidence_ref`), recorded human decision or "none obtained".

Readiness levels, never higher than the evidence: 1 proposal-only; 2 verified synthetic observations (development-only); 3 real-asset evidence exists but production qualification remains blocked. At least 300 unique untouched independent real cases per specialist, multiple source families, both PMX/VMD and native Blender tracks, explicit exact-scope `sol_light_review` and `human_gate`, and an independently measured Codex effort baseline are required. This release cannot automatically emit a production-qualified verdict because the <=35% cost gate has no trusted producer. For non-PMX tasks, readiness remains domain-specific and not automatically qualified.

Best lap is chosen by a rule frozen at lap 0: highest validation-split first-try rate, ties broken by lower mean verified seconds. With no validation split the capability row has `best_lap_id: null` and reports dev-only counts per lap.

Domain content (Blender stage checks, the 75% / 35% / 300 thresholds, motion tests) belongs to a domain attachment. In this change the thresholds still appear in the generator as constants (`PILOT_N`, `PILOT_RATE`, `PROD_N` in `evidence/report.py`) because the PMX project is its only user; moving them to a profile is a follow-up.

## Migration from committed v1 (`MODEL_REPORT_STANDARD.md`)

v1 is left untouched. Same: seven sections, lap chronology, within-model comparison, no cross-model section. Changed: tables are generated, not typed; a first-try pass requires a hash-bound, isolation-verified verdict; `first_try`, severity and approvals cannot be self-declared; retries are counted separately; holdout exposure is recorded; Section 6 manifest is derived. v1 fields with no event source yet (hardware, license, Codex fallback, Sol Light review detail) print "not recorded" or "not measured"; add them as lap `environment` entries or new event types when needed. Historical Qwen-lab results stay on `archive/Qwen-Local-Helper-2026-11-05` and are not converted.
