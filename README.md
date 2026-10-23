# Anime Blender Skills

Eleven Codex skills for converting PMX anime game characters, especially Wuthering Waves-style humanoids, into native Cycles Blender animation assets. Version 1.0.0.

The pack includes the orchestrator, ten stage skills, stage action policies, candidate/approval ledger, PMX inventory parser, experimental Blender tools, shader seed definitions, templates and model-role configuration examples. It contains no game models, textures, professional reference rigs or approved character recipes.

## Download and install

Download [anime-blender-skills-v1.0.0.zip](https://github.com/AlexV4981/PMX--Blender/raw/refs/heads/main/downloads/anime-blender-skills-v1.0.0.zip) while signed into GitHub with access to this private repository. If GitHub displays a file page, use its download button. [SHA256SUMS](https://github.com/AlexV4981/PMX--Blender/blob/main/downloads/SHA256SUMS) records the archive checksum.

Extract the ZIP directly into your personal Codex skills directory: `~/.agents/skills` on macOS/Linux or `%USERPROFILE%\.agents\skills` on Windows. For a repository-scoped installation, use `<your-project>/.agents/skills` instead. All eleven `anime-blender-*` folders must be siblings, each with `SKILL.md` directly inside it. Avoid installing a second copy of the same named skill.

Alternatively, copy the eleven directories from the local export's `skills/` folder into that location. `INSTALL.md` and `pack-manifest.json` in the ZIP can stay outside the skills directory. Codex detects local skill changes; restart it if the skills do not appear. These paths follow the [official OpenAI skills documentation](https://learn.chatgpt.com/docs/build-skills), checked 2026-10-23. This is a direct skill-folder distribution, not a published plugin.

## Start a character

Choose GPT-6.1 Sol with high reasoning as the parent/orchestrator in your Codex host, where available. A skill does not change the parent model automatically. The optional TOML examples in `skills/anime-blender-pipeline/assets/codex-agents/` describe the low-reasoning routine worker, High implementation worker and Astra escalation role. Follow `references/roles.md` to configure supported agent roles; account/model availability still applies.

Prompt Codex:

> Use $anime-blender-pipeline for this character. Start at stage 00, inspect my supplied PMX, textures, in-game reference images and Blender rig references, and stop at every human gate. Report missing inputs and actual Blender access before starting conversion.

Provide a local Blender installation and access to the actual character sources. The cloud workspace containing a skill does not automatically control your laptop. Missing visual references must be recorded and any proposed assumptions presented for human review.

## Stages

| Stage | Skill | Purpose |
| --- | --- | --- |
| Coordinator | `anime-blender-pipeline` | Enforce the contract, evidence, roles and human gates |
| 00 | `anime-blender-00-setup` | Pin environment, scope and references |
| 01 | `anime-blender-01-import` | Import PMX and inventory losses |
| 02 | `anime-blender-02-materials` | Restore Cycles materials |
| 03 | `anime-blender-03-geometry` | Establish geometry and deformation |
| 04 | `anime-blender-04-rig` | Build native Blender controls |
| 05 | `anime-blender-05-ready` | Prepare facial and animator controls |
| 06 | `anime-blender-06-tests` | Qualify animation and integrity |
| 07 | `anime-blender-07-look` | Match the approved in-game appearance |
| 08 | `anime-blender-08-physics` | Build editable native simulations |
| 09 | `anime-blender-09-audit` | Audit, approve optimization and deliver |

## Non-negotiable workflow

- Preserve original files; work on derivative candidates. Every stage requires human review before advancement. Create at most three candidate IDs per gate and only as many as needed.
- Priorities: fidelity, animation, realism, performance, convenience, in that order. Visual, material and geometry changes need matched comparisons and explicit human acceptance.
- Deliver a ready-to-animate Cycles `.blend`, editable toggleable simulations, portable texture assets and an animator guide. PMX compatibility is not a final requirement.
- Permit construction add-ons and reviewed embedded Python. A hyperspecific final runtime add-on requires ten distinct failed alternative approaches and explicit acceptance of the dependency.
- Optimize at stage 09. Measure Material Preview on the actual Nitro V laptop: Ryzen 5 7535HS, 16 GB RAM, 6 GB VRAM. Physics off requires at least 24 average FPS; fresh active physics targets about 12 FPS, with severe stalls disclosed.

## Validation and current limits

The skill manifests passed static validation; the pure-Python suite passed 21 tests. No real character conversion, Blender fixture execution, laptop benchmark or second-machine replay has been completed. Shader seeds are experimental definitions, not tested `.blend` shader libraries. Near-identical showcase reproduction requires qualified character recipes, exact assets, pinned versions and approved numeric tolerances; this pack alone does not establish that result.

Run the included utility checks from the local export root (or remove the `skills/` prefix when running from the extracted ZIP):

```sh
python3 -m unittest discover -s skills/anime-blender-pipeline/scripts/tests -v
python3 skills/anime-blender-pipeline/scripts/blender_tools.py validate-seeds
```

Read `anime-blender-pipeline/references/qualification.md` in the extracted ZIP before claiming additional qualification. `pack-manifest.json` contains SHA-256 hashes of the exported skill files, with paths relative to the local export root. Keep source assets, working scenes and per-character approvals outside this distribution folder.
