# Usage report — final full-dataset run

## Run

- Command: `python3 code/main.py` (writes root `output.csv`)
- Dataset: 518 requests, 94 evidence files
- Engine: deterministic Python 3 standard library; no network, no secrets

## Model usage

| Provider | Model | Calls | Input tokens | Output tokens | Cost |
|---|---|---|---:|---:|---:|
| none | none (deterministic engine) | **0** | **0** | **0** | **$0.00** |

- Total calls: **0**
- Total tokens: **0**
- Average per request: **0 tokens, $0.00**
- Per-model totals: not applicable (no model used in the verdict path)

## Why zero

Every verdict is a function of the supplied CSV/JSON/SQL/log/PDF artefacts:
identity resolution, evidence parsing, point-in-time state, policy application,
and step ordering. A model in this path could only introduce a hallucinated
resource id, timestamp or citation, which the contract forbids. There is no
model path in the runtime. A future extractor would be limited to candidate
facts, with a content hash and a deterministic schema check; it would never set
a verdict, timestamp or citation.

## Runtime shape

Parsing dominates: 94 artefacts (28 JSON, 24 SQL, 26 logs, 4 PDFs, 11
screenshots read through the content-hashed digest, 1 handover text), then
~2,900 facts are folded into 518 case states. No per-case model latency.
