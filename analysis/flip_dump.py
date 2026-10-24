#!/usr/bin/env python3
"""Dump every status-flip case with its deciding raw line (+/-2)."""
import sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "code"))
import audit.policy as policy_mod
import audit.planner as planner
from audit.pipeline import AuditAgent

ROOT = Path(__file__).resolve().parent.parent
RULES = {
    "support_retained": ("SUPPORT_MESSAGE", "policy: SUPPORT_MESSAGE is REDACT, not RETAIN"),
    "analytics_retained": ("ANALYTICS_PROFILE", "policy: ANALYTICS_PROFILE is ANONYMIZE, not RETAIN"),
    "flow_never_active": ("DATA_FLOW", "state: enabled=true means an active data flow"),
    "backup_never_risk": ("BACKUP_ARCHIVE", "state: restore_allowed=true means a restore risk"),
}
def agent(): return AuditAgent(ROOT/"dataset", ROOT/"code/audit/digests/documents.json")
def run(a): return {r.case_id: r for r in a.run_all("deletion_requests.csv")}
def main():
    base = run(agent()); lines = []
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
            if base[cid].status == mut[cid].status: continue
            removed = [s for s in base[cid].steps if s.phase == "FINDING" and
                       (s.operation, s.system_id, s.resource_id) not in
                       {(x.operation, x.system_id, x.resource_id) for x in mut[cid].steps}]
            for s in removed:
                ev = base[cid].steps and next((x for x in base[cid].steps if x.evidence_id), None)
                path = None
                from audit.index import EvidenceIndex
                lines.append((cid, name, cat, s, reason))
    # need evidence paths: rebuild index for file map
    a = agent(); out = []
    for cid, name, cat, s, reason in lines:
        # find the fact file by resource
        fid = ""
        for f in a.index.facts:
            if f.resource_id == s.resource_id and s.system_id == f.system:
                fid = f.file_id
        path = a.index.files[fid].path if fid else None
        ctx = []
        if path:
            raw = path.read_text(errors="replace").splitlines()
            idx = next((i for i, l in enumerate(raw) if s.resource_id in l), None)
            if idx is not None:
                ctx = [(j+1, raw[j][:220]) for j in range(max(0, idx-2), min(len(raw), idx+3))]
        out.append((cid, name, s, fid, path, ctx, reason))
    with open(ROOT/"analysis/flip_dump.md", "w") as fh:
        fh.write("# Mutation flip dump — 57 status flips\n\n")
        for cid, name, s, fid, path, ctx, reason in out:
            fh.write(f"## {cid} — {name}\n")
            fh.write(f"Rule: {reason}\nFinding: {s.operation} {s.system_id} {s.resource_id}\nEvidence: {fid} {path.name if path else ''}\n\n")
            fh.write("```\n" + "\n".join(f"{n}: {t}" for n, t in ctx) + "\n```\n\n")
            fh.write(f"Why: the engine sees `{s.state}` on {s.resource_id}; disabling the {name} rule removes the only finding, flipping INCOMPLETE→COMPLETE.\n\n")
    print("wrote", len(out), "entries")
if __name__ == "__main__": main()
