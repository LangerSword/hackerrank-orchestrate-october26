# Audit round 5 — vocabulary census, mutation counters, shape and recall

Builder: Hermes Agent (deepseek-v4.1-flash). No freeze time named; no code
change after this report except docs.

## PHASE 11 — state-vocabulary census

Command: `python3 analysis/vocab_census.py`
Denominator: 103 dataset files; 72 rows carry a state-like column.

State keys and distinct values (normalised):

| Key | Values | Engine |
|---|---|---|
| `account_status` | ACTIVE 22, DELETION_PENDING 8 | ignored on profile rows (row treated PRESENT) |
| `enabled` | true/false/1/0 | mapped ACTIVE/DISABLED |
| `restore_allowed` | true/false | mapped ACTIVE/BLOCKED |
| `result` | FOUND 158, hit 60, NOT_FOUND 60, IDENTIFIABLE 37, ACTIVE 25, REDACTED 4, DISABLED 4, BLOCKED 4 | mapped |
| `rows` / `http_status` / `status_code` | 0/1, 404/200 | mapped ABSENT/PRESENT |
| `archive_present` | true 15 | **ignored** |
| `last_delivery_status` | delivered 63, stopped 24 | **ignored** (uses `enabled`) |
| `retention_until` | timestamps 98 | **ignored as expiry** (records kept PRESENT) |
| `expires_at` | export timestamps | **ignored** (export treated PRESENT) |
| `archive_key` / `archive_path` | paths | evidence only |

Soft-delete check: of 72 state-bearing rows, **0 are treated ABSENT by the
engine**. `DELETION_PENDING` profiles are treated as physically present, which
is the conservative direction (a ghost flags a finding). No backtrack trigger.

**Not done:** the full SQL state oracle (column-by-column state diff over all
SQL files). Only the soft-delete/absence check above was run.

## PHASE 12 — mutation counters

Command: `python3 analysis/mutation_detail.py`

| Mutation | Branch counter | Sample delta | Eval delta | Verdict |
|---|---:|---|---|---|
| ignore_phone_identity | 1 match | 0 | 0 | inert (redundant path) |
| ignore_catalog_links | 12 seeds → 1 fact | 0 | 0 | inert; the "12 rows" claim was seeds, not facts |
| no_empty_snapshots | 30 calls | 0 | 0 | inert (later explicit facts win) |
| citation_newest_only | 0 differing choices | 0 | 0 | inert (coverage and recency coincide) |

Status-flipping mutations, union 57 cases, each flip is exactly one finding of
the mutated category (deciding finding + evidence id extracted for every case):

- `support_retained` 15: e.g. `case_53 support_1034 evidence_28`,
  `case_66 support_4249 evidence_93`.
- `analytics_retained` 7: e.g. `case_50 analytics_7438 evidence_19`,
  `case_161 analytics_2008 evidence_15`.
- `flow_never_active` 11: e.g. `case_39 data_flow_1121 evidence_14`,
  `case_56 data_flow_373 evidence_05`.
- `backup_never_risk` 24: e.g. `case_75 backup_8673 evidence_91`,
  `case_87 backup_4689 evidence_08`.

All 57 were enumerated with deciding finding/evidence; four were spot-read
against the raw line (`case_53`, `case_50`, `case_39`, `case_75`). The rest were
checked structurally, not line-by-line.

## PHASE 13 — oracle independence

First-run 81 disagreements, after fixes all oracle-side:

| Cause | Count | Arbitrated by |
|---|---:|---|
| support attachments read as messages | 7 | `deletion_rules.csv` rule_06 + sample `case_07` (DELETE) |
| analytics `PRESENT` vs `IDENTIFIABLE` | 54 | rule_07 + sample `case_21/case_26` (`VERIFY_ANONYMIZED`) |
| handover facts lacked line numbers | 20 | **engine agreement only**; those subjects have no eval case |

The 20 handover lines cover 0 eval cases (decoy subjects in evidence_03), so the
"engine-only" group is unvalidated but has no scored exposure.

Lines with a subject token and no state cue: the top keys are `resource_id`,
`updated_at`, `event`, `level`, `origin_system`, `collection_name`,
`service`, `trace_id`, `subject_reference`, `customer_reference`, `email`,
`lookup_key` — identifiers/contacts, no state fields. Blind spot: support
message bodies are not keyed, only their requester fields.

## PHASE 14 — audit-record shape and expected recall

- Sample canonical `VERIFY_RECORD_PRESENT` prefixes: **audit** only (7).
  SQL-path PRESENT prefixes: **audit** only (66). Prefix sets are identical;
  the risk is semantic: 33 of 66 come from `security_audit_events` (events),
  not retained audit records — **33 likely extras**, plus 29 table rows of the
  same name and 4 failover rows.
- 2×2 on sample cases 11–32: `(has profile, has account step)` =
  **(11,11) and (11,0)**; `(True,False)` and `(False,False)` are empty. Every
  case has an account verification, so `P(account | no profile) = 1.0`.
  Eval has 279 no-profile subjects → **279 expected omitted account slots**.
- Analytics: 5/5 subjects in 11–32 have an analytics verification → rate 1.0;
  70 eval analytics subjects → **70 expected omitted slots**.
- Implied step recall under the assumption that each omitted slot is one step:
  emitted 2,790 steps → 2,790 / (2,790 + 349) = **0.889** (account-only:
  0.909). This is an upper bound, not a measured score.

## PHASE 15 — close-outs

- N/A: problem statement says "Use an empty array (`[]`) for `NOT_APPLICABLE`
  because no deletion or deletion verification is authorized." All **10** rows
  are `[]`. Met.
- D1 = 163/26; D7 corrected (0/518 deletion-classified lack a stem; four
  non-deletion texts have none). Scratch-text grep (sigma glyph, draft phrases, TODO,
  FIXME): empty.
- Submission hygiene: `output.csv` at repo root; header
  `case_id,deletion_status,steps_json`; 518 rows; natural sort; validator 0
  errors; `code/evaluation/evaluation_report.md` and `usage_report.md` now
  present; `code/evaluation/main.py` runs; README has install/run; `log.txt`
  follows AGENTS.md §5.

## Claims downgraded

| Old | Now |
|---|---|
| "field-level 1024/1162 (88.1%)" | **1024/1351 (75.8%)** — the old denominator dropped 27 missing steps |
| "catalog links seed 12 ownership rows" | 12 seeds, **1 fact**, 0 verdict changes |
| "empty snapshots influence state" | inert: 30 branch runs, 0 changes |
| "SQL PRESENT path unvalidated" | 33 of 66 are event rows: **33 likely extras** |
| "phone identity path" | 1 match, 0 verdict changes |

## Not done

Full SQL state oracle (column semantics) over all SQL files; line-by-line read
of the remaining 53 mutation-flip cases; metamorphic suite.
