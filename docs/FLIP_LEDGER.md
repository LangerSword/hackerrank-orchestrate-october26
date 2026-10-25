# Flip ledger

Two changes explain the status movement. One is reverted; one is kept.

## 1. Full-run flip: case_55 (reverted)

| Item | Value |
|---|---|
| Commit that caused it | `343f655` — “Option A: case_55 BLOCKED->ACTIVE” |
| File changed | `code/audit/digests/documents.json`, `evidence_32` |
| Change | `state: "BLOCKED"` → `state: "ACTIVE"` |
| Output effect | case_55 `COMPLETE` → `INCOMPLETE`; full run `153/355/10` → `152/356/10` |

Raw record: `dataset/evidence/images/backup_restore_console_20260429.png` (captured
2026-04-29T09:00:00Z), case_55 audit 2026-04-30T11:00:00Z. The screenshot shows
`backup_9287`, account `areed1433@gmail.com`, region `eu-west-1`, created
26 Apr 2026, size 84768, encryption AES-256, checksum verified, last drill
29 Mar 2026, retention end 26 Jul 2026. It does **not** show a restore status,
a restore control, or `restore_allowed`.

There is no evidence chain for `ACTIVE`. The change was a hand-authored digest
edit, not a parsed observation. The correct action is to revert it, not to
defend it. Reverted in the current commit:

- `evidence_32.state` is `BLOCKED` again.
- case_55 is `COMPLETE` with `VERIFY_RESTORE_BLOCKED` citing `evidence_32`.
- full run is back to `153 COMPLETE / 355 INCOMPLETE / 10 NOT_APPLICABLE`.
- `output.csv` SHA-256 is `93eb70b7f428ddb1487fe379f5329ff964129c85a769483e6094cf29faa9891c`.

Honest limit: `BLOCKED` is a policy default, not a photographed fact. The
screenshot proves the archive exists; it does not prove restore is blocked. If
a later record shows `restore_allowed=true`, reopen case_55.

## 2. Recovered sample step: case_06 (kept)

| Item | Value |
|---|---|
| Commit | `b20101e` — “Round 10: linked-account verification for case_06” |
| Output effect | sample 166 → 167 steps of 193; omitted account slots `18` → `17`; full run unchanged |
| Rule | `planner.add_linked_verifications`: a resource with a known foreign-key owner and an unverified `DELETE_RECORD` claim gets a future `VERIFY_RECORD_ABSENT` step with empty evidence |

Evidence chain:

1. `dataset/evidence/databases/customer_search_primary_20260910.sql`, captured
   2026-09-10T08:45:00Z:
   `INSERT INTO "search_documents_primary" VALUES('search_001','Jonas Berg','jonas.berg@outlook.com','account_006','2026-09-09T22:12:00Z');`
2. `search_001` belongs to `jonas.berg@outlook.com` (`case_06`, requested
   2026-08-29T06:51:00Z, audit 2026-09-10T09:15:00Z).
3. `source_resource_id = account_006` is the foreign key. The account id is
   copied from the row; it is not invented.
4. `dataset/system_activity.csv` line `activity_3545`, 2026-08-30T17:08:20Z:
   `DELETE_RECORD, account_service, account_006, SUCCESS` — a claim, with no
   readback proving absence.
5. The sample canonical output for `case_06` includes
   `VERIFY_RECORD_ABSENT, account_service, account_006, ABSENT, evidence_id=""`.
   The engine now matches that step.

This is the difference between a derived id and a guessed id: the resource id
comes from a same-record foreign key, and the operation is a future
verification, not a finding with a fabricated citation.

## 3. case_55 association test

All activity rows touching `backup_9287`:

- `activity_3387` `RESTORE_BACKUP` 2026-08-22 — after case_55 audit; excluded.
- `activity_3388` `DELETE_RECORD` `search_4882` `FAILED` 2026-08-22 — after audit.
- `activity_4006` `LINK_RESOURCE_IDENTITY` 2026-04-29 — links `backup_9287` to
  `areed1433@gmail.com` and `user_16`.

Crosstab over all sample and eval backup cases:

| Backup state | In-window CHECK_RESTORE_ACCESS or BLOCK_RESTORE | Cases |
|---|---|---:|
| ACTIVE | yes (CHECK_RESTORE_ACCESS) | 28 |
| BLOCKED | yes (BLOCK_RESTORE) | 35 |
| BLOCKED | **no** | **1 (case_55)** |

The association is clean: every ACTIVE backup has a restore-access check, every
BLOCKED backup has a block action, and case_55 is the only backup with neither.
That makes the **absence** of a restore-access activity weak evidence for
BLOCKED.

It is still not proof. The screenshot proves the archive exists and shows no
restore field; it does not prove BLOCKED. Both `BLOCKED` and `ACTIVE` are
inferences. The output keeps the conservative default `BLOCKED`/`COMPLETE` and
does not change case_55 without a record that names `restore_allowed`.
