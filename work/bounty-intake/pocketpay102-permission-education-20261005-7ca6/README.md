# PocketPay102: explain camera access before prompting

The current scanner requests camera permission from an effect as soon as its permission response is available. That gives the user no opportunity to read the scanner's explanation first, and the effect's predicate also admits a denied-but-requestable response. This patch leaves requesting permission to the existing explicit Grant Permission button.

## Source and attribution

- Canonical issue: https://github.com/Stellar-PocketPay/pocketpay-mobile/issues/102
- Source repository: Stellar-PocketPay/pocketpay-mobile.
- Observed current main: c3a24abacb45030eb4fef41aabc46b312aaf54a3.
- Source path: src/components/QrScanner.tsx.
- Exact preimage: 1307e0933d3565be2bb902831a6c9023cc63ac28.
- Exact postimage after applying permission-education.patch: 630bf3d8b2d15995fc59657679cf8053aa1a0e48.
- Actual caller: app/send.tsx, blob 8c1a38fda246c7421acf23612a7be24649b7b8e4. Its modal mounts QrScanner; onClose clears isScanning; the destination FormField remains available for manual entry.

Credit remains with the PocketPay contributors whose current scanner and send flow this patch extends. Current issue metadata assigns Lspnjr1. The returned historical bot comment 5007814832 instead names abioye-emma; this packet does not resolve or supersede either contributor's assignment. The issue reports five comments, while the successful comments response returned four; this is a coverage limitation. A bounded issue102 PR-body query returned zero results, with incomplete_results=false, and a public PocketPay/102 activity query returned zero/native END. Neither is a global absence guarantee.

This is a Commons source continuation, not a new upstream submission, assignment claim, or whole-issue acceptance claim.

## Behavior

The permission hook still reads the existing camera permission. A loading response still shows the existing checking state. Once a not-granted response is available, the scanner explains that access is for a Stellar wallet-address QR code and offers cancellation/manual entry. It does not claim support for payment-request payloads that the current validator does not accept.

The existing button remains available only when canAskAgain is true. Its onPress requests permission. A non-requestable response retains the existing device-settings guidance and Cancel button. Already-granted access still renders the same camera and scan callback. Removing the effect means permission response changes cannot themselves trigger another request.

The scan validator, debounce, success/error/close callbacks, camera configuration, send routing, signing, payment classification, and SDK442 work are unchanged.

## Dependency contract

The source package.json blob 08681ade42555a374cf7ba5d55660cc226515681 declares expo ~54.0.33 and expo-camera ~17.0.10. The official Expo SDK54 camera documentation lists ~17.0.10 and demonstrates useCameraPermissions with explanation text followed by an explicit button calling requestPermission:

https://docs.expo.dev/versions/v54.0.0/sdk/camera/#usage

That primary example supports the hook/button arrangement used here. It is documentation evidence, not a device or installed-package run.

## Integration and limitations

Apply permission-education.patch to the exact source above, or reconcile its small hunks with a newer scanner. Preserve other accepted PocketPay patches. Production delta: +9/-11; one source file. The complete upstream source is not republished: the retained complete sponsor tree supplies no LICENSE file.

CONTRIBUTING.md d8493281d318b348f98a9bd999c2ffd6cc966d0d requires upstream UI-state, screen-matrix, accessibility, tests, typecheck/lint and contributor-assessment work. Relevant existing guides are docs/ui-states.md c53acaa9238a52c5d5517ebe39d59034af5f4c21, docs/screen-test-matrix.md 6af9f58a8bcaa1594daf396995aaa1d8dff59313, and docs/accessibility.md 965dbee318bb12b75abdd7d62f839b18ea1443d6. Those upstream acceptance requirements remain pending.

This patch was assessed from complete production source and the actual caller only. No runtime, tests, typecheck, build, camera, permission prompt, device, account, wallet, or payment action was performed. Permission-request pending/error handling is supplied by the follow-through below. Existing permission refresh after device settings, initial permission-read failure, scan-timer cleanup, native configuration and real-device accessibility remain outside this change. No bounty award, payment or maintainer approval is claimed.

## Follow-through: pending and failed permission requests

Apply permission-request-state.patch **after** permission-education.patch. The first artifact remains unchanged. Incremental source preimage is 630bf3d8b2d15995fc59657679cf8053aa1a0e48; postimage is 030319ba664c2522d1df04a5fa15a125b3529711; incremental production delta is +30/-2.

The existing button previously delegated its promise directly. The follow-through awaits that promise in a scanner-local handler, displays Requesting while it is pending, disables the request button and marks it busy. A ref is set synchronously before requesting, so another callback before the pending render cannot start a second request in this component instance. The existing permission response remains authoritative: already granted or non-requestable responses are not requested again.

A thrown or rejected request displays a fixed local message with retry/manual-entry guidance; no provider error object is displayed or logged. The prior error clears at the start of the next explicit attempt. Finally always clears the local in-flight and pending state when that attempt settles. A resolved denial uses the existing denied/settings UI; it is not relabeled as a request failure. Cancel remains available, and the explanation-first behavior from31786 remains intact.

Expo SDK54 documents useCameraPermissions and the Promise<PermissionResponse> request method: https://docs.expo.dev/versions/v54.0.0/sdk/camera/#usecamerapermissionsoptions . Its PermissionResponse defines granted and canAskAgain, including settings guidance for a non-requestable permission. React Native0.81 documents the disabled and busy accessibilityState fields, alert role and Android polite live regions: https://reactnative.dev/docs/0.81/accessibility . These are primary source contracts, not executed device observations.

The ref covers one component instance and one outstanding request. It is not a cross-instance lock, timeout, native cancellation mechanism or lifecycle transaction. Closing the scanner does not claim to cancel an OS prompt. Initial hook-read failure, settings-return refresh, native device behavior and the other original integration limits remain outside this patch. Upstream tests/typecheck/lint/accessibility acceptance are still pending, and no runtime, camera, permission prompt, wallet, payment or upstream action was performed.
