#!/usr/bin/env python3
"""Strict-mode provenance: state-bearing lines with a subject token but no fact."""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))

from audit.pipeline import AuditAgent  # noqa: E402

COMPLETED = re.compile(r'event[=:]\s*"?[a-z_]*completed', re.IGNORECASE)


def main() -> int:
    agent = AuditAgent(ROOT / "dataset", ROOT / "code/audit/digests/documents.json")
    tokens = set()
    for user in agent.identities.users.values():
        tokens |= {email.lower() for email in user.emails}
        tokens.add(user.user_id.lower())

    fact_lines: dict[str, set[int]] = {}
    for fact in agent.index.facts:
        line = fact.detail.get("__lineno")
        if line:
            fact_lines.setdefault(fact.file_id, set()).add(int(line))

    raw = state_bearing = 0
    offenders: Counter = Counter()
    for file_id, evidence in agent.index.files.items():
        if evidence.path.suffix.lower() not in {".log", ".txt"}:
            continue
        try:
            lines = evidence.path.read_text(errors="replace").splitlines()
        except OSError:
            continue
        consumed = fact_lines.get(file_id, set())
        for number, line in enumerate(lines, start=1):
            low = line.lower()
            if not any(token and token in low for token in tokens):
                continue
            raw += 1
            if number in consumed or "resource_id" not in low or not COMPLETED.search(line):
                continue
            state_bearing += 1
            offenders[file_id] += 1

    print(f"raw subject-token lines outside facts: {raw}")
    print(f"state-bearing completed lines outside facts: {state_bearing}")
    for file_id, count in offenders.most_common(10):
        print(f"  {file_id} {count} {agent.index.files[file_id].path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
