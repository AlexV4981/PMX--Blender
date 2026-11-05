# Multi-model PMX → Blender experiment workflow

**Active branch:** `Multi-Model-PMX-Benchmark`. **Frozen archive:** `archive/Qwen-Local-Helper-2026-11-05` at commit `e1cd60736b4aa8fe2021bd6c7211105f5ece8712`. This is a non-destructive fork; the Qwen-only scripts and all historic results remain unchanged. Do not run old `astra-qwen-weight-lab/pilot.py` on this branch: it intentionally rejects non-Qwen branches and is pinned to Qwen2.5-Coder 7B. The new runner below is independent.

## Explicit stage ownership and invocation

| Stage | Owner | When to invoke local <model> | Required handoff |
|---|---|---|---|
| 00 Setup | Codex ONLY | NEVER | Accepted source inventory |
| 01 PMX import | Codex | NEVER | Approved imported checkpoint |
| 02 Cycles materials | Codex | NEVER | Approved material checkpoint |
| 03 Geometry | Codex by default; experimental <model> only after an explicit **stage-03 experimental proposal** request | On approved **disposable** source copy, and only after model is selected and fixture pilot authorized | One inert bpy proposal → independent Blender oracle → Sol Light review → human gate; fallback Codex |
| 04 Rig | Codex by default; experimental <model> only for **left-arm pilot** | Only when Stage 03 accepted, left-arm task and source rest/space data supplied, pole issue explicitly excluded | Same checks; no pole construction/rig completion claims |
| 05 Animation-ready | Codex by default; experimental <model> after approved rig checkpoint | On explicit character-specific face/control task with source morph mapping | Candidate → tests → independent review → human gate |
| 06 Motion qualification | Codex owns final gate; <model> may propose **test harness only** | On explicit Stage 06 test-writing task with pinned fixture/motion manifest | Execute tests independently, never let model self-score or repair accepted rig |
| 07 Cycles look | Codex | NEVER | Original look review |
| 08 Physics | Codex | NEVER | Original physics review |
| 09 Audit/delivery | Codex | NEVER | Original audit, human delivery |

**Experiment state machine:** `NOT_SELECTED → SELECTED → MODEL_PINNED → FIXTURES_PINNED → BASELINE_INFERENCE → EXTERNAL_BLENDER_ORACLE → REVIEWED → PROMPT_SPECIALIZATION → EXTERNAL_ORACLE → (OPTIONAL TRAINING) → HOLDOUT → HUMAN_GATE`. Any failed/unsupported step stops and records evidence; no implicit promotion. Stage 04 stays left-arm only. Models have **one proposal per production task, no automatic retry**; optional feedback retry is labeled research only.

## Models (one at a time, no automatic download)

Use exact **installed** Ollama tags and digests; aliases are not guaranteed to exist on every Ollama version. Primary current user baseline: `qwen3.5:9b` Q4_K_M **verify tag and quantization locally**. Challengers to check individually: Gemma 4 12B, Ministral 3 8B, Granite 4.2 8B, Phi-4 14B, Nemotron 3 Nano 4B. The registry contains suggestions, not claims that these are installed or qualified. If a tag does not exist, record it as unavailable; do not silently substitute a different size or quantization. Do not run Blender concurrently with inference on the 6 GB GPU / 16 GB RAM laptop.

**Order:** Qwen3.5 9B first, then Ministral 3 8B, Granite 4.2 8B, Gemma 4 12B, Phi-4 14B, Nemotron 3 Nano 4B. Selection is sequential, **not a cross-model report**. Each model gets its own report per stage. Do not fine-tune all six: prompt-specialize first; only consider compatible source-checkpoint LoRA after a demonstrated narrow, reproducible failure, verified license and sufficient training VRAM.

## Benchmarks — measurable gates, not inferred passes

