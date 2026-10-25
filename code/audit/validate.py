"""Submission validator: every contract rule we can check without the grader."""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

PHASE_ORDER = {"FINDING": 0, "REMEDIATION": 1, "VERIFICATION": 2}

OP_ORDER = {
    "REPORT_REMAINING_RECORD": 0,
    "REPORT_EXPOSED_PII": 1,
    "REPORT_ACTIVE_DATA_FLOW": 2,
    "REPORT_RESTORE_RISK": 3,
    "DISABLE_DATA_FLOW": 0,
    "BLOCK_RESTORE": 1,
    "DELETE_RECORD": 2,
    "REDACT_RECORD": 3,
    "ANONYMIZE_RECORD": 4,
    "VERIFY_RECORD_ABSENT": 0,
    "VERIFY_RECORD_PRESENT": 1,
    "VERIFY_RECORD_REDACTED": 2,
    "VERIFY_RECORD_ANONYMIZED": 3,
    "VERIFY_DATA_FLOW_DISABLED": 4,
    "VERIFY_RESTORE_BLOCKED": 5,
}

ALLOWED_STATE = {
    "REPORT_REMAINING_RECORD": "PRESENT",
    "REPORT_EXPOSED_PII": "PRESENT",
    "REPORT_ACTIVE_DATA_FLOW": "ACTIVE",
    "REPORT_RESTORE_RISK": "ACTIVE",
    "DISABLE_DATA_FLOW": "DISABLED",
    "BLOCK_RESTORE": "BLOCKED",
    "DELETE_RECORD": "ABSENT",
    "REDACT_RECORD": "REDACTED",
    "ANONYMIZE_RECORD": "ANONYMIZED",
    "VERIFY_RECORD_ABSENT": "ABSENT",
    "VERIFY_RECORD_PRESENT": "PRESENT",
    "VERIFY_RECORD_REDACTED": "REDACTED",
    "VERIFY_RECORD_ANONYMIZED": "ANONYMIZED",
    "VERIFY_DATA_FLOW_DISABLED": "DISABLED",
    "VERIFY_RESTORE_BLOCKED": "BLOCKED",
}


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_submission(output_csv: Path, requests_csv: Path,
                        evidence_csv: Path | None = None) -> Report:
    report = Report()
    with output_csv.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        if fieldnames != ["case_id", "deletion_status", "steps_json"]:
            report.errors.append(f"header is {fieldnames}")
        rows = list(reader) if set(fieldnames) >= {"case_id", "deletion_status", "steps_json"} else []
    with requests_csv.open(newline="", encoding="utf-8") as handle:
        requests = {row["case_id"]: row for row in csv.DictReader(handle)}

    captured: dict[str, datetime] = {}
    activity_at: dict[str, datetime] = {}
    audit_at_map: dict[str, datetime] = {}
    if evidence_csv and evidence_csv.exists():
        with evidence_csv.open(newline="", encoding="utf-8") as handle:
            from .model import parse_ts
            for row in csv.DictReader(handle):
                captured[row["file_id"]] = parse_ts(row["captured_at"])
    dataset_dir = requests_csv.parent
    activity_csv = dataset_dir / "system_activity.csv"
    if activity_csv.exists():
        with activity_csv.open(newline="", encoding="utf-8") as handle:
            from .model import parse_ts
            for row in csv.DictReader(handle):
                activity_at[row["activity_id"]] = parse_ts(row["event_time"])
    audit_log_csv = dataset_dir / "user_audit_log.csv"
    if audit_log_csv.exists():
        with audit_log_csv.open(newline="", encoding="utf-8") as handle:
            from .model import parse_ts
            for row in csv.DictReader(handle):
                audit_at_map[row["audit_id"]] = parse_ts(row["event_time"])

    if len(rows) != len(requests):
        report.errors.append(f"{len(rows)} rows for {len(requests)} requests")
    seen = set()
    phases = {"FINDING": 0, "REMEDIATION": 0, "VERIFICATION": 0}
    statuses = {"COMPLETE": 0, "INCOMPLETE": 0, "NOT_APPLICABLE": 0}
    for row in rows:
        case_id = row["case_id"]
        if case_id in seen:
            report.errors.append(f"{case_id}: duplicate row")
        seen.add(case_id)
        if case_id not in requests:
            report.errors.append(f"{case_id}: unknown case")
            continue
        status = row["deletion_status"]
        if status not in statuses:
            report.errors.append(f"{case_id}: bad status {status}")
        else:
            statuses[status] += 1
        try:
            steps = json.loads(row["steps_json"])
        except json.JSONDecodeError as exc:
            report.errors.append(f"{case_id}: invalid JSON ({exc})")
            continue
        if not isinstance(steps, list):
            report.errors.append(f"{case_id}: steps_json is not a list")
            continue
        if status == "NOT_APPLICABLE":
            if steps:
                report.errors.append(f"{case_id}: NOT_APPLICABLE with steps")
            continue
        if not steps:
            report.errors.append(f"{case_id}: {status} with empty steps")
        audit_at = None
        try:
            from .model import parse_ts
            audit_at = parse_ts(requests[case_id]["audit_at"])
        except Exception:
            pass
        last = (-1, "")
        has_finding = False
        for index, step in enumerate(steps, start=1):
            if step.get("step_no") != index:
                report.errors.append(f"{case_id}: step_no {step.get('step_no')} != {index}")
            phase = step.get("phase")
            if phase not in PHASE_ORDER:
                report.errors.append(f"{case_id}: bad phase {phase}")
                continue
            phases[phase] = phases.get(phase, 0) + 1
            operation = step.get("operation")
            if operation not in OP_ORDER:
                report.errors.append(f"{case_id}: bad operation {operation}")
                continue
            if ALLOWED_STATE.get(operation) != step.get("state"):
                report.errors.append(f"{case_id}: state {step.get('state')} invalid for {operation}")
            key = (PHASE_ORDER[phase], OP_ORDER[operation], step.get("system_id", ""),
                   step.get("resource_id", ""))
            if key < last:
                report.errors.append(f"{case_id}: step {index} out of canonical order")
            last = key
            evidence_id = step.get("evidence_id", "")
            if phase == "FINDING":
                has_finding = True
                if not evidence_id:
                    report.errors.append(f"{case_id}: finding {index} has no evidence")
            if status == "COMPLETE" and phase == "VERIFICATION" and not evidence_id:
                report.errors.append(f"{case_id}: COMPLETE verification {index} has no evidence")
            if status == "INCOMPLETE" and phase in {"REMEDIATION", "VERIFICATION"} and evidence_id:
                report.errors.append(f"{case_id}: future step {index} cites evidence")
            if evidence_id:
                cited_at = captured.get(evidence_id)
                if cited_at is None:
                    cited_at = activity_at.get(evidence_id)
                if cited_at is None:
                    cited_at = audit_at_map.get(evidence_id)
                if cited_at is None:
                    report.errors.append(f"{case_id}: unknown evidence {evidence_id}")
                elif audit_at and cited_at > audit_at:
                    report.errors.append(f"{case_id}: cites post-audit evidence {evidence_id}")
        if status == "COMPLETE" and has_finding:
            report.errors.append(f"{case_id}: COMPLETE with findings")
        if status == "INCOMPLETE" and not has_finding:
            report.errors.append(f"{case_id}: INCOMPLETE without findings")

    report.metrics = {
        "rows": len(rows),
        "requests": len(requests),
        "statuses": statuses,
        "phases": phases,
    }
    return report
