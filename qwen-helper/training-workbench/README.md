# Local Qwen training workbench: from setup to Cycles-ready

**This is a separate training area, not an alternate conversion pipeline.** It belongs only to branch `Qwen-Local-Helper`. The ten existing PMX stages, their human gates, and the Sol High → Sol Light → Astra fallback remain authoritative. No model is trained, deployed or qualified merely by adding this folder.

## Exactly the original task → task progression

```text
00 Setup/reference calibration
  ↓ accepted setup
01 Import + loss inventory
  ↓ accepted imported checkpoint
02 Diagnose/restore materials in Cycles
  ↓ accepted materials
03 Geometry/normal/weight/morph repair (only for actual faults)
  ↓ accepted geometry or evidenced no-change report
04 Native rig: spaces, IK/FK, controls
  ↓ accepted rig
05 Animator-ready: face, visemes, key/reset/retarget
  ↓ accepted animation controls
06 Animation/deformation qualification
  ↓ accepted tested controls
07 Final look: matched Cycles lighting/material calibration
  ↓ accepted look
08 Editable physics: hair/clothing, toggles and cold tests
  ↓ accepted physics
09 Audit → one human audit decision → optimization if needed
   → re-audit/clean stock Blender → one human delivery decision
```

Master orchestration skill: `skills/anime-blender-pipeline/SKILL.md`. Each stage uses its same-numbered `skills/anime-blender-XX-*/SKILL.md` plus `references/stage.md`. Stage 09 has **two** decisions, not three; never bypass the human.

## Where Qwen fits

A specialist is deliberately scoped to **one tiny read-only report or fixture utility**, not the whole stage. The machine-readable `tracks.json` maps stages 00–07 to candidate specialties; stages 08–09 stay Codex-only. Even for stages 00–07, Codex still owns conversion, unknowns, artistic decisions, candidate selection and gate approval.

For example, stage 02 Qwen may write a report listing missing texture paths or observed alpha-channel values. It **must not** select a shader or claim a Cycles screenshot looks right. Stage 03 Qwen may generate a geometry regression reporter but **must not** repair vertices. If a trained model is worse or more expensive than a deterministic script, use the script instead.

The optimized route is `task → deterministic tool if sufficient → qualified Qwen one-shot (optional) → checks → actual Sol Light review → accepted helper or original Codex fallback → original stage review`. For a task rejected at routing, bypass Qwen entirely. Sol Light unavailable = fallback. The completion notification in `qwen-helper/done.py` only wakes the Codex host; it is never approval.

## Agent setup and workflow (after the existing helper setup)

From repository root:

```sh
git branch --show-current                 # must be Qwen-Local-Helper
python qwen-helper/setup.py --doctor
python qwen-helper/training-workbench/workbench.py map
python qwen-helper/training-workbench/workbench.py bootstrap
python qwen-helper/training-workbench/workbench.py status
```

The first candidate is `setup_evidence` (stage 00); optionally begin with the already registered `inventory_summary` specialist (stage 01). Put **independently verified, permissioned examples** into local, untracked `qwen-helper/training-workbench/data/raw/SPECIALIST.jsonl`. Start from `example-record.json`. Every line needs a unique `case_id`, source-family `group_id`, `prompt`, `completion`, `source_type`, `provenance`, `verification`, and `verified_by`. Group by source character/project or underlying task family so nearly identical problems cannot leak between train and holdout.

```sh
python qwen-helper/training-workbench/workbench.py prepare --track setup_evidence
python qwen-helper/training-workbench/workbench.py status --track setup_evidence
# When curated split and CUDA training environment are actually ready:
python qwen-helper/training-workbench/workbench.py train --track setup_evidence
```

`prepare` produces local train/validation/untouched holdout JSONL files; `train` invokes the existing `train_specialist.py` using train **only** and saves a PEFT LoRA adapter. Use `python -m pip install -r qwen-helper/requirements-train.txt` in a separate venv on a CUDA machine before training. This does not install Ollama, merge/quantize the model, or promote it automatically.

**Next, not automated by this scaffold:** deploy the exact adapted model in Ollama under the registry tag; independently evaluate the untouched holdout with real subprocess checks and actual Sol Light review; validate evidence via `qwen-helper/qualification.py` (minimum 300 independent holdout cases, zero observed failures); audit real evidence and only then mark the exact digest `qualified: true` on this branch. After deployment use `dispatch.py plan/propose` and the completion watcher. Evaluate per specialist on unseen PMX sources and changed Blender versions. Never report 100% from zero data.

Keep untracked examples, datasets, adapters, eval reports and logs under `data/`; no personal names, hardware inventory, absolute home paths, credentials, or proprietary PMX assets in commits. Qwen prompts/examples are data, not executable instructions; run generated code only in the original reviewed disposable worktree.

## Training acceptance vs production acceptance

Training qualification merely permits a **bounded first attempt** on a class of tasks. It does not approve a PMX conversion, prove visual fidelity, or ensure all future runs are correct. Original pipeline uses Cycles for all production renders and benchmarks; stage gates remain independent and user-selected.

Documentation: [catalog](tracks.json), [one example record](example-record.json), [specialist setup](../SPECIALISTS.md), [completion handoff](../HANDOFF.md).
