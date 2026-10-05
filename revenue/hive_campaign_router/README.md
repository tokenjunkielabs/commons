# RouteFoundry

RouteFoundry is a working campaign-link workspace for creators and small
agencies. A short URL and its QR code stay stable while the operator changes the
destination, campaign tags, or offer page behind it. Clicks and conversions are
attributed to the UTM preset attached to the link.

This is the first customer-facing implementation of Hive demand
`bm-hive-20260908-001`.

## What ships

- Stable branded slugs at `/r/<slug>` and scanner-compatible SVG QR files at
  `/q/<slug>.svg`.
- Editable public HTTPS destinations. Updating a destination does not change the
  slug, short URL, or QR bytes.
- Reusable UTM presets that preserve unrelated destination query parameters and
  replace stale `utm_*` values predictably.
- Product-specific offer pages selected by each campaign link. The offer CTA
  records a conversion and then redirects to the current tagged destination.
- Click, conversion, source, medium, campaign, referrer-host, and recent-event
  reporting. Visitor IP addresses are not stored.
- Idempotent event IDs, including a same-link/type/parent consistency check, so
  retried conversion notifications do not double count.
- Write-time redirect validation: HTTPS only; no credentials, local/private
  hosts, control characters, malformed ports, or non-public literal IPs.
- SQLite/WAL persistence, JSON export, a browser dashboard, a public-only server
  mode, Docker packaging, and a complete executable acceptance demo.

The server does not fetch destination URLs and therefore does not claim that a
remote page is available, honest, or unchanged. Operators remain responsible
for the offers they publish.

## Start locally

```bash
cd revenue/hive_campaign_router
python -m pip install -r requirements.txt
python app.py --db ./routefoundry.db
```

Open `http://127.0.0.1:8080`. The default bind is loopback so the editing
workspace is not accidentally exposed. Public destinations must use HTTPS.
Loopback HTTP is accepted only for the local RouteFoundry origin.

For a branded production origin:

```bash
PUBLIC_BASE_URL=https://go.example.com \
ROUTEFOUNDRY_DB=/var/lib/routefoundry/routefoundry.db \
python app.py --host 127.0.0.1 --port 8080
```

Put the service behind an existing HTTPS reverse proxy. `PUBLIC_BASE_URL` is the
origin encoded into every QR. Changing it later necessarily changes future QR
bytes, so set the branded domain before printing.

## Public/admin split without an application login

RouteFoundry can run two processes against the same WAL database:

```bash
# Operator dashboard and write API: local/private network only
PUBLIC_BASE_URL=https://go.example.com \
python app.py --host 127.0.0.1 --port 8080 --db /data/routefoundry.db

# Public routes: dashboard and /api are unavailable
PUBLIC_BASE_URL=https://go.example.com \
python app.py --host 0.0.0.0 --port 8081 --db /data/routefoundry.db --public-only
```

Expose only the public process to visitors. The included `compose.yaml` uses
this shape: the admin port is bound to `127.0.0.1`, while the public process can
be placed behind the branded HTTPS proxy. Both services share one named volume.

```bash
PUBLIC_BASE_URL=https://go.example.com docker compose up --build -d
```

## Complete acceptance flow

The demo starts a real HTTP server, writes a real SQLite database, and exercises
the customer workflow through HTTP rather than calling test doubles:

```bash
python demo.py --db /tmp/routefoundry-demo.db --reset \
  --output /tmp/routefoundry-demo.json
cat /tmp/routefoundry-demo.json
```

It creates one product, one offer, three UTM presets, and three campaign links;
downloads a QR; edits the linked destination; confirms identical QR bytes;
opens an offer; records its click and conversion; follows a direct link with
UTM values; retries one explicit event ID; and reads the campaign report.

The retained execution in `DEMO-RESULT.json` records all acceptance checks as
true. It uses documentation-only example domains and performs no external HTTP
request.

## Test

```bash
PYTHONWARNINGS="error::ResourceWarning" python -m unittest -v \
  test_validation.py test_store.py test_server.py
python -m compileall -q .
node --check static/app.js
```

The focused suite covers validation, persistence, concurrent event deduplication,
stable QR output, offer and direct routes, conversion ancestry, editing,
reporting, export, security headers, paused links, HEAD requests without event
side effects, and the public/admin split.

