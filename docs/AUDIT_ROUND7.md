# Audit round 7 — final pass: full flip dump, parser exposure, expiry

Builder: Hermes Agent (deepseek-v4.1-flash). No freeze time named; no code
behaviour changed.

## 1. Flip dump v2

File: `analysis/flip_dump_v2.md` — 57 entries, 1,243 lines. Each entry now has:
case, status, `requested_at`, `audit_at`, subject identifiers (all forms), the
identifier that tied the row (kind, exact/loose), deciding `observed_at`, the
whole record (SQL: CREATE TABLE + column dict; JSON: full dict; log: full line;
PNG: digest entry + OCR text), and the rule under test.

Screenshot-only flips are now auditable:
- `case_53 support_1034` — tied by `kagyeman8947@fastmail.com` (email, exact),
  fact observed 2026-05-24, audit 2026-05-25; OCR shows the support console
  with "Kofi Agyeman … kagyeman8947@fastmail.com".
- `case_50 analytics_7438` — tied by `darwish.omar@icloud.com`, OCR shows
  "user_20 - analytics_7438 - darwish.omar@icloud.com".
- `case_39 data_flow_1121` — tied by `user_14`, OCR shows the connector console
  row `data_flow_1121`.
These three rest on the digest. **Retracted:** the claim that OCR is legible
for the decisive tokens was wrong for case_39 (no user_14 in OCR). Vision
re-check in `docs/AUDIT_ROUND8.md` confirms data_flow_1121 / jain.aditi
(user_14) / Continuous in the image; OCR fidelity, not the fact, was at fault.

Cropping is fixed: full records are printed. The earlier JSON/SQL cut-offs
(e.g. case_224, case_147, case_279, case_531, case_160, case_460, case_459) are
gone; the decisive `enabled` / `restore_allowed` fields are visible in v2.

## 2. Parser-path exposure

Command: `python3 analysis/parser_exposure.py`
Denominator: every finding in the 32 sample and 518 eval cases, keyed by
`file-family:source` (log event name, SQL table[:collection], JSON collection,
or `document_digest`).

Sample-exercised paths (sample cases / agreements):
- `log:restore_candidate_evaluated` 2 / 2 — the `eligible/deletion_block`
  inference is sample-validated (case_09/17).
- `log:message_pii_scan` 1 / 1 — `matched_value` as PII is sample-validated.
- `txt:handover` 7 / 7; `log:index_query_completed` 3 / 3;
  `json:support_conversations` 2 / 2; `json:connector_configurations` 2 / 2.

Zero-sample paths that decide eval statuses (eval status-dependent cases):

| Path | Eval cases whose status rests on it |
|---|---:|
| `json:operational_record_history` | 46 |
| `json:manifest` | 38 |
| `log:record_lookup` | 36 |
| `sql:customer_search_documents` | 9 |
| `png:document_digest` | 9 |
| `json:index_queries` | 8 |
| `sql:customer_data_primary:backup_catalog` | 6 |
| `sql:customer_data_failover_replica:deleted_customer_references` | 4 |
| `json:backup_catalog` | 4 |
| `sql:customer_data_primary:support_conversations` | 3 |
| `sql:customer_analytics_profiles` | 3 |
| `log:export_download_check_completed` | 3 |
| `sql:backup_restore_entries` | 3 |
| 9 further paths | 1–2 each |

**191 of 518 eval cases (36.9%) have a status decided solely by a parser path
with zero sample exposure.**

Specific items requested:
- `restore_candidate_evaluated eligible/deletion_block` — sample 2/2, keep.
- `message_pii_scan matched_value` — sample 1/1, keep.
- `BACKUP_ARCHIVE result=ACTIVE` in `json:manifest` — **0 sample cases**. The
  engine reads `result=ACTIVE` as restore risk; alternative reading is that a
  manifest row is a catalog claim, not a live restore policy. No sample or
  policy line decides it; left unchanged.
- SQL columns: `backup_restore_entries(resource_id, customer_reference,
  customer_email, archive_key, restore_allowed INTEGER, updated_at)` and
  `connector_subscriptions(resource_id, customer_reference, customer_email,
  connector_name, enabled INTEGER, last_delivery_status, updated_at)`. The
  engine reads **named columns**, not positions; the fifth column is
  `restore_allowed`/`enabled` as expected. `sql:backup_restore_entries` has 3
  eval status dependencies, 0 sample.
- `operational_record_history`: rows are
  `{recorded_at, system, resource_id, record_type, result: FOUND|NOT_FOUND,
  lookup_value}`. The engine treats `FOUND` as current PRESENT. Alternative:
  it is a treatment-history log, so `FOUND` may be historical. 46 statuses
  depend on this, 0 sample cases. No change without evidence.
- `record_lookup`: same shape (`result`, `subject_reference`), 36 status
  dependencies, 0 sample.
- `DELETION_PENDING`: 8 SQL rows; the engine treats the profile row as
  physically PRESENT (conservative). Sample/eval split not enumerated.
- PNG digests: 9 findings / 9 status dependencies, 0 sample (the sample's
  digest steps are PDF-sourced, not PNG). `case_53/50/39` rest on OCR.

Alternative readings and evidence: for each zero-sample path the engine's
choice is the conservative one (a row that exists is a finding). The exception
is `operational_record_history`/`record_lookup`, where "FOUND" might be a
historical claim; that is the largest single unvalidated inference (82 statuses
combined).

## 3. Expiry enumeration

- `expires_at < audit_at` on eval export rows: **0**. Live: 1 (`case_08`).
- `retention_until < audit_at`: **0** (all 30 retention rows are 2026+ and
  audits are 2026). There is no eval case on the unexercised side.

## 4. Hygiene

Scratch-text grep (sigma glyph, draft phrases, 716 marker, TODO/FIXME) over README, `docs/`,
`analysis/`, `log.txt` — see command output; hits removed if any. README,
DECISIONS and OPEN_PROBLEMS agree on: field 75.8% positional / 83.0%
content-only, recall estimate 0.889, 33 events kept, 27 omitted slots.

## 5. Freeze

No freeze time named by Lakshaya ("leave the worrying part to me"), so no code
was frozen. Sample unchanged: 32/32, 166/193, 0 extra; full run 153/355/10;
validator 0 errors.
