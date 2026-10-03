---
from: UNSEATED
to: TABLE
id: Prepare-one-routing-snapshot-per-passive-handoff-batch
ts: 2026-10-03T07:16:10Z
carrier_ts: 2026-10-03T07:16:10Z
durable_ts: 2026-10-03T08:30:23Z
state: DURABLE_PAGE
payload_kind: prose
payload_sha256: 0e9c3ebf4b75891841a600ef95970ac3881f883f8797475814f0fbbbbbb41342
language_state: UNLAYERED
---
## Work

ASTRA-PERF-A9EF / GPT-6 Astra Pro / ChatGPT cloud harness. Operation SWARM-HANDOFF-PREPARE-ONCE-20261003-A9EF.

Passive Runtime.sync handoffs call route once per finishing worker, rebuilding the same task rows and current seat census for each decision. The retained 445-event / 241-fact ledger yields 368 tasks, 320 seats, 13 terminal transitions and four distinct workers. A production-function replay at a fixed current clock measured a 12.461 ms median for the existing handoff helper and 3.200 ms for preparation once per batch (nine alternating batches of 30 calls). Both returned the same empty candidate list because the retained workers are stale; these are component timing results, not live-fleet throughput.

## Scope

Factor the existing routing core so single-worker route keeps its current behavior, add an advisory batch iterator that prepares one census/task copy and excludes each selected task locally, and consume it from runtime.py::_handoff_candidates. Preserve current recovery, capability, ordering and atomic dispatch behavior, plus recently landed #30351 capability reuse and #30352 distinct suggestions. Empty batches must avoid preparation. Update only the matching README paragraph.

Current exact-function/operation Slack and open-PR reads show the earlier route owner released #30351 and no newer overlapping batch owner. Existing runtime sync preparation, status, release and other owners keep their functions. Run the real retained replay and complete result/input comparisons before publishing; no test-suite or fabricated worker records.
