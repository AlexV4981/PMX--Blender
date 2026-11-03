# Specialist Qwen — Codex-budget-safe offload

## Branch precedence: stage-specialist construction (Qwen-Local-Helper only)

For stages **03 geometry, 04 rig, 05 animation ready, 06 animation tests**, use `qwen-helper/training-workbench/README.md` and `stage_worker.py`: after independent specialist qualification, Qwen can propose the **main stage implementation** in a private `data/candidates/` derivative, not just diagnostics. Codex verifies input and executes only in a safe disposable Blender environment with observed Sol Light review, then takes the original stage human gate. On any failure, unsupported model, unknowns or unqualified task, use original Sol High/Light/Astra execution. **Stage 00 is always Codex-only**, not eligible for any Qwen worker. Stages 01/02/07 remain Codex-led (optional tiny Qwen diagnostic helpers); 08/09 remain Codex-only. This stage scope supersedes older text below restricting all Qwen work to menial reports, without changing historical accepted artifacts, source files, gates or Cycles.


**Branch-only experiment.** This directory adds an **optional** first attempt before the original Sol High / Sol Light / Astra pipeline. Never alter `main`, alter frozen conversions, or bypass human gates. No local specialist is qualified out of the box.

## Agent bootstrap (minimum interaction)

1. Verify branch: `git branch --show-current` must print `Qwen-Local-Helper`. Never perform setup, promotion or repository changes on `main`.
2. Inspect `qwen-helper/POLICY_PMX.md`, `skills/anime-blender-pipeline/SKILL.md`, `skills/anime-blender-pipeline/references/roles.md` and this file. Run `python qwen-helper/setup.py` and `python qwen-helper/setup.py --doctor`. Preserve preexisting local skill/config.
3. Ensure Ollama installed/running on `127.0.0.1:11434`. Pull `ollama pull qwen2.5-coder:1.5b-instruct-q4_K_M` for lightweight smoke tests. It is **not** a qualified specialist. Never download weights or install GPU packages without checking system capacity and permission. No credentials belong in this repository.
4. For training on a CUDA machine create a separate virtual environment and run `python -m pip install -r qwen-helper/requirements-train.txt`, first recording version pins. Model choice: [Qwen2.5-Coder-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct), under Apache-2.0. For this GPU budget, prefer 4-bit QLoRA with one adapter per narrow task. Benchmark VRAM, temperature and time; 6 GB inference does not guarantee 6 GB fine-tuning.
5. Start with synthetic deterministic cases; collect independently verified real PMX examples. Keep *separate* training and unseen holdout JSONL files outside Git, preferably `qwen-helper/data/` (gitignored). Each row: `case_id`, `prompt`, `completion`. Never train on Sol/Codex-generated text where terms prohibit model-development use, and never train on the holdout.
6. Train **one** bounded task at a time: `python qwen-helper/train_specialist.py --specialist inventory_summary --train /private/train.jsonl --output /private/adapters/inventory_summary`. Model saved as PEFT LoRA adapter; no automatically exported Ollama model. For deployment, merge the adapter with the exact original base model then quantize/serve with a verified supported route (e.g. GGUF conversion and `ollama create`). Pin resulting model digest and use the exact tag in `specialists.json`. Avoid loading an incompatible LoRA on an unrelated quantized base.
7. Evaluate on truly unseen examples using an **independent evaluator**, real execution in a disposable sandbox, exact expected outputs, task-specific regressions and separate Sol Light review. One row per holdout `case_id` in the evaluation report: `deterministic_pass` and `sol_light_pass`; both must be observed true. Minimum 300 independent holdouts, **zero failures** as a conservative promotion target; this is not a guarantee of perfection. Do not invent review identities, commands, measurements, or outcomes.
8. `python qwen-helper/qualification.py --specialist inventory_summary --report /private/evaluation.json --output qwen-helper/qualifications/inventory_summary.json` only *validates reported evidence*. Independently audit every underlying result, dataset separation, adapter/model digest, negative tests, and an actual Sol Light invocation; then and only then explicitly change that specialist's `qualified` field from false to true on this branch. If any evidence changes, revoke qualification. Track evaluations separately from the production 10% failure ledger.
9. Before assigning a job, construct a task JSON using `task.specialist.example.json`. `python qwen-helper/dispatch.py plan --task /private/task.json` tells you whether to offload. If it returns `original_codex_pipeline`, do exactly that. If eligible, `python qwen-helper/dispatch.py propose --task /private/task.json` makes **one** Ollama attempt, saves an inert proposal **and automatically emits the completion signal** for the trusted host watcher.
10. Compile and independently test the proposed code. Invoke an **actually available** Sol Light worker once to inspect correctness and fit. Sol Light emits a signed-off *record* (not a cryptographic signature) referencing the SHA-256 of the exact proposal file, role, decision and observed evidence. Use `sol-light-review.example.json`; reject on doubt, unavailability or missing evidence. Only after approval: `python qwen-helper/dispatch.py finalize --task /private/task.json --review /private/sol-review.json`. Any failure -> original pipeline; **never retry local**.
11. Complete the original task-specific tests, recipe, Cycles comparison, qualified stage gates and required human selection. Local success does **not** mean character acceptance. Document actual saved token usage / runtime / fallback counts rather than assuming savings.

