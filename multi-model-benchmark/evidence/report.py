"""Deterministic seven-section report from a validated ledger. The report is never the source of truth.

Fails closed: an invalid ledger raises ReportBlocked. Missing verdicts count as `no_verdict`
(never pass). Human interpretation is accepted only as separately attributed narrative text.
"""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import sys

from .ledger import ArtifactStore, Ledger, compromised_holdout_cases, validate_events

SECTIONS = ("1. Experiment Summary", "2. Performance, Quality and Benchmark Results",
            "3. Lap-by-Lap Failure and Adjustment Analysis", "4. Specialization Effectiveness",
            "5. Workflow Integration, Reliability and Safety",
            "6. Miscellaneous Findings and Future Model Analysis", "7. Final Verdict")
SELECTION_RULE = "max validation-split first-try pass rate; ties -> lower mean verified seconds"
PILOT_N, PILOT_RATE, PROD_N = 20, 0.75, 300
PILOT_FAMILIES = 5
PROD_FAMILIES = 10  # minimum *different real-character families*, not samples



class ReportBlocked(ValueError):
    pass


def wilson(k, n, z=1.96):
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - m), min(1.0, c + m))


def nearest_rank(values, q):
    v = sorted(values)
    return v[max(0, math.ceil(q * len(v)) - 1)] if v else None


def _pct(x):
    return "n/a" if x is None else "%.0f%%" % (100 * x)


def _ci(k, n):
    w = wilson(k, n)
    return "n/a" if w is None else "%.0f-%.0f%%" % (100 * w[0], 100 * w[1])


def _f(x, nd=2):
    return "not measured" if x is None else ("%.*f" % (nd, x))


def table(headers, rows):
    if not rows:
        return "_No rows._\n"
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out) + "\n"


class Model:
    """Indexes one experiment's events."""

    def __init__(self, events, experiment_id):
        self.experiment_id = experiment_id
        self.events = [e for e in events if e["experiment_id"] == experiment_id]
        self.all_events = events
        self.laps = [e for e in self.events if e["event_type"] == "lap"]
        self.attempts = [e for e in self.events if e["event_type"] == "attempt"]
        self.decisions = [e for e in self.events if e["event_type"] == "decision"]
        self.verdict = {}
        self.verdicts = [e for e in self.events if e["event_type"] == "verdict"]
        for v in self.verdicts:
            self.verdict[v["attempt_id"]] = v  # later (re-evaluation) verdict supersedes
        self.compromised = compromised_holdout_cases(self.events)

    def status(self, a):
        v = self.verdict.get(a["attempt_id"])
        return v["result"] if v else "no_verdict"

    def groups(self):
        g = {}
        for a in self.attempts:
            g.setdefault((a["lap_id"], a["task_id"], a["split"], a["role"]), []).append(a)
        return g

    def stats(self, attempts):
        first = [a for a in attempts if a["attempt_no"] == 1]
        counts = {k: 0 for k in ("pass", "fail", "not_run", "not_applicable", "blocked", "no_verdict")}
        severe = 0
        for a in first:
            counts[self.status(a)] += 1
            v = self.verdict.get(a["attempt_id"])
            severe += 1 if v and v["severe_regression"] else 0
        times, tok_in, tok_out = [], [], []
        for a in first:
            v = self.verdict.get(a["attempt_id"])
            if a["inference_seconds"] is not None and v and v["wall_seconds"] is not None:
                times.append(a["inference_seconds"] + v["wall_seconds"])
            if a["input_tokens"] is not None:
                tok_in.append(a["input_tokens"])
            if a["output_tokens"] is not None:
                tok_out.append(a["output_tokens"])
        repair_pass = sum(1 for a in attempts if a["attempt_no"] > 1 and self.status(a) == "pass")
        return {"n": len(first), "counts": counts, "severe": severe,
                "cases": len({a["case_id"] for a in first}), "families": len({a["source_family"] for a in first}),
                "times": times, "tok_in": tok_in, "tok_out": tok_out,
                "repairs": sum(1 for a in attempts if a["attempt_no"] > 1), "repair_pass": repair_pass}


