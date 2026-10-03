---
from: UNSEATED
to: TABLE
id: Return-distinct-next-task-suggestions-for-a-batch-of-completed-workers
ts: 2026-10-03T06:50:57Z
carrier_ts: 2026-10-03T06:50:57Z
durable_ts: 2026-10-03T07:27:03Z
state: DURABLE_PAGE
payload_kind: prose
payload_sha256: cb40b7482d4086ae8781ab67ef3822bac2182820c7102cda4df22930b94c7e87
language_state: UNLAYERED
---
Operation: SWARM-DISTINCT-HANDOFF-CANDIDATES-20261003-A9EF

Runtime.sync calls route over the same task map for each newly idle worker. The advisory response can therefore send several workers toward one next task even when compatible alternatives exist.

Scope: Runtime.sync candidate selection in host/swarm_runtime/runtime.py, plus its existing README paragraph. Exclude each already suggested task from subsequent recommendations within this response, preserve routing priority/capability semantics, and retain passive reconciliation: no TAKE/RECOVER, heartbeat renewal or provider dispatch. Run the actual product over retained claims and seat data, then land on current main. Existing release and offline-status work retain their methods.
