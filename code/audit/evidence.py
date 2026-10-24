"""Evidence ingestion: turn the manifest's files into time-stamped facts.

Each supplied artefact is a normal business record.  The parser only extracts
what the record says (who, which resource, what state, observed when); policy
and planning happen later.  Formats covered:

* records-assurance JSON exports (`service_exports`, snapshot bundles,
  manifests, export jobs, analytics reports)
* SQLite-compatible SQL snapshots (inventory, replicas, search primary)
* observability logs (four different line dialects)
* plain-text handover notes
* PDF documents and console screenshots (text digest cache)
"""
from __future__ import annotations

import json
import re
import sqlite3
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .model import (
    ABSENT,
    ACCOUNT_TOMBSTONE,
    ACTIVE,
    ANALYTICS_PROFILE,
    ANONYMIZED,
    BACKUP_ARCHIVE,
    BLOCKED,
    CACHE_ENTRY,
    DISABLED,
    EMAIL_DELIVERY_LOG,
    IDENTIFIABLE,
    LEGAL_HOLD_RECORD,
    MARKETING_PROFILE,
    PRESENT,
    PRODUCT_TELEMETRY,
    REDACTED,
    SEARCH_INDEX_ENTRY,
    SECONDARY_IDENTIFIER,
    SECURITY_AUDIT_LOG,
    SUPPORT_ATTACHMENT,
    SUPPORT_MESSAGE,
    USER_EXPORT,
    USER_PROFILE,
    Fact,
    norm_email,
    norm_hash,
    norm_phone,
    parse_ts,
)

KEEP = "RETAIN"


def _add(bucket: list, fact) -> None:
    if fact is not None:
        bucket.append(fact)


@dataclass(frozen=True)
class EvidenceFile:
    file_id: str
    path: Path
    origin: str
    captured_at: datetime

    @property
    def name(self) -> str:
        return self.path.name


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _identifiers(record: dict, extra_keys=()) -> frozenset[str]:
    """Collect direct identifiers from a record without guessing."""
    out: set[str] = set()
    for key in (
        "email",
        "customer_email",
        "owner_email",
        "requester_email",
        "subject_reference",
        "customer_reference",
        "user_id",
        "subject_selector",
        "uploaded_by",
        "matched_value",
        "lookup_key",
        "lookup_value",
        *extra_keys,
    ):
        value = record.get(key)
        if isinstance(value, str) and value.strip() and value.strip().lower() not in {"null", "none"}:
            out.add(value.strip())
    document = record.get("document")
    if isinstance(document, dict):
        out |= _identifiers(document)
    for key in ("phone", "requester_phone", "owner_phone"):
        value = record.get(key)
        if isinstance(value, str) and norm_phone(value):
            out.add("p:" + norm_phone(value))
    for key in ("email_hash",):
        value = record.get(key)
        if isinstance(value, str) and norm_hash(value):
            out.add(value.strip())
    return frozenset(out)


_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
_PHONE_RE = re.compile(r"\+?\d[\d ()-]{7,}\d")
_HASH_RE = re.compile(r"\b[0-9a-f]{64}\b")


def _text_has_pii(value: str) -> bool:
    text = value or ""
    if "[REDACTED]" in text.upper():
        text = text.replace("[REDACTED]", "").replace("[redacted]", "")
    return bool(_EMAIL_RE.search(text) or _HASH_RE.search(text) or _PHONE_RE.search(text))


def _has_direct_pii(record: dict) -> bool:
    for key in (
        "message_text",
        "message_excerpt",
        "body",
        "content",
    ):
        value = record.get(key)
        if isinstance(value, str) and _text_has_pii(value):
            return True
    for key in (
        "email",
        "phone",
        "email_hash",
        "full_name",
        "requester_email",
        "requester_name",
        "requester_phone",
        "display_name",
        "name",
    ):
        value = record.get(key)
        if isinstance(value, str) and value.strip() and value.strip().lower() != "null":
            return True
    document = record.get("document")
    if isinstance(document, dict) and _has_direct_pii(document):
        return True
    return False


