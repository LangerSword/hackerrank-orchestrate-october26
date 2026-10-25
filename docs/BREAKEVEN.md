# Break-even under two scoring models

Correction: **omission** causes the step-number shift, not a wrong guess. A
wrong-id guess still occupies its slot. The previous table guessed all 26 slots;
that was wrong. Only the 17 account slots have a candidate pool. The 7 analytics
and 2 audit slots have none and stay omitted.

Metrics are strict canonical index alignment: `steps[i]` is compared with
canonical `steps[i]` for `i < min(len(pred), len(gold))`, over the seven fields,
denominator `len(gold) * 7 = 1351`. Missing positions score 0; extra predictions
beyond the canonical length are not counted. Exact-step F1 is set-based on the
six content fields (step number excluded): a prediction matches a canonical
step if phase, system, resource, operation, state and evidence all match.

## 1. Exact-step F1

Let current F1 be `F`. Add one guessed step with probability `p` of being exact.

- Correct: one true positive, one more prediction.
- Wrong: one false positive and one false negative.

The expected change is positive only when:

```text
p > F / 2
```

With `F = 0.928`, break-even is **0.464**. The best measured account guesser is
`14/32 = 0.438`, below it.

## 2. Sample measurements

4,000 seeded trials; guesses only on account slots at `p = 0.438`.

| Strategy | Strict positional fields | Precision | Recall | F1 | Exact-step F1 |
|---|---:|---:|---:|---:|---:|
| Omit all 26 (current output) | 1033/1351 = **76.5%** | 1.000 | 0.865 | 0.928 | **0.928** |
| Oracle-fill all 26 | 1351/1351 = **100%** | 1.000 | 1.000 | 1.000 | 1.000 |
| Fill 9 non-account slots only; omit 17 account | 1099/1351 = **81.3%** | 1.000 | 0.912 | 0.954 | 0.954 |
| Guess 17 account slots at 0.438; omit 9 | 1235/1351 = **91.4%** | 0.948 | 0.904 | 0.926 | **0.926** |

The shift-only row isolates alignment: filling the 9 non-account slots exactly
recovers 4.8 field points and 0.026 F1. The remaining 17 account slots cost
another 14.8 field points. Guessing those at 0.438 recovers 10.1 field points
but loses 0.002 exact-step F1 versus omission.

## 3. What this means

- **Exact-step F1:** abstain. `0.438 < 0.464`; the guess row is 0.926 vs 0.928.
- **Strict index-aligned fields:** guessing account slots is worth about +10
  points (76.5% → 91.4%), still short of the 100% oracle.
- The asymmetry is real: −0.002 F1 versus +10 fields. The grader's alignment
  determines which matters.
- The contract says array order is significant, so index alignment cannot be
  dismissed. It does not prove the grader uses it.
- **Decision:** the shipped output abstains. `case_06` is not a guess:
  `account_006` comes from `search_documents_primary.source_resource_id`, a
  same-record foreign key, and the emitted step is a future verification.

If a guess rule were ever adopted, it would be limited to account slots, with a
documented deterministic candidate rule, a README disclosure, and an interview
answer. It would not be a hidden finding.
