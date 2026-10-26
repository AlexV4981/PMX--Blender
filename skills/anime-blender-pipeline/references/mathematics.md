# Mathematical fitting and human acceptance

## Contents

- Shared fitting rules and method status
- Color measurements and the provisional Delta E target
- 00 camera and reference calibration
- 01 import correspondence
- 02 material fitting
- 03 geometry and deformation
- 04 control rig and switching
- 05 face and expression fitting
- 06 qualification
- 07 final appearance
- 08 motion identification
- 09 audit and acceptance
- Primary references

## Shared fitting rules and method status

Use mathematics to answer a concrete question within the current stage; do not run every method on every asset. Keep stage boundaries, required check names, candidate caps and ownership. Follow the active lightweight path in workflow.md, including the two stage-09 decisions. Use the detailed diagnostic ladder for observed/uncertain faults, not every correct subsystem. This is a method reference, not an automatic repair system. Human approval can accept a disclosed approximation; it does not turn an unperformed test into a pass.

Classify a method as implemented-and-tested utility, external optional solver, or specified mathematical procedure requiring project implementation. Bundled math_tools.py implements CIEDE2000, declared sRGB-to-Lab conversion, residual summaries, SVD rigid alignment and quaternion angular distance. It does not implement camera/rig optimization, ARAP, PSD, a Bayesian optimizer, inverse simulation, or differentiation through Cycles. Never claim those solvers ran because their formulas are documented.

For each actual fit, copy assets/mathematical-profile.template.json into a mutable run derivative. Record input/baseline/fixture hashes, correspondences or masks, parameter names/bounds/units, frozen blocks, objective terms/scales, method/version, evaluation budget, stopping rule, metrics, visual evidence and known ambiguity. Register the profile with the candidate; keep outputs as separate evidence. Leave unknown tolerances null, not invented. Do not mutate an accepted profile or existing frozen ledger policy.

Use a stage-local objective:

    minimize E_stage(theta) + lambda * ||D * (theta - theta_baseline)||^2
    subject to approved bounds and all protected feature constraints.

D gives comparable scales to unlike units; lambda is recorded, not a universal magic value. Preserve the priority order lexicographically: fidelity, animation, realism, performance, convenience. Never let a favorable aggregate hide a failed eye region, broken rig or runtime dependency. Numerical proposals are not human acceptance.

Freeze camera, lighting, display transform and source-map interpretation before material fitting. Fit one causal block at a time; permit a coupled block only after a distinguishing test establishes its interaction. Use bounded coordinate search/line search with actual Cycles evaluations initially. Another renderer, including an external differentiable renderer, requires an explicit user request; use it only within that requested scope and re-evaluate final work in Cycles unless the request changes that requirement. No claim of automatic Cycles gradients is supplied.

Use preferential Bayesian optimization only when repeated human comparisons and enough evaluations justify it. A simple side-by-side or slider choice is the default human interface, with equally valid 'neither'/'already good' outcomes. Record attribute-specific feedback, such as 'A shadows, B palette'; do not infer a global preference from one attribute. A learned preference estimates the next useful experiment; it cannot approve a candidate. Preserve at most three formal candidate IDs. Numerical trials are bounded experiments inside an ID, not a loophole for unlimited designs. Record a finite render/iteration budget before starting; absent a budget, prepare the fit and bounded proposal rather than launch an open-ended search. Keep the two non-improving experiment stop rule.

## Color measurements and the provisional Delta E target

Use CIEDE2000 (Delta E 00), not Delta E 76 or raw RGB distance, with kL=kC=kH=1 unless a different documented application requires otherwise. Validate the implementation against Sharma, Wu and Dalal's published cases, especially zero-chroma and hue wraparound. The user's previously successful numeric setting is not confirmed; adopt **Delta E 00 < 3 as a provisional project target**, not a universal visibility guarantee or proof the earlier run used this exact statistic.

