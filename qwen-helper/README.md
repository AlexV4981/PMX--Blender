# Qwen local maintenance helper — experimental

This worker is only for menial Python repairs and small new diagnostic tools. It is **not** allowed to change pipeline architecture, Blender rendering, materials, physics, rigging, candidate gates, or human approvals.

## Official benchmark basis

The Qwen team's [Qwen2.5-Coder release](https://qwenlm.github.io/blog/qwen2.5-coder/) and [Qwen2.5-Coder family report](https://qwenlm.github.io/blog/qwen2.5-coder-family/) report code generation/reasoning and repair evaluations. The headline **73.7 Aider score belongs to 32B Instruct**, not the 7B model. These benchmarks support exploring localized coding tasks, **not** a measured 90% success boundary for this 7B Q4 model in Blender. Start with the below conservative scope and refine it using actual outcomes.

## Capability admission hard stop

Accept: isolated, reproducible one-file Python bugs, unexpected `0` results with known expected input/output, small logging/tests, and standalone diagnostic scripts named `qwen_*.py`.

Reject to Codex *before inference*: cross-module refactors, unclear correct behavior, more than one reference, existing target or reference over 5,500 bytes, source/task over 9,200 characters, core `pipeline.py`, `blender_tools.py`, `math_tools.py`, `pmx_inventory.py`, anything requiring visual or mathematical solver architecture judgment. Generated replacement cannot exceed 6,500 bytes. These are deliberately chosen heuristics, **not** directly measured benchmark limits.

## Laptop use

1. Install Ollama on Nitro V and run `ollama pull qwen2.5-coder:7b-instruct-q4_K_M`. Confirm the exact tag is available and fits in 6 GB VRAM; model residency/performance have not been tested here.
2. Copy [task.example.json](task.example.json) outside tracked examples; replace with a real reproducible task and expected behavior.
3. Run `python qwen-helper/local_worker.py propose --task /path/to/real-task.json`. This calls local Ollama at 127.0.0.1:11434 (4K context); it **generates but does not run** proposed code.
4. Review `qwen-helper/outbox/<task-id>.json` and execute in a disposable local Git worktree: `python qwen-helper/local_worker.py apply --task /path/to/real-task.json --proposal qwen-helper/outbox/<task-id>.json`.
5. Apply syntax-checks, runs the repository Python test suite and seed validation, and **restores the original file if tests fail**. Also run a *task-specific* regression test. Unit tests alone cannot prove that the zero bug or Blender-specific behavior was fixed. Review the diff, do not automatically merge.
6. If Qwen fails, the higher-capability reviewer diagnoses and repairs it; preserve exact failing test/stack trace, diff and subsequent repair in a review entry. That human/Codex repair is not automatically performed by this helper or GitHub Actions.

### Repair-rate accounting and alerts

Each **reviewed** Qwen submission gets one manually verified JSONL row in [reviews.jsonl](reviews.jsonl), with `task_id`, `status`, `model`, `commit`, `verification`, `reviewed_at`, and `repair_notes` if it failed. Status must be `passed_first_try`, `reviewer_repaired`, or `rejected_unresolved`. A Qwen task that fails but is fixed by Codex counts as **reviewer_repaired**.

Example format only (not a real task): `{"task_id":"bugfix-001","status":"reviewer_repaired","model":"qwen2.5-coder:7b-instruct-q4_K_M","commit":"ACTUAL_COMMIT","verification":"test details","reviewed_at":"YYYY-MM-DD","repair_notes":"Describe actual fix"}`.

Run `python qwen-helper/review.py` to calculate:

**correction rate = (reviewer_repaired + rejected_unresolved) / all reviewed Qwen submissions**.

A strict rate **above 10%** (not equal to 10%) triggers a GitHub issue and failed CI once the updated ledger is pushed to this branch. With no reviews, the rate is **unmeasured**, not zero proven errors. Subscribe to GitHub issues/Actions notifications. GitHub notification delivery is not guaranteed instant; local uncommitted work is invisible to GitHub; ChatGPT cannot autonomously repair future code between conversations.

Existing PMX/Blender stage acceptance and human review rules remain unchanged.
