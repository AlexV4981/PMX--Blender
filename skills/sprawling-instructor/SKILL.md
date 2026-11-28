---
name: sprawling-instructor
description: Evidence-first execution guidance for long multi-stage projects; prevent repeated unsuccessful work, context growth and unbounded investigations while preserving authoritative approvals and requirements.
---

# Sprawling Instructor

This optional skill is separate from Graphify Pipeline. It adds a persistent work-budget journal, not authority to approve work. Graphify remains a read-only source navigator; use it when installed, or use the project's source index.

## Run protocol

1. Read the authoritative project contract, current checkpoint, active issue and relevant evidence only. Never load the whole history by default. Verify graph/source freshness. Do not infer that a graph edge or an agent report is an approval.
2. Initialize the budget journal once per run using explicit human-approved positive integer limits for run, stage and issue attempts. Use stable issue IDs, even if ownership, revision or hypothesis changes. Journal paths must persist across sessions; archive evidence, not counters.
3. Record a narrowly scoped issue with its owner, baseline, protected behavior, completion criterion and distinguishing test. Before any experiment, reserve an attempt with a unique evidence-backed hypothesis. All implementation attempts and renewed diagnostic cycles count. No work after a blocked decision; two non-improving implementations require rollback and renewed causal evidence. The third non-improvement blocks further attempts on that issue. Run and stage limits also apply.
4. Record outcome with an immutable evidence reference: improved, rejected, inconclusive, harness-failure, environment-failure, or diagnosis. Classify failures before changing the model. A harness failure is not a model failure. No claims from placeholder measurements. An interrupted reservation remains charged and pending until disposition.
5. Escalate exhausted budgets, conflicting requirements, absent evidence or repeated failure. Report the best checkpoint and alternatives. Do not rename issues or restart the journal to bypass limits. Any extension needs an observed explicit human decision and a new authorized policy; the supplied CLI intentionally does not grant extensions.
6. Use deterministic tools for hashing, inventory, repeatable validation, bookkeeping and indexing. Use AI for interpretation, new causal hypotheses and implementation. Validate harnesses with positive and negative controls; predefine acceptance criteria. Reuse evidence only with verified matching dependencies; unknown dependencies require fresh tests.
7. Final completion requires authoritative gate evidence and human decisions where required. A stopped investigation is not a passed check.

## Context and documentation

Keep AGENTS.md <= 8,000 bytes and RESUME-HERE.md <= 12,000 bytes as proposed pilot limits. Keep one authoritative current state; archive superseded instructions unchanged. Human summary: what changed, what failed, preserved quality, remaining work and decision needed, in plain language within one screen. Engineering report: hypotheses, actual measurements, limits, dependencies, rollback. Machine evidence: artifacts, hashes, test versions, statuses, duration and actual usage if available (estimates labeled).

Use `scripts/budget.py --help`. The journal counts reservations, not tokens. It cannot prevent direct execution outside the wrapper, verify human identity or prove a hypothesis. Project-specific gate enforcement remains with the project. See README for examples and pilot limitations.

## Convergence review

Use `budget.py report JOURNAL` at handoff and before authorizing more work. Compare retained improvement with effort, distinguish measured and estimated token counts, and report missing coverage. A failed renewed diagnosis is terminal for that issue under the pilot journal; do not create another issue ID to retry it. Use the project defect register to link aliases or shared causes. Before expensive verification run a static preflight and focused smoke/viability test; full acceptance is unchanged. If no viable experiment remains, report blocked/deferred rather than keeping the agent busy. Record one compact status summary for the human and preserve detailed evidence separately.

## Artifact lifecycle subgate

At completed technical subgate batches, run the [exact duplicate artifact procedure](references/artifact-dedup.md). Preserve all original paths and unique research evidence; use kernel copy-on-write storage sharing only on verified equal bytes in a quiescent workspace. Unsupported copies stay intact.