def _selected_lap(m, task, digest):
    """Predeclared validation selector; holdout results never choose a lap."""
    choices = []
    for lap in m.laps:
        relevant = [a for a in m.attempts if a["lap_id"] == lap["lap_id"]
                    and a["task_id"] == task and a["role"] == "target"
                    and a["split"] == "validation" and a["attempt_no"] == 1
                    and a["model_digest"] == digest]
        if not relevant:
            continue
        scores = m.stats(relevant)
        times = scores["times"]
        mean_time = (sum(times) / len(times)) if len(times) == scores["n"] else float("inf")
        choices.append((-(scores["counts"]["pass"] / scores["n"]), mean_time, lap["lap_id"]))
    return min(choices)[2] if choices else None


def readiness(m):
    """Conservative state, never a self-attested production certificate.

    Qualification is scoped to ONE model digest, ONE selected lap and ONE task.
    Trial repetitions do not increase independent case coverage. Unidentified
    assets or generic reviewer statements can never produce a qualified state.
    """
    if not m.attempts:
        return "no attempts recorded", ["record at least one attempt"]
    digests = {a["model_digest"] for a in m.attempts}
    if len(digests) != 1:
        return "BLOCKED: mixed model digests", ["use a separate experiment/report for each exact model digest"]
    digest = next(iter(digests))
    verified = [a for a in m.attempts if a["attempt_id"] in m.verdict
                and m.verdict[a["attempt_id"]]["result"] in ("pass", "fail")
                and m.verdict[a["attempt_id"]]["isolation_verified"]]
    if not verified:
        return "1 proposal-only", ["independent isolation-verified domain oracle verdict needed"]
    if all(a["stage"] is None for a in m.attempts):
        return "2 verified observations (domain qualification NOT configured)", [
            "a versioned domain-specific acceptance profile and independent real-workflow evaluation are required"]
    real = [a for a in verified if a["fixture_kind"] == "real" and a.get("license_record_sha256")]
    if not real:
        return "2 verified synthetic observations (development-only)", ["real licensed PMX/VMD and Blender assets not evaluated"]

    unmet = []
    tasks = {a["task_id"] for a in m.attempts if a["role"] == "target"}
    for task in sorted(tasks):
        selected = _selected_lap(m, task, digest)
        if selected is None:
            unmet.append("%s: no preselection from validation split" % task)
            continue
        lap = next(x for x in m.laps if x["lap_id"] == selected)
        finals = [x for x in m.laps if x.get("holdout_final_eval") is True
                  and x["parent_lap_id"] == selected and x["task_id"] == task
                  and x["selection_rule_sha256"] == lap["selection_rule_sha256"]]
        if len(finals) != 1:
            unmet.append("%s: requires exactly one frozen final-evaluation child lap of selected %s" % (task, selected))
            continue
        final_lap = finals[0]
        hold = [a for a in m.attempts if a["task_id"] == task and a["model_digest"] == digest
                and a["lap_id"] == final_lap["lap_id"] and a["split"] == "holdout"
                and a["role"] == "target" and a["attempt_no"] == 1
                and a["case_id"] not in m.compromised
                and a.get("final_eval_selection_rule_sha256") == final_lap["selection_rule_sha256"]
                and a["fixture_kind"] == "real" and a.get("license_record_sha256")]
        # Same exact case repeated 300 times is ONE unique test, not 300 holdouts.
        cases = {a["case_id"] for a in hold}
        families = {a["source_family"] for a in hold}
        successful = all(m.status(a) == "pass" for a in hold)
        if len(cases) < PROD_N or len(families) < PROD_FAMILIES or len(hold) != len(cases) or not successful:
            unmet.append("%s/%s: need >=%d distinct untouched REAL cases, >=%d source families, "
                         "no duplicated case IDs or failures (have %d unique cases, %d families, %d trials)" %
                         (task, selected, PROD_N, PROD_FAMILIES, len(cases), len(families), len(hold)))
        # Provenance is explicit, not inferred from a license flag.
        tracks = {a.get("asset_track") for a in hold}
        if not {"pmx_vmd", "blender_native"}.issubset(tracks):
            unmet.append("%s: both PMX/VMD and native Blender animation tracks not evidenced" % task)
        for kind in ("sol_light_review", "human_gate"):
            scope = "%s|%s|%s|%s" % (m.experiment_id, digest, task, selected)
            if not any(d["decision_kind"] == kind and d["outcome"] == "approved"
                       and d["scope"] == scope for d in m.decisions):
                unmet.append("%s: no exact-scope approved %s decision (%s)" % (task, kind, scope))
    if unmet:
        return "3 real-asset evidence exists (NOT qualified)", unmet
    # The operational Codex-effort <=35% cost gate is not yet stored as a trusted
    # event or review; no automatic qualification even after all other gates.
    return "3 real-asset evidence exists (NOT qualified)", [
        "Codex time + required human review cost gate not independently recorded; manual qualification blocked"]


