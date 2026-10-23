#!/usr/bin/env python3
"""Read-only bounded PMX inventory. No Blender/importer dependency or repairs.

PMX 2.0 sections are parsed. PMX 2.1 soft-body count is reported, but nonzero
soft-body payloads are explicitly partial; never count this as full support.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import struct
import sys


class FormatError(Exception):
    pass


class Reader:
    def __init__(self, data):
        self.data = memoryview(data)
        self.offset = 0
        self.widths = {}
        self.encoding = "utf-8"

    def take(self, n):
        if n < 0 or self.offset + n > len(self.data):
            raise FormatError(f"Truncated or invalid PMX at byte {self.offset}")
        value = self.data[self.offset:self.offset+n]
        self.offset += n
        return value

    def value(self, fmt):
        return struct.unpack("<"+fmt, self.take(struct.calcsize("<"+fmt)))[0]

    def count(self, label):
        n = self.value("i")
        if n < 0 or n > 20_000_000 or n > len(self.data):
            raise FormatError(f"Implausible {label} count {n}")
        return n

    def text(self):
        n = self.count("string bytes")
        try:
            return bytes(self.take(n)).decode(self.encoding, errors="strict")
        except UnicodeError as e:
            raise FormatError(f"Invalid {self.encoding} string at byte {self.offset-n}") from e

    def index(self, kind):
        size = self.widths[kind]
        fmt = {1: "B", 2: "H", 4: "I"} if kind == "vertex" else {1: "b", 2: "h", 4: "i"}
        return self.value(fmt[size])

    def floats(self, n):
        return struct.unpack("<"+"f"*n, self.take(4*n))

    def names(self):
        return {"name_jp": self.text(), "name_en": self.text()}


def inventory(path):
    path = Path(path).resolve()
    data = path.read_bytes()
    r = Reader(data)
    if bytes(r.take(4)) != b"PMX ":
        raise FormatError("Not a PMX file")
    version = r.value("f")
    if not (abs(version-2.0)<1e-5 or abs(version-2.1)<1e-5):
        raise FormatError(f"Unsupported PMX version {version}")
    header = bytes(r.take(r.value("B")))
    if len(header) < 8 or header[0] not in (0, 1) or header[1] > 4:
        raise FormatError("Unsupported PMX global header")
    r.encoding = "utf-16-le" if header[0] == 0 else "utf-8"
    adduv = header[1]
    for k, n in zip(["vertex", "texture", "material", "bone", "morph", "rigid"], header[2:8]):
        if n not in (1, 2, 4): raise FormatError(f"Invalid {k} index width {n}")
        r.widths[k] = n
    result = {"schema_version": 1, "source": str(path), "sha256": hashlib.sha256(data).hexdigest(),
              "bytes": len(data), "pmx_version": round(version, 1), "encoding": r.encoding,
              "additional_uv_count": adduv, "header_extra_bytes": len(header)-8,
              "model": r.names(), "comments": r.names(), "issues": []}
    count = r.count("vertices")
    deform = Counter()
    nonfinite = bad_weights = 0
    for _ in range(count):
        values = r.floats(8+4*adduv)
        nonfinite += any(not math.isfinite(x) for x in values)
        t = r.value("B")
        if t == 0:
            r.index("bone"); w = [1.0]
        elif t in (1, 3):
            r.index("bone"); r.index("bone"); w0 = r.value("f"); w = [w0, 1.0-w0]
            if t == 3: r.take(36)
        elif t in (2, 4):
            for _ in range(4): r.index("bone")
            w = r.floats(4)
        else:
            raise FormatError(f"Unsupported deform type {t}")
        bad_weights += any(not math.isfinite(x) or x < 0 or x > 1 for x in w) or abs(sum(w)-1)>1e-4
        deform[{0:"BDEF1",1:"BDEF2",2:"BDEF4",3:"SDEF",4:"QDEF"}[t]] += 1
        r.take(4)  # Per-vertex edge scale remains in source.
    result["vertices"] = {"count": count, "deform_types": dict(deform),
                          "nonfinite_position_normal_uv_records": nonfinite,
                          "invalid_deform_weight_records": bad_weights}
    indices = r.count("face indices")
    r.take(indices*r.widths["vertex"])
    result["face_indices"] = indices
    if indices % 3: result["issues"].append("Face-index count is not divisible by three")
    textures = []
    for _ in range(r.count("textures")):
        name = r.text()
        candidate = (path.parent / name.replace("\\", "/")).resolve()
        textures.append({"source_name": name, "resolved_path": str(candidate),
                         "exists": candidate.is_file(), "outside_model_directory": not candidate.is_relative_to(path.parent)})
    result["textures"] = textures
    materials = []
    for i in range(r.count("materials")):
        m = {"source_index": i, **r.names()}
        m["diffuse_rgba"] = r.floats(4); m["specular_rgb"] = r.floats(3)
        m["specular_power"] = r.value("f"); m["ambient_rgb"] = r.floats(3)
        flags = r.value("B")
        m["flags_raw"] = flags
        m["flags"] = {name: bool(flags & (1<<bit)) for bit, name in enumerate([
            "double_sided", "ground_shadow", "self_shadow_map", "self_shadow", "edge", "vertex_color", "point", "line"])}
        m["edge_rgba"] = r.floats(4); m["edge_size"] = r.value("f")
        m["texture_index"] = r.index("texture"); m["sphere_texture_index"] = r.index("texture")
        m["sphere_mode"] = r.value("B"); shared = r.value("B")
        if shared not in (0,1): raise FormatError("Invalid shared-toon flag")
        m["shared_toon"] = bool(shared)
        m["toon_index"] = r.value("B") if shared else r.index("texture")
        m["memo"] = r.text(); m["face_index_count"] = r.count("material face indices")
        materials.append(m)
    result["materials"] = materials
    if sum(m["face_index_count"] for m in materials) != indices:
        result["issues"].append("Material face-index totals disagree with mesh")
    bones = []
    for i in range(r.count("bones")):
        b = {"source_index": i, **r.names(), "position": r.floats(3), "parent": r.index("bone"),
             "transform_layer": r.value("i"), "flags_raw": r.value("H")}
        flags = b["flags_raw"]
        b["tail"] = {"bone": r.index("bone")} if flags & 1 else {"offset": r.floats(3)}
        if flags & 0x300: b["grant"] = {"parent": r.index("bone"), "ratio": r.value("f"),
                                        "rotation": bool(flags & 0x100), "translation": bool(flags & 0x200)}
        if flags & 0x400: b["fixed_axis"] = r.floats(3)
        if flags & 0x800: b["local_axes"] = {"x": r.floats(3), "z": r.floats(3)}
        if flags & 0x2000: b["external_parent_key"] = r.value("i")
        if flags & 0x20:
            ik = {"target": r.index("bone"), "iterations": r.value("i"), "angle_limit": r.value("f"), "links": []}
            for _ in range(r.count("IK links")):
                link = {"bone": r.index("bone"), "limited": bool(r.value("B"))}
                if link["limited"]: link.update(lower=r.floats(3), upper=r.floats(3))
                ik["links"].append(link)
            b["ik"] = ik
        bones.append(b)
    result["bones"] = bones
    morphs = []
    for i in range(r.count("morphs")):
        m = {"source_index": i, **r.names(), "panel": r.value("B"), "type": r.value("B"), "offset_count": r.count("morph offsets")}
        t = m["type"]
        if t in (9,10) and result["pmx_version"] < 2.1: result["issues"].append("PMX 2.1 morph in a 2.0 file")
        sizes = {0: r.widths["morph"]+4, 1: r.widths["vertex"]+12,
                 2: r.widths["bone"]+28, **{k:r.widths["vertex"]+16 for k in range(3,8)},
                 8:r.widths["material"]+1+112, 9:r.widths["morph"]+4, 10:r.widths["rigid"]+1+24}
        if t not in sizes: raise FormatError(f"Unsupported morph type {t}")
        r.take(sizes[t]*m["offset_count"])
        morphs.append(m)
    result["morphs"] = morphs
    frames = []
    for _ in range(r.count("display frames")):
        f = {**r.names(), "special": r.value("B"), "elements": []}
        for _ in range(r.count("display elements")):
            t = r.value("B")
            if t not in (0,1): raise FormatError("Unknown display element")
            f["elements"].append({"type": t, "index": r.index("bone" if t == 0 else "morph")})
        frames.append(f)
    result["display_frames"] = frames
    bodies = []
    for i in range(r.count("rigid bodies")):
        b = {"source_index": i, **r.names(), "bone": r.index("bone"),
             "group": r.value("B"), "noncollision_mask": r.value("H"), "shape": r.value("B"),
             "size": r.floats(3), "position": r.floats(3), "rotation": r.floats(3),
             "mass": r.value("f"), "linear_damping": r.value("f"), "angular_damping": r.value("f"),
             "restitution": r.value("f"), "friction": r.value("f"), "mode": r.value("B")}
        bodies.append(b)
    result["rigid_bodies"] = bodies
    joints = []
    for i in range(r.count("joints")):
        j = {"source_index": i, **r.names(), "type": r.value("B"),
             "body_a": r.index("rigid"), "body_b": r.index("rigid")}
        if j["type"] not in range(6): raise FormatError("Unknown joint type")
        for key in ["position", "rotation", "translation_lower", "translation_upper", "rotation_lower", "rotation_upper", "translation_spring", "rotation_spring"]:
            j[key] = r.floats(3)
        joints.append(j)
    result["joints"] = joints
    soft = r.count("soft bodies") if result["pmx_version"] >= 2.1 else 0
    result["soft_body_count"] = soft
    result["unparsed_bytes"] = len(data)-r.offset
    result["inventory_status"] = "complete" if soft == 0 and r.offset == len(data) else "partial"
    if soft: result["issues"].append("Nonzero PMX 2.1 soft-body payload requires manual/specialist inventory")
    if result["unparsed_bytes"] and not soft: result["issues"].append("Unexpected trailing data; investigate before approving inventory")
    return result


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("pmx"); p.add_argument("--output")
    args = p.parse_args(argv)
    try:
        result = inventory(args.pmx)
        value = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False)+"\n"
        if args.output:
            target = Path(args.output)
            if target.resolve() == Path(args.pmx).resolve(): raise FormatError("Never overwrite the source")
            target.parent.mkdir(parents=True, exist_ok=True); target.write_text(value, encoding="utf-8")
        else: print(value, end="")
        return 0 if result["inventory_status"] == "complete" else 3
    except (FormatError, OSError, ValueError, OverflowError) as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr); return 2


if __name__ == "__main__":
    raise SystemExit(main())
