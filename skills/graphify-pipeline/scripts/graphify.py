#!/usr/bin/env python3
"""Dependency-free, read-only navigation graph of authoritative Blender skills."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PACK = Path("skills/anime-blender-pipeline")
SHARED = ("SKILL.md", "assets/stage-policy.json", "references/contract.md",
          "references/workflow.md", "references/diagnosis.md",
          "references/construction.md", "references/roles.md",
          "references/qualification.md", "references/tools.md",
          "references/schemas.md", "references/sources.md",
          "references/mathematics.md")
# Provisional diagnosis.md symptom -> editing owner, NEVER a claimed diagnosis.
FAULTS = (("Pink material", "02"), ("Washed-out/dark color", "02"),
          ("Dirty anime face shadows", "02"), ("Cutout fringes", "02"),
          ("Dark/disappearing eyes", "02"), ("Rig collapses", "04"),
          ("Limb flips", "04"), ("Physics explosion", "08"),
          ("Physics toggle does little", "08"), ("Late geometry change", "03"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def register(files, root, path):
    path = Path(path)
    if not (root / path).is_file():
        raise ValueError("Missing authoritative file: " + path.as_posix())
    files[path.as_posix()] = digest(root / path)


def roles_of(text):
    roles = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) != 3 or cols[0] == "Role" or not cols[0].strip("-: "):
            continue
        roles.append(dict(role=cols[0], requested=cols[1], responsibility=cols[2]))
    return roles


def build_graph(root):
    root = root.resolve()
    policy = json.loads((root / PACK / "assets/stage-policy.json").read_text(encoding="utf-8"))
    ids = [f"{i:02d}" for i in range(10)]
    if sorted(policy.get("stages", {})) != ids:
        raise ValueError("Unrecognized stage set; inspect policy before generating graph")
    if policy.get("candidate_limit") != 3 or policy.get("stage09_human_reviews") != ["audit", "delivery"]:
        raise ValueError("Unrecognized gate policy; update generator with audited semantics")
    files, stages, nodes, edges = {}, [], [], []
    for name in SHARED:
        register(files, root, PACK / name)
    nodes += [dict(id="start", type="source", title="Preserved PMX/source"),
              dict(id="end", type="end", title="Accepted native delivery")]
    for sid in ids:
        matches = list((root / "skills").glob(f"anime-blender-{sid}-*/SKILL.md"))
        if len(matches) != 1:
            raise ValueError("Expected exactly one skill for stage " + sid)
        skill = matches[0].relative_to(root)
        detail = (matches[0].parent / "references/stage.md").relative_to(root)
        register(files, root, skill)
        register(files, root, detail)
        header = re.search(r"(?m)^#\s+" + sid + r"\s+[—-]\s+(.+)$",
                           (root / skill).read_text(encoding="utf-8"))
        if not header:
            raise ValueError("Missing stage header: " + str(skill))
        checks = policy["stages"][sid]["required_checks"]
        if not checks or len(set(checks)) != len(checks):
            raise ValueError("Duplicate or missing check at stage " + sid)
        gates = ["audit", "delivery"] if sid == "09" else ["approval"]
        stage = dict(id=sid, title=header.group(1).strip(), skill=skill.as_posix(),
                     procedure=detail.as_posix(), required_checks=checks, human_gates=gates)
        stages.append(stage)
        nodes.append(dict(id="stage:" + sid, type="stage", title=stage["title"]))
        for path in (skill, detail):
            edges.append(dict(source="stage:" + sid, target="file:" + path.as_posix(),
                              type="read"))
        for check in checks:
            cid = "check:" + sid + ":" + check
            nodes.append(dict(id=cid, type="required_check", title=check))
            edges.append(dict(source="stage:" + sid, target=cid, type="requires"))
            edges.append(dict(source=cid, target="gate:" + sid + ":" + gates[-1],
                              type="must_pass_before_acceptance"))
        for gate in gates:
            gid = "gate:" + sid + ":" + gate
            nodes.append(dict(id=gid, type="human_gate", title=gate))
            edges.append(dict(source="stage:" + sid, target=gid, type="review"))
        if sid == "00":
            edges.append(dict(source="start", target="stage:00", type="input"))
        if sid != "09":
            edges.append(dict(source="gate:" + sid + ":approval",
                              target="stage:" + f"{int(sid)+1:02d}",
                              type="advance_after_pass_and_explicit_approval"))
        else:
            edges.append(dict(source="gate:09:audit", target="gate:09:delivery",
                              type="work_reaudit_and_final_submission"))
            edges.append(dict(source="gate:09:delivery", target="end",
                              type="delivery_is_final_acceptance"))
    role_path = PACK / "references/roles.md"
    roles = roles_of((root / role_path).read_text(encoding="utf-8"))
    config_paths = sorted((root / PACK / "assets/codex-agents").glob("*.toml"))
    configs = [p.relative_to(root).as_posix() for p in config_paths]
    for path in configs:
        register(files, root, path)
    for i, role in enumerate(roles):
        nodes.append(dict(id="model:" + str(i), type="requested_model_role",
                          title=role["role"], requested=role["requested"]))
        edges.append(dict(source="model:" + str(i), target="file:" + role_path.as_posix(),
                          type="documented_by"))
    for symptom, sid in FAULTS:
        fid = "failure:" + re.sub(r"[^a-z0-9]+", "-", symptom.lower()).strip("-")
        nodes.append(dict(id=fid, type="diagnostic_symptom", title=symptom))
        edges.append(dict(source=fid, target="stage:" + sid, type="provisional_route"))
    edges.append(dict(source="stage:09", target="stage:03",
                      type="late_geometry_backtrack_requalify_downstream"))
    for path, fingerprint in sorted(files.items()):
        nodes.append(dict(id="file:" + path, type="source_file",
                          title=path, sha256=fingerprint))
    return dict(schema_version=1, kind="source_linked_non_authoritative_index",
                pack_version=policy["pack_version"],
                policy=(PACK / "assets/stage-policy.json").as_posix(),
                source_hashes=dict(sorted(files.items())),
                stages=stages, model_roles=roles, model_configs=configs,
                fault_routes=[dict(symptom=s, owner_stage=owner, provisional=True)
                              for s, owner in FAULTS],
                nodes=nodes, edges=edges,
                warnings=["Graph is not acceptance evidence or a new policy.",
                          "Diagnose symptom routes; requalify affected downstream work.",
                          "Verify actual model availability and human approval.",
                          "Read original contract, workflow, stage procedure and run policy."])


HTML = r"""<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Graphify Pipeline</title>
<style>
:root{color-scheme:dark;font-family:system-ui,sans-serif;color:#e8effa;background:#0b1320}
body{max-width:1200px;margin:auto;padding:22px}h1{margin-bottom:4px}
small,p.note{color:#9baec7}.layout{display:grid;grid-template-columns:1fr 1fr;gap:16px}
section{background:#152239;border:1px solid #364b68;border-radius:12px;padding:16px}
.pair{display:grid;grid-template-columns:1.2fr 32px 1fr;gap:8px;align-items:center}
button{cursor:pointer;background:#224060;color:#eff7ff;border:1px solid #53739a;border-radius:8px;padding:12px;text-align:left}
button:focus,button:hover{outline:2px solid #8ab9ec}.gate{background:#294338;border-color:#5b856d}
.arrow,.down{text-align:center;color:#9ec5ec}.down{font-size:12px;padding:5px}
h2{font-size:18px}h3{font-size:15px}li{margin:6px 0}a{color:#a2cfff;overflow-wrap:anywhere}
@media(max-width:760px){.layout{grid-template-columns:1fr}body{padding:10px}}
</style>
<h1>PMX → Blender Pipeline Graph</h1>
<p class="note">Exact gate identifiers from source policy. Click stages to inspect linked procedures. No automatic approval.</p>
<div class="layout"><section><h2>Stages → human gates</h2><div id="graph"></div></section>
<div><section id="details"><h2>Choose a stage</h2></section>
<section><h2>Model-role requests</h2><div id="models"></div><p class="note">Verify runtime model availability.</p></section>
<section><h2>Diagnose / backtrack</h2><div id="faults"></div><p class="note">These are provisional owner routes. Late geometry → Stage 03, then rerun affected downstream checks and approvals.</p></section>
</div></div><script type="application/json" id="payload">__DATA__</script>
<script>
(function(){
"use strict";
const d=JSON.parse(document.getElementById("payload").textContent);
const get=id=>document.getElementById(id);
function add(parent,tag,value,cls){const x=document.createElement(tag);if(value!==null)x.textContent=value;if(cls)x.className=cls;parent.appendChild(x);return x;}
function file(parent,path){const a=add(parent,"a",path);a.href="../../../"+path;}
function detail(s){const p=get("details");p.replaceChildren();add(p,"h2","Stage "+s.id+": "+s.title);
add(p,"h3","Exact required checks");const u=add(p,"ul",null);s.required_checks.forEach(c=>add(u,"li",c));
add(p,"h3","Human gates");add(p,"p",s.human_gates.join(" → "));
add(p,"h3","Authoritative files");const f=add(p,"ul",null);
[s.skill,s.procedure,d.policy,"skills/anime-blender-pipeline/references/contract.md","skills/anime-blender-pipeline/references/workflow.md"].forEach(v=>file(add(f,"li",null),v));
add(p,"p","Proof requires live evidence, current run ledger and explicit human approval.","note");
}
d.stages.forEach((s,i)=>{const x=add(get("graph"),"div",null,"pair");
let b=add(x,"button",s.id+" "+s.title);b.onclick=()=>detail(s);
add(x,"div","→","arrow");b=add(x,"button",s.human_gates.join(" → "),"gate");b.onclick=()=>detail(s);
if(i<d.stages.length-1)add(get("graph"),"div","↓ approved transition","down");});
const m=add(get("models"),"ul",null);d.model_roles.forEach(r=>add(m,"li",r.role+": "+r.requested+" — "+r.responsibility));
const f=add(get("faults"),"ul",null);d.fault_routes.forEach(r=>add(f,"li",r.symptom+" → "+r.owner_stage));
detail(d.stages[0]);
})();
</script></html>"""


def html_for(data):
    encoded = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    encoded = encoded.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return HTML.replace("__DATA__", encoded)


def context_for(data):
    lines = ["# Pipeline navigation (not policy)", "",
             "| Stage | Exact required checks | Human gates | Authoritative procedure |",
             "| --- | --- | --- | --- |"]
    for s in data["stages"]:
        lines.append("| " + s["id"] + " " + s["title"] + " | " +
                     ", ".join(s["required_checks"]) + " | " +
                     ", ".join(s["human_gates"]) + " | " + s["procedure"] + " |")
    lines += ["", "Requested models (check actual availability):"]
    lines += ["- " + r["role"] + ": " + r["requested"] for r in data["model_roles"]]
    lines += ["", "Failure routes are provisional. Late geometry → 03; rerun affected downstream gates.",
              "Read original contract/workflow/stage source and live run policy before modifying anything."]
    return "\n".join(lines) + "\n"


def verify(current, snapshot):
    if snapshot.get("schema_version") != 1:
        raise ValueError("Incompatible graph format")
    for key in ("source_hashes", "stages", "model_roles", "fault_routes", "nodes", "edges"):
        if current[key] != snapshot.get(key):
            raise ValueError("Stale graph " + key + ": rebuild from current source")
    return True


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=("build", "verify", "stage", "fault", "models", "impact"))
    p.add_argument("target", nargs="?")
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--out", type=Path)
    args = p.parse_args(argv)
    root = args.root.resolve()
    out = args.out.resolve() if args.out else root / "skills/graphify-pipeline/generated"
    d = build_graph(root)
    if args.command == "build":
        out.mkdir(parents=True, exist_ok=True)
        (out / "graph.json").write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (out / "graph.html").write_text(html_for(d), encoding="utf-8")
        (out / "context.md").write_text(context_for(d), encoding="utf-8")
        print("Generated", out, ":", len(d["stages"]), "stages,",
              sum(len(s["required_checks"]) for s in d["stages"]), "exact required checks")
    elif args.command == "verify":
        verify(d, json.loads((out / "graph.json").read_text(encoding="utf-8")))
        print("Fresh graph; source hashes and exact gates match")
    elif args.command == "stage":
        sid = (args.target or "").zfill(2)
        s = next((v for v in d["stages"] if v["id"] == sid), None)
        if s is None:
            raise ValueError("Stage must be 00–09")
        print("STAGE", sid, s["title"], "\nCHECKS:", ", ".join(s["required_checks"]),
              "\nHUMAN:", " → ".join(s["human_gates"]),
              "\nREAD:", s["skill"], s["procedure"],
              "\nSHARED:", PACK / "references/contract.md", PACK / "references/workflow.md",
              "\nCheck current frozen run policy and evidence before advancing.")
    elif args.command == "models":
        for m in d["model_roles"]:
            print(m["role"], ":", m["requested"], "—", m["responsibility"])
        print("These are requested roles, not verified active model assignments.")
    elif args.command == "fault":
        needle = (args.target or "").strip().casefold()
        if not needle:
            raise ValueError("Provide a symptom")
        routes = [r for r in d["fault_routes"]
                  if needle in r["symptom"].casefold() or r["symptom"].casefold() in needle]
        for route in routes:
            print(route["symptom"], "→ provisional stage", route["owner_stage"])
        if not routes:
            print("No exact route. Diagnose using", PACK / "references/diagnosis.md")
        print("Confirm actual cause with distinguishing test; never auto-approve.")
    elif args.command == "impact":
        path = (args.target or "").replace("\\", "/")
        if not path:
            raise ValueError("Provide repo-relative source path")
        affected = [s["id"] for s in d["stages"] if path in (s["skill"], s["procedure"])]
        print("Source indexed:", path in d["source_hashes"], "direct stage owners:", affected or "shared/unknown")
        print("Re-run tests and approvals affected by changed dependencies; never assume all/none.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, json.JSONDecodeError) as e:
        print("Graphify:", e, file=sys.stderr)
        raise SystemExit(2)
