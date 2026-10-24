#!/usr/bin/env python3
"""State-vocabulary census + soft-delete check over every evidence file."""
from __future__ import annotations

import csv
import json
import re
import sqlite3
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "dataset"
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
HASH_RE = re.compile(r"(?<![0-9A-Fa-f])[0-9A-Fa-f]{64}(?![0-9A-Fa-f])")
UID_RE = re.compile(r"(?<![A-Za-z0-9])user[ _\-]?0*(\d+)(?![A-Za-z0-9])", re.I)
PHONE_RE = re.compile(r"\+?\d[\d\-\s().]{7,}\d")
RID_RE = re.compile(r"\b(?:account|search|analytics|support|export|audit_record|backup|data_flow|tombstone|marketing|object|legal_hold|cache|email_delivery)_\d+\b")
STATE_KEY = re.compile(r"deleted|tombstone|archiv|purge|anonymi|soft|status|state|retention|expir|restor|hold|redact|mask|flag|active|enabled|marker|result|rows|http", re.I)


def ekey(s):
    s = unicodedata.normalize("NFKC", s).strip().lower()
    if "@" in s:
        a, _, b = s.rpartition("@")
        return a.split("+")[0].replace(".", "") + "@" + b
    return s


def pkey(s):
    d = re.sub(r"\D", "", s)
    return d[-10:] if len(d) >= 10 else None


def subject_token(text):
    for m in EMAIL_RE.finditer(text):
        yield ("email", ekey(m.group(0)))
    for m in HASH_RE.finditer(text):
        yield ("hash", m.group(0).lower())
    for m in PHONE_RE.finditer(text):
        k = pkey(m.group(0))
        if k:
            yield ("phone", k)
    for m in UID_RE.finditer(text):
        yield ("uid", f"user_{int(m.group(1))}")


def norm(v):
    s = str(v)
    s = EMAIL_RE.sub("<email>", s)
    s = HASH_RE.sub("<hash>", s)
    s = RID_RE.sub("<id>", s)
    s = re.sub(r"\+?\d[\d\-\s().]{7,}\d", "<phone>", s)
    s = re.sub(r"\b\d{4}-\d{2}-\d{2}T[\d:.]+Z?\b", "<ts>", s)
    s = re.sub(r"\b\d+(\.\d+)?\b", "<num>", s)
    return s[:80]


def main() -> int:
    subjects = json.loads((ROOT / "analysis/subjects.json").read_text())
    owner = set()
    for v in subjects.values():
        for e in v["emails"]:
            owner.add(("email", ekey(e)))
        for p in v["phones"]:
            if pkey(p):
                owner.add(("phone", pkey(p)))
        for h in v["hashes"]:
            owner.add(("hash", h.lower()))
        owner.add(("uid", v["subject"]))

    facts = json.loads((ROOT / "analysis/facts_dump.json").read_text())
    by_res = defaultdict(set)
    for f in facts:
        by_res[(f["file"], f["resource_id"])].add(f["state"])
    status = {r["case_id"]: r["deletion_status"] for r in csv.DictReader(open(ROOT / "output.csv"))}
    case_subject = {c: v["subject"] for c, v in subjects.items()}

    pairs = Counter()
    files = defaultdict(set)
    state_keys = defaultdict(Counter)
    soft_rows = []
    no_cue = Counter()

    def note(key, value, rel):
        pairs[(key, norm(value))] += 1
        files[(key, norm(value))].add(rel)
        if STATE_KEY.search(key):
            state_keys[key][norm(value)] += 1
        else:
            no_cue[key] += 1

    for path in sorted(DATASET.rglob("*")):
        if not path.is_file():
            continue
        rel = str(path.relative_to(DATASET))
        suf = path.suffix.lower()
        if suf == ".sql":
            con = sqlite3.connect(":memory:")
            try:
                con.executescript(path.read_text(errors="replace"))
            except sqlite3.Error:
                continue
            tables = [r[0] for r in con.execute("select name from sqlite_master where type='table'")]
            for table in tables:
                cols = [r[1] for r in con.execute(f'PRAGMA table_info("{table}")')]
                for row in con.execute(f'SELECT * FROM "{table}"'):
                    blob = dict(zip(cols, row))
                    text = " ".join(str(v) for v in row if v is not None)
                    if not (set(subject_token(text)) & owner):
                        continue
                    rid = str(blob.get("resource_id") or "")
                    for k, v in blob.items():
                        if v is not None:
                            note(k, v, rel)
                    soft = {k: v for k, v in blob.items() if STATE_KEY.search(k)}
                    if soft and rid:
                        soft_rows.append((rel, table, rid, soft, by_res.get((rel, rid), set()),
                                          blob.get("account_status") or blob.get("status") or ""))
            con.close()
        elif suf == ".json":
            try:
                doc = json.loads(path.read_text(errors="replace"))
            except json.JSONDecodeError:
                continue
            stack = [doc]
            while stack:
                node = stack.pop()
                if isinstance(node, dict):
                    text = json.dumps(node)
                    if set(subject_token(text)) & owner:
                        for k, v in node.items():
                            if not isinstance(v, (dict, list)):
                                note(k, v, rel)
                    for v in node.values():
                        if isinstance(v, (dict, list)):
                            stack.append(v)
                elif isinstance(node, list):
                    stack.extend(v for v in node if isinstance(v, (dict, list)))
        elif suf in {".log", ".txt", ".csv"}:
            if rel in {"deletion_requests.csv", "sample_deletion_requests.csv", "user_identities.csv",
                       "user_audit_log.csv", "sample_output.csv", "output.csv", "evidence_files.csv",
                       "deletion_rules.csv"}:
                continue
            for line in path.read_text(errors="replace").splitlines():
                if not (set(subject_token(line)) & owner):
                    continue
                for m in re.finditer(r'([A-Za-z_]+)=("([^"]*)"|\'([^\']*)\'|(\S+))', line):
                    val = m.group(3) or m.group(4) or m.group(5) or ""
                    note(m.group(1), val, rel)

    print("== state-like keys (distinct normalised values) ==")
    for key, vals in sorted(state_keys.items()):
        print(f"  {key}: {dict(vals.most_common(8))}")
    print("\n== unknown / non-state keys, top 20 ==")
    for k, n in no_cue.most_common(20):
        print(f"  {k:28} {n}")

    print("\n== soft-delete / status rows and engine state ==")
    ghosts = []
    for rel, table, rid, soft, states, statusv in soft_rows:
        if states == {"ABSENT"} or (states and "ABSENT" in states and len(states) == 1):
            ghosts.append((rel, table, rid, soft, states))
    print(f"rows with state-like columns: {len(soft_rows)}; engine says ABSENT for {len(ghosts)}")
    for g in ghosts[:10]:
        print("  GHOST?", g)
    if not ghosts:
        print("  no soft-deleted row is treated as ABSENT by the engine")

    # prefix census of PRESENT facts in SQL
    sql_present = Counter()
    for f in facts:
        if f["state"] == "PRESENT" and f["file"].endswith(".sql") and f["resource_id"]:
            sql_present[f["resource_id"].split("_")[0]] += 1
    print("\n== SQL PRESENT resource prefixes ==", dict(sql_present))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
