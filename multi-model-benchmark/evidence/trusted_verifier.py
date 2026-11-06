"""TRUSTED verification phase. Never executes candidate Python.

Run in a NEW Blender process/container with --disable-autoexec. Candidate's
.blend and result.json are read-only untrusted inputs. The verdict is written to
an entirely separate host output mount not present in the candidate container.
"""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import traceback


def strict_result_json(text):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("Duplicate result key")
            result[key] = value
        return result
    def bad(value):
        raise ValueError("Nonfinite result number")
    def number(value):
        result = float(value)
        if not math.isfinite(result):
            bad(value)
        return result
    return json.loads(text, object_pairs_hook=pairs, parse_constant=bad, parse_float=number)


def validate_motion_samples(result):
    for sample in result.get("samples", []):
        values = [sample.get("angle_deg")] + list(sample.get("tip", []))
        if len(values) != 4 or any(type(v) not in (int, float) or not math.isfinite(v) for v in values):
            raise ValueError("Motion samples must contain finite numeric values")


def finite_object(obj):
    def check(values):
        if any(not math.isfinite(v) for v in values):
            raise ValueError("Nonfinite Blender data")
    for row in obj.matrix_world:
        check(row)
    if obj.type == "MESH":
        for vertex in obj.data.vertices:
            check(vertex.co)
            check(g.weight for g in vertex.groups)
        if obj.data.shape_keys:
            for key in obj.data.shape_keys.key_blocks:
                check([key.value])
                for point in key.data:
                    check(point.co)
    if obj.type == "ARMATURE":
        for bone in obj.data.bones:
            check(bone.head_local); check(bone.tail_local)
        for bone in obj.pose.bones:
            check(bone.rotation_euler)
            for constraint in bone.constraints:
                check([constraint.influence])
                if constraint.target:
                    for row in constraint.target.matrix_world:
                        check(row)


def fixture_hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()


def protected_state(obj):
    """Independent protected geometry/rest state; only task-specific changes allowed."""
    state = {"matrix_local": tuple(tuple(row) for row in obj.matrix_local),
             "matrix_world": tuple(tuple(row) for row in obj.matrix_world),
             "parent": obj.parent.name if obj.parent else None,
             "modifiers": tuple((m.name, m.type) for m in obj.modifiers),
             "constraints": tuple((c.name, c.type) for c in obj.constraints)}
    if obj.type == "MESH":
        state.update(
            positions=tuple(tuple(v.co) for v in obj.data.vertices),
            edges=tuple(tuple(e.vertices) for e in obj.data.edges),
            polygons=tuple(tuple(p.vertices) for p in obj.data.polygons),
            uv_layers=tuple((layer.name, tuple(tuple(item.uv) for item in layer.data))
                            for layer in obj.data.uv_layers),
            materials=tuple(m.name if m else None for m in obj.data.materials),
            groups=tuple((g.name, g.lock_weight) for g in obj.vertex_groups),
            keys=tuple((key.name, tuple(tuple(v.co) for v in key.data))
                       for key in obj.data.shape_keys.key_blocks) if obj.data.shape_keys else ())
    elif obj.type == "ARMATURE":
        state['bones'] = tuple((b.name, tuple(tuple(row) for row in b.matrix_local),
                                b.parent.name if b.parent else None, b.use_connect, b.use_deform)
                               for b in obj.data.bones)
    return state


def check_ik_response(obj):
    import bpy
    lower = obj.pose.bones['Forearm_L']
    constraints = [c for c in lower.constraints if c.type == 'IK']
    if len(constraints) != 1:
        raise ValueError('Exactly one pilot IK constraint required')
    constraint = constraints[0]
    if constraint.mute or abs(constraint.influence - 1.0) > 1e-6:
        raise ValueError('IK constraint must be enabled with full influence')
    target = constraint.target
    if target is None:
        raise ValueError('IK target missing')
    original = target.matrix_world.copy()
    try:
        bpy.context.view_layer.update()
        initial = obj.matrix_world @ lower.tail
        root = obj.matrix_world @ obj.pose.bones['UpperArm_L'].head
        desired = root + (initial - root) * 0.9
        changed = original.copy(); changed.translation = desired
        target.matrix_world = changed
        bpy.context.view_layer.update()
        measured = obj.matrix_world @ lower.tail
        if any(not math.isfinite(v) for v in measured):
            raise ValueError('Nonfinite evaluated IK tip')
        if (measured - initial).length < 1e-4 or (measured - desired).length > 2e-3:
            raise ValueError('IK did not follow independently moved target')
    finally:
        target.matrix_world = original
        bpy.context.view_layer.update()


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
        protected_before = protected_state(baseline)
        raw_result = strict_result_json(Path("/candidate_artifacts/result.json").read_text(encoding="utf-8"))
        if case["stage"] == "06":
            validate_motion_samples(raw_result)
        # --disable-autoexec is required in the Docker argv; no candidate scripts
        # are imported by this process. Open the saved derivative as untrusted data.
        bpy.ops.wm.open_mainfile(filepath="/candidate_artifacts/candidate.blend",
                                load_ui=False, use_scripts=False)
        name = {"03": "RepairMesh", "04": "ArmaturePilot", "05": "FaceMesh",
                "06": "MotionArm"}[case["stage"]]
        obj = bpy.data.objects.get(name)
        if obj is None:
            raise RuntimeError("Required source object missing from candidate derivative")
        finite_object(obj)
        if protected_state(obj) != protected_before:
            raise ValueError('Geometry, MASK, or shape keys changed: protected topology, transforms or rest data')
        if case["stage"] == "05":
            controller = bpy.data.objects.get("CTRL_Face")
            if controller is not None:
                for key in case["params"]["keys"]:
                    for value in (0.0, 0.5, 1.0):
                        controller[key] = value
                        bpy.context.view_layer.update()
                        deps = bpy.context.evaluated_depsgraph_get()
                        measured = obj.evaluated_get(deps).data.shape_keys.key_blocks[key].value
                        if not math.isfinite(measured):
                            raise ValueError("Nonfinite evaluated driver")
                    controller[key] = 0.0
        good, reason = oracle.validate(bpy.context.scene, obj, case, before, raw_result)
        if good and case["stage"] == "04":
            check_ik_response(obj)
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
