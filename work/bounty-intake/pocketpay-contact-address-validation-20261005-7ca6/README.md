# PocketPay contact form address validation

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

Only the two-line production correction and this guide are published. No license file was present in the complete 374-entry sponsor tree, so the packet does not republish its full source module.

The separate `app/contacts.tsx`/appStore persistence work in existing PR549 is untouched. ContactManagement's parent mounting, broad edit-address confirmation, store unification, persistence failures, concurrent mutation and acceptance of every possible address kind remain outside this patch. This does not establish account existence, funding, network eligibility or payment safety; it only aligns the mounted contact form with the app's existing local address parser.

Validation was static source/caller/primary-contract inspection plus exact artifact and source-postimage hashing. No Expo, TypeScript, Jest, lint, device, accessibility, storage, network, wallet or chain operation ran. Contributor requirements for tests, typecheck, lint, self-assessment and device review remain unfulfilled external acceptance steps. No upstream branch change, submission, reward eligibility, issue acceptance or payment is asserted.
