# Audit round 3 — supervision brief execution

Builder: Hermes Agent (deepseek-v4.1-flash). Requester: Lakshaya.
Every number below is from the command shown, run on 2026-10-25 in
`~/projects/hackerrank-orchestrate-october26`.

## PHASE 0 — premises

Command: `python3 - <<'PY'` (id intersection, subject fan-out, extension census)

Denominator: 32 sample ids, 518 evaluation ids, 94 manifest files.

Result:
- sample ids inside the 518: **0/32**. Sample range `case_01..case_32`,
  evaluation range `case_33..case_550`.
- distinct subjects: **517** for 518 cases; exactly **1** subject with two
  cases (ingrid.dahl); 0 unresolved.
- extensions: `.csv 9, .log 26, .json 28, .sql 24, .txt 1, .png 11, .pdf 4`.
  All are read: png/pdf through the content-hashed digest (15/15).

Three raw examples: `sample case_01 not in deletion_requests.csv`;
`case_33 ingrid.dahl` and `case_37 ingrid.dahl` share `user_18`;
`dataset/evidence/images/*.png` is non-text and digest-only.

What would have falsified it: any sample id present in the 518, or an
identically named evidence file with a different hash.

Decision: premise corrected — **the sample is a separate fixture, not a
validated subset of the scored rows**. Its labels validate behaviour, not the
exact rows. Sample check: 32/32.

## PHASE 1 — loose scan and conflicts

Commands:
```
python3 analysis/export_subjects.py
python3 analysis/conflicts.py --subjects analysis/subjects.json --evidence dataset \
  --ignore '^(deletion_requests|sample_deletion_requests|user_identities|user_audit_log|sample_output|output|evidence_files)\.csv$'
python3 analysis/sweep.py --subjects analysis/subjects.json --output output.csv \
  --evidence dataset --ignore '<same>' [--consumed analysis/consumed.json]
```
Ignore regex excludes only request/identity/answer tables. 79 text evidence
files plus 2 root tables scanned; 15 pdf/png skipped (digest-only).

Result:
- (a) identifiers owned by more than one subject: **0**.
- (b) lines naming two different subjects: **0**.
- COMPLETE cases with ≥1 raw subject hit: 153/153 (expected: absence readbacks).
- Loose-only cases: **10**, all phone-format variants.
- With token provenance: 13 cases, 17 unconsumed lines. Top files:
  `system_activity.csv 25`, `regional_replicas_20260424 8`,
  `regional_replicas_20260330 7`, bundles 5–6 each.
- Presence-only candidate lines in COMPLETE cases: **0**.
- All 10 loose phone rows are attributed to the case subject by the engine
  under digit normalisation: **10/10**.

Three raw examples: `system_activity.csv:4011` (catalog link, not a state
fact, by design); `customer_data_snapshot_bundle_20260819.json:385`
(`phone +234 803 344 0634`, consumed as `p:2348033440634`);
`customer_data_snapshot_bundle_20260322.json:15` (same pattern).

What would have falsified it: one COMPLETE case with a presence line that the
engine neither consumed nor explained.

Decision: unchanged. Claims downgraded: "0 flags" now reads
"0 shared identifiers and 0 cross-subject lines across 79 text evidence files".
Sample check: 32/32.

## PHASE 2 — parser provenance

`analysis/consumed.json` is emitted from the fact store (file → identifier
tokens). **Limitation, disclosed:** tokens only, no line numbers; a token
anywhere in a file counts that file's lines as consumed. This over-approximates
consumption, so the gap counter is a lower bound.

Reviewed top files: `system_activity.csv` is not state evidence (only
`LINK_RESOURCE_IDENTITY` is used, for ownership); replica/bundle entries are
phone-format variants already consumed. No parser-gap file found.

What would have falsified it: an unconsumed line carrying a presence state
(`FOUND`, `rows=1`, `200`, `enabled=true`, `restore_allowed=true`). None.

Decision: unchanged; docs now state the token-level limitation.

## PHASE 3 — state edges

Command: `python3 - <<'PY'` (ties, boundary equality, replica disagreement,
fallback, citation candidates)

Denominator: 518 cases, all facts ≤ `audit_at`.

Result:
- same resource + same timestamp, differing state: **0**. Tie-break exists
  (`max(observed_at, state != ABSENT)`) but is unexercised.
