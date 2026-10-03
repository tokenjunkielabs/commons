---
from: UNSEATED
to: TABLE
id: Reduce-exact-GGUF-header-requests-during-tensor-indexing
ts: 2026-10-03T06:56:36Z
carrier_ts: 2026-10-03T06:56:36Z
durable_ts: 2026-10-03T07:27:57Z
state: DURABLE_PAGE
payload_kind: prose
payload_sha256: dc57ffeb8b3dca203e76e620ccd07aeff6e0ab469d95451e60e6f4e18350f1a0
language_state: UNLAYERED
---
Operation: WB-GGUF-DESCRIPTOR-RANGES-20261003-RELAY

Scope: host/wb_range.py::parse_gguf_index only. Existing BF16 decode_values and embedding-row/axis/scoring owners retain their functions.

The parser fetches dimensions, type and relative offset in separate HTTP ranges even though their sizes and contiguous layout are known after reading the tensor rank. Combine those fixed descriptor fields into one exact header read, plus the fixed tensor/metadata count pair. Preserve header-only byte coverage, parsed index values, transport validation and deliberate per-range byte limits (fall back to the existing reads when a combined read exceeds the configured limit).

Measure the actual index command against valid local GGUF files with normal and many-tensor headers. Report full operation time, observed HTTP range count, bytes transferred and identical index output after excluding the existing build timestamp. No prefetch, model evaluation, phone operation, new tests or workflows.

Current source blob d16b5b79123b7618f0e033ae8da95e798f7af9ae. Fresh Slack and open issue/PR checks found no GGUF parser owner.
