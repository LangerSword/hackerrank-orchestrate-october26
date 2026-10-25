# Round 9B — forensic check

No code change. Output unchanged.

## 1. Blocker A — case_63

`activity_4008` (raw):
`2026-09-16T07:27:01Z, LINK_RESOURCE_IDENTITY, data_catalog -> marketing_platform,
marketing_001, SUCCESS, "Data catalog linked marketing_001 (marketing_001) to
kwame-mensah@proton.me and user_09."`

case_63: email kwame-mensah@proton.me; requested 2026-09-14T04:20Z; reported
2026-09-15T22:20Z; audit 2026-09-17T09:20Z. evidence_60 captured
2026-09-16T07:20:00Z — the link is **7 minutes after** the image.

Token search over every file (SQL, logs, JSON, CSV, PDFs): only 6 hits —
activity_4008, the request row, and the identity row. No SQL, log, JSON or PDF
mentions `user_09`, `kwame-mensah@proton.me`, `marketing_001` or
`sj.park@naver.com`. user_09 has **exactly one fact** (marketing_001, from the
digest, observed 07:20). Removing it leaves zero facts, hence COMPLETE `[]`;
no filter dropped a verification — there is nothing to verify.

Citation contract: problem_statement says findings and COMPLETE verifications
"must cite a `file_id`, `activity_id`, or `audit_id`". So `activity_4008` is
contract-legal. But all 32 sample canonical citations use `evidence_*` only,
and `code/audit/validate.py` builds its allowed set from `evidence_files.csv`,
so citing an activity id **fails the current validator**. Using it needs a
validator change and departs from sample precedent.

## 2. Blocker B — case_55

`rule_14, BACKUP_ARCHIVE, "Restore access can be blocked", RETAIN`.
Code: `planner._finding` emits `REPORT_RESTORE_RISK` only when state is
`ACTIVE`; `BLOCKED` yields no finding; the required final state is `BLOCKED`.

Correcting evidence_32 to `ACTIVE` changes **only case_55**:
- current: COMPLETE, 1 step `VERIFY_RESTORE_BLOCKED backup_9287 evidence_32`
- ACTIVE: INCOMPLETE, 3 steps
  `REPORT_RESTORE_RISK backup_9287 evidence_32`,
  `BLOCK_RESTORE backup_9287 ""`,
  `VERIFY_RESTORE_BLOCKED backup_9287 ""`
Contract invariants hold (finding cites evidence, future steps empty, ordering
correct). Vision: the console shows no restore policy/control for backup_9287,
but `Restore success 99.6%` and sibling restores `backup_9286`, `backup_9281`
completed the day before. `BLOCKED` is an unsupported inference; `ACTIVE` is
the conservative reading.

## 3. Vision on the remaining PNGs

- `evidence_23` (case_33/52): image confirms `export_1260` owner
  `ingrid.dahl@outlook.com`, status `Ready`, created 18 Jun 06:42, expires
  **25 Jun 2026**. export_1842 is not shown. Digest matches. Note: the export
  expires before case_33's audit (19 Jul); expiry is not modelled.
- `evidence_04` (case_34): image confirms `user_11 · account_5762`, Haruka Sato,
  haruka.s1838@zoho.com, +81 90 7610 2507, full profile. Digest matches.
  Image also shows `Support: CS-8538 · support_9538`; the digest does not
  include support_9538, so a possible support step is missing (status already
  INCOMPLETE).
- `evidence_42` (tombstone_17 / user_17): image shows a **Retained reference**
  for `user_17`, customer key, no name/email/phone. `tombstone_17` itself is
  not shown; activity_4011 supplies the id. The `REDACTED` state is supported.

## 4. The three undigested PDFs

Why: `EvidenceIndex._extract` returns no facts for PDFs whose hash is absent
from the digest; these three have no digest entry, so they are **ignored**.
- evidence_18 (account_history_report): Ingrid Dahl, user_18, statement
  NST-2026-0718-1842 (= export_1842), order ORD-20261260. No account/analytics
  ids. Could support an extra export_1842 finding for case_33/52 (status
  already INCOMPLETE).
- evidence_27 (legal retention register): orders for user_08, 12, 17, 21, 24,
  29, retain-until 2033. Only eval case is user_17 (case_46). The sample's
  canonical for those users contains no legal-hold steps, so the register is
  decoy/out of scope by sample precedent.
- evidence_55 (security_retention_extract): audit_record_003 / user_03, retain
  until 2027. Duplicate of the fact already read from evidence_37.
None contains user_09 or any account/analytics resource id; they do not help
the 279 account or 70 analytics unnameable slots.

## Status
Option A applied: evidence_32 BLOCKED -> ACTIVE; case_55 now INCOMPLETE (3 steps). Two status-affecting decisions remain: case_63 (conflict) and
case_55 (BLOCKED vs ACTIVE). Adding evidence_18/27/55 entries would change
steps, not the current statuses; evidence_27 would add steps contradicted by
sample precedent.
