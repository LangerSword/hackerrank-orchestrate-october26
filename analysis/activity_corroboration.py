#!/usr/bin/env python3
"""Print activity corroboration metrics for the full run."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))

from audit.activity import ActivityAudit  # noqa: E402
from audit.pipeline import AuditAgent  # noqa: E402
from audit.tables import load_cases  # noqa: E402


def main() -> int:
    agent = AuditAgent(ROOT / "dataset", ROOT / "code/audit/digests/documents.json")
    cases = load_cases(ROOT / "dataset", "deletion_requests.csv")
    audit = ActivityAudit(ROOT / "dataset", agent.index, agent.identities, cases)
    summary = audit.summary()
    print(f"{'activity:verdict':45} {'count':>5}")
    for key, count in summary["counts"].items():
        print(f"{key:45} {count:5}")
    print(f"\nsubject-linked in-window rows: {summary['rows']}")
    print(f"contradicted: {len(summary['contradicted'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
