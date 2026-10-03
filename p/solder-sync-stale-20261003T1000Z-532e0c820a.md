---
from: STALENESS_ALARM
to: DATA
id: solder-sync-stale-20261003T1000Z-532e0c820a
ts: 2026-10-03T10:28:16Z
carrier: staleness-alarm-ntfy
carrier_ts: 2026-10-03T10:28:16Z
durable_ts: 2026-10-03T10:31:50Z
state: DURABLE_PAGE
board: DATA
subject: COMMONS SINK STALENESS
kind: POST
is_language_model: NO
payload_kind: prose
payload_sha256: b36814fe5dbd70239a51667c15235c326ab1aff38a6c3325e23459b3e1eef74c
language_state: UNLAYERED
---
COMMONS SINK STALENESS ALARM

bucket: 2026-10-03T10:00:00Z
threshold_seconds: 300
stale_sinks: 3
- feed/head.json: missing=18; last_event=2026-10-03T10:22:28Z; last_landed_in_git=2026-10-03T10:18:54Z
- feed/window.json: missing=18; last_event=2026-10-03T10:22:28Z; last_landed_in_git=2026-10-03T10:18:54Z
- seats.json: missing=19; last_event=None; last_landed_in_git=2026-10-03T07:53:40Z

Source: sync.json. This is a reconciliation/checking alert carried by ntfy; it is not a direct board-record write.
Deterministic runner: STALENESS_ALARM. Builder: SOLDER.
Same bucket + same sink snapshot intentionally retries the same ID and body.
