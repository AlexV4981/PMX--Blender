# 07 — Final appearance calibration: working procedure

## Routine path

Reuse accepted camera/map/color definitions. Check changed look regions and critical Cycles face/eye/silhouette regressions, then ask visual critique. Rediscover materials only for a new fault. Use PACK/references/workflow.md; retain Cycles-only evidence unless the user explicitly requests another engine. The technical sections below are the focused procedures for the work actually needed, not a requirement to redo unchanged systems.

## 1. Calibrate the reference before the shader

Load the exact accepted stage 02 material plan and stage 06 rig. Re-run the material diagnostic ladder if texture/alpha/color faults reappear; do not conceal them with a new grade. Identify character/costume, pose, projection, lighting, exposure and postprocessing differences in the target image. Register reference landmarks before judging proportions. Unknown camera or tone mapping limits the accuracy claim.

Match pose/camera, then light direction/shadow, then material response, then final grade. Freeze already solved variables between experiments. Compare silhouette, local palette, shadow boundary, highlight shape, face/eye readability and line weight as separate dimensions. Photorealistic roughness/SSS is not an improvement unless the approved reference calls for it.

## 2. Tune the smallest supported parameter

Change a bounded parameter or one evidenced mask connection at a time. Preserve the raw textures. Texture painting is a separate reviewed proposal with original/delta assets. Do not add emission to brighten a wrong normal, remove shadows to expose eyes, or manipulate exposure to hide dark albedo. Use the same material plan/version and record final numeric socket values, ramps, normal treatment and output targets.

For shell outlines under perspective approximate width_px=f_px*t_perpendicular/z. Width varies with distance and normal direction; orthographic width scales with resolution/ortho span. Calibrate at actual camera/resolution and test face, hands, eyelashes and silhouette across motion. Freestyle is a render line system; test its actual final Cycles output and disclose any Cycles Rendered viewport difference. New shell topology returns to 03. Avoid promising constant pixel width from fixed world thickness.

Test hair/eyebrow visibility in front, profile, head turn, reflections, shadow and backlight before accepting any ray-dependent trick. Preserve occlusion consistency or disclose a deliberate stylized exception.

## 3. Store the accepted look

Save numeric palette/shadow/highlight settings, node-group hashes, map/channel roles, outlines and camera/light/OCIO assumptions. Do not regenerate a palette by reclustering screenshots on replay. Check final Cycles output and the Cycles Rendered viewport with the same material graph; do not build an alternate-engine approximation. Compare a short animation, not only a flattering still.

## Evidence

| Check | Minimum actual evidence |
| --- | --- |
| final-style-spec | Exact saved settings/assets and per-feature reference confidence |
| cycles-look-comparisons | Matched views and individual parameter deltas with actual image inspection |
| lighting-and-motion | Key/backlight sweep and head/body motion regressions |
| preview-limitations | Actual Cycles Rendered viewport comparison/settings and any difference from final Cycles output |

## Apply mathematical support

Reuse the material color/camera profile. Use regional CIEDE2000 and boundary comparisons; optional LPIPS is supporting evidence only. Use human preference feedback for artistic selection while preserving protected attributes.

Read PACK/references/mathematics.md for the 07 procedure, equations, assumptions, evidence fields and primary references. Use only methods relevant to this fault; preserve the ordered work above. Bundled measurements do not imply the optional solvers were implemented or that a human approved the result.

## Technical references

Consult PACK/references/sources.md for primary documentation matched to the pinned Blender build. Treat formulas and proposed methods here as engineering guidance, not evidence that the character has been qualified.
