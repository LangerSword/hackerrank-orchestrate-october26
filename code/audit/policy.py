"""Deletion policy: the CSV rules translated into deterministic decisions.

`deletion_rules.csv` is the authority.  The code only knows how to *apply* an
action (DELETE / REDACT / ANONYMIZE / RETAIN) to an observed state; it never
hardcodes which category gets which action.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from .model import (
    ABSENT,
    ACCOUNT_TOMBSTONE,
    ACTIVE,
    ANALYTICS_PROFILE,
    ANONYMIZED,
    BACKUP_ARCHIVE,
    BLOCKED,
    CACHE_ENTRY,
    DISABLED,
    EMAIL_DELIVERY_LOG,
    IDENTIFIABLE,
    LEGAL_HOLD_RECORD,
    MARKETING_PROFILE,
    PRESENT,
    PRODUCT_TELEMETRY,
    REDACTED,
    SEARCH_INDEX_ENTRY,
    SECONDARY_IDENTIFIER,
    SECURITY_AUDIT_LOG,
    SUPPORT_ATTACHMENT,
    SUPPORT_MESSAGE,
    USER_EXPORT,
    USER_PROFILE,
)

DELETE = "DELETE"
REDACT = "REDACT"
ANONYMIZE = "ANONYMIZE"
RETAIN = "RETAIN"

# Findings that indicate the record itself must go.
DELETE_CATEGORIES = {
    USER_PROFILE,
    SECONDARY_IDENTIFIER,
    SEARCH_INDEX_ENTRY,
    CACHE_ENTRY,
    SUPPORT_ATTACHMENT,
    USER_EXPORT,
    MARKETING_PROFILE,
}
REDACT_CATEGORIES = {SUPPORT_MESSAGE, EMAIL_DELIVERY_LOG, ACCOUNT_TOMBSTONE}
ANONYMIZE_CATEGORIES = {ANALYTICS_PROFILE, PRODUCT_TELEMETRY}
RETAIN_CATEGORIES = {SECURITY_AUDIT_LOG, LEGAL_HOLD_RECORD}
FLOW = "DATA_FLOW"


@dataclass(frozen=True)
class Rule:
    rule_id: str
    category: str
    condition: str
    action: str


class Policy:
    def __init__(self, rules: dict[str, Rule]) -> None:
        self.rules = rules

    @classmethod
    def load(cls, dataset_dir: Path) -> "Policy":
        rules: dict[str, Rule] = {}
        with (dataset_dir / "deletion_rules.csv").open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                category = row["data_category"].strip()
                rules[category] = Rule(
                    row["rule_id"].strip(),
                    category,
                    row["condition"].strip(),
                    row["required_action"].strip().upper(),
                )
        return cls(rules)

    def action_for(self, category: str) -> str:
        rule = self.rules.get(category)
        if rule:
            return rule.action
        # Safe fallbacks only for categories the policy table does not name.
        if category in DELETE_CATEGORIES:
            return DELETE
        if category in REDACT_CATEGORIES:
            return REDACT
        if category in ANONYMIZE_CATEGORIES:
            return ANONYMIZE
        if category in RETAIN_CATEGORIES:
            return RETAIN
        return DELETE

    def required_final_state(self, category: str) -> str:
        action = self.action_for(category)
        if category == FLOW:
            return DISABLED
        if category == BACKUP_ARCHIVE:
            return BLOCKED
        if action == DELETE:
            return ABSENT
        if action == REDACT:
            return REDACTED
        if action == ANONYMIZE:
            return ANONYMIZED
        return PRESENT

    def is_violation(self, category: str, state: str) -> bool:
        if category == FLOW:
            return state == ACTIVE
        if category == BACKUP_ARCHIVE:
            return state == ACTIVE
        action = self.action_for(category)
        if action == DELETE:
            return state in {PRESENT, IDENTIFIABLE, ACTIVE}
        if action == REDACT:
            return state == IDENTIFIABLE
        if action == ANONYMIZE:
            return state == IDENTIFIABLE
        return False
