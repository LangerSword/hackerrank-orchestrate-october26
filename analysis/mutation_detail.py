#!/usr/bin/env python3
"""Instrumented mutation detail: branch counters, status flips, deciding facts."""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))

import audit.policy as policy_mod  # noqa: E402
import audit.planner as planner  # noqa: E402
import audit.index as index_mod  # noqa: E402
import audit.state as state_mod  # noqa: E402
from audit.pipeline import AuditAgent  # noqa: E402
from audit.tables import load_cases  # noqa: E402


def agent():
    return AuditAgent(ROOT / "dataset", ROOT / "code/audit/digests/documents.json")


def run(a, f):
    return {r.case_id: r for r in a.run_all(f)}


def sig(r):
    return (r.status, tuple((s.phase, s.system_id, s.resource_id, s.operation, s.state) for s in r.steps))


def main() -> int:
    a = agent()
    base_s = run(a, "sample_deletion_requests.csv")
    base_e = run(a, "deletion_requests.csv")
    cases = {c.case_id: c for c in load_cases(ROOT / "dataset")}

    # counters for the four questioned mutations
    phone_hits = Counter()
    orig = index_mod.IdentityGraph.resolve_identifier

    def counted(self, value):
        out = orig(self, value)
        v = (value or "").strip()
        if out and not any(ch.isalpha() for ch in v) and sum(ch.isdigit() for ch in v) >= 7:
            phone_hits["phone"] += 1
        return out

    with patch.object(index_mod.IdentityGraph, "resolve_identifier", counted):
        agent()
    catalog = sum(1 for f in a.index.facts if "catalog_link" in (f.detail.get("paths") or []))
    seeded = sum(len(v) for v in a.index.resource_link_paths.values())
    empty_calls = 0
    for case in cases.values():
        u = a.identities.resolve_email(case.email)
        if a.states._empty_snapshots(a.index.facts_for(u, case.audit_at)):
            empty_calls += 1
    # citation difference: newest-only vs current choice
    cite_diff = 0
    for cid, r in base_e.items():
        steps = json.loads(json.dumps([s.as_dict(i + 1) for i, s in enumerate(r.steps)]))
        if not steps:
            continue
        relevant = {s["resource_id"] for s in steps}
        viol = {s["resource_id"] for s in steps if s["phase"] == "FINDING"}
        cur = next((s["evidence_id"] for s in steps if s["evidence_id"]), "")
        cands = [(len({f.resource_id for f in a.index.facts if f.file_id == fid and f.resource_id in relevant}),
                  len({f.resource_id for f in a.index.facts if f.file_id == fid and f.resource_id in relevant} & viol),
                  ev.captured_at, fid) for fid, ev in a.index.files.items() if ev.captured_at <= cases[cid].audit_at]
        cands = [c for c in cands if c[0]]
        if not cands:
            continue
        if viol:
            best = max(c[1] for c in cands)
            top = [c for c in cands if c[1] == best]
        else:
            best = max(c[0] for c in cands)
            top = [c for c in cands if c[0] == best]
        top.sort(key=lambda c: (c[2], c[3]))
        if top[-1][3] != cur:
            cite_diff += 1
    print(f"counters: phone_identity_matches={phone_hits['phone']} catalog_path_facts={catalog} "
          f"catalog_seeds={seeded} empty_snapshot_calls={empty_calls} citation_choice_differs={cite_diff}")

    # status-flipping mutations: list changed cases + removed finding
    muts = {
        "support_retained": ("SUPPORT_MESSAGE", "SUPPORT_MESSAGE"),
        "analytics_retained": ("ANALYTICS_PROFILE", "ANALYTICS_PROFILE"),
        "flow_never_active": ("DATA_FLOW", "DATA_FLOW"),
        "backup_never_risk": ("BACKUP_ARCHIVE", "BACKUP_ARCHIVE"),
    }
    for name, (cat, _) in muts.items():
        if name.endswith("retained"):
            orig_action = policy_mod.Policy.action_for
            with patch.object(policy_mod.Policy, "action_for",
                              lambda self, c, cat=cat, o=orig_action: "RETAIN" if c == cat else o(self, c)):
                m = run(agent(), "deletion_requests.csv")
        else:
            orig_find = planner._finding
            with patch.object(planner, "_finding",
                              lambda st, p, cat=cat, o=orig_find: None if st.category == cat else o(st, p)):
                m = run(agent(), "deletion_requests.csv")
        flipped = [cid for cid in base_e if base_e[cid].status != m[cid].status]
        print(f"\n{name}: {len(flipped)} status flips")
        for cid in flipped[:25]:
            removed = [(s.operation, s.system_id, s.resource_id, s.evidence_id)
                       for s in base_e[cid].steps
                       if s.phase == "FINDING" and (s.operation, s.system_id, s.resource_id)
                       not in {(x.operation, x.system_id, x.resource_id) for x in m[cid].steps}]
            print(f"  {cid} {base_e[cid].status}->{m[cid].status} removed={removed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
