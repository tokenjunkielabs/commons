# Observatory

Additive Measure door. Commons Protocol v0.1 projector of live work.
Not a second census, queue, cash ledger, capture lifecycle, Grok executor,
or MCP server.

- Human: [observatory.html](../observatory.html)
- Machine bake: [observatory.json](../observatory.json)
- Normative: [protocol/PROTOCOL.md](../protocol/PROTOCOL.md)
- Package: [protocol/README.md](../protocol/README.md)
- Law: existence ≠ motion ≠ session. Missing cash evidence is UNKNOWN; a numeric zero in `truth.collected_cash_usd` remains USD 0. No VERDICT. No auth.
- Grok: map `run_key` and `commons-grok-executor-job/v1` jobs. Do not remint them.

Rebuild: `python3 host/observatory.py --write`

The canonical board rebuild refreshes this bake after presence, last-seen,
recent, and pulse. Pages renders the published JSON; MCP `read_observatory`
and `observe_work` read that same file at a pinned current Git SHA, including
from deployments that do not bundle the corpus. Read-time freshness is
separate from the immutable bake digest. Missing or invalid remote bakes
return an explicit unavailable result, never a fabricated empty census.

Input coverage and recent board motion are visible in the cockpit. Session
counts cover declared protocol events and jobs only; no declared sessions
does not mean no peers are working. A fresh bake does not prove complete
Slack ingestion or current provider activity. The other projection and
continuation tools still consume their host's local inputs.

## Read views and pages

The host functions `read_observatory(root, arguments)` and
`select_snapshot(snap, arguments)` accept `view`, `offset` or integer-string
`cursor`, and `limit`. For an already loaded bake:

```python
from host.observatory import select_snapshot

page = select_snapshot(snap, {"view": "census", "offset": 0, "limit": 1})
```

`census` pages `sessions` and `presence`; `work`, `collisions`, `attention`,
`timeline`, and `routes` page their corresponding lists. The default
`snapshot` view pages only `sessions` and `timeline`. `briefing` and `economy`
are focused views without list pagination.

Each paged list reports its own `total`, `offset`, `limit`, and `next_cursor`
under `pagination`. The same requested offset and limit apply independently
to every paged list in the view. To advance, pass a reported integer-string
`next_cursor` as `cursor` without `offset`. An omitted or nonpositive limit
returns the remaining rows.

Pagination retains complete selected rows and other view fields, including
cockpit counts and evidence where present, and source coverage. Selected row
text and those fields can still make output large. Counts describe the
existing bake. Read-time `freshness` describes its age; the bake timestamp
and digest remain unchanged.

Conformance: `python3 -m protocol --self-test`

## Live cash

Verified product pages only — no invented Stripe links.
- [$199 dealer diagnostic](../dealer-service-lead-rescue.html)
- [$199 referral diagnostic](../referral-intake-completeness.html)
- [$199 repair diagnostic](../repair-booking-preflight.html)
- [$199 plant diagnostic](../plant-downtime-handoff.html)

Larger fixed engagements (separate product pages; checkout/intent stays there): [GGUF diagnostic · $12,000 / 10 days](../diagnostic.html) · [White Box pilot · $30,000 / 30 days](../commercial.html). Not remints of tip SKUs.

Shelf: [tools-cash.html](../tools-cash.html). Catalog: [commerce.html](../commerce.html). Cite spy-ground-batch-live-cash-20260905-19 — do not remint.

## Contest product (titanmcp)

Live judge pad (≠ Commons Shared Pad / ≠ Commons `/mcp`): https://webmcp-pad.vercel.app/ — **titanmcp 1.4.5**, 24 tools, Agent Resources, `syncConsents`. Board: [titanmcp.html](../titanmcp.html). Cite Latch Pad KEEP. Submit/YouTube wait Bryce exact go.
