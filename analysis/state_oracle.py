#!/usr/bin/env python3
"""Independent state oracle for non-SQL text files.

Does not import audit.evidence. Reads raw files, resolves loose subject tokens,
derives a state from the line/record's own fields, and diffs against
analysis/facts_dump.json keyed by (file, line) for logs and (file, resource)
for JSON.
"""
from __future__ import annotations

import csv
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "dataset"

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\+?\d[\d\-\s().]{7,}\d")
HASH_RE = re.compile(r"(?<![0-9A-Fa-f])[0-9A-Fa-f]{64}(?![0-9A-Fa-f])")
UID_RE = re.compile(r"(?<![A-Za-z0-9])user[ _\-]?0*(\d+)(?![A-Za-z0-9])", re.I)
RID_RE = re.compile(r"\b(account|search|analytics|support|export|audit_record|backup|data_flow|tombstone|marketing|object|legal_hold|cache|email_delivery)_\d+\b")


def ekey(s):
    s = unicodedata.normalize("NFKC", s).strip().lower()
    if "@" in s:
        local, _, dom = s.rpartition("@")
        return local.split("+")[0].replace(".", "") + "@" + dom
    return s


def pkey(s):
    d = re.sub(r"\D", "", s)
    return d[-10:] if len(d) >= 10 else None


def ukey(s):
    m = UID_RE.fullmatch(s.strip())
    return f"user_{int(m.group(1))}" if m else None


def hkey(s):
    return s.strip().lower()


def tokens(line):
    out = []
    for m in EMAIL_RE.finditer(line):
        out.append(("email", m.group(0), ekey(m.group(0))))
    for m in HASH_RE.finditer(line):
        out.append(("hash", m.group(0), hkey(m.group(0))))
    for m in PHONE_RE.finditer(line):
        k = pkey(m.group(0))
        if k:
            out.append(("phone", m.group(0), k))
    for m in UID_RE.finditer(line):
        k = ukey(m.group(0))
        if k:
            out.append(("uid", m.group(0), k))
    return out


def state_from_text(line: str) -> str | None:
    low = line.lower()
    if any(k in low for k in ("rows=0", "rows\": \"0", "http_status=404", "http_status\": \"404",
                              "result=miss", "result\": \"miss", "not_found", "no_hit")):
        return "ABSENT"
    if any(k in low for k in ("enabled=false", "enabled\": false")):
        return "DISABLED"
    if any(k in low for k in ("restore_allowed=false", "restore_allowed\": false")):
        return "BLOCKED"
    if "pii_scan" in low or "matched_value" in low or "identifiable" in low:
        return "IDENTIFIABLE"
    if any(k in low for k in ("[redacted]", "redacted", "requester_email=null")):
        return "REDACTED"
    if any(k in low for k in ("anonymized", "direct_identifiers=0", "direct_identifiers\": \"0")):
        return "ANONYMIZED"
    if any(k in low for k in ("enabled=true", "enabled\": true",
                              "restore_allowed=true", "restore_allowed\": true")):
        return "ACTIVE"
    if any(k in low for k in ("rows=1", "rows\": \"1", "http_status=200", "http_status\": \"200",
                              "result=hit", "result\": \"hit", "found")):
        return "PRESENT"
    return None


def json_state(rec: dict, rid: str = "") -> str | None:
    low = json.dumps(rec).lower()
    if rec.get("enabled") is False:
        return "DISABLED"
    if rec.get("enabled") is True:
        return "ACTIVE"
    if rec.get("restore_allowed") is False:
        return "BLOCKED"
    if rec.get("restore_allowed") is True:
        return "ACTIVE"
    if rec.get("download_available") is False:
        return "ABSENT"
    if "deleted" in str(rec.get("account_status", "")).lower():
        return "REDACTED"
    if "result" in rec:
        r = str(rec["result"]).upper()
        if r == "NOT_FOUND":
            return "ABSENT"
        if r == "FOUND":
            return "PRESENT"
        if r in {"REDACTED", "ANONYMIZED", "DISABLED", "BLOCKED", "ACTIVE", "IDENTIFIABLE"}:
            return r
    direct = any(rec.get(k) for k in ("email", "phone", "email_hash", "full_name",
                                      "display_name", "name", "requester_email",
                                      "requester_name", "uploaded_by", "owner_email"))
    msg = str(rec.get("message_text") or rec.get("message_excerpt") or "")
    if "[redacted]" in msg.lower():
        return "REDACTED"
    if rec.get("requester_email") is None and "support" in low and msg:
        return None
    if any(k in rec for k in ("file_name", "storage_class")) or rec.get("uploaded_by"):
        return "PRESENT"
    prefix = rid.split("_")[0] if rid else ""
    if prefix == "analytics":
        return "IDENTIFIABLE" if direct or re.search(EMAIL_RE, msg) else "ANONYMIZED"
    if prefix == "tombstone":
        return "IDENTIFIABLE" if direct else "REDACTED"
    if prefix == "support":
        if msg and "[redacted]" in msg.lower():
            return "REDACTED"
        if direct or re.search(EMAIL_RE, msg):
            return "IDENTIFIABLE"
        return None
    if direct:
        return "PRESENT"
    return None


