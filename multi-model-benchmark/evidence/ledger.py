"""Append-only, hash-chained JSONL ledger with strict schema and cross-event checks.

The hash chain detects casual mutation. It is NOT tamper-proof: whoever controls the
files can rewrite the whole chain. Producer roles are labels enforced by the append
API, not authentication.
"""
import datetime
try:
    import fcntl
except ImportError:  # Windows: separate single-byte file lock via msvcrt
    fcntl = None
    import msvcrt
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import re
import uuid

SCHEMA_VERSION = 1
EVENT_TYPES = ("lap", "attempt", "verdict", "decision")
PRODUCER_FOR = {"lap": "controller", "attempt": "orchestrator",
                "verdict": "trusted_evaluator", "decision": "reviewer"}
RESULTS = ("pass", "fail", "not_run", "not_applicable", "blocked")
FAILURE_CATEGORIES = ("none", "invalid_output", "blender_api", "rig_space", "deformation",
                      "morph", "retarget", "timeout", "resource", "sandbox", "integrity",
                      "evaluator", "unsupported")
SEVERITIES = ("none", "minor", "major", "critical")
SPLITS = ("dev", "validation", "holdout")
ROLES = ("target", "canary")
FIXTURE_KINDS = ("synthetic", "real")
DECISION_KINDS = ("sol_light_review", "human_gate")
DECISION_OUTCOMES = ("approved", "rejected", "changes_requested")
GENERATION_STATUS = ("produced", "inference_error")

COMMON = ("schema_version", "event_id", "event_type", "experiment_id", "created_at_utc",
          "producer", "previous_event_hash", "event_hash")
SHA = re.compile(r"[0-9a-f]{64}\Z")

# name -> (kind, nullable). kinds: str sha str_or_none int num bool list dict enum:<tuple>
_NUM = "num"
REQUIRED = {
    "lap": {"lap_id": ("str", False), "parent_lap_id": ("str", True), "task_id": ("str", False),
            "change_reason": ("str", False), "selection_rule_sha256": ("sha", False),
            "split_manifest_sha256": ("sha", False), "cases_consulted_for_change": ("list", False)},
    "attempt": {"attempt_id": ("str", False), "lap_id": ("str", False), "trial_id": ("str", False),
                "attempt_no": ("int", False), "task_id": ("str", False), "stage": ("str", True),
                "case_id": ("str", False), "source_family": ("str", False),
                "split": (SPLITS, False), "role": (ROLES, False),
                "fixture_kind": (FIXTURE_KINDS, False), "fixture_sha256": ("sha", False),
                "model_digest": ("str", False), "prompt_sha256": ("sha", False),
                "template_sha256": ("sha", True), "raw_output_sha256": ("sha", True),
                "candidate_sha256": ("sha", True), "generation_status": (GENERATION_STATUS, False),
                "seed": ("int", True), "temperature": (_NUM, False), "num_ctx": ("int", False),
                "reasoning_mode": ("str", False), "input_tokens": ("int", True),
                "output_tokens": ("int", True), "inference_seconds": (_NUM, True)},
    "verdict": {"attempt_id": ("str", False), "candidate_sha256": ("sha", True),
                "fixture_sha256": ("sha", False), "oracle_version": ("str", False),
                "runtime_identity": ("str", False), "result": (RESULTS, False),
                "failure_category": (FAILURE_CATEGORIES, False), "severity": (SEVERITIES, False),
                "severe_regression": ("bool", False), "evidence_sha256": ("sha", True),
                "evidence_path": ("str", True), "wall_seconds": (_NUM, True),
                "isolation_verified": ("bool", False), "evaluator_limitations": ("list", False),
                "reason": ("text", False), "reevaluation_of": ("str", True)},
    "decision": {"decision_kind": (DECISION_KINDS, False), "outcome": (DECISION_OUTCOMES, False),
                 "reviewer_id": ("str", False), "review_evidence_sha256": ("sha", False),
                 "scope": ("str", False)},
}
OPTIONAL = {
    "lap": {"selection_rule_id": ("str", False), "environment": ("dict", False),
            "holdout_final_eval": ("bool", False)},
    "attempt": {"model_tag": ("str", False), "asset_track": (("pmx_vmd", "blender_native"), False),
                "license_record_sha256": ("sha", False),
                "final_eval_selection_rule_sha256": ("sha", False)},
    "verdict": {"peak_rss_mb": (_NUM, True), "peak_vram_mb": (_NUM, True),
                "blocked_reason": ("str", False)},
    "decision": {},
}
FORBIDDEN_ANYWHERE = {"first_try", "qualified", "human_approved", "sol_light_reviewed"}
FORBIDDEN_OUTSIDE_VERDICT = {"result", "severity", "blender_executed", "blender_pass"}


