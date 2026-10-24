# Audit round 8 — digest fidelity, pair exposure, provenance

Builder: Hermes Agent (deepseek-v4.1-flash). Analysis only; no behaviour
change. Sample 32/32, full run 153/355/10, validator 0.

## 1. Digest literal check and vision

Literal check: for all 13 digest entries, the resource id and every identifier
must appear in the OCR text. **7 fail**:

| entry | missing from OCR |
|---|---|
| evidence_09 search_428 | `user_13` |
| evidence_14 data_flow_1121 | `user_14` |
| evidence_23 export_1260 | `ingrid.dahl@outlook.com` |
| evidence_32 backup_9287 | `areed1433@gmail.com` |
| evidence_42 tombstone_17 | `tombstone_17`, `user_17` |
| evidence_46 object_19 | `object_19`, `priya.raman@gmail.com` |
| evidence_60 marketing_001 | `kwame-mensah@proton.me` |

9 eval cases rest solely on PNG digest: `case_33, 34, 35, 39, 50, 52, 53, 61,
63`.

Vision checks (the model read the actual images):
- **case_39 / evidence_14** — row `data_flow_1121` exists with selector
  `jain.aditi@gmail.com` (user_14), mode **Continuous**, last contact 07:59:42.
  The digest is correct; tesseract simply failed to read the identifier.
  `data_flow_9846 / lucia-torres` is the second row. **Retract the Round 7
  "OCR is legible for the decisive tokens" claim.**
- **case_35 / evidence_09** — `search_428` shows Gabriel Silva,
  `g.silva76@gmail.com`, `user_13`; `search_1874` is a decoy with
  `g.silva76.jr@gmail.com`. Digest correct.
- **case_61 / evidence_46** — the image shows `delivery_confirmation_19.pdf`
  in the bucket, but **no `object_19` id and no priya email**. Ownership comes
  only from `activity_4007` (catalog link), which is participant data but is
  not the cited evidence. **Digest entry overstates what the image proves.**
  No behaviour change; flagged for review. The finding cites an image that does
  not itself establish the link.

## 2. Exposure by (category, normalised state)

Semantic pairs, independent of file family:

| Pair | Sample | Eval | Eval status-dependent |
|---|---:|---:|---:|
| SEARCH_INDEX_ENTRY / PRESENT | 12 | 270 | 28 |
| BACKUP_ARCHIVE / ACTIVE | 3 | 25 | 24 |
| SUPPORT_MESSAGE / IDENTIFIABLE | 5 | 98 | 15 |
| USER_PROFILE / PRESENT | 3 | 56 | 12 |
| DATA_FLOW / ACTIVE | 6 | 113 | 11 |
| USER_EXPORT / PRESENT | 2 | 31 | 8 |
| ANALYTICS_PROFILE / IDENTIFIABLE | 5 | 70 | 7 |
| SUPPORT_ATTACHMENT / PRESENT | 3 | 14 | 4 |
| ACCOUNT_TOMBSTONE / IDENTIFIABLE | 1 | 4 | 4 |
| **MARKETING_PROFILE / PRESENT** | **0** | **1** | **1** |
| SUPPORT_ATTACHMENT / IDENTIFIABLE | 0 | 4 | 0 |

At pair level only **1 eval status (case_63)** rests on a pair with zero sample
exposure. The Round 7 path-level figure (191) overstated semantic risk: the
same (category, state) vocabulary is shared across file families, as the
manifest/operational_record_history/record_lookup shapes show.

## 3. Staleness of FOUND-type rows

For eval rows from `operational_record_history`, `manifest`, `record_lookup`:
**268/268 deciding rows are inside [requested_at, audit_at]**, 0 earlier
(74 + 81 + 113). The "82 statuses on stale historical FOUND" risk is
**retracted**; the historical reading applies to `case_33` only.

## 4. Log provenance

`case_284 data_flow_6953`: fact line **31**, first line mentioning the resource
is 30 (the `*_started` line); line 31 is
`event=connector_config_read_completed … enabled=true`.
`case_291 backup_7079`: fact line **23**, first 22; line 23 is
`event=restore_policy_read_completed … restore_allowed=true`.
The fact store's provenance is the **completed** line; the v1/v2 dump printed
the first occurrence. `analysis/flip_dump_v2.py` now prints
`fact.detail["__lineno"]`; the line-level oracle was already keyed to the fact
line, so it is unaffected.

## 5. Docs

Round 7's OCR claim retracted; this file is the per-entry check. DECISIONS and
README updated: pair-level exposure (1 status), 268/268 inside window, digest
provenance defect at evidence_46.
