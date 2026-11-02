#!/usr/bin/env python3
"""Bootstrap the portable helper inside an existing project (Python stdlib only)."""
import argparse
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
from urllib.request import urlopen

DEFAULT_MODEL = "qwen2.5-coder:7b-instruct-q4_K_M"
EXTENSIONS = [".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs"]
CONVENTIONAL = ("src", "lib", "scripts", "tests", "test", "app", "cmd", "internal")

def detect_checks(root):
    package = root / "package.json"
    if (root / "Cargo.toml").exists():
        return [["cargo", "test"]]
    if (root / "go.mod").exists():
        return [["go", "test", "./..."]]
    if package.exists():
        try:
            script = json.loads(package.read_text(encoding="utf-8")).get("scripts", {}).get("test", "")
            if script and "no test specified" not in script:
                return [["npm", "test"]]
        except (ValueError, OSError, TypeError):
            pass
    if any((root / key).exists() for key in ("pytest.ini", "tox.ini")) or (
            (root / "pyproject.toml").exists() and (root / "tests").exists()):
        return [[sys.executable, "-m", "pytest", "-q"]]
    if (root / "tests").is_dir():
        return [[sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]]
    return []

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--project", type=Path, default=Path.cwd())
    p.add_argument("--allow", action="append", help="Allowed relative source directories, repeatable")
    p.add_argument("--check", action="append", help="Test command, repeatable, e.g. 'python -m pytest -q'")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--force-config", action="store_true")
    p.add_argument("--force-skill", action="store_true")
    p.add_argument("--github-alert", action="store_true")
    p.add_argument("--doctor", action="store_true")
    args = p.parse_args(argv)
    root = args.project.resolve()
    helper = root / "qwen-helper"
    if not (helper / "local_worker.py").is_file() or not (helper / "CODEX_SKILL.md").is_file():
        p.error("Copy the complete qwen-helper directory to the project root first")
    if args.doctor:
        print("Python:", sys.version.split()[0])
        print("Ollama CLI:", shutil.which("ollama") or "not found")
        try:
            with urlopen("http://127.0.0.1:11434/api/tags", timeout=2) as res:
                tags = json.loads(res.read().decode())
            found = [m.get("name") for m in tags.get("models", [])]
            print("Ollama local server: reachable; model tag present:", args.model in found)
        except Exception as exc:
            print("Ollama local server: unavailable:", exc)
        return 0

    config_file = helper / "project.json"
    if config_file.exists() and not args.force_config:
        print("Keeping existing configuration:", config_file)
    else:
        allow = args.allow or [s for s in CONVENTIONAL if (root / s).is_dir()]
        if not allow:
            p.error("Cannot infer allowed source directories: provide --allow")
        for name in allow:
            location = (root / name).resolve()
            if name.startswith(".") or name == "qwen-helper" or not location.is_dir() or not location.is_relative_to(root):
                p.error("Invalid --allow (must be an existing unhidden project directory): " + name)
        commands = [shlex.split(c) for c in args.check] if args.check else detect_checks(root)
        if not commands or any(not c for c in commands):
            p.error("No test command identified. Pass --check 'your project tests' (required)")
        cfg = {"version": 1, "model": args.model,
               "ollama_url": "http://127.0.0.1:11434/api/generate",
               "allow_paths": allow, "deny_paths": [], "extensions": EXTENSIONS,
               "checks": commands,
               "limits": {"max_references": 1, "max_file_bytes": 5500,
                          "max_input_chars": 9200, "max_output_bytes": 6500,
                          "context_tokens": 4096, "output_tokens": 1536,
                          "test_timeout_seconds": 180}}
        config_file.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
        print("Wrote:", config_file)
    skill = root / ".agents" / "skills" / "qwen-local-helper" / "SKILL.md"
    if not skill.exists() or args.force_skill:
        skill.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(helper / "CODEX_SKILL.md", skill)
        print("Installed Codex skill:", skill)
    else:
        print("Keeping existing skill:", skill)
    if args.github_alert:
        workflow = root / ".github" / "workflows" / "qwen-helper.yml"
        if workflow.exists():
            print("Keeping existing GitHub workflow:", workflow)
        else:
            workflow.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(helper / "github-alert.template.yml", workflow)
            print("Installed optional GitHub issue alert:", workflow)
    print("Next: run python qwen-helper/setup.py --doctor, then start Codex in this project.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
