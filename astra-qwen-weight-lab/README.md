# Qwen2.5-Coder-7B-Instruct — active PMX specialist pilot

**ACTIVE** on `Qwen-Local-Helper`. The earlier Qwen3.5-0.8B implementation and three measured failures are preserved at [archive/qwen3.5-0.8b](archive/qwen3.5-0.8b/README.md) for retrospective review. **Do not run the archived tools in production.**

## Fixed model and pipeline

Use the already-configured local Ollama tag `qwen2.5-coder:7b-instruct-q4_K_M` (Q4_K_M). Verify it exists and pin its actual digest; **do not silently pull or replace it**. Stage 00 is ALWAYS Codex. Stages 01/02/07/08/09 remain original Codex. Stages 03,04,05,06 may eventually use qualified specialist Qwen candidates, always with deterministic Blender validation, real Sol Light review, Codex/Astra fallback and original human gates. **None is qualified yet**.

Stage 04 is **left-arm pilot ONLY**, with pole placement unresolved. Do not ask Qwen to construct pole targets or claim a finished IK/FK rig until Codex resolves the mathematical cause.

## One-prompt setup

Paste [CODEX_INSTALL_PROMPT.md](CODEX_INSTALL_PROMPT.md) into Codex. It coordinates existing-model discovery, 80 synthetic fixtures, four docs-grounded Modelfiles, A/B evaluations, real Blender oracles, and a measured recommendation. It does not authorize a model download, run training on the 6 GB laptop, or bypass the stage gate.

## Pilot sequence

1. `python astra-qwen-weight-lab/fixtures.py generate` — **20 generated synthetic cases per stage, 80 total** with deterministic fixture parameters/oracles. This is a synthetic *PoC*, not 80 diverse real characters. Never treat it as the 300-case production holdout. Generated files go under gitignored `astra-qwen-weight-lab/data/`.
2. `python astra-qwen-weight-lab/modelfiles.py` — produce **four Modelfiles** with authoritative contents of each stage's `references/stage.md`. `--create` explicitly adds Ollama specialist tags only after the base tag is installed. No downloaded weights.
3. `python astra-qwen-weight-lab/pilot.py run --cases astra-qwen-weight-lab/data/fixtures/cases.jsonl --models qwen2.5-coder:7b-instruct-q4_K_M,pmx-geometry-7b:pilot --stage 03 --out astra-qwen-weight-lab/data/responses/ab03.jsonl` — use matching base and stage tag, not a 0.8B candidate. One local inference at a time.
4. Pilot runs **greedy legacy** (temperature 0 / 4K context / 1536 outputs) and **sampled 7B** (temperature 0.6 / 8K context / 4096 outputs). It attempts thinking on/off only where the running Ollama/backend explicitly accepts it; unsupported think mode is **reported unsupported**, not a model failure. Qwen2.5-Coder-Instruct is not a native reasoning-model family.
5. Codex independently executes selected generated scripts in a **disposable, network-disabled, resource-limited Blender container** (not the desktop). Use `blender_oracle.py` as the fixture builder and deterministic verifier inside that container. Validate source and candidate hashes. A syntax pass alone is not a Blender pass.
6. Score observed first-try pass, need for Astra repair, severe regression, runtime and costs. **Pre-register go/no-go:** ≥75% first-try verified pass on the 20-case-per-stage pilot, zero severe regressions, and local+review work ≤35% of normal Codex work; otherwise do not proceed to LoRA. These are exploration gates, not production certification.
7. Keep **one Qwen attempt and zero retries in production**. Optional **offline feedback retry** can be benchmarked only with actual failed Blender evidence and separately labeled second attempt; never use that number as first-try success or change production policy without explicit user agreement.
8. Generate **training data before GPU rental**. Use only independently verified, licensed, source-family-separated examples. Minimum 300 untouched held-out **per specialist** and zero observed failures for production qualification; a proof-of-concept never sets `qualified=true`.
9. If prompt specialization fails due to narrow repeatable errors, use a compatible Qwen2.5-Coder-7B full-weight checkpoint for LoRA on an optional **≥24 GB training GPU**, merge, quantize back to Q4_K_M, create exact Ollama tag and pin digest. The 6 GB target only runs one inference model at a time; do not run Blender and Qwen together there.
10. **Weight editing only if repeated, reproducible reasoning loops appear**; not as a generic fix for invalid Blender API or low competence. The old experimental patcher is archived.

## Prevent false qualification

- The 20 cases in each stage are seeded parametric variants. Validate on additional independently authored families before treating numbers as representative.
- Real Blender execution is required for an observed pass; Codex/Sol Light/human review are separate stages.
- If Stage 04 pole placement is unresolved, report blocked and use Codex fallback rather than promoting a fake rig.
- Existing `qwen-helper/` baseline and master skills remain independent and usable.
- This entire experiment is designed to be removed without affecting the originals.
