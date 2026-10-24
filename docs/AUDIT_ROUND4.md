# Audit round 4 — independent state oracle, mutations, claim structure

Builder: Hermes Agent (deepseek-v4.1-flash). All numbers below are raw command
output on 2026-10-25.

## PHASE 6 — independent state oracle (non-SQL)

Commands:
```
python3 analysis/dump_facts.py
python3 analysis/state_oracle.py
```
Denominator: 959 log/handover/CSV lines and 761 JSON records that carry a loose
subject token and a state cue. The oracle does not import
`code/audit/evidence.py`; it re-derives state from raw text with its own
regexes, keyed by `(file, line)` for logs and `(file, resource_id)` for JSON.

First run: 20 unconsumed + 61 JSON mismatches. Every one was an **oracle bug**,
not an engine bug:
- analytics/support taxonomy (`PRESENT` vs `IDENTIFIABLE`),
- ticket attachments read as messages,
- handover facts had no line numbers (now fixed in `_parse_handover`).
After fixes: **0 disagreements**.

Engine provenance is now line-level for logs (1,059 facts carry `__lineno`) and
handover; JSON/SQL remain record-level, disclosed.

**Retraction:** the previous "0 presence-only candidate lines" result was
token-level and therefore untested. The line-level oracle is the replacement;
it finds 0 engine misses on 959 lines.

Limitation, disclosed: the same author wrote engine and oracle; shared
misreadings of column semantics (soft deletes, tombstones, null vs empty) would
pass both. SQL state is not covered by this oracle.

## PHASE 7 — mutation testing

Command: `python3 analysis/mutations.py` plus two corrected `_finding`
mutations. Baseline: sample 32/32, eval 153/355/10.

| Mutation | Sample status | Sample steps | Eval status | Eval steps |
|---|---:|---:|---:|---:|
| intent_always_delete | 0 | 0 | **10** | 10 |
| no_findings | 13 | 18 | 218 | 320 |
| support_retained | 0 | 8 | 15 | 156 |
| analytics_retained | 0 | 5 | 7 | 70 |
| backup_never_risk | 3 | 3 | 24 | 25 |
| flow_never_active | 1 | 6 | 11 | 113 |
| verify_order_reversed | 0 | 22 | 0 | 408 |
| drop_verify_present | 0 | 22 | 0 | 416 |
| drop_remediation | 0 | 22 | 0 | 355 |
| ignore_hash_identity | 1 | 1 | 0 | 0 |
| ignore_phone_identity | 0 | 0 | 0 | 0 |
| ignore_catalog_links | 0 | 0 | 0 | 0 |
| no_empty_snapshots | 0 | 0 | 0 | 0 |
| citation_newest_only | 0 | 0 | 0 | 0 |

Unvalidated with real exposure: **intent** (10 eval statuses; the sample has no
NOT_APPLICABLE case at all, so intent has zero label coverage). Inert on this
corpus: phone ownership, catalog links, empty snapshots (3 markers, no effect),
citation coverage (recency always coincides). Backup and flow rules are
sample-exercised (3 and 1 status flips). Hash ownership is sample-exercised but
eval-inert.

Hand-read: `case_55` (backup console, now a single BLOCKED verification),
`case_64` (five verification types, all from one inventory), `case_59` (one
retained audit record), `case_33` (fallback path), `case_151` (four
verifications, no findings).

## PHASE 8 — claim vs evidence structure

Sample reported → canonical (32): COMPLETE→COMPLETE 6, PARTIAL→COMPLETE 1,
NOT_STARTED→COMPLETE 3; COMPLETE→INCOMPLETE 11, PARTIAL→INCOMPLETE 4,
NOT_STARTED→INCOMPLETE 7. **No NOT_APPLICABLE cell exists** — intent is
unvalidated by labels.

Eval reported → derived (518): 163 COMPLETE→INCOMPLETE, 91 COMPLETE→COMPLETE,
116 PARTIAL→INCOMPLETE, 36 PARTIAL→COMPLETE, 76 NOT_STARTED→INCOMPLETE,
26 NOT_STARTED→COMPLETE, 10 NOT_STARTED→NOT_APPLICABLE. (D1's "25" is now 26.)

Iff test on the sample: "no USER_PROFILE fact ≤ audit" ⇔ "canonical has an
account verification" is **false, 14/32**. The 18 exceptions are all
`(no profile fact, canonical account step)` — the account record is gone
because it was deleted, which is precisely why the id is unnameable. So the
279 eval subjects with no profile fact are expected to carry an omitted account
slot each. On the sample this class alone is 18/193 = 9.3% of steps; the eval
recall implication is directional, not a computed score.

## PHASE 9 — audit-record shape

66 SQL-only COMPLETE cases emit 66 `VERIFY_RECORD_PRESENT` steps:
29 from the `security_audit_records` table, 33 from `customer_data_primary`
record_json (`security_audit_events`), 4 from the failover replica.

Sample `VERIFY_RECORD_PRESENT` steps with evidence come from: 1 log, 5 service
export, 1 bundle, **0 SQL**. The sample's SQL inventory (evidence_93) contains
only a backup row for the relevant subject; its canonical retained-audit ids
appear nowhere. Therefore the SQL PRESENT path is not sample-validated.
**66 steps are at risk of being extras (precision) in the eval.**

## PHASE 10 — close-outs

- Backup console (`evidence_32`) is cited by **0 sample cases**. The console
  path is unvalidated; it affects the eval only through `case_55`. Marked in
  DECISIONS/README. Backup restore-risk findings (25) come from logged
  `restore_allowed` facts, not the console.
- Intent vocabulary filter: 36 eval cases and 4 sample cases contain
  access/copy/correct/update/unsubscribe/login/reset words; reading them shows
  only "apply the correct treatment" and "before changing it" — no hidden
  access/copy request. No change.
- Account suffix hash test: 8/32 matches, all "account_00N = user_N" fixture
  cases (01–10); 0 md5/sha1/sha256 matches. Precommitted bar 18/18 → **failed**,
  stop.
- D7 fixed: 0/518 **deletion-classified** texts lack a delete stem; the 4 texts
  with none (533/535/540/541) are non-deletion.
- D1 fixed: 163 and 26 (not 25).

## Claims downgraded / retracted

| Old | Now |
|---|---|
| "0 presence-only candidate lines" (token-level) | retracted; line-level oracle: 0 misses on 959 lines |
| "sqlite oracle 0 disagreements" | true for **ids**, 66 SQL-only COMPLETE, not state |
| "140/140 probes" | first run 75/140; tuned to 140/140; self-authored |
| "backup rule unvalidated" | restore-risk is sample-exercised (3 status flips); console path is unvalidated |
| "empty-snapshot rule" | inert: 3 markers, 0 verdict changes |

## Not done

SQL state oracle for soft-delete/tombstone columns; mutation coverage of
`state.py`'s tie-break and window filter; metamorphic suite.