def capability_rows(m, head):
    rows = []
    stats_by = m.groups()
    for task in sorted({a["task_id"] for a in m.attempts if a["role"] == "target"}):
        for digest in sorted({a["model_digest"] for a in m.attempts if a["task_id"] == task and a["role"] == "target"}):
            best, best_key, best_stats = None, None, None
            dev = {}
            for (lap, t, split, role), atts in stats_by.items():
                if t != task or role != "target":
                    continue
                atts = [a for a in atts if a["model_digest"] == digest]
                if not atts:
                    continue
                s = m.stats(atts)
                if split == "dev":
                    dev[lap] = [s["counts"]["pass"], s["n"]]
                if split == "validation" and s["n"]:
                    mean_t = (sum(s["times"]) / len(s["times"])) if s["times"] else float("inf")
                    key = (-s["counts"]["pass"] / s["n"], mean_t, lap)
                    if best_key is None or key < best_key:
                        best, best_key, best_stats = lap, key, s
            level, _ = readiness(m)
            row = {"task_id": task, "model_digest": digest, "best_lap_id": best,
                   "selection_rule": SELECTION_RULE, "split_basis": "validation" if best else "none",
                   "first_try_pass_count": best_stats["counts"]["pass"] if best else None,
                   "n": best_stats["n"] if best else None,
                   "uncertainty": ({"wilson95": [round(x, 3) for x in wilson(best_stats["counts"]["pass"], best_stats["n"])],
                                    "independent_families": best_stats["families"],
                                    "note": "within-family correlation makes the interval optimistic"} if best else None),
                   "dev_only_first_try_by_lap": dev,
                   "trusted_scope": "development-only synthetic smoke; not a production scope" if not best else "validation split only",
                   "readiness": level, "evidence_ref": head}
            rows.append(row)
    return rows


