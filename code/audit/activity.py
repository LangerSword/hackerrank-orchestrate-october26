"""Corroborate system_activity rows against the fact store.

Activity rows are claims, never state evidence. This module answers a narrower
question: for each in-window activity about one of the subject's resources, does
the evidence corroborate it, contradict it, or leave it unresolved? It changes
no output.
"""
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .model import Case, Fact, parse_ts

EVENTS = {
    "SYNC_RECORD", "CHECK_DATA_FLOW", "DISABLE_DATA_FLOW",
    "CHECK_RESTORE_ACCESS", "BLOCK_RESTORE", "RESTORE_BACKUP",
}
CORROBORATES = "CORROBORATES"
CONTRADICTED = "CONTRADICTED"
UNRESOLVED = "UNRESOLVED"
EXCLUDED_POST_AUDIT = "EXCLUDED_POST_AUDIT"


@dataclass
class ActivityResult:
    case_id: str
    activity_id: str
    event_type: str
    resource_id: str
    event_time: datetime
    verdict: str
    reason: str


class ActivityAudit:
    def __init__(self, dataset_dir: Path, index, identities, cases: list[Case]) -> None:
        self.dataset_dir = Path(dataset_dir)
        self.index = index
        self.identities = identities
        self.cases_by_user: dict[str, list[Case]] = defaultdict(list)
        for case in cases:
            self.cases_by_user[self.identities.resolve_email(case.email)].append(case)
        self.facts_by_resource: dict[str, list[Fact]] = defaultdict(list)
        for fact in self.index.facts:
            self.facts_by_resource[fact.resource_id].append(fact)
        for group in self.facts_by_resource.values():
            group.sort(key=lambda fact: fact.observed_at)
        self.rows = []
        path = self.dataset_dir / "system_activity.csv"
        if path.exists():
            with path.open(newline="", encoding="utf-8") as handle:
                self.rows = list(csv.DictReader(handle))
        self.results: list[ActivityResult] = []
        self.run()

    def _case_for(self, users: set[str], when: datetime,
                  include_post: bool = False) -> Case | None:
        for user in users:
            for case in self.cases_by_user.get(user, []):
                if case.requested_at <= when <= case.audit_at:
                    return case
                if include_post and when > case.audit_at:
                    return case
        return None

    def _state_after(self, resource: str, when: datetime) -> str:
        facts = [f for f in self.facts_by_resource.get(resource, [])
                 if f.observed_at >= when]
        if not facts:
            return ""
        return facts[-1].state

    def _classify(self, event: str, resource: str, when: datetime) -> tuple[str, str]:
        state = self._state_after(resource, when)
        if event == "RESTORE_BACKUP":
            return UNRESOLVED, "restore claim; downstream state needs its own observation"
        if event == "CHECK_DATA_FLOW":
            if state == "ACTIVE":
                return CORROBORATES, f"later state {state}"
            if state == "DISABLED":
                return CONTRADICTED, f"later state {state}"
            return UNRESOLVED, "no later flow state"
        if event == "SYNC_RECORD":
            if state:
                return CORROBORATES, f"later resource state {state}"
            return UNRESOLVED, "no later resource state"
        if event == "DISABLE_DATA_FLOW":
            if state == "ACTIVE":
                return CONTRADICTED, "later evidence still shows enabled"
            if state == "DISABLED":
                return CORROBORATES, f"later state {state}"
            return UNRESOLVED, "no later flow state"
        if event == "CHECK_RESTORE_ACCESS":
            if state == "ACTIVE":
                return CORROBORATES, "later evidence still shows restore allowed"
            if state == "BLOCKED":
                return CONTRADICTED, f"later state {state}"
            return UNRESOLVED, "no later restore state"
        if event == "BLOCK_RESTORE":
            if state == "ACTIVE":
                return CONTRADICTED, "later evidence still shows restore allowed"
            if state == "BLOCKED":
                return CORROBORATES, f"later state {state}"
            return UNRESOLVED, "no later restore state"
        return UNRESOLVED, "unhandled event"

    def run(self) -> None:
        for row in self.rows:
            event = row.get("event_type", "")
            if event not in EVENTS:
                continue
            resource = row.get("resource_id", "")
            when = parse_ts(row.get("event_time", ""))
            users = (self.index.resource_users.get((row.get("target_system", ""), resource), set())
                     | self.index.resource_users.get((row.get("source_system", ""), resource), set()))
            case = self._case_for(users, when, include_post=event == "RESTORE_BACKUP") if users else None
            if case is None:
                continue
            if event == "RESTORE_BACKUP" and when > case.audit_at:
                verdict, reason = EXCLUDED_POST_AUDIT, "event is after audit_at"
            else:
                verdict, reason = self._classify(event, resource, when)
            self.results.append(ActivityResult(
                case.case_id, row.get("activity_id", ""), event, resource,
                when, verdict, reason,
            ))

    def summary(self) -> dict:
        counts = Counter((r.event_type, r.verdict) for r in self.results)
        return {
            "rows": len(self.results),
            "counts": {f"{event}:{verdict}": count
                       for (event, verdict), count in sorted(counts.items())},
            "contradicted": [
                {
                    "case_id": r.case_id, "activity_id": r.activity_id,
                    "event_type": r.event_type, "resource_id": r.resource_id,
                    "event_time": r.event_time.isoformat(), "reason": r.reason,
                }
                for r in self.results if r.verdict == CONTRADICTED
            ],
        }
