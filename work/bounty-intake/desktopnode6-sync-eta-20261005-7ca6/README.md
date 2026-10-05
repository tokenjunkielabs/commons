# Desktop-node sync-time estimate

The current [issue 6](https://github.com/kryptokrona/desktop-node/issues/6) asks for the remaining synchronization time in hh:mm. This source packet adds a labelled estimate below the existing Sync card, using the local height and network height already supplied by the existing getinfo poller. It does not request any additional node endpoint.

## Exact source and result

All source is based on upstream main `b9e38b0592c4a99db33f16c07741641c63f6d730`, tree `8910dc11b3b9927af694fe2181bcff7388b64ddf`.

| Path or source | Original Git blob | Result Git blob |
| --- | --- | --- |
| `src/lib/store.js` | `27f06c22db934a63249654db583e8e4a80651516` | `8e6bac57153ab06da0dfab88b2861cccd4e57acf` |
| `src/routes/dashboard.svelte` | `39b97713b7449f9357fd9729e3c7bb3466df210f` | `90f15bbb8944547aa2666521d490f8a9df7698e5` |
| Upstream README | `29e88d1fc3861279515397e75d52cdbd40a09e8a` | unchanged upstream |
| Upstream package | `1706b6f052e95fae2ce1cdd633524e3c9fe93695` | unchanged upstream |

The complete original producer and dashboard were transferred from the source scout and independently matched to their native Git blob identities before editing. The prepared producer is 2,969 bytes and dashboard is 4,468 bytes. `change.patch` is `ff8556f2dc43cff6d11d6f6274fa5cb5e1fb61ba`, 3,688 bytes, four hunks and +66/-5 across the two production files. Its serialized context and removals were checked against the complete original texts, and reconstruction reproduced both complete postimages exactly. This was text comparison, not execution of the application or estimator.

## Estimate and state transitions

The old producer polls every 5,000 ms and immediately places a successful JSON response in the node store. The old dashboard displays a percentage or “Synced”; it has no duration estimate. A timer's requested interval does not establish actual elapsed processing time.

The new `syncRemainingMinutes` store starts as null. After a complete, accepted response body is available, the producer takes `performance.now()` and associates that receipt time with the same response's local height, target height and start_time value. Only nonnegative safe-integer local heights and strictly larger safe-integer network heights are eligible, with `synced === false`.

An estimate requires a previous eligible sample, positive observed height progress, positive elapsed receipt time, a nondecreasing target height, and unchanged start_time. The remaining target height is divided by the observed block-processing rate, then rounded up to whole minutes. Only a finite positive safe-integer result is displayed. Hours have at least two digits and are not wrapped at 24; minutes have two digits. Before usable samples exist, the card says “Estimated remaining: Estimating...”.

A first sample, stalled or regressing progress, target regression, changed start_time, invalid observation or completed/error response clears the displayed estimate as appropriate. A valid stalled or regressing observation becomes the next baseline; an invalid observation or request error discards the baseline. start_time is used only for equality as a conservative reset signal; no timestamp units, elapsed duration or block rate are inferred from it. Hashrate is not used.

Each request receives a sequence number. Successful responses and errors advance the same last-settled sequence. An older result cannot overwrite node data or restore an estimate after a newer success or error. An accepted HTTP/network/JSON error clears the baseline and estimate and logs the existing no-data message with the error. The existing supply request expression and five-second interval remain byte-identical; supply fetching now follows a handled getinfo error as well. Supply errors remain outside this catch.

This is a linear estimate from the last two accepted local observations. It is not a predicted deadline, a measured node-internal processing rate, or a guarantee of synchronization completion. Network delay, processing variation and target growth can change it. The value is not a countdown; it remains the latest estimate between responses. No new timeout, smoothing model, background-job cancellation or freshness deadline is introduced. A request that remains pending indefinitely does not itself clear the last estimate.

## Existing integration limitation

The complete pinned dashboard imports and calls `resetStore`, while the complete pinned store exports no such function. This preexisting mismatch is preserved and explicitly prevents claiming a buildable or accepted full integration here. The patch adds no guessed replacement/reset API. The dashboard's existing one-million network-height loading threshold, stop/restart behavior, supply logic and all styling remain unchanged apart from the new text below the Sync card.

The package declares Svelte 3.49, SvelteKit next.372 and Electron 19. No Svelte compiler, Electron process, native node, localhost request, chain connection, browser, test, lint, build, workflow, account, wallet or synthetic sample was run. Only source authoring, identity calculation, patch reconstruction and connected publication/readback were performed.

A single direct open of `https://developer.mozilla.org/en-US/docs/Web/API/Performance/now` returned ServerError (`turn1632view0`). That exact route is held, with no alternate or retry. No successful independent documentation read is asserted for that method.

## Source, attribution and license

Original application authors, including Swepool, retain credit. Changed source sections carry a 2026-10-05 modification notice. The complete upstream README declares “GPL-3.0 License.” Observed complete root, src, routes and lib directory listings contain no AGENTS.md or contribution-instruction file; the root has no separate LICENSE file. This is coverage of those observed ancestor directories, not a whole-repository policy census.

`LICENSE` carries the complete GNU GPL version 3 text unchanged, Git blob `e142a525bd3fcc4eb1964d6b6b9a0434eee11d89`, 34,470 bytes. The text was copied from the already identified immutable Commons license asset at `f55eb766a83d054681131d9de8e2376710364283/contributions/retroshare-adapter-error-cleanup/LICENSES/GPL-3.0-or-later.txt`; its identity was checked during this packet's acquisition. That donor filename does not expand the upstream project's GPL-3.0 declaration into an independently asserted “or later” election. The license text and original attribution accompany the complete source postimages and patch.

## Issue chronology and limits

All five reported issue comments were returned. Member Swepool [offered 10,000 XKR in August 2022](https://github.com/kryptokrona/desktop-node/issues/6#issuecomment-1222125298) and [specified hh:mm in August 2023](https://github.com/kryptokrona/desktop-node/issues/6#issuecomment-1693178924). A contributor subsequently asked whether the offer remained active and posted /attempt; the complete discussion contains no later sponsor answer. This packet does not assume a renewed offer, USD value, paid assignment, escrow or payout.

The issue is open and unassigned. A bounded all-state own-PR query and a term-limited external PR query for syncing each returned zero results with incomplete_results false. The latter is not a complete external-PR census. A precise public activity search returned no hit, also without proving universal absence.

Internal activity `1791204299.882799` records this exact two-file scope. Its complete readback matched after the one observed ordinary issue-URL wrapper and provider attribution footer. No sponsor contact, external claim, upstream mutation, duplicate PR, account operation, deployment, bounty completion or payment assertion is made. Future authorized integration must start from the pinned preimages and address the independently disclosed build limitation with actual source evidence.
