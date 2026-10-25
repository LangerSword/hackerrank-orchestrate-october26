# Ghost Data Still Exists — Deletion Audit Agent

This repository contains a deletion audit agent for the HackerRank Orchestrate
October 2026 challenge. The agent reads 518 deletion requests. It decides if
each deletion is complete. It writes one row for each request to `output.csv`.

The agent uses only the supplied data. It does not use a language model. It does
not use the network. The result is deterministic.

## Quick start

```bash
git clone https://github.com/LangerSword/hackerrank-orchestrate-october26.git
cd hackerrank-orchestrate-october26
# Put the official dataset at ./dataset, or fetch it if network is available:
./scripts/fetch_dataset.sh
python3 code/main.py
```

The command writes `output.csv` in the repository root. The code-only README
with the module map is at `code/README.md`.

To run the sample check:

```bash
python3 code/main.py --sample
python3 analysis/compare.py
```

To run the contract check:

```bash
python3 code/evaluation/main.py
```

This regenerates `output.csv` and `analysis/sample_output.csv` first, then runs
the sample diff and the 518-row validator.

Requirements: Python 3.10 or later. The runtime uses the standard library only.
The dataset is not stored in this repository. `scripts/fetch_dataset.sh` gets
it from the official starter repository.

## How the agent works

```mermaid
flowchart TD
  subgraph Input
    A[dataset CSVs] --> B[Identity graph]
    A --> C[Evidence parsers]
    D[Activity links] --> E[Fact store]
    C --> E
    B --> E
  end

  subgraph Audit
    E --> F[Resource ownership]
    F --> G[State at audit_at]
    G --> H[Policy rules]
    H --> I[Planner]
    I --> J[steps_json]
  end

  J --> K[Contract validator]
  K --> L[output.csv]

  subgraph Verification
    M[sample_output.csv] --> N[compare.py]
    L --> N
    K --> O[Gate result]
    N --> O
  end
```

The steps are:

1. `tables.py` builds one identity for each person. It uses the current email,
   phone and hash. It also uses all historical values in `user_audit_log.csv`.
2. `evidence.py` reads each evidence file. It reads JSON, SQL, logs, text, PDF
   and image digests. It makes one fact for each observed resource state.
3. `index.py` links each fact to a person. A link can come from an identifier,
   a user ID, an earlier snapshot, or a catalog activity.
4. `state.py` selects the newest fact for each resource. The fact must be at or
   before `audit_at`. A row in any replica counts as present.
5. `policy.py` applies `deletion_rules.csv`. It maps each data category to
   DELETE, REDACT, ANONYMIZE or RETAIN.
6. `planner.py` writes the findings. It writes the remediation steps. It writes
   the verification steps. It uses the required order.
7. `validate.py` checks the output contract. It checks the row count, the step
   numbers, the phase order, the citation rules and the time rules.

The agent treats a reported status as a claim. It treats an activity SUCCESS as
a claim. It does not use either one as proof.

## Output

`output.csv` has this header:

```text
case_id,deletion_status,steps_json
```

The file has 518 data rows. The rows are sorted by `case_id`.

Each step has these fields: `step_no`, `phase`, `system_id`, `resource_id`,
`operation`, `state`, `evidence_id`.

Phases are ordered: FINDING, REMEDIATION, VERIFICATION.

## Verification

The repository includes four checks.

