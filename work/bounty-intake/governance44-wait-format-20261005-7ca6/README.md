# Smart Gas Price: retain the complete wait duration

This attributed source continuation repairs the wait-label formatter requested by [DigixGlobal/governance-ui issue 44](https://github.com/DigixGlobal/governance-ui/issues/44). It is a Commons source packet, not an upstream submission or a deployed wallet change.

## Original implementation and provenance

The issue requires API wait values in minutes to be displayed as hours, minutes and seconds. Its explicit examples include 0.4 minutes as 24 seconds, 1.3 minutes as 1 minute 18 seconds, and 61.5 minutes as 1 hour 1 minute 30 seconds. The current formatter returns fractional minutes below an hour and discards the minute/second remainder above an hour.

The original work by eswarasai was merged in [governance-ui PR 46](https://github.com/DigixGlobal/governance-ui/pull/46) and [governance-ui-components PR 381](https://github.com/DigixGlobal/governance-ui-components/pull/381). Their merge commits are 75cf0108f46ec998ffd7a83fc86d5c1e2e3e471b and 58eaef3c1cc695a61d7fce7221d0eb6fa70040cb. The issue's historical payment/completion comments remain historical; this packet makes no current funding or compensation claim.

The complete issue, all 25 issue comments, both linked PR descriptions, the two PR46 comments and PR381's changed-path list were read. Current component develop was observed at b53a48ceed76c1fc4d2d78fcfd7d7d0058a3f9b4. The gas-price file remains the same blob carried by PR381. The current open-PR list returned three records (421, 426 and 427), none describing this formatter. A bounded public activity search for the exact phrase "Smart Gas Price" returned no records; this is not a repository-wide absence proof.

## Exact source scope

| Item | Immutable identity |
| --- | --- |
| Components source commit | b53a48ceed76c1fc4d2d78fcfd7d7d0058a3f9b4 |
| Original gas-price/index.js | e8cc4a4a629faf1593ad0c502e4170012429fb07 |
| Complete corrected source | c42c4bd6b84c87b8e540ebdeaff56610bb520295 |
| Exact unified patch | fb77da038c69a258cdc852fee74448a5e19912cc |
| Original BSD license, copied unchanged | bc5b09893d1f96880d32a85ad83b89443cff385a |
| Actual governance-ui caller commit | 912b4d10ec3e1ebdb1165d164c31183788fec15c |
| Complete transaction_signing_overlay.jsx caller | 2a2bf0e737133811cac2dc7ebd95c3ee3fa185f3 |

The original path is src/components/common/blocks/gas-price/index.js. The packet contains its complete postimage at source/src/components/common/blocks/gas-price/index.js plus change.patch and LICENSE.md. The source still requires its original package, React, dependencies and relative aliases; the packet is not a standalone runnable application.

Only formatTime changes. It rounds total minutes to the nearest whole second once, then derives hours, minutes and seconds from that same integer total. It emits the nonzero units in order, with a zero-second fallback when the duration is zero. A single second uses the singular label. The intended domain is a finite nonnegative wait estimate, not a forecast guarantee. No new validation or fallback for malformed provider values is introduced; in particular, invalid values are not deliberately converted into a reassuring zero estimate.

Gas selection, the fast default, slider behavior, fee arithmetic, the API endpoint and fetch behavior, the parent callback, signing and broadcasting are outside the changed function and retain their original bytes. The complete caller was read to bind the production use: it imports this GasPrice component and supplies gas and onGasPriceChange. Its transaction controls were not changed.

## Source-only evidence and limits

The actual complete preimage was independently identified using Git blob hashing. The exact function replacement preserves the entire source prefix and suffix. The patch text was reconciled with that same complete preimage and postimage. These are source/custody checks, not execution of the formatter or application.

No test, fixture, package installation, build, browser, wallet, gas API call, RPC, transaction, signing, deployment or hosted workflow was performed. The original author's historical wallet checks were not repeated and do not validate this new postimage. The issue's examples above are requested behavior, not newly executed outputs.

The current component README, full BSD license, root listing and .github PR template were read. No root AGENTS.md or CONTRIBUTING file appeared in that listing. The README links a contribution wiki; the direct wiki read and the related governance-ui Contribution-Guide read both returned DisabledError and remain unacquired, without retry or alternate access. This licensed Commons artifact is not represented as satisfying an unacquired upstream submission policy. Preserve the copied license and original authors when integrating it.

A separate existing source concern remains outside this display-only patch: the successful JSON callback does not validate missing/null gas quote fields before dividing fast by ten, and the rejected-fetch callback only logs. This packet does not claim to repair fallback synchronization, asynchronous request ordering, provider compatibility or the whole Smart Gas Price feature.

Operation: DIGIX44-WAIT-FORMAT-20261005-7CA6. Original activity: https://tokenjunkielabs.slack.com/archives/C0BS7AZ4BSL/p1791209468287449 . Stable branch: work/governance44-wait-format-20261005-7ca6.
