# 00 — Setup and reference calibration: working procedure

## 1. Establish evidence and identity

Inventory PMX, archive, textures, source terms and supplied references by hash. Identify exact character, costume and source revision. Distinguish an original game asset from a fan PMX interpretation: missing game shader inputs cannot be recovered from the PMX by wishful inference. Preserve source readmes and encoding. Label reference confidence per feature (direct visible evidence, indirect, unknown).

Record Blender executable/build hash, importer release/commit, OS, Python, GPU/driver, enabled add-ons and OCIO configuration. Pin a tested combination; do not upgrade an existing conversion to a moving latest release. Run the environment probe and existing utility tests. A missing laptop blocks hardware qualification, not preparation of the scene.

## 2. Calibrate comparison conditions

Create separate immutable fixture settings for (a) texture/emission diagnosis, (b) neutral diffuse response, (c) directional light sweep and (d) final showcase. Pin cameras, projection/focal length, resolution, lights/world, exposure, view transform/look, samples, seed and denoising. Use Standard as a proposed diagnostic setting, not a global cure for washed-out colors. Preserve a separately approved showcase transform. Do not adjust exposure while tuning a texture.

Choose Z-up, -Y-forward and meters if compatible with the project. Measure body height using anatomical landmarks, excluding tall accessories. For approved height H and measured import height h, scale factor s=H/h; transform mesh, rest bones, shape-key positions and later physical dimensions consistently. Setting scene units alone does not resize geometry. Do not apply transforms to a bound character without a correspondence test.

Classify screenshots by camera, pose and lighting uncertainty. Use matched landmarks before color comparison; unknown FOV and perspective can imitate proportion errors. Record all assumptions and proposed tolerance units. Leave uncalibrated thresholds null. Never invent model measurements or universal color-error limits.

## 3. Specify a practical pilot

Freeze required rig controls, expressions, physics categories and approved ranges. Begin with a small material pilot: one face/skin patch, one hair clump, one opaque garment and one alpha edge, including front/three-quarter/backlight views. Do not launch full-character shader replacement before this pilot works. Keep geometry and animation acceptance separate from shader matching.

Define actual UI benchmark protocol and its availability; headless evaluation is not viewport FPS. Prepare fixtures without claiming they have run on the target laptop.

## Evidence

| Check | Minimum actual evidence |
| --- | --- |
| source-inventory | File hashes, model identity, license/readme inventory, missing dependencies |
| environment-lock | Executable/build/add-on/OCIO facts and probe log |
| reference-and-scope | Reference board with confidence, allowed edits, cameras and calibrated assumptions |
| capability-spec | Rig/physics requirements, pilot scene settings, tolerance status and hardware test plan |

## Apply mathematical support

Use robust landmark reprojection fitting to calibrate camera while keeping known pose/geometry fixed. Save pixel residuals and ambiguity; ask for framing/landmark confirmation at the existing setup gate.

Read PACK/references/mathematics.md for the 00 procedure, equations, assumptions, evidence fields and primary references. Use only methods relevant to this fault; preserve the ordered work above. Bundled measurements do not imply the optional solvers were implemented or that a human approved the result.

## Technical references

Consult PACK/references/sources.md for primary documentation matched to the pinned Blender build. Treat formulas and proposed methods here as engineering guidance, not evidence that the character has been qualified.
