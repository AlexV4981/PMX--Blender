# Qwen Local Helper — optional PMX → Blender maintenance worker

## Branch precedence: stage-specialist construction (Qwen-Local-Helper only)

For stages **03 geometry, 04 rig, 05 animation ready, 06 animation tests**, use `qwen-helper/training-workbench/README.md` and `stage_worker.py`: after independent specialist qualification, Qwen can propose the **main stage implementation** in a private `data/candidates/` derivative, not just diagnostics. Codex verifies input and executes only in a safe disposable Blender environment with observed Sol Light review, then takes the original stage human gate. On any failure, unsupported model, unknowns or unqualified task, use original Sol High/Light/Astra execution. **Stage 00 is always Codex-only**, not eligible for any Qwen worker. Stages 01/02/07 remain Codex-led (optional tiny Qwen diagnostic helpers); 08/09 remain Codex-only. This stage scope supersedes older text below restricting all Qwen work to menial reports, without changing historical accepted artifacts, source files, gates or Cycles.


This is a **general helper for this PMX→native Blender project**, not a universal Python/JS/Rust/Go assistant. Its generic defaults are intended for a broad variety of PMX characters. Users customize **each character model** through that conversion run's `character-profile.json`, reference evidence and accepted recipe. They should not rewrite the shared pipeline for individual characters.

**Read [the PMX default/exception policy](POLICY_PMX.md).** The default existing eleven-skill workflow still owns import, materials, geometry, rigs, rendering, physics, reviews and delivery. Qwen only fixes isolated coding mistakes (including incorrect `0` values), writes small tools, tests and diagnostics. Codex handles everything complicated.

## Let Codex set up the helper

Open Codex in a checkout of `Qwen-Local-Helper` and ask:

> Set up the Qwen Local Helper for this PMX→Blender project. Use its PMX-specific configuration and tests, verify Ollama and the coding model, install the project-local Codex skill, and preserve all generic conversion behavior and human gates. Let me specify different PMX character requirements through each run's character profile.

The setup already has a conservative allowlist and two project checks:

```sh
python qwen-helper/setup.py
python qwen-helper/setup.py --doctor
ollama pull qwen2.5-coder:7b-instruct-q4_K_M
```

The setup does not install Ollama or download the model automatically. It does not change global Codex settings. The skill is copied into `.agents/skills/qwen-local-helper/SKILL.md` without overwriting an existing one.

The local Ollama model tag, context and limits can be intentionally changed in `qwen-helper/project.json`; the converted **PMX character model** is controlled separately by the run's `character-profile.json`. Do not confuse these two kinds of models.

## Two kinds of programming tasks

| Task scope | Example | Effect |
| --- | --- | --- |
| `generic` (default) | Repair an isolated summary function returning zero; create a read-only inventory report | Keep working for all PMX characters |
| `character_specific` (explicit opt-in) | A tiny accessory-report adapter for a particular character's observed naming convention | Separate `qwen_character_*.py` tool; never modify generic defaults |

Start with [generic task example](task.example.json). Only create a [character-specific task](task.character.example.json) after consulting a real run's profile. A character-specific script remains an optional external construction aid, not a required part of the final native Blender delivery.

```sh
python qwen-helper/local_worker.py propose --task /path/to/task.json
# Codex/human reviews the full proposal before any execution.
python qwen-helper/local_worker.py apply --task /path/to/task.json --proposal qwen-helper/outbox/TASK_ID.json --reviewed
```

Use a disposable Git worktree, inspect the generated code, and run a task-specific regression test beyond existing unit tests. The worker automatically restores the original code if configured checks fail. No merges or approvals are automatic.

## Confidence boundaries and 10% alert

The project deliberately limits tasks to one small Python file, at most one reference and 4K prompt context. These restrictions are conservative policy choices; official Qwen coding benchmarks **do not establish a reliable 90% success ceiling** on this PMX codebase. Do not treat "majority of cases" as an observed success statistic.

For each actually reviewed Qwen submission, record the outcome in `reviews.jsonl`. Check with `python qwen-helper/review.py --fail-over-threshold`. A correction/rejection rate **strictly greater than 10%** stops new proposals and requires Codex to alert the user during active work. The GitHub workflow can open an issue only after a review log is pushed; it cannot see unpublished laptop work. Zero reviewed submissions means unmeasured performance.

The main pipeline, immutable approvals, versioned recipes, shader/rig/physics decisions and Cycles-only checks remain with Codex and the human reviewer.
