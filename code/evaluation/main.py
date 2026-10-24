#!/usr/bin/env python3
"""Evaluation workflow: sample gate + contract validator + metric summary."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))
from audit.validate import validate_submission  # noqa: E402


def rows(path: Path) -> dict:
    with path.open(newline="") as f:
        return {r["case_id"]: r for r in csv.DictReader(f)}


def main() -> int:
    gold = rows(ROOT / "dataset/sample_output.csv")
    pred = rows(ROOT / "analysis/sample_output.csv")
    status = seq = 0
    fields = total = 0
    for cid, g in gold.items():
        p = pred.get(cid)
        if not p:
            continue
        status += g["deletion_status"] == p["deletion_status"]
        gs, ps = json.loads(g["steps_json"]), json.loads(p["steps_json"])
        seq += gs == ps
        for i in range(max(len(gs), len(ps))):
            gstep = gs[i] if i < len(gs) else {}
            pstep = ps[i] if i < len(ps) else {}
            for key in ("step_no", "phase", "system_id", "resource_id",
                        "operation", "state", "evidence_id"):
                total += 1
                fields += gstep.get(key) == pstep.get(key)
    report = validate_submission(ROOT / "output.csv",
                                 ROOT / "dataset/deletion_requests.csv",
                                 ROOT / "dataset/evidence_files.csv")
    print(f"sample status {status}/{len(gold)} | exact sequence {seq}/{len(gold)} "
          f"| fields {fields}/{total}")
    print(f"full run: {report.metrics} | validator errors {len(report.errors)}")
    for error in report.errors[:10]:
        print("  ", error)
    return 0 if report.ok and status == len(gold) else 1


if __name__ == "__main__":
    raise SystemExit(main())