def _infer_category(system: str, collection: str, record: dict) -> str:
    blob = f"{collection} {system}".lower()
    if "tombstone" in blob or "deleted_customer_reference" in blob or system == "identity_service":
        return ACCOUNT_TOMBSTONE
    if "attachment" in blob:
        return SUPPORT_ATTACHMENT
    if "support" in blob:
        return SUPPORT_MESSAGE
    if "search" in blob:
        return SEARCH_INDEX_ENTRY
    if "analytics" in blob or "telemetry" in blob:
        return ANALYTICS_PROFILE if "analytics" in blob else PRODUCT_TELEMETRY
    if "backup" in blob:
        return BACKUP_ARCHIVE
    if "connector" in blob or "data_flow" in blob or system == "integration_service":
        return "DATA_FLOW"
    if "export" in blob:
        return USER_EXPORT
    if "marketing" in blob:
        return MARKETING_PROFILE
    if "delivery" in blob or "email" in blob:
        return EMAIL_DELIVERY_LOG
    if "cache" in blob:
        return CACHE_ENTRY
    if "legal" in blob or "retained_order" in blob:
        return LEGAL_HOLD_RECORD
    if "security" in blob or "audit" in blob:
        return SECURITY_AUDIT_LOG
    if "profile" in blob or "account" in blob:
        return USER_PROFILE
    return ""


def _state_for_category(category: str, record: dict) -> str:
    if category == "DATA_FLOW":
        return ACTIVE if record.get("enabled") in (True, 1, "1", "true", "True") else DISABLED
    if category == BACKUP_ARCHIVE:
        allowed = record.get("restore_allowed")
        return ACTIVE if allowed in (True, 1, "1", "true", "True") else BLOCKED
    if category in (ACCOUNT_TOMBSTONE, SUPPORT_MESSAGE, EMAIL_DELIVERY_LOG):
        return IDENTIFIABLE if _has_direct_pii(record) else REDACTED
    if category in (ANALYTICS_PROFILE, PRODUCT_TELEMETRY):
        return IDENTIFIABLE if _has_direct_pii(record) else ANONYMIZED
    if category in (SECURITY_AUDIT_LOG, LEGAL_HOLD_RECORD):
        return PRESENT
    return PRESENT


def _resource_of(record: dict) -> str:
    return str(record.get("resource_id") or record.get("id") or "").strip()


def _make_fact(
    evidence: EvidenceFile,
    system: str,
    category: str,
    resource_id: str,
    state: str,
    observed_at: datetime,
    identifiers: frozenset[str] = frozenset(),
    user_ref: str = "",
    source: str = "",
    detail: dict | None = None,
) -> Fact | None:
    if not resource_id:
        return None
    return Fact(
        system=system.strip(),
        category=category,
        resource_id=resource_id,
        state=state,
        observed_at=observed_at,
        file_id=evidence.file_id,
        file_captured_at=evidence.captured_at,
        identifiers=identifiers,
        user_ref=user_ref,
        origin=evidence.origin,
        source=source,
        detail=detail or {},
    )


