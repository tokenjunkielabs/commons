# PocketPay: reject numeric overflow in amount validation

The shared amount validator accepts a sufficiently large digit-only input when no balance is supplied: its decimal syntax passes, conversion produces positive Infinity, the NaN check does not reject it, and the remaining positive/decimal-place checks can pass. This packet replaces the NaN-only condition with a finite-number condition. The existing error text and every other amount rule are retained.

## Source and attribution

Canonical repository: [Stellar-PocketPay/pocketpay-mobile](https://github.com/Stellar-PocketPay/pocketpay-mobile). Pinned source: `c3a24abacb45030eb4fef41aabc46b312aaf54a3`.

The complete retained `src/utils/validation.ts` is the input to this new correction. Its bounded current file history credits abore9769's field-level validation, estyemma/Emmzyemms's payment-field sanitisation, and subsequent contributions by Sparexonzy95, Chigybillionz and Favouratambi. This packet preserves that work and does not claim a new assignment, original-feature completion or reward.

| Source path | Before Git blob | After Git blob |
| --- | --- | --- |
| `src/utils/validation.ts` | `3401c0bb763b27fbb8f20028cee69da7bcdc989f` | `899bfa377e0cdf2479ddd89059ca250e1393df02` |

Production delta: +1/-1. Apply `finite-amount.patch` to that preimage, or compose the single condition with newer source. Other validators in the same module are unchanged.

## Actual caller and existing contribution

The current receive screen, `app/receive.tsx` blob `088b7a6aef30e9e7958ec22c8a9c07f533b1aac6`, calls `validateAmount(amount)` without a balance: a requester is not spending their own balance. That exact callsite was transferred from retained complete source and is unchanged in the separately completed responsive-QR postimage `86db673951e5a5c21fe559b9a73371356d5400d9` ([Commons 31800](https://github.com/woahwhattheheck/commons/pull/31800)).

The full current formatter, `src/features/receive/qrPayload.ts` blob `6556a1742e7c219f15c8b5e186056369857acdcb`, explicitly trusts prior amount validation and copies the original trimmed amount string into the URI. This is a concrete consumer of the validator, not an invented optional-argument caller.

The existing [PR 554](https://github.com/Stellar-PocketPay/pocketpay-mobile/pull/554) for issue 523 is OPEN/unmerged at observed head `a245d7575384e0f1d84ee38e5063b6169c5a1d09`, authored by woahwhattheheck, with zero comments/review comments. Its actual changed-path list and QR production patch show that it delegates amount checks to the same shared `validateAmount`; it does not alter `src/utils/validation.ts`. Preserve that contribution's address/network/request handling and pending acceptance. This single helper correction can compose with it rather than duplicate it.

The baseline receive screen separately omits invalid optional fields from the generated payload. This patch does not change that behavior or claim the whole invalid-QR workflow is complete; PR 554 addresses that wider concern. The already completed responsive-QR, contact-validation and memo-feedback work also remain separate.

## Numeric contract

ECMAScript distinguishes Infinity from NaN. Its [Number-type definition](https://tc39.es/ecma262/multipage/ecmascript-data-types-and-values.html#sec-ecmascript-language-types-number-type) specifies the finite representable range and conversion to infinity at overflow. The [Number.isFinite definition](https://tc39.es/ecma262/multipage/numbers-and-dates.html#sec-number.isfinite) returns true only for finite Numbers. The existing decimal regular expression excludes a literal word such as Infinity, but places no upper bound on a digit sequence's magnitude.

The official [Stellar operation source](https://stellar.github.io/js-stellar-base/operation.js.html) also rejects non-finite amounts in its standard operation validator. That primary source supports rejecting overflow here; it is not evidence of running the app's installed SDK.

The correction preserves trimming, decimal syntax, positive-value checks, the existing seven-decimal-place rule, optional balance/reserve checks and their current messages. It introduces no new maximum-amount policy or parser. Finite values beyond Stellar's operation range, floating-point precision, balance validity and asset-specific rules remain outside this one-line correction.

## Validation and integration limits

Source validation is static: complete validator and formatter input, the actual receive callsite, the current PR 554 production delta, and official numeric contracts. No synthetic numeric input, generated fixture, test, SDK invocation, application, native/device, wallet, account, network, QR scan or transaction was executed. No installed-version or whole-payment correctness claim is made.

Current retained `CONTRIBUTING.md` is `d8493281d318b348f98a9bd999c2ffd6cc966d0d`. Required upstream checks, UI-state/screen-matrix updates and native acceptance remain pending for any upstream integration. This delivery is a Commons source packet only; no upstream branch, PR, comment, assignment, account or payment action is performed.

The observed complete sponsor tree contains no LICENSE file. Only the narrow attributed patch and this guide are published; no complete sponsor module or invented license is included. Funding, awards and payment are not asserted.