class LedgerError(ValueError):
    pass


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def event_hash(event):
    body = {k: v for k, v in event.items() if k != "event_hash"}
    return hashlib.sha256(canonical(body)).hexdigest()


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def fixture_hash(case):
    """Identical to multi-model-benchmark/runner.py's fixture_sha256."""
    return hashlib.sha256(json.dumps(case, sort_keys=True).encode()).hexdigest()


def _no_constants(name):
    raise ValueError("non-finite JSON constant: " + name)


def loads_strict(text):
    return json.loads(text, parse_constant=_no_constants)


def _type_ok(kind, nullable, v):
    if v is None:
        return nullable
    if isinstance(kind, tuple):
        return isinstance(v, str) and v in kind
    if kind == "str":
        return isinstance(v, str) and bool(v)
    if kind == "text":
        return isinstance(v, str)
    if kind == "sha":
        return isinstance(v, str) and bool(SHA.fullmatch(v))
    if kind == "int":
        return isinstance(v, int) and not isinstance(v, bool)
    if kind == _NUM:
        return isinstance(v, (int, float)) and not isinstance(v, bool) and v == v and abs(v) != float("inf")
    if kind == "bool":
        return isinstance(v, bool)
    if kind == "list":
        return isinstance(v, list) and all(isinstance(x, str) for x in v)
    if kind == "dict":
        return isinstance(v, dict) and all(isinstance(k, str) and isinstance(x, (str, int, float, bool)) for k, x in v.items())
    return False


def validate_event_schema(ev):
    """Pure schema check for one event; returns a list of violation strings."""
    errs = []
    if not isinstance(ev, dict):
        return ["event is not an object"]
    et = ev.get("event_type")
    if et not in EVENT_TYPES:
        return ["unknown event_type: %r" % (et,)]
    if ev.get("schema_version") != SCHEMA_VERSION:
        errs.append("unsupported schema_version")
    for k in ("event_id", "experiment_id", "created_at_utc"):
        if not _type_ok("str", False, ev.get(k)):
            errs.append("missing/invalid " + k)
    if ev.get("producer") != PRODUCER_FOR[et]:
        errs.append("producer %r not allowed for %s (expected %s)" % (ev.get("producer"), et, PRODUCER_FOR[et]))
    if "previous_event_hash" not in ev or not _type_ok("sha", True, ev.get("previous_event_hash")):
        errs.append("missing/invalid previous_event_hash")
    if not _type_ok("sha", False, ev.get("event_hash")):
        errs.append("missing/invalid event_hash")
    specs = dict(REQUIRED[et])
    specs.update(OPTIONAL[et])
    allowed = set(COMMON) | set(specs)
    for k in ev:
        if k in FORBIDDEN_ANYWHERE or (et != "verdict" and k in FORBIDDEN_OUTSIDE_VERDICT):
            errs.append("forbidden field (not supplied by this producer): " + k)
        elif k not in allowed:
            errs.append("unknown field: " + k)
    for k, (kind, nullable) in REQUIRED[et].items():
        if k not in ev:
            errs.append("missing field: " + k)
        elif not _type_ok(kind, nullable, ev[k]):
            errs.append("invalid value for " + k)
    for k, (kind, nullable) in OPTIONAL[et].items():
        if k in ev and not _type_ok(kind, nullable, ev[k]):
            errs.append("invalid value for " + k)
    if et == "attempt" and isinstance(ev.get("attempt_no"), int) and ev["attempt_no"] < 1:
        errs.append("attempt_no must be >= 1")
    if et == "verdict" and not errs:
        if ev["result"] == "pass" and (ev["failure_category"] != "none" or ev["severity"] != "none"
                                       or not ev["evidence_sha256"] or not ev["candidate_sha256"]
                                       or not ev["isolation_verified"]):
            errs.append("pass requires candidate hash, evidence hash, verified isolation, no failure")
        if ev["result"] in ("not_run", "blocked", "not_applicable") and ev["severity"] == "critical":
            errs.append("severity critical requires an executed fail")
        if ev["severe_regression"] and ev["severity"] != "critical":
            errs.append("severe_regression requires severity critical")
    return errs


