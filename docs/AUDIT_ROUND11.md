# Round 11 — final pre-gate checks

## Check 1 — source_resource_id links in COMPLETE cases
Scanned all 32 sample and 518 eval COMPLETE cases for a subject-owned search
document carrying `source_resource_id=account_N` (the only account foreign key
in any evidence table). Result: **0 in the sample, 0 in the eval set**. No
COMPLETE case can gain a linked-account verification. No change.

## Check 2 — export_1842 and the statement
`export_1842` **does appear** in `system_activity.csv`:
`activity_4009, 2026-07-18T11:07:01Z, LINK_RESOURCE_IDENTITY, data_catalog,
export_service, export_1842, SUCCESS, "Data catalog linked export_1842
(NST-2026-0718-1842) to ingrid.dahl@outlook.com and user_18."`
So `NST-2026-0718-1842` is the export's name, not a coincidental statement
number. Timelines:
- case_33: requested 07-16 08:00, reported 07-18 02:00, audit 07-19 13:00.
  evidence_18 captured 07-18 11:00 (inside); evidence_23 captured 06-18 12:00
  (before the request).
- case_52: requested 06-16, audit 06-19 14:00. evidence_18 and activity_4009
  (07-18) are after its audit; they cannot be used.
**Applied.** 11 of 12 `LINK_RESOURCE_IDENTITY` rows already had a digest
entry; only `export_1842` was missing. Added `evidence_18` as
`export_1842 PRESENT` (ingrid, user_18, observed 2026-07-18T11:00Z).
Result: only **case_33** changes — export_1260 (pre-request, expired 06-25) is
replaced by export_1842 with evidence_18, still 3 steps, status INCOMPLETE.
**case_52 remains export_1260 / evidence_23.** Sample unchanged (32/32,
167/193), full run 152/356/10, validator 0.

## 3A — evaluation entrypoint
`code/evaluation/main.py` imports `csv, json, sys, pathlib` and
`audit.validate`; standard library only. It reads `dataset/sample_output.csv`,
`analysis/sample_output.csv`, `output.csv`, `dataset/deletion_requests.csv`,
`dataset/evidence_files.csv`; writes nothing; prints status/sequence/field
metrics plus validator metrics; exits 0 on pass, 1 on any validator error or
sample status mismatch.

## 3B — sample metrics through the harness
`sample status 32/32 | exact sequence 12/32 | fields 1033/1351`
Full: 518 rows, 152 COMPLETE / 356 INCOMPLETE / 10 NOT_APPLICABLE, validator 0.
Step precision 1.000, recall 0.865 (167/193), F1 0.928. Content-only fields
(phase/system/resource/operation/state/evidence) are 167/167 each.

## 3C — adversarial negative controls (12/12 caught)
| mutation | caught | first error |
|---|---|---|
| 517 rows | PASS | 517 rows for 518 requests |
| duplicate case_id | PASS | duplicate row |
| wrong header | PASS | header is ['case','status','steps'] |
| COMPLETE with [] | PASS | COMPLETE with empty steps |
| N/A with steps | PASS | NOT_APPLICABLE with steps |
| INCOMPLETE without findings | PASS | step_no 3 != 1 |
| non-consecutive step_no | PASS | step_no 4 != 2 |
| phase order reversed | PASS | future step cites evidence |
| tie-break order | PASS | step 4 out of canonical order |
| future step cites evidence | PASS | future step 3 cites evidence |
| post-audit evidence | PASS | cites post-audit evidence evidence_94 |
| activity_* citation | PASS | unknown evidence activity_4008 |
The header case previously crashed the validator; fixed to report an error and
continue.

## 3D — determinism, runtime, network
Two consecutive full runs produced the identical SHA-256
`633bf9dfca5a13e72741a1d8d619f785c16d3b2644c0cee48774fea3798800b5`.
Runtime: sample 0.48 s, full 1.19 s, evaluation 0.05 s, fetch script 0.00 s
(dataset present). No network/LLM imports in `code/`; zero outbound calls.

## Final
Tag after the gate; output hash above; statuses 152/356/10.
