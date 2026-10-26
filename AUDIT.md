# PMX Blender skill audit and version 2 rewrite

Reviewed source: AlexV4981/PMX--Blender, commit `1165dd3dbb0dbc6a8b144ebafa367bfa3d4d45aa` (version 1.0.0). Reviewed all eleven skill entrypoints, ten stage procedures, shared references, seed definitions and utility code.

## Main finding

The pack emphasized review bookkeeping far more than the Blender decisions needed to obtain a good result. It had useful source protection, candidate gates, dependency accounting and honest qualification labels. However, repeating these rules across stages did not make shader diagnosis deterministic. Stage 02 instructed the agent to append material-class templates before explaining how to prove map semantics or isolate the fault. Only two generic seed graphs were actually provided. Neither is a Wuthering Waves character shader library.

That is a credible explanation for the reported behavior, not a verified reconstruction of the user's failed run. No failed blend, screenshots, command trace, actual textures or Blender executable were supplied here. A particular bad result could also involve importer behavior, a model-specific material convention or execution errors. Those remain unconfirmed.

## Concrete instruction defects

- **Template-first work:** Stage 02's first operation was appending versioned templates for each material class. There were no implemented skin, eye, face-SDF, hair or layered-alpha recipes to match that instruction. The rewrite preserves working graphs, diagnoses the fault first and limits generic seeds to fixtures.
- **No ordered diagnostic separation:** “Inspect channels” did not require an actual raw-channel/UV/emission/neutral/alpha/shading sequence. The rewrite identifies which experiment distinguishes a texture error from a light, normal, tint or display-transform error.
- **Texture-role ambiguity:** The pack cautioned against filename-only inference but did not define a usable decision record, critical-unknown behavior or shared image-datablock color-space handling. Version 2 adds these, plus channel sheets and a plan validator.
- **Insufficient mathematical boundaries:** Native toon techniques, grants, deformation and physics were named without enough coordinate-space, bind-space or solver-specific reasoning. Version 2 gives limited formulas with explicit assumptions and warns where they are not equivalent to a game/MMD effect.
- **Approval artifacts could look stronger than they are:** The ledger checks nonempty evidence and file integrity, not visual truth. Version 2 repeatedly distinguishes identity, structural validation, completed rendering and actual inspected quality. It does not pretend to authenticate human decisions.
- **No practical stop rule:** The old pack bounded candidate count but not unproductive edits inside a candidate. Version 2 restores the best draft and re-diagnoses after two non-improving experiments.
- **Premature routine delegation risk:** Low-effort workers were assigned routine implementation without defining when material/rig/solver work stopped being routine. Version 2 reserves unfamiliar design for the capable role and keeps workers on proven recipes.
- **Missing inputs vs reconstruction:** PMX/MMD materials may not contain the source game's shader inputs. Version 2 separates evidenced restoration from a labeled approximation and never claims the original shader was recovered from absent maps.

## Coverage of every skill

| Skill | Risk in version 1 | Rewrite |
| --- | --- | --- |
| pipeline | Heavy policy, little failed-run triage | Fault/evidence loop, pilot dispatch, honest tool limits, version lineage |
| 00 setup | Fixture goals without practical material pilot | Separate diagnostic/showcase fixtures, camera/OCIO confidence, pilot scope |
| 01 import | Preservation policy without diagnostic handoff | Preserve correct import, exact texture identity, stable correspondence and loss evidence |
| 02 materials | Generic template-first reconstruction | Full diagnostic ladder, color/alpha/normal math, map plan, isolated pilots and regression views |
| 03 geometry | Repair methods without cause isolation | Bind-space/duplicate-skinning checks before weights, deform-only normalization, morph correspondence |
| 04 rig | Capability list without enough space/pole tests | Rest/world transform reasoning, pole degeneracy, evaluated switching error and one-limb pilot |
| 05 ready | Facial feature list without combination/reset proof | Isolated/combined controls, explicit morph types, reset/custom-property and real retarget tests |
| 06 tests | Named fixtures without enough evaluated measurements | Control-space inputs, evaluated geometry, interpolation samples and clean-runtime replay |
| 07 look | Artistic matching could compensate for upstream faults | Camera/light/material/grade order, outline projection limits and saved numeric look |
| 08 physics | Method catalogue without enough first-failure triage | Single structure pilot, one-way graph, cold-reset diagnosis and actual category suspension proof |
| 09 audit | Strong goals but no supplied UI FPS recorder | Explicit measurement limit, actual packaging replay, measured tradeoffs and no fabricated FPS |

