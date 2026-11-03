# Agent bootstrap and boundary

Read [INSTALL_PROMPT.md](INSTALL_PROMPT.md) and [README.md](README.md) before starting. Only branch `Qwen-Local-Helper` is allowed. Preserve existing work and verify commit-contributor policy before any remote push. Never touch `main`.

**Stage 00 = Codex exclusively.** Stages 01/02/07 = Codex main, optional narrow local diagnostics; 08/09 = Codex. Stage 03/04/05/06 = **qualified** local Qwen may perform main implementation/test scripting on disposable candidates, checked by actual Sol Light then original human gates. No agent or local model can approve a gate.

Reuse the *already installed* Ollama coding model; configure it through `install.py` with its exact observed tag/digest. No model pulls or global configuration changes. An Ollama GGUF tag is not a full-weight HF fine-tuning base; verify compatibility before QLoRA.

The local specialist returns only a script proposal. `done.py` completion is an event, not acceptance. Codex independently verifies predecessor acceptance, approved constraints, stage skill requirements, candidate render/evaluation evidence, sandbox, and human decisions. Failure/absence/uncertainty routes to original Codex without retrying the local specialist.

Train only with original/permissioned verified examples; keep datasets, models, runtime config, logs and candidates in ignored `data/`. Unseen holdout never enters training or prompt tuning. The qualification manifest needs real independent evidence (minimum 300 held-out cases and zero failures, Sol Light and actual runtime checks) and an exact model digest. No fabricated results or claimed perfection.
