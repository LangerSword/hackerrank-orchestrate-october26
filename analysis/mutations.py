#!/usr/bin/env python3
"""Mutation testing: disable/invert each rule, measure sample vs eval deltas."""
from __future__ import annotations

import csv
import json
import sys
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))

import audit.pipeline as pipeline  # noqa: E402
import audit.planner as planner  # noqa: E402
import audit.policy as policy_mod  # noqa: E402
import audit.index as index_mod  # noqa: E402
import audit.state as state_mod  # noqa: E402
from audit.pipeline import AuditAgent  # noqa: E402
from audit.tables import load_cases  # noqa: E402


def signature(result):
    return (result.status, tuple((s.phase, s.system_id, s.resource_id, s.operation, s.state)
                                 for s in result.steps))


def run(agent, filename):
    return {r.case_id: r for r in agent.run_all(filename)}


def compare(base, mut):
    status = sum(1 for c in base if base[c].status != mut[c].status)
    steps = sum(1 for c in base if signature(base[c]) != signature(mut[c]))
    return status, steps


def make_agent():
    return AuditAgent(ROOT / "dataset", ROOT / "code/audit/digests/documents.json")


@contextmanager
def mutation(name):
    if name == "intent_always_delete":
        with patch.object(pipeline, "classify", lambda text: ("DELETE", "mut")):
            yield
    elif name == "no_findings":
        with patch.object(policy_mod.Policy, "is_violation", lambda self, c, s: False):
            yield
    elif name == "support_retained":
        orig = policy_mod.Policy.action_for
        with patch.object(policy_mod.Policy, "action_for",
                          lambda self, c: "RETAIN" if c == "SUPPORT_MESSAGE" else orig(self, c)):
            yield
    elif name == "analytics_retained":
        orig = policy_mod.Policy.action_for
        with patch.object(policy_mod.Policy, "action_for",
                          lambda self, c: "RETAIN" if c == "ANALYTICS_PROFILE" else orig(self, c)):
            yield
    elif name == "backup_never_risk":
        orig = policy_mod.Policy.is_violation
        with patch.object(policy_mod.Policy, "is_violation",
                          lambda self, c, s: False if c == "BACKUP_ARCHIVE" else orig(self, c, s)):
            yield
    elif name == "flow_never_active":
        orig = policy_mod.Policy.is_violation
        with patch.object(policy_mod.Policy, "is_violation",
                          lambda self, c, s: False if c == "DATA_FLOW" else orig(self, c, s)):
            yield
    elif name == "verify_order_reversed":
        rev = {k: -v for k, v in planner.VERIFICATION_ORDER.items()}
        with patch.object(planner, "VERIFICATION_ORDER", rev):
            yield
    elif name == "drop_verify_present":
        orig = planner._verification
        with patch.object(planner, "_verification",
                          lambda st, p: None if p.required_final_state(st.category) == "PRESENT"
                          else orig(st, p)):
            yield
    elif name == "drop_remediation":
        orig = planner._remediation
        with patch.object(planner, "_remediation", lambda st, f, p: None):
            yield
    elif name == "ignore_hash_identity":
        orig = index_mod.IdentityGraph.resolve_identifier
        def no_hash(self, value):
            v = (value or "").strip().lower()
            if len(v) == 64 and all(c in "0123456789abcdef" for c in v):
                return ""
            return orig(self, value)
        with patch.object(index_mod.IdentityGraph, "resolve_identifier", no_hash):
            yield
    elif name == "ignore_phone_identity":
        orig = index_mod.IdentityGraph.resolve_identifier
        def no_phone(self, value):
            v = (value or "").strip()
            if not any(ch.isalpha() for ch in v) and sum(ch.isdigit() for ch in v) >= 7:
                return ""
            return orig(self, value)
        with patch.object(index_mod.IdentityGraph, "resolve_identifier", no_phone):
            yield
    elif name == "ignore_catalog_links":
        with patch.object(index_mod.EvidenceIndex, "_seed_activity_links", lambda self, ids: None):
            yield
    elif name == "no_empty_snapshots":
        with patch.object(state_mod.StateBuilder, "_empty_snapshots", lambda self, facts: []):
            yield
    elif name == "citation_newest_only":
        def newest(states, steps, index, audit_at, status, policy):
            if not steps:
                return steps
            candidates = [ev for ev in index.files.values() if ev.captured_at <= audit_at]
            if not candidates:
                return steps
            fid = max(candidates, key=lambda e: (e.captured_at, e.file_id)).file_id
            out = []
            for s in steps:
                if s.phase == "FINDING" or status == "COMPLETE":
                    out.append(planner.Step(s.phase, s.system_id, s.resource_id,
                                            s.operation, s.state, fid))
                else:
                    out.append(s)
            return out
        with patch.object(planner, "attach_evidence", newest):
            yield
    else:
        raise ValueError(name)


MUTATIONS = [
    "intent_always_delete", "no_findings", "support_retained", "analytics_retained",
    "backup_never_risk", "flow_never_active", "verify_order_reversed",
    "drop_verify_present", "drop_remediation", "ignore_hash_identity",
    "ignore_phone_identity", "ignore_catalog_links", "no_empty_snapshots",
    "citation_newest_only",
]


def main() -> int:
    base_agent = make_agent()
    base_sample = run(base_agent, "sample_deletion_requests.csv")
    base_eval = run(base_agent, "deletion_requests.csv")

    rows = []
    for name in MUTATIONS:
        with mutation(name):
            agent = make_agent()
            sample = run(agent, "sample_deletion_requests.csv")
            evals = run(agent, "deletion_requests.csv")
        ss, sstep = compare(base_sample, sample)
        es, estep = compare(base_eval, evals)
        rows.append((name, ss, sstep, es, estep))
        print(f"{name:24} sample status {ss:2d} steps {sstep:2d} | eval status {es:3d} steps {estep:3d}")

    print("\nUnvalidated (sample delta 0) ranked by eval exposure:")
    for r in sorted([r for r in rows if r[1] == 0 and r[2] == 0], key=lambda x: -x[4]):
        print(f"  {r[0]:24} eval status {r[3]:3d} steps {r[4]:3d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
