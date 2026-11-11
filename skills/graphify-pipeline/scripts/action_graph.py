#!/usr/bin/env python3
"""Source-derived task graph. Navigation only: never executes a fix or approves a gate."""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path
import graphify

HERE = Path(__file__).resolve().parents[3]
DEFAULT_OUT = Path("skills/graphify-pipeline/generated")
DIAGNOSIS = "skills/anime-blender-pipeline/references/diagnosis.md"
PATTERN = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$")


def source_tasks(root, stage):
    path = root / stage["procedure"]
    lines = path.read_text(encoding="utf-8").splitlines()
    matches = [(i, m.group(1), m.group(2)) for i, line in enumerate(lines)
               if (m := PATTERN.match(line))]
    if not matches:
        raise ValueError("No numbered tasks in " + stage["procedure"])
    result = []
    for idx, (i, num, title) in enumerate(matches):
        end = matches[idx + 1][0] if idx + 1 < len(matches) else len(lines)
        end = next((j for j in range(i + 1, end) if lines[j].startswith("## ")), end)
        body = [s.strip() for s in lines[i + 1:end] if s.strip() and not s.startswith("|")]
        excerpt = next((s for s in body if len(s) > 20), "")
        result.append(dict(id="task:" + stage["id"] + ":" + num, title=title,
                           source=stage["procedure"], line=i + 1, end_line=end,
                           preview=excerpt[:200]))
    return result


