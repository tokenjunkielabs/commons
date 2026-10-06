# Preserve the initiated vault-withdrawal result screen

This source-only continuation keeps the canonical lock-detail component mounted when its own confirmed withdrawal removes the selected lock. It preserves the existing loading, result, preview/live copy and explicit Done/Close flow instead of replacing them immediately with "Lock Not Found".

## Canonical source, contributor and campaign boundaries

Canonical repository: https://github.com/Stellar-PocketPay/pocketpay-mobile

Current main used for both source and the final source-ref check: `c3a24abacb45030eb4fef41aabc46b312aaf54a3`.

| Production path | Input Git blob | Proposed Git blob | Delta |
| --- | --- | --- | --- |
| `app/vault/[id].tsx` | `7347062a8a9ef442fcbd4088014fbab9fb69720d` | `719fccf291639cdfe9240d1ebf541e318b749ff1` | +11/-3 |
| `src/components/VaultLockDetail.tsx` | `0068d8745393ca1fdb08205c6dca4bc989ab38e8` | `c4598a9ffa14afd8db0ecbd58d6c37df254f17ae` | +18/-2 |

The original current-main withdrawal implementation is credited to Adeolu01's commit [840f01e09afed8809b988d711eb62161870f483e](https://github.com/Stellar-PocketPay/pocketpay-mobile/commit/840f01e09afed8809b988d711eb62161870f483e); earlier detail/education work by adnaan-id and comzzy-comzzy remains credited to those authors.

[Issue203](https://github.com/Stellar-PocketPay/pocketpay-mobile/issues/203) is OPEN and assigned to apatafamilycompound123-ops. Both current comments were read, including the actual campaign assignment. The separate existing external [PR542](https://github.com/Stellar-PocketPay/pocketpay-mobile/pull/542), by that contributor, is OPEN/unmerged at `4cd33fe253675cf23983a0151d064eb3a935a70c` on `apatafamilycompound123-ops/pocketpay-mobile`, based on the source main above. Its sole comment requests review. Its five changed paths do not change the canonical route or VaultLockDetail: they address the legacy route, shared modal/progress/hook and a workflow. This patch is against current main, not that external branch, and does not claim its authorship, approval or whole-feature completion. Its separate syntax/build and integration issues were not repaired here.

The previously completed [PR562](https://github.com/Stellar-PocketPay/pocketpay-mobile/pull/562) legacy Alert import and the existing issue223 detail feature remain separate. A precise public VaultLockDetail search returned the earlier issue223 already-implemented disposition, not this completion-order correction. The broader PocketPay/542 activity matches were unrelated numeric/hash matches; they are not evidence of a542 source completion.

## Source-supported ordering

| Input source | Exact blob | Relevant contract |
| --- | --- | --- |
| `src/store/vaultStore.ts` | `9ab36de8f91b523cd7710c90e7e802baee49e1fa` | `withdrawMaturedLock` awaits withdrawal and storage, removes the lock with `set({ locks: remainingLocks })`, refreshes the balance, then returns the result. |
| `src/hooks/useVault.ts` | `3e2b6d66c5538eb10310eae06d4df41b1b08888e` | Subscribes to the store; `findLock` searches the current lock array. |
| `src/features/vault/useMaturedLockWithdrawal.ts` | `c2c72ac69f0d75db585d1c46ff16fe9cc1d0248f` | The component-local hook sets result/success only after the awaited store method returns. |
| `src/components/MaturedLockWithdrawalModal.tsx` | `6a578419dee4ad222dea511feb734fca42713041` | Renders submitting/success/failure from the hook's step, preserves preview notices and the returned result, and dismisses through existing callbacks. |
| `docs/vault-integration-assumptions.md` | `13b91db7ddab2b751d599766c370a0f431a54037` | Documents the confirmation/loading/success/failure flow, post-withdrawal local removal and explicit placeholder boundary. |

The old route returns its missing-lock branch as soon as the store no longer contains the selected id. That removes VaultLockDetail, including the hook that is awaiting the result. The child cannot preserve its modal simply by navigating back when Done is eventually pressed, because its state-owning subtree has already been removed.

React's primary [state-preservation documentation](https://react.dev/learn/preserving-and-resetting-state) explains that component state is associated with its place in the rendered tree and is discarded when that component is removed. This is a static source inference from the actual caller/store ordering, not an observed device run.

## Correction and lifetime

- The route holds an optional lock snapshot only for its own confirmed withdrawal. It prefers a current live lock; when absent, it may use the retained snapshot only if its id still matches the route id.
- The detail component preserves the existing submitting guard, calls the optional route callback immediately before invoking `withdrawal.confirm()`, and therefore records the snapshot before the asynchronous operation can remove the lock.
- The same component remains at its existing tree position, so its local submitting/result/error state can finish through the current modal.
- On flow dismissal, the existing submitting guard remains effective, the hook closes, and the route clears its snapshot. The existing success-only `router.back()` remains.
- Confirmation cancellation happens before a snapshot is captured. Retry retains the same already-captured flow until it is dismissed; no new retry or transaction path is added.

A lock absent on initial entry, or removed before this route has confirmed a withdrawal, still uses the original missing-record UI. The snapshot is not written to the store and does not resurrect a lock for eligibility or another submission: the unchanged store still finds and validates its current record.

## Composition and limits

Apply `withdrawal-result-lifetime.patch` to the two pinned main-source files, or compose those hunks with newer source. Do not replace a newer module with a pinned postimage. Neither the legacy `app/vault-lock/[id].tsx` route nor external PR542 is modified. Completed scanner298/102, wallet refresh31806, receive QR and payment SDK442 work is outside these paths.

This correction preserves the specifically identified record-removal transition. Navigation away, component unmount, changed availability and the existing loading branch can still end the flow; persistence across those boundaries is not introduced. It adds no attempt-generation system or stronger overlapping-callback/double-submission guarantee. It does not alter eligibility, local-clock assumptions, fees, contract execution, storage, account identity, returned hashes, recovery classification or atomicity. A returned result retains the original implementation's meaning; no real withdrawal or settlement is asserted by this packet.

## Instructions and source verification

Current CONTRIBUTING.md `d8493281d318b348f98a9bd999c2ffd6cc966d0d` and retained security guidance `ea0b3c4e05d644ec10fd0de148911a74ae3031e7` apply. Retained relevant UI-state/matrix/accessibility sections were transferred without provider replay: `c53acaa9238a52c5d5517ebe39d59034af5f4c21`, `6af9f58a8bcaa1594daf396995aaa1d8dff59313`, and `965dbee318bb12b75abdd7d62f839b18ea1443d6`. They require distinct pending/success/error states, safe content preservation, truthful preview/live labels, and appropriate focus/accessibility behavior. These are requirements, not executed acceptance evidence.

Complete real source files were inspected; input/output Git-blob hashes and the literal two-file delta were checked. Infra supplied a reasoning-only assessment of the proposed snapshot/callback ordering, leading to preservation of the existing submitting guard before capture; that assessment was not runtime or full-source verification and was not an approval prerequisite.

No tests, compiler, synthetic input, app, simulator/device, storage call, SDK request, wallet operation or transaction was executed. Upstream tests/typecheck/lint/device/review/campaign requirements remain unperformed. No upstream submission, issue closure, bounty claim, acceptance or payment is represented.

The retained complete upstream tree has no LICENSE or applicable AGENTS file. Only the minimal attributed patch and this original guide are published; no full module or new license is redistributed.
