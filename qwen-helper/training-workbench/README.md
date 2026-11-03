# Training workbench: local Qwen for the MAIN work in stages 03–06

**Use `Qwen-Local-Helper` only. Stage 00 ALWAYS uses the original Codex pipeline.** This folder is a separate training area. You already have an Ollama model: the installer discovers and reuses it, with no model download or automatic replacement.

## The actual pipeline in order

```text
00 Setup / references                  → Codex ONLY → human gate
01 Import / losses                     → Codex (Qwen reports optional) → human gate
02 Materials / Cycles restoration      → Codex (Qwen reports optional) → human gate
03 Geometry / morph / weights          → qualified Qwen geometry_builder main work → Sol Light checks → Codex fallback → human gate
04 Native controls / rig               → qualified Qwen rig_builder main work → Sol Light checks → Codex fallback → human gate
05 Animation-ready controls            → qualified Qwen animator_builder main work → Sol Light checks → Codex fallback → human gate
06 Animation / deformation tests       → qualified Qwen animation_qualifier main work → Sol Light checks → Codex fallback → human gate
07 Final Cycles look                   → Codex (Qwen reports optional) → human gate
08 Editable secondary physics          → Codex → human gate
09 Audit and delivery                  → Codex → audit decision → re-audit → delivery decision
```

**Important:** The stage 03 geometry repair and 04/05 build scripts are *real Blender implementation work*, not just reports. Stage 06 generates/runs tests, never repairs the accepted rig. Qwen gets **one proposal**, not unlimited retries. Its Python script operates only on a disposable candidate under a trusted sandbox and is never accepted automatically. Sol Light and existing stage-specific checks plus the explicit human gate are still mandatory. A failed/unqualified/unknown task routes directly to original Sol High/Light/Astra without further Qwen attempts. Stage 00 is hard blocked from the local path.

## Single-prompt agent install

Copy [INSTALL_PROMPT.md](INSTALL_PROMPT.md) into Codex from a checkout of this branch. The prompt makes the agent inspect this README, verify the branch, discover your existing Ollama model, run `python qwen-helper/training-workbench/install.py`, create the ignored data workspace, run tests, and report the first training task. No other installation command should be necessary when Ollama, Python and Blender are already installed.

The direct (agent-independent) command is:

```sh
python qwen-helper/training-workbench/install.py
```

If multiple Qwen coding tags are installed and no existing project-model match resolves them, supply `--model YOUR_EXISTING_OLLAMA_TAG`. It never silently pulls a new model, assumes that Ollama GGUF weights are fine-tunable, changes global Codex settings, or writes to main.

## Train and qualify each stage specialist

```sh
python qwen-helper/training-workbench/workbench.py map
python qwen-helper/training-workbench/workbench.py status
python qwen-helper/training-workbench/workbench.py prepare --track geometry_builder
python qwen-helper/training-workbench/workbench.py train --track geometry_builder
```

Dataset examples are actual verified scripts/recipes for **one narrowly defined operation** inside each stage, not broad "do any geometry" prompts. Put permissioned data under ignored `data/raw/geometry_builder.jsonl`, `rig_builder.jsonl`, `animator_builder.jsonl`, `animation_qualifier.jsonl`. Each record needs `case_id`, `group_id`, `prompt`, `completion`, `source_type`, `provenance`, `verification`, and `verified_by`. Split by PMX source family; unseen holdout must stay untouched. Review the example template. Data, weights and logs stay untracked.

The existing QLoRA training script needs a compatible **full precision/4-bit-loadable base**, not simply an installed quantized Ollama model. Agent must verify matching weights/license or use prompt-specialized Qwen initially, then add a compatible HF base intentionally via `--base-model`. Do not fabricate training examples or silently train on Codex/Sol output. Training is optional for first baseline evaluation, but a specialist cannot be enabled without independent qualification.

Production qualification requires ≥300 independent, held-out, observed cases **with zero recorded failures**, actual Sol Light review and true test evidence, plus an exact Ollama model digest. The 10% production error threshold remains. Nobody should interpret 300 clean cases as a universal perfection guarantee.

## Execute candidate work (after qualification)

1. Codex finishes preceding stage, records accepted input identity and approved repair/mapping constraints. The agent writes a task using [stage-task.example.json](stage-task.example.json), with stage 03–06 and the matching specialist.
2. Run `python qwen-helper/training-workbench/stage_worker.py plan --task /path/to/task.json`. Unqualified stage → immediate original Codex path. To **pilot without qualification**, use `demo` with `fixture_only=true` and synthetic data: this produces an inert candidate only, never enters production.
3. Run `python qwen-helper/training-workbench/stage_worker.py propose --task /path/to/task.json` for a qualified specialist. It calls the selected local Ollama model **once**, stores an inert Blender Python script proposal, and emits the standard `done.py` completion signal.
4. Trusted Codex watcher reviews the proposal; executes it **only in a separate, sandboxed Blender process with no credentials/network, on a copied/approved input**. Never execute generated arbitrary Python directly on the desktop. Record actual source hash, candidate hash, exact stage-required checks and Sol Light decision. The script cannot approve a stage.
5. `stage_worker.py finalize --task ... --review ... --validation ...` checks records and returns candidate-for-human-review only; rejected/missing evidence → original Codex fallback. Actual required check quality is an independent Codex responsibility, not proven by self-attested JSON.
6. Original pipeline presents at most three user-facing candidates and waits for an observed human decision at the *existing* gate, preserving Cycles-only rendered evidence, fidelity-first priority, frozen checkpoint identity and historical approvals.

For the job-done signal, the existing trusted completion watcher uses `qwen-helper/done.py --watch`; Qwen itself does not need to know anything except that it has finished.

## Exact skill ownership

- 03: `skills/anime-blender-03-geometry/references/stage.md` — geometry-change-comparisons, morph-integrity, deformation-tests, correspondence-map.
- 04: `skills/anime-blender-04-rig/references/stage.md` — control-capabilities, rig-integrity, switching-demonstrations, runtime-dependencies.
- 05: `skills/anime-blender-05-ready/references/stage.md` — face-and-visemes, animation-usability, retarget-profiles, animator-guide.
- 06: `skills/anime-blender-06-tests/references/stage.md` — motion-fixtures, deformation-review, integrity-lint, clean-core-rig.

No unverified stage scripts can change the main pipeline or approved state. Stage 03 may submit a no-change report when there is no actual fault; Stage 04 uses one arm/leg pilot first; Stage 05 tests neutral/isolated/combined controls; Stage 06 tests physics-off and clean stock Blender.

[AGENTS.md](AGENTS.md) contains instructions for a future agent. [tracks.json](tracks.json) is the machine-readable map.
