# Evidence pipeline hardening v2 — additive changes to Claude's implementation

**Scope:** This patch is meant to apply **after** `0001-feat-hash-chained-evidence-ledger-hash-bound-evaluat.patch` on `Multi-Model-PMX-Benchmark`. It does **not** replace, rewrite, or delete the archived Qwen work. The supplied archive is a code snapshot, **not a live Blender benchmark**.

## What is changed

1. **Fresh-process verification:** generated `solve(scene)` code runs in a disposable Blender **builder** container and outputs an untrusted `.blend` + JSON result. A **separate** Blender **verifier** container, with no candidate script execution, opens that derivative with `--disable-autoexec`/`use_scripts=False`, recomputes the trusted synthetic oracle, and writes the only trusted result to a different mount. Builder cannot mount that result directory. Both container commands use no network, read-only root, no capabilities, non-root user, no-new-privileges, limited CPU/RAM/PIDs, and a pinned image digest.
2. **Fail-closed results:** a pass requires both process exit codes zero, no timeout, matching candidate/case/oracle hashes, fresh-verifier marker, and a content-addressed receipt. The hash-chain validator rechecks the receipt, so a hand-written `blender_pass: true` and an old same-process oracle output are rejected. Probe exit code must be zero, too.
3. **Safe qualification:** reports reject mixed exact model digests; 300 repeat runs of one case are **one unique case**; production evidence requires distinct held-out real cases, multiple source families, both VMD/PMX and native Blender tracks, one frozen selected configuration, and narrowly scoped independent decisions. The 35% Codex-effort gate is still not automatically measurable, so this implementation **never issues an automatic production-qualified verdict**.
4. **Lap and metric repairs:** attempt numbering is scoped by experiment + lap + trial + case; the 20-case development pilot requires 20 unique first attempts and at least five fixture families; repeated blocked reasons are actually counted. The rate labeled model+oracle excludes human review and should not be called end-to-end throughput.
5. **Preserved raw outputs:** runner captures full raw output text; ingest checks its digest and stores content-addressed raw bytes, not only a hash or extracted code. Missing/tampered raw artifacts invalidate recorded provenance.
6. **Frozen splits and holdout guard:** family-separated manifest is a versioned, hashed JSON file. The CLI checks membership on ingest. Final holdout runs require explicit `--final`, a previously frozen **final-eval child lap** of a validation-tested parent, and a selection-rule hash. Exposed holdouts are marked compromised and never silently treated as untouched.
7. **Reviewer command:** `python -m evidence.cli decision` appends a scoped decision with a hashed human-authored review document. **Reviewer names and role strings are not authentication.**
8. **Windows:** `fcntl` and Windows `msvcrt` byte locking have a compatible code path. Native Windows behavior has NOT been tested. WSL2/Linux remains the recommended runtime for Docker/Blender and shell commands.

## Minimal setup on the full GitHub repository

After applying Claude's patch, apply the accompanying `0002-...patch`. The new module uses existing repository sources at `astra-qwen-weight-lab/fixtures.py` and `blender_oracle.py`; the standalone evidence archive does not include them.

```bash
# On Multi-Model-PMX-Benchmark, after applying 0001
# git apply --check /path/to/0002-harden-model-evaluation.patch
# git apply /path/to/0002-harden-model-evaluation.patch
python -m unittest discover -s multi-model-benchmark/tests -v
python astra-qwen-weight-lab/fixtures.py generate
```

Run the application commands from inside `multi-model-benchmark/`:

```bash
cd multi-model-benchmark
python -m evidence.splits --cases ../astra-qwen-weight-lab/data/fixtures/cases.jsonl \
    --out data/synthetic-dev-splits.json
python -m evidence.cli lap --data qwen35-stage03 --experiment qwen35-03 \
    --lap-id lap-00 --task geometry_weight_normalize --reason "untuned baseline" \
    --split-manifest data/synthetic-dev-splits.json
# Run Ollama's proposal-only runner separately and then ingest its exact JSONL:
python runner.py inspect --model qwen3.5:9b
python runner.py run --model qwen3.5:9b --stage 03 \
    --cases ../astra-qwen-weight-lab/data/fixtures/cases.jsonl \
    --out data/qwen35-03-lap00.jsonl
python -m evidence.cli ingest --data qwen35-stage03 --experiment qwen35-03 \
    --lap-id lap-00 --trial-id t1 --runner-jsonl data/qwen35-03-lap00.jsonl \
    --cases ../astra-qwen-weight-lab/data/fixtures/cases.jsonl --split dev
# Requires a real, locally installed, digest-pinned Blender image:
python -m evidence.cli probe --data qwen35-stage03 --image blender@sha256:<actual-image-digest>
python -m evidence.cli evaluate --data qwen35-stage03 --experiment qwen35-03 \
    --image blender@sha256:<actual-image-digest>
python -m evidence.cli verify --data qwen35-stage03
python -m evidence.cli report --data qwen35-stage03 --experiment qwen35-03 \
    --out data/qwen35-03-report.md
```

Do not treat placeholders as actual model/image tags. The installed model's digest, quantization and correct Ollama name must be verified first. The runtime does **not** download models or animation assets automatically.

### Final holdout protocol (later, only when a meaningful real-model holdout exists)

- Author a family-separated split manifest and freeze it at lap 0. Never use development fixtures as a production holdout.
- Run development and validation on a candidate lap; freeze selection **without consulting holdouts**.
- Create exactly one child lap with `--parent <selected-validation-lap> --final-eval` and the same split manifest and selection-rule hash.
- Only then ingest the held-out cases with `--split holdout --final`. Contaminated holdout exposure remains recorded.
- A scope-specific review requires a real review artifact. Example:

```bash
python -m evidence.cli decision --data qwen35-stage03 --experiment qwen35-03 \
    --kind human_gate --outcome changes_requested --reviewer operator \
    --scope 'qwen35-03|<model-digest>|geometry_weight_normalize|<selected-validation-lap>' \
    --review-file /path/to/actual-review.md
```

## Test status and limitations

- **Offline mock regression tests** prove wiring, evidence receipt checking, split validation, qualification guards, trial scoping and nonzero exit handling. They do **not** prove the Blender Python API, actual container isolation, security against a compromised host, or realism of the PMX/animation benchmark.
- Run the correct/wrong Stage 03 smoke candidates in a **real** pinned Docker Blender image before trusting the bridge. Inspect network isolation, `--disable-autoexec`, user permissions, container logs, and exact source hashes. The old same-process oracle's vulnerability is no longer used to grant passes; keep its historical regression test for reference.
- Stage 04–06 require separate positive and negative real Blender smoke runs. **No real Blender, Ollama inference, PMX, VMD or motion-validation evidence was produced while preparing this patch.**
- The 300-case holdout, 35% cost gate and externally verified human approvals are deliberately **not automatically qualified**.
- Motion source links and `not_downloaded  manifest entries from the original archive remain untouched. Unlicensed motion files are not silently added.
- The hash chain is not tamper-proof against a host administrator. Blender can still have parser vulnerabilities; use an updated image, disposable data and defense-in-depth.