def main() -> int:
    subjects = json.loads((ROOT / "analysis/subjects.json").read_text())
    owner = defaultdict(set)
    for cid, v in subjects.items():
        for e in v["emails"]:
            owner[("email", ekey(e))].add(v["subject"])
        for p in v["phones"]:
            if pkey(p):
                owner[("phone", pkey(p))].add(v["subject"])
        for h in v["hashes"]:
            owner[("hash", hkey(h))].add(v["subject"])
        owner[("uid", v["subject"])].add(v["subject"])
    subject_cases = defaultdict(set)
    for cid, v in subjects.items():
        subject_cases[v["subject"]].add(cid)
    status = {r["case_id"]: r["deletion_status"] for r in
              csv.DictReader(open(ROOT / "output.csv"))}
    facts = json.loads((ROOT / "analysis/facts_dump.json").read_text())
    by_line = defaultdict(set)
    by_res = defaultdict(set)
    for f in facts:
        if f["line"]:
            by_line[(f["file"], f["line"])].add(f["state"])
        by_res[(f["file"], f["resource_id"])].add(f["state"])

    stats = Counter()
    dis = []
    for path in sorted(DATASET.rglob("*")):
        if not path.is_file():
            continue
        rel = str(path.relative_to(DATASET))
        suf = path.suffix.lower()
        if suf in {".log", ".txt", ".csv"}:
            if rel.split("/")[-1] in {"deletion_requests.csv", "sample_deletion_requests.csv",
                                      "user_identities.csv", "user_audit_log.csv",
                                      "sample_output.csv", "output.csv", "evidence_files.csv"}:
                continue
            with open(path, errors="replace") as fh:
                for n, line in enumerate(fh, 1):
                    hits = [(k, t, key) for k, t, key in tokens(line) if owner.get((k, key))]
                    if not hits:
                        continue
                    stats["log_lines"] += 1
                    state = state_from_text(line)
                    if not state:
                        continue
                    rid = RID_RE.search(line)
                    resource = rid.group(0) if rid else ""
                    engine_states = by_line.get((rel, n))
                    if not engine_states:
                        stats["unconsumed"] += 1
                        dis.append(("UNCONSUMED", rel, n, resource, state,
                                    sorted({s for _, _, key in hits for s in owner[(_, key)]})))
                    elif state not in engine_states:
                        stats["mismatch"] += 1
                        dis.append(("MISMATCH", rel, n, resource, state, sorted(engine_states)))
        elif suf == ".json":
            try:
                doc = json.loads(path.read_text(errors="replace"))
            except json.JSONDecodeError:
                continue
            stack = [(doc, "$")]
            while stack:
                node, jp = stack.pop()
                if isinstance(node, dict):
                    text = json.dumps(node)
                    hit_keys = {s for k, t, key in tokens(text) for s in owner.get((k, key), ())}
                    if hit_keys and node.get("resource_id"):
                        stats["json_records"] += 1
                        rid = str(node.get("resource_id"))
                        st = json_state(node, rid)
                        if st:
                            engine_states = by_res.get((rel, rid))
                            if not engine_states:
                                stats["json_unconsumed"] += 1
                                dis.append(("JSON_UNCONSUMED", rel, jp, rid, st, sorted(hit_keys)))
                            elif st not in engine_states:
                                stats["json_mismatch"] += 1
                                dis.append(("JSON_MISMATCH", rel, jp, rid, st, sorted(engine_states)))
                    for k, v in node.items():
                        if isinstance(v, (dict, list)):
                            stack.append((v, f"{jp}.{k}"))
                elif isinstance(node, list):
                    for i, v in enumerate(node):
                        if isinstance(v, (dict, list)):
                            stack.append((v, f"{jp}[{i}]"))

    print("== stats ==", dict(stats))
    # rank: COMPLETE cases first
    def cases_for(users):
        return sorted({c for u in users for c in subject_cases.get(u, ())})
    dis.sort(key=lambda d: (0 if any(status.get(c) == "COMPLETE" for c in cases_for(d[5])) else 1, d[0], d[1]))
    for d in dis[:40]:
        cs = cases_for(d[5])
        print(d[0], d[1], d[2], d[3], "oracle=", d[4], "engine=", d[5] if d[0] != "UNCONSUMED" else "-", "cases=", cs[:3])
    out = ROOT / "analysis" / "state_disagreements.csv"
    with out.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["kind", "file", "line_or_path", "resource", "oracle_state", "engine_states", "cases"])
        for d in dis:
            w.writerow([d[0], d[1], d[2], d[3], d[4], "|".join(d[5]) if isinstance(d[5], list) else d[5],
                        "|".join(cases_for(d[5]) if isinstance(d[5], list) else [])])
    print(f"wrote {len(dis)} disagreements to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
