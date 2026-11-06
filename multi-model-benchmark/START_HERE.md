# Start here — model tests + premade animations

This branch contains the **hardened** append-only experiment ledger and **two-process** Blender verifier, plus links and an optional downloader for premade human animation files. **No local AI model is downloaded or installed.** The benchmark remains **unqualified** until a real Docker/Blender run verifies the isolation and a correct/wrong smoke pair behaves as expected.

The command examples assume a clone of **`Multi-Model-PMX-Benchmark`**, Python 3.10+, Git, and a compatible machine with Docker Desktop+WSL2 or Linux. When Docker images and Ollama models are already present, re-use them.

## Quick path (from repository root)

```bash
git switch Multi-Model-PMX-Benchmark
python -m unittest discover -s multi-model-benchmark/tests -v
python astra-qwen-weight-lab/fixtures.py generate

# Download free public standard motion packs and the upstream VMD format sample:
python multi-model-benchmark/assets.py fetch --asset mmd-tools-vmd-smoke
# Download both free Standard ZIPs from their publisher pages, then:
python multi-model-benchmark/assets.py import --asset quaternius-ual1 --file /path/to/UAL1-Standard.zip
python multi-model-benchmark/assets.py import --asset quaternius-ual2 --file /path/to/UAL2-Standard.zip
python multi-model-benchmark/assets.py verify
python multi-model-benchmark/assets.py list

# See installed models; DO NOT pull/reinstall:
ollama list
python multi-model-benchmark/runner.py list
```

**Download limitations:** The Quaternius free Standard ZIPs are not assumed to have permanent direct download URLs; download the exact free release from the publisher page and use the `import` command shown above. The helper validates and hashes the archive and extracts only supported motion formats. The upstream VMD test file can be fetched automatically, but its first-acquisition hash must be frozen in an approved experiment manifest before a reproducibility claim. Never claim the links alone mean binary assets are bundled.

## Animation sources (linked so humans and agents can fetch)

| Track | Asset | Direct source / publisher | License / usage | Automated? |
|---|---|---|---|---|
| Blender | [Quaternius Universal Animation Library 1](https://quaternius.itch.io/universal-animation-library) | Free Standard ZIP, FBX + GLB | CC0 1.0 | `assets.py import --asset quaternius-ual1 --file FILE.zip` |
| Blender | [Quaternius Universal Animation Library 2](https://quaternius.itch.io/universal-animation-library-2) | Free Standard ZIP, FBX + GLB | CC0 1.0 | `assets.py import --asset quaternius-ual2 --file FILE.zip` |
| PMX/MMD | [MMD Tools test.vmd](https://github.com/MMD-Blender/blender_mmd_tools/blob/main/samples/vmd/test.vmd) | [Raw upstream VMD](https://raw.githubusercontent.com/MMD-Blender/blender_mmd_tools/main/samples/vmd/test.vmd) | Upstream sample; inspect its license before reusing outside local technical tests | `assets.py fetch --asset mmd-tools-vmd-smoke` |
| PMX/MMD | [Eye-dart + breathing VMD](https://bowlroll.net/file/231043) | Download manually from creator; confirm included CC0 terms | Listed CC0; verify actual archive | Manual optional |
| Blender | [KinemIQ 35 free animations](https://kinemiq.itch.io/free-game-animations) | ZIP of 35 FBX/GLB clips | CC0 1.0 | Manual optional |
| Blender | [CMU motion capture archive](https://mocap.cs.cmu.edu/) | Original ASF/AMC; BVH conversions | CMU source terms, note derivative provenance | Manual optional |
| Blender | [ACCAD Open Motion Project](https://accad.osu.edu/research/motion-lab/mocap-system-and-data) | BVH motion clips | CC BY 3.0 attribution | Manual optional |

Quaternius free Standard is a **subset**, not all 120+/130+ animations from paid Source tiers. Packs may be bigger than the actual testing subset. No external animation is inherently compatible with every PMX rig: retargeting, bone mapping, rest pose, coordinate scale and IK solver differences must be measured. The MMD Tools VMD is a **format import/export smoke sample, not a proven full humanoid movement suite**. Real paired PMX/Blender motion qualification remains to be developed and validated; do not claim that downloading these files completes it.

The script stores original packages and VMD under ignored `multi-model-benchmark/data/animation-assets/`, extracts FBX/GLB only, writes source/hash receipts, and never runs downloaded executable content. Source files are kept separate from converted outputs. `multi-model-benchmark/animation-assets/manifest.json` documents intended sources; ignored `data/animation-assets/receipts/*.json` records what's *actually* present on the testing machine. **Do not commit third-party binaries without verifying rights.**

## First genuine Blender verification (no model required)

1. Find an **already installed** Blender Docker image, or manually obtain a compatible image. Note its **exact image digest** (an image ID is not the same as a registry manifest digest): `docker image ls --digests`.
2. Probe the sandbox; it must verify network blocking, read-only root, no secrets, and no ledger mounts.
3. Run both prewritten Stage 03 scripts: one should pass the original Blender oracle, and one should fail.

```bash
python multi-model-benchmark/smoke/run_stage03_smoke.py \
  --image 'blender@sha256:REPLACE_WITH_YOUR_ACTUAL_64_HEX_DIGEST'
```

This command requires a **real** Docker/Blender image and does not work with the placeholder digest. It creates a fresh ignored smoke ledger, executes the candidate in a throwaway Blender builder container, then validates the resulting `.blend` in a **separate** verifier container. Success requires `correct=pass` **and** `wrong=fail`. If isolation or either expected result fails, STOP: don't use those results to qualify an AI model. This test has not been demonstrated in a live Blender runtime in this handoff.

## Run one of your already-installed Ollama models (development pilot)

After the smoke succeeds, use the exact tag printed by `ollama list` (the illustrative `qwen3.5:9b` may not be your tag):

```bash
python multi-model-benchmark/runner.py inspect --model YOUR_INSTALLED_TAG
python multi-model-benchmark/runner.py run \
  --model YOUR_INSTALLED_TAG --stage 03 \
  --cases astra-qwen-weight-lab/data/fixtures/cases.jsonl \
  --out multi-model-benchmark/data/your-model-stage03-lap00.jsonl
```

This collects **inert code proposals**; it is **not** Blender verification. For the subsequent evidence-ledger ingestion, oracle and report commands, follow [HARDENING_v2_README.md](HARDENING_v2_README.md) exactly. The original `astra-qwen-weight-lab/pilot.py` and `score.py` are Qwen-only historical paths; do not use them to score the new runner. Reports are per model per specialization, and final cross-model comparison comes later.

## Evidence and safety limits

- Static unit tests cannot demonstrate actual Blender execution. Even a working Docker smoke does not constitute independent PMX/Blender character or animation qualification.
- Run model-generated Python only inside the independently isolated builder. **Never** run it directly in your desktop Blender or the legacy same-process oracle.
- A verified smoke is not a pass for any of the six models. Production qualification requires independent untouched real families, animation tracks, reviewer approval, and a measured efficiency gate.
- No claim that the archive/publisher URLs are reachable from every network; failures must be shown to the operator, not hidden.
