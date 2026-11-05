# Humanoid motion qualification: PMX/MMD and native Blender

**Status:** Source/reference plan for the existing Stage 04–06 workflow; research catalog, **not** installed motions, downloaded assets, passing test results or a new approval gate. Reviewed 2026-11-05.

## Why two complementary suites

1. **Deterministic controlled range-of-motion (ROM) sweep**: generate our *own* stage-authorized, versioned joint/control fixtures. This tests the complete **supported rig/control range** for each character, not an invented universal human anatomical angle. A dance/walk file cannot prove every axis, combination or intermediate frame.
2. **Real motion validation**: independently sourced, rights-cleared human motion clips are retargeted to test actual locomotion, contact, deformation, switching and usability. Preserve the original source clip, source skeleton, unit/scale, FPS, mappings and license provenance. A retargeted clip is not automatically a PMX-native motion.

Maintain both:
- **PMX/MMD baseline:** .pmx model with known rest pose + VMD bone/morph animation, or VPD poses, evaluated in an MMD-compatible reference runtime where possible.
- **Blender native result:** imported/converted candidate .blend with native Action/NLA and/or BVH/FBX-derived baked Actions, evaluated with Blender's actual constraints and deformation. Compare common semantic targets/landmarks rather than naive bone Euler numbers.
- **Cross-format paired source:** derive a controlled VMD and Blender Action from the same verified semantic joint target fixture when the relevant bones/controls support it; verify exporter/importer mappings separately.

MMD Tools imports and exports PMX/VMD/VPD but its documentation warns **MMD and Blender IK solvers can differ**. Do not label differences as model failures until mapping/solver/runtime baselines are known.

## Required ROM fixture coverage (both sides, where supported)

| Family | Controlled tests | Real motion follow-up |
|---|---|---|
| Root / COG / torso | reset, translations, axial twist, bend, combined lean | walk/run, turn, crouch |
| Shoulders / upper arms | forward/back, lateral raise, twist, cross-body; isolated & combined | reaching, overhead reach, dance |
| Elbows / forearms | bend/extend, pronation/supination; mirrored | reaching, carrying, punching |
| Wrists / fingers | bend, deviation, rotation, curl/spread, grip; expressive combinations | hand gesture / grip when source tracks fingers |
| Hips / knees | hip swing/abduction/twist, knee flex; mirrored & symmetrical | squat, lunge, kick, stair/contact |
| Ankles / feet / toes | pitch/roll/toe flex, plantar contact, foot roll | walk/run, planted turn, jump/landing |
| Neck / head | look, tilt, turn, combinations | turning, reacting |
| IK/FK / spaces | target-pole, switch mid-pose, mirrored side, keyed and interpolated frames | feet planted, hands reaching |
| Face/morphs | neutral, blink, eye aim, brows, jaw, visemes; isolation and combined | face clips only if explicitly available |
| Secondary appendages | approved tail/hair/clothing motions only when present | physics-off first; separate secondary check |

Probe neutral, interior, edge-of-approved-range and return-to-neutral, never automatically force a pose beyond the character-approved limits. Include keyed **and in-between** frames, single-axis and interacting rotations, positive/negative controls where valid, left/right symmetry, reset, scale, root motion/in-place, physics-off, clean Blender process and failed/missing-bone behavior. Stage 04 remains **left-arm pilot only** until pole placement is independently resolved.

Check bone endpoint trajectories and world-space IK/FK continuity, nonfinite transforms, mesh deformation and topology anomalies, self-intersections, foot slide and contact, hand reach, thumb/finger compatibility, face clipping, and stable visually inspected Cycles contact sheets; use model-specific tolerances and source identity. Preserve observed failures with frame/time and causes.

## Suggested independent real-motion sources

