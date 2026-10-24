#!/usr/bin/env python3
"""Ghost Data Still Exists — deletion-audit agent.

Usage:
    python3 code/main.py                 # audit dataset/deletion_requests.csv -> output.csv
    python3 code/main.py --sample        # audit the public sample -> analysis/sample_output.csv
    python3 code/main.py --case case_33  # print one case's reconstructed state
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))

from audit.model import CaseResult  # noqa: E402
from audit.pipeline import AuditAgent  # noqa: E402


def natural_key(case_id: str):
    parts = case_id.split("_")
    return (parts[0], int(parts[1])) if len(parts) == 2 and parts[1].isdigit() else (case_id, 0)


def write_rows(results: list[CaseResult], path: Path) -> None:
    rows = sorted(results, key=lambda r: natural_key(r.case_id))
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["case_id", "deletion_status", "steps_json"])
        for result in rows:
            writer.writerow([
                result.case_id,
                result.status,
                json.dumps(result.steps_json(), separators=(",", ":"), sort_keys=True),
            ])


def debug_case(agent: AuditAgent, case_id: str, filename: str) -> None:
    from audit.tables import load_cases

    for case in load_cases(agent.dataset_dir, filename):
        if case.case_id != case_id:
            continue
        user = agent.identities.resolve_email(case.email)
        print(f"{case.case_id} email={case.email} user={user} audit_at={case.audit_at}")
        states = agent.states.build(user, case.audit_at)
        for state in states:
            print(f"  {state.system:22} {state.resource_id:20} {state.category:22} "
                  f"{state.state:12} {state.observed_at} {state.file_id}")
        result = agent.audit(case)
        print(f"-> {result.status}")
        for step in result.steps:
            print(f"   {step.phase:11} {step.operation:28} {step.system_id:22} "
                  f"{step.resource_id:20} {step.state:12} {step.evidence_id}")
        return
    print(f"case not found: {case_id}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", action="store_true", help="run the 32 public samples")
    parser.add_argument("--out", default="", help="output CSV path")
    parser.add_argument("--case", default="", help="debug a single case")
    parser.add_argument("--dataset", default=str(ROOT / "dataset"))
    args = parser.parse_args()

    dataset = Path(args.dataset)
    digest = ROOT / "code" / "audit" / "digests" / "documents.json"
    agent = AuditAgent(dataset, digest)
    filename = "sample_deletion_requests.csv" if args.sample else "deletion_requests.csv"

    if args.case:
        debug_case(agent, args.case, filename)
        return 0

    results = agent.run_all(filename)
    out = Path(args.out) if args.out else (
        ROOT / ("analysis/sample_output.csv" if args.sample else "output.csv")
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    write_rows(results, out)
    counts: dict[str, int] = {}
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1
    print(f"wrote {len(results)} rows to {out}")
    print("status:", json.dumps(counts, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
