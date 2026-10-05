# PocketPay contact validation, editing and recent recipients

The mounted send-screen contact form accepts a G-prefixed, 56-character base32 string after shape checks alone. This patch makes that existing form also use the app's shared `validateAddress` result before its unchanged duplicate lookup and save callback. The shape checks, inline error text, trimming, name limits, selected-contact ID exclusion, and caller callbacks remain unchanged. Production delta: +2/-1 in one file.

## Source and attribution

Canonical repository: https://github.com/Stellar-PocketPay/pocketpay-mobile .
Current main read for this continuation: `c3a24abacb45030eb4fef41aabc46b312aaf54a3`.

Carlys17's existing merged [PR379](https://github.com/Stellar-PocketPay/pocketpay-mobile/pull/379), head `f69ee7d4f371d95ec671af099f821a0cab056aad`, introduced the contact-form/send integration; its implementation and credit remain intact. This is a new correction against the actual current-main form, not a replay or whole-feature replacement. Current PR379 metadata is CLOSED/merged and its comments endpoint returned zero comments. Historical test claims in its body are the author's evidence, not a new run.

The intake sources were [issue86](https://github.com/Stellar-PocketPay/pocketpay-mobile/issues/86) and [issue300](https://github.com/Stellar-PocketPay/pocketpay-mobile/issues/300): both require validation in saved-contact editing. They remain OPEN and assigned to emmyoat and Muhammad-Al-amin respectively. Issue86's issue header reports three comments; the complete returned comments response contains two, so discussion coverage is explicitly incomplete. Issue300 returned two of two comments. Campaign assignment and external maintainer review remain with those contributors. This Commons source packet does not claim either issue, request payment, or complete the broader edit flow.

| Input | Git blob |
| --- | --- |
| `src/components/ContactForm.tsx` | `e4e4cf4b838960d8de727944a95c3a07fac686f8` |
| `app/send.tsx` | `8c1a38fda246c7421acf23612a7be24649b7b8e4` |
| `src/utils/validation.ts` | `3401c0bb763b27fbb8f20028cee69da7bcdc989f` |
| `src/features/contacts/contactStore.ts` | `fa7d2a5c221462be743c28134e9db2d6e4e64c65` |
| `src/components/ContactManagement.tsx` | `25874bf19b80318d69df03dfac70237abca01469` |
| `app/contacts.tsx` | `9722843b217e96a17917dcfc2f87ea0abe6b5b81` |
| `package.json` | `08681ade42555a374cf7ba5d55660cc226515681` |
| `src/sdk-stub/package.json` | `f958747a5c679b32f7fc5063aeb5783219c95917` |
| `src/sdk-stub/index.js` | `ec02c486d040a884f86bc69aa637cb68ad9056e3` |
| `src/sdk-stub/pocketpay-sdk.js` (same blob in the complete current tree) | `ec02c486d040a884f86bc69aa637cb68ad9056e3` |
| `metro.config.js` | `dbe00f063c6e030c3a1ee28d1245fb8eb9e5ccb5` |
| `CONTRIBUTING.md` | `d8493281d318b348f98a9bd999c2ffd6cc966d0d` |

## Actual contract and correction

The send screen mounts `ContactForm` and forwards saved names/addresses to the existing contact store. The form already checks duplicate addresses and excludes the selected contact's ID. Its local shape predicate, however, returns true without decoding the address or checking its checksum.

The shared `validateAddress` already trims input, calls `validatePublicKey`, and converts an exception to an inline-readable error result; null means success. The current package maps `pocketpay-sdk` to `file:./src/sdk-stub`. That package selects `pocketpay-sdk.js`; the complete tree records the identical blob as the read `index.js`. Its validator calls `StellarSdk.Keypair.fromPublicKey` and throws on a failed parse. Metro's resolver selects the installed Stellar SDK CJS entry and otherwise delegates resolution; no installed-package or device execution is claimed.

Official primary source supports the distinction: [Keypair.fromPublicKey](https://stellar.github.io/js-stellar-base/keypair.js.html) decodes an Ed25519 public key and checks its decoded length; [StrKey.decodeCheck](https://stellar.github.io/js-stellar-base/strkey.js.html) validates canonical encoding, the version byte, and the checksum. These are documented source semantics, not measurements against an installed dependency. No address, key, fixture or transaction was generated or executed.

The form retains its existing G-prefix, 56-character and alphabet checks, then returns `validateAddress(trimmed) === null`. It supplies no own-wallet key, so this contact-entry check does not add the payment-only self-recipient restriction. The existing error branch handles failure, and the unchanged duplicate lookup/save callback follows only after successful validation.

## Application and limits

Apply `contact-address-validation.patch` to the documented source preimage. The expected resulting `src/components/ContactForm.tsx` blob is `4dcb85c2e8a1e839be026d66fd04151fe127f19d`. Compose by hunk against a newer source; do not overwrite another contributor's module.

Only narrow production patches and this guide are published. No license file was present in the complete 374-entry sponsor tree, so the packet does not republish full source modules.

The separate `app/contacts.tsx`/appStore persistence work in existing PR549 is untouched. ContactManagement's parent mounting, broad edit-address confirmation, store unification, persistence failures, concurrent mutation and acceptance of every possible address kind remain outside this patch. This does not establish account existence, funding, network eligibility or payment safety; it only aligns the mounted contact form with the app's existing local address parser.

Validation was static source/caller/primary-contract inspection plus exact artifact and source-postimage hashing. No Expo, TypeScript, Jest, lint, device, accessibility, storage, network, wallet or chain operation ran. Contributor requirements for tests, typecheck, lint, self-assessment and device review remain unfulfilled external acceptance steps. No upstream branch change, submission, reward eligibility, issue acceptance or payment is asserted.

## Contact editor caller continuation

The same current main contains a second, independent integration defect: `ContactPickerProps.onEdit` is required and every saved-contact pencil invokes it, but the mounted `app/send.tsx` supplies no `onEdit`. Its form save callback also always adds a contact. The existing form and store already support an edited contact's ID and an update action.

`contact-edit-caller.patch` wires that actual callback to selected-contact state in the send screen. Selecting Edit closes the picker and opens the existing form with that contact; Save calls `updateContact` with the captured ID, while Add still calls `addContact`. Add, Cancel and successful synchronous callback completion clear edit identity. Opening/canceling the editor does not mutate the store or destination. The payment destination, validation, amount, routing and signing paths are unchanged.

The picker also recomputes its recent-recipient labels when its contacts array changes. Previously its memo depended only on the recent-address list and stable lookup function, so renaming a saved contact could leave the recent section showing the old name even though the saved-contact list had updated. [React's official useMemo contract](https://react.dev/reference/react/useMemo) explains that unchanged dependencies may reuse the previous result; the contacts dependency now records the data read by the stable store lookup.

| Changed source | Before | After |
| --- | --- | --- |
| `app/send.tsx` | `8c1a38fda246c7421acf23612a7be24649b7b8e4` | `739545125800d863b2c0cd63b67ced5080bf7771` |
| `src/components/ContactPicker.tsx` | `fcff58527685bea2469b55ae98f3e9cfc6cda30d` | `148ff15e4b2c1d443d906f0efd0410633da3338b` |

This second patch is +20/-4 and composes with the first patch because it changes different files. Apply both at the documented main preimages; later source requires hunk-level composition. The original address-validation patch is unchanged.

The complete current picker, form, synchronous store action and mounted send caller establish this correction. The repo-local recent-recipient query returned the already-merged PR379; issue85's three returned comments preserve its Primex-hub assignment. The editor patch does not repair the recent-recipient producer: the retained send/review flow does not call its imported `addRecentRecipient`. The separate recording continuation below addresses that missing successful-result consumer; broad issue acceptance remains unclaimed.

The existing edit form validates before invoking Save and excludes the selected ID from duplicate-address lookup. Issue86's suggested extra confirmation before changing an address is not implemented here. Existing local store persistence semantics, concurrent deletion/update, storage-error reporting, two-store unification, and broad editing acceptance remain outside this callback correction. The destination is deliberately left unchanged by editing a saved record; the user selects a recipient through the existing picker action.

No runtime, tests, synthetic inputs, native modal interaction, storage operation, payment or upstream submission was performed. The static call-chain and postimage checks do not establish device behavior, persistence reliability or issue acceptance. Original contributor credit, assignments and external acceptance requirements remain as stated above.

## Completed-result recent-recipient recording

The current send → signing confirmation → review path reaches `store.completeSigning(signingResult)` after the existing send call resolves. The review screen already reacts to `phase === 'completed'` plus a non-null `lastResult` to refresh and navigate. None of these inspected caller files invokes the contact store's existing `addRecentRecipient`; the send screen only imports/destructures it without using it. The picker reads `recentRecipients`, resolves saved names and calls its ordinary destination-selection callback.

`recent-recipient-recording.patch` adds the existing store action inside that completed-result effect. It records `store.lastResult.review.destinationPublicKey`, so the shortcut comes from the completed result's review rather than independently rereading route parameters. The surrounding success condition, refresh, 1.5-second navigation timer and cleanup remain exact. Review, failed, cancelled, submitting and confirming phases do not run the added action.

The action already moves a matching address to the front, removes its previous occurrence, and keeps five entries. Calling it again for the same completed result therefore does not append a duplicate. Its existing persisted state contains addresses, not signing secrets. The correction does not introduce a new storage key, history format, wallet/network partition, account lookup, transaction call, signature or payment action.

A synchronous exception from this optional shortcut update is contained locally so that it does not prevent the already-completed flow's existing success handling. No caught exception or address is logged. This is a best-effort use of the existing synchronous-typed action: its internal AsyncStorage persistence is not awaited, and this patch does not add asynchronous persistence-error reporting, storage transactions or durability guarantees.

| Source input | Git blob |
| --- | --- |
| `app/review-transaction.tsx` before | `2ae491e16b271a0564576d615cf765188678335b` |
| `app/review-transaction.tsx` after | `d363eb677c1fe4fbd8978096212e0512a305c927` |
| `src/store/signerStore.ts` | `33e68f81887d5cd89e448689ee490fa77493f77a` |
| `src/types/signer.ts` | `6ec62299bd9ca5630738b8121de3c4bea7886a3c` |
| `app/sign-confirmation.tsx` | `4ff8ba59f6d9d59c90177216abb7e87313108bac` |
| `app/send.tsx` current main | `8c1a38fda246c7421acf23612a7be24649b7b8e4` |
| `src/features/contacts/contactStore.ts` | `fa7d2a5c221462be743c28134e9db2d6e4e64c65` |

Production delta: +8/-0 in the review screen. Apply the new patch at its exact source preimage; it composes with the preceding two patches on distinct files. No previous patch is overwritten or replaced.

[Issue85](https://github.com/Stellar-PocketPay/pocketpay-mobile/issues/85) explicitly proposes deriving shortcuts from previous payments or successful send actions. It remains OPEN and assigned to Primex-hub. All three returned comments were read; they include the campaign assignment and contributor requests, not maintainer acceptance of this continuation. The bounded repo-local recent-recipient PR search returned Carlys17's already-merged PR379; its credit and prior evidence remain preserved. Exact public searches for the current issue/action produced no matching later source completion; those bounded results are not global absence claims.

This correction records an existing application-level completed result. It does not independently establish network finality, fix current signer/result lifecycle races, backfill historical recipients, handle an unmounted screen, isolate recents by wallet/network, or claim every issue85 criterion and device interaction is accepted. Signing/submission/error-classification code, SDK442 work and the separate contact appStore/persistence carrier remain untouched.

No generated transaction, fixture, test, application execution, runtime/device, storage, payment, chain or upstream action was performed. Static source/caller inspection and exact publication readbacks are the only validation for this continuation. External contributor evaluation, current funding and payment remain unclaimed.
