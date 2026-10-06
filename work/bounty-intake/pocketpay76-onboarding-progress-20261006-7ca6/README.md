# PocketPay76: onboarding progress on the existing create and import paths

## Result

This source packet adds a lightweight, themed progress display to the existing wallet setup screens. The create path shows **Generate keys → Back up your key → Wallet**; the import path shows **Import key → Wallet**. Each displayed phase includes its step number and a short explanation of what comes next.

It also removes an obsolete inline create-success fragment that references `isSuccess` and `handleGoToWallet` without declarations or imports in that module. The existing save handler already navigates to the separate `wallet-creation-success` route, whose real handler and layout were acquired before this removal.

The patch changes four source paths, with **132 added lines, 34 removed lines and 17 hunks**. It is a Commons source continuation, not an upstream submission, deployed app, runtime result, completed accessibility audit, issue acceptance or reward. [Issue76](https://github.com/Stellar-PocketPay/pocketpay-mobile/issues/76) remains assigned to Primex-hub.

## Exact source basis

Repository: [Stellar-PocketPay/pocketpay-mobile](https://github.com/Stellar-PocketPay/pocketpay-mobile).

Pinned main commit: `c3a24abacb45030eb4fef41aabc46b312aaf54a3`.

Root tree: `d1b90aee6dd5b26f1f6f6d4521a77debde9db8ba`.

The complete recursive tree contains 374 entries and reports `truncated: false`. It contains no OnboardingProgress component. The current issue body and all three comments were read in full. The latest assignment notice names Primex-hub; the earlier contribution requests and existing authorship are preserved. The bounded repository-local PR query for 76 returned zero results with `incomplete_results: false`. Exact PocketPay/76 Slack search returned one unrelated preparation notice in which 76 was a changed-line count, not this issue.

The current create fragment was separately checked against the retained source and the dedicated success route. The exact PocketPay/isSuccess Slack search returned zero results with native END. CI and the infrastructure lane had no retained owner or fix for that fragment; those are bounded custody statements, not a global ownership claim.

### Source files changed

| Path | Preimage Git blob | Prepared postimage Git blob | Postimage UTF-8 bytes |
|---|---|---|---:|
| `app/(auth)/create.tsx` | `f790cb1ad52715792c847db70855050e6398a664` | `f78de5ecfff9a5a26257c83c8e6b58f6bf68e867` | 9065 |
| `app/(auth)/import.tsx` | `38a3f75f9aafb94084456110853457f792f2aab3` | `0deee7c2bd551d50ccf4d9d1e17332d63fa54a8d` | 9402 |
| `app/(auth)/wallet-creation-success.tsx` | `d170bd84996dbc84389e019c3791d518d96f3fde` | `6043ed06a07897f2ab408fd28e73991fd342d74b` | 2108 |
| `src/components/OnboardingProgress.tsx` | Absent in the complete pinned tree | `b9cf3ec74e5a2f7807a07ca8a1fc5130d2c999c7` | 2763 |

The original create, import and dedicated success files are 9537, 8886 and 1806 UTF-8 bytes respectively. Each complete source acquisition matched its native blob identifier and an independent Git blob identity calculation.

### Supporting source read

| Path | Git blob | UTF-8 bytes | Relevance |
|---|---|---:|---|
| `app/(auth)/_layout.tsx` | `8b81fa1ea9dc527224734c768807b882dbfeaafc` | 791 | Existing Stack registration and route titles |
| `app/(auth)/index.tsx` | `01835e58ce4066eb684c69aa11868b2cee05f1a5` | 1022 | Existing create/import choice screen |
| `app/_layout.tsx` | `7b6a2916cd9a897b87577d0584a6cc536458eae0` | 8420 | Startup, wallet, lock and auth-redirect behavior |
| `src/types/onboarding.ts` | `cc4586ac32bf7dd00d110ffa8bcddce0badc66ec` | 5660 | Existing failure and recovery model |
| `src/constants/theme.ts` | `cbd428b48e7fdce3e26c95ffcc4d95b25fa719a6` | 1579 | Actual palette, spacing and radius tokens |
| `docs/design-system.md` | `a94ed602b3cd9d2c88dc3366bddf83c6c8dcf994` | 15682 | Theme resolution, typography, spacing and scroll guidance |
| `docs/accessibility.md` | `965dbee318bb12b75abdd7d62f839b18ea1443d6` | 17066 | Grouping, labels, scalable text and device evidence requirements |
| `docs/mobile-onboarding-checklist.md` | `13f00b14e089521dfee85beb4955906eb927e772` | 3675 | Contributor setup instructions; not a product onboarding state machine |

The previously acquired package manifest `08681ade42555a374cf7ba5d55660cc226515681` declares React Native 0.81.5, React 19.1.0, Expo 54 and Expo Router 6. No dependency is added. The previously acquired README `aa291a89b2a33f51144b40f9d938830041d4bac6` describes a Testnet development project. The complete tree contains no LICENSE path; this packet does not infer a license grant.

## Display behavior

| Existing rendered state | Indicator | What follows |
|---|---|---|
| Create screen before a keypair exists | Step 1 of 3: Generate keys | Back up the secret key, then reach the wallet |
| Create screen with its existing generated keypair | Step 2 of 3: Back up your key | Use the existing backup confirmation and save path |
| Dedicated wallet-creation-success screen, if rendered | Step 3 of 3: Wallet | Existing Go to Wallet action; Testnet funding from Home |
| Import form | Step 1 of 2: Import key | Existing validation, import and wallet-save path |
| Existing import success branch, if rendered | Step 2 of 2: Wallet | Existing Go to Wallet action and Home balance display |

The new component receives only a static flow/stage pair. It receives no public or secret key, account, amount, network client or persistent state. The create/import stage union makes the supported combinations explicit. The display derives its labels and decorative segments from two small constant step arrays; it does not add a setup controller, timer, gate, storage field or asynchronous action.

The selected phase is described in text as well as by its segments. The component uses the existing resolved theme, `SIZES` and `RADIUS`. Text has no line-count limit or fixed container height.

The existing recovery returns still take priority and retain their original error/retry content. The initial create/import choice screen is unchanged. Funding is not inserted as a required step before entering the wallet; the existing creation-success copy already locates Friendbot on Home.

### Navigation and completion limits

The existing root auth guard redirects a signed-in wallet from auth routes to `/(tabs)`. That redirect may take the user to the wallet before a success screen remains visible. This patch does not delay or change that guard. The final indicator is present when an existing success view renders; no minimum display duration or new success-route reachability is claimed.

The source's existing wallet save, backup-pending marker, validation, import, retry, reset and navigation handlers retain their exact bytes. The final label reflects the existing success view and destination. It is not an independent assertion of funding, network readiness, persistence durability or production readiness.

## Obsolete create view removed

The create source has one obsolete success-return fragment with undeclared module references, followed by the real generate/reveal branches. Its current successful save callback already calls `router.replace('/(auth)/wallet-creation-success')`. The separate route defines its own real `handleGoToWallet` and is registered in the auth layout.

The patch removes that obsolete fragment, its now-unused CheckCircle import and its successIcon style. It does not introduce a replacement state variable or reconstruct missing control flow. This removes the source references that obstruct the normal create render; no compiler or runtime pass is asserted.

## Scrolling and accessibility

The generate and existing success content regions become bounded ScrollViews with centering on their content containers. The import form remains within the existing KeyboardAvoidingView and gains a ScrollView with handled keyboard taps and bottom content padding. Its existing submit button remains a sibling below the scrolling form. These changes give the additional progress copy and growing text a scrollable content region without changing the action handlers.

The indicator is one accessible group with a `progressbar` role, a flow label and a textual `accessibilityValue` containing the current step and next action. Its decorative segments are hidden from accessibility traversal on iOS and Android. A polite live region is requested for supported platforms. No key value is included in the announcement.

[React Native 0.81 accessibility documentation](https://reactnative.dev/docs/0.81/accessibility) documents accessible grouping, the progressbar role, textual accessibility values and descendant hiding. It also distinguishes platform behavior. These API semantics support the source design; they do not constitute an observed VoiceOver or TalkBack result.

The repository's accessibility checklist requires device/simulator, large-text, focus and component evidence for upstream UI acceptance. That checklist has not been completed by this source packet. No device, simulator, keyboard, contrast measurement, screen-reader session, lint, compiler or tests were run while execution was offline. Layout, focus and announcement behavior remain runtime integration work.

## Artifact integrity

`onboarding-progress.patch` contains 11,375 UTF-8 bytes with Git blob identity `da5cdac240dbd635c3f6e673f7aeb9322a552c80`. Its four paths use mode 100644 and complete preimage/postimage IDs.

Every retained hunk row was included without clipping. Reconstructing each postimage from the complete original source and the exact hunk rows reproduced all four full source strings and the blob identities above. The component logic before the first render boundary is byte-identical in each existing screen, which covers the existing handlers and state declarations. The full diff also preserves the recovery branches.

The final Commons receipt records the two artifact identities, actual publisher outcome, full immutable readbacks and separate current-main observation. The patch is based on the exact donor revision above; later source changes require integration against their actual contents. No upstream issue claim, PR, merge, workflow, wallet, account, chain or payment action was performed.
