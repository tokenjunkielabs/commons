# Counterfactual Commons / BRAMBLE

A real local workspace for synthetic continuity experiments. Inspect evidence,
change working records, record notes, exercise instruments, preserve a checkpoint,
and resume from a different client. The operator chooses the investigation; there
is no saved model-decision script, next-step scheduler, or compulsory route.

## Run

Python 3.10 or later; no third-party dependencies. From the repository root:

```sh
python host/counterfactual_lab/lab.py --db counterfactual.sqlite3
```

Open `http://127.0.0.1:8765`. From the standalone package directory, `python lab.py`
works too. Keep the same database path on restart. Ctrl+C stops the server without
deleting workspaces. `--port` selects another port. The server binds to loopback
by default; `--host` can change that for an explicitly chosen shared environment.
It is a development/research HTTP server, not a public production service. There
are no accounts or admission checks. All effect operations change **only the
synthetic SQLite workspace**: no mail, deployment, payment, provider login, or
external customer action is connected.

A second browser or HTTP client pointed at this same server sees the same state.
Use Refresh to recover updates from another client. Across separate machines,
export and import a bundle to create a labeled fork; that is not shared live
synchronization. Import never overwrites an existing workspace.

## Four incidents

- A primary connector has a transient failure while a separate CLI really is
  unconfigured. Determine the states independently and exercise the primary road.
- An older instruction resurfaces in a newer peer quotation. Scope, source kind,
  timestamps, and explicit supersession remain inspectable.
- An old handoff says a delivery is pending; the remote ledger contains its
  receipt. Additional deliveries remain visible even after the report is fixed.
- A submission receipt and approved artifact disagree, or agree in the second
  variation. Confirmation and artifact equality are separate observations.

Each incident has two **disclosed** variations. They are synthetic fixtures, not
blinded held-out cases or verbatim reconstructions of private conversations.
Fixture timestamps are fictional. A source identifier is scoped by the case ID
and variant; the bundle also preserves document bytes, their hashes, author,
source kind, scope, and supersession. Existing Commons source-linked experience
packets inspired the evidence representation; this package does not invoke the
experience procedure compiler or amend existing skills/policies.

## Instruments and API

The UI and JSON API operate on one store. JSON responses report actual effects,
revisions, and errors. GET `/api/cases` lists incidents; GET `/api/runs` lists saved
workspaces. POST `/api/runs` with `{"case_id":"duplicate-handoff","variant":0}`
creates one. GET `/api/runs/<id>` retrieves it.

POST `/api/runs/<id>` accepts an operation, object-valued `args`, an optional
expected `revision`, and an optional idempotency `request_id`. For example:

```json
{"operation":"inspect","args":{"id":"remote-ledger"},"revision":0,"request_id":"my-inspection-1"}
```

The operations are independent instruments, not steps to execute in this order:

| Operation | Arguments / mechanical effect |
| --- | --- |
| `inspect` | `id`: return the full source record |
| `write` | Merge the supplied object into the working record |
| `probe` | `surface`: `primary`, `secondary`, or another named surface; return the synthetic observation |
| `effect` | Nonempty `kind`, plus fields: append a synthetic effect |
| `note` | `text`, optional `sources` array of document IDs |
| `checkpoint` | Same fields; also preserve a snapshot of the working record |
| `request_human` | Same fields; record a request, but do not contact anyone |
| `record_usage` | Optional nonnegative `tokens`, `elapsed_seconds`; explicitly unverified operator report |
| `evaluate` | Return outcome predicates, including irreversibly recorded duplicate/wrong effects |

Task-relevant effect kinds are `publish` (with `release`), `delivery` (with `job`),
and `replace_artifact`. Other effect kinds are recorded, but the evaluator does
not pretend they have modeled real-world consequences. Results, not one preferred
investigation sequence, determine task success. Tests intentionally exercise bad
actions to calibrate the scorer; those tests are not delivered as agent routines.

SQLite transactions preserve concurrent events. Supplying a stale revision
returns HTTP 409 rather than clobbering newer state. Repeating the **same**
`request_id`, operation, and arguments returns the original receipt without
applying a second effect; reuse with different arguments returns 409. After an
ambiguous HTTP failure, API clients should retry the same request ID. The UI
Refresh button reveals persisted state; inspect it before choosing to issue a
new effect after a network error.

GET `/api/runs/<id>/export` returns a JSON envelope containing the full case,
working state, event chain, and recomputed outcome. POST that envelope to
`/api/import` to create a new fork. The UI supports both. A SHA-256 checksum catches
accidental bundle damage; event hashes expose uncorrected history edits. **Neither
is an authenticity signature or proof that an imported operator was truthful.**
Imported data is labeled untrusted and never executes code. This version checks
fixture bytes and event-chain integrity; it does not prove the final state was
derived honestly by an external exporter. Retain the original source version
with evidence. Requests/imports are limited to 1 MB; this is a small-case lab.

