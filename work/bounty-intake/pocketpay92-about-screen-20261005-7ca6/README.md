# PocketPay92: About screen and settings entry

## Result and scope

The pinned mobile application has a Settings footer with a hard-coded version and Testnet label, but no About route. This source continuation adds `app/about.tsx` and a Settings entry so users can find the project's purpose, app version, configured network, Testnet disclaimer, and related repositories.

The artifact is a source patch against the exact public mobile commit below. It does not represent an upstream submission, deployed application, device result, issue acceptance, or reward. Issue92 remains assigned to Primex-hub; that assignment and the existing contributors' authorship remain intact.

## Source basis

Canonical repository: [Stellar-PocketPay/pocketpay-mobile](https://github.com/Stellar-PocketPay/pocketpay-mobile).

Pinned main commit: `c3a24abacb45030eb4fef41aabc46b312aaf54a3`.

Root tree: `d1b90aee6dd5b26f1f6f6d4521a77debde9db8ba`.

A complete recursive response contained 374 entries with `truncated: false`. It contained no About route. The fresh donor-branch guard before publication still matched this commit and tree. Every source listed below was read in full and matched both its native blob pin and an independent Git blob identity calculation.

| Input | Blob | UTF-8 bytes | Use |
|---|---|---:|---|
| `app/(tabs)/settings.tsx` | `0295e4c93d564ff44adfb7391fe0bc02c09eaf09` | 7457 | Exact edited preimage; existing theme, buttons and footer |
| `README.md` | `aa291a89b2a33f51144b40f9d938830041d4bac6` | 9682 | Testnet purpose and declared related repositories |
| `package.json` | `08681ade42555a374cf7ba5d55660cc226515681` | 2544 | Existing Expo54, Router6, Constants18 and safe-area5 dependencies |
| `app.json` | `48c09ad592715d7c187bd7c085254093bfbb80ce` | 1111 | Existing application version1.0.0 and router configuration |
| `app/_layout.tsx` | `7b6a2916cd9a897b87577d0584a6cc536458eae0` | 8420 | Existing startup, wallet and lock guards around Slot |
| `app/diagnostics.tsx` | `eebcacf7a9ac8c310e9e071109663a48bdc2ae85` | 10697 | Existing display/navigation conventions only |
| `src/features/settings/useNetworkEnvironment.ts` | `4bda5630ccb6a28c49efd0d5e69bc43c0b27f8c3` | 5410 | Inspected existing settings network implementation |
| `src/components/Button.tsx` | `61547c6c1d186c2d65209723b80bd2fb5fba8f31` | 2666 | Existing themed TouchableOpacity and forwarded accessibility props |
| `src/constants/network.ts` | `feb94455be9d80c9ec1139fb1cf9bd966a82d455` | 120 | Existing configured-network string |

The complete [issue92](https://github.com/Stellar-PocketPay/pocketpay-mobile/issues/92) body requests project description, Testnet use/disclaimer, version when available, related SDK/contracts references and a Settings/menu entry. All three returned comments were read; the latest assignment notice names Primex-hub. No implementation source link appeared in those comments.

The repository-local all-state PR search for `about` returned13 results, including closed PR190 about version display, PR162 about Settings, and PR291 about network labeling. Closed state and narrative descriptions do not establish merge or runtime acceptance. The distinct PR search for92 returned0 with `incomplete_results: false`. Exact PocketPay/92 Slack intake produced an unrelated aggregate containing PocketPay524 and a different repository's issue92. These observations describe their bounded queries and the pinned current source, not an exhaustive ownership census.

## Source changes

The patch contains three hunks: two hunks in Settings and one new route. The total is **165 added lines and2 removed lines**.

| Source path | Preimage | Postimage | Bytes after |
|---|---|---|---:|
| `app/(tabs)/settings.tsx` | `0295e4c93d564ff44adfb7391fe0bc02c09eaf09` | `84b721536e5d2251e74c88249da2904cf732e4b8` | 7777 |
| `app/about.tsx` | Absent in the complete pinned tree | `db734a445635cd499ad15fe295f567398faa5b0c` | 4825 |

### Settings entry and footer

The Management card gains an About PocketPay button that navigates to `/about`. The existing hard-coded footer version and network assertion become the project name and “Testnet demo.” Actual version and configured-network values live on the new screen.

The existing export-secret flow, app-lock controls, wallet reset modal, developer route and styles keep their source bytes outside the two displayed hunks.

### About content and navigation

The route uses the existing theme and Button. It displays:

- A short description of PocketPay as an Expo wallet project for Stellar Testnet experimentation.
- `Constants.expoConfig?.version?.trim() || 'Not available'` as the app version.
- `CURRENT_STELLAR_NETWORK.trim() || 'Testnet'` under **Configured network**.
- The project's development-only/Testnet disclaimer, including no production or real-asset readiness claim and the absence of monetary value for Testnet XLM.
- Links to the current mobile repository and the SDK/contracts URLs declared by the pinned README.

The network field is the existing environment-derived configuration label. It is not a live Horizon/RPC endpoint observation, network health check, or readiness signal. The screen does not import the vault-coupled network hook, diagnostics probes, secret-key API, or wallet store.

Back navigation uses `router.canGoBack()` and `router.back()`, with `router.replace('/(tabs)/settings')` if no prior screen exists. The existing root Slot and its startup, wallet and lock guards continue to control access; no new public route exception is introduced.

A route-local SafeAreaProvider wraps SafeAreaView outside the ScrollView. This gives the new screen its own inset context, including web, without editing the root layout. No remount-sensitive initial-window-metrics optimization is used. Existing font scaling remains enabled; information text wraps and the content scrolls. These are source properties, not measured device accessibility results.

Each project control uses a literal HTTPS URL, link accessibility role, and browser-opening hint. `Linking.openURL` is awaited inside a try/catch so a rejected open produces a visible error alert. The static repository URLs come from the public source; their current availability or redirect destination was not probed.

## Primary API references

The pinned manifest declares Expo `~54.0.33`, Expo Router `~6.0.24`, Expo Constants `~18.0.13`, React Native `0.81.5`, and safe-area context `~5.6.0`. No dependency is added.

- [Expo54 Constants](https://docs.expo.dev/versions/v54.0.0/sdk/constants/) documents nullable `expoConfig` and the application config. The screen reads the app version there; it does not use the Expo Go version.
- [Expo54 Router](https://docs.expo.dev/versions/v54.0.0/sdk/router/) documents the file-based route model and the `canGoBack`, `back`, `push` and `replace` methods used here.
- [Expo54 safe-area context](https://docs.expo.dev/versions/v54.0.0/sdk/safe-area-context/) documents provider context and SafeAreaView padding. It permits providers at relevant route roots and requires one on web.
- [React Native0.81 Linking](https://reactnative.dev/docs/0.81/linking) documents the `openURL` promise and rejection behavior. These links use HTTPS, so no custom-scheme availability check is introduced.

## Artifact integrity and practical limits

`about-screen.patch` is6413 UTF-8 bytes with Git blob identity `395a2b796d3678a21d0d1c629689ecbd783a9741`. It includes full preimage/postimage IDs, regular-file mode100644, exact Settings hunk context, and a new-file hunk for the route.

The retained diff comparison covered every Settings hunk row without clipping. Applying those exact rows to the retained preimage reconstructed the prepared Settings source byte-for-byte; the new-file lines reconstructed the complete route byte-for-byte. Both resulting blob identities match the table above. This is an artifact/source integrity check only.

Compilation, lint, tests, Expo navigation, browser/device rendering, safe-area behavior, dynamic font layout and link-opening behavior were not executed while the executor was offline. No wallet, storage, chain, account or external submission action was taken. The repository's existing dependency duplication and unrelated source defects were not investigated or changed by this patch. The complete tree did not expose a LICENSE path, so this packet does not invent a license grant.

The patch is intended for the exact donor preimage above. Later source changes require an ordinary integration decision using their actual contents. The Commons publication receipt records the artifact identities and the new publisher's local tree-identity result; it does not substitute for upstream integration or application runtime evidence.
