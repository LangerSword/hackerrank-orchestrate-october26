#!/usr/bin/env python3
"""Compare generated output with the public sample answers."""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path


def load(path: Path) -> dict:
    with path.open(newline="", encoding="utf-8") as handle:
        return {row["case_id"]: row for row in csv.DictReader(handle)}


def steps(row: dict) -> list[dict]:
    return json.loads(row["steps_json"])


def main() -> int:
    gold = load(Path(sys.argv[1] if len(sys.argv) > 1 else "dataset/sample_output.csv"))
    pred = load(Path(sys.argv[2] if len(sys.argv) > 2 else "analysis/sample_output.csv"))
    status_ok = 0
    seq_ok = 0
    field_total = field_ok = 0
    op_total = op_ok = 0
    for case_id in sorted(gold):
        g, p = gold[case_id], pred.get(case_id)
        if not p:
            print(f"MISSING {case_id}")
            continue
        gs, ps = steps(g), steps(p)
        status = g["deletion_status"] == p["deletion_status"]
        status_ok += status
        seq = gs == ps
        seq_ok += seq
        for i in range(len(gs)):
            field_total += 7
            if i < len(ps):
                field_ok += sum(1 for k in ("step_no", "phase", "system_id", "resource_id",
                                            "operation", "state", "evidence_id")
                                if gs[i].get(k) == ps[i].get(k))
                op_total += 1
                op_ok += gs[i].get("operation") == ps[i].get("operation")
        if not status or not seq:
            print(f"\n=== {case_id} status {'OK' if status else 'MISMATCH'} "
                  f"gold={g['deletion_status']} pred={p['deletion_status']}")
            print("  gold:")
            for s in gs:
                print("   ", s["step_no"], s["operation"], s["system_id"], s["resource_id"],
                      s["state"], s["evidence_id"])
            print("  pred:")
            for s in ps:
                print("   ", s["step_no"], s["operation"], s["system_id"], s["resource_id"],
                      s["state"], s["evidence_id"])
    n = len(gold)
    print(f"\nstatus {status_ok}/{n}  exact-sequence {seq_ok}/{n}  "
          f"fields {field_ok}/{field_total}  ops {op_ok}/{op_total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
