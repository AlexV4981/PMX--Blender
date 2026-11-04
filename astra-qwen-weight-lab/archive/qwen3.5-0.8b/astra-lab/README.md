# Astra × Qwen Weight Lab (isolated experiment)

**Separate from every existing Qwen helper.** This entire experiment is confined to this top-level folder on `Qwen-Local-Helper`. The existing `qwen-helper/`, `qwen-helper/training-workbench/`, original master skill, original checkpoints, and `main` are NOT edited, configured, or overwritten by this lab.

## What this experiment tests

MIT CSAIL's November 2, 2026 weight-space programming experiment modified a tiny fraction of Qwen3.5-0.8B's weights to repair a looping defect. This is evidence that a bounded weight patch can correct some deficiencies, **not** evidence that it can imbue a 0.8B model with arbitrary Blender skills. The edited checkpoint is a candidate baseline, not automatically best.

- Base reference: https://huggingface.co/Qwen/Qwen3.5-0.8B
- Published edited baseline: https://huggingface.co/RikiyaT/Qwen3.5-0.8B-weight-space-programming
- Research: https://rikiyat.github.io/blog/weight-space-programming/

Goal: **one source-weight family with four separately evaluated variants**, targeting stages **03 geometry, 04 rig, 05 animator controls, 06 motion testing**. Keep untouched reference weights and make independent scratch patches or adapters for each specialty. Stage **00 always Codex**; other stages retain original ownership.

## Single-prompt setup

Copy [`CODEX_INSTALL_PROMPT.md`](CODEX_INSTALL_PROMPT.md) into a Codex session opened in the `Qwen-Local-Helper` checkout. It instructs Codex to install only what is needed, discover your installed Ollama model, keep the legacy helpers untouched, run tests and create the first read-only inference comparison. The script here never automatically downloads model weights or imports edited weights.

Manual equivalent from the checkout root:

```bash
python astra-qwen-weight-lab/lab.py doctor
python astra-qwen-weight-lab/lab.py init
python -m unittest discover -s astra-qwen-weight-lab/tests -v
python astra-qwen-weight-lab/lab.py pilot --models YOUR_INSTALLED_TAG --stage 06 --out astra-qwen-weight-lab/data/responses/stage06_baseline.jsonl
```

**Pilot is deliberately inert:** it asks existing Ollama tags for code, saves the untrusted response under ignored `data/`, and checks only JSON/Python syntax. It never executes output or modifies Blender scenes. Codex must independently run candidate scripts inside a disposable network-blocked Blender sandbox, then provide verifiable outcomes.

## Research sequence

1. Pin exact source repository revision and original SHA-256 hashes. Prefer your already-installed Ollama model for first inference testing; original Qwen3.5-0.8B and MIT-edited checkpoint are OPTIONAL comparisons requiring explicit model acquisition.
2. Build 20 genuinely distinct, verified synthetic/permissioned stage tasks **per specialty** (80 minimum) with separate source families. The supplied four cases are **examples, not evidence**.
3. Compare original Qwen, MIT-edited Qwen, your existing coder, and optionally small prompt variants at matched decoding settings. Measure actual Blender pass/fail after isolated execution, along with runtime and reviewer cost.
4. Have Astra inspect recurring *classes of failure*, test one bounded hypothesis and propose a patch specification plus separately stored numeric delta(s). Apply changes only to a fresh local copy of HF `safetensors` with `weight_patch.py`, never to installed Ollama weights or the shared source.
5. Compare untouched base, MIT edit, targeted weight patch, and (if useful) independently trained LoRA adapter on never-seen cases. Reject if benchmark doesn't improve, even if a general benchmark improves. Every failure still routes to original Codex/Astra work, not additional local loops.
6. Only after substantial holdout evidence (current policy: ≥300 independent evaluated cases and zero recorded failures **per specialty**, Sol Light review, immutable artifact digest) consider integration into the main pipeline. Do not assume a measured pass-rate guarantees perfection or bypass human gates.

## Fallback and cost calculation

Qwen attempts its bounded work once → deterministic validation → *actual* Sol Light review if available → if fail/uncertain, Codex/Astra repairs through the original pipeline → original human gate. Don't use Astra to rewrite weights for every failed candidate. Only offline recurring defects justify testing a new weight patch.

If a normal Codex task costs **C**, local attempt plus checking costs **R**, and fallback costs **F**, expected work is `R + (1-p)*F` for first-pass success probability **p**. Test whether that is less than **C**, measuring both runtime and usage. The lab's `score.py` records observed task pass rates, not guessed probabilities.

## Boundaries

- All weight files/deltas/adapters/benchmark outputs are ignored under `astra-qwen-weight-lab/data/`; never commit checkpoints, proprietary PMX models, credentials, private paths or raw user sources.
- Weight editing is experimental and supports local HF `safetensors`, not GGUF/Ollama blobs. Original checkpoint must be separately backed up and verified, untouched.
- The edit tool does **not** autonomously discover improved patches; Astra must supply an independently reasoned, reviewed, testable delta. A numeric delta can make a model worse. Test rigorously.
- Stage 00 is Codex-only; never claim model-generated code is safe because AST parsing passed. Never execute code without separate sandbox validation.
- Do not touch Bobcat-fitness or any other repo. This experiment never modifies the existing Qwen helper work.
