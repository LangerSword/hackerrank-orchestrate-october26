# Edge census

Every resource-id value in a row, JSON key, log field, handover field or digest
entry was scanned. The value must match `account|analytics|audit_record|search|
export|backup|data_flow|support|object` + digits, and the field must not be the
row's own `resource_id`/`id`.

## Result

| Source | Field | Target | Occurrences | Engine uses it |
|---|---|---|---:|---|
| `sql:search_documents_primary` | `source_resource_id` | account | 3 | **yes** (case_06) |

No other `_id` / `source_resource_id` edge into an account, analytics, search,
export, backup or audit resource was found in the participant data.

Keys that look like references but are not foreign keys:

- `archive_key`, `object_key` — storage paths (`archive/...`, `exports/...`),
  not resource ids.
- `lookup_key` — a query key in a log line, sometimes an email; not an edge.
- handover `field_2` — the system column, not a resource reference.
- digest `user_ref` — identity refs, not resource refs.

## Consequence

The census finds **no unused deterministic edge** that can name the 17 omitted
account slots or the 204 anonymous facts. `source_resource_id` is the one real
edge, and it is already used for case_06. The 77 unknown-identifier facts have
no in-graph owner; the 204 anonymous facts have no identifier. There is no
legitimate output recovery here without a new record.

Do not implement an unvalidated edge. A future edition would need a sample case
that validates the edge and a deterministic rule, then a measured step delta.
