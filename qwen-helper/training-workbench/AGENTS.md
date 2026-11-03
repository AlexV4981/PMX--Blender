# Agent instructions — local PMX training area

1. Read `README.md`, `tracks.json`, `../SPECIALISTS.md` and `../../skills/anime-blender-pipeline/SKILL.md`.
2. Work ONLY on `Qwen-Local-Helper`; never write to `main`. Respect the GitHub contributor restriction before pushing.
3. `workbench.py map/bootstrap/status` first. Build permissioned, task-specific supervised examples and independently verify code; do not invent observed tests, benchmarks, or reviewer actions.
4. Train one specialist at a time, group-split by task/source family, freeze the unseen holdout before training and never use it for training or manual prompt tuning.
5. No private paths, personal details, secrets, PMX assets or large model weights in the repo. Keep training data and output under ignored `data/`.
6. Fine-tune the selected 1.5B Qwen base only when real examples exist. The presence of a training script is not evidence it works on the hardware; stop and disclose setup or GPU limitations.
7. Do not promote from a plausible JSON report. Require actual independent execution, Sol Light verification, exact Ollama digest, documented threshold and then explicit registry update.
8. Original Sol High/Light/Astra path, human decisions and Cycles-only fidelity standards are unchanged.
