# Ghost Data Still Exists — deletion-audit agent

HackerRank Orchestrate, October 2026. An agent that proves whether a user's
personal data is actually gone, reconstructs the state at `audit_at` from
supplied evidence, and emits the ordered remediation and verification plan.

**Status:** 32/32 public-sample statuses, 166/193 sample steps (the 27 omitted
slots are not derivable from participant data — see `docs/OPEN_PROBLEMS.md`),
518/518 rows on the full run with a clean contract validator.

## Run

```bash
git clone https://github.com/interviewstreet/hackerrank-orchestrate-october26.git dataset-src
ln -s "$PWD/dataset-src/dataset" dataset
python3 code/main.py            # writes output.csv
python3 code/main.py --sample   # writes analysis/sample_output.csv
python3 analysis/compare.py     # sample diff vs dataset/sample_output.csv
python3 code/main.py --case case_33   # inspect one case's reconstructed state
```

Python 3.10+, standard library only. No network, no model calls, no keys.

## Architecture

```
dataset/ ──► ingest ──► identity graph ──► evidence facts ──► state @ audit_at ──► policy ──► steps
```

| Stage | Module | What it decides |
|---|---|---|
| Identity | `code/audit/tables.py` | Current + historical emails/phones/hashes → one subject; 518/518 resolved |
| Intent | `code/audit/intent.py` | Deletion vs access/correction/portability/opt-out, six languages |
| Evidence | `code/audit/evidence.py` | JSON exports, snapshot bundles, manifests, SQL snapshots, four log dialects, handover text, PDF/screenshot digest |
| Ownership | `code/audit/index.py` | Resource → subject by identifier, `user_id`, earlier snapshot, or data-catalog link |
| State | `code/audit/state.py` | Latest observation ≤ `audit_at`; replication drift; empty readback snapshots; post-request horizon |
| Policy | `code/audit/policy.py` | `deletion_rules.csv` drives DELETE / REDACT / ANONYMIZE / RETAIN |
| Plan | `code/audit/planner.py` | Findings → remediation → verification, canonical operation order, one evidence citation per case |
| Gate | `code/audit/validate.py` | Row count, step numbering, phase/operation order, post-audit citation ban, empty remediation evidence |

Key design rule: **reported statuses and operation results are claims**. The
verdict comes only from evidence whose own `observed_at` is at or before the
case's `audit_at`.

## Current output

- 153 COMPLETE, 355 INCOMPLETE, 10 NOT_APPLICABLE
- 518 data rows, sorted, header `case_id,deletion_status,steps_json`
- Every finding cites an evidence id; every future step cites none
- Validator: 0 errors

## Open problems

See `docs/OPEN_PROBLEMS.md`: 27 sample verification slots no participant can
attribute from the shipped data, plus the modelling questions behind them.