| Source | Format / scope | Best use | Licensing / caveat |
|---|---|---|---|
| [CMU Graphics Lab Motion Capture](https://mocap.cs.cmu.edu/) | 2605 human trials; original ASF/AMC, converted BVH links | Broad walking, running, athletics, pantomime, testing | Official site says 'free for all uses'; verify source and conversion notices; captured fingers/thumbs are **not tracked**. No VMD supplied. |
| [Ohio State ACCAD Open Motion Project](https://accad.osu.edu/research/motion-lab/mocap-system-and-data) | BVH packs incl. general motions, running, walking, handspring, martial arts | Diverse independent real Blender clips, high-motion stress | Site marks Open Motion Project **CC BY 3.0**; record required attribution and per-clip source. No native VMD. |
| [Blender BVH importer](https://docs.blender.org/manual/en/4.5/addons/import_export/anim_bvh.html) | BVH into animated armature | Import real clips, bake mapped native Actions, check FPS/axes | Blender's import does not automatically retarget different bones/rig controls. |
| [Blender MMD Tools](https://github.com/MMD-Blender/blender_mmd_tools) | PMX/PMD, VMD/VPD import/export | PMX baseline, own synthetic VMD/vpd fixtures, controlled format roundtrip | Match Blender/add-on versions. PMX, VMD and Blender constraints/IK are not identical. |
| [Community MMD motion portals](https://bowlroll.net/) | Creator-specific VMD | Optional real PMX dance/morph motion | Not automatically licensed for ML training/testing or redistribution; require original creator license and motion provenance before use. |
| [Rokoko free mocap assets](https://www.rokoko.com/free-resources) | FBX motion packs | Optional manual artist/reference validation | Use in AI model **testing/training** only after explicit license check/authorization; advertised free animation use does not establish ML evaluation rights. |
| [Adobe Mixamo](https://www.mixamo.com/) | FBX human animations | **Excluded from AI evaluation datasets** | [Mixamo additional terms](https://wwwimages2.adobe.com/content/dam/cc/en/legal/servicetou/Mixamo-Addl-Terms-en_US-20210623.pdf) expressly bar ML training, testing and improvement using Mixamo content. |

For our **AI model** benchmark, prioritize *our self-authored deterministic fixtures* and the CMU/ACCAD rights-reviewed research data. Do not train on or use disallowed third-party motions to test/improve models. Third-party format-converted files may have additional licensing and accuracy constraints.

## Operational order (not a new pipeline)

1. Freeze one licensed test PMX rig and one native Blender rig plus rest poses, source hashes, versions and mapping profiles. Keep them outside public Git if redistribution rights are unclear.
2. Build/curate one semantic JSON fixture manifest (joint targets, constraints, sample frames, expected coverage) from character-approved limits. Produce independent own VMD/VPD for PMX and Blender Actions for the native rig; do not assume a direct one-click conversion gives identical joints.
3. Run PMX reference/VMD baseline, then Blender-native test separately; record solver and retargeting differences. For Stage 04 obey arm-pilot restriction.
4. Select real held-out clip families (walk, run, crouch, reach, kick, jump/landing, turning, dance/gestures). Retarget BVH onto Blender test rig with calibrated rest pose/axes/units, bake native Actions, sample keyed and intermediate frames. Where a VMD is needed, create a *mapped and reviewed derivative* only where rights allow; otherwise use our own VMD suite.
5. Execute in disposable isolated Blender with physics-off baseline; run exact stage checks and Cycles contacts, Sol Light review, and the existing human gate. Do not silently repair failures in Stage 06.
6. Record fixture IDs, source motion IDs, bone coverage %, frame coverage, failed mappings, observed errors, baseline-vs-final, runtime, confidence and report links in the single-model [MODEL_REPORT_STANDARD.md](MODEL_REPORT_STANDARD.md).

## Limitations / scope exclusions

- No existing external motion set proves full ROM for every anatomical and custom PMX joint. Rig-specific generated stress poses are essential.
- Generic BVH captures generally lack shape-key facial animation and can omit reliable fingers; use our own verified finger and expression fixtures.
- A model unable to animate a **missing/unsupported** control should be marked scoped-not-applicable, not a false pass.
- External animation licenses may distinguish Blender use, redistribution, training, evaluation and generated derivatives. Verify each before using for AI evaluation or publishing converted data.
- This document does not assert any clips have been downloaded, inspected or applied to actual PMX/Blender models.
