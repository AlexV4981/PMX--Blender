# MIT weight-space Qwen3.5-0.8B: Stage 03–06 pilot

**Research basis:** [MIT CSAIL, November 2, 2026](https://rikiyat.github.io/blog/weight-space-programming/) and [authors' reproducible weight edit](https://huggingface.co/RikiyaT/Qwen3.5-0.8B-weight-space-programming). The published gain repairs a reasoning-loop defect, NOT general Blender construction ability. Do not use the math score as a coding benchmark. The paper/blog is preliminary.

## Goal

Determine whether **one exact open-weight Qwen3.5-0.8B base** can support **four independently specialized workers**:
Stage 03 geometry, 04 native rig, 05 animator controls, 06 motion qualification.

Astra has *two possible roles*:
1. **Production:** After one Qwen proposal, deterministic tests and an actually available Sol Light review; Astra/Codex repairs a failed candidate using original stage process. No further local attempts.
2. **Research offline:** If many verified failures reveal one reproducible internal model defect (like MIT's reasoning loops), Astra may investigate a copied checkpoint's weights and propose one *auditable* patch. Never directly modify the shared original or all four specialized checkpoints. Benchmark against both baselines on unseen cases. This is experimental, not established transfer learning.

Do **not** have Astra patch weights per failed Blender task. Fix generated work in Codex instead; repeated local misbehavior is separately diagnosed with controlled A/B tests and LoRA fine-tuning.

## Hardware considerations

Official Ollama `qwen3.5:0.8b` is about **1.2–1.3 GB per model download**; official BF16 weights are ~1.7–1.8 GB. Actual VRAM also requires context, temporary buffers and Blender/Cycles. **Do not run 4 independent inference workers or Blender at once on a 6 GB GPU.** Prefer one shared Qwen3.5-0.8B checkpoint plus four separate low-rank adapters; activate only one specialist at a time. If adapter switching for this architecture is unsupported, use four merged and quantized tags loaded sequentially. Record exact upstream revision and MIT edited checkpoint SHA; adapters should be trained against the *same precise base* they will use in production.

The previously committed QLoRA script was designed for Qwen2.5-Coder-1.5B. It is NOT yet verified to support Qwen3.5's hybrid DeltaNet layers. An agent must adapt model loading, PEFT targeting, training format and adapter export before declaring 0.8B training ready. No model auto-downloading in this pilot.

## Controlled A/B sequence

1. Build a test matrix: official original Qwen3.5-0.8B with **thinking off**, MIT edited checkpoint with thinking off and thinking on, plus your currently installed coding model.
2. Use the same synthetic/approved fixture prompts for every model. Stage 03–06 scripts must use approved mappings and private Blender scenes. Cap each prompt at one bounded construction/test operation.
3. Test the inert outputs with `pilot.py` first. It checks JSON formatting, Python syntax and a few obvious static warnings; **it never executes Qwen-generated code**.
4. Codex then runs selected candidate scripts in disposable, network-restricted Blender with explicit acceptance oracles: correspondence/silhouette for 03, rest-space/IK-FK switches for 04, reset/expression combinations for 05, fixture/deformation/clean-open for 06. Check actual Cycles evidence and human gates separately. Preserve source and approved assets.
5. Record for each: first-try verified success, repair needed, severe regression, elapsed time, Sol Light review cost and Astra fallback usage. Only performance on unseen held-out **PMX source families** supports production deployment.
6. If the 0.8B model struggles at a stage, **do not force it into production**. Compare the existing stronger coder model or a 2B/4B option. If a narrow operation is validated, create a specialist adapter using verified original/permissioned data, then repeat the independent benchmark.
7. The production gate remains strict: at least 300 independent held-out outcomes, zero observed failures and a real Sol Light review in the repo's qualification policy. This is a policy target, not a demonstrated model success rate.

### Commands (from repository root, only on Qwen-Local-Helper)

The script works only with already-installed Ollama model tags. First add enough independently verified cases to an ignored `data/...` JSONL file. The included `cases.example.jsonl` has **only four illustrative synthetic cases**; it is not a representative benchmark.

```bash
ollama list
python qwen-helper/training-workbench/experiments/weight-space-08b/pilot.py --cases qwen-helper/training-workbench/experiments/weight-space-08b/cases.example.jsonl --models qwen3.5:0.8b,YOUR_EDITED_MODEL_TAG --out qwen-helper/training-workbench/data/evaluations/08b_pilot.jsonl
```

Run a separate `--think` comparison for patched thinking mode and an optional run with your existing coder. No downloads or trainer executions occur. A model tag is not guaranteed available locally; the script refuses missing tags. The MIT edited checkpoint exists on Hugging Face but must be explicitly imported into your compatible local runtime.

### How to judge go/no-go

Do not infer stage success from Python syntax! A tiny 0.8B model may be excellent for narrowly specified fixtures but poor at open-ended Blender repairs. Pilot at least 10–20 representative *independent* tasks per stage before investing in adapters, then use much larger frozen held-out sets for promotion. Set thresholds in advance (e.g. meaningful first-try pass rate at a fraction of Astra repair cost, no protected-asset changes) and measure actual outcomes rather than extrapolating MIT's math improvement.

Astra's direct weight editing is an **optional investigation** of a reproducible defect, not the main training strategy. The first baseline and LoRA adaptation should be conventional, independently verified, and reproducible.