# --------------------------------------------------------------------------
# JSON
# --------------------------------------------------------------------------
def _parse_service_export(evidence: EvidenceFile, doc: dict) -> list[Fact]:
    facts: list[Fact] = []
    exports = doc.get("service_exports") or {}
    for system, collections in exports.items():
        if not isinstance(collections, dict):
            continue
        for collection, rows in collections.items():
            if not isinstance(rows, list):
                continue
            for row in rows:
                if not isinstance(row, dict):
                    continue
                observed = parse_ts(row.get("observed_at") or doc.get("exported_at") or "")
                resource_id = _resource_of(row)
                if system == "account_service":
                    profile = row.get("profile")
                    detail = profile or {}
                    state = PRESENT if profile else ABSENT
                    if row.get("status_code") in (404, 410):
                        state = ABSENT
                    facts.append(
                        _make_fact(evidence, system, USER_PROFILE, resource_id, state,
                                   observed, _identifiers(detail), source=collection)
                    )
                elif system == "search_service":
                    hits = row.get("hits") or {}
                    documents = hits.get("documents") or []
                    total = hits.get("total", len(documents))
                    if documents:
                        for doc_row in documents:
                            facts.append(
                                _make_fact(evidence, system, SEARCH_INDEX_ENTRY,
                                           _resource_of(doc_row) or resource_id, PRESENT,
                                           observed, _identifiers(doc_row), source=collection)
                            )
                    elif total == 0:
                        facts.append(
                            _make_fact(evidence, system, SEARCH_INDEX_ENTRY, resource_id,
                                       ABSENT, observed, _identifiers(row), source=collection)
                        )
                else:
                    category = _infer_category(system, collection, row)
                    state = _state_for_category(category, row)
                    if category == BACKUP_ARCHIVE and row.get("restore_allowed") is True:
                        state = ACTIVE
                    if category == "DATA_FLOW" and row.get("enabled") is True:
                        state = ACTIVE
                    user_ref = str(row.get("customer_reference") or row.get("subject_reference") or "")
                    facts.append(
                        _make_fact(evidence, system, category, resource_id, state, observed,
                                   _identifiers(row), user_ref=user_ref, source=collection,
                                   detail={"message_text": row.get("message_excerpt")
                                           or row.get("message_text") or ""})
                    )
    return [f for f in facts if f]


def _parse_snapshot_bundle(evidence: EvidenceFile, doc: dict):
    facts: list[Fact] = []
    empties: list[dict] = []
    for snapshot in doc.get("snapshots") or []:
        store = str(snapshot.get("data_store") or "")
        collection = str(snapshot.get("collection") or "")
        captured = parse_ts(snapshot.get("captured_at") or doc.get("exported_at") or "")
        records = snapshot.get("records") or []
        category = _infer_category(store, collection, {})
        for record in records:
            if not isinstance(record, dict):
                continue
            if record.get("record_type") and record.get("system"):
                system = str(record["system"])
                cat = _infer_category(system, str(record["record_type"]), record)
                name = str(record.get("result") or "").upper()
                state = {
                    "NOT_FOUND": ABSENT, "FOUND": PRESENT, "REDACTED": REDACTED,
                    "ANONYMIZED": ANONYMIZED, "DISABLED": DISABLED,
                    "BLOCKED": BLOCKED, "ACTIVE": ACTIVE,
                    "IDENTIFIABLE": IDENTIFIABLE,
                }.get(name, _state_for_category(cat, record))
                observed = parse_ts(record.get("recorded_at") or captured.isoformat())
                _add(facts, _make_fact(
                    evidence, system, cat, _resource_of(record), state, observed,
                    _identifiers(record), source=collection,
                ))
                continue
            cat = _infer_category(store, collection, record)
            state = _state_for_category(cat, record)
            _add(facts, _make_fact(
                evidence, store, cat, _resource_of(record), state, captured,
                _identifiers(record),
                user_ref=str(record.get("customer_reference") or ""),
                source=collection,
                detail={"message_text": record.get("message_text")
                        or record.get("message_excerpt") or ""},
            ))
        if not records:
            empties.append({
                "file_id": evidence.file_id,
                "store": store,
                "category": category,
                "collection": collection,
                "captured_at": captured,
            })
    return facts, empties


