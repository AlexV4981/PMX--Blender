# Active 7B lab agent instructions

Read `README.md` and `CODEX_INSTALL_PROMPT.md`; work only on `Qwen-Local-Helper`. The original `qwen-helper/` and `skills/` are not yours to rewrite. Prior 0.8B materials are archived in `archive/qwen3.5-0.8b/` for retrospective comparison.

Only local tag `qwen2.5-coder:7b-instruct-q4_K_M` is the active base, verified by actual Ollama tags/digest. Four stage-specific Modelfiles use literal authoritative contents of each stage's technical `references/stage.md`. Never invent fixes for unresolved Stage 04 pole placement: left-arm IK target pilot only.

The 80-fixture run and first-try vs one-feedback-retry metrics are *experiments*. Production remains one attempt and no retries. Run generated scripts only in independently isolated Blender container and never on live source, accepted files, or host desktop. Record actual validation commands and failures. Do not claim passing on syntax alone.

Go/no-go registered: ≥75% first-try verified passes per stage, zero severe regressions, relative local+review work ≤0.35 normal Codex. If pilot fails, fallback to original Codex. QLoRA only after verified failure clusters, on optional ≥24GB GPU, with exact compatible Hugging Face weights; production qualification requires 300 independent held-out cases and zero observed failures plus real Sol Light/human gates. Weight edits reserved for diagnosed repetition loops only.

Keep all data, model training artifacts, generated Modelfiles, candidate code and verdicts in ignored `data/`. Never download weights or rent hardware without explicit approval.
