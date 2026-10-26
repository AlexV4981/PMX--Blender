# 02 — Material diagnosis and Cycles restoration: working procedure

## 1. Separate restoration from reconstruction

Treat PMX as geometry plus MMD material semantics, not the original game's shader. PMX diffuse/specular/ambient, base texture, toon texture, sphere mode, material morph and draw flags do not map one-to-one to a game PBR set. A fan PMX may omit the game's masks, face SDF, light maps or normals. Record missing inputs as missing; use a labeled proposed approximation only after showing its limits.

Preserve existing materials and create private copies for experiments. Do not call nodes.clear() across the character, replace all materials with Principled/Toon, repaint textures, generate replacement textures, or perform blanket gamma/normal fixes. The generic seeds in PACK are fixture graphs, not skin, face, eye, cloth or game presets. Do not append them until an isolated fixture has passed in the pinned Blender build.

## 2. Inventory maps before connecting them

For every used material slot, record mesh/polygon ownership, source material ID, PMX factors/flags/morphs, image hashes, UV map, image-node interpolation/extension/projection, active output target and existing node path. Identify unused slots separately. Use PACK/scripts/texture_audit.py on explicit texture files to produce raw-channel contact sheets and statistics. These are observations, not automatic classifiers. Inspect the contact sheets and UV overlay.

Build a material plan using PACK/assets/material-plan.template.json. For each map assign exactly one evidenced role or unknown; record separate per-channel roles for packed maps. Names and RGB appearance only suggest hypotheses. A purple image is not proof of tangent-space normals; alpha can contain a mask unrelated to opacity. Never connect an unknown map to Base Color or Alpha to make the graph complete. Unknown critical inputs block fidelity claims; preserve unused unknown maps in the inventory.

Image color-space settings belong to the image datablock, not each node. When one file is sampled as color and numeric data, use separately configured image datablocks and record both. Do not change a shared image setting and unknowingly alter other materials.

## 3. Run the diagnostic ladder in order

Use fixed camera, resolution, display transform and UV mapping. Save each diagnostic as a temporary material/scene derivative, never as the production fix.

| Diagnostic | What to isolate | Decision |
| --- | --- | --- |
| Raw file and RGBA channels | Decode, channel content, alpha edges | Fix exact dependency/decoding first; do not repaint |
| UV overlay/checker on material region | Correct UV layer, transform, seam and face ownership | Fix mapping only if demonstrated; route actual UV edits to 03 |
| Base color to Emission, strength 1, opaque | Texture and tint without lighting response | If wrong here, investigate map/UV/color/tint, not light or roughness |
| Constant neutral diffuse with original normals | Lighting, face orientation, split/custom normals | If wrong here, isolate normals/geometry/lighting; do not alter albedo |
| Verified opacity on a checker background | Actual opacity/association, edge fringe | Test straight/premultiplied interpretation and source flags |
| One diffuse/stylized response, then specular | Shading and highlight separately | Add only components justified by references |
| Whole material and nearby materials | Layering, shadows and interreflection | Expand only after the pilot works |

Emission diagnosis is unlit, not color-management-free; keep the display transform fixed. Compare rendered output with a properly transformed reference, not raw file bytes. Emission final materials also affect scene lighting in Cycles, so an emission diagnostic is not a production default.

## 4. Interpret color, alpha and normals explicitly

For ordinary sRGB color, Blender converts the sample to scene linear. Do not add a second gamma node. The sRGB decode is c/12.92 for c<=0.04045, otherwise ((c+0.055)/1.055)^2.4. Numeric roughness/metallic/masks/normal data use Non-Color unless source evidence specifies another encoding. HDR/linear maps require their actual source encoding. Raw PNG channel statistics are encoded-file values, not shader-linear color.

Document PMX diffuse multiplication and material morph effects. A texture multiplied by a nonwhite diffuse factor can become too dark, but setting every factor to white may destroy deliberate tinting. Isolate texture-only versus texture*tint and show the difference. MMD ambient is not automatically emission, AO or a physical color correction. Sphere maps use source multiply/add/subtexture semantics and coordinates; they are not ordinary albedo. A toon ramp is a shading lookup, not a face diffuse texture.

