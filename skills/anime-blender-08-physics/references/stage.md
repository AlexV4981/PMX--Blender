# 08 — Editable native physics: working procedure

## Routine path

Use the short cold-reset/settle/turn/landing demo and human motion critique before expensive fitting. Still test category suspension, manual fallback, collisions and stability. Use PACK/references/workflow.md; retain Cycles-only evidence unless the user explicitly requests another engine. The technical sections below are the focused procedures for the work actually needed, not a requirement to redo unchanged systems.

## 1. Start with one physical structure

Map PMX bodies/joints plus visible hair, garments, accessories, tail/ears and applicable soft tissue to source IDs. Use the PMX as intent evidence; MMD solver numbers are not transferable Blender material constants. Choose one representative chain or panel before full-character construction. Preserve manual rig behavior and approved visible shape.

Choose cloth proxy for sheetlike garments; reviewed strip/volume proxy or constrained rigid-body chain for hair/tails; constrained rigid bodies for rigid pendants; localized soft-body or cloth proxy for suitable soft regions. Record why a method fits bending/stretch/collision needs and what it cannot model. Do not call a tracked empty, sinusoidal driver or damping-only constraint a native dynamic simulation.

## 2. Build one-way evaluation

Use animation rig -> animated attachments/colliders -> simulation proxy -> visible deformation. Keep proxy rest shape, pin/goal weights, collision surface and rendered mesh separate. Never drive an attachment from the already simulated mesh. Test modifier order with rigid translation/rotation and physics disabled first: render motion must not be applied twice.

Bind Surface Deform/Mesh Deform or other native transfer in the intended rest pose and record transforms/topology; rebind after relevant topology or rest changes. Test identity at rest, unit translation, rotation and manual fallback. Do not add Armature after proxy transfer merely to fix a double transform without measuring spaces.

Record real scale and apply transforms only with correspondence verification. Collision margin must be small relative to part thickness/separation, not a memorized meter value. Fix intersecting rest shapes and pinning before raising quality. Exclude adjacent constrained bodies from mutual collision where technically justified; preserve intended body/garment contacts. Add collision pairs gradually.

## 3. Tune from dynamics and failures

For a conceptual spring m*x''+c*x'+k*x=0, natural frequency omega=sqrt(k/m), damping ratio zeta=c/(2*sqrt(k*m)), and timestep dt=1/(fps*substeps). These explain oscillation and stability; Blender cloth/soft-body parameters are not all literal k and c. Do not paste these values into unrelated settings. Record solver-specific actual settings, mass/density assumptions, quality, substeps, gravity and timebase.

If it explodes at frame 1, inspect scale, initial intersections, pinning, masses, binding and dependency loops before stiffness. If it stretches, inspect constraint limits/proxy resolution/timestep before hiding it with damping. If it penetrates, inspect collision scope/margins and speed before increasing every quality setting. If it is too rigid, verify cache clearing and pin weights before lowering stiffness.

Define rest frame, sequential pre-roll, reset/cache-clear procedure and parameter-change invalidation. Run settle, start/stop, turns, locomotion, crouch, landing and contact tests from fresh caches. Measure tip travel/part length, stretch, penetration, settling and explosive frames. Report cold behavior separately from cached playback.

## 4. Implement honest independent category controls

Category off must provide a tested manual-animation result and stop that category's solver work. Cloth/soft-body modifiers can be disabled using tested native properties; rigid bodies share a world and category isolation requires actual tested architecture. Do not assume hiding a collection or changing constraint influence removes solver cost. If independent suspension cannot be established, mark it blocked instead of inventing a toggle.

Test every category alone and all combined, including viewport AND render state. A native property driver must reach the intended data path without handlers. Switching may require reset/pre-roll; do not promise seamless arbitrary-frame toggling unless demonstrated. Deliver editable unbaked simulations. Temporary QA caches are permitted; clear final bakes without deleting simulations.

## Evidence

| Check | Minimum actual evidence |
| --- | --- |
| physics-part-map | Every requested category, method, source parts, attachment/solver/transfer graph |
| cold-motion-tests | Fresh-reset clips, metrics, settings, cache state and failure frames |
| category-toggles | Each off/on state, manual fallback, real evaluation/cost evidence and reset limits |
| editable-unbaked | Native solver/proxy/settings retained, final bake/cache state |
| physics-settings | Exact solver parameters/units, collision scope, bindings and reset/pre-roll recipe |

## Apply mathematical support

Fit declared native solver settings to observed or human-approved target motion using inverse simulation. Freeze driver motion/timebase/reset. Keep XPBD and oscillator equations as appropriately limited references; prove actual toggles/cold behavior.

Read PACK/references/mathematics.md for the 08 procedure, equations, assumptions, evidence fields and primary references. Use only methods relevant to this fault; preserve the ordered work above. Bundled measurements do not imply the optional solvers were implemented or that a human approved the result.

## Technical references

Consult PACK/references/sources.md for primary documentation matched to the pinned Blender build. Treat formulas and proposed methods here as engineering guidance, not evidence that the character has been qualified.
