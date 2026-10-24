#!/usr/bin/env python3
"""Round 8: digest literal check, pair exposure, staleness, provenance."""
import csv, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/"code"))
import audit.planner as planner
from audit.pipeline import AuditAgent
from audit.tables import load_cases

a = AuditAgent(ROOT/"dataset", ROOT/"code/audit/digests/documents.json")
digest = json.loads((ROOT/"code/audit/digests/documents.json").read_text())
print("== 1. digest literal check ==")
fails = []
for fid, rows in digest.items():
    if fid == "_meta": continue
    ocr = (ROOT/"analysis/text"/f"{fid}.txt")
    text = ocr.read_text(errors="replace").lower() if ocr.exists() else ""
    for r in rows:
        need = [r["resource_id"]] + [str(x) for x in r.get("identifiers", [])]
        missing = [t for t in need if t.lower() not in text]
        if missing:
            fails.append((fid, r["resource_id"], missing, r["state"]))
            print("FAIL", fid, r["resource_id"], "missing", missing)
print("digest entries failing literal OCR check:", len(fails), "of", sum(len(v) for k, v in digest.items() if k != "_meta"))
# PNG-dependent statuses
out = {r["case_id"]: r for r in csv.DictReader(open(ROOT/"output.csv"))}
cases = {c.case_id: c for c in load_cases(ROOT/"dataset")}
png_cases = []
for cid, r in out.items():
    if r["deletion_status"] != "INCOMPLETE": continue
    c = cases[cid]; u = a.identities.resolve_email(c.email)
    fs = a.states.build(u, c.audit_at, c.requested_at)
    ds = set()
    for st in fs:
        step = planner._finding(st, a.policy)
        if not step: continue
        fact = max([f for f in a.index.facts_for(u, c.audit_at)
                    if f.resource_id == st.resource_id and f.system == st.system],
                   key=lambda f: f.observed_at, default=None)
        if fact: ds.add(a.index.files[fact.file_id].path.suffix)
    if ds == {".png"}: png_cases.append(cid)
print("eval cases whose status rests solely on PNG digest:", len(png_cases), png_cases)
print("\n== 2. exposure by (category, state) ==")
sample = {r.case_id: r for r in a.run_all("sample_deletion_requests.csv")}
scases = {c.case_id: c for c in load_cases(ROOT/"dataset", "sample_deletion_requests.csv")}
gold = {r["case_id"]: r for r in csv.DictReader(open(ROOT/"dataset/sample_output.csv"))}
def pairs(res, cases):
    out = []
    for cid in res:
        c = cases[cid]; u = a.identities.resolve_email(c.email)
        fs = a.states.build(u, c.audit_at, c.requested_at)
        out.append((cid, [(f.category, f.state) for f in fs if planner._finding(f, a.policy)]))
    return out
sp = Counter(); sa = Counter()
for cid, ps in pairs(sample, scases):
    canon = {(s["operation"], s["system_id"], s["resource_id"]) for s in json.loads(gold[cid]["steps_json"]) if s["phase"] == "FINDING"}
    for p in ps: sp[p] += 1
ep = Counter(); ed = Counter()
for cid, ps in pairs(out, cases):
    for p in ps:
        ep[p] += 1
        if len(set(ps)) == 1: ed[p] += 1
for p in sorted(set(sp) | set(ep), key=lambda x: (0 if sp[x] == 0 and ed[x] > 0 else 1, -ed[x])):
    print(f"sample {sp[p]:3d} eval {ep[p]:3d} dep {ed[p]:3d}  {p}")
print("\n== 3. staleness of FOUND-type rows ==")
stale = Counter()
for cid in out:
    c = cases[cid]; u = a.identities.resolve_email(c.email)
    for f in a.index.facts_for(u, c.audit_at):
        if f.source in ("operational_record_history", "manifest", "record_lookup"):
            inside = c.requested_at <= f.observed_at <= c.audit_at
            stale[(f.source, "inside" if inside else "earlier")] += 1
print(dict(stale))
print("\n== 4. log provenance start/completed ==")
bad = 0; checked = 0
for f in a.index.facts:
    if not str(f.source).endswith("_completed") and f.source not in ("connector_heartbeat",):
        continue
    if "__lineno" not in f.detail: continue
    ev = a.index.files[f.file_id]; lines = ev.path.read_text(errors="replace").splitlines()
    n = int(f.detail["__lineno"]); checked += 1
    line = lines[n-1] if 0 < n <= len(lines) else ""
    if not any(k in line for k in ("enabled=", "restore_allowed=", "rows=", "http_status=", "result=", "matched_value=")):
        bad += 1
        if bad <= 5: print("BAD", ev.path.name, n, f.source, line[:120])
print("checked", checked, "bad provenance", bad)
