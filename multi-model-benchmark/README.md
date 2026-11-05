# Multi-model benchmark runner

Run **one explicitly selected model** at a time on `Multi-Model-PMX-Benchmark`. See [workflow](../MULTI_MODEL_WORKFLOW.md), [seven-section report standard](../MODEL_REPORT_STANDARD.md), [premade motion catalog](../PREMADE_ANIMATION_PACKS.md), and [motion asset manifest](animation-assets/manifest.json).

## Preparation

1. Install Ollama and the chosen model **manually**; confirm the exact installed tag and Q4_K_M (or explicitly document a different quantization). No script downloads models.
2. Generate the existing 80 synthetic fixtures with `python astra-qwen-weight-lab/fixtures.py generate` (verify the legacy fixture generator accepts the new branch; if branch-guarded, use its documented output from a separate sandbox and copy the fixture JSONL into the ignored data folder). Never rewrite archived evidence.
3. `python multi-model-benchmark/runner.py inspect --model qwen3.5:9b` records the locally installed digest.
4. `python multi-model-benchmark/runner.py run --model qwen3.5:9b --stage 03 --cases astra-qwen-weight-lab/data/fixtures/cases.jsonl --out multi-model-benchmark/data/qwen35-03-lap00.jsonl`
5. Optional stage-document prompting: rerun with `--specialized` and a **different new output file**. It does not train or change model weights.
6. Have Codex independently execute candidate scripts in a disposable, network-disabled Blender container, with original `blender_oracle.py` fixtures and deterministic checks. **The runner does not do this**. Record results in the [report standard](../MODEL_REPORT_STANDARD.md). Stage 06 must never repair accepted rig.
7. Only after the initial pilot and actual reviewed failure evidence, consider LoRA separately. Do not claim a stage passes merely because Ollama returned valid JSON.

`python -m unittest discover -s multi-model-benchmark/tests -v` runs static runner safety checks, not a Blender or model quality benchmark.

## Animation assets

Premade motion download sources and license notes are in [PREMADE_ANIMATION_PACKS.md](../PREMADE_ANIMATION_PACKS.md). The manifest contains source links and **not_downloaded** states. The binary VMD/BVH/FBX/GLB assets are **not yet bundled**; use separate PMX and Blender directories under ignored `data/animation-assets/` and retain hashes/provenance. Do not count a missing asset as a passed test.
