# Smart Gas Price: complete wait labels and guarded quote fallback

This attributed source continuation repairs the wait-label formatter and malformed/rejected quote fallback requested by [DigixGlobal/governance-ui issue 44](https://github.com/DigixGlobal/governance-ui/issues/44). It is a Commons source packet, not an upstream submission or a deployed wallet change.

## Original implementation and provenance

The issue requires API wait values in minutes to be displayed as hours, minutes and seconds. Its explicit examples include 0.4 minutes as 24 seconds, 1.3 minutes as 1 minute 18 seconds, and 61.5 minutes as 1 hour 1 minute 30 seconds. The current formatter returns fractional minutes below an hour and discards the minute/second remainder above an hour.

The original work by eswarasai was merged in [governance-ui PR 46](https://github.com/DigixGlobal/governance-ui/pull/46) and [governance-ui-components PR 381](https://github.com/DigixGlobal/governance-ui-components/pull/381). Their merge commits are 75cf0108f46ec998ffd7a83fc86d5c1e2e3e471b and 58eaef3c1cc695a61d7fce7221d0eb6fa70040cb. The issue's historical payment/completion comments remain historical; this packet makes no current funding or compensation claim.

The complete issue, all 25 issue comments, both linked PR descriptions, the two PR46 comments and PR381's changed-path list were read. Current component develop was observed at b53a48ceed76c1fc4d2d78fcfd7d7d0058a3f9b4. The gas-price file remains the same blob carried by PR381. The current open-PR list returned three records (421, 426 and 427), none describing this formatter. A bounded public activity search for the exact phrase "Smart Gas Price" returned no records; this is not a repository-wide absence proof.

## Exact source scope

| Item | Immutable identity |
| --- | --- |
| Components source commit | b53a48ceed76c1fc4d2d78fcfd7d7d0058a3f9b4 |
| Original gas-price/index.js | e8cc4a4a629faf1593ad0c502e4170012429fb07 |
| Complete corrected source | dab3a7e12b8a19657a01f472dd55146242b782e1 |
| Exact unified patch | 1ee60d16ab681bf2c97ae3b07a1c506c9513b1ef |
| Original BSD license, copied unchanged | bc5b09893d1f96880d32a85ad83b89443cff385a |
| Actual governance-ui caller commit | 912b4d10ec3e1ebdb1165d164c31183788fec15c |
| Complete transaction_signing_overlay.jsx caller | 2a2bf0e737133811cac2dc7ebd95c3ee3fa185f3 |

The original path is src/components/common/blocks/gas-price/index.js. The packet contains its complete postimage at source/src/components/common/blocks/gas-price/index.js plus change.patch and LICENSE.md. The source still requires its original package, React, dependencies and relative aliases; the packet is not a standalone runnable application.

The formatter change was first published independently in [Commons PR31628](https://github.com/woahwhattheheck/commons/pull/31628), merge 3b38bebe730b691c48d771a51abe74b416299bf2, source c42c4bd6b84c87b8e540ebdeaff56610bb520295. It rounds total minutes to the nearest whole second once, then derives hours, minutes and seconds from that same integer total. It emits the nonzero units in order, with a zero-second fallback when the duration is zero. A single second uses the singular label. This follow-through preserves that function exactly. The intended domain is a finite nonnegative wait estimate, not a forecast guarantee.

The separate quote follow-through changes component lifecycle and quote-result application in the same source file. The original code divided the unvalidated fast field by ten and selected the fast card even for missing/null fields. Its rejected-fetch handler only logged. That did not implement the issue's explicit fallback: no selected quote option and a synchronized 10 gwei slider/gas price.

The component actually renders all four prices (average, fast, fastest, safeLow) and their four waits (avgWait, fastWait, fastestWait, safeLowWait). All eight must now be finite nonnegative JSON numbers before the response is applied. Missing fields, nulls, strings, negative or nonfinite values use fallback; no coercion or min/max clamp is added. Zero remains accepted. Successful complete quotes retain the original fast/10 conversion and card behavior. This is a numeric field-shape check, not evidence that a quotation is current, economically appropriate or within every downstream numerical limit.

An unsuccessful HTTP response, JSON rejection or fetch rejection uses the same 10 gwei fallback. Fallback opens the slider view, leaves all quote options deselected, updates the displayed value and notifies the existing onGasPriceChange callback after state commits. The current constants file has a separate global DEFAULT_GAS_PRICE of 25 gwei; it is unchanged. The fallback remains the explicitly requested 10 gwei, not a new global fee policy.

Both explicit selection handlers synchronously record that a user has selected a value before their existing state/callback work. Quote application checks mounted/no-selection state at entry, inside its functional setState updater and again before notifying the parent. Thus a pending result is not allowed to overwrite an explicit slider/option choice; unmount prevents later quote state/callback application. The network request itself is not aborted or retried. An indefinitely pending request does not settle into fallback, and this patch does not add a loading/signing gate or change the initial interval before settlement/user input.

The fast default and /10 unit conversion for valid quotes, manual selection values, slider limits, fee arithmetic, API endpoint, actual parent callback implementation, signing and broadcasting are preserved. The complete caller was read to bind the production use: it imports this GasPrice component, supplies gas and onGasPriceChange, and uses its gasPrice state in newTxData. Its transaction controls were not changed.

Two additional complete dependency leaves at the same component commit bind this follow-through: the Slider wrapper (a73619507b37703c57dd28fe98bbdf8b90ea1f2b) forwards all props to rc-slider unchanged, and constants.js (2a633db4ec9a531cf637aaaaf839cd4aa11fa4b7) defines the issue's API endpoint and the separate global default. Neither file is copied or edited in this packet.

## Source-only evidence and limits

The actual complete preimage was independently identified using Git blob hashing. The formatter replacement and subsequent lifecycle/quote block replacement preserve all source bytes outside those two regions. The cumulative two-hunk patch was reconciled with the same original complete preimage and final postimage; the standalone formatter from PR31628 is unchanged. Mounted/selection guards and callback ordering were inspected statically. These are source/custody checks, not execution of the formatter, component, event ordering or application.

No test, fixture, package installation, build, browser, wallet, gas API call, RPC, transaction, signing, deployment or hosted workflow was performed. The original author's historical wallet checks were not repeated and do not validate this new postimage. The issue's examples above are requested behavior, not newly executed outputs.

The current component README, full BSD license, root listing and .github PR template were read. No root AGENTS.md or CONTRIBUTING file appeared in that listing. The README links a contribution wiki; the direct wiki read and the related governance-ui Contribution-Guide read both returned DisabledError and remain unacquired, without retry or alternate access. This licensed Commons artifact is not represented as satisfying an unacquired upstream submission policy. Preserve the copied license and original authors when integrating it.

The first PR31628 guide correctly recorded malformed/rejected quote handling as unmodified. This distinct follow-through addresses that retained source concern; it does not retroactively claim that the first formatter-only source fixed it. It makes no whole-feature, current gas-provider availability, browser compatibility, runtime race, signing safety, deployment or upstream acceptance claim.

Original operation: DIGIX44-WAIT-FORMAT-20261005-7CA6. Original activity: https://tokenjunkielabs.slack.com/archives/C0BS7AZ4BSL/p1791209468287449 . The independent follow-through is DIGIX44-QUOTE-FALLBACK-20261005-7CA6, reply1791210504.332619 in that same thread. Its stable branch is work/governance44-quote-fallback-20261005-7ca6.
