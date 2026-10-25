# Code — Ghost Data Still Exists

Deterministic deletion-audit engine. Python 3.10+; standard library only; no
network and no model calls.

## Setup

Put the official dataset at `./dataset` from the repository root. If the
`dataset/` directory is missing and network access is available:

```bash
./scripts/fetch_dataset.sh
```

## Run

From the repository root:

```bash
# Full run: 518 rows -> output.csv
python3 code/main.py

# Public sample: 32 rows -> analysis/sample_output.csv
python3 code/main.py --sample

# One-command gate: regenerates both outputs, checks the 32 sample answers,
# then validates all 518 rows
python3 code/evaluation/main.py

# Sample diff
python3 analysis/compare.py

# Validator negative controls
python3 analysis/test_eval_negative.py

# Claims check: no retracted phrases; numbers match a fresh run
python3 scripts/check_claims.py

# Sync/restore activity coverage
python3 analysis/activity_coverage.py

# Package gate: build zip, extract clean, run every check
python3 scripts/verify_package.py

# Intent probes
python3 analysis/test_intent.py
```

`code/evaluation/main.py` regenerates `output.csv` and
`analysis/sample_output.csv` before reading them, so it works from a clean
extraction. It exits non-zero if the sample status check or the contract
validator fails.

## Entry points

| Path | Purpose |
|---|---|
| `main.py` | CLI: full run, sample run, or `--case case_NN` debug view |
| `audit/tables.py` | identity graph from current and historical identifiers |
| `audit/evidence.py` | JSON/SQL/log/text/PDF/image parsers into facts |
| `audit/index.py` | manifest load and fact-to-subject attribution |
| `audit/state.py` | newest observation at or before `audit_at`; replica presence wins |
| `audit/policy.py` | `deletion_rules.csv` lookup and required final state |
| `audit/planner.py` | FINDING -> REMEDIATION -> VERIFICATION steps |
| `audit/validate.py` | 518-row contract, phase order, citations, time boundary |
| `evaluation/main.py` | sample gate plus full-run contract check |

## Design invariants

- Reported status and activity `SUCCESS` are claims, never proof.
- State comes from observations at or before `audit_at`; a row in any replica
  counts as present.
- A resource with no identifiers is omitted, not guessed.
- Findings cite evidence; remediation and future verification use an empty
  `evidence_id`.
- `step_no` is consecutive from 1; no gaps.

## Measured result

- Sample: 32/32 statuses, 167/193 steps, 0 extra, 12/32 exact sequences.
- Fields: 1033/1351 positional; 1002/1002 content fields on emitted steps.
- Full run: 153 COMPLETE / 355 INCOMPLETE / 10 NOT_APPLICABLE; 0 validator errors.
- 0 model calls, 0 tokens, $0.

See `evaluation/evaluation_report.md` and `evaluation/usage_report.md`.
