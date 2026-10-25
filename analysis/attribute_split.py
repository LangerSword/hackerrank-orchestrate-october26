#!/usr/bin/env python3
"""Split unattributed facts into known-other, unknown-identifier, anonymous."""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))

from audit.pipeline import AuditAgent  # noqa: E402
from audit.tables import load_cases  # noqa: E402


def main() -> int:
    agent = AuditAgent(ROOT / "dataset", ROOT / "code/audit/digests/documents.json")
    cases = load_cases(ROOT / "dataset", "deletion_requests.csv")
    subjects = {agent.identities.resolve_email(case.email) for case in cases}
    subjects.discard("")

    counts = Counter()
    for fact in agent.index.unattributed:
        keys = fact.identity_keys()
        if not keys:
            counts["anonymous"] += 1
            continue
        owners = {agent.identities.resolve_identifier(key) for key in keys}
        owners.discard("")
        if owners and not (owners & subjects):
            counts["known_other_subject"] += 1
        else:
            counts["unknown_identifier"] += 1

    print(f"request subjects: {len(subjects)}")
    print(f"unattributed facts: {sum(counts.values())}")
    for key in ("known_other_subject", "unknown_identifier", "anonymous"):
        print(f"  {key:24} {counts[key]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