def diagnostic_table(root):
    rows = []
    for line_no, line in enumerate((root / DIAGNOSIS).read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 4 or cells[0] == "Symptom" or cells[0].startswith("---"):
            continue
        rows.append(dict(symptom=cells[0], causes=cells[1], tests=cells[2],
                         avoid=cells[3], source=DIAGNOSIS, line=line_no))
    if len(rows) < 9:
        raise ValueError("Expected diagnosis source rows are missing")
    return rows


def make_graph(root, base=None):
    root = Path(root).resolve()
    base = base or graphify.build_graph(root)
    nodes, edges, stages = [], [], []

    def node(id, kind, title, **extra):
        nodes.append(dict(id=id, kind=kind, title=title, **extra))

    def edge(a, b, condition):
        edges.append(dict(source=a, target=b, condition=condition))

    for stage in base["stages"]:
        sid = stage["id"]
        tasks = source_tasks(root, stage)
        sequence = [x["id"] for x in tasks]
        if sid == "09":
            sequence.insert(1, "gate:09:audit")
        sequence += ["required:" + sid + ":" + x for x in stage["required_checks"]]
        sequence += ["gate:" + sid + (":delivery" if sid == "09" else ":approval")]
        stages.append(dict(id=sid, title=stage["title"], tasks=tasks,
                           sequence=sequence, checks=stage["required_checks"],
                           gates=stage["human_gates"], procedure=stage["procedure"]))
        node("start:" + sid, "entry", "Start stage " + sid)
        edge("start:" + sid, sequence[0], "begin_after_verified_predecessor")
        for i, current in enumerate(sequence):
            following = (sequence[i+1] if i+1 < len(sequence) else
                         ("start:" + f"{int(sid)+1:02d}" if sid != "09" else "end"))
            if current.startswith("gate:"):
                node(current, "human_gate", current.split(":")[-1],
                     source="skills/anime-blender-pipeline/references/workflow.md")
                edge(current, following, "only_after_real_explicit_human_decision_recorded")
                continue
            task = next((x for x in tasks if x["id"] == current), None)
            if task:
                node(current, "task", task["title"], source=task["source"],
                     line=task["line"], end_line=task["end_line"], preview=task["preview"])
                check = "qc:" + current
                node(check, "local_check_not_formal_gate", "Inspect task result: " + task["title"],
                     source=task["source"], line=task["line"])
                edge(current, check, "perform_then_inspect")
            else:
                check = current
                node(check, "required_check", current.split(":",2)[2],
                     source=base["policy"], evidence_details=stage["procedure"])
            edge(check, following, "pass_with_real_evidence")
            diag, attempt1, retest1, attempt2, retest2, rollback = [
                prefix + ":" + current for prefix in
                ("diagnose", "attempt1", "retest1", "attempt2", "retest2", "rollback")
            ]
            node(diag, "diagnose", "Identify fault and distinguishing test", source=DIAGNOSIS)
            node(attempt1, "repair", "Try one evidence-based reversible fix", source=DIAGNOSIS)
            node(retest1, "retest", "Measure fix and regressions")
            node(attempt2, "repair", "Try next supported fix only if needed", source=DIAGNOSIS)
            node(retest2, "retest", "Measure fix and regressions")
            node(rollback, "rollback", "After 2 non-improving attempts restore best; re-diagnose", source=DIAGNOSIS)
            for a,b,condition in [
                (check,diag,"fail_or_uncertain"), (diag,attempt1,"distinguishing_test"),
                (attempt1,retest1,"run_isolated_trial"), (retest1,check,"fixed_return_to_interrupted_check"),
                (retest1,diag,"improving_but_still_wrong_reassess"),
                (retest1,attempt2,"non_improving_attempt_1"),
                (attempt2,retest2,"run_isolated_trial"), (retest2,check,"fixed_return_to_interrupted_check"),
                (retest2,diag,"improving_but_still_wrong_reassess"),
                (retest2,rollback,"two_consecutive_non_improving_attempts"),
                (rollback,diag,"restored_best_reassess_or_escalate"),
            ]:
                edge(a,b,condition)
    node("end", "delivery", "Final accepted native asset; external approval required")
    return dict(schema_version=1, kind="source_linked_action_router_not_policy",
                source_hashes=base["source_hashes"], policy=base["policy"],
                stages=stages, faults=diagnostic_table(root),
                model_roles=base["model_roles"], nodes=nodes, edges=edges)


HTML = r"""<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Graphify Action Navigator</title>
<style>
:root{font:15px system-ui;background:#0d1524;color:#e5efff;color-scheme:dark}
body{margin:auto;padding:18px;max-width:1480px}
h1{margin:0}h2{font-size:18px}h3{font-size:15px}
main{display:grid;grid-template-columns:200px 1fr 1fr;gap:14px}
section{background:#16243b;border:1px solid #384d67;border-radius:10px;padding:14px}
button{font:inherit;cursor:pointer;background:#284361;border:1px solid #547595;
color:#fff;padding:10px;border-radius:8px;text-align:left}
button:hover,button:focus{outline:2px solid #99caff}
button.active{background:#33638e}button.good{background:#28583c}
button.bad{background:#713c36}.stages,.stack{display:flex;flex-direction:column;gap:8px}
.node{border:1px solid #466484;padding:10px;border-radius:8px;margin:8px 0}
.node.on{outline:2px solid #9dcbff}.arrow{color:#add0fb;text-align:center}
small,.muted{color:#acc1da}.muted{font-size:13px}
a{color:#9dcdff;overflow-wrap:anywhere}.controls{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}
.repair{border-left:3px solid #ce9c5f;padding-left:12px;margin-top:14px}
@media(max-width:900px){main{grid-template-columns:1fr}}
</style>
<h1>PMX → Blender action graph</h1>
<p class="muted">Task → local check → success: next task | problem: diagnosis → bounded attempt → retest → same check.
All formal stage checks and human approvals still apply. UI navigation does not approve work.</p>
<main><section><h2>Stages</h2><div class="stages" id="stages"></div><h3>Requested model roles</h3><div id="models"></div></section>
<section><h2 id="stagehead"></h2><div id="path"></div></section>
<section><h2>Selected node</h2><div id="focus"></div><div id="trouble"></div></section></main>
<script id="payload" type="application/json">__DATA__</script>
<script>
(function(){
"use strict";
const g=JSON.parse(document.getElementById("payload").textContent);
const at=id=>document.getElementById(id);
const make=(p,t,text,cls)=>{const v=document.createElement(t);if(text!==null)v.textContent=text;
if(cls)v.className=cls;p.appendChild(v);return v};
let stage=g.stages[0],pointer=0,interrupted=null,step=0;
function findTask(id){return stage.tasks.find(t=>t.id===id)}
function choose(s){stage=s;pointer=0;interrupted=null;step=0;draw()}
function link(p,path,line){const a=make(p,"a",path+(line?" (line "+line+")":""));
a.href="../../../"+path}
function fail(){interrupted=pointer;step=0;draw()}
function repaired(){pointer=interrupted;interrupted=null;step=0;draw()}
function advance(){if(pointer+1<stage.sequence.length){pointer++;draw()}}
function draw(){
at("stages").replaceChildren();at("models").replaceChildren();
g.stages.forEach(s=>{const b=make(at("stages"),"button",s.id+" "+s.title,
s.id===stage.id?"active":"");b.onclick=()=>choose(s)});
g.model_roles.forEach(r=>make(at("models"),"p",r.role+": "+r.requested,"muted"));
at("stagehead").textContent="Stage "+stage.id+": "+stage.title;
at("path").replaceChildren();at("focus").replaceChildren();at("trouble").replaceChildren();
stage.sequence.forEach((id,i)=>{
const task=findTask(id),gate=id.startsWith("gate:"),formal=id.startsWith("required:");
const label=task?task.title:gate?"HUMAN "+id.split(":").pop():"REQUIRED "+id.split(":").slice(2).join(":");
const card=make(at("path"),"div",null,"node"+(pointer===i?" on":""));
const b=make(card,"button",(i+1)+". "+label);b.onclick=()=>{pointer=i;interrupted=null;step=0;draw()};
if(task)make(card,"p","↓ Local result inspection (not a new gate)","muted");
if(gate)make(card,"p","Explicit human decision in real pipeline ledger","muted");
if(!gate)make(card,"p","PASS ↓ next   /   FAIL → diagnose and repair","muted");
if(i<stage.sequence.length-1)make(at("path"),"div","↓ verified success","arrow");
});
const id=stage.sequence[pointer],task=findTask(id),gate=id.startsWith("gate:"),formal=id.startsWith("required:");
if(task){make(at("focus"),"h3",task.title);make(at("focus"),"p",task.preview);
link(at("focus"),task.source,task.line);
make(at("focus"),"p","Inspect actual work and original source text before marking navigation pass.","muted")}
if(formal){make(at("focus"),"h3",id.split(":").slice(2).join(":"));
make(at("focus"),"p","This is an exact required check, not an invented quality threshold.");
link(at("focus"),stage.procedure);make(at("focus"),"p",null);link(at("focus"),g.policy)}
if(gate){make(at("focus"),"h3","Human decision required");
make(at("focus"),"p","STOP: this graph cannot accept or record approval. Read the source and use the existing review/approval CLI.");
link(at("focus"),"skills/anime-blender-pipeline/references/workflow.md");
const b=make(at("focus"),"button","View next node (does not grant approval)");
b.onclick=advance}
if(!gate&&interrupted===null){
const c=make(at("focus"),"div",null,"controls");
const a=make(c,"button","PASS → next","good");a.onclick=advance;
const b=make(c,"button","FAIL → diagnose","bad");b.onclick=fail;
make(at("focus"),"p","Buttons only move the graph pointer; they do not evaluate Blender output or modify evidence.","muted")}
if(interrupted!==null){
const p=at("trouble");make(p,"h3","Failure and return route");
make(p,"p","Interrupted: "+stage.sequence[interrupted],"muted");
const messages=[
"Diagnose: record symptom, last correct checkpoint and distinguishing test",
"Attempt 1: change one justified variable; keep rollback",
"Retest 1: compare measured result and neighboring regressions",
"Attempt 2: different supported fix if first trial did not improve",
"Retest 2: compare measured result and neighboring regressions",
"Restore best checkpoint; re-diagnose or escalate after two consecutive non-improving trials"
];
messages.forEach((m,i)=>make(p,"div",(i+1)+". "+m,
"node"+(step===i?" on":"")));
const c=make(p,"div",null,"controls");
if(step===0||step===1||step===3){const b=make(c,"button",step===0?"Evidence identified → attempt":"Attempt done → retest");
b.onclick=()=>{step++;draw()}}
else if(step===2||step===4){
const a=make(c,"button","Verified fix → SAME original check","good");a.onclick=repaired;
const b=make(c,"button","Improving but unresolved → re-diagnose");b.onclick=()=>{step=0;draw()};
const d=make(c,"button",step===2?"No improvement → next bounded attempt":"Two non-improving → rollback","bad");
d.onclick=()=>{step++;draw()}
}else{const b=make(c,"button","Restore done → re-diagnose");b.onclick=()=>{step=0;draw()}}
const relevant=g.faults.filter(x=>stage.id==="02"?/material|color|shadow|fringe|eyes/i.test(x.symptom):
stage.id==="04"?/rig|limb/i.test(x.symptom):
stage.id==="08"?/physics/i.test(x.symptom):false);
if(relevant.length){make(p,"h3","Potential diagnostics from actual source");
relevant.forEach(x=>{const d=make(p,"div",x.symptom+": "+x.tests,"repair");
link(d,x.source,x.line)})}
make(p,"p","After a repair passes, return to the ORIGINAL quality check. Then pass that check with evidence before continuing.","muted");
}
}
draw();
})();
</script></html>"""


def render_html(data):
    packed = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    packed = packed.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return HTML.replace("__DATA__", packed)


def context(data):
    lines = ["# Task router (not authoritative policy)", ""]
    for stage in data["stages"]:
        lines.append("## " + stage["id"] + ": " + stage["title"])
        for task in stage["tasks"]:
            lines.append("- " + task["title"] + " — " + task["source"] +
                         " line " + str(task["line"]))
        lines.append("- Exact stage checks: " + ", ".join(stage["checks"]))
        lines.append("- Existing human gates: " + ", ".join(stage["gates"]))
    lines.extend(["", "Repair → retest → same interrupted check → next task after evidence.",
                  "Two consecutive non-improving experiments → rollback/re-diagnose.",
                  "Never infer or record human acceptance from graph navigation."])
    return "\n".join(lines) + "\n"


def build_files(root, out, base=None):
    graph = make_graph(root, base)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "action_graph.json").write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "action_graph.html").write_text(render_html(graph), encoding="utf-8")
    (out / "actions_context.md").write_text(context(graph), encoding="utf-8")
    print("Generated action flow:", sum(len(s["tasks"]) for s in graph["stages"]),
          "source tasks,", sum(len(s["checks"]) for s in graph["stages"]), "exact checks")
    return graph


