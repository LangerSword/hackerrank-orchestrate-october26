#!/usr/bin/env python3
"""Export every case's subject with all current and historical identifiers."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))

from audit.tables import IdentityGraph, load_cases


def main() -> int:
    graph = IdentityGraph.build(ROOT / "dataset")
    out = {}
    for case in load_cases(ROOT / "dataset"):
        user = graph.resolve_email(case.email)
        if not user:
            continue
        ident = graph.users[user]
        out[case.case_id] = {
            "subject": user,
            "emails": sorted(ident.emails),
            "phones": sorted(ident.phones),
            "hashes": sorted(ident.hashes),
            "user_ids": [user],
        }
    target = ROOT / "analysis" / "subjects.json"
    target.write_text(json.dumps(out, indent=1))
    print(f"wrote {len(out)} subjects to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
