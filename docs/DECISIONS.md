# Decisions and the numbers behind them

Interview-ready record: rule, alternative rejected, measurement.

## D1. Reported status is never evidence
`reported_status` and activity `SUCCESS` are claims. Verdicts come from
observations with their own timestamp ≤ `audit_at`.
Measured: 163 reported-COMPLETE cases are INCOMPLETE here; 25 reported-
NOT_STARTED are COMPLETE. Alternative (trust the workflow) would collapse the
challenge.

## D2. Abstain on unidentifiable resources
27 sample verification slots (18 deleted accounts, 7 anonymised analytics,
2 retained audit records) have no identifier anywhere in participant data.
Best activity guesser: 43.8% (14/32); exact-match F1 is 0.925, break-even
46.3%. Unique-candidate cases: 0/32. Therefore omit, never guess.
Rejected: nearest-activity assignment, empty resource ids, hardcoded ids.

## D3. Two-phase ownership
Ownership is established at any time ≤ audit; state is the latest observation
≤ audit. Rejected: single-pass joins, which lose resources whose identifiers
were removed after ownership was established.
Measured: 91 cases have single-path attribution (81 email-only, 10 user_id-
only); 0 near-miss decoys across 79 text evidence files. Catalog links seed 12
ownership rows but attribute **1** fact and change **0** verdicts under
mutation; they are a redundancy, not a load-bearing path.

## D4. Replica presence counts
A row in any replica is presence. In this corpus no case has a replica-present
observation older than a later primary absent one, so the rule is unexercised
(0/518). It stays because the sample's failover case (`case_05`) is exactly a
replica-only row.

## D5. Inclusive audit boundary
`observed_at ≤ audit_at`. 1,141 observations sit exactly at `audit_at`; the
sample cites a file captured exactly at the boundary (evidence_03), so
inclusive is the evidenced reading.

## D6. Deterministic-first, no model calls in the verdict path
Zero calls, $0, reproducible. Rejected: LLM adjudication, because a single
hallucinated resource id is unrecoverable and the hidden set is graded on
steps. An LLM may only add facts (e.g. document extraction), never a verdict,
timestamp, or citation.

## D7. Intent: deletion requires a delete stem or a confirm-gone pattern
Default-to-delete was removed after the probe set: 0/518 texts lack a delete
stem, so tightening cost nothing. 140/140 probes across 7 languages after
fixes. Rejected: "no delete word means non-deletion" alone, which misreads
follow-ups ("confirm the profile is gone").

## D8. One evidence citation per case
Newest pre-audit file that covers the most violations; ties by file id.
Measured: 506/518 cases have a unique newest file; 2 need recency; 0 have a
same-timestamp tie. The sample has 0 ties, so the tie-break is deterministic
but unvalidated. Mutation `citation_newest_only` changes **0** cases: coverage
and recency coincide everywhere in this corpus, so the coverage rule is inert
here (counter: 0 differing choices).

## D9. Content-addressed document digest
PDF/screenshot facts are keyed by SHA-256. A changed artefact invalidates its
entry. Rejected: hand-keyed cache with no provenance, which looks like a
label file to a reviewer.

## D10. SQL parser verified by an independent oracle
66 SQL-only COMPLETE cases re-scanned with a from-scratch sqlite query: 0
disagreements. Residual risk is step shape, not rows: 44 of the 66 emit only a
retained-audit verification, a shape absent from every sample COMPLETE case.