- observations exactly at `requested_at`: **0**; exactly at `audit_at`:
  **1141**. Inclusive `≤` is validated by sample cases citing `evidence_03`
  captured exactly at `audit_at`.
- replica vs primary disagreement in both directions: **0 true cases**.
- fallback (facts exist, none after `requested_at`): **1** (`case_33`).
- citation: unique newest file **506**; recency decides **2**; same-timestamp
  tie **0**. The sample has 0 ties, so the file-id tie-break is unvalidated.

Examples: `case_33` (only fallback); `case_70` present 09-10 → absent 09-16 in
one log; `case_11` evidence captured exactly at audit.

Decision: unchanged; the tie-break is documented as unexercised, not verified.

## PHASE 4 — independent sqlite oracle

Command: `python3 analysis/sql_oracle.py`

Denominator: 66 SQL-only COMPLETE cases, 66 sqlite files. The oracle re-loads
each snapshot with `sqlite3` and scans every table/column with its own loose
normalisation; it does not import `code/audit/evidence.py`.

Result: **0 disagreements**. (The first oracle run reported 29; the cause was
the oracle's own missing table→system map — the engine facts were correct.
Disclosed because the oracle is also code.)

Shape divergence: 44 of the 66 emit **only** `VERIFY_RECORD_PRESENT`, a shape
that appears in no sample COMPLETE case. 8 emit ABSENT+PRESENT, 7 emit
FLOW+PRESENT+REDACTED+BACKUP, 4 PRESENT+REDACTED, 3 ABSENT+PRESENT+REDACTED+
FLOW+BACKUP.

Examples: `case_59 lars-nielsen` → one retained audit record only;
`case_64 zulu.lindiwe` → ABSENT+PRESENT+REDACTED+FLOW+BACKUP.

What would have falsified it: an oracle row whose resource id is absent from
the engine's facts.

Decision: parser trusted for these 66; **step shape flagged as unvalidated**.

## PHASE 5 — intent

Command: `python3 analysis/test_intent.py`

Result:
- 518 requests: **508 triggered by a delete stem**, **10 by a non-deletion
  marker**; **0 weak triggers** (no case relies on "gone/closed/removed" alone).
- 10 NOT_APPLICABLE cases: no post-request evidence contradicts the reading
  (`case_533` has two PRESENT facts, consistent with keeping the account).
- Probes: **140/140** after fixes (EN/ES/PT/FR/DE/KO/JA, 20 each). First run
  was 75/140; fixes were stems (`elimín`, `encerr`), language-specific
  negations, conditionals, CJK negation, and a separate keep-pattern set so a
  conditional deletion overrides "keep the account" but never a negation.

Examples: "Si vous ne pouvez pas garder le compte, supprimez-le." → DELETE;
"¿Qué pasa si elimino mi cuenta?" → NON_DELETE; "삭제하지 마세요" → NON_DELETE.

Decision: classifier strengthened; visible corpus unchanged (153/355/10).
Sample check: 32/32.

## PHASE 8 — cheap innovations

- Differential status: INCOMPLETE ⟺ findings ⟺ remediation, **0
  disagreements / 518**.
- Generator structure: only **239/518** subjects have any `USER_PROFILE` fact
  ≤ audit; 279 have none. Security 418, search 270, support 162, flow 145,
  analytics 70, backup 58, export 31, attachment 19, tombstone 9.
- Mutation testing: **not run** (stated as not done).
- `docs/DECISIONS.md` written.

## Claims downgraded

| Old | Now |
|---|---|
| "Near-miss decoys: 0 flags" | "0 shared identifiers and 0 cross-subject lines across 79 text evidence files (loose matcher)" |
| "27 slots: closed, underivable" | "could not derive from shipped data; tests and denominators listed in OPEN_PROBLEMS" |
| "62 COMPLETE `.sql`: consistent" | "66 SQL-only COMPLETE agree with an independent sqlite scan; 44 have a step shape absent from every sample" |
| "sample is a validated subset" | "false: 0/32 sample ids appear in the 518" |
| "no hidden corpus for inputs" | "the scored file is assumed to be the shipped 518; unverified by us" |

## Not done

Mutation testing of every rule; metamorphic row-shuffle/identifier-rewrite
suite; extending provenance to line numbers for logs.
