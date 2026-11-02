# PMX model-agnostic default and per-character exceptions

**Goal:** Conversion behavior should be correct for common PMX cases by default; any *particular character's* deviations should be explicit, qualified overrides. "Most characters" is a design intention, **not** a proven success statistic.

## Default path

- Use the eleven existing PMX→native Blender skills and their ten stage handoffs as documented. Cycles-only render/checks; keep the human choice gates and candidate cap.
- Import and preserve observed PMX data; do not guess semantics from texture names. Use the deterministic inventory, math and diagnostics already bundled where sufficient.
- Leave unknown fields/thresholds as unknown. Do not impose game-specific shader, face, eye, rig, or physics assumptions on an unqualified character.
- Only dispatch Qwen for **menial coding**, not for the conversion itself: a reproducible incorrect zero result, a small report utility, unit test coverage, diagnostics or logging. Core pipeline files stay denied. If the task needs many modules, complex Blender evaluation, shader design, a guessed target, or visual judgment, route it to Codex.

## Character-specific customization

1. Copy `skills/anime-blender-pipeline/assets/character-profile.template.json` into the **run workspace** as `character-profile.json`, as prescribed by the main skill. Fill actual source IDs, scale, mappings, physics categories, reference evidence, limitations and tolerances based on that PMX character. Do not modify the committed template for each new character.
2. Store **observed** deviations in that run's profile/recipe and evidence. Keep the default unchanged for other characters.
3. If a tiny custom helper genuinely needs code, Codex can submit an **opt-in** Qwen task with `scope: character_specific`, `kind: new_tool`, target `qwen_character_<descriptive_name>.py`, nonempty `character_id`, `character_requirements`, and `generic_baseline`. Codex must verify requirements against the actual run profile before submission.
4. Review the proposed helper. Run generic automated tests *and* a targeted fixture for that character. Integrate only by explicit reference in its own run recipe. Do not make it a universal default or a required delivery dependency unless separately qualified.
5. If the change is actually a generic bug fix, solve it generically with a regression fixture covering ordinary cases and the character that revealed the error; do **not** hardcode a model ID.
6. If the character needs complicated shaders, bone structure, dynamics, new math or visual matching, **Codex** handles it; Qwen is not assigned architecture or artistic judgments.

## Qwen acceptance and reviewer threshold

Qwen tasks are individual code submissions, not conversion candidates. One file, one extra reference, small context, clear expected result, and a reproducible bug case when fixing a bug. The task gate enforces the **separation of generic and opt-in character-specific work**; byte limits are conservative heuristics rather than validated capacity limits for Qwen 7B.

Codex checks output, runs it in isolation after review, fixes failures, and records `passed_first_try`, `reviewer_repaired`, or `rejected_unresolved` in `qwen-helper/reviews.jsonl`. A reviewed repair/rejection rate **strictly greater than 10%** blocks new Qwen proposals and requires a prompt alert. An empty ledger means performance has not been measured.
