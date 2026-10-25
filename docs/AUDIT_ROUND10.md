# Round 10 — recoveries from the sync report

## 1. Unverified linked-account claim (case_06)

Premise correction: `evidence_id=""` in gold for case_06 is **because the case is
INCOMPLETE** (future steps carry no evidence), not a marker for an unverified
claim. But the step is real: `account_006` is linked by
`search_documents_primary.source_resource_id` (search_001, jonas.berg email),
has a `DELETE_RECORD` claim in system_activity (activity_3545, 2026-08-30), and
no readback fact. Gold emits `VERIFY_RECORD_ABSENT account_006` as step 3.

Rule implemented (`planner.add_linked_verifications`): in an INCOMPLETE case,
for a subject-owned search document with `source_resource_id=account_N`, if
`account_N` has a DELETE_RECORD claim inside [requested_at, audit_at] and no
fact, append `VERIFY_RECORD_ABSENT account_service account_N ABSENT ""`.

Test: triple exists **1 sample case (case_06)** and **0 eval cases**.
- sample: 166→**167/193** steps, exact sequence 11→**12/32**, fields
  1024→**1033/1351**, 0 extra, statuses 32/32.
- eval: **0 cases changed**; full run 152/356/10 unchanged; validator 0.

## 2. evidence_04 / support_9538

Policy: SUPPORT_MESSAGE → REDACT (rule_05); SUPPORT_ATTACHMENT → DELETE
(rule_06). support_9538 appears in system_activity as `DELETE_RECORD …
FAILED` (2026-08-28) and in `service_events_ap_south_20260915.log` as
`attachment_pii_scan matched_value="+81 90 6156 0005"` — **not** Haruka's phone
(+81 90 7610 2507). The image shows it as Haruka's support ticket, the log
shows a different phone. Adding it would add a contested support step to
case_34 (already INCOMPLETE). **Not added.**

## 3. The three undigested PDFs

- evidence_18: user_18 (cases 33 and 52), statement `NST-2026-0718-1842`
  (= export_1842), order ORD-20261260. Adding it would add an export_1842
  finding + remediation + verification to case_33/52 (statuses already
  INCOMPLETE). No sample case covers user_18, so unvalidated. **Not added.**
- evidence_27: legal holds for user_08/12/17/21/24/29. Only eval user is user_17
  (case_46); the other five have no eval case. Sample canonicals for those users
  contain **no legal-hold steps**, so the register is decoy/out of scope.
  **Not added.**
- evidence_55: audit_record_003/user_03 (case_45), duplicate of the fact already
  read from evidence_37. Adding changes nothing (same resource, dedupe).
  **Not added.**

## 4. Export expiry

All export records: `export_001` (case_08) expires 2026-10-04, audit 09-14 →
live; `export_843` has `download_available=false` and is already ABSENT;
`export_1260` (case_33/52) expires **2026-06-25**, before audit 2026-07-19, but
is modelled PRESENT from the console. No sample case has an expired export, so
the expired side is unvalidated. Changing it would flip case_33/52
(INCOMPLETE→COMPLETE), so no change without evidence.

## 5. evidence_54 / evidence_92

- evidence_54 (failover replica): contains `account_005`, **not account_001**;
  gold cites it for account_001 anyway. The id is not in the file.
- evidence_92: `account_6440` and `analytics_5335` appear as bare resource rows
  with null identifiers; no same-line subject tie.
No deterministic link exists for these 10 slots. Correctly omitted.
