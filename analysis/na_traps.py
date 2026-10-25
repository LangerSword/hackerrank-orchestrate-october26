#!/usr/bin/env python3
"""Map the 10 NOT_APPLICABLE rows to the contract's non-deletion trap types."""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# case_id -> (trap type, marker that should appear in request_text)
TRAPS = {
    "case_533": ("correction", "replace it"),
    "case_534": ("marketing opt-out", "stop the promotional emails"),
    "case_535": ("portability", "download my account information"),
    "case_536": ("login support", "resetting the login"),
    "case_537": ("correction", "misspelled"),
    "case_538": ("marketing opt-out", "marketing lists only"),
    "case_539": ("access", "information request"),
    "case_540": ("portability", "copy of last year's invoices"),
    "case_541": ("correction", "change the email address"),
    "case_542": ("access", "copy of the information"),
}


def main() -> int:
    requests = {row["case_id"]: row["request_text"] for row in
                csv.DictReader((ROOT / "dataset/deletion_requests.csv").open(
                    newline="", encoding="utf-8"))}
    output = list(csv.DictReader((ROOT / "output.csv").open(
        newline="", encoding="utf-8")))
    na = {row["case_id"] for row in output if row["deletion_status"] == "NOT_APPLICABLE"}
    if na != set(TRAPS):
        print(f"NOT_APPLICABLE set mismatch: {sorted(na ^ set(TRAPS))}")
        return 1

    counts = Counter()
    print(f"{'case':10} {'type':18} marker")
    for case_id in sorted(TRAPS):
        kind, marker = TRAPS[case_id]
        text = requests[case_id]
        if marker.lower() not in text.lower():
            print(f"{case_id}: missing marker {marker!r}")
            return 1
        counts[kind] += 1
        print(f"{case_id:10} {kind:18} {marker}")
    print()
    print("type distribution:", dict(sorted(counts.items())))
    print(f"exposure bound: 10 / {len(output)} rows = {10/len(output):.1%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
