# Make the existing scan-to-pay review input editable

## Source defect and correction

The current `app/scan-pay.tsx` initializes `rawInput` to an empty string, displays it in read-only `Text`, and only calls `setRawInput` to clear it. There is no input callback, camera callback or route-parameter producer in that complete module. Its Parse scan button is disabled while the string is empty, so this screen's existing parsing/review path cannot receive user input through the rendered UI.

The patch replaces that read-only display with the app's existing `FormField`, bound to `rawInput`. Its change callback stores the new text and resets the prior review. Thus edited text cannot continue showing or confirming an earlier parsed result; the user explicitly chooses Parse scan again. The field has a matching accessibility label, a payload placeholder, and no automatic capitalization or correction. The now-unused display styles are removed.

Parsing, validation, safe-error display, cancellation and the existing confirmation placeholder remain unchanged. This does not add camera access, read a clipboard programmatically, create a payment intent, sign, submit, or wire confirmation into Send. The original contribution explicitly defers that handoff.

## Exact source and author

Canonical repository: [Stellar-PocketPay/pocketpay-mobile](https://github.com/Stellar-PocketPay/pocketpay-mobile).
Current pinned main: `c3a24abacb45030eb4fef41aabc46b312aaf54a3`, freshly observed unchanged.

[Issue407](https://github.com/Stellar-PocketPay/pocketpay-mobile/issues/407) remains OPEN and assigned to **deepak0x**. Its two current comments are the author's request and GrantFox assignment; no new submission or assignment was made. The original [PR427](https://github.com/Stellar-PocketPay/pocketpay-mobile/pull/427) by deepak0x is MERGED, with head `46d0b31808adadc1c24dc72bbef5a84017114902` and merge `e8150d3150a65c09fa53ee827c759948df6d9568`. Its body says the feature is review-only and leaves Send wiring for a follow-up. Original code, authorship and external acceptance rights are preserved.

| Input | Git blob | Use |
| --- | --- | --- |
| `app/scan-pay.tsx` | `9687ded9b1390dc3f69fb47f8297f8a26cef487e` | Complete production preimage; read-only input defect |
| `src/features/payments/useScanPayReview.ts` | `6ec5f297bf1b73b70e1a7f9f6b155900b36dcb82` | Existing reset clears review and returns to idle; no payment effects |
| `src/components/FormField.tsx` | `0654b841729849a2b0099d4ef8b191a5733b33fe` | Existing editable TextInput wrapper forwards value/change/accessibility props |
| `docs/scan-to-pay.md` | `22ab00c2f55c1b7fdb1d1579107278becf4f5ba8` | Review-only scope and explicit deferred Send handoff |
| `package.json` | `08681ade42555a374cf7ba5d55660cc226515681` | React Native 0.81.5 declaration |

[React Native 0.81 TextInput documentation](https://reactnative.dev/docs/0.81/textinput) describes text input and its onChangeText callback, including the auto-capitalization and correction options. The actual FormField source supplies the wrapper contract. No dependency or native API was installed or executed.

The separate `app/scan.tsx` (`5e14eaf76c8abc47d3cfc1dd1d264a15b1630d33`) and embedded QrScanner are different flows. They are not altered or described as completed payment-request consumers. Existing scanner continuation31811 and edit-return31823 remain separate.

## Patch and composition

Production delta: **+10/-19**, one file, three hunks.

| Path | Preimage | Postimage |
| --- | --- | --- |
| `app/scan-pay.tsx` | `9687ded9b1390dc3f69fb47f8297f8a26cef487e` | `eaebca363ab2729fa74ee4e4069e4d7ae2203ab5` |

Apply `review-input.patch` to the exact source or compose the same narrow hunks into a newer screen. Do not overwrite a newer full module. No LICENSE was present in the retained current tree, so the packet republishes only this minimal diff and original guide.

## Validation and limits

The full real module, hook, component wrapper and feature guide were inspected. Source and artifact Git blob identities were independently computed; exact replacement and reverse reconstruction preserve all unrelated source bytes. The existing pure validator was not executed, rebuilt or re-proved. The PR author's historical test claims are not new results from this operation.

Current CONTRIBUTING, UI state catalogue, screen test matrix and accessibility requirements remain applicable to upstream integration. They require actual UI/device and test evidence that this source-only packet does not supply.

No app, device, browser, camera, clipboard, wallet, account, storage, chain/payment, dependency installation, build, typecheck, lint, test, fixture or hosted workflow was run. No upstream issue/comment/PR, assignment, bounty or payment action was performed. This fixes the reachable manual-input surface of the existing review route; it does not claim a new camera entry point, end-to-end scan-to-pay integration, current balance revalidation, payment execution, whole-issue acceptance or a security audit.
