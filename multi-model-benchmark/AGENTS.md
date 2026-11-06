# Agent setup instructions — Multi-Model-PMX-Benchmark

The human and agent use exactly the same public setup commands in [START_HERE.md](START_HERE.md).

1. Work only on Multi-Model-PMX-Benchmark. Do not touch unrelated branches or repositories, including Bobcat-fitness. Confirm Python >=3.10, Git, and existing Docker/Ollama. Ask before installing system dependencies, downloading Docker images, or making privileged system changes.
2. From repository root execute: python multi-model-benchmark/setup.py prepare. This creates the ignored folder hierarchy, runs unit tests, and generates the existing synthetic fixtures. Report test failures exactly; do not claim ready if anything fails.
3. **Do not download animation packs or the VMD sample**, including by assets.py fetch, browser, curl, wget or another download command. Do not download or replace AI model weights. Human personally downloads the files named in the manual-inbox/README.txt. Keep the inbox intact.
4. Once the human has supplied files, run python multi-model-benchmark/assets.py import-inbox; then python multi-model-benchmark/assets.py list. Missing files are WAITING, not a successful qualification. Review licenses and source hashes before freezing any benchmark.
5. If a locally available, pinned Blender image exists and you have permission to use Docker, run the Stage 03 correct/wrong smoke test from START_HERE.md. Stop on isolation failure. Preserve all evidence and never run model-generated code directly on the host.
6. Inspect only existing Ollama models. Run model proposal/evidence evaluation only after the smoke passes. Report what ran, results, installed dependencies, manual inbox paths, missing assets, next exact manual commands, and blockers. Never invent a pass.

**Manual equivalence:** The user can do every agent step with the exact commands in START_HERE.md. Leave the environment in a state they can resume at any point.

**Branch scope:** Running astra-qwen-weight-lab/fixtures.py generate is permitted on Multi-Model-PMX-Benchmark for test data only; its historical AGENTS.md targets Qwen-Local-Helper. Do not modify the original Qwen lab or historical data.