For genuine opacity a in [0,1], an explicit Cycles mix uses factor a, first shader Transparent BSDF, second shader surface. Confirm orientation with a=0 and a=1 fixtures. Do not infer a from luminance or use every alpha channel as opacity. Include PMX material alpha/morph multipliers only when their semantics are evidenced. Inspect fringes over light and dark backgrounds. Correct image alpha association without repeatedly premultiplying. Do not use an obsolete Eevee blend-mode property as proof that Cycles alpha is fixed.

For evidenced tangent normals decode n=normalize(2*RGB-1) through a Normal Map node with the correct UV basis. Never plug raw RGB into a shader Normal input. Test channel convention before flipping green. Do not reconstruct a normal map from a color texture. Preserve custom face normals; global recalculation can destroy anime facial shading. Route any approved normal edits to 03.

## 5. Choose a Cycles method with stated limits

Shader to RGB cannot supply Cycles lighting. Toon BSDF is a Cycles option, not a universal game-lighting reconstruction. BSDF output cannot be converted to a scalar light value by wiring it through Color Ramp. Test actual nodes and sockets in the pinned build.

If a controlled analytic toon approximation is proposed, use a declared key direction L and normalized shading normal N in the same coordinate space: x=dot(N,L), t=smoothstep(e0,e1,x), C=(1-t)*Cshadow+t*Clight. Use u=clamp((x-e0)/(e1-e0),0,1), smoothstep=u*u*(3-2*u), e1>e0. A dot-product ramp alone does not receive scene-light shadows, attenuation, indirect illumination or multiple lights. Do not advertise it as the original shader. Object-space light vectors must follow head/body transforms correctly. Test rotating the head and key independently.

Use a face SDF only if a real map and its convention are known. Derive head-space light using inverse rotation (exclude scale/translation), verify left/right mirroring and thresholds against actual channels. Do not invent an SDF from arbitrary albedo or apply spherical body shading to a face until it happens to resemble a screenshot.

Test eyes as layered parts: sclera, iris, pupil, highlights, eyelid/lash and any cornea. Diagnose double reflections, dark refraction and incorrect alpha separately. Do not solve eye readability by moving/replacing geometry in 02. Keep hair-over-eye/eyebrow visibility proposals separate; do not disable all shadows, make hair transparent, or shrink eye occluders as an unreviewed shortcut.

Treat outlines as a separate system with face/eye exclusions and a measured width in the comparison camera. Preserve imported edge information. New shell geometry belongs to 03; final line styling belongs to 07.

## 6. Validate before expansion

Render face/skin, hair, opaque garment and alpha pilots in Cycles front/three-quarter/profile, plus key-light sweep and backlight. Inspect actual images at native pixel size. Preserve local color, shadow placement, highlights, silhouettes and neighboring material behavior separately. Roll back any edit that improves one crop but breaks another. Only copy a proven setup to materials with the same evidenced semantics; material names alone are insufficient.

Material Preview uses a different renderer. Toon BSDF and other Cycles-only features need a separately tested preview approximation or Rendered Cycles viewport. Share palette/mask values where feasible; label the preview limits rather than promising identical lighting. Verify renderer-specific Material Output targets in the actual build and inspect both views.

Run `python3 "$PACK/scripts/material_plan.py" PLAN.json` before registering. This validates evidence fields and role completeness, not appearance or whether the claims are true. Preserve unresolved uncertainty and never fill evidence fields with fabricated paths.

## Evidence

| Check | Minimum actual evidence |
| --- | --- |
| material-mapping | Completed plan, channel sheets, UV/material ownership, graph/socket/image settings, before/after semantic inspection |
| cycles-comparisons | Inspected diagnostic ladder and pilot images; full-character regression views, exact fixture settings and delta explanations |
| preview-behavior | Actual Material Preview and Cycles comparison; unavailable effects and approximation labels |
| material-flag-report | Every relevant PMX tint/alpha/morph/toon/sphere/shadow/double-side/edge decision and remaining unknown |

A necessary map that is absent, or an unresolved face/alpha fault, remains blocked. Present a draft for critique when needed; do not call it shader restoration merely because it renders.

## Technical references

Consult PACK/references/sources.md for primary documentation matched to the pinned Blender build. Treat formulas and proposed methods here as engineering guidance, not evidence that the character has been qualified.
