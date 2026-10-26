# 06 — Animation qualification: working procedure

## 1. Test without secretly repairing

Use a private test derivative with a versioned action/pose fixture and approved character-specific ranges. Freeze control-space inputs and sample frames. Test shoulders/hips, elbow/knee flexion, forearm twist, wrists, spine/neck, crouch, walk/run, planted-foot turn, jump/landing, fingers/grip and face combinations. Add only applicable fixtures; explain scoped exclusions.

Before and after the suite compare neutral reset, evaluated geometry and bone endpoints. Sample both keyed and interpolated frames to expose rotation flips and switching pops. Test mirrored controls, scale, IK/FK and spaces, root motion and supported retarget clips. Compare physics-off first; secondary motion must not conceal a bad body rig.

## 2. Measure the evaluated result

For corresponding vertices use d_i=norm(p_test_i-p_reference_i)/H in a common space and report max plus regional distributions. This detects differences, not whether a deformation is attractive. For switches use world translation and quaternion rotation errors. Check near-zero edge length, extreme triangle area change and penetrations as localized warning indicators, not automatic proof every garment contact is invalid. Use character-calibrated bounds, not invented universal anatomy.

Inspect actual face/hand/foot close-ups and silhouettes. Numeric metrics supplement appeal and control usability. Check nonfinite coordinates, invalid drivers/paths/targets, unintended duplicate deformation, bindings and evaluation warnings. An empty log does not prove absence of every dependency cycle.

## 3. Repeat with a clean runtime

Open the test derivative with stock Blender, construction add-ons unavailable and auto execution disabled. Run the same controls/frames and compare results. Test approved optional embedded helpers separately with their exact execution requirements. Do not infer dependency independence from the enabled-add-on list alone.

Route failures to 02/03/04/05 as appropriate with a minimal reproduction, affected frame, expected/observed result and artifact identity. Do not edit production in this qualification stage. Re-run only affected suites plus meaningful neighboring regression views after a repair.

## Evidence

| Check | Minimum actual evidence |
| --- | --- |
| motion-fixtures | Actual versioned inputs, sample frames and rendered clips/contact sheets |
| deformation-review | Evaluated regional metrics, silhouettes/close-ups, human review items |
| integrity-lint | Actual driver/target/numeric/binding diagnostics and resolved intentional exceptions |
| clean-core-rig | Fresh-process fixture results and environment/dependency facts |

## Apply mathematical support

Evaluate held-out poses/views plus fixed regression fixtures, compare actual arrays with calibrated tolerances, and report residual distributions/worst cases/repeatability. Human visual review does not replace hidden rig/dependency tests.

Read PACK/references/mathematics.md for the 06 procedure, equations, assumptions, evidence fields and primary references. Use only methods relevant to this fault; preserve the ordered work above. Bundled measurements do not imply the optional solvers were implemented or that a human approved the result.

## Technical references

Consult PACK/references/sources.md for primary documentation matched to the pinned Blender build. Treat formulas and proposed methods here as engineering guidance, not evidence that the character has been qualified.
