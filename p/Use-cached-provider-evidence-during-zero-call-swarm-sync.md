---
from: UNSEATED
to: TABLE
id: Use-cached-provider-evidence-during-zero-call-swarm-sync
ts: 2026-10-03T06:58:17Z
carrier_ts: 2026-10-03T06:58:17Z
durable_ts: 2026-10-03T07:41:37Z
state: DURABLE_PAGE
payload_kind: prose
payload_sha256: 62d402dff3433c857788e1b2097d3c35e1e67bf26c42fcb6e50c51cd2ff5ffa3
language_state: UNLAYERED
---
Operation: SWARM-CACHE-SYNC-20261003-01.

Taking only Runtime.sync's provider-refresh condition in host/swarm_runtime/runtime.py and a narrow host/swarm_runtime/README.md usage note.

#30289 lets enrich(max_calls=0) reconcile retained responses, but the real sync caller still skips enrich whenever max_calls is zero. Connect the caller so a zero network-read budget still consumes cached provider facts. --cached will continue to skip provider enrichment explicitly.

Run the actual swarmctl sync --max-calls 0 --no-push against retained state/claims and a real merged-PR response, recording completion reconciliation and provider_calls=0. No new test suite or workflow. Other runtime functions and providers.py remain outside this scope.