def validate_events(events, artifacts=None):
    """Chain + cross-event semantics. Returns violation strings (empty list = valid)."""
    errs = []
    prev = None
    ids = set()
    laps, attempts, verdict_by_attempt, verdict_ids = {}, {}, {}, {}
    trial_seq = {}
    case_identity, task_stage = {}, {}
    for i, ev in enumerate(events):
        tag = "event[%d]" % i
        schema = validate_event_schema(ev)
        errs.extend(tag + ": " + e for e in schema)
        if schema:
            prev = ev.get("event_hash") if isinstance(ev, dict) else None
            continue
        if ev["previous_event_hash"] != prev:
            errs.append(tag + ": broken hash chain (previous_event_hash mismatch)")
        if event_hash(ev) != ev["event_hash"]:
            errs.append(tag + ": event_hash does not match content")
        prev = ev["event_hash"]
        if ev["event_id"] in ids:
            errs.append(tag + ": duplicate event_id " + ev["event_id"])
        ids.add(ev["event_id"])
        et = ev["event_type"]
        if et == "lap":
            if ev["lap_id"] in laps:
                errs.append(tag + ": duplicate lap_id")
            p = ev["parent_lap_id"]
            if p is not None and p not in laps:
                errs.append(tag + ": parent_lap_id not defined earlier")
            previous_laps = [l for l in laps.values() if l["experiment_id"] == ev["experiment_id"]]
            if previous_laps and any(l["selection_rule_sha256"] != ev["selection_rule_sha256"]
                                     or l["split_manifest_sha256"] != ev["split_manifest_sha256"] for l in previous_laps):
                errs.append(tag + ": split manifest or lap-selection rule changed after freeze")
            if ev.get("holdout_final_eval") and (p is None or laps.get(p, {}).get("experiment_id") != ev["experiment_id"]):
                errs.append(tag + ": final holdout lap must have prior same-experiment parent")
            laps[ev["lap_id"]] = ev
        elif et == "attempt":
            if ev["attempt_id"] in attempts:
                errs.append(tag + ": duplicate attempt_id (replay is not an extra attempt)")
            lap = laps.get(ev["lap_id"])
            if lap is None:
                errs.append(tag + ": attempt references undefined lap")
            elif lap["experiment_id"] != ev["experiment_id"]:
                errs.append(tag + ": attempt references another experiment's lap")
            elif lap["task_id"] != ev["task_id"] and ev["role"] == "target":
                errs.append(tag + ": target attempt task_id differs from its lap task_id")
            key = (ev["experiment_id"], ev["lap_id"], ev["trial_id"], ev["case_id"])
            expect = trial_seq.get(key, 0) + 1
            if ev["attempt_no"] != expect:
                errs.append(tag + ": attempt_no %d not monotonic (expected %d)" % (ev["attempt_no"], expect))
            trial_seq[key] = ev["attempt_no"]
            ident = (ev["task_id"], ev["stage"], ev["source_family"], ev["fixture_sha256"], ev["split"])
            if case_identity.setdefault((ev["experiment_id"], ev["case_id"]), ident) != ident:
                errs.append(tag + ": case_id %s has conflicting task/stage/family/fixture/split" % ev["case_id"])
            if task_stage.setdefault((ev["experiment_id"], ev["task_id"]), ev["stage"]) != ev["stage"]:
                errs.append(tag + ": task_id %s has conflicting stage" % ev["task_id"])
            if ev["generation_status"] == "produced" and ev["candidate_sha256"] is None:
                pass  # model produced no usable code; handled as not_run by the bridge
            attempts[ev["attempt_id"]] = ev
            if artifacts is not None and ev["raw_output_sha256"] is not None:
                if not artifacts.exists("raw_outputs", ev["raw_output_sha256"], ".txt"):
                    errs.append(tag + ": raw model output missing or corrupted")
        elif et == "verdict":
            a = attempts.get(ev["attempt_id"])
            if a is None:
                errs.append(tag + ": orphan verdict (no earlier attempt)")
            else:
                if ev["experiment_id"] != a["experiment_id"]:
                    errs.append(tag + ": verdict references another experiment")
                if ev["candidate_sha256"] != a["candidate_sha256"]:
                    errs.append(tag + ": verdict candidate hash differs from attempt")
                if ev["fixture_sha256"] != a["fixture_sha256"]:
                    errs.append(tag + ": verdict fixture hash differs from attempt")
                prior = verdict_by_attempt.get(ev["attempt_id"])
                if prior is not None and ev["reevaluation_of"] != prior["event_id"]:
                    errs.append(tag + ": second verdict for attempt without explicit reevaluation_of")
                if prior is None and ev["reevaluation_of"] is not None:
                    errs.append(tag + ": reevaluation_of set but no prior verdict")
                if ev["result"] == "pass" and a["generation_status"] != "produced":
                    errs.append(tag + ": pass for an attempt with no produced candidate")
                verdict_by_attempt[ev["attempt_id"]] = ev
            verdict_ids[ev["event_id"]] = ev
            if artifacts is not None and ev["evidence_sha256"]:
                if not artifacts.exists("evidence", ev["evidence_sha256"], ".json"):
                    errs.append(tag + ": evidence artifact missing or hash mismatch")
                elif ev["result"] == "pass" and a is not None:
                    # A pass requires independently supplied TWO-PROCESS evidence,
                    # not only a hand-written success flag or legacy oracle output.
                    try:
                        receipt = loads_strict(artifacts.get("evidence", ev["evidence_sha256"], ".json").decode("utf-8"))
                        witness = receipt.get("trusted_verifier_result", {})
                        ok = (receipt.get("builder_exit_code") == 0
                              and receipt.get("verifier_exit_code") == 0
                              and receipt.get("timed_out") is False
                              and witness.get("verifier_phase") == "fresh_process_no_candidate_exec"
                              and witness.get("blender_executed") is True
                              and witness.get("blender_pass") is True
                              and witness.get("source_sha256") == ev["candidate_sha256"]
                              and witness.get("fixture_sha256") == ev["fixture_sha256"]
                              and witness.get("oracle_sha256") in ev["oracle_version"]
                              and witness.get("case_id") == a["case_id"]
                              and witness.get("stage") == a["stage"])
                        if not ok:
                            errs.append(tag + ": pass lacks independently bound two-process verifier receipt")
                    except (ValueError, TypeError, UnicodeError, AttributeError):
                        errs.append(tag + ": pass receipt is not valid trusted evidence")
        elif et == "decision":
            if artifacts is not None and not artifacts.exists("reviews", ev["review_evidence_sha256"], ""):
                errs.append(tag + ": review evidence artifact missing or hash mismatch (approval not evidenced)")
    return errs


