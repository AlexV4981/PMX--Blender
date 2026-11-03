---
name: qwen-local-helper
description: Configure and supervise local Qwen for small PMX-to-Blender Python maintenance tasks; keep general character conversion behavior as default and model-specific overrides opt-in.
---

# Codex: Qwen Local Helper for PMX → native Blender

This assistant is **only for the PMX-to-Blender project**. "Model-specific" means the user's **PMX character model**, not changing the LLM itself. Read `qwen-helper/POLICY_PMX.md`, `skills/anime-blender-pipeline/SKILL.md`, and the pipeline's `references/roles.md` before dispatch. Do not replace the stages, generic model-agnostic behavior, Cycles-only requirements, candidate cap, or human gates.

1. **Setup**: From this repository root, run `python qwen-helper/setup.py` to install the project-local `.agents/skills/qwen-local-helper/SKILL.md`. The PMX-specific allowlist, protected paths and checks are already in `qwen-helper/project.json`. Setup rejects unrelated repositories and preserves existing configuration unless explicitly forced. Verify them, then run `python qwen-helper/setup.py --doctor`. Only install Ollama and pull the configured coding model with permission; never overwrite existing user settings.
2. **Default pathway**: Follow the generic PMX workflow with read-only/deterministic tools. Dispatch a local Qwen job only when Codex encounters a bounded programming chore with a known expected result (e.g. wrong zero return, a small reporting function, test or diagnostic).
3. **Keep character exceptions separate**: For each PMX model, use the conversion run's `character-profile.json` and recipe. Never write one character's constants into the generic tools. If genuinely necessary, supply a distinct `scope: character_specific` task using `task.character.example.json` and verified requirements from that profile. Only a new standalone `qwen_character_*.py` helper is eligible. The normal task template has `scope: generic`. Escalate non-programming character design to Codex.
4. **Delegate**: Prepare exact task, reproducer for bugs, expected behavior, permitted one-file target, and tests. Run `python qwen-helper/local_worker.py propose --task TASK.json` in a clean disposable worktree with local Ollama. The proposal is *not executed*. Inspect full code; do not trust generated content.
5. **Validate**: After reviewing, use `python qwen-helper/local_worker.py apply --task TASK.json --proposal qwen-helper/outbox/ID.json --reviewed`. It rejects dirty/stale targets, runs configured checks and reverts on failure. Then run a task-specific regression. Generic tests passing alone does not prove a bug fixed; character adapters require the actual character fixture.
6. **Codex repairs**: If Qwen's result errors or misses expected behavior, Codex repairs the patch, runs tests and writes an accurate review in `qwen-helper/reviews.jsonl`; count it as `reviewer_repaired`. Unresolved proposals count as `rejected_unresolved`. Record real commands and evidence, never invented outcomes.
7. **Hard stop**: `python qwen-helper/review.py --fail-over-threshold`. Above 10% repaired/rejected among reviewed Qwen submissions, **tell the user immediately during active work and stop assigning Qwen tasks**. The proposer enforces this from the committed/local ledger. GitHub issue notification requires reviews to be pushed; it is not a real-time watcher.
8. Preserve preexisting work, human approvals, frozen runs and source models. Qwen is not allowed to finalize or sign off conversion stages. Never claim Ollama or Blender ran without observed evidence.

## Branch-local specialist offload

For new optimized routing, first read `qwen-helper/SPECIALISTS.md`. Only on branch `Qwen-Local-Helper`, issue `python qwen-helper/dispatch.py plan --task TASK.json`; a qualified specialist gets **one** local attempt followed by deterministic checks and an observed Sol Light review. Otherwise follow this skill's original Codex path without Qwen. No automatic approval, adapter training, model download, or model deployment. The specialist registry ships unqualified. Keep original manual helper functionality for tasks without `specialist` field, but treat it as non-optimized/explicit manual use.
