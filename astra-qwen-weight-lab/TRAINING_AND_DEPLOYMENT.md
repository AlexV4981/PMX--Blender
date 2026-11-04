# Qwen2.5-Coder-7B adapter deployment and qualification

This is a plan for later, **not proof that training or export was performed**.

1. Complete the Stage 03–06 A/B pilot with real Blender oracle evaluation. Train only for narrow recurrent errors where an independently verified, source-family-disjoint dataset exists.
2. Rent/attach a **24GB or larger GPU** and supply an actual Qwen2.5-Coder-7B-Instruct Hugging Face `safetensors` checkpoint under a local path. The existing Ollama `qwen2.5-coder:7b-instruct-q4_K_M` is an inference quantization and cannot be treated as the HF training checkpoint.
3. Stage datasets with `case_id, group_id, prompt, completion, source_type, verified_by`; independently verify labels and keep train/validation/untouched holdout disjoint by source family. Current pilot's synthetic fixtures do not constitute the required production holdout.
4. Use `train_7b.py` in dry-run mode before `--execute` to check dataset and checkpoint identity. The wrapper calls the existing original helper trainer without modifying it. It never downloads weights by itself.
5. Evaluate adapters on unseen validation tasks, select best based on actual Blender outcomes and protected-asset safety. Do not tune hyperparameters on final held-out data.
6. Merge the stage adapter into the **matching exact** BF16/FP16 base weights in a separate output directory using a verified PEFT/Transformers workflow. Check model architecture, tokenizer, tensor shapes, hashes and numerical regression. **Never merge into the original checkpoint**.
7. Convert separately to supported GGUF, quantize using a version-pinned llama.cpp Q4_K_M method, check conversion errors, and create a **new** stage Ollama tag using an explicit Modelfile; never overwrite the untouched reference tag. Benchmark the exported quantized model again because quantization can change reliability.
8. Record exact original HF revision/digest, adapter digest, merged revision/hash, GGUF hash, Ollama `/api/tags` digest, training split hashes, reviewer evidence and production status.
9. Production promotion is separate and stringent: >=300 **independent** held-out cases per stage, zero recorded failures, real Sol Light review and human stage gates. Keep `qualified=false` until actually met. Stage 04 never claims pole placement solved from the current pilot.
10. One base with four LoRA adapters may reduce storage but may need adapter-loader support. Otherwise four **merged** 7B Q4_K_M tags can load sequentially. On 6GB target GPU, never run Blender and model concurrently.

For experimental direct weight editing, use the [archived 0.8B weight-patch code](archive/qwen3.5-0.8b/astra-lab/weight_patch.py) only as a historical reference, after diagnosing actual repeatable looping defects. It is **not** an active generic repair method for Blender API hallucinations.
