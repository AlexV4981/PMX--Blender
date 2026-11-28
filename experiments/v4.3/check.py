"""Structural validation only; never grants permissions, qualification or approvals."""
import argparse
import json
from pathlib import Path
import re

def nonempty(value):
    return isinstance(value, str) and bool(value.strip())

def validate(data, kind):
    if not isinstance(data, dict) or type(data.get("schema")) is not int or data["schema"] != 1:
        raise ValueError("Expected schema 1")
    key = {"cases":"cases", "scenarios":"scenarios", "permissions":"assets"}[kind]
    rows = data.get(key)
    if not isinstance(rows,list) or not rows:
        raise ValueError("Nonempty row list required")
    seen = set()
    for row in rows:
        if not isinstance(row,dict) or not nonempty(row.get("id")) or row["id"] in seen:
            raise ValueError("Unique nonempty ID required")
        seen.add(row["id"])
        if kind == "cases":
            for k in ("symptom","applicability","procedure","limitations"):
                if not nonempty(row.get(k)):
                    raise ValueError("Missing "+k)
            if not isinstance(row.get("tags"),list) or not row["tags"] or not all(nonempty(x) for x in row["tags"]):
                raise ValueError("Tags required")
            if row.get("status") not in ("candidate","verified","retired"):
                raise ValueError("Invalid case status")
            evidence = row.get("evidence")
            if not isinstance(evidence,list):
                raise ValueError("Evidence list required")
            if row["status"] == "verified":
                if not evidence or not all(isinstance(x,dict) and nonempty(x.get("ref")) and isinstance(x.get("sha256"),str) and re.fullmatch(r"[0-9a-f]{64}",x["sha256"]) for x in evidence):
                    raise ValueError("Verified case needs evidence references and hashes")
                for k in ("reproduction","distinguishing_test","protected_checks","observed_result","environment"):
                    if not nonempty(row.get(k)):
                        raise ValueError("Verified case missing "+k)
        elif kind == "scenarios":
            if not all(nonempty(row.get(k)) for k in ("input","expected","forbidden")):
                raise ValueError("Incomplete scenario")
        else:
            if not isinstance(row.get("license_evidence"),list):
                raise ValueError("License evidence list required")
            for k in ("private_use","modification","redistribution","training"):
                if row.get(k) not in ("allowed","prohibited","unknown"):
                    raise ValueError("Invalid permission: "+k)
                if row[k] == "allowed" and not (nonempty(row.get("creator")) and nonempty(row.get("source")) and any(isinstance(e,dict) and e.get("use")==k and nonempty(e.get("ref")) for e in row["license_evidence"])):
                    raise ValueError("Allowed use requires use-specific evidence")
    return {"structural_status":"valid", "rows":len(rows), "qualification":"not performed"}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("kind",choices=("cases","scenarios","permissions"))
    p.add_argument("file",type=Path)
    args=p.parse_args()
    try:
        print(json.dumps(validate(json.loads(args.file.read_text(encoding="utf-8")),args.kind)))
    except (ValueError,OSError) as e:
        p.exit(2,str(e)+"\n")

if __name__ == "__main__":
    main()
