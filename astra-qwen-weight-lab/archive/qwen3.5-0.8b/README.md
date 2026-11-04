# Archived Qwen3.5-0.8B experiments — November 2026

Immutable retrospective source copy. These files were copied by Git blob identity from the `Qwen-Local-Helper` branch at commit `7517ccfed5017bc0080da72adac650cd4a4ffe41`. Do not execute archived setup scripts for the current 7B experiment.

## Archive inventory

- `astra-lab/`: previous standalone MIT-style 0.8B weight-edit code, tests, documentation, configuration, pilot cases, patcher and scoring.
- `workbench-pilot/`: earlier nested 0.8B pilot scripts and docs.
- `reports/`: full observed Stage 03, 04 and 05 attempts (also left at their original report paths to preserve existing references).

## Recorded outcome

The Stage 03/04/05 reports show all compared 0.8B source/weight-edited responses failed the requested Blender inventory or diagnostic. Output often contained invented Blender API properties, JSON truncation/loops, or unverified scene assumptions. None of those output scripts was executed in Blender; do not interpret code parse as semantic correctness. The isolated Stage 04 arm pilot under the original Codex workflow did not resolve pole placement or complete the full rig gate.

These records are small-sample exploratory failures, not a statistically representative overall model score. No 0.8B patch was promoted. The active 7B pipeline lives at `../../README.md`; do not mix archived results into 7B baselines.

Source snapshot: 7517ccfed5017bc0080da72adac650cd4a4ffe41

## Retrospective data limitation

This Git archive preserves the tracked experiment scripts, configurations, and the full three published trial reports. Raw model completions, HF weight shards, patched checkpoints and other files stored solely in the old ignored local `data/` directories were **not committed**, and therefore are **not** part of this GitHub archive. Preserve a separate local backup of those original raw artifacts if they are still present and needed for a reproducible retrospective. Do not infer their availability from this archive.