def verify_files(root, out):
    actual = make_graph(root)
    saved = json.loads((Path(out) / "action_graph.json").read_text(encoding="utf-8"))
    for name in ("source_hashes", "stages", "nodes", "edges", "faults", "model_roles"):
        if actual[name] != saved.get(name):
            raise ValueError("Stale action graph at " + name + "; rebuild")
    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=("build", "verify", "stage"))
    p.add_argument("stage", nargs="?")
    p.add_argument("--root", type=Path, default=HERE)
    p.add_argument("--out", type=Path)
    a = p.parse_args()
    root = a.root.resolve()
    out = a.out.resolve() if a.out else root / DEFAULT_OUT
    if a.command == "build":
        build_files(root, out)
    elif a.command == "verify":
        verify_files(root, out)
        print("Action graph current")
    else:
        graph = make_graph(root)
        s = next((v for v in graph["stages"] if v["id"] == (a.stage or "").zfill(2)), None)
        if not s:
            raise ValueError("Stage must be 00–09")
        print("START", s["id"], s["title"])
        for task in s["tasks"]:
            print("TASK", task["title"], "→ inspect → PASS next / FAIL diagnosis, fix, retest, return")
        print("REQUIRED:", ", ".join(s["checks"]))
        print("HUMAN:", ", ".join(s["gates"]))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError) as exc:
        print("Action Graphify:", exc, file=sys.stderr)
        sys.exit(2)
