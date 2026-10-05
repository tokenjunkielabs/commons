# Faucet node status: preserve observed disconnects

## Change and origin

This packet continues [TrickBaker's external faucet pull request 6](https://github.com/kryptokrona/kryptokrona-faucet/pull/6), pinned to head `60ae3176529b6e084aab4d0386a2ddb9d68d1fc5`. That contribution already adds node details to the status route and a 503 response when wallet/status collection fails. The original node-status feature and its error-handling work belong to that author.

The additional patch prevents positive, cached daemon heights from overriding a disconnect observed through the SDK's public events. It changes only two hunks in `wallet.js`: **7 added lines and 2 removed lines**. It attaches connection listeners immediately after constructing the daemon, derives the existing connected result from both its height check and the observed connection state, and requires that connected result before reporting synced.

[Issue 5](https://github.com/kryptokrona/kryptokrona-faucet/issues/5) requests node connection information; [issue 2](https://github.com/kryptokrona/kryptokrona-faucet/issues/2) requests improved error handling. Both remained open in the observed records, with one historical comment each. The member offers in comments [1222122746](https://github.com/kryptokrona/kryptokrona-faucet/issues/5#issuecomment-1222122746) and [1222123199](https://github.com/kryptokrona/kryptokrona-faucet/issues/2#issuecomment-1222123199) date to August 22, 2022. They do not establish current funding, assignment, payment eligibility or issue completion. No upstream claim or submission is made here.

## Source evidence

| Source | Immutable identity | What was used |
| --- | --- | --- |
| Faucet PR 6 head | `60ae3176529b6e084aab4d0386a2ddb9d68d1fc5` | Actual external contribution and two changed paths |
| Faucet `wallet.js` preimage | `d144bcc157a15e4468bf02d808674c9fd0fcede9` | Complete 5,183-byte source retained for exact patch application |
| Faucet `wallet.js` postimage | `d34e9f23adc5fa96c23f45f854e6d8382ac74866` | 5,390 bytes; represented by the patch, not copied as a complete module |
| Faucet `routes/status.js` | `1e56bba7a9c45fb17c326e02082e72338ea40958` | Existing concurrent status collection, normal node response and 503 catch |
| Faucet `package.json` | `4a3773ea2f805cccbbeef50bfc7c6bdde282551b` | Declares `kryptokrona-wallet-backend-js: ^2.4.1` |
| SDK source commit | `d32d582101307ff9b68812d7b8d572bfb3e71b4a` | Canonical repository's observed source |
| SDK `package.json` | `afaf901942463eb9c711bf1c11bec82640456102` | Version 2.6.1, within the declared faucet dependency range |
| SDK `lib/Daemon.ts` | `868203bfb517961b70d2d8e59661332af9383647` | Constructor, connection transitions, request failure paths, cached-height getters and refresh method |
| SDK `lib/IDaemon.ts` | `90cfcbbf7819787193943aab87ffc765541ec437` | Complete public interface, including connect/disconnect events |

The source package has no observed lockfile, and no installed or deployed dependency version was acquired. The SDK evidence is specifically version 2.6.1 within the requested range; it is not a statement about a running faucet's actual package resolution. Selected relevant sections of the complete SDK source were inspected; this is not a review of every SDK function.

Primary source links:

- [Pinned faucet wallet](https://github.com/kryptokrona/kryptokrona-faucet/blob/60ae3176529b6e084aab4d0386a2ddb9d68d1fc5/wallet.js)
- [Pinned status route](https://github.com/kryptokrona/kryptokrona-faucet/blob/60ae3176529b6e084aab4d0386a2ddb9d68d1fc5/routes/status.js)
- [Pinned SDK daemon implementation](https://github.com/kryptokrona/kryptokrona-wallet-backend-js/blob/d32d582101307ff9b68812d7b8d572bfb3e71b4a/lib/Daemon.ts)
- [Pinned SDK interface](https://github.com/kryptokrona/kryptokrona-wallet-backend-js/blob/d32d582101307ff9b68812d7b8d572bfb3e71b4a/lib/IDaemon.ts)
- [Pinned SDK package metadata](https://github.com/kryptokrona/kryptokrona-wallet-backend-js/blob/d32d582101307ff9b68812d7b8d572bfb3e71b4a/package.json)

## Why the original condition can be wrong

In the inspected SDK, `updateDaemonInfo()` catches a failed information request and returns without clearing the last successful local or network heights. The faucet's outer catch therefore need not run. Its original condition checks whether either cached height is positive, which can continue to yield true after contact has failed.

The SDK records the failed request through a public `disconnect` event and a later successful reconnection through `connect`. Its initial internal connection flag is true specifically so that an initial failed contact emits a disconnect. The constructor itself performs configuration without starting a request. Registering listeners directly after construction therefore precedes wallet startup and later refresh requests.

The patch records those transitions in a local boolean. While the last observed transition is a disconnect, both connected and synced are false even when cached heights remain positive. A connect event clears that disconnection state. The original positive-height requirement remains, including its behavior when both heights are zero.

The change does not access the SDK's private connection field, infer connection from endpoint metadata, introduce another request, or add polling. The event state is shared daemon contact state; it is not a per-request freshness timestamp or a guarantee that cached height data is current. Heights and blocksBehind remain available as the original cached values.

## Resulting boundary

The original status route still returns its normal response when node information reports disconnected, and retains the original 503 behavior for exceptions from the combined status collection. This packet does not turn a disconnected-node result into a new HTTP error.

The transaction route, payout ordering, wallet initialization, persistence callbacks, balance handling and address validation are unchanged. The actual SDK address validator returns a boolean; no change to that existing call is warranted by this review. Broader persistence and retry semantics require a separate transaction design and are not claimed by this status correction.

This delta is based on PR 6. The distinct failover contribution in PR 7 and its earlier Commons continuation are not replayed or claimed as included.

## Artifact and validation

`node-disconnect.patch` is an ordinary unified diff against the exact PR 6 wallet preimage above. The serialized patch itself was parsed, its two hunk positions/counts and every context/removal row were checked against the complete retained preimage, and its resulting full text matched the stated postimage. Independent Git blob calculations matched the original native source identity and the prepared artifact identities.

No application, wallet, daemon, RPC, transaction, dependency install, test suite, workflow, browser session or runtime acceptance check was executed. Static source reasoning and exact artifact checks support this delivery. In particular, no live outage, reconnect, synchronization or payment outcome is claimed.

A fresh PR record retained the same external head and zero comments/reviews. The narrow Commons PR query returned no matches. The code query returned no matches with `incomplete_results: true`; it is not an exhaustive absence result. The exact public Slack query returned an empty bounded rendering and provider end, without proof that its query was applied. These observations are coordination evidence only.

## Attribution and redistribution scope

The faucet package metadata declares ISC, while its pinned README describes GPL 3. The complete 21-entry source tree had no standalone license file or additional contribution instructions. This packet records that conflict without supplying a license grant or choosing between the declarations. It contains the focused patch and this guide only; it does not republish the complete wallet module or unrelated embedded configuration. The SDK's AGPL 3 declaration is recorded as source provenance; its implementation is linked and described, not copied into this packet.

The external author retains credit for PR 6. This Commons continuation is not upstream acceptance, completion of either whole issue, a bounty claim, or evidence of payment.
