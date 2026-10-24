# Claude handoff — Ghost Data Still Exists (HackerRank Orchestrate, Oct 2026)

**Who is asking:** Lakshaya Sharma (LangerSword).
**Who is building:** Hermes Agent (Nous Research), running in the Hermes TUI on
`deepseek-v4.1-flash` via `opencode-go`. Hermes wrote the architecture, the
parsers, the diagnostics below, and this document.
**Repo (public, fresh-clone verified):** https://github.com/LangerSword/hackerrank-orchestrate-october26
**Dataset:** not committed; `scripts/fetch_dataset.sh` links the official
starter repo (`interviewstreet/hackerrank-orchestrate-october26`).
**Ask:** read the diagnostics, then tell us where the next points are. We will
implement; Hermes will run and verify.

---

## 1. The contract

518 cases. One row each: `case_id,deletion_status,steps_json`.
`deletion_status` ∈ COMPLETE / INCOMPLETE / NOT_APPLICABLE.

For each case the agent must:

1. decide whether the request actually authorises deletion (10 of 518 are
   access / correction / portability / opt-out / login-support traps);
2. resolve current **and historical** identifiers (email changes, phone
   changes, email-hash changes);
3. reconstruct each resource's state at `audit_at` — reported statuses and
   operation `SUCCESS` values are claims, never proof;
4. apply `deletion_rules.csv` (DELETE / REDACT / ANONYMIZE / RETAIN per data
   category);
5. emit FINDING → REMEDIATION → VERIFICATION, ordered by operation rank then
   `system_id`, `resource_id` (string ascending), with evidence ids on
   findings (and on COMPLETE verifications), empty on future steps.

The hidden truth was generated from a private structured table. Only the 32
public samples have answers.

---

## 2. What is built

Deterministic engine, zero model calls, Python stdlib only, ~2.5k LOC.

| Stage | Module | Detail |
|---|---|---|
| Identity | `code/audit/tables.py` | Current + audit-log identifiers per subject; case-insensitive; SHA-256 hash forms; 518/518 requests resolve (418 current, 100 historical-only) |
| Intent | `code/audit/intent.py` | 6-language delete lexicon; non-deletion marker patterns (negation, "keep the account", marketing-only, information request, login reset); default is DELETE only when no marker governs the text |
| Evidence | `code/audit/evidence.py` | 6 JSON schemas, 5 SQL table families, 4 log dialects (key=value, JSON, pipe, RFC5424), handover text, content-hashed PDF/screenshot digest |
| Ownership | `code/audit/index.py` | resource → subject by any identifier, `user_id`, earlier snapshot, or `LINK_RESOURCE_IDENTITY` activity; two-phase (lifetime ownership, then point-in-time state) |
| State | `code/audit/state.py` | latest observation ≤ `audit_at`; presence in any replica counts as present; empty readback snapshot proves absence; observations older than `requested_at` are dropped only when newer ones exist |
| Policy | `code/audit/policy.py` | `deletion_rules.csv` is the only policy source |
| Plan | `code/audit/planner.py` | findings → remediations → verifications; one evidence citation per case, chosen by violations-covered then recency; never post-audit |
| Gate | `code/audit/validate.py` | header, 518 rows, step numbering, phase/op order, banned post-audit citation, empty future evidence, COMPLETE-with-findings |

Measured:

- **Sample: 32/32 statuses.** Steps 166/193 emitted, 0 extra, 27 omitted.
  Field-level 1024/1162. Precision 1.0, recall 0.860, F1 0.925.
- **Full run:** 518 rows — 153 COMPLETE, 355 INCOMPLETE, 10 NOT_APPLICABLE.
  Validator: 0 errors. 685 findings, 685 remediations, 1420 verifications.
- A fresh clone reproduces the sample run (`python3 code/main.py --sample`;
  `python3 analysis/compare.py`).

The 27 omissions: 18 deleted-account verifications, 7 anonymised-analytics
verifications, 2 retained-audit-record verifications. Details in §3.1/§3.4.

---

## 3. Answers to the seven review items (with fresh numbers)

### 3.1 The 69% vs 50% gap — diagnostic run

The bucket split you proposed does not apply as stated because of an
architectural difference: **INCOMPLETE is only ever produced by a positive
finding**, never by absence of proof. A case with no facts yields COMPLETE with
zero steps, not INCOMPLETE.

Results over the 355 INCOMPLETE rows:

| Bucket | Count |
|---|---|
| (a) presence/active fact observed in `[requested_at, audit_at]` | **354** |
| (b) presence fact only before `requested_at` (fallback path) | **1** (`case_33`) |
| (c) no presence fact at all | **0** |

Other checks:

- COMPLETE with zero steps: **0** (this is where "deletion by ignorance"
  would show up in this architecture).
- Cases with any evidence **mention** of the subject: 507/508. Mention but
  **zero extracted facts**: **4**, all PDFs:
  `case_33` + `case_52` (account_history_report), `case_45`
  (security_retention_extract), `case_46` (legal_retention_register).
  None of the four is INCOMPLETE because of the gap; three are duplicate or
  supporting artefacts.
- Findings-per-INCOMPLETE distribution: 1→99, 2→206, 3→3, 4→48.

Interpretation: the 69% is not a parser-gap artefact. It is what positive
evidence says. The real over-calling risk is the **opposite** failure: a
misattributed decoy or an over-broad category turning a compliant case into
INCOMPLETE. The 206 two-finding cases are the structural family to audit
(typically search-present + one of analytics-PII / support-PII / flow-active).