1. **Synthetic pilot:** 20 versioned parametric cases per Stage 03/04/05/06 (80 total) using the existing `astra-qwen-weight-lab/fixtures.py` fixture generator and `blender_oracle.py`. Existing 80-case set is a smoke test, **not** independent real-model coverage.
2. **Baseline vs prompt-specialized:** identical frozen fixtures, context constraints, decoding profiles and Blender versions; report thinking enabled/disabled separately where supported. Every response gets model digest, prompt hash, fixture hash, raw JSON, syntax diagnostics and wall time.
3. **Actual Blender execution:** proposals are **never run by the inference runner**. Codex executes in a disposable, network-disabled, resource-limited Blender environment; record per-case pass/fail and errors. No pass without observed oracle execution. Static syntax alone is not a pass.
4. **Real model and animation:** run at least one independent PMX/VMD baseline and one native Blender action/BVH/FBX baseline, using a pinned rights-cleared source manifest. Evaluate joint coverage, sampled keyed and interpolated frames, retarget maps, IK/FK switch continuity, geometry/penetration warnings, foot contact, face, physics-off baseline and Cycles human views. Unknown and unlicensed assets are NOT passes.
5. **Exploratory per-stage gate:** >=75% observed first-try Blender passes on 20 synthetic fixtures, **zero** severe regressions, and <=35% local+review effort vs Codex original. Do not infer cost gate without a real Codex measurement. Preserve >10% repair/rejection escalation rule.
6. **Production:** >=300 *independent* held-out examples **per specialist**, zero observed failures, Sol Light independent review and explicit human gate. This does not guarantee zero future failures. Stage 04 remains blocked outside left-arm scope until pole solution approved.
7. **Every lap:** capture failures, root cause vs hypothesis, exact changes/why, before-after results, and real-world quality, in [MODEL_REPORT_STANDARD.md](MODEL_REPORT_STANDARD.md). No cross-family comparison in an individual report.

## Command sequence (inert proposal collection only)

```bash
git switch Multi-Model-PMX-Benchmark
python astra-qwen-weight-lab/fixtures.py generate
python multi-model-benchmark/runner.py list
python multi-model-benchmark/runner.py inspect --model qwen3.5:9b
python multi-model-benchmark/runner.py run --model qwen3.5:9b --stage 03 --cases astra-qwen-weight-lab/data/fixtures/cases.jsonl --out multi-model-benchmark/data/qwen35-stage03-lap00.jsonl
python -m unittest discover -s multi-model-benchmark/tests -v
```

The runner **only queries localhost Ollama and writes ignored JSONL proposals**. It does not execute `bpy`, Blender, model-authored code, or external downloads. `inspect` prints exact local digest/metadata. Outputs never overwrite. The model is never automatically launched for a stage; the operator must supply explicit `--model` and `--stage`. External Blender oracle execution and review remain separate.

## Premade animation retention

- [PREMADE_ANIMATION_PACKS.md](PREMADE_ANIMATION_PACKS.md) lists real VMD/FBX/GLB/BVH download sources.
- [multi-model-benchmark/animation-assets/manifest.json](multi-model-benchmark/animation-assets/manifest.json) pins **asset slots** and formats, with `status: not_downloaded`. This is not a false claim of included files.
- Keep licensed motion **source files and PMX/Blender derivatives** in `multi-model-benchmark/data/animation-assets/{pmx-vmd,blender-native}/` locally (gitignored), or in a separately approved licensed asset repository/storage with hashes and provenance. No random mirrors or unlicensed files.
- For each asset log URL, creator, license, explicit permission for AI testing, SHA256, filename, rig profile, FPS, original vs retargeted format, frame ranges and evaluation results. Do not distribute a third-party binary unless license allows it.
- The original PMX/VMD and the Blender-retargeted action must remain **separate** and intact. Do not convert in place or delete originals.
- Quaternius/KinemIQ CC0 downloads are best first Blender candidates; CMU/ACCAD require attribution/provenance checks; the MMD Guide VMD pack is **not authorized for AI model evaluation until rights are verified**. The CC0 eye/breath VMD is a PMX-side starter. Mixamo is excluded from AI model testing/training under Adobe terms.

## Migration boundaries

Do **not** rewrite old Qwen specialist registration, archive results, or modify main. The old scripts are historical references and may reject the new branch by design. New experiment files live under `multi-model-benchmark/`. Preserve original stage gate report separately from individual-model report. No qualified production model exists just because its Ollama tag is installed.
