#!/usr/bin/env python3
"""Parser-path exposure: which source paths decide findings, and sample coverage."""
import csv, json, re, sqlite3, sys
from collections import Counter, defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))
import audit.planner as planner
from audit.pipeline import AuditAgent
from audit.tables import load_cases

a = AuditAgent(ROOT/"dataset", ROOT/"code/audit/digests/documents.json")
def run(f): return {r.case_id: r for r in a.run_all(f)}
sample = run("sample_deletion_requests.csv"); evals = run("deletion_requests.csv")
scases = {c.case_id: c for c in load_cases(ROOT/"dataset", "sample_deletion_requests.csv")}
ecases = {c.case_id: c for c in load_cases(ROOT/"dataset")}
gold = {r["case_id"]: r for r in csv.DictReader(open(ROOT/"dataset/sample_output.csv"))}

def desc(f):
    suffix = a.index.files[f.file_id].path.suffix.lstrip(".")
    return f"{suffix}:{f.source or 'unknown'}"

def findings(cid, cases, res):
    c = cases[cid]; u = a.identities.resolve_email(c.email)
    states = a.states.build(u, c.audit_at, c.requested_at)
    out = []
    for st in states:
        step = planner._finding(st, a.policy)
        if not step: continue
        fact = max([f for f in a.index.facts_for(u, c.audit_at)
                    if f.resource_id == st.resource_id and f.system == st.system],
                   key=lambda f: f.observed_at, default=None)
        out.append((step, desc(fact) if fact else "none", fact))
    return out

sample_paths = Counter(); sample_agree = Counter()
for cid in sample:
    canon = {(s["operation"], s["system_id"], s["resource_id"])
             for s in json.loads(gold[cid]["steps_json"]) if s["phase"] == "FINDING"}
    for step, d, _ in findings(cid, scases, sample):
        sample_paths[d] += 1
        sample_agree[d] += (step.operation, step.system_id, step.resource_id) in canon
eval_paths = Counter(); eval_dep = Counter()
for cid in evals:
    fs = findings(cid, ecases, evals)
    ds = {d for _, d, _ in fs}
    for _, d, _ in fs:
        eval_paths[d] += 1
        if len(ds) == 1: eval_dep[d] += 1

rows = []
for d in set(sample_paths) | set(eval_paths):
    rows.append((sample_paths[d], sample_agree[d], eval_paths[d], eval_dep[d], d))
rows.sort(key=lambda r: (0 if r[0] == 0 and r[3] > 0 else 1, -r[3], -r[2]))
print("sample_cases sample_agree eval_findings eval_status_dep path")
for r in rows[:45]: print(f"{r[0]:5d} {r[1]:5d} {r[2]:5d} {r[3]:5d}  {r[4]}")
print("zero-sample paths with eval status dependency:")
for r in rows:
    if r[0] == 0 and r[3] > 0: print(f"  {r[3]:3d}  {r[4]}")
# DELETION_PENDING
dp = 0; dps = 0
for p in (ROOT/"dataset/evidence/databases").glob("*.sql"):
    txt = p.read_text(errors="replace")
    for line in txt.splitlines():
        if "DELETION_PENDING" in line:
            dp += 1
print("DELETION_PENDING rows in SQL:", dp)
# CREATE TABLEs
con = sqlite3.connect(":memory:")
con.executescript((ROOT/"dataset/evidence/databases/customer_data_inventory_20260916.sql").read_text())
for t in ("backup_restore_entries", "connector_subscriptions"):
    print(con.execute("select sql from sqlite_master where name=?", (t,)).fetchone()[0])
# Phase 18 expiry
req = {**ecases, **scases}
email2case = defaultdict(list)
for cid, c in req.items(): email2case[c.email.lower()].append(cid)
expired = []; live = 0
for p in (ROOT/"dataset/evidence/records").glob("*.json"):
    try: doc = json.loads(p.read_text(errors="replace"))
    except: continue
    for r in doc.get("records", []) if isinstance(doc, dict) else []:
        if r.get("expires_at") and r.get("owner_email"):
            for cid in email2case.get(r["owner_email"].lower(), []):
                c = req[cid]
                if r["expires_at"] < c.audit_at.isoformat(): expired.append((cid, r["resource_id"]))
                else: live += 1
print("export rows: expired-before-audit", len(expired), expired[:10], "| live", live)
# retention
ret_before = []
for p in (ROOT/"dataset/evidence/databases").glob("*.sql"):
    c = sqlite3.connect(":memory:")
    try: c.executescript(p.read_text(errors="replace"))
    except: continue
    for (t,) in c.execute("select name from sqlite_master where type='table'"):
        cols = [x[1] for x in c.execute(f'PRAGMA table_info("{t}")')]
        if "retention_until" not in cols or "subject_reference" not in cols: continue
        for rid, sub, ru in c.execute(f'select resource_id,subject_reference,retention_until from "{t}"'):
            for cid, case in req.items():
                if a.identities.resolve_email(case.email) == sub and ru < case.audit_at.isoformat():
                    ret_before.append((cid, rid))
print("retention rows expired before audit:", len(ret_before), ret_before[:10])