def _parse_manifest(evidence: EvidenceFile, doc: dict) -> list[Fact]:
    facts: list[Fact] = []
    for record in doc.get("records") or []:
        if not isinstance(record, dict):
            continue
        system = str(record.get("system") or "")
        category = _infer_category(system, str(record.get("record_type") or ""), record)
        result = str(record.get("result") or "").upper()
        if result in {"NOT_FOUND", "ABSENT"}:
            state = ABSENT
        elif result == "FOUND":
            state = PRESENT
        elif result in {"REDACTED", "DISABLED", "ANONYMIZED", "BLOCKED", "ACTIVE", "IDENTIFIABLE"}:
            state = result
        else:
            state = _state_for_category(category, record)
        observed = parse_ts(record.get("recorded_at") or doc.get("exported_at") or "")
        facts.append(
            _make_fact(evidence, system, category, _resource_of(record), state, observed,
                       _identifiers(record),
                       user_ref=str(record.get("customer_reference") or record.get("subject_reference") or ""),
                       source="manifest")
        )
    return [f for f in facts if f]


def _parse_export_jobs(evidence: EvidenceFile, doc: dict) -> list[Fact]:
    facts = []
    captured = parse_ts(doc.get("captured_at") or doc.get("exported_at") or "")
    for record in doc.get("records") or []:
        if not isinstance(record, dict):
            continue
        state = PRESENT if record.get("download_available", True) else ABSENT
        facts.append(
            _make_fact(evidence, "export_service", USER_EXPORT, _resource_of(record),
                       state, captured, _identifiers(record), source="customer_export_jobs")
        )
    return [f for f in facts if f]


def _parse_analytics(evidence: EvidenceFile, doc: dict) -> list[Fact]:
    facts = []
    captured = parse_ts(doc.get("captured_at") or doc.get("exported_at") or "")
    for record in doc.get("records") or []:
        if not isinstance(record, dict):
            continue
        facts.append(
            _make_fact(evidence, "analytics_platform", ANALYTICS_PROFILE,
                       _resource_of(record), _state_for_category(ANALYTICS_PROFILE, record),
                       captured, _identifiers(record), source="customer_analytics_report")
        )
    return [f for f in facts if f]


def _parse_json(evidence: EvidenceFile, text: str):
    try:
        doc = json.loads(text)
    except json.JSONDecodeError:
        return [], []
    if isinstance(doc, list):
        doc = {"records": doc}
    if not isinstance(doc, dict):
        return [], []
    if "service_exports" in doc:
        return _parse_service_export(evidence, doc), []
    if "snapshots" in doc:
        return _parse_snapshot_bundle(evidence, doc)
    if "records" in doc:
        name = evidence.name
        if "export_jobs" in name:
            return _parse_export_jobs(evidence, doc), []
        if "analytics" in name:
            return _parse_analytics(evidence, doc), []
        return _parse_manifest(evidence, doc), []
    return [], []


# --------------------------------------------------------------------------
# SQL
# --------------------------------------------------------------------------
_SNAPSHOT_TABLES = {
    "customer_profiles": (USER_PROFILE, "account_service", PRESENT),
    "customer_search_documents": (SEARCH_INDEX_ENTRY, "search_service", PRESENT),
    "customer_analytics_profiles": (ANALYTICS_PROFILE, "analytics_platform", None),
    "support_records": (SUPPORT_MESSAGE, "support_platform", None),
    "customer_exports": (USER_EXPORT, "export_service", PRESENT),
    "connector_subscriptions": ("DATA_FLOW", "integration_service", None),
    "backup_restore_entries": (BACKUP_ARCHIVE, "backup_service", None),
    "security_audit_records": (SECURITY_AUDIT_LOG, "security_service", PRESENT),
    "search_documents_primary": (SEARCH_INDEX_ENTRY, "search_service", PRESENT),
    "customer_profiles_primary": (USER_PROFILE, "account_service", PRESENT),
    "customer_profiles_failover_replica": (USER_PROFILE, "account_service", PRESENT),
}

