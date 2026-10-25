# ARCHITECT SYNC REPORT — Ghost Data deletion-audit agent

Builder: Hermes Agent (deepseek-v4.1-flash). Repo: https://github.com/LangerSword/hackerrank-orchestrate-october26

## 1. Repo and pipeline map

| dataset file | rows | columns |
|---|---:|---|
| `deletion_requests.csv` | 518 | case_id,email,requested_at,reported_status,reported_at,audit_at,request_text |
| `deletion_rules.csv` | 15 | rule_id,data_category,condition,required_action |
| `evidence_files.csv` | 94 | file_id,file_path,origin,captured_at |
| `output.csv` | 0 |  |
| `sample_deletion_requests.csv` | 32 | case_id,email,requested_at,reported_status,reported_at,audit_at,request_text |
| `sample_output.csv` | 32 | case_id,deletion_status,steps_json |
| `system_activity.csv` | 4011 | activity_id,event_time,event_type,source_system,target_system,resource_id,reported_result,details |
| `user_audit_log.csv` | 306 | audit_id,user_id,event_time,field_name,old_value,new_value |
| `user_identities.csv` | 850 | user_id,name,email,phone,email_hash,updated_at |
| `dataset/evidence/` | 94 files | json 28, sql 24, log 26, png 11, pdf 4, txt 1 |

Flow: `tables.py` identity graph (current + historical emails/phones/hashes) → `evidence.py` parsers (JSON/SQL/log/handover/digest) → `index.py` ownership (identifier, user_id, earlier snapshot, catalog link) → `state.py` latest observation ≤ audit_at, replica presence, empty snapshots → `policy.py` rules CSV → `planner.py` findings/remediation/verification, canonical order, evidence citation → `validate.py` contract gate. No model calls in the verdict path.

PDFs without digest entries: `evidence_18`, `evidence_27`, `evidence_55` are **ignored** — `EvidenceIndex._extract` returns no facts for PDFs absent from the content-hashed digest. evidence_18 contains export_1842/user_18; evidence_27 legal holds for user_08/12/17/21/24/29; evidence_55 duplicates audit_record_003/user_03. None contains user_09 or account/analytics ids.

## 2. Content-only field accuracy (166 matched steps)

**There are zero content-field mismatches.** Every matched step agrees on phase, system_id, resource_id, operation, state and evidence_id (166/166 each). The 83.0% (1122/1351) is not content error: it is 189 fields from the 27 missing steps plus 40 step_no shifts. Matched-step content excluding step_no is **996/996 (100%)**. Positional including step_no is 1024/1351 (75.8%).

| field | match | mismatch |
|---|---:|---:|
| phase | 166 | 0 |
| system_id | 166 | 0 |
| resource_id | 166 | 0 |
| operation | 166 | 0 |
| state | 166 | 0 |
| evidence_id | 166 | 0 |
| step_no | 126 | 40 |

Table of content mismatches: **empty** (0 rows).

## 3. The 27 missing sample steps

All are VERIFICATION steps. `raw evidence` counts files under `dataset/evidence` containing the id; `activity` counts system_activity rows.

