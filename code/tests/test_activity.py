"""Positive controls for the activity contradiction detector."""
from __future__ import annotations

import unittest
from datetime import datetime, timezone
from types import SimpleNamespace

from audit.activity import ActivityAudit, CONTRADICTED
from audit.model import ACTIVE, BLOCKED, DISABLED


def at(day: int) -> datetime:
    return datetime(2026, 9, day, 12, 0, tzinfo=timezone.utc)


def detector() -> ActivityAudit:
    audit = object.__new__(ActivityAudit)
    audit.facts_by_resource = {}
    return audit


class ActivityPositiveControls(unittest.TestCase):
    def test_disable_flow_success_is_contradicted_by_later_active(self) -> None:
        audit = detector()
        audit.facts_by_resource["data_flow_1"] = [
            SimpleNamespace(observed_at=at(6), state=ACTIVE),
        ]
        verdict, _ = audit._classify("DISABLE_DATA_FLOW", "data_flow_1", at(5))
        self.assertEqual(verdict, CONTRADICTED)

    def test_block_restore_is_contradicted_by_later_restore_allowed(self) -> None:
        audit = detector()
        audit.facts_by_resource["backup_1"] = [
            SimpleNamespace(observed_at=at(6), state=ACTIVE),
        ]
        verdict, _ = audit._classify("BLOCK_RESTORE", "backup_1", at(5))
        self.assertEqual(verdict, CONTRADICTED)

    def test_restore_check_is_contradicted_by_later_blocked(self) -> None:
        audit = detector()
        audit.facts_by_resource["backup_1"] = [
            SimpleNamespace(observed_at=at(6), state=BLOCKED),
        ]
        verdict, _ = audit._classify("CHECK_RESTORE_ACCESS", "backup_1", at(5))
        self.assertEqual(verdict, CONTRADICTED)

    def test_disable_flow_success_corroborated_by_later_disabled(self) -> None:
        audit = detector()
        audit.facts_by_resource["data_flow_1"] = [
            SimpleNamespace(observed_at=at(6), state=DISABLED),
        ]
        verdict, _ = audit._classify("DISABLE_DATA_FLOW", "data_flow_1", at(5))
        self.assertEqual(verdict, "CORROBORATES")


if __name__ == "__main__":
    unittest.main()