_JSON_COLLECTION = {
    "customer_profiles": (USER_PROFILE, "account_service"),
    "customer_search_documents": (SEARCH_INDEX_ENTRY, "search_service"),
    "customer_analytics_reports": (ANALYTICS_PROFILE, "analytics_platform"),
    "support_conversations": (SUPPORT_MESSAGE, "support_platform"),
    "ticket_attachments": (SUPPORT_ATTACHMENT, "support_platform"),
    "customer_export_jobs": (USER_EXPORT, "export_service"),
    "connector_configurations": ("DATA_FLOW", "integration_service"),
    "backup_catalog": (BACKUP_ARCHIVE, "backup_service"),
    "security_audit_events": (SECURITY_AUDIT_LOG, "security_service"),
    "retained_order_records": (LEGAL_HOLD_RECORD, "legal_service"),
    "deleted_customer_references": (ACCOUNT_TOMBSTONE, "identity_service"),
}


def _sql_capture_time(text: str, evidence: EvidenceFile) -> datetime:
    match = re.search(r"Captured at:\s*([0-9T:\-+.Z]+)", text)
    if match:
        return parse_ts(match.group(1))
    return evidence.captured_at


def _row_state(category: str, row: dict) -> str:
    if category == "DATA_FLOW":
        value = row.get("enabled")
        return ACTIVE if value in (1, "1", True, "true") else DISABLED
    if category == BACKUP_ARCHIVE:
        value = row.get("restore_allowed")
        return ACTIVE if value in (1, "1", True, "true") else BLOCKED
    if category == SUPPORT_MESSAGE:
        return IDENTIFIABLE if _has_direct_pii(row) else REDACTED
    if category in (ANALYTICS_PROFILE, PRODUCT_TELEMETRY, ACCOUNT_TOMBSTONE):
        return IDENTIFIABLE if _has_direct_pii(row) else (
            ANONYMIZED if category != ACCOUNT_TOMBSTONE else REDACTED
        )
    return PRESENT


def _row_identifiers(row: dict) -> frozenset[str]:
    out: set[str] = set()
    for key in ("email", "owner_email", "requester_email", "customer_email",
                "subject_selector", "uploaded_by", "customer_reference",
                "subject_reference", "user_id"):
        value = row.get(key)
        if isinstance(value, str) and value.strip() and value.strip().lower() != "null":
            out.add(value.strip())
    for key in ("phone", "requester_phone", "owner_phone"):
        value = row.get(key)
        if isinstance(value, str) and norm_phone(value):
            out.add("p:" + norm_phone(value))
    value = row.get("email_hash")
    if isinstance(value, str) and norm_hash(value):
        out.add(value.strip())
    document = row.get("document")
    if isinstance(document, dict):
        out |= _row_identifiers(document)
    return frozenset(out)


def _parse_sql(evidence: EvidenceFile, text: str) -> list[Fact]:
    facts: list[Fact] = []
    captured = _sql_capture_time(text, evidence)
    connection = sqlite3.connect(":memory:")
    try:
        connection.executescript(text)
        tables = [row[0] for row in connection.execute(
            "select name from sqlite_master where type='table'")]
        for table in tables:
            if table == "snapshot_scope":
                continue
            columns = [info[1] for info in connection.execute(f'PRAGMA table_info("{table}")')]
            try:
                rows = connection.execute(f'SELECT * FROM "{table}"').fetchall()
            except sqlite3.Error:
                continue
            for raw in rows:
                row = dict(zip(columns, raw))
                if evidence.name == "support_replica.log":
                    pass
                if "record_json" in row and row.get("record_json"):
                    try:
                        payload = json.loads(row["record_json"])
                    except (TypeError, json.JSONDecodeError):
                        continue
                    collection = str(row.get("collection_name") or "")
                    system = str(row.get("origin_system") or "")
                    category, default_system = _JSON_COLLECTION.get(collection, ("", system))
                    if not category:
                        continue
                    state = _row_state(category, payload)
                    if category == LEGAL_HOLD_RECORD:
                        state = PRESENT
                    facts.append(
                        _make_fact(evidence, system or default_system, category,
                                   str(row.get("resource_id") or payload.get("resource_id") or ""),
                                   state, captured, _row_identifiers(payload),
                                   user_ref=str(payload.get("subject_reference") or payload.get("customer_reference") or payload.get("user_id") or ""),
                                   source=f"{table}:{collection}",
                                   detail={"message_text": payload.get("message_text")
                                           or payload.get("message_excerpt") or ""})
                    )
                    continue
                if table not in _SNAPSHOT_TABLES:
                    continue
                category, system, fixed_state = _SNAPSHOT_TABLES[table]
                state = fixed_state or _row_state(category, row)
                if category == SUPPORT_MESSAGE:
                    # A support conversation is retained but only the
                    # requester's direct identifiers determine exposure.
                    state = IDENTIFIABLE if _has_direct_pii(row) else REDACTED
                facts.append(
                    _make_fact(evidence, system, category, str(row.get("resource_id") or ""),
                               state, captured, _row_identifiers(row),
                               user_ref=str(row.get("customer_reference") or row.get("subject_reference") or ""),
                               source=table,
                               detail={"message_text": row.get("message_text")
                                       or row.get("message_excerpt") or ""})
                )
    finally:
        connection.close()
    return [f for f in facts if f]


