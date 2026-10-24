# Audit round 6 — field diff, events decision, time keys, numbering

Builder: Hermes Agent (deepseek-v4.1-flash). No status flips; sample 32/32.

## PHASE 16 — the 138 field mismatches

Method: content alignment by `(phase, operation, system_id, resource_id)` first,
then field diff inside matched steps.

Denominator: 193 canonical sample steps, 166 emitted (27 omitted, 0 extra).

| Field | Match | Mismatch | Raw (ours, canonical, case) |
|---|---:|---:|---|
| step_no | 126 | **40** | (3, 4, case_06), (3, 4, case_07), (3, 4, case_08) |
| phase | 166 | 0 | — |
| system_id | 166 | 0 | — |
| resource_id | 166 | 0 | — |
| operation | 166 | 0 | — |
| state | 166 | 0 | — |
| evidence_id | 166 | **0** | — |

So the 138 are not content errors. They are **40 step-number mismatches plus
98 fields compared against the wrong step** by positional alignment (the old
1024/1162 denominator). Content-only score: **1122/1351 (83.0%)**; excluding
step_no, matched-step content is **996/996 (100%)**. Positional score:
**1024/1351 (75.8%)**; gap **98 fields (14 step-equivalents)**.

Classification and fixability:
- step number — 40, shifted only by the 27 omitted slots; not fixable without
  the unnameable ids.
- evidence id — 0 mismatches; canonical cites exactly one id per step, as we do.
  No multi-id rule exists to implement.
- free-text/detail — none in the output schema.
- enum/state — 0.
- other — 0.

No code change: there is no rule that raises field accuracy without inventing
ids. Claim downgraded: "138 mismatched fields" are alignment artefacts, not
wrong values.

## PHASE 17 — the 33 `security_audit_events` steps

Sample matched `VERIFY_RECORD_PRESENT` sources (7):
- `case_03 audit_record_2016` — log `resource_lookup_trace_20260926` (security_service)
- `case_21/25/26/27/28` — `service_resource_export_20260915` `security_service.audit_records`
- `case_31 audit_record_6909` — **bundle `customer_data_snapshot_bundle_20260915`, collection `security_audit_events`**

The sample therefore contains an **events-type source producing a canonical
PRESENT step**. Raw shapes are identical: `audit_record_N`, `subject_reference`,
`event_name=account_deletion_reviewed`. `security_audit_records` rows add
`event_code` and `retention_until`; the id pattern is the same.

No counterexample found: no sample subject has events rows and lacks a canonical
PRESENT step. Decision rule: **keep the 33**. p is at least 0.5 by the sample
precedent and the identical id shape; the F1/2 bar is ~0.46. Do not drop.
(Previous "33 likely extras" claim is retracted.)

## PHASE 18 — time-based keys

- `expires_at`: only one export row maps to a case — `export_001`, `case_08`,
  expires 2026-10-04 after audit 2026-09-14 (live), canonical INCOMPLETE.
  The **expired-before-audit side is unexercised** (0 mapped sample cases; eval
  count not enumerated in this pass).
- `retention_until`: 30 rows, all after 2026; audit dates are 2026. The
  **expired-retention side is unexercised, 0 rows**.
- `last_delivery_status`: 25 rows; `enabled=true` with `stopped` occurs **0**
  times, so the engine's `enabled`-only reading has no conflicting row. Reading
  defensible.

No rule change: the policy file does not state an expiry action, and the sample
only exercises the retained/live side.

## PHASE 19 — numbering and matching

Quotes: "Step numbers start at `1` and increase consecutively." and "The grader
parses `steps_json` as JSON … array order is significant."
Scores: content-only **1122/1351 (83.0%)**; positional including step number
**1024/1351 (75.8%)**; gap **98 fields**. Numbering gaps are **not permitted**
by the quoted contract, so no change. The 27 omissions are the sole cause of
the 40 number shifts.

## PHASE 20 — flip dump

`analysis/flip_dump.md`: 57 entries, 844 lines, each with case, rule, finding,
evidence id, raw line ±2 and a one-sentence reason. Four examples:
`case_124 support_9126 evidence_87`, `case_160 support_4148 evidence_15`,
`case_50 analytics_7438 evidence_19`, `case_75 backup_8673 evidence_91`.

## PHASE 21 — remaining

- 10 support bodies read: one `[REDACTED]`, the rest contain the subject's email
  inside the message ("Please send the delivery update to …"). No body says
  "removed", "deleted", "still visible" or similar state text.
- SQL column-semantics oracle over all SQL files: **not done** (only the
  soft-delete absence check from Round 5).
- Docs consistency: field metric 75.8% everywhere; recall 0.889; events
  decision now "keep 33" in DECISIONS and README.

## Claims changed

| Old | Now |
|---|---|
| 138 mismatched fields inside matched steps | 40 step_no + 98 positional-alignment artefacts; content 996/996 |
| 33 events likely extras | **kept** — sample `case_31` is an events-type PRESENT |
| expired export/retention behaviour | unexercised, not validated |