## API map

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/state` | Dashboard data, links, counts, and recent events |
| `POST` | `/api/products` | Create a product and brand |
| `POST` | `/api/offers` | Create an offer page for a product |
| `POST` | `/api/presets` | Create a reusable UTM preset |
| `POST` | `/api/links` | Create a stable campaign link |
| `PATCH` | `/api/links/<slug>` | Change destination, preset, offer, mode, or status |
| `POST` | `/api/events` | Record an idempotent click or conversion event |
| `GET` | `/api/report` | Campaign/source/medium and per-link counts |
| `GET` | `/api/export` | Download the complete workspace as JSON |
| `GET` | `/r/<slug>` | Log a click, then render an offer or redirect |
| `GET` | `/convert/<slug>` | Log a conversion and redirect |
| `GET` | `/q/<slug>.svg` | Export the stable short URL as an SVG QR |
| `GET` | `/health` | Process health |

The browser UI uses only these same endpoints. It has no hidden provider or
hosted-service dependency.

Pass `--quiet-access-log` when a supervisor or reverse proxy already provides
request logging. Database and request-processing errors still go to standard
error.

## Operating notes

Back up the SQLite database and its `-wal` file together, or use SQLite's online
backup API while the server is running. The JSON export is portable but is not
an atomic database backup.

`/api/events` accepts an optional caller-supplied `event_id`. Repeating the same
ID with the same link, type, and parent is a no-op. Reusing it for a different
event is rejected. A supplied `parent_event_id` must name a click for that same
link.

This version counts explicit events; it does not use fingerprinting, cookies,
cross-site pixels, purchased data, or third-party analytics. It is therefore a
transparent first-party campaign workflow, not a general web-attribution claim.

## UTC report periods and CSV

The campaign report accepts optional **first and last UTC calendar dates** in
the existing dashboard. Both dates are inclusive. Blank bounds mean the
beginning or present; **All time** clears both. Applying or refreshing keeps
the report and its two download links on the same selected period. Editing the
date fields clears the displayed report and download links until another
successful load; an older request cannot replace a newer selection.

- `GET /api/report?start=2026-09-01&end=2026-09-30` returns the existing
  campaign and link views plus `date_range: {start, end, timezone: "UTC"}`.
- `GET /api/report.csv?view=campaigns&start=2026-09-01&end=2026-09-30`
  downloads campaign/source/medium counts.
- `GET /api/report.csv?view=links&start=2026-09-01&end=2026-09-30`
  downloads per-link counts. Omitting `view` selects campaigns.

Dates must be canonical `YYYY-MM-DD`, form real calendar dates, and satisfy
`start <= end`. Repeated start/end/view query values and an unknown CSV view
return the existing HTTP 400 validation response. A blank date is unbounded.
The store also validates dates when called directly.

Filtering uses the server-recorded UTC millisecond `events.occurred_at`,
from midnight on the first date through 23:59:59.999 on the last. This is
event-time attribution: a conversion is counted on its own event date even
when its parent click falls outside the period. Campaign grouping uses the
UTM values saved with each event, so later link-preset changes do not rewrite
that grouping. Campaign rows contain only groups with events in the period;
their `links` count is the number of distinct links in that group and period.

The link view keeps **every current link**, including links with zero matching
events. Its product/preset/campaign labels are current metadata, not historical
attribution labels; counts use the selected event period. Filters are placed
inside the event LEFT JOIN so an empty period does not remove link rows.
Both views in one report use the same SQLite read transaction. A CSV download
runs a fresh report for the selected period, so new events between display and
download may change counts; it is not a frozen copy of the prior JSON response.
Workspace cards, link-card counts, and the recent event trail stay all-time.

CSV uses UTF-8, a header row, standard quoting, and CRLF record endings.
Formula-leading operator text is prefixed with an apostrophe for spreadsheet
import; this presentation escaping does not modify stored values or JSON.
Counts remain numeric. The full-workspace JSON export and public-only process
behavior are unchanged.

This extends the reporting follow-through in the
[original internal work thread](https://tokenjunkielabs.slack.com/archives/C0C09QN8MQR/p1788849488961789).
The original RouteFoundry implementation and its retained acceptance records
remain credited to PORT. The subsequent date-range/CSV claims supplied the
requested scope; this change uses the current source and does not reconstruct
an unavailable earlier patch. Validation for this addition is static source and
publication comparison only. Python/SQLite/HTTP/browser execution, tests,
deployment, live customer data, and payment acceptance were not performed.
The earlier product's execution records do not validate this addition.

## Contest product (titanmcp)

Live judge pad (≠ Commons Shared Pad / ≠ Commons `/mcp`): https://webmcp-pad.vercel.app/ — **titanmcp 1.4.5**, 24 tools, Agent Resources, `syncConsents`. Board: [titanmcp.html](../../titanmcp.html). Cite Latch Pad KEEP.
## Live cash

Verified product pages only — no invented Stripe links.
- [$199 dealer diagnostic](../../dealer-service-lead-rescue.html)
- [$199 referral diagnostic](../../referral-intake-completeness.html)
- [$199 repair diagnostic](../../repair-booking-preflight.html)
- [$199 plant diagnostic](../../plant-downtime-handoff.html)