def compromised_holdout_cases(events):
    """Holdout cases that were consulted during development or run without final-eval authorization."""
    laps = {e["lap_id"]: e for e in events if e.get("event_type") == "lap"}
    out = {}
    for e in events:
        if e.get("event_type") == "lap":
            for c in e["cases_consulted_for_change"]:
                out.setdefault(c, "consulted_for_change in " + e["lap_id"])
    for e in events:
        if e.get("event_type") == "attempt" and e["split"] == "holdout":
            lap = laps.get(e["lap_id"])
            ok = (lap is not None and lap.get("holdout_final_eval") is True
                  and e.get("final_eval_selection_rule_sha256") == lap["selection_rule_sha256"])
            if not ok:
                out.setdefault(e["case_id"], "holdout run without final-eval authorization in " + e["lap_id"])
    return out


class ArtifactStore:
    """Content-addressed, write-once artifact directory (ignored by git under data/)."""

    def __init__(self, root):
        self.root = Path(root)

    def _path(self, kind, sha, ext):
        if not SHA.fullmatch(sha) or not re.fullmatch(r"[a-z_]+", kind) or not re.fullmatch(r"(\.[a-z0-9]+)?", ext):
            raise LedgerError("bad artifact address")
        return self.root / kind / (sha + ext)

    def put(self, kind, data, ext=""):
        sha = sha256_bytes(data)
        p = self._path(kind, sha, ext)
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.exists():
            if sha256_bytes(p.read_bytes()) != sha:
                raise LedgerError("artifact collision/corruption at " + str(p))
            return sha
        with p.open("xb") as f:
            f.write(data)
        p.chmod(0o444)
        return sha

    def get(self, kind, sha, ext=""):
        p = self._path(kind, sha, ext)
        if p.is_symlink() or not p.is_file():
            raise LedgerError("artifact missing: %s/%s" % (kind, sha))
        data = p.read_bytes()
        if sha256_bytes(data) != sha:
            raise LedgerError("artifact hash mismatch: %s/%s" % (kind, sha))
        return data

    def exists(self, kind, sha, ext=""):
        try:
            self.get(kind, sha, ext)
            return True
        except LedgerError:
            return False


