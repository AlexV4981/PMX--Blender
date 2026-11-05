# Premade humanoid animation packs for PMX and Blender

**Last checked:** 2026-11-05. **Status:** curated download links only. No clips downloaded, retargeted, executed, or verified on a particular PMX/.blend character. This list exists so Stage 04–06 can use **real premade animation**, not solely synthetic motion sweeps.

## Download first — Blender / FBX / GLB / BVH

| Source and verified link | What you actually get | License and access | Good stage tests |
|---|---|---|---|
| [Quaternius Universal Animation Library 1](https://quaternius.com/packs/universalanimationlibrary.html) | Free *Standard* pack around 45 humanoid clips (FBX/GLB); full Source tier advertises 120+ clips and .blend project; **do not assume all 120+ are free** | CC0 on creator's current listing; full Source may require purchase | 8-direction locomotion, jog/sprint, crawling, swimming, gestures, combat |
| [Quaternius Universal Animation Library 2](https://quaternius.com/packs/universalanimationlibrary2.html) | Free Standard subset; full Source advertises 130+ clips and .blend file | CC0 on current creator listing; full Source may require purchase | Parkour, melee combos, recovery, farming, zombie motions |
| [KinemIQ 35 CC0 clips ZIP](https://kinemiq.itch.io/free-game-animations) | On-page free downloads: 35 premade FBX/GLB actions, **not** all 460. 460-clip library browsable through [studio](https://kinemiq.app/), export FBX/GLB/BVH individually | The free on-page 35 are CC0. Full collection combines CC0 with attributed CC BY 3.0/4.0 sources; preserve individual provenance | Quick smoke/regression, many categories on one shared skeleton |
| [CMU BVH motion archive](https://github.com/una-dinosauria/cmu-mocap) and [official CMU index](https://mocap.cs.cmu.edu/) | **Actual** hundreds/thousands of premade motion BVHs (third-party conversion of CMU captured data); official source ASF/AMC | CMU says free for all uses. Keep conversion provenance; verify individual derivative notices | Real walking, running, turns, crouch, jumps, dance, athletics |
| [ACCAD Open Motion Project](https://accad.osu.edu/research/motion-lab/mocap-system-and-data) | Direct BVH downloads for numerous clips, other formats for more | CC BY 3.0, requires attribution | Handsprings, walking/running, martial-arts, turns |
| [Mesh2Motion source motions](https://mesh2motion.org/) | Blender source models and animation files, reusable animations and exported GLB/FBX | Publisher states CC0; confirm exact bundled asset provenance | Native Blender action/rig reference and export smoke test |

## Download first — PMX / MMD VMD / VPD

| Source and verified link | What you get | Rights check / limitations | Good stage tests |
|---|---|---|---|
| [MMD Guide — Walking, Running Motion Pack](https://mikumikudanceguide.weebly.com/downloads.html) | **Six premade motion clips**: male/female/chibi run + normal/lazy/cool-guy walk; click the *Walking, Running Motion Pack* download | Page requests credit to tweekcrystal; no express general AI training/testing grant found; inspect archive README and creator terms | PMX/VMD walk/run retarget, planted feet |
| [MMD Tools sample test.vmd](https://github.com/MMD-Blender/blender_mmd_tools/blob/main/samples/vmd/test.vmd) | One real 143 KB VMD test asset in the official add-on sample directory | License applicability to test asset must be checked; limited/synthetic test content unknown without preview | Parser/import/export smoke test |
| [CC0 Eye-dart & Breathing VMD](https://bowlroll.net/file/231043) | Premade **Eyedart_Breath_motion_v1.1.zip**, inside VMD motion files | Creator explicitly marks pack **CC0** on BowlRoll listing; content is eye/breath, not whole-body ROM | Stage 05 eyes, face controls and torso breathing |
| [LearnMMD downloadable motions](https://learnmmd.com/downloads/) | Full-body VMD meme/short performance examples plus lip-sync VMD assets and VPD poses | **Creator-by-creator license**; not a blanket AI testing/training or redistribution license | Body + lips, pose import |
| [XSTAGE VMD-capable motion packs](https://www.xstage.co/en/guide/how-to-make-character-dance-animations-in-mmd%3A-using-xstage-motion-data) | Commercial motion products where selected packs allow **VMD** download and include paired PMX mannequin | Paid; inspect EULA **before** any AI benchmark or redistribution | High-complexity pre-made dance, finger movement, jumps |

**Do not assume any VMD downloaded from random mirrors is copyright-cleared.** The GitHub collection [bear0830/mmd](https://github.com/bear0830/mmd) includes a walk VMD and many numbered motions but its README says the assets are collected from Touhou/Vocaloid; **not recommended as an AI benchmark source until original authors and redistribution rights are traced**.

## What to select for usable full movement

- **Locomotion:** 2 walks (one slow, one fast), jog, sprint, directional strafe, backward movement, planted turn.
- **Large joint excursions:** crawl, deep crouch, lunge, overhead reach, kick, roll, get-up, jump-and-land, acrobatic clip.
- **Interaction and rigor:** hand gestures, grasping/contact clips where hands are tracked, asymmetrical action, mirrored stances, IK/FK transitions.
- **Face:** eyes/blink/breath VMD and separately rights-cleared lip/viseme VMD.
- **Retarget variability:** at least one true VMD on an MMD skeleton; at least one Blender-compatible BVH/FBX on a non-MMD humanoid; test each individually on its native rig before mapping.

Even all these clips combined do not certify anatomical full ROM or finger/face coverage: CMU/ACCAD body BVH typically lacks detailed finger or facial tracks. Use the existing authored controlled range tests as a **supplement**, not replacement.

## Import/application procedure

1. Use **original PMX + VMD** in MMD or MMD Tools to observe source motion; pin source hashes, author/attribution, and bone names. VPD is a pose, not an animation clip.
2. Use **FBX, BVH, or GLB** to import premade animation into a *temporary* Blender scene; identify source action, FPS, rig scale, root motion and rest pose. Retarget via a verified bone correspondence map and bake a temporary target Action.
3. Run matching movement on original PMX and imported/converted native .blend as feasible. Beware **MMD vs Blender IK differences**; do not diagnose every retarget mismatch as bad geometry.
4. Evaluate Stage 04 (only approved arm pilot), Stage 05 controls, Stage 06 whole-body motion; sample interpolated as well as keyed frames, review Cycles frames, and log failures in [MODEL_REPORT_STANDARD.md](MODEL_REPORT_STANDARD.md).
5. Before using a third-party clip as **LLM training or model-development evaluation** rather than simply animating a 3D character, verify that specific license allows it. **Do not use Adobe Mixamo clips for AI training, testing, or improvement** under Adobe's Mixamo Additional Terms.

**Selection suggestion:** For the first smoke pass, take the 35 CC0 KinemIQ clips plus free Quaternius Standard pack(s) for Blender, the MMD Guide walk/run pack for PMX after verifying rights, and the explicitly CC0 Eye-dart/Breath VMD. Use CMU/ACCAD for the more diverse real-motion holdout.
