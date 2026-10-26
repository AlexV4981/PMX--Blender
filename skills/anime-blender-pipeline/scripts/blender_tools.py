#!/usr/bin/env python3
"""Read-only Blender probes/fingerprints and deterministic seed-library builder.

Run with Blender --background --factory-startup --disable-autoexec [FILE.blend]
--python THIS_SCRIPT -- inspect|probe|build-seeds --output PATH.
Outside Blender only validate-seeds and --help work. Live Blender qualification
is required; successful static/pure-Python tests do not qualify .blend results.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

PACK = Path(__file__).resolve().parents[1]


def sha_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for c in iter(lambda: f.read(1024*1024), b""): h.update(c)
    return h.hexdigest()


def sha_floats(values):
    h = hashlib.sha256()
    for value in values: h.update(struct.pack("<d", float(value)))
    return h.hexdigest()


def sha_ints(values):
    h = hashlib.sha256()
    for value in values: h.update(struct.pack("<q", int(value)))
    return h.hexdigest()


def plain(v):
    if v is None or isinstance(v, (str, bool, int, float)): return v
    if hasattr(v, "name"): return {"name": v.name, "type": type(v).__name__}
    try: return [plain(x) for x in v]
    except TypeError:
        return {"rna_type": getattr(getattr(v, "bl_rna", None), "identifier", type(v).__name__),
                "not_serialized": True}


def simple_rna(value):
    result = {}
    for p in value.bl_rna.properties:
        if p.identifier == "rna_type" or p.type == "COLLECTION": continue
        try: result[p.identifier] = plain(getattr(value,p.identifier))
        except (AttributeError, RuntimeError): pass
    return result


def seed_spec(path=None):
    return json.loads(Path(path or PACK / "assets" / "shader-seeds.json").read_text())


def validate_seeds(spec):
    if spec.get("schema_version") != 1 or spec.get("qualification") != "requires_live_blender_and_character_review":
        raise ValueError("Unknown seed schema/qualification status")
    names = set()
    for group in spec["groups"]:
        if group["name"] in names: raise ValueError("Duplicate group name")
        names.add(group["name"])
        ids = [n["id"] for n in group["nodes"]]
        if len(ids) != len(set(ids)): raise ValueError("Duplicate node ID")
        inputs = [s["name"] for s in group["inputs"]]
        if len(inputs) != len(set(inputs)): raise ValueError("Duplicate socket name")
        for link in group["links"]:
            if len(link) != 4 or link[0] not in ids or link[2] not in ids:
                raise ValueError("Invalid declarative node link")
    return {"valid": True, "groups": sorted(names), "qualification": spec["qualification"]}


def inspect_scene(bpy):
    bpy.context.view_layer.update()
    result = {"schema_version": 1, "blender_version": bpy.app.version_string,
              "build_hash": bpy.app.build_hash.decode(errors="replace"),
              "file": bpy.data.filepath, "fingerprints": {}, "issues": [],
              "qualification": "inspection_only_not_model_quality_or_ui_fps",
              "limitations": ["Not a complete semantic fingerprint for every Blender data type",
                              "No UI performance measurement", "No automatic determination of dependency necessity",
                              "Evaluate required poses and native physics separately"]}
    if bpy.context.scene.render.engine != "CYCLES":
        result["issues"].append({"kind":"non-cycles-engine-review", "engine":bpy.context.scene.render.engine,
                                 "requirement":"Cycles by default; another engine needs an explicit user request"})
    meshes = {}
    for mesh in sorted(bpy.data.meshes, key=lambda x:x.name):
        entry = {"vertices": len(mesh.vertices), "polygons": len(mesh.polygons), "loops": len(mesh.loops),
                 "positions_sha256": sha_floats(c for v in mesh.vertices for c in v.co),
                 "topology_sha256": sha_ints(i for poly in mesh.polygons for i in (len(poly.vertices), *poly.vertices)),
                 "material_assignment_sha256": sha_ints(p.material_index for p in mesh.polygons),
                 "uv": {uv.name: sha_floats(c for loop in uv.data for c in loop.uv) for uv in mesh.uv_layers}}
        try: entry["corner_normals_sha256"] = sha_floats(c for n in mesh.corner_normals for c in n.vector)
        except (AttributeError, RuntimeError):
            entry["corner_normals_sha256"] = None
            result["issues"].append({"kind":"normal-inspection-unavailable", "mesh":mesh.name})
        if mesh.shape_keys:
            entry["shape_keys"] = {k.name:{"positions_sha256":sha_floats(c for p in k.data for c in p.co),
                                                  "relative_key":k.relative_key.name if k.relative_key else None,
                                                  "range":[k.slider_min,k.slider_max]} for k in mesh.shape_keys.key_blocks}
        meshes[mesh.name] = entry
    result["fingerprints"]["meshes"] = meshes
    objects = {}
    for obj in sorted(bpy.data.objects, key=lambda x:x.name):
        e = {"type":obj.type, "parent":obj.parent.name if obj.parent else None,
             "parent_bone":obj.parent_bone, "matrix_local":plain(obj.matrix_local),
             "library":obj.library.filepath if obj.library else None,
             "modifiers":[], "constraints":[]}
        for mod in obj.modifiers:
            props = {}
            for prop in mod.bl_rna.properties:
                if prop.identifier in ("rna_type", "name") or prop.type == "COLLECTION": continue
                try: props[prop.identifier] = plain(getattr(mod,prop.identifier))
                except (AttributeError,RuntimeError): pass
            settings = {key:simple_rna(getattr(mod,key)) for key in ("settings","collision_settings","point_cache")
                        if getattr(mod,key,None) is not None and hasattr(getattr(mod,key),"bl_rna")}
            e["modifiers"].append({"name":mod.name,"type":mod.type,"properties":props,"settings":settings})
        e["constraints"] = constraint_records(obj.constraints, result["issues"], obj.name)
        if obj.type == "MESH":
            groups = {g.index:g.name for g in obj.vertex_groups}
            e["weights_sha256"] = sha_floats(value for v in obj.data.vertices for g in sorted(v.groups,key=lambda x:x.group) for value in (v.index,g.group,g.weight))
            e["vertex_group_names"] = groups
        if obj.type == "ARMATURE":
            e["bones"] = {b.name:{"parent":b.parent.name if b.parent else None,
                                    "matrix_local":plain(b.matrix_local),"length":b.length,"deform":b.use_deform}
                          for b in sorted(obj.data.bones,key=lambda x:x.name)}
            e["pose"] = {}
            for b in obj.pose.bones:
                if b.bone.length < 1e-8: result["issues"].append({"kind":"zero-length-bone-review","object":obj.name,"bone":b.name})
                e["pose"][b.name] = {"rotation_mode":b.rotation_mode,
                    "constraints":constraint_records(b.constraints,result["issues"],obj.name+"/"+b.name)}
        if max(obj.scale)-min(obj.scale)>1e-6:
            result["issues"].append({"kind":"nonuniform-scale-review","object":obj.name,"scale":plain(obj.scale)})
        objects[obj.name] = e
    result["fingerprints"]["objects"] = objects
    images = {}
    for im in sorted(bpy.data.images,key=lambda x:x.name):
        raw = im.filepath
        resolved = Path(bpy.path.abspath(raw, library=im.library)) if raw else None
        packed = bool(im.packed_file) or bool(getattr(im,"packed_files",None))
        e = {"source":im.source,"filepath":raw,"colorspace":im.colorspace_settings.name,
             "alpha_mode":im.alpha_mode,"packed":packed,"size":plain(im.size)}
        if im.source == "FILE" and not packed:
            if resolved and resolved.is_file(): e["sha256"] = sha_file(resolved)
            else: result["issues"].append({"kind":"missing-external-image","image":im.name,"filepath":raw})
        if im.packed_file: e["packed_sha256"] = hashlib.sha256(im.packed_file.data).hexdigest()
        images[im.name] = e
    result["fingerprints"]["images"] = images
    node_trees = {}
    trees = [("material/"+m.name,m.node_tree) for m in bpy.data.materials if m.node_tree]
    trees += [("group/"+g.name,g) for g in bpy.data.node_groups]
    for name,tree in trees:
        node_trees[name] = {"nodes":[{"name":n.name,"type":n.bl_idname,
            "group":n.node_tree.name if hasattr(n,"node_tree") and n.node_tree else None,
            "inputs":[{"name":s.name,"identifier":s.identifier,"default":plain(s.default_value) if hasattr(s,"default_value") else None} for s in n.inputs],
            "outputs":[{"name":s.name,"identifier":s.identifier,"default":plain(s.default_value) if hasattr(s,"default_value") else None} for s in n.outputs],
            "properties":{k:plain(getattr(n,k)) for k in ("operation","blend_type","component","target","interpolation","extension","projection") if hasattr(n,k)},
            "image":n.image.name if hasattr(n,"image") and n.image else None,
            "color_ramp": {"interpolation":n.color_ramp.interpolation,"mode":n.color_ramp.color_mode,
                "elements":[{"position":e.position,"color":plain(e.color)} for e in n.color_ramp.elements]} if hasattr(n,"color_ramp") else None}
            for n in sorted(tree.nodes,key=lambda x:x.name)],
            "links":sorted([[l.from_node.name,l.from_socket.identifier,l.to_node.name,l.to_socket.identifier] for l in tree.links])}
        if hasattr(tree,"interface"):
            node_trees[name]["interface"] = [{"name":s.name,"in_out":s.in_out,"socket_type":s.socket_type,
                "default":plain(s.default_value) if hasattr(s,"default_value") else None} for s in tree.interface.items_tree if s.item_type == "SOCKET"]
    result["fingerprints"]["node_trees"] = node_trees
    drivers = []
    ids = [*bpy.data.objects,*bpy.data.shape_keys,*bpy.data.materials,*bpy.data.node_groups,*bpy.data.scenes]
    ids += [m.node_tree for m in bpy.data.materials if m.node_tree]
    for block in ids:
        anim = getattr(block,"animation_data",None)
        if not anim: continue
        for f in anim.drivers:
            d = f.driver
            vars_ = []
            for v in d.variables:
                targets = [{"id":t.id.name if t.id else None,"path":t.data_path,
                            "bone":getattr(t,"bone_target",None),"transform":getattr(t,"transform_type",None),
                            "space":getattr(t,"transform_space",None)} for t in v.targets]
                vars_.append({"name":v.name,"type":v.type,"targets":targets})
            drivers.append({"owner":block.name,"path":f.data_path,"index":f.array_index,"type":d.type,
                            "expression":d.expression,"simple_expression":bool(getattr(d,"is_simple_expression",False)),"variables":vars_})
            if not d.is_valid: result["issues"].append({"kind":"invalid-driver","owner":block.name,"path":f.data_path})
            if d.type == "SCRIPTED" and not getattr(d,"is_simple_expression",False):
                result["issues"].append({"kind":"python-driver-review","owner":block.name,"path":f.data_path})
    result["fingerprints"]["drivers"] = sorted(drivers,key=lambda x:(x["owner"],x["path"],x["index"]))
    result["runtime_inventory"] = {"enabled_addons": sorted(bpy.context.preferences.addons.keys()),
        "text_blocks":[{"name":t.name,"sha256":hashlib.sha256(t.as_string().encode()).hexdigest(),"use_module":t.use_module} for t in bpy.data.texts],
        "registered_handlers":{name:[getattr(f,"__module__","")+"."+getattr(f,"__name__",str(type(f))) for f in getattr(bpy.app.handlers,name)]
            for name in ("load_post","frame_change_pre","frame_change_post","depsgraph_update_pre","depsgraph_update_post")}}
    result["scene"] = {"engine":bpy.context.scene.render.engine,"fps":bpy.context.scene.render.fps,
        "fps_base":bpy.context.scene.render.fps_base,"frame":bpy.context.scene.frame_current,
        "view_transform":bpy.context.scene.view_settings.view_transform,
        "look":bpy.context.scene.view_settings.look,"exposure":bpy.context.scene.view_settings.exposure,
        "gamma":bpy.context.scene.view_settings.gamma}
    return result


def constraint_records(constraints, issues, owner):
    records = []
    for c in constraints:
        props = {}
        for prop in c.bl_rna.properties:
            if prop.identifier in ("rna_type", "name") or prop.type == "COLLECTION": continue
            try: props[prop.identifier] = plain(getattr(c,prop.identifier))
            except (AttributeError, RuntimeError): pass
        records.append({"name":c.name,"type":c.type,"properties":props})
        if hasattr(c,"target") and c.target is None:
            issues.append({"kind":"missing-constraint-target-review","owner":owner,"constraint":c.name})
        if hasattr(c,"is_valid") and not c.is_valid:
            issues.append({"kind":"invalid-constraint-review","owner":owner,"constraint":c.name})
    return records


def build_seeds(bpy, spec, output):
    validate_seeds(spec)
    if bpy.data.filepath:
        raise ValueError("Build seeds in factory startup without opening a production .blend")
    if Path(output).exists(): raise ValueError("Refuse to overwrite an existing library")
    bpy.context.scene.render.engine = "CYCLES"
    for g in spec["groups"]:
        if g["name"] in bpy.data.node_groups: raise ValueError("Seed group already exists")
        tree = bpy.data.node_groups.new(g["name"],"ShaderNodeTree"); tree.use_fake_user = True
        tree["pack_version"] = spec["pack_version"]; tree["qualification"] = spec["qualification"]
        for socket in g["inputs"]:
            s=tree.interface.new_socket(name=socket["name"],in_out="INPUT",socket_type=socket["type"])
            if "default" in socket: s.default_value=socket["default"]
        tree.interface.new_socket(name="Shader",in_out="OUTPUT",socket_type="NodeSocketShader")
        nodes = {}
        for definition in g["nodes"]:
            n=tree.nodes.new(definition["type"]); n.name=definition["id"]; n.location=definition.get("location",[0,0])
            for key,value in definition.get("properties",{}).items(): setattr(n,key,value)
            for key,value in definition.get("inputs",{}).items(): n.inputs[key].default_value=value
            nodes[definition["id"]]=n
        for a,b,c,d in g["links"]: tree.links.new(nodes[a].outputs[b],nodes[c].inputs[d])
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(output).resolve()))
    return {"output":str(output),"groups":[g["name"] for g in spec["groups"]],"qualification":spec["qualification"]}


def main(argv=None):
    if argv is None: argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("command",choices=["probe","inspect","build-seeds","validate-seeds"])
    p.add_argument("--output"); p.add_argument("--spec")
    args=p.parse_args(argv)
    try:
        if args.command == "validate-seeds": result=validate_seeds(seed_spec(args.spec))
        else:
            try: import bpy
            except ImportError as e: raise ValueError("Run this command inside Blender; bpy is unavailable") from e
            if args.command == "probe":
                result={"blender_version":bpy.app.version_string,"build_hash":bpy.app.build_hash.decode(errors="replace"),
                        "binary":bpy.app.binary_path,"python":sys.version,"enabled_addons":sorted(bpy.context.preferences.addons.keys()),
                        "background":bpy.app.background,"qualification":"environment_probe_only"}
            elif args.command == "inspect": result=inspect_scene(bpy)
            else:
                if not args.output or Path(args.output).suffix.lower() != ".blend": raise ValueError("Use --output NEW_LIBRARY.blend")
                result=build_seeds(bpy,seed_spec(args.spec),args.output)
                print(json.dumps(result,indent=2)); return 0
        value=json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n"
        if args.output:
            out=Path(args.output)
            if out.exists(): raise ValueError("Refuse to overwrite evidence; use a new output path")
            out.parent.mkdir(parents=True,exist_ok=True); out.write_text(value,encoding="utf-8")
        else: print(value,end="")
        return 0
    except (ValueError,OSError,RuntimeError,KeyError,AttributeError,TypeError) as e:
        print(json.dumps({"error":str(e)}),file=sys.stderr); return 2


if __name__ == "__main__": raise SystemExit(main())
