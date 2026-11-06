"""Frozen, family-separated experiment splits; JSON artifact is content addressed.

A manifest is data, not authorization to peek at holdouts. The CLI additionally
requires an explicit final-evaluation action and an independently selected lap.
"""
import json
from .ledger import LedgerError

SPLITS = {"dev", "validation", "holdout"}


def parse_manifest(raw):
    try:
        doc = json.loads(raw)
    except (ValueError, UnicodeDecodeError) as exc:
        raise LedgerError("split manifest must be UTF-8 JSON: " + str(exc)) from exc
    if not isinstance(doc, dict) or doc.get("schema_version") != 1 or not isinstance(doc.get("cases"), list):
        raise LedgerError("split manifest requires schema_version=1 and cases list")
    if not doc["cases"]:
        raise LedgerError("empty split manifest")
    found = {}
    families = {}
    for row in doc["cases"]:
        if not isinstance(row, dict):
            raise LedgerError("split manifest row must be object")
        case, split, family = row.get("case_id"), row.get("split"), row.get("source_family")
        if not all(isinstance(x, str) and x for x in (case, family)) or split not in SPLITS:
            raise LedgerError("invalid split row case/family/split")
        if case in found:
            raise LedgerError("duplicate split case_id: " + case)
        if family in families and families[family] != split:
            raise LedgerError("source_family leaked across split boundaries: " + family)
        found[case] = (split, family)
        families[family] = split
    return found


def enforce_case_split(cases, labels, selected_split):
    for case in cases:
        ident = labels.get(case["case_id"])
        if ident is None:
            raise LedgerError("case missing from pinned split manifest: " + case["case_id"])
        family = case.get("fixture_family") or case.get("source_family") or "unknown"
        if ident != (selected_split, family):
            raise LedgerError("split manifest mismatch for %s: %r vs (%s,%s)" %
                              (case["case_id"], ident, selected_split, family))


def main(argv=None):
    """Create a development-only split manifest from generated synthetic fixtures.

    Independent real-model splits must be carefully curated, not automatically
    inferred from parametric synthetic variants.
    """
    import argparse
    from pathlib import Path
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cases", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)
    rows = []
    for line in args.cases.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        c = json.loads(line)
        if not c.get("synthetic") or not isinstance(c.get("fixture_family"), str):
            raise LedgerError("development-only generator accepts only labeled synthetic fixtures")
        rows.append({"case_id": c["case_id"], "source_family": c["fixture_family"], "split": "dev"})
    doc = {"schema_version": 1, "cases": rows}
    encoded = (json.dumps(doc, sort_keys=True, indent=2) + "\n").encode()
    parse_manifest(encoded)
    with args.out.open("xb") as f:
        f.write(encoded)
    print("Frozen development-only split manifest:", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
