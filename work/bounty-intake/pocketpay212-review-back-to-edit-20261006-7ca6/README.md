# Return transaction review to editable payment details

## Concrete behavior

The current mobile flow is `Send → Sign Confirmation → Review`. The action labelled **Back to Edit** in the review screen uses `router.back()`, so it returns to the read-only signing-confirmation screen. That screen's explicit Cancel action returns to the tabs route. The root layout renders `Slot`, so this correction does not assume that an earlier form's component state remains mounted.

The review-phase edit action now replaces the review route with `/send`, carrying its existing public destination, amount and memo values. Send reads these optional route parameters to initialize its three editable fields; missing or non-string values initialize as empty. The values are initial form input, not authorization or validated payment data. Existing on-change and submit validation remains unchanged, and pressing the normal form action still goes through confirmation before submission.

Only the review-phase edit action and Send's input initialization change. No new persistent draft, signing, submission, SDK, fee, contact, wallet, result or error-classification behavior is added. This is a narrow continuation for [issue212](https://github.com/Stellar-PocketPay/pocketpay-mobile/issues/212), not a new review feature or whole-issue acceptance claim.

## Actual source and attribution

Canonical repository: [Stellar-PocketPay/pocketpay-mobile](https://github.com/Stellar-PocketPay/pocketpay-mobile).
Pinned sponsor main: `c3a24abacb45030eb4fef41aabc46b312aaf54a3`, freshly observed unchanged during this continuation.

| Source | Git blob | Role |
| --- | --- | --- |
| `app/review-transaction.tsx` | `2ae491e16b271a0564576d615cf765188678335b` | Complete production preimage and review-only edit callback |
| `app/send.tsx` | `8c1a38fda246c7421acf23612a7be24649b7b8e4` | Editable fields, validation and push to sign confirmation |
| `app/sign-confirmation.tsx` | `4ff8ba59f6d9d59c90177216abb7e87313108bac` | Actual intermediate route and push to review |
| `app/_layout.tsx` | `7b6a2916cd9a897b87577d0584a6cc536458eae0` | Root `Slot` navigation; not an assumed retained Stack |
| `package.json` | `08681ade42555a374cf7ba5d55660cc226515681` | Declares `expo-router: ~6.0.24` |
| `CONTRIBUTING.md` | `d8493281d318b348f98a9bd999c2ffd6cc966d0d` | Upstream contribution and acceptance requirements |

**Kend07** supplied the original review in [PR313](https://github.com/Stellar-PocketPay/pocketpay-mobile/pull/313), head `3ccc87e5b3f9b64d2e9d653bb66220b98c50298e`, merged at `cbdf449bf31f7740169bd0ee0bddbdf5be32dec1`. **nanaabdul1172**'s [PR348](https://github.com/Stellar-PocketPay/pocketpay-mobile/pull/348) introduced the signing-confirmation flow; **giftexceed**'s [PR383](https://github.com/Stellar-PocketPay/pocketpay-mobile/pull/383) supplied the shared UI. Their work and attribution remain intact.

Issue212 was OPEN, unassigned and had zero comments at the observed read. A bounded exact issue-number PR-body query returned zero matches; the actual source-path chronology identified the existing review and confirmation contributions above. Neither result establishes exhaustive absence of other work.

Known fee-estimate PR553, recent-recipient continuation31781, shared failure/receipt changes and draft prerequisite PR563 remain separate. This packet does not replace those carriers or infer completed native/device acceptance.

## Primary navigation contract

The [Expo Router SDK54 API](https://docs.expo.dev/versions/v54.0.0/sdk/router/) documents `Slot` as rendering selected content, `useLocalSearchParams` as returning the current route's parameters, and `replace` as navigating without appending a history entry. The [Expo navigation guide](https://docs.expo.dev/router/basics/navigation/) distinguishes replacing the current page from going back to its predecessor.

The new return route uses an object Href with the same three non-secret payment values already carried between the existing screens. A new Send screen initializes from those values rather than relying on old component memory. These primary contracts and the actual layout support the source change; they are not an installed-package or device result.

## Applying and composing

Apply `review-back-to-edit.patch` to the pinned source, or compose its four hunks with newer files. Production delta: **+19/-5** across two files.

| Production path | Preimage | Postimage |
| --- | --- | --- |
| `app/review-transaction.tsx` | `2ae491e16b271a0564576d615cf765188678335b` | `22702b203c52bfcaebd12592a2a2a96deb4b1c11` |
| `app/send.tsx` | `8c1a38fda246c7421acf23612a7be24649b7b8e4` | `60b48610724c0e4e3dbc33b89d990191bac9223a` |

Preserve all separate recipient, fee, receipt, failure-copy and prerequisite improvements when integrating. This is a patch, not a whole-module replacement. The source tree contains no LICENSE file; this Commons packet includes only a minimal diff and original guide.

The parameters initialize the new form only. There is no reactive synchronization of later parameter changes into an already edited field, durable draft persistence, restoration of arbitrary unreviewed input or history cleanup beyond replacing the current review route. Original form whitespace was already trimmed by the preceding flow. Additional payment asset types and secret material are not introduced.

## Validation and limits

Complete retained source and the actual root layout were inspected. The exact source preimages were independently hashed; unique replacements and reverse reconstruction preserve every other byte. Publication checks cover full artifact text, native and independently computed Git identities, expected paths and commit lineage.

No app, browser, emulator, camera, wallet/account/storage, SDK, chain/payment, build, typecheck, lint, test, fixture or hosted workflow was run. No upstream issue/comment/PR, assignment, bounty claim or payment action was performed. Upstream device, accessibility, screenshots, tests and maintainer review remain unperformed.

Known prerequisites remain: current sign-confirmation source has import/component concerns described by draft PR563; review still uses its current combined SDK call; fee/result/failure improvements have their own carriers. No full app readiness, security, atomicity, transaction cancellation or durable draft guarantee follows from this edit-return correction.
