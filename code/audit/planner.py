"""Step planning: findings -> remediation -> verification in canonical order."""
from __future__ import annotations

from datetime import datetime

from .model import (
    ABSENT,
    ACCOUNT_TOMBSTONE,
    ACTIVE,
    ANONYMIZED,
    BACKUP_ARCHIVE,
    BLOCKED,
    DISABLED,
    IDENTIFIABLE,
    PRESENT,
    REDACTED,
    ResourceState,
    Step,
)
from .policy import ANONYMIZE, DELETE, REDACT, Policy

PHASES = ("FINDING", "REMEDIATION", "VERIFICATION")

FINDING_ORDER = {
    "REPORT_REMAINING_RECORD": 0,
    "REPORT_EXPOSED_PII": 1,
    "REPORT_ACTIVE_DATA_FLOW": 2,
    "REPORT_RESTORE_RISK": 3,
}
REMEDIATION_ORDER = {
    "DISABLE_DATA_FLOW": 0,
    "BLOCK_RESTORE": 1,
    "DELETE_RECORD": 2,
    "REDACT_RECORD": 3,
    "ANONYMIZE_RECORD": 4,
}
VERIFICATION_ORDER = {
    "VERIFY_RECORD_ABSENT": 0,
    "VERIFY_RECORD_PRESENT": 1,
    "VERIFY_RECORD_REDACTED": 2,
    "VERIFY_RECORD_ANONYMIZED": 3,
    "VERIFY_DATA_FLOW_DISABLED": 4,
    "VERIFY_RESTORE_BLOCKED": 5,
}

REMEDIATION_FOR_FINDING = {
    "REPORT_REMAINING_RECORD": ("DELETE_RECORD", ABSENT),
    "REPORT_EXPOSED_PII": None,  # depends on policy action
    "REPORT_ACTIVE_DATA_FLOW": ("DISABLE_DATA_FLOW", DISABLED),
    "REPORT_RESTORE_RISK": ("BLOCK_RESTORE", BLOCKED),
}

VERIFICATION_FOR_STATE = {
    ABSENT: ("VERIFY_RECORD_ABSENT", ABSENT),
    PRESENT: ("VERIFY_RECORD_PRESENT", PRESENT),
    REDACTED: ("VERIFY_RECORD_REDACTED", REDACTED),
    ANONYMIZED: ("VERIFY_RECORD_ANONYMIZED", ANONYMIZED),
    DISABLED: ("VERIFY_DATA_FLOW_DISABLED", DISABLED),
    BLOCKED: ("VERIFY_RESTORE_BLOCKED", BLOCKED),
}


def _finding(state: ResourceState, policy: Policy) -> Step | None:
    category = state.category
    if category == "DATA_FLOW":
        if state.state == ACTIVE:
            return Step("FINDING", state.system, state.resource_id,
                        "REPORT_ACTIVE_DATA_FLOW", ACTIVE)
        return None
    if category == BACKUP_ARCHIVE:
        if state.state == ACTIVE:
            return Step("FINDING", state.system, state.resource_id,
                        "REPORT_RESTORE_RISK", ACTIVE)
        return None
    if not policy.is_violation(category, state.state):
        return None
    action = policy.action_for(category)
    if action == DELETE:
        return Step("FINDING", state.system, state.resource_id,
                    "REPORT_REMAINING_RECORD", PRESENT)
    return Step("FINDING", state.system, state.resource_id,
                "REPORT_EXPOSED_PII", PRESENT)


def _remediation(state: ResourceState, finding: Step, policy: Policy) -> Step | None:
    mapping = REMEDIATION_FOR_FINDING.get(finding.operation)
    if mapping is None:
        action = policy.action_for(state.category)
        if action == REDACT:
            return Step("REMEDIATION", state.system, state.resource_id,
                        "REDACT_RECORD", REDACTED)
        if action == ANONYMIZE:
            return Step("REMEDIATION", state.system, state.resource_id,
                        "ANONYMIZE_RECORD", ANONYMIZED)
        return Step("REMEDIATION", state.system, state.resource_id,
                    "DELETE_RECORD", ABSENT)
    operation, final_state = mapping
    return Step("REMEDIATION", state.system, state.resource_id, operation, final_state)