# --------------------------------------------------------------------------
# logs
# --------------------------------------------------------------------------
_TS_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)")
_PAIRS_RE = re.compile(r'([a-zA-Z_]+)=("([^"]*)"|\'([^\']*)\'|(\S+))')


def _line_pairs(line: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for match in _PAIRS_RE.finditer(line):
        value = match.group(3)
        if value is None:
            value = match.group(4)
        if value is None:
            value = match.group(5)
        out.setdefault(match.group(1), value)
    return out


def _line_service(line: str, pairs: dict[str, str]) -> str:
    if pairs.get("service"):
        return pairs["service"]
    if pairs.get("function"):
        return pairs["function"]
    bracket = re.match(r"^\S+\s+\[[A-Z]+\]\s+\[([a-z_]+)\]", line)
    if bracket:
        return bracket.group(1)
    pipe = line.split("|")
    if len(pipe) > 2 and re.match(r"^\s*[a-z_]+\s*$", pipe[2]):
        return pipe[2].strip()
    match = re.search(r"<\d+>\d+ \S+ ([a-z_]+) ", line)
    if match:
        return match.group(1)
    return ""


def _line_event(line: str, pairs: dict[str, str]) -> str:
    if pairs.get("event"):
        return pairs["event"]
    colon = re.search(r"\[[a-z_0-9-]+\]\s+([a-z_]+):", line)
    if colon:
        return colon.group(1)
    pipe = line.split("|")
    if len(pipe) > 4 and re.match(r"^\s*[a-z_]+\s*$", pipe[4]):
        return pipe[4].strip()
    return ""


def _bool(value: str) -> bool | None:
    lowered = (value or "").strip().lower()
    if lowered in {"true", "1", "yes"}:
        return True
    if lowered in {"false", "0", "no"}:
        return False
    return None


def _parse_logs(evidence: EvidenceFile, text: str) -> list[Fact]:
    facts: list[Fact] = []
    pending: dict[str, dict] = {}
    for lineno, line in enumerate(text.splitlines(), 1):
        stamp = _TS_RE.match(line.strip())
        if not stamp:
            continue
        observed = parse_ts(stamp.group(1))
        pairs = _line_pairs(line)
        pairs["__lineno"] = str(lineno)
        brace = line.find("{")
        if brace != -1:
            try:
                payload = json.loads(line[brace:])
                if isinstance(payload, dict) and payload.get("event"):
                    pairs = {k: ("" if v is None else str(v)) for k, v in payload.items()}
                    pairs["__lineno"] = str(lineno)
            except json.JSONDecodeError:
                pass
        message = re.search(r'message="(.*)"', line)
        if message and "\\" in message.group(1):
            inner = re.sub(r'\\+"', '"', message.group(1))
            pairs.update(_line_pairs(inner))
        service = _line_service(line, pairs)
        event = _line_event(line, pairs)
        trace = pairs.get("trace_id") or (re.search(r"\btr-[\w-]+\b", line).group(0)
                                         if re.search(r"\btr-[\w-]+\b", line) else "")
        if not service or not event:
            continue
        if trace:
            pending.setdefault(trace, {}).update(
                {k: v for k, v in pairs.items()
                 if k in {"lookup_key", "match_key", "scan_key", "subject_key",
                          "correlation_key", "subject_ref"}}
            )
        context = dict(pending.get(trace, {}))
        context.update({k: v for k, v in pairs.items()
                        if k in {"lookup_key", "match_key", "scan_key", "subject_key",
                                 "correlation_key", "subject_ref"}})

        def emit(system, category, resource, state, ref="", ids=None, source=""):
            identifiers = frozenset(ids or []) | frozenset(
                v for k, v in context.items()
                if k in {"lookup_key", "match_key", "scan_key", "subject_key",
                         "correlation_key", "subject_ref"}
            )
            fact = _make_fact(evidence, system, category, resource, state, observed,
                              identifiers, user_ref=ref, source=source or event, detail=pairs)
            if fact:
                facts.append(fact)

        if event == "profile_lookup_completed":
            rows = pairs.get("rows", "")
            status = pairs.get("http_status", "")
            state = ABSENT if (rows in {"0", ""} or status in {"404", "410"}) else PRESENT
            if rows == "0":
                state = ABSENT
            emit("account_service", USER_PROFILE, pairs.get("resource_id", ""), state)
        elif event in {"index_query_completed", "record_lookup"}:
            result = (pairs.get("result") or "").lower()
            if event == "record_lookup":
                category = _infer_category(pairs.get("system", ""), pairs.get("record_type", ""), {})
                state = ABSENT if result == "not_found" else (
                    PRESENT if result == "found" else (result.upper() or PRESENT))
                emit(pairs.get("system", ""), category, pairs.get("resource_id", ""), state,
                     ref=pairs.get("subject_reference", ""),
                     ids=[pairs.get("subject_reference", "")])
            elif result in {"hit", "found"}:
                emit("search_service", SEARCH_INDEX_ENTRY, pairs.get("resource_id", ""), PRESENT)
            elif result in {"miss", "not_found", "no_hit"} or pairs.get("total_hits") == "0":
                emit("search_service", SEARCH_INDEX_ENTRY, pairs.get("resource_id", ""), ABSENT)
        elif event == "contact_lookup_completed":
            state = PRESENT if pairs.get("rows", "0") not in {"0", ""} else ABSENT
            emit("analytics_platform", SECONDARY_IDENTIFIER, pairs.get("resource_id", ""), state)
        elif event == "analytics_identity_scan":
            count = pairs.get("direct_identifiers")
            state = IDENTIFIABLE if count not in {"0", "none", ""} else ANONYMIZED
            emit("analytics_platform", ANALYTICS_PROFILE, pairs.get("resource_id", ""), state)
        elif event in {"analytics_profile_read", "analytics_profile_read_completed"}:
            count = pairs.get("direct_identifiers")
            state = ANONYMIZED if count in {"0", "none", ""} else IDENTIFIABLE
            if pairs.get("email") and pairs["email"] not in {"null", "none"}:
                state = IDENTIFIABLE
            emit("analytics_platform", ANALYTICS_PROFILE, pairs.get("resource_id", ""), state)
        elif event in {"support_ticket_read_completed", "message_read"}:
            has = any(pairs.get(k) not in (None, "", "null", "none")
                      for k in ("requester_email", "requester_name", "requester_phone"))
            emit("support_platform", SUPPORT_MESSAGE, pairs.get("resource_id", ""),
                 IDENTIFIABLE if has else REDACTED)
        elif event in {"message_pii_scan", "attachment_pii_scan"}:
            category = SUPPORT_MESSAGE if event == "message_pii_scan" else SUPPORT_ATTACHMENT
            emit("support_platform", category, pairs.get("resource_id", ""), IDENTIFIABLE)
        elif event in {"connector_config_read_completed", "connector_heartbeat"}:
            enabled = _bool(pairs.get("enabled", ""))
            emit("integration_service", "DATA_FLOW", pairs.get("resource_id", ""),
                 ACTIVE if enabled else DISABLED)
        elif event == "restore_candidate_evaluated":
            blocked = _bool(pairs.get("deletion_block", "false"))
            emit("backup_service", BACKUP_ARCHIVE, pairs.get("resource_id", ""),
                 BLOCKED if blocked else ACTIVE)
        elif event == "restore_policy_read_completed":
            allowed = _bool(pairs.get("restore_allowed", ""))
            emit("backup_service", BACKUP_ARCHIVE, pairs.get("resource_id", ""),
                 ACTIVE if allowed else BLOCKED)
        elif event == "audit_record_read_completed":
            emit("security_service", SECURITY_AUDIT_LOG, pairs.get("resource_id", ""),
                 PRESENT, ref=pairs.get("correlation_key", ""))
        elif event in {"export_completed", "export_download_check_completed",
                       "export_metadata_read_completed"}:
            available = _bool(pairs.get("download_available", "true"))
            emit("export_service", USER_EXPORT, pairs.get("resource_id", ""),
                 PRESENT if available is not False else ABSENT)
        elif event == "contact_query_completed":
            rows = pairs.get("rows", "0")
            category = (SUPPORT_ATTACHMENT if evidence.name == "support_replica.log"
                        else SUPPORT_MESSAGE)
            emit("support_platform", category, pairs.get("resource_id", ""),
                 PRESENT if rows not in {"0", ""} else ABSENT)
        elif event == "deletion_marker_check":
            # A marker check describes the deletion workflow, not the record's
            # presence; the contact query already established that.
            pass
        elif event == "attachment_scan_started":
            pass
    return facts


# --------------------------------------------------------------------------
# text / digest
# --------------------------------------------------------------------------
def _parse_handover(evidence: EvidenceFile, text: str) -> list[Fact]:
    facts = []
    for lineno, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line.startswith("- "):
            continue
        parts = [p.strip() for p in line[2:].split("|")]
        if len(parts) < 5:
            continue
        observed = parse_ts(parts[0])
        system, resource, record_type, state_text = parts[1], parts[2], parts[3], parts[4]
        category = _infer_category(system, record_type, {})
        state = state_text.upper()
        if state in {"FOUND"}:
            state = PRESENT
        elif state in {"NOT_FOUND"}:
            state = ABSENT
        elif state in {"IDENTIFIABLE"}:
            state = IDENTIFIABLE
        identifier = parts[5] if len(parts) > 5 else ""
        ids = frozenset({identifier}) if identifier and identifier != "no direct identifier" else frozenset()
        facts.append(_make_fact(evidence, system, category, resource, state, observed, ids,
                                source="handover", detail={"__lineno": str(lineno)}))
    return [f for f in facts if f]


def _parse_digest(evidence: EvidenceFile, digest: dict) -> list[Fact]:
    """Facts extracted offline from PDFs / screenshots.

    The digest stores only what the artefact says (resource, identifiers,
    state, timestamp); the runtime never depends on OCR being installed.
    """
    facts = []
    for row in digest.get(evidence.file_id, []):
        facts.append(
            _make_fact(
                evidence,
                row["system"],
                _infer_category(row["system"], row.get("record_type", ""), {}),
                row["resource_id"],
                row["state"],
                parse_ts(row.get("observed_at") or evidence.captured_at.isoformat()),
                frozenset(row.get("identifiers") or []),
                user_ref=row.get("user_ref", ""),
                source="document_digest",
            )
        )
    return [f for f in facts if f]
