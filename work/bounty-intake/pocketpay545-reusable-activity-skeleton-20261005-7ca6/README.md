# PocketPay PR545 reusable activity skeleton

This attributed continuation repairs the reusable component/export path in ghg001's existing [Stellar-PocketPay/pocketpay-mobile PR545](https://github.com/Stellar-PocketPay/pocketpay-mobile/pull/545), addressing [issue99](https://github.com/Stellar-PocketPay/pocketpay-mobile/issues/99). The issue remains assigned to ghg001 under its recorded GrantFox campaign. No external branch or submission is replaced.

## Apply to the actual contributor source

Contributor repository: `ghg001/pocketpay-mobile`  
Branch: `feat/issue-99-add-activity-list-skeleton-loading-state`  
Head: `a5a4f1cd306748a0bd178eef8adb3f20322fbde5`  
Observed sponsor base: `c3a24abacb45030eb4fef41aabc46b312aaf54a3`

Apply `reusable-activity-skeleton.patch` to that pinned input, or reconcile its three source hunks with a newer carrier. Do not overwrite newer history-screen work. In particular, the separate PR544 refresh-error continuation in Commons31735 is based on another contributor branch and must be composed by its actual hunks.

| Production path | Before Git blob | After Git blob |
| --- | --- | --- |
| `app/(tabs)/history.tsx` | `b96464448f3524ce0507b29882103544bdf1ea45` | `f9096d48b2fdfb0460ca307dcc2b2d0e9314e094` |
| `src/components/ActivitySkeleton.tsx` | `0f5fe5febea4dd205cf44a7c11140564c9765857` | `cc474d4e04aecc545f0ff6e3f4091e2e0836230f` |
| `src/components/index.ts` | `b053ef65be5a4382f1bb6849971016d5c783025d` | `da5e36536f810cc011077e1c4b65bead704d1ad4` |

Production delta: +67/-57 across these three existing paths. The packet contains only this guide and the narrow patch; the complete donor tree had 375 entries, was not truncated, and exposed no license file or nested instruction file.

## Concrete source correction

The actual history screen already implemented six neutral skeleton rows inline. In contrast, the reusable `ActivitySkeleton.tsx` was only a one-line re-export of `./ActivityListSkeleton`; that module is absent from the complete pinned tree. The component barrel also contained seven malformed `etport` tokens, including an export from that absent module.

This patch moves the retained inline implementation and its styles into the existing `ActivitySkeleton.tsx`. It uses the documented `useTheme`/`useMemo` pattern, keeps the same six rows, colors, spacing, shapes and 60%/40% line widths, and represents the prior 40/12 dimensions with the existing equivalent size tokens. The screen imports this actual component and no longer carries a duplicate implementation or its styles.

The repaired barrel restores the six unrelated export statements and exports both `ActivitySkeleton` and its existing intended barrel name `ActivityListSkeleton` from the real component. It does not add or reconstruct an `ActivityListSkeleton.tsx` file.

The component groups the neutral placeholders as a progress indicator labelled “Loading activity” with a busy state. No fake transaction text or values are introduced. The existing `isLoading && transactions.length === 0` condition, cached-data refresh indicator, list rendering, filters, pagination and empty-state branch remain unchanged. No timer, shimmer or network request is added.

## Source boundaries and acceptance

The direct request for `src/components/ActivityListSkeleton.tsx` at the pinned head returned typed 404 NOT_FOUND. That exact request remains held; it was not retried or recovered through another content route. The already-required complete tree supplied independent path metadata. The new implementation comes from the complete existing history screen, not presumed missing-module bytes. The one-line alias preimage is complete in the native PR patch and independently matches its reported Git blob.

The pinned tree preserves the already-read `CONTRIBUTING.md` (`d8493281d318b348f98a9bd999c2ffd6cc966d0d`), UI-state catalogue (`c53acaa9238a52c5d5517ebe39d59034af5f4c21`), accessibility guide (`965dbee318bb12b75abdd7d62f839b18ea1443d6`) and screen matrix (`6af9f58a8bcaa1594daf396995aaa1d8dff59313`). The design-system guide (`a94ed602b3cd9d2c88dc3366bddf83c6c8dcf994`) was read for this extraction; the actual size/color tokens are `cbd428b48e7fdce3e26c95ffcc4d95b25fa719a6`.

The patch was checked as text against the three real preimages and reconstructs the recorded postimages exactly. No TypeScript compilation, lint, installation, application run, tests, device or screen-reader operation occurred. Those upstream contribution and acceptance requirements remain pending. Existing missing-wallet hook ordering and general failed-fetch presentation are outside this correction; the donor workflow change is untouched. No whole-PR readiness, visual equivalence on a device, shimmer animation or global accessibility compliance is claimed.

Original author/assignment credit, maintainer review and any GrantFox award/payment conditions remain separate. No upstream comment, claim, source mutation, wallet/account, chain or payment action was performed.
