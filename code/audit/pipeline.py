"""End-to-end audit pipeline."""
from __future__ import annotations

from pathlib import Path

from .index import EvidenceIndex
from .intent import DELETE, classify
from .model import Case, CaseResult
from .planner import add_linked_verifications, attach_evidence, plan_steps
from .policy import Policy
from .state import StateBuilder
from .tables import IdentityGraph, load_cases


class AuditAgent:
    def __init__(self, dataset_dir: Path, digest_path: Path | None = None) -> None:
        self.dataset_dir = Path(dataset_dir)
        self.identities = IdentityGraph.build(self.dataset_dir)
        self.policy = Policy.load(self.dataset_dir)
        self.index = EvidenceIndex.load(self.dataset_dir, self.identities, digest_path)
        self.states = StateBuilder(self.index, self.identities)
        self.account_claims = {}
        activity = self.dataset_dir / "system_activity.csv"
        if activity.exists():
            import csv as _csv
            with activity.open(newline="", encoding="utf-8") as handle:
                for row in _csv.DictReader(handle):
                    if row.get("event_type") == "DELETE_RECORD" and row.get("target_system") == "account_service":
                        self.account_claims.setdefault(row["resource_id"], []).append(
                            __import__("audit.model", fromlist=["parse_ts"]).parse_ts(row["event_time"]))

    def audit(self, case: Case) -> CaseResult:
        verdict, _reason = classify(case.request_text)
        if verdict != DELETE:
            return CaseResult(case.case_id, "NOT_APPLICABLE", [])
        user_id = self.identities.resolve_email(case.email)
        if not user_id:
            user_id = self.identities.resolve_identifier(case.email)
        if not user_id:
            # An unresolvable subject cannot be audited; the safe answer is
            # that no authorized deletion could be verified.
            return CaseResult(case.case_id, "NOT_APPLICABLE", [])
        states = self.states.build(user_id, case.audit_at, case.requested_at)
        status, steps = plan_steps(states, self.policy)
        steps = add_linked_verifications(case, user_id, steps, self.index, self.account_claims)
        steps = attach_evidence(states, steps, self.index, case.audit_at, status,
                                self.policy)
        return CaseResult(case.case_id, status, steps)

    def run_all(self, filename: str = "deletion_requests.csv") -> list[CaseResult]:
        return [self.audit(case) for case in load_cases(self.dataset_dir, filename)]