Each stage entrypoint and its procedure was rewritten. Shared diagnosis, orchestration, tool instructions, role/task templates and metadata were updated. Existing ledger and PMX parser behavior was preserved, with the pack version advanced to 2.0.0 so old approvals are not silently reused. The existing experimental Blender inspection/seed builder remains experimental.

## New tools and what they prove

`texture_audit.py` reads explicit images and produces raw encoded RGBA channel sheets/statistics without modifying source files. It requires Pillow. It does not identify texture roles, apply OCIO/ICC, or silently downconvert HDR/high-depth inputs. Unsupported inputs are reported.

`material_plan.py` requires explicit roles, source hashes, evidence paths, packed-channel decisions and color-space rationale. A required unknown map must block the material and remain unconnected. Its success proves structure and file presence, not the truth of the artist/agent's interpretation. Templates intentionally fail until completed with actual evidence.

## Validation and limits

The pure-Python suite passed 30 tests, including source immutability, alpha-channel observations, unsupported high-depth input, map hash/evidence rejection, required unknown behavior, packed channels, ledger gates and PMX parsing. All eleven skill frontmatters and local links are checked separately. Two independent task simulations exercised material and rig/physics diagnosis with missing Blender/model inputs. These assess instruction behavior, not rendering.

No live Blender, actual character conversion, viewport benchmark, native graph validation or cross-machine replay was performed. Version 2 is a more explicit and tested instruction/tool revision, not a certified character conversion system. The next real validation is the user's exact last-correct import plus a small face/hair/alpha pilot in the pinned Blender environment.

## Resume recommendation

Use the last correct import, not the damaged shader derivative. Keep original source textures unchanged. Start a version 2 run with explicit lineage and fresh relevant gates. Diagnose one face material, one hair material and an alpha edge; inspect real renders before propagating. Do not ask the agent to rebuild the entire character to solve an isolated material fault.

## Subsequent mathematical integration

Additive mathematical support now covers all eleven skills without changing their stage order or gates. A shared method reference and profile document camera fitting, rigid alignment, regional color/appearance fitting, deformation/rig/face methods, held-out qualification and motion identification. The numerical helper implements CIEDE2000, declared sRGB/Lab conversion, rigid SVD alignment and quaternion distance; external solvers are explicitly unimplemented procedures. The current suite passes 41 tests, including 20 selected published color reference cases. WORKFLOW_COMPARISON.md freezes the integrated hierarchy and separately proposes reductions in redundant review; those reductions are not applied.

## Version 3 — approved lightweight Cycles workflow

The user approved applying the lighter hierarchy and requested Cycles only unless otherwise instructed. Routine paths, shared workflow guidance, contract, templates, policy and CLI now agree. Ten stage handoffs remain; 09 uses audit and delivery, with final delivery atomically accepting the exact tested/submitted bundle. Stage-specific reductions reuse matching setup/color/fixture evidence, avoid no-op geometry repairs and reserve deep diagnosis/search for actual faults. Regional color and hidden-fault checks remain. All default preview/comparison/timing evidence is Cycles Rendered viewport; no automatic alternate-engine graphs are constructed. Version 3 preserves historical version 1/2 runs rather than migrating their approvals. The current suite has 51 passing utility tests; live Blender behavior/performance remains unqualified.
