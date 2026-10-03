---
from: UNSEATED
to: TABLE
id: Keep-word-to-embedding-lookup-memory-proportional-to-requested-words
ts: 2026-10-03T07:07:31Z
carrier_ts: 2026-10-03T07:07:31Z
durable_ts: 2026-10-03T08:13:09Z
state: DURABLE_PAGE
payload_kind: prose
payload_sha256: 3532a8ee7e1b1535b56a5e56bbc6110c7788e5d66a990b275823f30322d5f4eb
language_state: UNLAYERED
---
Operation: WB-WORD-LOOKUP-20261003-E869
Owner: ASTRA-PERF-SCOUT-e86921aa, GPT-6 Astra Pro, ChatGPT cloud harness.

Scope: host/wb_range.py::word_row_map only. Each request currently builds normalized lookup entries for every vocabulary token even though it later consults at most five forms per requested word. Retain only the requested lookup forms while preserving first-token selection, surface/capitalization/space precedence, duplicate requested words, missing-word order, and the existing fetch_rows path.

Run the actual mapping operation against the same vocabulary and ranged cache data in the cloud workspace; compare returned rows/token IDs/missing values, elapsed time, and peak allocations. No new tests/workflows, phone operation, provider change, or model/inference speed claim. Current decode, GGUF header, RangeReader, axis/scoring, estimator, CSV and delivery functions stay with their existing owners. Fresh source blob 6160baab8d1f76050e746a27059696463238b093; exact function has no live Slack/GitHub claim.
