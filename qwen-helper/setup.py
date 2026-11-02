#!/usr/bin/env python3
"""Install project-local Qwen skill for the PMX-to-native-Blender pipeline only."""
import argparse
import json
from pathlib import Path
import shutil
import sys
from urllib.request import urlopen

PACK = "skills/anime-blender-pipeline"
SOURCE = PACK + "/scripts"
MODEL = "qwen2.5-coder:7b-instruct-q4_K_M"
DENIED = ["pipeline.py", "blender_tools.py", "math_tools.py", "pmx_inventory.py"]

def is_pmx_project(root):
    return (root / PACK / "SKILL.md").is_file() and (root / SOURCE / "pipeline.py").is_file()

def pmx_defaults(model=MODEL):
    return {"version": 1, "project_type": "pmx-to-native-blender", "model": model,
        "ollama_url": "http://127.0.0.1:11434/api/generate",
        "default_task_scope": "generic",
        "allow_paths": [SOURCE],
        "deny_paths": [SOURCE + "/" + name for name in DENIED],
        "extensions": [".py"],
        "checks": [
            ["python", "-m", "unittest", "discover", "-s", SOURCE + "/tests", "-v"],
            ["python", SOURCE + "/blender_tools.py", "validate-seeds"]],
        "limits": {"max_references": 1, "max_file_bytes": 5500,
                   "max_input_chars": 9200, "max_output_bytes": 6500,
                   "context_tokens": 4096, "output_tokens": 1536,
                   "test_timeout_seconds": 180}}

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--project", type=Path, default=Path.cwd())
    p.add_argument("--model", default=MODEL, help="Local Qwen coding model; not the PMX character model")
    p.add_argument("--doctor", action="store_true")
    p.add_argument("--force-config", action="store_true")
    p.add_argument("--force-skill", action="store_true")
    p.add_argument("--github-alert", action="store_true")
    args = p.parse_args(argv)
    root = args.project.resolve()
    helper = root / "qwen-helper"
    if not is_pmx_project(root):
        p.error("Only a PMX-to-native-Blender pipeline checkout is supported")
    if not (helper / "local_worker.py").is_file() or not (helper / "CODEX_SKILL.md").is_file():
        p.error("Missing complete qwen-helper directory")
    config_file = helper / "project.json"
    if args.doctor:
        print("PMX pipeline: detected")
        print("Python:", sys.version.split()[0])
        print("Ollama CLI:", shutil.which("ollama") or "not found")
        wanted = args.model
        if config_file.is_file():
            wanted = json.loads(config_file.read_text(encoding="utf-8")).get("model", wanted)
        try:
            with urlopen("http://127.0.0.1:11434/api/tags", timeout=2) as response:
                models = json.loads(response.read().decode("utf-8")).get("models", [])
            print("Ollama server: connected; model installed:", wanted in {x.get("name") for x in models})
        except (OSError, ValueError) as e:
            print("Ollama server: unavailable:", e)
        return 0
    if config_file.exists() and not args.force_config:
        cfg = json.loads(config_file.read_text(encoding="utf-8"))
        if cfg.get("project_type") != "pmx-to-native-blender":
            p.error("Existing config is not PMX-specific; inspect before --force-config")
        print("Preserved:", config_file)
    else:
        config_file.write_text(json.dumps(pmx_defaults(args.model), indent=2) + "\n", encoding="utf-8")
        print("Created PMX-specific config:", config_file)
    skill = root / ".agents" / "skills" / "qwen-local-helper" / "SKILL.md"
    if not skill.exists() or args.force_skill:
        skill.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(helper / "CODEX_SKILL.md", skill)
        print("Installed repository-local skill:", skill)
    else:
        print("Preserved repository-local skill:", skill)
    if args.github_alert:
        target = root / ".github" / "workflows" / "qwen-helper.yml"
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(helper / "github-alert.template.yml", target)
            print("Installed GitHub alert:", target)
        else:
            print("Preserved existing GitHub alert:", target)
    print("Next: run python qwen-helper/setup.py --doctor")
    return 0

if __name__ == "__main__":
    sys.exit(main())
