#!/usr/bin/env python3
"""Check that in-window sync/restore activity is covered by output steps.

The engine does not use activity SUCCESS as proof. This audit answers the
narrower question: for every subject-linked sync or restore activity inside a
case window, does the output already contain a step for that resource? If yes,
the activity adds no missed case; it is a claim already backed by evidence.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))

from audit.model import parse_ts  # noqa: E402
from audit.pipeline import AuditAgent  # noqa: E402
from audit.tables import load_cases  # noqa: E402

EVENTS = ("SYNC_RECORD", "CHECK_DATA_FLOW", "CHECK_RESTORE_ACCESS",
          "BLOCK_RESTORE", "DISABLE_DATA_FLOW", "RESTORE_BACKUP")


def main() -> int:
    agent = AuditAgent(ROOT / "dataset", ROOT / "code/audit/digests/documents.json")
    cases = load_cases(ROOT / "dataset", "deletion_requests.csv")
    by_user: dict[str, list] = defaultdict(list)
    for case in cases:
        by_user[agent.identities.resolve_email(case.email)].append(case)

    output = {row["case_id"]: row for row in
              csv.DictReader((ROOT / "output.csv").open(newline="", encoding="utf-8"))}
    resources = {
        case_id: {step.get("resource_id") for step in json.loads(row["steps_json"])}
        for case_id, row in output.items()
    }
    rows = list(csv.DictReader((ROOT / "dataset/system_activity.csv").open(
        newline="", encoding="utf-8")))

    totals: Counter = Counter()
    in_window: Counter = Counter()
    covered: Counter = Counter()
    missed: list[tuple[str, str, str, str, str]] = []
    for row in rows:
        event = row["event_type"]
        if event not in EVENTS:
            continue
        totals[event] += 1
        resource = row["resource_id"]
        when = parse_ts(row["event_time"])
        users = (agent.index.resource_users.get((row["target_system"], resource), set())
                 | agent.index.resource_users.get((row["source_system"], resource), set()))
        for user in users:
            for case in by_user.get(user, []):
                if not (case.requested_at <= when <= case.audit_at):
                    continue
                in_window[event] += 1
                if resource in resources.get(case.case_id, set()):
                    covered[event] += 1
                else:
                    missed.append((event, case.case_id, resource,
                                   output[case.case_id]["deletion_status"], row["activity_id"]))
                break
            else:
                continue
            break

    print(f"{'event':24} {'total':>6} {'in-window':>10} {'covered':>8} {'missed':>7}")
    for event in EVENTS:
        print(f"{event:24} {totals[event]:6} {in_window[event]:10} "
              f"{covered[event]:8} {in_window[event] - covered[event]:7}")
    for event, case_id, resource, status, activity in missed[:10]:
        print(f"  MISS {event} {case_id} {resource} status={status} activity={activity}")
    return 0 if not missed else 1


if __name__ == "__main__":
    raise SystemExit(main())