## Validation and evidence

From the repository root:

```sh
python -m unittest -v test_counterfactual_lab.py
```

Or from this package directory: `python -m unittest -v test_lab.py`.
33 tests cover all eight good and eight wrong fixture outcomes, strict value
types, source integrity, real HTTP operations, persistence across clients,
concurrent writes, stale revisions, request deduplication, export/import forks,
and malformed/tampered input. Subcases are included within the 33 tests.

The accompanying `evidence/interaction.json` records an actual browser-UI to HTTP
client continuation, then a deliberately duplicated delivery that fails even
though the written report stays correct. Both clients were driven by BRAMBLE;
**no independent second peer or comparative model experiment is claimed**.
The source-linked workspace is implemented; superiority over a conventional
summary remains unmeasured. Unknown token use, human corrections, and elapsed
model time are null rather than invented. Reported resource numbers are labeled
operator-reported, not provider-metered.

Browser validation used Chromium DOM interaction with a bridge to the real
running local HTTP backend because native browser navigation to loopback was
blocked by the test environment. It was not canned-response testing, but it is
not evidence of native browser HTTP navigation in that environment. JavaScript
reported no errors and a 390-pixel viewport had no horizontal overflow. Normal
native navigation is covered by the dated restoration below. Independent
cross-harness experiments remain unmeasured. This bounded release does not claim
to complete the full three-condition research study.

### Native UI restoration (2026-10-03)

The unrelated product retirement in [#15784](https://github.com/woahwhattheheck/commons/pull/15784)
removed the empty `cases`, `task`, `identity`, and `documents` containers
used by this page's renderer. Native Chromium navigation to the original
Python/SQLite server reproduced an empty incident chooser and
`Cannot read properties of null (reading 'append')`, while the server returned
all four incidents. Restoring those four containers from the original
[#8756](https://github.com/woahwhattheheck/commons/pull/8756) markup repairs the
chooser and workspace view. The inline JavaScript, backend, source fixtures,
and original evidence bytes are unchanged; the retired product stays retired.

Actual native loopback navigation in Chromium 153 then exercised the disclosed
Quartz tool-failure workspace. Source inspection, the existing two transient
primary observations followed by a successful read, the separate unconfigured
secondary surface, record writing, linked notes, checkpoint, and outcome
evaluation all persisted. A second native browser client resumed the same
workspace and added a note visible on reload. At 390 pixels the page's measured
width was exactly 390 pixels, with all four incident buttons and five source
documents present. Desktop and phone views were visually inspected.

The UI's 13,620-byte JSON download remained byte-identical after closing and
restarting both Chromium and the Python server with the same SQLite path
(SHA-256 `a454269a0cd7061ec4b9ddf5c94297623d17d9e3ed008d61817146add0821f0a`).
Import through the file input created a separate labeled fork with the working
record, notes, checkpoint, and prior events preserved; the original export was
unchanged. Importing both retained snapshots from `evidence/interaction.json`
also preserved their original outcomes: one delivery succeeded, while the
duplicate-delivery snapshot failed with one duplicate even though its record
remained correct. Four workspaces were retained in the local store.

The observation recorded 34 browser HTTP requests, no JavaScript or console
errors, and no external requests. Both browser clients were operated by the
same assistant. These are native UI and persistence observations of the existing
synthetic instrument; independent peer comparison and resource savings remain
`NOT_MEASURED`. No new tests or evidence artifacts are added to the repository.

## Continuation

A continuing peer, a replacement with a conventional summary, and a replacement
with the source-linked workspace can use these instruments without rewriting the
application. Record exact model/harness and evidence exposure in run metadata;
match tasks and resource budgets, and retain actual exported outcomes. In this
version experimental conditions are descriptive metadata, not enforced blinding
or automatic context construction. Source and exports expose the oracle, so a
future held-out comparison must address contamination explicitly. Do not infer
model superiority from unit tests or a self-authored demonstration.

## Live cash

Verified product pages only — no invented Stripe links.

- [$199 dealer diagnostic](../../dealer-service-lead-rescue.html)
- [$199 referral diagnostic](../../referral-intake-completeness.html)
- [$199 repair diagnostic](../../repair-booking-preflight.html)
- [$199 plant diagnostic](../../plant-downtime-handoff.html)

## Contest product (titanmcp)

Live judge pad (≠ Commons Shared Pad / ≠ Commons `/mcp`): https://webmcp-pad.vercel.app/ — **titanmcp 1.4.5**, 24 tools, Agent Resources, `syncConsents`. Board: [titanmcp.html](../../titanmcp.html). Cite Latch Pad KEEP. Submit/YouTube wait Bryce exact go.
