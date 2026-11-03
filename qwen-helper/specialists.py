"""Fail-closed eligibility for separately trained, single-purpose local Qwen workers."""
import json
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
REGISTRY = HERE / "specialists.json"
MANIFESTS = HERE / "qualifications"
TARGET_DIR = "skills/anime-blender-pipeline/scripts"

class Ineligible(ValueError):
    pass

def registry():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if data.get("version") != 1 or not isinstance(data.get("specialists"), dict):
        raise Ineligible("Invalid specialist registry")
    return data

def inspect(task, require_qualified=True):
    if not isinstance(task, dict):
        raise Ineligible("Invalid task")
    name = task.get("specialist")
    if not isinstance(name, str) or name not in registry()["specialists"]:
        raise Ineligible("Task has no registered specialist; use original Codex pipeline")
    spec = registry()["specialists"][name]
    if (task.get("scope", "generic") != spec["scope"] or task.get("kind") != spec["kind"]
            or task.get("cross_subsystem") or task.get("requires_visual_judgment")):
        raise Ineligible("Task outside narrow local specialization")
    target = task.get("target")
    if not isinstance(target, str) or "\\" in target:
        raise Ineligible("Invalid target")
    path = PurePosixPath(target)
    if (path.parent.as_posix() != TARGET_DIR or not path.name.startswith(spec["filename_prefix"])
            or path.suffix != ".py" or ".." in path.parts):
        raise Ineligible("Specialist can only create an approved standalone Python helper")
    if task.get("character_id") or task.get("character_requirements"):
        raise Ineligible("Character-specific requirements stay with the original pipeline")
    if require_qualified:
        if spec.get("qualified") is not True:
            raise Ineligible("Specialist has not passed held-out qualification")
        manifest = MANIFESTS / (name + ".json")
        if not manifest.is_file():
            raise Ineligible("Missing independent qualification evidence")
        evidence = json.loads(manifest.read_text(encoding="utf-8"))
        policy = registry()["qualification"]
        if (evidence.get("specialist") != name or evidence.get("model") != spec["model"]
                or evidence.get("passed_cases", 0) < policy["minimum_independent_holdout"]
                or evidence.get("failed_cases") != 0
                or evidence.get("sol_light_reviewed") is not True
                or not evidence.get("model_digest")
                or not evidence.get("training_set_sha256")
                or not evidence.get("holdout_set_sha256")
                or evidence["training_set_sha256"] == evidence["holdout_set_sha256"]):
            raise Ineligible("Qualification evidence invalid or stale")
    return {"name": name, **spec}

def model_for_task(task, default_model):
    if "specialist" not in task:
        return default_model  # Existing legacy/manual helper is unchanged.
    return inspect(task)["model"]
