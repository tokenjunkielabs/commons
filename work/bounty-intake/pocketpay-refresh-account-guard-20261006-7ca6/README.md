# Ignore wallet refresh results after an account change

This source-only continuation prevents a refresh that captured account A from writing its success or error state after the store has been cleared or now identifies a different account B. It also clears the refresh loading flag when wallet state is reset or a persisted replacement wallet is installed.

## Source and ownership

- Canonical repository: https://github.com/Stellar-PocketPay/pocketpay-mobile
- Current main inspected for this work: `c3a24abacb45030eb4fef41aabc46b312aaf54a3`.
- Production path: `src/store/walletStore.ts`.
- Exact input blob: `6ee485a9c9d2ffe3bb80b1e70c4bf720fcfbec81`.
- Exact proposed output blob: `1074e1f229cdc32b3fcd7cf3854f10c9a97872b3`.
- Production delta: +4/-1, four hunks. Only the patch and this guide are distributed.

The existing balance-state feature belongs to payfoxX's merged https://github.com/Stellar-PocketPay/pocketpay-mobile/pull/377 (head `b47669829ca563c8565211b4fe55df962d31cfc2`, merge `187eea6f3866efcc2e9ff0a9e0a7a25f817289e6`). Issue https://github.com/Stellar-PocketPay/pocketpay-mobile/issues/329 is closed. Current issue metadata lists payfoxX; its historical assignment-bot comment names Myart352. Those are distinct observations, not a reassignment by this packet. Existing store contributions, including khalifa-zoro and cLamberti, remain attributed to their authors. This packet does not claim the original balance feature or their payment rights.

A precise PR-body search for `refreshWalletData` returned only closed PR377 and PR75 (the latter describes previous store correctness and tests). A precise public activity search returned no messages. These bounded results do not establish a complete repository-wide contribution census. No old tests or accepted behavior were rerun.

## Actual caller and state evidence

| Input | Immutable identity | Relevant behavior |
| --- | --- | --- |
| `app/(tabs)/index.tsx` | `73f21ce04ee5b19c9b61e51ac9fa5e05450da7f5` | Mount and Retry/pull-to-refresh call `refreshWalletData`; UI consumes its balance, history, error, and loading state. |
| `app/(tabs)/settings.tsx` | `0295e4c93d564ff44adfb7391fe0bc02c09eaf09` | Retained exact reset handler awaits `clearWallet()`, then closes its modal and reports a failed clear. There is no refresh-loading check in this handler. Root's About continuation leaves this block unchanged. |
| `src/store/walletStore.ts` | input above | Refresh captures `publicKey`, awaits balance and history together, then formerly committed success or catch state unconditionally. Successful clear resets the key to null; successful set installs the supplied key. |

The source-supported sequence is a home refresh followed by a successful Settings reset before that refresh settles. The late success formerly repopulated the cleared store, and the late failure could set its balance state and error. The same unconditional write also applied when the store instead contained a different public key. No device or network sequence was executed.

## Correction

After the awaited balance/history results, compare the current store public key with the captured one before reconciling pending transactions or writing state. The catch branch performs the same comparison before logging or changing error/loading state. If the identity differs, return without touching the current account's refresh state.

The comparison and subsequent state construction contain no additional await. Existing pending transactions are still read after the fetch, preserving the existing optimistic-entry behavior for the account that remains current. Successful current-account balance, history, pagination, timestamp and funding-state updates retain their prior logic.

`resetWalletState()` now includes `isLoading: false`. Successful `setWallet()` also explicitly resets this flag. Therefore discarding an obsolete completion does not leave the previous account's spinner latched after these actual reset/replacement paths. SecureStore and AsyncStorage operations, their ordering, failure messages and return values are unchanged.

## Composition

Apply `refresh-account-guard.patch` only to the pinned source or manually compose its four hunks with newer source. Do not overwrite a newer store with this pinned postimage. Commons https://github.com/woahwhattheheck/commons/pull/31758 already carries a separate functional-update correction inside `loadMoreTransactions`; preserve it. This patch does not touch that method, payment submission, the SDK442 work, the completed receive QR work, or the import copy/cancel/progress patches.

## Explicit limits

- Identity here is the public-key value, not an invocation generation. Clearing and reinstalling the same key before a prior request settles is not detected. Nor are overlapping refreshes of the same key ordered by this change.
- This is not cancellation: obsolete network requests still settle. No request, SecureStore write, account operation, or payment is aborted or rolled back.
- Pagination, funding checks, Friendbot flows, storage operations and other async methods are not given new account-generation protection.
- Other pre-existing account-reset fields and initialization/concurrency behavior are not redesigned. This packet makes no general wallet-race, atomic-state, authorization or isolation guarantee.
- Upstream's contributor, test, typecheck, lint, device, review and campaign acceptance requirements remain outstanding. This is not an upstream-ready acceptance report and makes no bounty or payment claim.

## Source verification and distribution

The complete real store and home caller were read; the Settings handler was transferred from already retained source with its exact path and blob. The store preimage and constructed postimage were independently Git-blob hashed; the literal four-hunk delta was inspected. The canonical main remained at the recorded source pin. No app, TypeScript compiler, parser fixture, Jest suite, SDK request, storage call, wallet action or device was run.

Applicable upstream CONTRIBUTING.md is `d8493281d318b348f98a9bd999c2ffd6cc966d0d`; the retained security guide is `ea0b3c4e05d644ec10fd0de148911a74ae3031e7`. The complete retained source tree contains no LICENSE or applicable AGENTS file. This packet therefore publishes a minimal attributed patch and original guide, not a full source-module copy or a newly asserted license. External source, assignment and acceptance conditions remain unchanged.