| case | step | phase | operation | system | gold resource | gold evidence | why missing | raw evidence | activity |
|---|---:|---|---|---|---|---|---|---:|---:|
| case_01 | 1 | VERIFICATION | VERIFY_RECORD_ABSENT | account_service | `account_001` | evidence_54 | activity only, no identifier | 0 | 1 |
| case_02 | 1 | VERIFICATION | VERIFY_RECORD_ABSENT | account_service | `account_002` | evidence_54 | activity only, no identifier | 0 | 1 |
| case_03 | 3 | VERIFICATION | VERIFY_RECORD_ANONYMIZED | analytics_platform | `analytics_9406` | evidence_94 | evidence + activity, no subject tie | 1 | 1 |
| case_04 | 1 | VERIFICATION | VERIFY_RECORD_ABSENT | account_service | `account_004` | evidence_54 | id absent from all participant files | 0 | 0 |
| case_04 | 2 | VERIFICATION | VERIFY_RECORD_ANONYMIZED | analytics_platform | `analytics_901` | evidence_56 | evidence + activity, no subject tie | 1 | 1 |
| case_06 | 3 | VERIFICATION | VERIFY_RECORD_ABSENT | account_service | `account_006` | - | same-line subject tie (recoverable) | 1 | 1 |
| case_07 | 3 | VERIFICATION | VERIFY_RECORD_ABSENT | account_service | `account_007` | - | activity only, no identifier | 0 | 1 |
| case_08 | 3 | VERIFICATION | VERIFY_RECORD_ABSENT | account_service | `account_008` | - | activity only, no identifier | 0 | 1 |
| case_10 | 3 | VERIFICATION | VERIFY_RECORD_ABSENT | account_service | `account_010` | - | activity only, no identifier | 0 | 1 |
| case_18 | 9 | VERIFICATION | VERIFY_RECORD_ABSENT | account_service | `account_5521` | - | activity only, no identifier | 0 | 1 |
| case_18 | 11 | VERIFICATION | VERIFY_RECORD_PRESENT | security_service | `audit_record_6645` | - | id absent from all participant files | 0 | 0 |
| case_20 | 5 | VERIFICATION | VERIFY_RECORD_ABSENT | account_service | `account_5037` | - | activity only, no identifier | 0 | 1 |
| case_20 | 7 | VERIFICATION | VERIFY_RECORD_PRESENT | security_service | `audit_record_5569` | - | id absent from all participant files | 0 | 0 |
| case_21 | 1 | VERIFICATION | VERIFY_RECORD_ABSENT | account_service | `account_6440` | evidence_92 | evidence + activity, no subject tie | 1 | 1 |
| case_21 | 3 | VERIFICATION | VERIFY_RECORD_ANONYMIZED | analytics_platform | `analytics_5335` | evidence_92 | evidence + activity, no subject tie | 2 | 1 |
| case_22 | 5 | VERIFICATION | VERIFY_RECORD_ABSENT | account_service | `account_4990` | - | activity only, no identifier | 0 | 1 |
| case_23 | 5 | VERIFICATION | VERIFY_RECORD_ABSENT | account_service | `account_410` | - | activity only, no identifier | 0 | 1 |
| case_25 | 1 | VERIFICATION | VERIFY_RECORD_ABSENT | account_service | `account_3136` | evidence_92 | evidence + activity, no subject tie | 1 | 1 |
| case_25 | 3 | VERIFICATION | VERIFY_RECORD_ANONYMIZED | analytics_platform | `analytics_1895` | evidence_92 | evidence + activity, no subject tie | 2 | 1 |
| case_26 | 4 | VERIFICATION | VERIFY_RECORD_ANONYMIZED | analytics_platform | `analytics_4566` | evidence_92 | evidence + activity, no subject tie | 2 | 1 |
| case_27 | 4 | VERIFICATION | VERIFY_RECORD_ANONYMIZED | analytics_platform | `analytics_4574` | evidence_92 | evidence + activity, no subject tie | 2 | 1 |
| case_28 | 1 | VERIFICATION | VERIFY_RECORD_ABSENT | account_service | `account_5482` | evidence_92 | evidence + activity, no subject tie | 1 | 1 |
| case_28 | 4 | VERIFICATION | VERIFY_RECORD_ANONYMIZED | analytics_platform | `analytics_6077` | evidence_92 | evidence + activity, no subject tie | 2 | 1 |
| case_29 | 9 | VERIFICATION | VERIFY_RECORD_ABSENT | account_service | `account_7012` | - | activity only, no identifier | 0 | 1 |
| case_30 | 9 | VERIFICATION | VERIFY_RECORD_ABSENT | account_service | `account_4163` | - | activity only, no identifier | 0 | 1 |
| case_31 | 1 | VERIFICATION | VERIFY_RECORD_ABSENT | account_service | `account_4857` | evidence_51 | activity only, no identifier | 0 | 1 |
| case_32 | 3 | VERIFICATION | VERIFY_RECORD_ABSENT | account_service | `account_8858` | - | activity only, no identifier | 0 | 1 |

Total: 27 — 18 account `VERIFY_RECORD_ABSENT`, 7 `VERIFY_RECORD_ANONYMIZED`, 2 `VERIFY_RECORD_PRESENT`.
Only **1 of 27** is same-record recoverable: `case_06 account_006` appears in `search_documents_primary` next to `search_001` and `jonas.berg@outlook.com` (`source_resource_id`). The other 26 carry no same-line subject tie; the 2 audit ids appear nowhere. Naming is opaque (`account_5521`, `analytics_4566`), not derivable from user/email.

## 4. Remaining PNG vision results

- `evidence_23` (case_33/52): `export_1260`, owner `ingrid.dahl@outlook.com`, status `Ready`, created 18 Jun 06:42, expires **25 Jun 2026**. `export_1842` not shown. Digest matches; the export expires before case_33 audit (19 Jul) and expiry is not modelled.

- `evidence_04` (case_34): `user_11 · account_5762`, Haruka Sato, `haruka.s1838@zoho.com`, `+81 90 7610 2507`, full profile. Digest matches. Image also shows `Support: CS-8538 · support_9538`, which the digest omits (possible missing support step; status already INCOMPLETE).

- `evidence_42` (tombstone_17/user_17): image shows a **Retained reference** for `user_17`, customer key, **no name/email/phone**. `tombstone_17` is not shown; activity_4011 supplies the id. `REDACTED` is supported.

## 5. Current output after Option A

`evidence_32` state corrected BLOCKED → ACTIVE. case_55 now INCOMPLETE with `REPORT_RESTORE_RISK` + `BLOCK_RESTORE` + `VERIFY_RESTORE_BLOCKED`. Full run: **152 COMPLETE / 356 INCOMPLETE / 10 NOT_APPLICABLE**, validator 0 errors. Sample unchanged: 32/32 statuses, 166/193 steps, 0 extra.

