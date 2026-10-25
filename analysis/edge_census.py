#!/usr/bin/env python3
"""Census of cross-resource foreign-key edges in the shipped evidence."""
from __future__ import annotations

import json
import re
import sqlite3
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "dataset"
RID = re.compile(r"\b(account|analytics|audit_record|search|export|backup|data_flow|support|object)_[0-9]+\b")
OWN = {"resource_id", "id", "activity_id", "file_id", "case_id", "rule_id", "user_id",
       "audit_id", "event_id", "image_id"}
USED = {"source_resource_id"}  # search_documents_primary, case_06
counts: Counter = Counter()


def add(source: str, field: str, value: str) -> None:
    match = RID.search(str(value))
    if not match or field.lower() in OWN:
        return
    counts[(source, field.lower(), match.group(1))] += 1


def walk_json(source: str, value, path: str = "") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            walk_json(source, item, f"{path}.{key}" if path else key)
    elif isinstance(value, list):
        for item in value:
            walk_json(source, item, path)
    elif isinstance(value, str):
        add(source, path.split(".")[-1] if path else "", value)


def sql_file(path: Path) -> None:
    try:
        conn = sqlite3.connect(":memory:")
        conn.executescript(path.read_text(encoding="utf-8", errors="replace"))
        tables = [r[0] for r in conn.execute(
            "select name from sqlite_master where type='table'")]
        for table in tables:
            columns = [r[1] for r in conn.execute(f'pragma table_info("{table}")')]
            for row in conn.execute(f'select * from "{table}"'):
                for column, value in zip(columns, row):
                    if not isinstance(value, str):
                        continue
                    if column == "record_json":
                        try:
                            walk_json(f"sql:{table}", json.loads(value))
                            continue
                        except Exception:
                            pass
                    add(f"sql:{table}", column, value)
        conn.close()
    except Exception:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if "INSERT" in line.upper():
                for value in RID.findall(line):
                    counts[("sql:fallback", "value", value)] += 1


def main() -> int:
    for path in sorted(DATASET.rglob("*")):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix == ".sql":
            sql_file(path)
        elif suffix == ".json":
            try:
                walk_json(f"json:{path.stem}", json.loads(path.read_text(errors="replace")))
            except Exception:
                pass
        elif suffix in {".log", ".txt"}:
            for line in path.read_text(errors="replace").splitlines():
                for key, value in re.findall(r"([A-Za-z_][\w.-]*)=(\"[^\"]*\"|\S+)", line):
                    add(f"{suffix}:{path.stem}", key, value.strip('"'))
                if suffix == ".txt" and "|" in line:
                    parts = [p.strip() for p in line.split("|")]
                    for index, part in enumerate(parts):
                        add(f"handover:{path.stem}", f"field_{index}", part)

    print(f"{'source':42} {'field':22} {'target':14} {'count':>6} {'used':>5}")
    rows = [((source, field, target), count) for (source, field, target), count in counts.most_common()
            if field.endswith("_id") or field in USED]
    for (source, field, target), count in rows[:40]:
        used = "yes" if field in USED else "no"
        print(f"{source[:42]:42} {field[:22]:22} {target:14} {count:6} {used:>5}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
