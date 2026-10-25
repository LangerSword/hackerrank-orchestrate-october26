#!/usr/bin/env python3
"""Fail if a retracted claim is back in the judge-facing docs.

Also checks the headline numbers in README against a fresh output. Run this in
verify_package.py and before every submission.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = [
    ROOT / "README.md",
    ROOT / "code/README.md",
    ROOT / "code/evaluation/evaluation_report.md",
    ROOT / "code/evaluation/usage_report.md",
    ROOT / "docs/DECISIONS.md",
    ROOT / "docs/FLIP_LEDGER.md",
    ROOT / "docs/BREAKEVEN.md",
    ROOT / "docs/CASE_WALKTHROUGHS.md",
]

BANNED = [
    "191/518", "36.9%", "likely extras", "27 slots", "27 omitted",
    "166/193", "12/12", "0.925", "1024/1351", "75.8%",
    "18 deleted", "152 COMPLETE", "356 INCOMPLETE", "be792f",
    "OCR is legible", "138 mismatch", "underivable", "0 flags",
]


def fail(message: str) -> None:
    print("CLAIMS FAIL:", message)
    raise SystemExit(1)


def main() -> int:
    for path in DOCS:
        text = path.read_text(encoding="utf-8").lower()
        for phrase in BANNED:
            if phrase.lower() in text:
                fail(f"{path.relative_to(ROOT)} contains retracted phrase {phrase!r}")

    output = list(csv.DictReader((ROOT / "output.csv").open(newline="", encoding="utf-8")))
    counts = {"COMPLETE": 0, "INCOMPLETE": 0, "NOT_APPLICABLE": 0}
    for row in output:
        counts[row["deletion_status"]] = counts.get(row["deletion_status"], 0) + 1
    if counts != {"COMPLETE": 153, "INCOMPLETE": 355, "NOT_APPLICABLE": 10}:
        fail(f"full status counts are {counts}")

    gold = {r["case_id"]: r for r in
            csv.DictReader((ROOT / "dataset/sample_output.csv").open(newline="", encoding="utf-8"))}
    pred = {r["case_id"]: r for r in
            csv.DictReader((ROOT / "analysis/sample_output.csv").open(newline="", encoding="utf-8"))}
    status = steps = fields = total = 0
    for case_id, g in gold.items():
        p = pred.get(case_id)
        if not p:
            continue
        status += g["deletion_status"] == p["deletion_status"]
        gs, ps = json.loads(g["steps_json"]), json.loads(p["steps_json"])
        steps += sum(1 for i in range(len(gs)) if i < len(ps))
        for i in range(max(len(gs), len(ps))):
            gstep = gs[i] if i < len(gs) else {}
            pstep = ps[i] if i < len(ps) else {}
            for key in ("step_no", "phase", "system_id", "resource_id",
                        "operation", "state", "evidence_id"):
                total += 1
                fields += gstep.get(key) == pstep.get(key)
    if status != 32 or steps != 167 or fields != 1033 or total != 1351:
        fail(f"sample metrics are status={status}/32 steps={steps}/193 "
             f"fields={fields}/{total}")

    digest = hashlib.sha256((ROOT / "output.csv").read_bytes()).hexdigest()
    expected = "93eb70b7f428ddb1487fe379f5329ff964129c85a769483e6094cf29faa9891c"
    if digest != expected:
        fail(f"output hash is {digest}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for needle in (expected, "167/193", "153 COMPLETE", "355 INCOMPLETE", "15/15"):
        if needle not in readme:
            fail(f"README does not contain {needle!r}")

    print(f"CLAIMS OK  sample {status}/32, {steps}/193, fields {fields}/{total}; "
          f"full 153/355/10; hash {digest[:12]}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
