"""Temporal reconstruction: what each resource looked like at `audit_at`.

Rules implemented here:
* an observation only counts if it was made at or before the audit cutoff;
* the newest observation of a resource wins;
* presence in *any* replica/store is still presence (replication drift);
* an empty point-in-time snapshot proves absence for resources that the same
  subject had in that collection before the snapshot.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from .index import EvidenceIndex
import re

from .model import ABSENT, IDENTIFIABLE, REDACTED, SUPPORT_MESSAGE, Fact, ResourceState

_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
from .tables import IdentityGraph


class StateBuilder:
    def __init__(self, index: EvidenceIndex, identities: IdentityGraph) -> None:
        self.index = index
        self.identities = identities

    def build(self, user_id: str, audit_at: datetime,
              requested_at: datetime | None = None) -> list[ResourceState]:
        facts = self.index.facts_for(user_id, audit_at)
        if requested_at is not None:
            windowed = [f for f in facts if f.observed_at >= requested_at]
            if windowed:
                facts = windowed
        by_resource: dict[tuple[str, str], list[Fact]] = defaultdict(list)
        for fact in facts:
            if not fact.resource_id:
                continue
            by_resource[(fact.system, fact.resource_id)].append(fact)

        states: list[ResourceState] = []
        for (system, resource_id), group in by_resource.items():
            latest = max(group, key=lambda f: (f.observed_at, f.state != ABSENT))
            state = latest.state
            # An empty readback snapshot is stronger evidence of absence than
            # an older row: the collection was inspected and returned nothing.
            for snapshot in self._empty_snapshots(facts):
                if (snapshot["category"] == latest.category
                        and snapshot["captured_at"] >= latest.observed_at
                        and snapshot["captured_at"] <= audit_at
                        and snapshot["store"] == system):
                    state = ABSENT
            if latest.category == SUPPORT_MESSAGE and state == IDENTIFIABLE:
                text = str(latest.detail.get("message_text") or "")
                owned = {e.lower() for e in self.identities.users[user_id].emails}
                if text.strip() and not (owned & {e.lower() for e in _EMAIL_RE.findall(text)}):
                    state = REDACTED
            states.append(
                ResourceState(
                    resource_id=resource_id,
                    system=system,
                    category=latest.category,
                    state=state,
                    observed_at=latest.observed_at,
                    file_id=latest.file_id,
                    facts=sorted(group, key=lambda f: f.observed_at),
                )
            )
        return states

    def _empty_snapshots(self, facts: list[Fact]) -> list[dict]:
        file_ids = {f.file_id for f in facts}
        return [s for s in self.index.empty_snapshots if s["file_id"] in file_ids]
