#!/usr/bin/env python3
"""Dump the engine's fact store for an independent oracle (no parsing here)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))
from audit.pipeline import AuditAgent  # noqa: E402

def main() -> int:
    agent = AuditAgent(ROOT / "dataset", ROOT / "code/audit/digests/documents.json")
    rows = []
    for f in agent.index.facts:
        ev = agent.index.files.get(f.file_id)
        if not ev:
            continue
        rows.append({
            "file": str(ev.path.relative_to(ROOT / "dataset")),
            "line": int(f.detail.get("__lineno") or 0),
            "system": f.system,
            "category": f.category,
            "resource_id": f.resource_id,
            "state": f.state,
            "observed_at": f.observed_at.isoformat(),
            "users": f.detail.get("users", []),
            "tokens": sorted(f.identifiers),
        })
    out = ROOT / "analysis" / "facts_dump.json"
    out.write_text(json.dumps(rows))
    print(f"wrote {len(rows)} facts to {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