Report per region: pixel count, median, p95, maximum, and fraction >=3. The proposed initial summary target is p95<3 in each approved corresponding region; it becomes an acceptance rule only after the human accepts the masks, statistic and comparison conditions. This permits a tail, so always expose the tail/maximum and inspect its locations. For critical small regions (iris, eyelash, mouth detail), use separate masks and direct visual review; do not average them into skin. No whole-image average can overrule a visibly wrong feature. Store the chosen statistic; do not silently change it to make a result pass.

Compare registered render/reference image locations with fixed camera, lights, exposure, tone mapping and encoding. Use opaque interior palette masks for color diagnosis, plus separate alpha/edge/shadow masks/tests. Freeze masks before search. Do not shrink masks, exclude a failed area or warp the reference after looking at errors. Report segmentation and registration ambiguity. With screenshots of unknown lighting/grade, label the color result diagnostic and the original material parameters non-identifiable; do not force a numeric pass through altered albedo.

Bundled conversion accepts explicitly declared, display-referred standard sRGB [0,1], converts to linear sRGB then XYZ D65 then Lab using D65 reference white. It applies no ICC transform, OCIO, exposure, chromatic adaptation or tone mapping. Do not feed raw scene-linear EXR, HDR, Display P3 or ACES values into it. Convert both images through a known common display pipeline first and record that pipeline. This utility measures color samples; it does not identify texture roles or measure transparency/geometry.

CLI: `python3 "$PACK/scripts/math_tools.py" colors INPUT.json --output NEW_REPORT.json`. INPUT has encoding='display-srgb', matched_conditions_evidence=[actual nonempty file paths], and regions=[{name, reference_rgb:[[r,g,b],...], candidate_rgb:[[r,g,b],...]}]. Equal sample counts and explicit corresponding samples are required. Paths resolve relative to INPUT. Store pixel positions/mask hashes in the mathematical profile; exported samples must cover the declared region, not cherry-picked pixels. The CLI gives diagnostic summaries only and never issues stage acceptance. NumPy is required; no Blender API is used.

## 00 camera and reference calibration

Use annotated landmark reprojection residuals e_ij=project(K_j,R_j,t_j,X_i)-u_ij and bounded robust nonlinear least squares. Estimate only plausible camera degrees of freedom while freezing known geometry, pose, units and source identity. Fix scale/camera gauge freedoms explicitly; one image cannot uniquely recover focal length, depth and body scale. Use existing 3D correspondences rather than unnecessary full bundle adjustment. Weight observations by confidence; robust losses reduce outlier influence but do not authorize discarding mismatches. Report all landmark residuals in pixels, uncertainty and alternative plausible camera fits. Human confirms framing and landmarks at the existing 00 gate. Save fixed cameras/lighting for later measurements. Do not perform material fitting here.

## 01 import correspondence

Use stable source/import indices first. After documented axis conversion and scale, fit a proper rigid transform with known correspondences: min sum_i ||R p_i+t-q_i||^2, R^T R=I, det(R)=+1. math_tools.rigid_alignment returns R,t and residuals; for row vectors use p@R.T+t. It rejects collinear/degenerate data and does not allow reflection/scale. Record determinant, transforms, residual max and per-region errors. A wrong handedness or unexplained scale is a diagnostic fault, not a free fitting variable. Exact UV/topology/material checks remain separate. Do not use unconstrained nearest-neighbor ICP or nonrigid warping to hide lost features. Human reviews the loss report at 01.

## 02 material fitting

