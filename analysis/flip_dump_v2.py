#!/usr/bin/env python3
"""Flip dump v2: full records, identifiers, times, digest/OCR for PNGs."""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))
import audit.policy as policy_mod  # noqa: E402
import audit.planner as planner  # noqa: E402
from audit.pipeline import AuditAgent  # noqa: E402
from audit.tables import load_cases  # noqa: E402

RULES = {
    "support_retained": ("SUPPORT_MESSAGE", "policy: SUPPORT_MESSAGE is REDACT, not RETAIN"),
    "analytics_retained": ("ANALYTICS_PROFILE", "policy: ANALYTICS_PROFILE is ANONYMIZE, not RETAIN"),
    "flow_never_active": ("DATA_FLOW", "state: enabled=true means an active data flow"),
    "backup_never_risk": ("BACKUP_ARCHIVE", "state: restore_allowed=true means a restore risk"),
}


def agent():
    return AuditAgent(ROOT / "dataset", ROOT / "code/audit/digests/documents.json")


def run(a):
    return {r.case_id: r for r in a.run_all("deletion_requests.csv")}


def row_dict(path: Path, resource_id: str):
    con = sqlite3.connect(":memory:")
    try:
        con.executescript(path.read_text(errors="replace"))
    except sqlite3.Error:
        return None, None
    for (table,) in con.execute("select name from sqlite_master where type='table'"):
        cols = [r[1] for r in con.execute(f'PRAGMA table_info("{table}")')]
        for row in con.execute(f'SELECT * FROM "{table}"'):
            d = dict(zip(cols, row))
            if str(d.get("resource_id")) == resource_id:
                ddl = con.execute("select sql from sqlite_master where name=?", (table,)).fetchone()[0]
                return ddl, d
    return None, None


def main() -> int:
    a = agent()
    base = run(a)
    cases = {c.case_id: c for c in load_cases(ROOT / "dataset")}
    entries = []
    for name, (cat, reason) in RULES.items():
        if name.endswith("retained"):
            orig = policy_mod.Policy.action_for
            with patch.object(policy_mod.Policy, "action_for",
                              lambda self, c, cat=cat, o=orig: "RETAIN" if c == cat else o(self, c)):
                mut = run(agent())
        else:
            orig = planner._finding
            with patch.object(planner, "_finding",
                              lambda st, p, cat=cat, o=orig: None if st.category == cat else o(st, p)):
                mut = run(agent())
        for cid in sorted(base):
            if base[cid].status == mut[cid].status:
                continue
            removed = [s for s in base[cid].steps if s.phase == "FINDING" and
                       (s.operation, s.system_id, s.resource_id) not in
                       {(x.operation, x.system_id, x.resource_id) for x in mut[cid].steps}]
            for s in removed:
                entries.append((cid, name, cat, s, reason))

    out = []
    for cid, name, cat, s, reason in entries:
        case = cases[cid]
        user = a.identities.resolve_email(case.email) or a.identities.resolve_identifier(case.email)
        ident = a.identities.users[user]
        owned = {e.lower() for e in ident.emails} | {h.lower() for h in ident.hashes} | \
                {"p:" + p for p in ident.phones} | {user.lower()}
        fact = None
        for f in a.index.facts_for(user, case.audit_at):
            if f.resource_id == s.resource_id and f.system == s.system_id:
                if fact is None or f.observed_at > fact.observed_at:
                    fact = f
        ties = []
        if fact:
            for key in fact.identifiers:
                k = (key or "").strip().lower()
                if k in owned or (k.startswith("p:") and k[2:] in {p for p in ident.phones}):
                    ties.append((key, "phone" if k.startswith("p:") else ("email" if "@" in k else
                                                                           ("hash" if len(k) == 64 else "user_id")), "exact"))
            if not ties and fact.user_ref:
                ties.append((fact.user_ref, "user_id", "exact"))
        path = a.index.files[fact.file_id].path if fact else None
        record = None
        if path:
            if path.suffix == ".sql":
                ddl, row = row_dict(path, s.resource_id)
                record = ("sql", ddl, row)
            elif path.suffix == ".json":
                doc = json.loads(path.read_text(errors="replace"))
                stack = [doc]
                found = None
                while stack and not found:
                    node = stack.pop()
                    if isinstance(node, dict):
                        if str(node.get("resource_id")) == s.resource_id:
                            found = node
                        for v in node.values():
                            if isinstance(v, (dict, list)):
                                stack.append(v)
                    elif isinstance(node, list):
                        stack.extend(v for v in node if isinstance(v, (dict, list)))
                record = ("json", None, found)
            elif path.suffix in {".log", ".txt"}:
                raw = path.read_text(errors="replace").splitlines()
                idx = next((i for i, l in enumerate(raw) if s.resource_id in l), None)
                record = ("log", None, raw[idx] if idx is not None else None)
            elif path.suffix == ".png":
                digest = json.loads((ROOT / "code/audit/digests/documents.json").read_text())
                ocr = (ROOT / "analysis/text" / f"{fact.file_id}.txt")
                record = ("png", list(digest.get(fact.file_id, [])),
                          ocr.read_text(errors="replace")[:4000] if ocr.exists() else "OCR text unavailable")
        out.append(dict(case=cid, status=base[cid].status, requested=case.requested_at.isoformat(),
                        audit=case.audit_at.isoformat(), user=user, emails=sorted(ident.emails),
                        phones=sorted(ident.phones), hashes=sorted(ident.hashes),
                        ties=ties, rule=name, reason=reason, finding=s,
                        observed=fact.observed_at.isoformat() if fact else "",
                        file=str(path.relative_to(ROOT / "dataset")) if path else "",
                        record=record))

    target = ROOT / "analysis" / "flip_dump_v2.md"
    with target.open("w") as fh:
        fh.write(f"# Flip dump v2 — {len(out)} entries\n\n")
        for e in out:
            fh.write(f"## {e['case']} — {e['rule']}\n\n")
            fh.write(f"- status: {e['status']}; requested_at: {e['requested']}; audit_at: {e['audit']}\n")
            fh.write(f"- subject: {e['user']}; emails={e['emails']}; phones={e['phones']}; hashes={e['hashes']}\n")
            fh.write(f"- tied by: {e['ties']}\n")
            fh.write(f"- deciding fact observed_at: {e['observed']}; file: {e['file']}\n")
            fh.write(f"- finding: {e['finding'].operation} {e['finding'].system_id} {e['finding'].resource_id} state={e['finding'].state}\n")
            fh.write(f"- rule under test: {e['reason']}\n\n")
            kind, ddl, payload = e["record"] if e["record"] else ("none", None, None)
            if kind == "sql":
                fh.write("```sql\n" + str(ddl) + "\n-- row --\n" + json.dumps(payload, indent=1) + "\n```\n\n")
            elif kind == "json":
                fh.write("```json\n" + json.dumps(payload, indent=1) + "\n```\n\n")
            elif kind == "log":
                fh.write("```\n" + str(payload) + "\n```\n\n")
            elif kind == "png":
                fh.write("digest entry:\n```json\n" + json.dumps(ddl, indent=1) + "\n```\n")
                fh.write("OCR text (first 4000 chars):\n```\n" + str(payload) + "\n```\n\n")
            else:
                fh.write("_no record found_\n\n")
            fh.write(f"why: the engine reads `{e['finding'].state}` on {e['finding'].resource_id}; "
                     "disabling this rule removes the only finding.\n\n")
    print("wrote", len(out), "entries to", target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