@contextmanager
def _locked_file(fh):
    """Exclusive cross-process lock for a dedicated lock file.

    Producer labels are NOT proof of reviewer identity.
    """
    if fcntl is not None:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)
    else:
        fh.seek(0)
        if fh.read(1) != b"\0":
            fh.seek(0)
            fh.write(b"\0")
            fh.flush()
        fh.seek(0)
        msvcrt.locking(fh.fileno(), msvcrt.LK_LOCK, 1)
        try:
            yield
        finally:
            fh.seek(0)
            msvcrt.locking(fh.fileno(), msvcrt.LK_UNLCK, 1)


class Ledger:
    def __init__(self, path, clock=None):
        self.path = Path(path)
        self.clock = clock or (lambda: datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

    def read(self):
        if not self.path.exists():
            return []
        events = []
        for n, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                events.append(loads_strict(line))
            except ValueError as exc:
                raise LedgerError("line %d is not valid strict JSON: %s" % (n, exc))
        return events

    def verify(self, artifacts=None):
        return validate_events(self.read(), artifacts)

    def append(self, event_type, role, experiment_id, fields, *, artifacts=None, event_id=None):
        """Append one event after validating it against the whole ledger. Refuses on any violation."""
        if event_type not in EVENT_TYPES:
            raise LedgerError("unknown event type")
        if PRODUCER_FOR[event_type] != role:
            raise LedgerError("role %r may not append %s events" % (role, event_type))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Use a separate lock file so locks survive atomic readers and work
        # under Windows' msvcrt API as well as POSIX fcntl.
        with self.path.with_suffix(self.path.suffix + ".lock").open("a+b") as lock_fh:
            with _locked_file(lock_fh), self.path.open("a+b") as fh:
                fh.seek(0)
                text = fh.read().decode("utf-8")
                events = [loads_strict(l) for l in text.splitlines() if l.strip()]
                existing = validate_events(events, artifacts)
                if existing:
                    raise LedgerError("ledger already invalid; refusing append: " + "; ".join(existing[:3]))
                ev = {"schema_version": SCHEMA_VERSION, "event_id": event_id or (event_type + "-" + uuid.uuid4().hex[:16]),
                      "event_type": event_type, "experiment_id": experiment_id,
                      "created_at_utc": self.clock(), "producer": role,
                      "previous_event_hash": events[-1]["event_hash"] if events else None}
                ev.update(fields)
                ev["event_hash"] = event_hash(ev)
                errs = validate_events(events + [ev], artifacts)
                if errs:
                    raise LedgerError("; ".join(errs))
                fh.seek(0, 2)
                fh.write(json.dumps(ev, sort_keys=True, ensure_ascii=False, allow_nan=False).encode("utf-8") + b"\n")
                fh.flush()
                import os
                os.fsync(fh.fileno())
                return ev
