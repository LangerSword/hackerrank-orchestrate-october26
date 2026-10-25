# Evaluation report — Ghost Data Still Exists

Builder: Hermes Agent (deepseek-v4.1-flash). Final run: deterministic engine,
zero model calls.

## Method

- Sample gate: `python3 code/main.py --sample && python3 analysis/compare.py`
  against the 32 public answers.
- Full run: `python3 code/main.py`, then the contract validator over 518 rows.
- Enumeration audits (not sampling): loose identifier scan over 79 text
  evidence files, line-level state oracle over 959 lines and 761 JSON records,
  independent sqlite oracle over 66 SQL-only COMPLETE cases, 14 mutations.
  Validator negative controls: 15/15, including invalid status, unknown
  activity, and post-audit activity citations.
- Strict-mode provenance: 1,289 raw subject-token lines outside facts; **0
  state-bearing completed lines** outside facts. The raw lines are lookups,
  heartbeats and other non-observation events, not missed state.
- The sample contains no NOT_APPLICABLE case; intent has no label coverage.

## Metrics (32 public samples)

| Metric | Result |
|---|---|
| Case-level status accuracy | **32/32 (100%)** |
| Row completeness (518) | **518/518** |
| Step-level match | **167/193 (86.5%)**, 0 extra |
| Field-level match | **1033/1351 (76.5%)** (includes 26 missing steps) |
| Content fields on emitted steps | **1002/1002 (100%)** |
| Exact sequence | **12/32 (37.5%)** |
| Precision / recall / F1 (steps) | 1.000 / 0.865 / **0.928** |

Omitted 26 steps: 17 account verifications for deleted accounts, 7 anonymised
analytics verifications, 2 retained audit records. No identifier in
participant data ties those resources to the subject; the best activity guesser
scored 43.8% against a 46.3% exact-match break-even, so they are omitted rather
than guessed. Every emitted step matches the six content fields of a gold step;
the 26 misses are absent steps, not wrong fields. Positional field accuracy is
lower because each missing step shifts the steps after it.

## Custom evaluation cases

1. **Replica drift.** Primary table has no row; failover replica has the same
   `resource_id` at the same capture. Expected `REPORT_REMAINING_RECORD`
   (DELETE), then `VERIFY_RECORD_ABSENT`. Observed in sample `case_05`;
   engine output matches.
2. **Tombstone with identifiers.** Deleted-account reference with name/email
   present. Expected `REPORT_EXPOSED_PII` + `REDACT_RECORD` +
   `VERIFY_RECORD_REDACTED`; a nulled tombstone yields only the verification.
   Observed in sample `case_32` / `case_31`; matches.
3. **Post-audit evidence.** A record appears only in a capture after
   `audit_at`. Expected: does not change the verdict. Unit-tested against
   `case_127` (account present 08-19, audit 08-17); verdict stays COMPLETE.
4. **Retraction.** "Delete my account. Actually never mind, keep it."
   Expected `NOT_APPLICABLE`, `[]`; the classifier returns non-deletion.
5. **Conditional deletion.** "If you cannot keep my account, delete it."
   Expected DELETE; exercised in `analysis/test_intent.py`.

## Failures found and improvements made

- Support-replica contact rows were classified as messages (REDACT) instead of
  attachments (DELETE); fixed, which took the sample from 31/32 to 32/32.
- Backup console was read as restore risk; corrected to BLOCKED, removing an
  unsupported finding.
- Intent defaulted to deletion without a delete stem; tightened after 75/140
  adversarial probes, now 140/140 (self-authored, tuned).
- Token-level provenance could not detect a missed line; line-level provenance
  and an independent state oracle replaced it (0 disagreements on 959 lines).
- 66 SQL-sourced `VERIFY_RECORD_PRESENT` steps have no sample analogue; 33 come
  from `security_audit_events` (events, not retained records) and are the likely
  extras. Disclosed, not hidden.
- 279 eval subjects have no user-profile fact; every sample case without a
  profile still has an account verification (11/11), so those slots are expected
  but unnameable. Implied step recall under that assumption: ~0.89.

## Reproduction

```bash
./scripts/fetch_dataset.sh
python3 code/main.py --sample && python3 analysis/compare.py
python3 code/main.py
python3 code/evaluation/main.py
```
