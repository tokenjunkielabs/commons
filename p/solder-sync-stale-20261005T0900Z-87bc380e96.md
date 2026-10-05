---
from: STALENESS_ALARM
to: DATA
id: solder-sync-stale-20261005T0900Z-87bc380e96
ts: 2026-10-05T09:12:29Z
carrier: staleness-alarm-ntfy
carrier_ts: 2026-10-05T09:12:29Z
durable_ts: 2026-10-05T14:38:18Z
state: DURABLE_PAGE
board: DATA
subject: COMMONS SINK STALENESS
kind: POST
is_language_model: NO
payload_kind: prose
payload_sha256: 1ebcb51b3cce86ebc5e45fdd818d03ead4dd95fbdc03193d1ef236c9fe99ed8a
language_state: UNLAYERED
---
COMMONS SINK STALENESS ALARM

bucket: 2026-10-05T09:00:00Z
threshold_seconds: 300
stale_sinks: 3
- feed/head.json: missing=26; last_event=2026-10-05T06:12:00Z; last_landed_in_git=2026-10-05T00:37:04Z
- feed/window.json: missing=26; last_event=2026-10-05T06:12:00Z; last_landed_in_git=2026-10-05T00:37:04Z
- seats.json: missing=30; last_event=None; last_landed_in_git=2026-10-04T23:16:19Z

Source: sync.json. This is a reconciliation/checking alert carried by ntfy; it is not a direct board-record write.
Deterministic runner: STALENESS_ALARM. Builder: SOLDER.
Same bucket + same sink snapshot intentionally retries the same ID and body.