Complete the diagnostic ladder and verified role mapping first. Bound a small explicit block (e.g. existing tint or shadow threshold); do not search arbitrary graph topology or paint textures. Render in Cycles with fixed settings; evaluate regional Delta E and separate shadow/alpha/highlight/edge comparisons. Preserve already approved attributes as constraints. Use silhouette IoU=intersection/union and symmetric boundary distances when comparing registered masks; report resolution and mask definitions, and return not-applicable for empty required regions rather than divide by zero. Shadow boundaries often matter more than whole-image pixel loss for anime faces. If useful, take a bounded finite-difference sensitivity (E(theta+h)-E(theta-h))/(2h) with recorded step/seed/sample count and check that render noise is below the effect. Do not interpret noisy differences as reliable gradients. Human approves the pilot and any approximation at the existing 02 gate. Record metrics under material-mapping/cycles-comparisons evidence, not a new gate.

## 03 geometry and deformation

For explicitly approved geometry corrections, ARAP uses local edge preservation:

    E_ARAP = sum_(i,j) w_ij * ||(v'_i-v'_j)-R_i*(v_i-v_j)||^2,
    subject to approved handles, protected silhouette/face regions and correspondence.

It is an optional construction method, not a cleanup default or collision/volume guarantee. Preserve UVs, split normals, shape-key indices and intentional layers. Compare ordinary linear skinning with dual-quaternion/Preserve Volume alternatives for actual twist failures; none proves SDEF/QDEF equivalence. Pose-space corrective deformation is an option where weights alone cannot express the target. Compare evaluated poses and the neutral shape; displacement normalized by approved height H is ||p'-p||/H. Human accepts the isolated form and motion delta at 03; metrics cannot decide the character's design.

## 04 control rig and switching

Use bounded inverse kinematics/least squares to fit control transforms to approved target endpoints/orientations with joint limits and rest-space preservation. If a Jacobian solver is implemented, damped least-squares updates solve (J^T J+lambda^2 I) delta_q=J^T e; solve the system, do not explicitly invert it. Record coordinate conventions, unit scales, limits and damping; add rotational errors in a common frame and sensible units. Do not replace Blender's native solver merely to add this formula. Detect straight-limb pole degeneracy separately. Verify switched pose translation ||t_after-t_before||/H and quaternion angle 2*acos(clamp(abs(dot(q0,q1)),0,1)); normalized quaternions and the q/-q equivalence are required. Sample intermediate joints and keyed/interpolated frames, not only hand/foot endpoints. Human judges control behavior at 04; actual switching/runtime checks remain mandatory.

## 05 face and expression fitting

For known same-topology target shapes solve min ||W(Bw-d)||^2+lambda||w-w0||^2 with approved lower/upper bounds on shape weights. B contains existing shape deltas, d is a 3D target delta and W emphasizes declared regions; do not pretend 2D image coordinates are corresponding 3D vertices. Two-dimensional fitting needs projection and fixed camera or a nonlinear image objective. Never enforce sum(w)=1 on independent delta shape keys unless the chosen representation requires it. Preserve negative/overdrive ranges when explicitly approved. Pose Space Deformation/RBF methods can interpolate reviewed corrective samples in defined pose coordinates; extrapolation is unqualified until tested. Native shape keys/drivers remain the final portable representation. Human accepts expressive character and combination behavior at 05; retargeting is not proven by a low face fitting error.

## 06 qualification

Use test poses/views not used to tune the candidate, plus the approved fixed regression suite. Evaluate the mesh after modifiers/constraints. Report unit-normalized residual distributions, worst cases, switch errors, foot drift/contact, collision/collapse indicators and temporal discontinuities. Compare arrays directly with calibrated tolerances rather than hashes of rounded floats. Repeat representative cases to separate render/solver variation from a real regression; statistics do not prove all possible poses work. Fail hidden dependency, invalid numeric/driver/target and binding checks even if the beauty image looks good. Human sees the relevant clips/close-ups at 06. Keep existing check names.

## 07 final appearance

