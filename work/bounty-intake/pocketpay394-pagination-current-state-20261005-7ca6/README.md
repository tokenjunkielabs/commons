# PocketPay history pagination: preserve current records

This packet corrects one current-state integration defect found while qualifying [PocketPay issue394](https://github.com/Stellar-PocketPay/pocketpay-mobile/issues/394). It is a bounded source continuation, not completion of that broad normalization/filter/detail/status-refresh request.

## Pinned source and application

| Input | Identity |
| --- | --- |
| Sponsor repository | `Stellar-PocketPay/pocketpay-mobile` |
| Current main | `c3a24abacb45030eb4fef41aabc46b312aaf54a3` |
| Source path | `src/store/walletStore.ts` |
| Preimage Git blob | `6ee485a9c9d2ffe3bb80b1e70c4bf720fcfbec81` |
| Postimage Git blob | `4cfc670785416f08ccdec8202aaad1701243375e` |
| Production delta | +24/-12 |

Apply `pagination-current-state.patch` to this exact source, or port its `loadMoreTransactions` hunk after reading a newer carrier. The same whole source blob was independently returned at the already existing [PR547](https://github.com/Stellar-PocketPay/pocketpay-mobile/pull/547), `tokenjunkielabs/pocketpay-mobile:main` head `c80c00a1b4c7926c8b8d0b32845ffd9c3ee0f685`. That is compatibility evidence for this leaf, not a new acceptance result for PR547.

The main tree had 374 entries, was not truncated, and exposed the existing contribution guide but no license file. This packet contains a narrow patch and integration guide, not a complete sponsor module.

## Actual defect and correction

The previous `loadMoreTransactions` destructured `transactions` before awaiting `fetchTransactionsPage`. Its eventual setter then replaced the visible list with that old array plus the returned page. The real `addPendingTransaction` action independently prepends a new record through a functional setter, so an entry added while the page request is pending could disappear when pagination completed. A concurrently updated record could likewise be replaced by its earlier object.

The patch removes the pre-await list snapshot. Inside the completion's functional setter, it builds the existing-ID set from `state.transactions` and appends new page records to that same current list. Existing records keep their current object values and order; the page's new records retain their original order. The request arguments, page size, network call count, returned cursor and `hasMore` behavior stay unchanged.

Both success and error updates first compare the current public key, cursor and loading flag with the in-flight request's observed values. A response does not write into a visibly different wallet, reset cursor or no-longer-loading pagination state. Returning the current state leaves the replacement operation's state untouched.

## Real producer and consumer evidence

| Source at the main pin | Git blob | Relevant behavior |
| --- | --- | --- |
| `app/review-transaction.tsx` | `2ae491e16b271a0564576d615cf765188678335b` | Calls `addPendingTransaction(result.hash, { id: result.hash, ... })` after its existing send path returns. |
| `src/store/walletStore.ts` | `6ee485a9c9d2ffe3bb80b1e70c4bf720fcfbec81` | Prepends optimistic records with `status: 'pending'`; pagination previously overwrote a captured list. |
| `app/(tabs)/history.tsx` | `052c0da3373ea7d7d91ddcaf19c3cee34de44cc4` | Uses the store list, recognizes pending status, routes each row by ID and invokes older-page loading. |
| `src/services/stellar.ts` | `3cbe4124bbefb3f7a6539fdaef2502f84921715f` | Returns the requested page, cursor and continuation flag. |
| `src/components/TransactionListItem.tsx` | `6672b248a4c96b3460b4aefd1c821f5bbd082b4f` | Displays the existing pending/confirmed/failed status field. |

The separate detail/status mismatch initially found under issue394 is already the subject of PR547/issue322. Its completed resolver/hash-refresh work is preserved, with tokenjunkielabs and the original contributors credited; this packet does not recreate it. Existing PocketPay544/545/546/548 continuations also remain separate.

## Bounds and remaining work

This is static source reasoning and exact patch accounting. No application, function, numeric example, synthetic response, test, device, signing, wallet, account, network request to a chain or transaction was executed.

The guards are comparisons of existing state, not a request-generation mechanism. They do not distinguish an old request from a newer one if the wallet, cursor and loading flag have all returned to the same values. They do not cancel requests, serialize full refreshes, repair all wallet-switch lifecycle state, reconcile transaction hashes with operation IDs, deduplicate repeated IDs inside one returned page or provide snapshot pagination. In particular, `refreshWalletData` and wallet reset behavior are unchanged. No general race-free or atomic-booking claim is made.

Issue394 remains broader: unknown-state modeling, normalization across all sources and full UI acceptance are not completed here. The repository's `CONTRIBUTING.md` at `d8493281d318b348f98a9bd999c2ffd6cc966d0d` still requires upstream tests/typecheck/lint and UI/device evidence; those checks remain unperformed. Existing baseline source/type diagnostics are not asserted resolved.

PR547's sole current comment reports the existing auto-merge dispatch HTTP401 credential failure. This source patch cannot repair it, and its credential/workflow routes were not retried. Neither the external branch nor issue/PR was mutated. Original authorship, assignment, review, GrantFox evaluation and any award/payment conditions remain distinct.
