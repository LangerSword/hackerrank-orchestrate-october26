#!/usr/bin/env python3
"""Independent sqlite oracle for SQL-only COMPLETE cases.

Loads each cited SQL snapshot with sqlite3, scans every table/column for the
subject's identifiers using this file's own normalisation (no import from
code/audit), and compares the matched resource ids with the facts the engine
extracted from the same file.
"""
from __future__ import annotations

import csv
import json
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))
from audit.pipeline import AuditAgent  # noqa: E402
from audit.tables import load_cases  # noqa: E402


def loose(s: str) -> str:
    s = s.strip().lower()
    if "@" in s:
        local, _, dom = s.rpartition("@")
        return local.split("+")[0].replace(".", "") + "@" + dom
    d = re.sub(r"\D", "", s)
    if len(d) >= 7:
        return d[-10:]
    return s


def main() -> int:
    agent = AuditAgent(ROOT / "dataset", ROOT / "code/audit/digests/documents.json")
    cases = {c.case_id: c for c in load_cases(ROOT / "dataset")}
    out = {r["case_id"]: r for r in csv.DictReader(open(ROOT / "output.csv"))}

    sql_complete = []
    for cid, row in out.items():
        if row["deletion_status"] != "COMPLETE":
            continue
        steps = json.loads(row["steps_json"])
        files = {s["evidence_id"] for s in steps if s["evidence_id"]}
        if files and all(agent.index.files[f].path.suffix == ".sql" for f in files):
            sql_complete.append((cid, sorted(files)))

    disagreements = []
    checked_files = 0
    for cid, files in sql_complete:
        case = cases[cid]
        subject = agent.identities.resolve_email(case.email)
        ident = agent.identities.users[subject]
        keys = {loose(e) for e in ident.emails} | {p[-10:] for p in ident.phones} | set(ident.hashes) | {subject}
        engine = {(f.system, f.resource_id) for f in agent.index.user_facts[subject]
                  if f.file_id in files}
        for fid in files:
            path = agent.index.files[fid].path
            checked_files += 1
            con = sqlite3.connect(":memory:")
            try:
                con.executescript(path.read_text(encoding="utf-8", errors="replace"))
            except sqlite3.Error as exc:
                disagreements.append((cid, fid, "sqlite load failed", str(exc)[:120]))
                continue
            tables = [r[0] for r in con.execute("select name from sqlite_master where type='table'")]
            found = set()
            for table in tables:
                cols = [r[1] for r in con.execute(f'PRAGMA table_info("{table}")')]
                for row in con.execute(f'SELECT * FROM "{table}"'):
                    blob = {c: v for c, v in zip(cols, row)}
                    text = " ".join(str(v) for v in row if v is not None)
                    toks = {loose(t) for t in re.findall(r"[^\s\"',]+", text)}
                    if not (keys & toks):
                        continue
                    rid = str(blob.get("resource_id") or "")
                    if not rid and blob.get("record_json"):
                        try:
                            rid = str(json.loads(blob["record_json"]).get("resource_id") or "")
                        except Exception:
                            rid = ""
                    table_system = {
                        "customer_profiles": "account_service",
                        "customer_profiles_primary": "account_service",
                        "customer_profiles_failover_replica": "account_service",
                        "customer_search_documents": "search_service",
                        "search_documents_primary": "search_service",
                        "customer_analytics_profiles": "analytics_platform",
                        "support_records": "support_platform",
                        "customer_exports": "export_service",
                        "connector_subscriptions": "integration_service",
                        "backup_restore_entries": "backup_service",
                        "security_audit_records": "security_service",
                    }.get(table, "")
                    system = (blob.get("origin_system") or blob.get("system") or table_system)
                    if rid:
                        found.add((str(system), rid))
            con.close()
            missing_engine = found - engine
            if missing_engine:
                disagreements.append((cid, fid, "oracle rows not in engine facts",
                                     sorted(missing_engine)[:6]))

    print(f"SQL-only COMPLETE cases: {len(sql_complete)}; sqlite files loaded: {checked_files}")
    print(f"disagreements: {len(disagreements)}")
    for d in disagreements[:12]:
        print("  ", d)

    # shape comparison
    sample = {r["case_id"]: r for r in csv.DictReader(open(ROOT / "dataset/sample_output.csv"))}
    def shape(row):
        return tuple(sorted({s["operation"] for s in json.loads(row["steps_json"])
                             if s["phase"] == "VERIFICATION"}))
    sample_shapes = Counter(shape(r) for r in sample.values() if r["deletion_status"] == "COMPLETE")
    sql_shapes = Counter(shape(out[cid]) for cid, _ in sql_complete)
    print("\nsample COMPLETE verification-shape sets:")
    for k, n in sample_shapes.items():
        print(f"  {n:2d}  {k}")
    print("SQL-only COMPLETE shapes not present in any sample COMPLETE:")
    for k, n in sql_shapes.items():
        if k not in sample_shapes:
            print(f"  {n:3d}  {k}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