Reuse frozen camera/map/color definitions from 00/02; tune only the approved remaining look parameters. Use regional Delta E 00 target and boundary/silhouette metrics, plus optionally LPIPS on registered same-size crops with recorded model/version/normalization. LPIPS measures learned perceptual similarity, not anime identity, correct shader physics or a universal pass threshold. It is secondary; do not trade a wrong eye/palette for a better aggregate. Preferential line search can offer one parameter direction or up to three distinct alternatives with 'neither' available. Human approves the exact look under the existing 07 gate. Verify a held-out head turn/light condition before acceptance.

## 08 motion identification

Use inverse simulation only with target motion evidence or explicit reviewed stylized targets. Fit declared native solver parameters phi by minimizing sum_t,i w_i ||project(x_i_sim(phi,t))-u_i_ref(t)||^2 plus documented stretch/penetration/settling penalties; known 3D targets can be compared directly. Freeze the driving animation, camera, scale, gravity, timestep, reset and pre-roll, otherwise parameters are confounded. Match timing at the same scene timebase; do not time-warp a motion to hide lag unless the approved target explicitly permits it. For simple oscillation use omega_n=sqrt(k/m), zeta=c/(2sqrt(km)) as conceptual diagnostics; Blender solver coefficients are not interchangeable k/c values. XPBD is a separate compliant-constraint formulation, not a promise that Blender uses it or a direct conversion to Blender cloth settings. Keep final systems native/editable/unbaked. Human judges the motion feel at 08; actual cold reset/category suspension/manual fallback must still be demonstrated.

## 09 audit and acceptance

Keep separate quality, functionality, dependency and performance results; no single similarity percentage or combined score can accept the character. Use repeated timings and report variation, percentiles, longest stalls and cold/warm configuration. Do not call three repetitions a statistically established 95% guarantee, or claim headless frame stepping is UI throughput. Rank performance choices only among options meeting accepted fidelity and functional constraints. Human decisions are audit (including selected optimization disposition) and delivery (including re-audit and final acceptance), as specified in workflow.md. Use actual Cycles Rendered viewport with fixed sampling policy, not an alternate engine. Any asset/performance tradeoff requires the combined audit decision.

## Primary references

These establish methods; their application to this pack is an engineering design, not prior character validation.

- Ceres: bounded robust nonlinear least squares and outlier losses: https://ceres-solver.readthedocs.io/latest/nnls_tutorial.html
- Sorkine-Hornung/Rabinovich, Least-Squares Rigid Motion Using SVD: https://igl.ethz.ch/projects/ARAP/svd_rot.pdf
- Mitsuba inverse rendering (external renderer; no automatic Cycles derivative): https://mitsuba.readthedocs.io/en/stable/src/inverse_rendering/gradient_based_opt.html
- Sharma/Wu/Dalal (2005), CIEDE2000 implementation and published tests: https://hajim.rochester.edu/ece/sites/gsharma/ciede2000/
- Sorkine/Alexa (SGP 2007), ARAP: https://igl.ethz.ch/projects/ARAP/
- Kavan et al. (TOG 2008), dual-quaternion skinning and limitations: https://users.cs.utah.edu/~ladislav/dq/index.html
- Lewis/Cordner/Fong (SIGGRAPH 2000), Pose Space Deformation: https://doi.org/10.1145/344779.344862
- SciPy bounded linear least squares: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.lsq_linear.html
- Zhang et al. (CVPR 2018), LPIPS: https://richzhang.github.io/PerceptualSimilarity/
- Koyama et al. (SIGGRAPH 2017), human-guided Sequential Line Search: https://koyama.xyz/project/sequential_line_search/
- Astudillo/Frazier (AISTATS 2020), multi-attribute preference learning: https://proceedings.mlr.press/v108/astudillo20a.html
- Bhat et al. (SCA 2003), cloth parameter identification from video: https://graphics.cs.cmu.edu/projects/clothparameters/
- Macklin/Mueller/Chentanez (MiG 2016), XPBD: https://mmacklin.com/xpbd.pdf
- NIST measurement uncertainty: https://www.nist.gov/itl/sed/topic-areas/measurement-uncertainty
