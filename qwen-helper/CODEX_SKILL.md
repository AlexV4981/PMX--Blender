---
name: qwen-local-helper
description: Set up and delegate small, isolated source-code maintenance tasks to local Ollama Qwen, verify the returned patch, repair failures with Codex, and record a strict over-10-percent correction alert.
---

# Codex procedure: Qwen local helper

When the user asks to configure this helper, inspect the repository and environment. The helper must already be copied into the root as qwen-helper/. Do **not** alter Codex global settings or overwrite existing AGENTS.md.

1. Pick the smallest legitimate source directory allowlist and actual project test command(s). Run python qwen-helper/setup.py --project . --allow SOURCE_DIRECTORY --check "PROJECT_TEST_COMMAND" [--github-alert]. Re-run with --force-config only after comparing existing configuration and getting authority for replacement. Run --doctor, ensure Ollama is installed/running and the configured model is pulled. Never install packages without appropriate user approval.
2. Restrict tasks to a reproducible, isolated bug; a small diagnostic utility; test; or logging. Do not delegate secrets, permissions, security-sensitive logic, architecture, shader/rig/physics design, or approval decisions. Official coding benchmarks indicate possible competence, **not** a guaranteed 90% success rate. Task scopes are deliberately conservative.
3. Create a task JSON using qwen-helper/task.example.json. Set objective, expected_behavior, target, and reproducer for bug fixes. Require a task-specific test first when feasible. Do not send entire repositories to local models.
4. In a fresh disposable git worktree, run python qwen-helper/local_worker.py propose --task TASK.json. Inspect the generated outbox JSON and source carefully for unsafe behavior; do not trust LLM-generated code.
5. After explicit review, run python qwen-helper/local_worker.py apply --task TASK.json --proposal qwen-helper/outbox/ID.json --reviewed. The script checks the exact original digest, refuses a dirty target, runs configured checks without a shell, logs outcomes, and rolls back failed changes. Run task-specific repro/acceptance tests too; passing generic tests is insufficient.
6. On failure or incomplete behavior, **Codex** diagnoses, implements the minimal corrective patch itself, repeats tests and documents exactly what changed, with evidence. Stop delegating if the eligibility conditions are no longer met. Preserve existing PMX/Blender gates if using the original source repository.
7. Record **one** reviewed submission in qwen-helper/reviews.jsonl: task_id, model, commit (actual SHA), reviewed_at, verification, status=passed_first_try|reviewer_repaired|rejected_unresolved; include repair_notes for non-passes. Run python qwen-helper/review.py. The numerator includes Codex repairs and unresolved rejections; denominator includes every reviewed submission. If strictly >10%, immediately tell the user in this Codex session and stop delegating new tasks. If --github-alert was enabled, commit and push the review ledger so GitHub Actions can create/update an issue; alerts are not instantaneous from an uncommitted laptop.
8. Do not claim Qwen ran unless an Ollama call actually succeeded. Do not automatically accept, commit, merge or modify user-approved files. Never erase or rewrite historical review records to lower the error rate.
