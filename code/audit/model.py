"""Domain model for the Ghost Data deletion-audit agent.

Everything the planner needs is expressed as immutable dataclasses so the
pipeline stays deterministic and easy to audit.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable


# ---------------------------------------------------------------- categories
# Data categories come straight from deletion_rules.csv / evidence record
# types.  Keeping them as plain strings makes the rule table the source of
# truth instead of duplicating policy in code.
USER_PROFILE = "USER_PROFILE"
SECONDARY_IDENTIFIER = "SECONDARY_IDENTIFIER"
SEARCH_INDEX_ENTRY = "SEARCH_INDEX_ENTRY"
CACHE_ENTRY = "CACHE_ENTRY"
SUPPORT_MESSAGE = "SUPPORT_MESSAGE"
SUPPORT_ATTACHMENT = "SUPPORT_ATTACHMENT"
ANALYTICS_PROFILE = "ANALYTICS_PROFILE"
PRODUCT_TELEMETRY = "PRODUCT_TELEMETRY"
USER_EXPORT = "USER_EXPORT"
MARKETING_PROFILE = "MARKETING_PROFILE"
EMAIL_DELIVERY_LOG = "EMAIL_DELIVERY_LOG"
SECURITY_AUDIT_LOG = "SECURITY_AUDIT_LOG"
LEGAL_HOLD_RECORD = "LEGAL_HOLD_RECORD"
BACKUP_ARCHIVE = "BACKUP_ARCHIVE"
ACCOUNT_TOMBSTONE = "ACCOUNT_TOMBSTONE"

# ---------------------------------------------------------------- states
PRESENT = "PRESENT"
ABSENT = "ABSENT"
IDENTIFIABLE = "IDENTIFIABLE"  # record exists and still carries direct PII
REDACTED = "REDACTED"
ANONYMIZED = "ANONYMIZED"
ACTIVE = "ACTIVE"
DISABLED = "DISABLED"
BLOCKED = "BLOCKED"


def parse_ts(value: str) -> datetime:
    """Parse the dataset's ISO-8601 timestamps (always UTC)."""
    text = (value or "").strip()
    if not text:
        return datetime.min.replace(tzinfo=timezone.utc)
    text = text.replace("Z", "+00:00")
    if "." in text:
        head, tail = text.split(".", 1)
        tz = ""
        for marker in ("+", "-"):
            idx = tail.find(marker)
            if idx != -1 and tail[idx:].count(":") == 1:
                tz = tail[idx:]
                tail = tail[:idx]
                break
        text = head + ("." + tail[:6] if tail else "") + tz
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d %H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"):
            try:
                dt = datetime.strptime(text, fmt)
                break
            except ValueError:
                continue
        else:
            return datetime.min.replace(tzinfo=timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


@dataclass(frozen=True)
class Case:
    case_id: str
    email: str
    requested_at: datetime
    reported_status: str
    reported_at: datetime
    audit_at: datetime
    request_text: str


@dataclass(frozen=True)
class Identity:
    user_id: str
    name: str
    email: str
    phone: str
    email_hash: str
    updated_at: datetime


@dataclass
class UserIdentity:
    """A subject with current *and* historical identifiers."""

    user_id: str
    names: set[str] = field(default_factory=set)
    emails: set[str] = field(default_factory=set)
    hashes: set[str] = field(default_factory=set)
    phones: set[str] = field(default_factory=set)  # digits only

    def identifiers(self) -> set[str]:
        out = {self.user_id.lower()}
        out |= {e.lower() for e in self.emails}
        out |= {h.lower() for h in self.hashes if h}
        out |= {"p:" + p for p in self.phones if p}
        return out


@dataclass(frozen=True)
class Fact:
    """One observation of one resource at one point in time."""

    system: str
    category: str
    resource_id: str
    state: str
    observed_at: datetime
    file_id: str
    file_captured_at: datetime
    identifiers: frozenset[str] = frozenset()
    user_ref: str = ""
    origin: str = ""
    source: str = ""
    detail: dict = field(default_factory=dict)

    def identity_keys(self) -> set[str]:
        keys = {k.strip().lower() for k in self.identifiers if k}
        if self.user_ref:
            keys.add(self.user_ref.strip().lower())
        return keys


@dataclass
class ResourceState:
    resource_id: str
    system: str
    category: str
    state: str
    observed_at: datetime
    file_id: str
    facts: list[Fact] = field(default_factory=list)

    @property
    def key(self) -> tuple[str, str]:
        return (self.system, self.resource_id)


@dataclass(frozen=True)
class Step:
    phase: str
    system_id: str
    resource_id: str
    operation: str
    state: str
    evidence_id: str = ""

    def as_dict(self, step_no: int) -> dict:
        return {
            "step_no": step_no,
            "phase": self.phase,
            "system_id": self.system_id,
            "resource_id": self.resource_id,
            "operation": self.operation,
            "state": self.state,
            "evidence_id": self.evidence_id,
        }


@dataclass
class CaseResult:
    case_id: str
    status: str
    steps: list[Step]

    def steps_json(self) -> list[dict]:
        return [s.as_dict(i + 1) for i, s in enumerate(self.steps)]


def norm_email(value: str) -> str:
    return (value or "").strip().lower()


def norm_phone(value: str) -> str:
    return "".join(ch for ch in (value or "") if ch.isdigit())


def norm_hash(value: str) -> str:
    return (value or "").strip().lower()


def first(value: Iterable[str]) -> str:
    for item in value:
        return item
    return ""