## Routing / hard limits

- Approved categories: read-only JSON inventory summaries, read-only texture-link diagnosis, synthetic test-fixture generators. Start with `inventory_summary`; add new specialties only after measured failures show a legitimate need.
- Local specialist jobs create standalone, short `qwen_*.py` files in the allowlisted scripts directory. Existing core PMX tools and the live Blender session are **never** modified by the local model.
- Use deterministic Python tools for straightforward fixed rules; do **not** use an LLM simply to rename objects or count records.
- Character-specific, shader-design, geometry, morph, rig, physics, image-fidelity and stage-acceptance decisions go directly to original Codex.
- One local attempt, zero local retries. Existing test runner rolls back on failure. If Sol Light is unavailable, reject and route directly to original.
- Existing `review.py` ledger stops local delegation when observed repair/rejection rate is **strictly >10%**. It requires honest review entries. Zero entries means unmeasured, **not 100% success**. Keep per-specialist rates and confidence intervals separately; suspend on regression.
- Prefer one base weight set with separate LoRA adapters instead of duplicating full checkpoints. Keep adapter artifacts, raw datasets and models outside Git.

## Important limitations

The `qualification.py` gate checks **report structure and file identity**, not the truth of externally recorded measurements. A claimed result is not actual Sol Light execution or Blender verification. Agents must perform these checks, never fabricate them. A qualified specialist is trusted only for its narrowly defined interface, input distribution and exact model digest. New PMX character sources or changed engine versions require regression checks. Restore the **original pipeline** without Qwen interaction on any exception.

Review `qwen-helper/POLICY_PMX.md` for run-specific overrides and `qwen-helper/CODEX_SKILL.md` for existing worker safety boundaries.

### Runtime identity check

The dispatcher reads Ollama's local `/api/tags` and compares the **exact served model digest** to the independently audited qualification manifest. Any mismatch, unavailable Ollama server, dirty review ledger threshold, or wrong Git branch results in immediate original-Codex routing. Do not mark `qualified=true` solely because an evaluation JSON says it passed. Track separately the model digest, training code commit, frozen data splits and real Blender regression outcomes.

### Completion-only local worker

The local model only returns its result. No instructions about reviewers or fallback are needed inside Qwen's prompt. The trusted dispatch wrapper writes its proposal and calls the notification script. See [HANDOFF.md](HANDOFF.md). The separate host watcher must be started to resume the Codex CLI; this cannot notify or reactivate a ChatGPT app session directly.
