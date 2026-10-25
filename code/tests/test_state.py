"""Synthetic state tests. No dataset, no labels, no network."""
from __future__ import annotations

import unittest
from datetime import datetime, timezone
from types import SimpleNamespace

from audit.model import ABSENT, PRESENT, Fact
from audit.state import StateBuilder


def dt(day: int) -> datetime:
    return datetime(2026, 9, day, 12, 0, tzinfo=timezone.utc)


def fact(system: str, resource: str, state: str, day: int, file_id: str = "e1") -> Fact:
    return Fact(
        system=system,
        category="SEARCH_INDEX_ENTRY",
        resource_id=resource,
        state=state,
        observed_at=dt(day),
        file_id=file_id,
        file_captured_at=dt(day),
    )


class FakeIndex:
    def __init__(self, facts: list[Fact], empties: list[dict] | None = None) -> None:
        self.facts = facts
        self.empty_snapshots = empties or []

    def facts_for(self, user_id: str, cutoff: datetime) -> list[Fact]:
        return [f for f in self.facts if f.observed_at <= cutoff]


class FakeIdentities:
    def __init__(self) -> None:
        self.users = {"u1": SimpleNamespace(emails={"a@example.com"})}


def state_for(facts: list[Fact], audit_day: int = 10,
              empties: list[dict] | None = None) -> dict[tuple[str, str], str]:
    builder = StateBuilder(FakeIndex(facts, empties), FakeIdentities())
    states = builder.build("u1", dt(audit_day))
    return {(s.system, s.resource_id): s.state for s in states}


class StateTests(unittest.TestCase):
    def test_replica_presence_is_not_hidden_by_primary_absence(self) -> None:
        states = state_for([
            fact("search_service", "search_1", ABSENT, 5),
            fact("search_replica_eu", "search_1", PRESENT, 5),
        ])
        self.assertEqual(states[("search_service", "search_1")], ABSENT)
        self.assertEqual(states[("search_replica_eu", "search_1")], PRESENT)

    def test_newer_empty_snapshot_from_same_replica_proves_absence(self) -> None:
        states = state_for(
            [fact("search_replica_eu", "search_1", PRESENT, 5)],
            empties=[{"category": "SEARCH_INDEX_ENTRY", "captured_at": dt(7),
                      "store": "search_replica_eu", "file_id": "e1"}],
        )
        self.assertEqual(states[("search_replica_eu", "search_1")], ABSENT)

    def test_equal_timestamp_tie_prefers_presence(self) -> None:
        states = state_for([
            fact("search_service", "search_1", ABSENT, 5, "e1"),
            fact("search_service", "search_1", PRESENT, 5, "e2"),
        ])
        self.assertEqual(states[("search_service", "search_1")], PRESENT)

    def test_post_audit_observation_is_ignored(self) -> None:
        states = state_for([
            fact("search_service", "search_1", ABSENT, 5),
            fact("search_service", "search_1", PRESENT, 11),
        ], audit_day=10)
        self.assertEqual(states[("search_service", "search_1")], ABSENT)


if __name__ == "__main__":
    unittest.main()
