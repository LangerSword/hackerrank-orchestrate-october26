# Document digest provenance

The digest is not a raw record. Each field is classified:

- **literal** — the value appears in the OCR/PDF text.
- **visual** — read from the image by a model or a person.
- **inferred** — derived from a catalog link, filename or other record, not
  visible in the image.

Across 13 entries and 56 classified fields: **28 literal, 23 visual, 5
inferred**.

| Entry | Resource | State | Identifiers | User ref |
|---|---|---|---|---|
| evidence_04 | literal | visual | literal | visual |
| evidence_09 | literal | visual | literal | visual |
| evidence_14 | literal | visual | literal | visual |
| evidence_19 | literal | visual | literal | visual |
| evidence_23 | literal | literal | literal | visual |
| evidence_28 | literal | visual | literal | visual |
| **evidence_32** | literal | **inferred** | literal | **inferred** |
| evidence_37 | literal | visual | literal | visual |
| evidence_42 | literal | visual | literal | visual |
| **evidence_46** | **inferred** | visual | literal | visual |
| evidence_58 | literal | visual | literal | visual |
| **evidence_60** | literal | visual | **inferred** | **inferred** |
| evidence_18 | literal | literal | literal | visual |

## Why this matters

- `evidence_32` (`backup_9287`): the screenshot shows the archive and the
  account email. It does **not** show restore status or `user_16`; both are
  inferred. Reverting the digest to `BLOCKED` restores the policy default, not a
  photographed fact.
- `evidence_60` (`marketing_001`): the image shows `sj.park@naver.com`; the
  digest carries `kwame-mensah@proton.me` and `user_09` from a later catalog
  link. That is the case_63 conflict; it remains unresolved.
- `evidence_46` (`object_19`): the resource id is inferred from the attachment
  filename/catalog link; the image shows `delivery_confirmation_19.pdf`.

No entry is treated as literal unless the value is in the extractor output. The
engine's content hash still invalidates a changed file.
