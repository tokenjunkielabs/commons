# PocketPay 298: close the scanner while permission is loading

The scanner's initial permission-check view renders a spinner and “Checking camera permission…” but has no visible close control. This patch adds the existing **Cancel** button to that view. It calls the existing `onClose` callback, so the Send screen can return to manual recipient entry without waiting for the permission result.

This is a source-only continuation for [PocketPay issue 298](https://github.com/Stellar-PocketPay/pocketpay-mobile/issues/298). It does not implement another send form or duplicate the manual fallback already present in the caller.

## Source and attribution

Upstream project: [Stellar-PocketPay/pocketpay-mobile](https://github.com/Stellar-PocketPay/pocketpay-mobile). Original project and contributor credit remains with its authors. Existing Commons scanner continuations [31786](https://github.com/woahwhattheheck/commons/pull/31786) and [31788](https://github.com/woahwhattheheck/commons/pull/31788) retain their separate credit and scope.

A fresh canonical branch observation for this work returned upstream main `c3a24abacb45030eb4fef41aabc46b312aaf54a3`. The current issue was open, unassigned, and reported zero comments; its canonical comments page returned an empty array. One bounded repository PR search for `298` returned zero rows with `incomplete_results: false`. This is that query's result, not a repository-wide proof of absent work or an assignment.

| Input | Git blob identity |
|---|---|
| Upstream `src/components/QrScanner.tsx` at that main | `1307e0933d3565be2bb902831a6c9023cc63ac28` |
| Upstream `app/send.tsx` at that main | `8c1a38fda246c7421acf23612a7be24649b7b8e4` |
| Scanner after existing 31786 education change | `630bf3d8b2d15995fc59657679cf8053aa1a0e48` |
| Scanner after existing 31788 request handling change: this patch's preimage | `030319ba664c2522d1df04a5fa15a125b3529711` |
| Scanner after this patch | `92d9777629385d2f3b2ec0b1fc6d0ced820adc5f` |

The complete composed scanner preimage was transferred from retained source custody and independently identified as 10,917 UTF-8 bytes / blob `030319ba664c2522d1df04a5fa15a125b3529711`. It is a Commons patch composition, **not** an assertion that upstream main already contains 31786 or 31788. The private composed postimage is 11,205 UTF-8 bytes.

The retained complete 374-entry upstream tree had no LICENSE or AGENTS file. This packet publishes only the narrow patch and this note, not a full copy of the module or a newly asserted license.

## Exact change and caller contract

`change.patch` adds eight JSX lines in the `if (!permission)` branch. It reuses the existing `TouchableOpacity`, `styles.closeButtonFallback`, `styles.closeButtonFallbackText`, `onClose`, visible “Cancel” text, `accessibilityLabel="Close scanner"`, and button role already used by the permission-denied branch. The loading status and live region remain present.

The granted and denied permission branches already expose close controls. The missing initial-lookup control is the scope of this continuation; no claim is made that a permission lookup was observed to hang.

The retained current Send caller has `destination`, `amount`, `memo`, `errors`, and `isScanning` state in the same `SendScreen`. Its scanner close handler only calls `setIsScanning(false)`. Its invalid-code handler closes the modal and shows an alert, without clearing destination, amount, or memo. Its successful-scan handler closes the modal and updates destination through the existing validator. The destination form is already controlled and editable. Thus the added button reaches the existing manual-entry path; it does not reconstruct or reset input.

No changes are made to barcode validation, debounce, successful-scan handling, camera mounting, permission-request coalescing or error handling, navigation, payment validation, stores, or the caller callbacks. The added close action dismisses this UI; it does not cancel the permission hook's underlying lookup, prove camera shutdown, or revoke permission.

## Composition

Apply the prior 31786 and 31788 scanner patches first, preserving their order, then this patch. The full preimage blob must equal `030319ba664c2522d1df04a5fa15a125b3529711`; the resulting blob is `92d9777629385d2f3b2ec0b1fc6d0ced820adc5f`. The new hunk is disjoint from those patches' request/explanation changes. The complete source bytes outside this eight-line insertion are unchanged.

The patch's base is deliberately the composed scanner. It should not be represented as a complete replacement patch against unmodified upstream main.

## Instructions and validation limits

The current `CONTRIBUTING.md` contract is retained at blob `d8493281d318b348f98a9bd999c2ffd6cc966d0d`. These current documentation files were acquired at the same exact upstream commit, with complete native content and independent blob identities:

| Document | Blob |
|---|---|
| `docs/ui-states.md` | `c53acaa9238a52c5d5517ebe39d59034af5f4c21` |
| `docs/screen-test-matrix.md` | `6af9f58a8bcaa1594daf396995aaa1d8dff59313` |
| `docs/accessibility.md` | `965dbee318bb12b75abdd7d62f839b18ea1443d6` |

The relevant catalogue contract requires permission/scanning/invalid-code/close states and a non-camera alternative. The accessibility contract calls for a labelled scanner close control and equivalent typed content. The screen matrix and contributor instructions require component/flow checks as applicable, visual review, typecheck, lint, and device/assistive-technology evidence before upstream acceptance. Those requirements remain unperformed here.

Review performed: current issue/comment/branch chronology, the retained exact scanner and caller contract, the relevant documentation sections, the eight-line source insertion, and independent UTF-8/Git-blob identities. Publication checks concern artifact integrity only.

No app, scanner, permission request, wallet, camera, emulator, browser, test suite, lint, build, typecheck, CI workflow, or device interaction was executed. No synthetic fixture was created. Layout, hit targets, contrast, focus return, screen-reader behavior, and platform permission behavior were not measured. The existing caller's state-preservation conclusion is static source reasoning, not a completed interactive flow.

This packet is not an upstream submission, issue assignment, issue closure, evaluation approval, or payment claim. It closes one source-level omission; it does not certify all of issue 298's acceptance criteria or the wider scanner accessibility contract.