def generate(ledger_path, artifact_root, experiment_id, narrative=None):
    ledger = Ledger(ledger_path)
    store = ArtifactStore(artifact_root)
    events = ledger.read()
    errs = validate_events(events, store)
    if errs:
        raise ReportBlocked("ledger invalid; no report generated: " + "; ".join(errs[:5]))
    m = Model(events, experiment_id)
    if not m.laps:
        raise ReportBlocked("no lap events for experiment " + experiment_id)
    if len({a["model_digest"] for a in m.attempts}) > 1:
        raise ReportBlocked("mixed model digests: one individual report must cover one exact model")
    head = events[-1]["event_hash"]
    narrative = narrative or {}
    level, unmet = readiness(m)
    caps = capability_rows(m, head)
    md = ["# Model Evaluation Report v2.1: " + experiment_id, "",
          "_Generated from ledger head `%s` (%d events). Measures come only from validated events; narrative text is separately attributed._" % (head[:16], len(events)), ""]

    def interp(n):
        e = narrative.get(str(n))
        return ["", "**Interpretation:** " + ("(author: %s) %s" % (e["author"], e["text"]) if e else "_none authored_"), ""]

    # 1
    md += ["## " + SECTIONS[0], ""]
    digests = sorted({a["model_digest"] for a in m.attempts})
    tags = sorted({a.get("model_tag", "not recorded") for a in m.attempts})
    tasks = sorted({a["task_id"] for a in m.attempts if a["role"] == "target"} | {l["task_id"] for l in m.laps})
    stages = sorted({str(a["stage"]) for a in m.attempts if a["role"] == "target"})
    env = {}
    for l in m.laps:
        env.update(l.get("environment", {}))
    rows = [("Experiment", experiment_id), ("Model digest(s)", ", ".join(d[:19] for d in digests) or "none"),
            ("Model tag(s)", ", ".join(tags)), ("Task(s) / stage(s)", "%s / %s" % (", ".join(tasks), ", ".join(stages) or "null")),
            ("Laps recorded", len(m.laps)), ("Attempts recorded", len(m.attempts)),
            ("Decoding", "; ".join(sorted({"T=%s ctx=%s seed=%s reasoning=%s" % (a["temperature"], a["num_ctx"], a["seed"], a["reasoning_mode"]) for a in m.attempts})) or "none"),
            ("Native template hash", "recorded" if all(a["template_sha256"] for a in m.attempts) else "NOT RECORDED for %d attempt(s)" % sum(1 for a in m.attempts if not a["template_sha256"])),
            ("Environment (lap-declared)", json.dumps(env, sort_keys=True) if env else "not recorded"),
            ("Readiness (evidence-derived)", level)]
    md += [table(("Field", "Value"), rows)] + interp(1)

    # 2
    md += ["## " + SECTIONS[1], "",
           "Rate = verified passes / ALL first-try attempts in the group (blocked, not_run and no_verdict count against). Repair attempts (attempt_no > 1) are reported separately and never counted as first-try. Rates are exploratory; correlated families make intervals optimistic.", ""]
    rows, gates = [], []
    for (lap, task, split, role), atts in sorted(m.groups().items()):
        s = m.stats(atts)
        c = s["counts"]
        tp = (c["pass"] / (sum(s["times"]) / 60)) if s["times"] and len(s["times"]) == s["n"] else None
        rows.append((lap, task, split, role, "%d/%d" % (c["pass"], s["n"]), _pct(c["pass"] / s["n"] if s["n"] else None), _ci(c["pass"], s["n"]),
                     s["cases"], s["families"], c["fail"], c["not_run"], c["blocked"], c["no_verdict"], s["severe"],
                     "%d/%d" % (s["repair_pass"], s["repairs"]),
                     "%s / %s" % (_f(nearest_rank(s["times"], .5), 1), _f(nearest_rank(s["times"], .95), 1)) if s["times"] else "not measured",
                     _f(tp, 2) if tp is not None else "not measured (timing incomplete)",
                     "%s / %s" % (sum(s["tok_in"]) if s["tok_in"] else "n/m", sum(s["tok_out"]) if s["tok_out"] else "n/m")))
        if role == "target" and split == "dev":
            ok = (s["n"] == PILOT_N and s["cases"] == PILOT_N
                  and s["families"] >= PILOT_FAMILIES
                  and c["pass"] / s["n"] >= PILOT_RATE and s["severe"] == 0)
            gates.append("%s / %s: exploratory pilot gate (>=%d first-try, >=%d%% pass, 0 severe): %s; cost gate (<=35%% of Codex effort): NOT MEASURED, so the gate is INCOMPLETE." % (
                lap, task, PILOT_N, int(PILOT_RATE * 100), "numerically met" if ok else "not met (n=%d, pass=%d, severe=%d)" % (s["n"], c["pass"], s["severe"])))
    md += [table(("Lap", "Task", "Split", "Role", "First-try pass", "Rate", "Wilson 95%", "Cases", "Families", "Fail", "Not run", "Blocked", "No verdict", "Severe", "Repair pass/tries (offline)", "p50/p95 model+oracle s", "Model+oracle passes/min (not end-to-end)", "Tokens in/out"), rows), ""]
    md += ["**Exploratory gates:**", ""] + ["- " + g for g in gates] + [""]
    md += ["**Real-use gap:** real PMX/VMD and native Blender fixtures evaluated: %d attempt(s). Unknown is not pass." % sum(1 for a in m.attempts if a["fixture_kind"] == "real"), ""]
    comp = {c: r for c, r in m.compromised.items()}
    md += ["**Compromised holdout cases:** " + (", ".join("%s (%s)" % kv for kv in sorted(comp.items())) if comp else "none recorded"), ""] + interp(2)

    # 3
    md += ["## " + SECTIONS[2], ""]
    for lap in m.laps:
        atts = [a for a in m.attempts if a["lap_id"] == lap["lap_id"]]
        s = m.stats([a for a in atts if a["role"] == "target"])
        md += ["### %s (parent: %s)" % (lap["lap_id"], lap["parent_lap_id"] or "none"), "",
               "- Change reason (controller-declared): %s" % lap["change_reason"],
               "- Selection rule hash: `%s`; split manifest hash: `%s`" % (lap["selection_rule_sha256"][:16], lap["split_manifest_sha256"][:16]),
               "- Cases consulted for this change: %s" % (", ".join(lap["cases_consulted_for_change"]) or "none"),
               "- Target first-try: %d/%d pass; severe regressions: %d" % (s["counts"]["pass"], s["n"], s["severe"]), ""]
        bad = [a for a in atts if m.status(a) != "pass"]
        rows = []
        for a in bad:
            v = m.verdict.get(a["attempt_id"])
            rows.append((a["attempt_id"], a["case_id"], m.status(a), v["failure_category"] if v else "n/a", v["severity"] if v else "n/a",
                         ("evaluator note: " + v["reason"]) if v and v["reason"] else "none", v["evidence_path"] if v and v["evidence_path"] else "none"))
        md += [table(("Attempt", "Case", "Status", "Category", "Severity", "Evaluator note (not a root-cause analysis; may echo candidate-influenced text)", "Evidence"), rows),
               "Root cause: **unknown** unless attributed narrative below states otherwise.", ""]
    md += interp(3)

    # 4
    md += ["## " + SECTIONS[3], "", "Untuned baseline = a lap with no parent. Comparison uses only cases attempted first-try in both laps. Lap IDs reference Section 2; numbers here are deltas only.", ""]
    rows = []
    by = m.groups()
    canary_tasks = sorted({a["task_id"] for a in m.attempts if a["role"] == "canary"})
    for lap_meta in m.laps:
        if lap_meta["parent_lap_id"] is None:
            continue
        lap, lap_task = lap_meta["lap_id"], lap_meta["task_id"]
        base_laps = [l["lap_id"] for l in m.laps if l["parent_lap_id"] is None and l["task_id"] == lap_task]
        for role, role_tasks in (("target", [lap_task]), ("canary", canary_tasks)):
            for task in role_tasks:
                for split in ("dev", "validation", "holdout"):
                    b = [a for bl in base_laps for a in by.get((bl, task, split, role), []) if a["attempt_no"] == 1]
                    t = [a for a in by.get((lap, task, split, role), []) if a["attempt_no"] == 1]
                    common = {a["case_id"] for a in b} & {a["case_id"] for a in t}
                    if not common:
                        continue
                    bp = sum(1 for a in b if a["case_id"] in common and m.status(a) == "pass")
                    tp = sum(1 for a in t if a["case_id"] in common and m.status(a) == "pass")
                    n = len(common)
                    same_model = {a["model_digest"] for a in b} == {a["model_digest"] for a in t}
                    rows.append((lap, task, role, split, "%d/%d" % (bp, n), "%d/%d" % (tp, n), "%+d" % (tp - bp), "%+.0f pts" % (100 * (tp - bp) / n),
                                 "yes (frozen matched cases)" if same_model else "model digest differs"))
    md += [table(("Lap", "Task", "Role", "Split", "Baseline", "Lap", "Abs change", "Rel change", "Comparable?"), rows)]
    md += ["Canary rows are out-of-scope regression checks; absence of canary rows means **not measured**, not no regression.", ""] + interp(4)

    # 5
    md += ["## " + SECTIONS[4], ""]
    res = {}
    for v in m.verdicts:
        res[v["result"]] = res.get(v["result"], 0) + 1
    runtimes = sorted({v["runtime_identity"] for v in m.verdicts})
    lims = sorted({x for v in m.verdicts for x in v["evaluator_limitations"]})
    md += [table(("Item", "Observed"), [
        ("Verdicts by result", json.dumps(res, sort_keys=True) or "none"),
        ("Verdicts with isolation verified", "%d of %d" % (sum(1 for v in m.verdicts if v["isolation_verified"]), len(m.verdicts))),
        ("Evaluator runtime identities", "; ".join(runtimes) or "none"),
        ("Attempts with no verdict", sum(1 for a in m.attempts if a["attempt_id"] not in m.verdict)),
        ("Blocked/not_run reasons", json.dumps(dict(Counter(v.get("blocked_reason", v["result"]) for v in m.verdicts if v["result"] in ("blocked", "not_run"))), sort_keys=True)),
        ("Codex fallback frequency", "not measured (no fallback event type in this schema)"),
        ("Recorded decisions", "; ".join("%s=%s by %s" % (d["decision_kind"], d["outcome"], d["reviewer_id"]) for d in m.decisions) or "none obtained"),
    ])]
    md += ["**Evaluator limitations carried by verdicts:**", ""] + ["- " + x for x in lims] + ([""] if lims else ["- none recorded", ""])
    md += ["Hash chain detects casual mutation only; it is not tamper-proof against the operator. A model never supplies result, severity, isolation or approval fields.", ""] + interp(5)

    # 6
    md += ["## " + SECTIONS[5], "", "**Reproducibility manifest (from events):**", ""]
    md += [table(("Item", "Value"), [
        ("Ledger head hash", head), ("Oracle versions", "; ".join(sorted({v["oracle_version"] for v in m.verdicts})) or "none"),
        ("Selection-rule hashes", ", ".join(sorted({l["selection_rule_sha256"][:16] for l in m.laps}))),
        ("Split-manifest hashes", ", ".join(sorted({l["split_manifest_sha256"][:16] for l in m.laps}))),
        ("Fixture hashes", len({a["fixture_sha256"] for a in m.attempts})), ("Candidate hashes", len({a["candidate_sha256"] for a in m.attempts if a["candidate_sha256"]})),
        ("Attempts without raw-output hash", sum(1 for a in m.attempts if not a["raw_output_sha256"])),
    ])] + interp(6)

    # 7
    md += ["## " + SECTIONS[6], "", "**Readiness:** " + level, ""]
    md += ["**Unmet requirements for the next level:**", ""] + ["- " + u for u in unmet] + [""]
    md += ["**Capability rows (machine-readable):**", "", "```json", json.dumps(caps, indent=2, sort_keys=True), "```", ""]
    md += ["**Human decision:** " + ("; ".join("%s: %s (%s)" % (d["decision_kind"], d["outcome"], d["reviewer_id"]) for d in m.decisions) if m.decisions else "none obtained"), ""] + interp(7)
    return "\n".join(md) + "\n", caps


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ledger", type=Path, required=True)
    p.add_argument("--artifacts", type=Path, required=True)
    p.add_argument("--experiment", required=True)
    p.add_argument("--narrative", type=Path, help="JSON {section: {author, text}}")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--capability-out", type=Path)
    a = p.parse_args(argv)
    try:
        narrative = json.loads(a.narrative.read_text(encoding="utf-8")) if a.narrative else None
        md, caps = generate(a.ledger, a.artifacts, a.experiment, narrative)
        with a.out.open("x", encoding="utf-8") as f:
            f.write(md)
        if a.capability_out:
            with a.capability_out.open("x", encoding="utf-8") as f:
                json.dump(caps, f, indent=2, sort_keys=True)
    except (ReportBlocked, OSError, ValueError) as exc:
        print("REPORT BLOCKED:", exc, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
