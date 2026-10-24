# Open problems

Written for an external reviewer. Each item states the evidence, the current
choice, and what a better solution would need.

## 1. Twenty-seven verification slots have no participant-visible owner

On the 32 public samples the canonical output has 193 steps. This engine emits
166. The 27 missing slots are all `VERIFICATION` steps:

- `VERIFY_RECORD_ABSENT` for account resources whose account was deleted
  before the audit (`account_001`, `account_3136`, `account_5037`, …);
- `VERIFY_RECORD_ANONYMIZED` for analytics rows whose identifiers are already
  null (`analytics_5335`, `analytics_1895`, …);
- two `VERIFY_RECORD_PRESENT` steps for retained audit records.

The problem is ownership, not state. A deleted account leaves two traces:
an anonymous `404` lookup with no identifier, and a `DELETE_RECORD` activity
row with no identifier. Nothing in `dataset/` ties either to `user_25`. The
canonical answer knows the id from the organizer's private truth.

Options considered:

- **Omit** (current). Precision stays high; completeness loses one step per
  affected case.
- **Nearest-activity guess.** On samples the correct account id is within the
  top three nearest `DELETE_RECORD` rows to `reported_at` in 24/32 cases and
  rank 0 in 10/32. A greedy one-to-one assignment scores 12/32. Guessing
  injects a wrong resource id into a verification step, which is worse than an
  honest omission for a precision-weighted grader.
- **Constraint solve inside an evidence file.** When an export contains N
  anonymous accounts and N cases, the assignment is a bijection with no
  discriminating timestamps; list order does not follow case, user, or
  observation order. No solution found.

A better approach needs a signal this dataset does not ship, or a grader that
credits the operation/system/phase even with a wrong resource id. **Status:
we could not derive these ids; the tests and denominators are listed above,
not a claim that they are undeliverable in principle.**

## 2. Anonymised analytics rows

Six sample cases include `VERIFY_RECORD_ANONYMIZED` for an analytics row whose
`email`, `phone`, `hash`, and `user_id` are all null. That is the *desired*
end state, so the row cannot be attributed by construction. Same trade-off as
§1.

## 3. Intent defaults to deletion when no negation marker is present

Ten of 518 requests are non-deletion (access, correction, portability, login
reset, marketing opt-out) and all carry an explicit marker ("do not close",
"leave the account active", "not a request to erase"). Some deletion cases are
follow-ups that never repeat the word delete ("I found an old report saying my
account still existed… confirm the profile is gone"). Therefore the classifier
returns deletion unless a non-deletion marker governs the text. A reviewer
should attack this: is there a non-deletion request in the corpus with no
marker, or a deletion request whose reason contains one?

## 4. Category inference for support records

`support_replica.log` is a legacy contact index; its `contact_query_completed`
rows are classified as `SUPPORT_ATTACHMENT` (DELETE). This is the only reading
that matches sample `case_10`. Elsewhere support rows are `SUPPORT_MESSAGE`
(REDACT) or `ticket_attachments` (DELETE). If a future capture mixes both in
one file, the heuristic needs a record-level discriminator, not a filename.

## 5. Backup restore risk from a console screenshot

`backup_restore_console` shows an archive but no restore policy. The engine
treats that as `BLOCKED` (retained, restore must be blocked) rather than
`ACTIVE` (restore risk). The reasoning: a restore-risk finding needs evidence
that restore is allowed; an archive's existence is not that. A restore job in
`system_activity` only counts if it is at or before `audit_at` — one candidate
for case_55 fires two months later and must not change the answer.

## 6. What an LLM would add

The final run makes zero model calls: every verdict is reproducible from the
dataset and cheap to audit. An LLM layer is best used only where the artefact
is genuinely unstructured (a screenshot OCR failure, an unfamiliar PDF layout,
an out-of-distribution request language), and its output should be a *fact*
that enters the same fact store — never a verdict, a rule, a timestamp, or a
citation. The current document digest is a hand-verified cache; the natural
next step is a model-assisted digest builder with a human-checkable diff.

## 7. Evaluation

The only ground truth is the 32 public samples. The hidden 518 will diverge in
ways the sample cannot show: status distribution (this run is 69% INCOMPLETE
vs 50% in the sample), new evidence dialects, and new request phrasings. The
validator covers contract rules only; no local metric can estimate hidden
step accuracy.
