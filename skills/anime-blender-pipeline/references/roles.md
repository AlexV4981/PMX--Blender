# Role dispatch

| Role | Requested selection | Responsibility |
| --- | --- | --- |
| Orchestrator | gpt-6.1-sol / high | Assign work, enforce ownership, evaluate evidence and request human decisions |
| Routine worker | gpt-6.1-sol / low, Light in supporting clients | Run proven scripts, apply approved settings and collect tests |
| Difficult implementation | gpt-6.1-sol / high | Solve unfamiliar deformation, shader and solver problems |
| Escalation | gpt-6-astra / high when exposed; record actual effort | Investigate inability to produce a usable candidate |
| Acceptance | Human running the pipeline | Select/critique candidates and accept stages/exceptions |

1. Verify exposed delegation/model settings; never claim a model ran unless it actually did.
2. Use assets/worker-task.template.json: stage, input digest, objective, allowed/forbidden edits, relevant references, outputs and stop conditions. Do not send every worker the whole conversation or pack.
3. Give each worker private assets. Keep one writer to any live Blender session/.blend/image file. Parallelize independent research or static reports only when useful.
4. Return compact changes, command records, evidence paths, failures and assumptions. Avoid High repeating successful worker actions. Use scripts rather than LLM loops per vertex/object.
5. Diagnose routine failures with High; refine scope or implement a new method. Escalate to Astra if no usable candidate can be produced, supplying actual files and failed methods.
6. If Astra fails or is unavailable, stop that branch and offer actionable experiments with expected consequences and missing evidence for human selection.
7. Keep candidate caps, dependency attempts and model effort separate. Never force Light through ten incapable retries or manufacture ten variants.

This is dispatch policy, not a guaranteed universal Codex setting. Apply actual model/effort configuration through the available surface. Disclose inability to configure a requested role and use available capability honestly.

## Native custom-agent profiles

Use the supplied assets/codex-agents TOML files when the current local Codex supports the documented standalone custom-agent format. During project setup, copy them to the project's .codex/agents directory if absent; compare existing files instead of overwriting user configuration. They select Sol Light, Sol High and Astra High for named subagents. Select Sol High for the parent session separately; copying a worker profile does not change an already-running parent model. Where the surface exposes explicit model/effort arguments instead, use those and record actual selections.

Do not change global model defaults, permissions, provider, API keys or MCP settings merely to install these skills. The profiles inherit session permissions and cannot grant extra access. Verify model availability at execution time.


## Version 2 task boundary

Routine means a proven script or exact accepted recipe with known input checks and observable outputs. Texture classification, unfamiliar shader construction, rest-space conversion and novel solver architecture require implementation judgment. Assign those to the capable role, then use routine workers for bounded application/collection. Include fault hypotheses, distinguishing test and rollback path in the task record. Stop after two consecutive non-improving experiments and return evidence for renewed diagnosis; do not manufacture ten technical approaches or three designs as quotas.
