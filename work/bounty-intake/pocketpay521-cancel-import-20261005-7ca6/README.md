# PocketPay import cancellation

The current import screen has no explicit cancellation action, although the existing recovery component already supports a cancelled state. This patch connects that state to a Cancel Import button before importing starts. It clears the entered secret and transient errors, then offers the existing create-wallet route or a fresh empty import form.

This is a source-only continuation for [Stellar-PocketPay/pocketpay-mobile issue 521](https://github.com/Stellar-PocketPay/pocketpay-mobile/issues/521). It does not complete all of that issue's error-state and acceptance requirements.

## Apply and compose

Apply `change.patch` to `app/(auth)/import.tsx` at main commit `c3a24abacb45030eb4fef41aabc46b312aaf54a3`, original blob `38a3f75f9aafb94084456110853457f792f2aab3`. The production delta is +50/-6. Inspect newer changes and compose these hunks instead of replacing a newer whole screen.

The source belongs to the PocketPay contributors. Existing merged import-validation work from martinshub-tech (PR450) and onboarding-recovery work from Favouratambi (PR416) remain credited. The separate Sol-ImportShield-2112 activity at Slack message `1791162732.454539` remains an independent issue-wide contribution; its bounded thread had no carrier reply. This packet does not take over that activity, claim a bounty, or mutate any upstream or contributor branch.

The full observed 374-entry sponsor tree was not truncated and contained no LICENSE/COPYING file. This packet therefore contains an original narrow patch and integration guidance, not a redistributed complete source module or an inferred project license.

## Behavior and boundary

- Before an import begins, Cancel Import clears the masked input and local validation/recovery errors, then renders the existing `WalletEmptyState variant="cancelled"`.
- Import Existing Wallet starts over with an empty field. Create New Wallet navigates to the already-existing `/(auth)/create` route.
- A synchronous ref records when the import/save sequence starts, and the Cancel handler reads that ref. The button also becomes visibly and semantically disabled while importing. The ref and display state clear in `finally`, including failed saves.
- No cancel handler calls the SDK, the wallet store, SecureStore, a network service, or a signing/transaction API.
- Cancellation is unavailable during import/save. The existing secure-store API has no abort or rollback contract; this patch does not claim to cancel a write already in progress.
- The cancelled message describes this attempt only. It deliberately does not assert that an earlier failed persistence attempt changed nothing on the device.
- Existing validation, successful persistence, storage errors, root navigation, and other error recovery remain in place. This does not intercept navigation back gestures or add a cross-screen cancellation protocol.
- Duplicate-wallet behavior is not changed. The actual root layout redirects a loaded wallet away from auth; the missing duplicate check in this screen alone was not enough to establish an ordinary reachable duplicate-import defect.

The existing `AsyncActionButton` supplies the button role, visible-label accessibility label, disabled/busy state, and 56dp target. The new supporting action uses its outline variant and existing `SIZES.sm` spacing. Its hint explains why cancellation is unavailable while saving. Device layout, focus, large-text behavior and screen-reader transitions have not been exercised.

## Actual source contract inspected

All pins below are at the sponsor commit above.

| Source | Blob | Relevant contract |
| --- | --- | --- |
| `app/(auth)/import.tsx` | `38a3f75f9aafb94084456110853457f792f2aab3` | Existing validation, local state and import/save sequence |
| `src/components/WalletEmptyState.tsx` | `53b024e09ed8021f3f474186dce0f0140ffb27b3` | Cancelled variant, subtitle and create/import callbacks |
| `src/components/AsyncActionButton.tsx` | `1044f1c9154a43524165d4d4d5a7fdc784cbb7b0` | Existing accessible disabled/busy button and invocation handling |
| `src/store/walletStore.ts` | `6ee485a9c9d2ffe3bb80b1e70c4bf720fcfbec81` | Awaited SecureStore write; boolean save result; no abort API |
| `src/sdk-stub/index.js` | `ec02c486d040a884f86bc69aa637cb68ad9056e3` | Actual local synchronous key derivation used by package dependency |
| `app/_layout.tsx` | `7b6a2916cd9a897b87577d0584a6cc536458eae0` | Loaded-wallet redirect from auth |
| `app/(auth)/_layout.tsx` | `8b81fa1ea9dc527224734c768807b882dbfeaafc` | Existing import/create routes |
| `CONTRIBUTING.md` | `d8493281d318b348f98a9bd999c2ffd6cc966d0d` | Upstream contribution and acceptance expectations |
| `docs/security.md` | `ea0b3c4e05d644ec10fd0de148911a74ae3031e7` | Key handling and non-sensitive feedback |
| `docs/screen-test-matrix.md` | `6af9f58a8bcaa1594daf396995aaa1d8dff59313` | Import screen's required component/flow/visual coverage |
| `docs/ui-states.md` | `c53acaa9238a52c5d5517ebe39d59034af5f4c21` | Loading/error/disabled/pending conventions |
| `docs/accessibility.md` | `965dbee318bb12b75abdd7d62f839b18ea1443d6` | Accessible actions and manual device acceptance |
| `docs/design-system.md` | `a94ed602b3cd9d2c88dc3366bddf83c6c8dcf994` | Shared outline action and spacing tokens |
| `docs/user-flows.md` | `98891453a1ef78c738efe1208460275567bf38d9` | Import entry, persistence and root navigation |

## Acceptance still outstanding

Only source reasoning and exact publication readbacks were performed. No TypeScript compilation, lint, Jest/component/flow tests, device/simulator execution, storage operation, network request from the application, account operation, or wallet transaction was performed. No test or fixture was added.

Upstream issue521 and CONTRIBUTING still require major failure-state coverage, documentation and device/accessibility verification before review/payment evaluation. This Commons packet does not satisfy or waive those conditions, does not represent upstream acceptance, and does not claim whole-issue completion, assignment, funding, reward or payment.
