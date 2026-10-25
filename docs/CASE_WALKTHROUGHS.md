# Case walkthroughs

Two cases end to end: one COMPLETE with verification, one INCOMPLETE with two
findings. Raw records are quoted; no hidden labels.

## case_01 — COMPLETE, one verification

Subject: `amina.elmasri@gmail.com`, requested 2026-08-18, audit
2026-09-03T11:30:00Z.

Evidence: `evidence_54`, `dataset/evidence/databases/customer_accounts_failover_replica_20260902.sql`,
captured 2026-09-02T23:00:00Z (inside the request/audit window).

The failover-replica snapshot creates `customer_profiles_failover_replica` and
`customer_profiles_primary`. Neither table contains `account_001`; the visible
rows are `account_005`, `account_8741`, `account_9116`, `account_7204`. The
subject is resolved from the current snapshot and historical audit log, and the
account resource is absent from both stores.

Policy: `USER_PROFILE` → DELETE; current state `ABSENT` is the required state.

Emitted step:

```json
{"step_no":1,"phase":"VERIFICATION","system_id":"account_service",
 "resource_id":"account_001","operation":"VERIFY_RECORD_ABSENT",
 "state":"ABSENT","evidence_id":"evidence_54"}
```

Why it is COMPLETE: the only required account resource is absent in the
evidence at the audit cutoff. The verification cites the file that proves it.

## case_36 — INCOMPLETE, two findings

Subject: `aadebayo3975@fastmail.com`, requested 2026-09-07, audit
2026-10-01T12:00:00Z.

Evidence: `evidence_03`, `dataset/evidence/records/customer_account_handover_20261001.txt`,
captured 2026-10-01T12:00:00Z. Raw lines:

```text
- 2026-10-01T12:00:00Z | account_service | account_5823 | USER_PROFILE | NOT_FOUND | aadebayo3975@fastmail.com
- 2026-10-01T12:00:00Z | export_service  | export_7689  | USER_EXPORT   | FOUND     | aadebayo3975@fastmail.com
- 2026-10-01T12:00:00Z | search_service  | search_5575  | SEARCH_INDEX_ENTRY | FOUND | aadebayo3975@fastmail.com
- 2026-10-01T12:00:00Z | security_service | audit_record_2966 | SECURITY_AUDIT_LOG | FOUND | user_34
```

Policy: `USER_EXPORT` and `SEARCH_INDEX_ENTRY` → DELETE; `SECURITY_AUDIT_LOG` →
RETAIN. The account is already absent; the export and search entry remain.

Emitted steps, in canonical order:

1. FINDING `REPORT_REMAINING_RECORD` export_7689, evidence_03
2. FINDING `REPORT_REMAINING_RECORD` search_5575, evidence_03
3. REMEDIATION `DELETE_RECORD` export_7689, evidence empty
4. REMEDIATION `DELETE_RECORD` search_5575, evidence empty
5. VERIFICATION `VERIFY_RECORD_ABSENT` account_5823, evidence empty
6. VERIFICATION `VERIFY_RECORD_ABSENT` export_7689, evidence empty
7. VERIFICATION `VERIFY_RECORD_ABSENT` search_5575, evidence empty
8. VERIFICATION `VERIFY_RECORD_PRESENT` audit_record_2966, evidence empty

Why it is INCOMPLETE: two positive findings remain at the audit cutoff. The
retained audit record is a verification, not a finding. The account absence is
carried as a verification because the handover says `NOT_FOUND`.

Why the order: both findings first, then both remediations, then verifications.
All future steps use an empty `evidence_id`; only findings cite `evidence_03`.
