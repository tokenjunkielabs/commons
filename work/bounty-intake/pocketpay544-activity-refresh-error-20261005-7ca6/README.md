# PocketPay activity refresh error continuation

This patch repairs the history-screen integration of Binali223's existing [PocketPay mobile PR544](https://github.com/Stellar-PocketPay/pocketpay-mobile/pull/544), which implements [issue100](https://github.com/Stellar-PocketPay/pocketpay-mobile/issues/100). Issue100 remains assigned to Binali223. This is an attributed Commons source continuation, not a competing upstream submission, assignment, acceptance or reward claim.

## Pinned input and application

| Input | Identity |
| --- | --- |
| Sponsor repository | `Stellar-PocketPay/pocketpay-mobile` |
| Existing contributor branch | `Binali223/pocketpay-mobile:feat/issue-100-add-activity-refresh-error-banner` |
| Contributor head | `aa9583734f9fbc8eb7518a1e81b70d472c13b70e` |
| Sponsor base observed on that PR | `c3a24abacb45030eb4fef41aabc46b312aaf54a3` |
| Source path | `app/(tabs)/history.tsx` |
| Source Git blob before | `4b96e0a777f14b843cb76bbf8827d309ae616b66` |
| Source Git blob after | `588a009a0379f5992877a2eab2cb15649e4d880b` |

Apply `activity-refresh-error.patch` to the pinned contributor input, or port its small hunks to a newer carrier after reconciling that carrier's actual source. Do not replace a newer screen with the old donor. The production delta is +11/-4 in this one screen. The complete donor tree had 374 entries, was not truncated, and contained no license file; this packet therefore publishes only the narrow patch and this integration guide, not the complete sponsor module.

## Concrete correction

The donor store's `refreshWalletData` catches a failed refresh with existing transactions by setting `refreshError` and clearing `error`. The history header checked only `error`, so that known cached-refresh failure did not select its new banner. The screen now consumes `refreshError`, uses its presence for the cached-data banner, and includes it in the list's explicit extra data.

The donor's `fullScreenErrorTitle` style object was left unclosed, and the full-screen component referenced three absent style keys. The patch closes that object, supplies the message style using existing color/spacing tokens, and reuses the existing retry button and text styles. It does not add a new component or replace the existing retry callbacks.

The cached transactions remain the SectionList data; the no-data error still depends on `error`; the generic user-facing message remains unchanged. Filtering, pagination, wallet identity, the network-status banner, refresh calls, retry disabling and loading indicators retain their existing source behavior. No raw error string is added to the UI.

## Actual source used

| Path at the contributor head | Git blob |
| --- | --- |
| `src/store/walletStore.ts` | `f71f227f2c163ec0a3bb344583e166bea0cdf1ae` |
| `src/components/NetworkStatusBanner.tsx` | `e3b1e893eb048467fffd1c1c5f09aabc2de1067a` |
| `src/constants/theme.ts` | `cbd428b48e7fdce3e26c95ffcc4d95b25fa719a6` |
| `CONTRIBUTING.md` | `d8493281d318b348f98a9bd999c2ffd6cc966d0d` |
| `docs/screen-test-matrix.md` | `6af9f58a8bcaa1594daf396995aaa1d8dff59313` |
| `docs/ui-states.md` | `c53acaa9238a52c5d5517ebe39d59034af5f4c21` |
| `docs/accessibility.md` | `965dbee318bb12b75abdd7d62f839b18ea1443d6` |

The Activity state catalogue requires keeping loaded data usable after a failed refresh. The screen matrix names component and visual checks; the contribution guide also requires tests, type checking, linting and device/accessibility evidence before upstream UI acceptance. Those requirements remain pending. This operation did not install dependencies, execute the application, run tests, compile, typecheck, lint or use an emulator/device.

## Limits and remaining work

This correction is established by reading the actual store, caller and style definitions, with exact source/preimage accounting. It is not a successful build or a whole-PR readiness statement. Other observed donor issues are outside this one-screen delta:

- `NetworkStateBanner.tsx` passes `variant` although the imported `NetworkStatusBanner` props do not define it.
- `src/features/transactions/helpers.ts` renders literal `{asset}` in `formatTransactionAmount`; this packet does not change that separate helper or claim its consumer coverage.
- The history screen's preexisting missing-wallet early return precedes later hooks. No wallet-transition or general hook-order repair is claimed.
- Store balance semantics, concurrent refresh behavior, global accessibility compliance and the other changed PR files have not been corrected here.

No upstream branch, issue or PR was mutated. Binali223's contributor and assignment credit, maintainer review, GrantFox evaluation and any award/payment conditions remain distinct. No transaction, wallet, account, payment or chain action was performed.
