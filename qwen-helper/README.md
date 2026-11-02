# Qwen Local Helper — portable Codex-managed coding worker

Copy the whole `qwen-helper/` directory into a project root. **Do not copy `project.json` unchanged**: this branch's example is PMX-specific.

Tell Codex: **Set up qwen-helper for this repository. Inspect the code and real tests, configure a narrow source allowlist, install its project-local Codex skill, check my Ollama model, and retain my existing Codex settings.**

Codex can run (with real values):

```sh
python qwen-helper/setup.py --project . --allow src --check 'python -m pytest -q' --github-alert
python qwen-helper/setup.py --doctor
```

Setup can detect Python, JavaScript, Rust, and Go tests; requires at least one real check, preserves existing config by default, and installs `.agents/skills/qwen-local-helper/SKILL.md`. Use `--force-config` only after inspecting an existing config. `--github-alert` is optional; it installs the workflow template without overwriting an existing workflow. Install Ollama separately, then run `ollama pull qwen2.5-coder:7b-instruct-q4_K_M`.

## Delegate and verify

Write a real JSON task based on `task.example.json` with objective, target, expected behavior, and reproducible bug evidence. Run in an isolated disposable git worktree:

```sh
python qwen-helper/local_worker.py propose --task /path/to/task.json
# Inspect all generated source first.
python qwen-helper/local_worker.py apply --task /path/to/task.json --proposal qwen-helper/outbox/TASK_ID.json --reviewed
```

Proposals are not executed on generation. Applying requires `--reviewed`, checks the original digest and a clean target, uses allowlisted directories, and runs configured test commands without shell expansion. Failing generic checks roll back the file. Passing them does not prove the bug was fixed: Codex must run a task-specific regression test and repair any errors itself. Nothing is merged or approved automatically.

Only small isolated bugs, logging, tests and new local diagnostic tools qualify. Multi-subsystem bugs, security-critical changes, shaders, Blender rig/physics design, approvals, and large-context code are sent to Codex. Limits are configurable in `project.json`; default 5.5 KB per source file, one reference, 9.2K prompt characters, and 6.5 KB output. They are conservative operating heuristics, not established 90% benchmark capability.

Qwen's [official coder release](https://qwenlm.github.io/blog/qwen2.5-coder/) and [model-family report](https://qwenlm.github.io/blog/qwen2.5-coder-family/) support trialing bounded coding tasks but do not guarantee high accuracy on arbitrary repositories. The often-cited Aider 73.7 score is for **32B**, not the 7B local model.

## Correction-rate alert

Record one independently reviewed submission per line in `reviews.jsonl`. Required fields: task_id, status (`passed_first_try`, `reviewer_repaired`, `rejected_unresolved`), model, commit SHA, verification, reviewed_at, and repair_notes for failures. Run:

```sh
python qwen-helper/review.py --fail-over-threshold
```

Correction rate = (reviewer_repaired + rejected_unresolved) / all reviewed Qwen submissions. **Strictly over 10% means stop Qwen delegation and tell the user immediately.** Empty review history means unmeasured, not 0% demonstrated. With optional GitHub workflow enabled, a pushed ledger can create a GitHub issue, but local unpushed changes are invisible and delivery is not instantaneous.

PMX's tracked `project.json` excludes its main conversion tools and uses its existing tests. Preserve that branch's human review gates and stages.