### 3.2 Digest exposure — fixed

The PDF/screenshot cache is now **content-addressed**:

- `_meta.content_sha256` maps SHA-256 → `file_id` (15 artefacts, regenerate
  with `python3 code/tools/build_document_digest.py --hashes`).
- At load, the engine hashes each artefact; a hash that is absent or mismatched
  **invalidates** the cached entry rather than reusing it.
- `code/tools/build_document_digest.py` ships the extractor (`pdftotext`,
  `tesseract`), the `--text` dump, and `--check`.
- Entries contain facts only (system, resource, identifiers, state, observed
  time). No verdict, label, case id, or expected step.

### 3.3 "All 10 non-deletion requests carry a marker" — de-circularised

Test run: take all 518 requests, strip any text containing positive delete
vocabulary in six languages plus `gone`, `removed`, `closed`. Remaining: **4**
— and all four are already NOT_APPLICABLE (`case_533`, `535`, `540`, `541`).
So the population of "DELETE-classified requests with no delete vocabulary" is
**empty** in the visible corpus. The classifier never defaults on a text that
lacks a delete term; the 508 deletion cases all contain one. The residual risk
is hidden-corpus only. The six other N/A cases contain a delete word plus an
explicit negation ("do not close", "not asking for deletion", "without
removing", "marketing lists only", "not a request to erase", "don't delete").

### 3.4 Guess vs omit — break-even confirmed, no emittable subset

- F1 ≈ 0.925, threshold F1/2 ≈ **0.463**.
- Best activity-based guesser (nearest `DELETE_RECORD` to `reported_at` in
  `[requested_at, audit_at]`): **14/32 = 43.8%**, below threshold.
- Unique-candidate cases: **0/32**. Margin > 1 day between best and second
  candidate: **0/32**. There is no high-margin subset to emit, so abstention is
  not leaving points on the table under exact-match F1.
- Set vs positional matching is unknown. If positional, omission shifts step
  numbers and costs more than a false negative; this strengthens abstention.
- The two `VERIFY_RECORD_PRESENT` omissions are not a different class:
  `audit_record_6645` and `audit_record_5569` appear **nowhere** in the
  participant data (not in evidence, not in activity). They are as invisible as
  the deleted accounts, so there is no actor/subject field to exploit.

### 3.5 Anonymised analytics — quasi-identifier check (negative)

Anonymised rows carry `audience_cohort` only (`home_lifestyle`,
`returning_customer`, `general_shopper`, `mobile_browser`). No user profile,
order, or other evidence carries a cohort/segment attribute to join on. The
check was run; no legitimate join exists in the shipped data.

### 3.6 `support_replica.log` — coverage is tiny

3 extracted facts, 1 attributed case (`case_10`), 3 contact-query rows for
`support_4104`, `support_002`, `support_5914`. The filename rule affects one
sample case. The rows themselves carry no payload (`rows=1`, `last_write`, a
deletion-marker check), so there is no record-level discriminator inside that
file. Recommended refinement if we keep the rule: classify on row payload
(`message_text` vs `file_name`/`uploaded_by`), and treat the replica's
contact rows as attachment-index hits only because that is the sole reading
consistent with the sample.

### 3.7 Restore path — exclusion only, confirmed

`RESTORE_BACKUP` activity is **not** ingested; no code path flips BLOCKED to
ACTIVE on a restore job. The dataset has exactly one such row
(`activity_3387`, 2026-08-22) and it is after `case_55`'s `audit_at`
(2026-04-30), so the exclusion is the only exercised path. If we add ingestion,
it must be gated on `event_time ≤ audit_at` and must not override a later
explicit `restore_allowed=false` fact.

---

## 4. Ranked risks (our view, after the diagnostics)

1. **False presence / decoy attribution** (the reverse of the 69% concern):
   206 INCOMPLETE cases have exactly two findings; a single misattributed
   support or analytics row flips a COMPLETE to INCOMPLETE. Audit one family
   by hand against raw evidence.
2. **Category inflation**: 124 support-PII findings, 270 search findings, 113
   active-flow findings. Each category has a rule; a wrong category changes the
   operation (DELETE vs REDACT) and the final state.
3. **Hidden dialects**: 4 mention-but-no-fact cases here; the hidden 518 uses
   the same generator, so risk is low, but the digest invalidation now makes a
   changed artefact fail closed.
4. **Intent on the hidden set**: no visible counter-example; default-to-delete
   is still the one rule with no local oracle.
5. **Account/analytics attribution wall**: 27 sample slots; no legitimate
   signal found (see `docs/OPEN_PROBLEMS.md`). Any proposal must beat 46.3%.

---

## 5. What we want from you

1. Rank the next fixes by expected hidden-set gain, not sample gain.
2. For the 27-slot wall: is there a linkage signal we have not modelled
   (file-level residue, generator ordering, lifecycle attributes)? If not, say
   so and we stop spending on it.
3. For the false-presence risk: propose a cheap adversarial audit over the 206
   two-finding cases (what to sample, what to compare).
4. For intent: attack the lexicon with texts *not* in the corpus.
5. If you want code pasted, name the modules; the repo is ~2.5k LOC and the
   README carries the same architecture table.

---

## 6. Reproduce

```bash
git clone https://github.com/LangerSword/hackerrank-orchestrate-october26
cd hackerrank-orchestrate-october26
./scripts/fetch_dataset.sh
python3 code/main.py --sample && python3 analysis/compare.py
python3 code/main.py
python3 code/tools/build_document_digest.py --check
```
