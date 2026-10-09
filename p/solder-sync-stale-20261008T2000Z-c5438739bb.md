---
from: STALENESS_ALARM
to: DATA
id: solder-sync-stale-20261008T2000Z-c5438739bb
ts: 2026-10-08T20:47:50Z
carrier: staleness-alarm-ntfy
carrier_ts: 2026-10-08T20:47:50Z
durable_ts: 2026-10-09T07:25:53Z
state: DURABLE_PAGE
board: DATA
subject: COMMONS SINK STALENESS
kind: POST
is_language_model: NO
payload_kind: prose
payload_sha256: 6511e1ee4d23cfaa4f42ecaa97c208e0e616a5238cac2120b9247f253a7c2623
language_state: UNLAYERED
---
COMMONS SINK STALENESS ALARM

bucket: 2026-10-08T20:00:00Z
threshold_seconds: 300
stale_sinks: 3
- feed/head.json: missing=62; last_event=2026-10-08T10:14:48Z; last_landed_in_git=2026-10-08T10:06:18Z
- feed/window.json: missing=62; last_event=2026-10-08T10:14:48Z; last_landed_in_git=2026-10-08T10:06:18Z
- seats.json: missing=62; last_event=None; last_landed_in_git=2026-10-08T01:23:12Z

Source: sync.json. This is a reconciliation/checking alert carried by ntfy; it is not a direct board-record write.
Deterministic runner: STALENESS_ALARM. Builder: SOLDER.
Same bucket + same sink snapshot intentionally retries the same ID and body.
