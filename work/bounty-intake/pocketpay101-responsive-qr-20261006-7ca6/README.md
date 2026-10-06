# PocketPay101: responsive receive QR display

## Result

This source packet replaces the receive screen's fixed QR size with a size derived from its actual available layout width. The complete QR surface, including a conservative white quiet zone, is capped at 400 React Native layout units. The symbol uses black on white in either app theme.

The screen becomes scrollable so the public key, optional payment-request fields and existing copy/share actions can remain reachable when the content is taller than the viewport. The QR surface has a descriptive accessibility label and a hint pointing to the nearby public key and sharing actions.

The change is **50 additions and 13 removals across seven hunks in one production file**. This is an attributed Commons source packet. [Issue 101](https://github.com/Stellar-PocketPay/pocketpay-mobile/issues/101) remains assigned to Lajishola. Device integration, scan reliability and upstream acceptance are not established by this source work.

## Exact source and ownership basis

Repository: [Stellar-PocketPay/pocketpay-mobile](https://github.com/Stellar-PocketPay/pocketpay-mobile).

Pinned main commit: `c3a24abacb45030eb4fef41aabc46b312aaf54a3`.

Root tree: `d1b90aee6dd5b26f1f6f6d4521a77debde9db8ba`.

The complete recursive tree contains 374 entries and reports `truncated: false`. A current named-main observation matched this commit before the source work. A final donor observation is recorded with publication.

The complete issue body requests responsive sizing, surrounding quiet space, portrait readability and a visible or accessible public key. Tap-to-enlarge is optional. All three current comments were read: Menjay7's request, Lajishola's request and the GrantFox assignment notice. This packet preserves that assignment and existing authorship.

The bounded repository-local PR query referencing 101 returned zero results with `incomplete_results: false`. Exact PocketPay/101 Slack search reached native END with one complete result: an unrelated prior asset-format release whose README hash contains 101. Neither query establishes global absence of other work. CI and the infrastructure lane had no retained issue-101 carrier or QR-display hunk; their scanner, import-copy and tooling work is separate.

### Production identity

| Path | Preimage Git blob | Prepared postimage Git blob | Original / postimage UTF-8 bytes |
|---|---|---|---:|
| `app/receive.tsx` | `088b7a6aef30e9e7958ec22c8a9c07f533b1aac6` | `86db673951e5a5c21fe559b9a73371356d5400d9` | 6232 / 7633 |

### Supporting inputs read

| Path | Git blob | UTF-8 bytes | Use |
|---|---|---:|---|
| `src/features/receive/qrPayload.ts` | `6556a1742e7c219f15c8b5e186056369857acdcb` | 3698 | Existing address/payment-request payload selection |
| `docs/qr-payment-requests.md` | `24b09221f8e5d2fb47abbb9c3eea4bb93d18af18` | 4264 | Existing copy/share contract and parser limitation |
| `package.json` | `08681ade42555a374cf7ba5d55660cc226515681` | 2544 | React Native 0.81.5 and existing QR/SVG dependencies |
| `src/constants/theme.ts` | `cbd428b48e7fdce3e26c95ffcc4d95b25fa719a6` | 1579 | Actual light/dark colors and spacing |

Complete acquired source text matched both the native Git blob and an independent Git blob calculation. The manifest requests `react-native-qrcode-svg ^6.3.21` and `react-native-svg 15.12.1`; this is a declared dependency, not evidence of an installed or executed version. No dependency or lockfile changes are included.

The already-read accessibility and design guides remain applicable: `docs/accessibility.md` at `965dbee318bb12b75abdd7d62f839b18ea1443d6` and `docs/design-system.md` at `a94ed602b3cd9d2c88dc3366bddf83c6c8dcf994`. The complete source tree contains no LICENSE path; this packet does not infer a license grant.

## Concrete source problem

The current QR symbol is fixed at 250 units. Its card adds 24 units of padding on each side, and the screen adds another 32 units per side. That structure requires 362 horizontal layout units before any other inset. This is a source-derived width requirement, not an observed device measurement.

The QR also uses the theme's background as its dark-module color and the theme's primary text as its background. In the light theme these resolve to `#F5F7FB` and `#111524`, producing light modules on a dark surface. The proposed symbol and its entire surrounding surface instead use fixed black and white. Other screen text and controls retain their existing theme.

The original outer View has no scrolling. Additional request fields or larger text can make its content taller than the available screen.

## Sizing and quiet-space reasoning

The full-width QR container reports its actual width through `onLayout`. The handler floors that width and clamps it to a nonnegative value. Let:

- `W = min(measured width, 400)`;
- `q = ceil(4W / (21 + 8))`;
- `S = max(0, W - 2q)`.

The existing QR component receives `size=S`. A separate, rectangular white View pads it by `q` on every side. It does not apply rounded clipping to the quiet zone. Rendering waits until `S > 0`; the public-key text and existing actions do not depend on a successful QR measurement.

[DENSO's code-area guidance](https://www.qrcode.com/en/howto/code.html) specifies a four-module quiet zone. Its [version guidance](https://www.qrcode.com/en/about/version.html) gives 21 modules per side as the smallest standard QR symbol. These facts support the following conservative source calculation:

`29q >= 4W`, so `21q >= 4(W - 2q) = 4S`. For any actual standard QR dimension `N >= 21`, the needed four-module margin is `4S/N <= 4S/21 <= q`. Whenever the symbol is positive, the total white frame is exactly `S + 2q = W`, which fits the measured width.

This calculation deliberately avoids reading or re-encoding the generated matrix. Larger QR versions may receive more white space than their minimum. It is a layout-bound argument, not a physical scan, density, camera, display or decoder result.

The [official QR library documentation](https://github.com/Expensify/react-native-qrcode-svg) describes the existing size, color and background-color properties. This patch retains those APIs and uses an outer white View for the quiet zone. It does not add a library-specific export or image-saving path.

## Scrolling, accessibility and preserved behavior

The root ScrollView retains a bounded `flex: 1` style. Padding and child centering move to `contentContainerStyle`. `keyboardShouldPersistTaps="handled"` supports the existing input/button interactions, and `automaticallyAdjustKeyboardInsets` requests the documented iOS keyboard-inset behavior. The [React Native 0.81 ScrollView documentation](https://reactnative.dev/docs/0.81/scrollview) describes these platform and container semantics. The [View documentation](https://reactnative.dev/docs/0.81/view) states that layout events occur on mount and layout changes.

The white QR surface is one accessible image group, with separate labels for a public-key QR and a payment-request QR. No secret key is provided to it. The selectable public-key text remains below the symbol, followed by the same request toggle, fields and actions.

The exact existing validation, payload memoization, address-copy and OS-share handler source is preserved as one contiguous block. In particular:

- The QR still receives the same existing `payload` string.
- Copy Address still copies only the public key.
- Share still shares either the bare address or the existing payment-request URI.
- Invalid amount/memo handling, request-field state, network banner and retry callback are unchanged.

No payload parser, transaction, wallet-storage or SDK operation is added. The existing QR documentation notes a separate scan-side payment-request parsing limitation; responsive rendering does not repair or make a claim about that feature.

Tap-to-enlarge, brightness control and native image export are not implemented. They are not required to establish this bounded responsive-display source change.

## Artifact integrity and integration limits

`responsive-qr.patch` is 4176 UTF-8 bytes with Git blob identity `3c5d4a75edd209de9cbf2d0667e9a2ef6c9d08bb`. It uses mode 100644 and full preimage/postimage IDs.

All 110 rows of all seven hunks were retained without clipping. Forward reconstruction reproduced the full 7633-byte postimage and its blob above; reverse reconstruction reproduced the complete original source and blob. The unchanged validation/payload/copy/share block was also compared directly against the complete source.

No app, Expo, simulator, device, compiler, lint, tests, QR encoder or camera scan was executed. Small-screen layout, keyboard avoidance, OS color inversion, font scaling, accessibility focus and scanner performance remain integration observations to make on actual devices. A width of only a few layout units cannot establish readability; the existing public-key and share/copy alternatives remain available.

The Commons completion receipt separately records both published artifacts, actual merge outcome, complete immutable contents and identities, final metadata and the precisely observed relationship to main. A future integration must use its actual source revision and compose other changes to `app/receive.tsx`. No upstream claim, PR, merge, workflow, account, wallet, chain, payment or reward action was performed.
