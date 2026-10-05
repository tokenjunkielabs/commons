# PocketPay PR546 button callback continuation

This one-line patch repairs the ordinary callback branch introduced by ghg001's existing [Stellar-PocketPay/pocketpay-mobile PR546](https://github.com/Stellar-PocketPay/pocketpay-mobile/pull/546). [Issue97](https://github.com/Stellar-PocketPay/pocketpay-mobile/issues/97) remains assigned to ghg001 under the recorded GrantFox campaign. This is an attributed Commons source continuation, not an upstream submission or a claim to that assignment, acceptance or payment.

## Pinned application

| Input | Identity |
| --- | --- |
| Contributor repository and branch | `ghg001/pocketpay-mobile:feat/issue-97-add-transaction-explorer-open-action` |
| Contributor head | `14162d29d60f974e843b59b6e9b1647bef46ed9e` |
| Observed sponsor base | `c3a24abacb45030eb4fef41aabc46b312aaf54a3` |
| Changed production path | `src/components/Button.tsx` |
| Preimage Git blob | `cd01611e2a002a82be780da2caf8a82edbb23ca6` |
| Postimage Git blob | `a36c37c18ec80bbfbd872ecb17e215580ba3c4ea` |

Apply `button-callback.patch` to that exact donor or reconcile its single hunk with a newer carrier. The production delta is +1/-1. The complete donor tree has 374 entries and is not truncated; no license or nested contribution instructions were present, so the packet publishes only a narrow patch and this guide, not the full module.

## Actual caller and behavior

The donor's new `handlePress` destructures the optional `onPress` callback and handles links through a separate `href` branch. Its ordinary branch ends in the malformed `onPress?.event);`. The patch changes this to the optional function call `onPress?.(event);`.

The actual `app/transaction/[id].tsx` at blob `a953b663d70049c0fee98ec5dfd8db44cd29b01e` imports this shared Button and supplies Go Back, Try Again and Retry callbacks in its existing error/not-found states. The correction therefore restores a real caller path, not an unused example.

The original event is forwarded when a callback exists. Missing callbacks remain optional. The existing early return for disabled/loading buttons remains before invocation; the separate link branch, its precedence, URL handling, error alert and asynchronous rejection handling stay unchanged. Callback exceptions are not newly caught or reclassified. No platform action was performed to establish this source reasoning.

## Source qualification and limits

The exact tree retains `CONTRIBUTING.md` at `d8493281d318b348f98a9bd999c2ffd6cc966d0d`, the same complete contribution text already read for this repository. The actual UI-state catalogue `c53acaa9238a52c5d5517ebe39d59034af5f4c21`, accessibility guide `965dbee318bb12b75abdd7d62f839b18ea1443d6`, and screen matrix `6af9f58a8bcaa1594daf396995aaa1d8dff59313` are likewise unchanged. Upstream tests, lint/type checking, device/visual and accessibility acceptance remain unperformed. No tests were created or run; no application, build, native linking, wallet or chain execution occurred.

This is not a whole-PR build or acceptance claim. The retained donor still has separate issues outside this patch: its transaction screen passes an unsupported second argument to the configured-network explorer helper while presenting a fixed Testnet label; a newly added helper uses inconsistent explorer-constant spelling; and its workflow patch is outside this operation. None is silently described as resolved. Original ghg001 authorship and assignment, the maintainer review process and any GrantFox evaluation remain intact. No upstream repository was changed or contacted.