def _verification(state: ResourceState, policy: Policy) -> Step | None:
    target = policy.required_final_state(state.category)
    operation, observed_state = VERIFICATION_FOR_STATE[target]
    return Step("VERIFICATION", state.system, state.resource_id, operation, observed_state)


def plan_steps(states: list[ResourceState], policy: Policy) -> tuple[str, list[Step]]:
    findings: list[Step] = []
    remediation: list[Step] = []
    verification: list[Step] = []
    seen: set[tuple[str, str, str]] = set()

    for state in states:
        finding = _finding(state, policy)
        if finding and (finding.operation, finding.system_id, finding.resource_id) not in seen:
            seen.add((finding.operation, finding.system_id, finding.resource_id))
            findings.append(finding)
            fix = _remediation(state, finding, policy)
            if fix:
                remediation.append(fix)
        verify = _verification(state, policy)
        if verify:
            key = (verify.operation, verify.system_id, verify.resource_id)
            if key not in seen:
                seen.add(key)
                verification.append(verify)

    findings.sort(key=lambda s: (FINDING_ORDER[s.operation], s.system_id, s.resource_id))
    remediation.sort(key=lambda s: (REMEDIATION_ORDER[s.operation], s.system_id, s.resource_id))
    verification.sort(
        key=lambda s: (VERIFICATION_ORDER[s.operation], s.system_id, s.resource_id)
    )
    status = "INCOMPLETE" if findings else "COMPLETE"
    return status, findings + remediation + verification


def add_linked_verifications(case, user_id, steps, index, claims):
    """A linked account with a deletion claim and no readback gets a future
    verification in an INCOMPLETE case. The claim is not proof; the step exists
    because the state is unverified."""
    if not steps or not any(s.phase == "FINDING" for s in steps):
        return steps
    known = {s.resource_id for s in steps}
    linked = {}
    for f in index.facts_for(user_id, case.audit_at):
        acc = (f.detail or {}).get("source_resource_id")
        if f.system == "search_service" and acc:
            linked[acc] = f.observed_at
    added = []
    for acc, observed in linked.items():
        if acc in known:
            continue
        times = claims.get(acc, [])
        if not any(case.requested_at <= t <= case.audit_at for t in times):
            continue
        added.append(Step("VERIFICATION", "account_service", acc,
                          "VERIFY_RECORD_ABSENT", ABSENT))
    if not added:
        return steps
    out = list(steps) + added
    out.sort(key=lambda s: (PHASES.index(s.phase),
                            {"FINDING": FINDING_ORDER, "REMEDIATION": REMEDIATION_ORDER,
                             "VERIFICATION": VERIFICATION_ORDER}[s.phase].get(s.operation, 99),
                            s.system_id, s.resource_id))
    return out


def attach_evidence(
    states: list[ResourceState],
    steps: list[Step],
    index,
    audit_at: datetime,
    status: str,
    policy: Policy,
) -> list[Step]:
    """Pick the newest pre-audit artefact that proves the case's state."""
    if status == "NOT_APPLICABLE" or not steps:
        return steps
    relevant = {s.resource_id for s in states}
    violating = {s.resource_id for s in states if policy.is_violation(s.category, s.state)}
    candidates = []
    for file_id, evidence in index.files.items():
        if evidence.captured_at > audit_at:
            continue
        facts = [f for f in index.facts if f.file_id == file_id and f.resource_id in relevant]
        if not facts:
            continue
        covered = {f.resource_id for f in facts}
        candidates.append((len(covered & violating), len(covered), evidence.captured_at, file_id))
    if not candidates:
        return steps
    if status == "INCOMPLETE":
        # Prefer the artefact that proves the most violations, then the newest.
        candidates.sort(key=lambda c: (c[0], c[1], c[2], c[3]))
    else:
        candidates.sort(key=lambda c: (c[1], c[2], c[3]))
    evidence_id = candidates[-1][3]

    out = []
    for step in steps:
        if step.phase == "FINDING" or status == "COMPLETE":
            out.append(Step(step.phase, step.system_id, step.resource_id,
                            step.operation, step.state, evidence_id))
        else:
            out.append(step)
    return out


def _is_violating(state: ResourceState) -> bool:
    if state.category == "DATA_FLOW":
        return state.state == ACTIVE
    if state.category == BACKUP_ARCHIVE:
        return state.state == ACTIVE
    return state.state in {PRESENT, IDENTIFIABLE}
