#!/usr/bin/env python3
"""Negative controls for the validator: every illegal output must be caught."""
import csv, json, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))
from audit.validate import validate_submission

base = list(csv.DictReader(open(ROOT/"output.csv")))
by = {r["case_id"]: r for r in base}
HEADER = ["case_id","deletion_status","steps_json"]

def write(rows, path):
    with open(path,"w",newline="") as fh:
        w=csv.DictWriter(fh,HEADER); w.writeheader(); w.writerows(rows)

def steps(cid): return json.loads(by[cid]["steps_json"])
def with_steps(cid, new, status=None):
    rows=[dict(r) for r in base]
    for r in rows:
        if r["case_id"]==cid:
            r["steps_json"]=json.dumps(new)
            if status: r["deletion_status"]=status
    return rows

def expect(name, rows, ok_if_error=True):
    p=Path(tempfile.mkdtemp())/"o.csv"; write(rows,p)
    rep=validate_submission(p, ROOT/"dataset/deletion_requests.csv", ROOT/"dataset/evidence_files.csv")
    caught=bool(rep.errors)
    print(f"{name:42} {'PASS' if caught==ok_if_error else 'FAIL'}  errors={len(rep.errors)}  first={rep.errors[0] if rep.errors else '-'}")
    return caught==ok_if_error

checks=[]
# A. rows / ids / header
checks.append(expect("A1 517 rows", base[:-1]))
d=[dict(r) for r in base]; d[1]["case_id"]=d[0]["case_id"]; checks.append(expect("A2 duplicate case_id", d))
with open("/tmp/bad_header.csv","w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["case","status","steps"]); [w.writerow([r["case_id"],r["deletion_status"],r["steps_json"]]) for r in base]
rep=validate_submission(Path("/tmp/bad_header.csv"), ROOT/"dataset/deletion_requests.csv", ROOT/"dataset/evidence_files.csv")
print(f"{'A3 wrong header':42} {'PASS' if rep.errors else 'FAIL'}  errors={len(rep.errors)}  first={rep.errors[0] if rep.errors else '-'}")
checks.append(bool(rep.errors))
# B. status/step invariants
checks.append(expect("B1 COMPLETE with []", with_steps("case_57", [], "COMPLETE")))
checks.append(expect("B2 N/A with steps", with_steps("case_533", steps("case_57"), "NOT_APPLICABLE")))
s=[x for x in steps("case_33") if x["phase"]=="VERIFICATION"]
checks.append(expect("B3 INCOMPLETE without findings", with_steps("case_33", s, "INCOMPLETE")))
bad=[dict(r) for r in base]; bad[0]["deletion_status"]="BANANA"; checks.append(expect("B4 bad status", bad))
# C. numbering / order
s=steps("case_33"); s[1]["step_no"]=4; checks.append(expect("C1 non-consecutive step_no", with_steps("case_33", s, "INCOMPLETE")))
s=steps("case_33"); s[0]["phase"],s[1]["phase"]=s[1]["phase"],s[0]["phase"]; checks.append(expect("C2 phase order", with_steps("case_33", s, "INCOMPLETE")))
s=steps("case_33")+[{"step_no":4,"phase":"VERIFICATION","system_id":"aaa_service","resource_id":"audit_record_1","operation":"VERIFY_RECORD_ABSENT","state":"ABSENT","evidence_id":""}]; checks.append(expect("C3 tie-break order", with_steps("case_33", s, "INCOMPLETE")))
# D. provenance / time
s=steps("case_33"); s[2]["evidence_id"]="evidence_32"; checks.append(expect("D1 future step cites evidence", with_steps("case_33", s, "INCOMPLETE")))
s=steps("case_57"); s[0]["evidence_id"]="evidence_94"; checks.append(expect("D2 post-audit evidence", with_steps("case_57", s, "COMPLETE")))
s=steps("case_33"); s[0]["evidence_id"]="activity_4006"; checks.append(expect("D3 valid activity citation", with_steps("case_33", s, "INCOMPLETE"), ok_if_error=False))
s=steps("case_33"); s[0]["evidence_id"]="activity_9999"; checks.append(expect("D4 unknown activity citation", with_steps("case_33", s, "INCOMPLETE")))
s=steps("case_33"); s[0]["evidence_id"]="activity_3387"; checks.append(expect("D5 post-audit activity", with_steps("case_33", s, "INCOMPLETE")))
print(f"\n{sum(checks)}/{len(checks)} negative controls caught")
sys.exit(0 if all(checks) else 1)
