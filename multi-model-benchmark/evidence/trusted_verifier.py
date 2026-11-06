"""TRUSTED verification phase. Never executes candidate Python.

Run in a NEW Blender process/container with --disable-autoexec. Candidate's
.blend and result.json are read-only untrusted inputs. The verdict is written to
an entirely separate host output mount not present in the candidate container.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import traceback


def fixture_hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()


def main():
    import bpy
    src = Path("/lab/candidate.py").read_bytes()
    case = json.loads(Path("/lab/case.json").read_text(encoding="utf-8"))
    case_sha = fixture_hash(case)
    code_sha = hashlib.sha256(src).hexdigest()
    oracle_bytes = Path("/lab/oracle.py").read_bytes()
    oracle_sha = hashlib.sha256(oracle_bytes).hexdigest()
    result = {"verifier_phase": "fresh_process_no_candidate_exec", "blender_executed": True,
              "source_sha256": code_sha, "fixture_sha256": case_sha,
              "oracle_sha256": oracle_sha, "case_id": case["case_id"],
              "stage": case["stage"], "blender_pass": False, "oracle_detail": "", "error_feedback": ""}
    try:
        spec = importlib.util.spec_from_file_location("trusted_oracle", "/lab/oracle.py")
        oracle = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(oracle)
        if not case.get("synthetic") or case["stage"] not in ("03", "04", "05", "06"):
            raise RuntimeError("Unsupported fixture")
        # Independently construct the baseline and its protected-state snapshot.
        baseline = oracle.setup_stage(bpy.context.scene, case)
        before = oracle.snapshot(case["stage"], baseline, case)
        raw_result = json.loads(Path("/candidate_artifacts/result.json").read_text(encoding="utf-8"))
        # --disable-autoexec is required in the Docker argv; no candidate scripts
        # are imported by this process. Open the saved derivative as untrusted data.
        bpy.ops.wm.open_mainfile(filepath="/candidate_artifacts/candidate.blend",
                                load_ui=False, use_scripts=False)
        name = {"03": "RepairMesh", "04": "ArmaturePilot", "05": "FaceMesh",
                "06": "MotionArm"}[case["stage"]]
        obj = bpy.data.objects.get(name)
        if obj is None:
            raise RuntimeError("Required source object missing from candidate derivative")
        good, reason = oracle.validate(bpy.context.scene, obj, case, before, raw_result)
        result["blender_pass"] = bool(good)
        result["oracle_detail"] = str(reason)[:2000]
        if not good:
            result["error_feedback"] = str(reason)[:2000]
    except Exception as exc:
        result["oracle_detail"] = "Trusted verifier error: " + str(exc)[:1000]
        result["error_feedback"] = traceback.format_exc()[-2500:]
    Path("/trusted_out/oracle.json").write_text(json.dumps(result, sort_keys=True), encoding="utf-8")
    # A test failure has exit 0: the trusted verifier ran successfully and
    # returned an actual FAIL. Infrastructural crashes/no output are BLOCKED.
    return 0


if __name__ == "__main__":
    sys.exit(main())