| Check | Command | Result |
|---|---|---|
| Public sample | `python3 code/main.py --sample && python3 analysis/compare.py` | 32/32 statuses, 167/193 steps, 0 extra steps, F1 0.928 |
| Contract | `python3 code/evaluation/main.py` | 518 rows, 0 validator errors |
| Negative controls | `python3 analysis/test_eval_negative.py` | 15/15 illegal outputs caught |
| State tests | `python3 -m unittest discover -s code/tests -t code` | 4/4 synthetic replica/tie/empty-snapshot tests |
| Claims check | `python3 scripts/check_claims.py` | no retracted phrases; headline numbers match a fresh run |
| Activity coverage | `python3 analysis/activity_coverage.py` | 82/82 sync, 83/83 data-flow, 25/25 restore covered |
| Activity corroboration | `python3 analysis/activity_corroboration.py` | 255 in-window; 32/36 disable claims, 0 contradicted |
| Attribution split | `python3 analysis/attribute_split.py` | 281 unattributed: 0 known-other, 77 unknown-id, 204 anonymous |
| N/A traps | `python3 analysis/na_traps.py` | 10/10 mapped: access 2, correction 3, portability 2, opt-out 2, login 1 |
| Strict mode | `python3 analysis/strict_mode.py` | 0 state-bearing completed lines outside facts |
| Break-even | `python3 analysis/breakeven.py` | exact F1 0.928 vs guess 0.924; index fields 76.5% vs 98.3% |
| Interview evidence | `python3 scripts/interview_evidence.py` | one-page evidence sheet for every answer |
| Package gate | `python3 scripts/verify_package.py` | clean extraction passes every check |
| Intent probes | `python3 analysis/test_intent.py` | 140/140 self-authored probes |

The full run gives 153 COMPLETE, 355 INCOMPLETE and 10 NOT_APPLICABLE.

The output is deterministic. Two runs give the same SHA-256:
`93eb70b7f428ddb1487fe379f5329ff964129c85a769483e6094cf29faa9891c`.

Two independent checks support the evidence parsers:

- A state oracle read 959 log lines and 761 JSON records again. It found 0
  disagreements with the fact store.
- A SQL oracle read 66 SQL-only COMPLETE cases again. It found 0 disagreements.

## Activity corroboration

`analysis/activity_corroboration.py` checks every subject-linked activity inside
a case window against later evidence. It is corroboration only; activity
`SUCCESS` never becomes state.

| Activity | In-window | Corroborated | Contradicted |
|---|---:|---:|---:|
| SYNC_RECORD | 82 | 82 | 0 |
| CHECK_DATA_FLOW | 83 | 83 | 0 |
| DISABLE_DATA_FLOW | 32 of 36 | 32 | 0 |
| CHECK_RESTORE_ACCESS | 25 | 25 | 0 |
| BLOCK_RESTORE | 32 | 32 | 0 |
| RESTORE_BACKUP | 0 (1 post-audit) | 0 | 0 |

No in-window `DISABLE_DATA_FLOW` claim is contradicted by later evidence. The
one `RESTORE_BACKUP` (`backup_9287`, 2026-08-22) is after case_55's audit and is
excluded.

The agent makes 0 model calls. It makes 0 network calls.

## Limits

The sample has 26 verification steps that the agent cannot attribute. The
records have no subject identifier after deletion or anonymisation. The agent
does not guess these resource IDs. The best activity-based guess scored 43.8%.
The break-even point is 46.3%.

Two cases have a known evidence conflict:

- `case_63`: the image shows one owner. A catalog link 7 minutes later shows a
  different owner. The agent keeps the resource link and reports the conflict.
- `case_55`: the backup console shows an archive but no restore field. The
  engine defaults to `BLOCKED` and emits `VERIFY_RESTORE_BLOCKED`; the image
  does not prove the block. This is a policy default, not an observation.

These limits are recorded in `docs/DECISIONS.md`. The agent does not invent data
to remove them.

## Repository map

```text
code/
  main.py                 entry point
  audit/                  identity, evidence, state, policy, planner, validator
  evaluation/             evaluation and usage reports
  tools/                  digest builder
analysis/
  compare.py              sample diff
  test_eval_negative.py   validator negative controls
  test_intent.py          intent probes
docs/
  DECISIONS.md            design decisions and measurements
scripts/
  fetch_dataset.sh        dataset loader
output.csv                final predictions
log.txt                   agent session log
```
