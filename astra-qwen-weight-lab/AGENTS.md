# Agent guide

This directory is a self-contained optional model-weight experiment, not a new production pipeline. Work only here and its ignored `data/`. Never modify `qwen-helper/` (including original helpers and training workbench), `skills/`, accepted Blender artifacts, or `main`.

Read `CODEX_INSTALL_PROMPT.md` and `README.md`. Start with `lab.py doctor/init` and tests. Record exact installed model identity and pin weight SHA/revisions. Stage 00 remains Codex. Target stages 03–06 only. Keep four variants isolated.

All produced code and weight-delta files are untrusted. No generated Python execution or direct host Blender calls inside this lab. For actual qualification, Codex must use disposable, no-network sandbox execution on copied fixtures with observed commands and independent Sol Light review. Never fabricate evidence or use benchmark math claims as Blender evidence.

Weight changes are experiment artifacts; always compare against the intact baseline and MIT edited baseline when available. Astra may propose hypothesis and numeric patch using direct weight analysis only when model files and actual tools are available; do not assert weight modifications from a chat alone. Patch within hard fraction/norm bounds, never auto-promote.
