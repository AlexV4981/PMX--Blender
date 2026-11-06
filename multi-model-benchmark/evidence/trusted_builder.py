"""UNTRUSTED phase. Runs a candidate in a disposable Blender container.

Anything written under /candidate_out is untrusted and MUST be verified in an
independent Blender process. No data from this process can grant a pass.
"""
import importlib.util
import json
from pathlib import Path
import sys


def main():
    import bpy
    spec = importlib.util.spec_from_file_location("synthetic_fixture", "/lab/oracle.py")
    oracle = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(oracle)
    case = json.loads(Path("/lab/case.json").read_text(encoding="utf-8"))
    if case.get("stage") not in ("03", "04", "05", "06") or not case.get("synthetic"):
        raise RuntimeError("Unsupported synthetic fixture")
    scene = bpy.context.scene
    oracle.setup_stage(scene, case)
    script = Path("/lab/candidate.py").read_text(encoding="utf-8")
    scope = {"__builtins__": __builtins__, "__name__": "__candidate__"}
    # This is intentionally untrusted: execution occurs with no network, credentials,
    # real PMX files, ledger, or user files mounted into this disposable container.
    exec(compile(script, "/lab/candidate.py", "exec"), scope)
    solve = scope.get("solve")
    if not callable(solve):
        raise RuntimeError("Candidate must implement solve(scene)")
    result = solve(scene)
    out = Path("/candidate_out")
    # The candidate can alter these artifacts. They are NEVER used as a trusted verdict.
    bpy.ops.wm.save_as_mainfile(filepath=str(out / "candidate.blend"), compress=False)
    try:
        (out / "result.json").write_text(json.dumps(result, allow_nan=False), encoding="utf-8")
    except (TypeError, ValueError):
        raise RuntimeError("Candidate returned non-JSON-serializable result")
    return 0


if __name__ == "__main__":
    sys.exit(main())
