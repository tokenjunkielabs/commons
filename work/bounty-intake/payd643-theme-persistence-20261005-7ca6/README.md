# Keep theme choice usable when persistence is unavailable

This packet continues [Protocol-Guild/PayD issue #285](https://github.com/Protocol-Guild/PayD/issues/285), Add Dark/Light Mode Theme Switcher, through SrvFernandes's [PR #643](https://github.com/Protocol-Guild/PayD/pull/643). It corrects the submitted theme provider's storage boundary and aligns the browser color-scheme declaration with the selected theme.

## Canonical source and authorship

PR #643 was OPEN/unmerged at `62238188669482cfd6c742984b0cbb74ff3c065d`, branch `SrvFernandes/PayD:feat/onlydust-fix-285-1790981163460`, against base `171c74b454daba241bfb75f36d10a0a3a77a68e5`. Issue #285 was OPEN/unassigned. Its complete two-comment chronology contains a third-party proposal and SrvFernandes's submitted-PR link/claim, not maintainer assignment or acceptance. The PR discussion and inline-comment collections were empty at qualification.

Complete original source was read at these identities:

| Path | Git blob |
| --- | --- |
| src/context/ThemeContext.jsx | a469d39947d3dcc50ca3b89b0b3355c09694409d |
| src/index.css | b85f791ce2b3da3982fceb3c397194cccdf576c0 |
| src/App.jsx | 346575654f4052d8b31610298c7ae760c7024d45 |
| src/components/ThemeToggle.jsx | d73bee4af285f2194b995970a464949760e88c4f |

App.jsx wraps the submitted ThemeToggle with ThemeProvider. The toggle consumes theme/toggleTheme and remains unchanged, including its existing button type, label and icon. The four-file proposal is original contributor work; this separate patch does not modify the external branch or submit an upstream claim.

## Concrete failure paths

The lazy state initializer reads localStorage without handling an exception. Browser storage access can be unavailable under an origin or persistence policy, so that read can abort initialization instead of reaching the existing system-preference fallback. Any truthy saved value is also accepted, even though the provider and toggle support only light and dark.

The effect changes the document's dark class and then performs an unguarded storage write. A failed persistence operation can throw from that effect despite the selected class already being applied. Saving the preference is not necessary to keep the current mounted UI usable.

The stylesheet declares color-scheme: light dark for both selected themes. That allows browser-provided controls and scrollbars to follow the browser's chosen scheme while the application colors follow html.dark, including when the user explicitly chooses the opposite theme. These are source-derived paths, not observed browser failures or visual measurements.

## Correction

The initializer wraps only window.localStorage access and getItem in a try/catch. It accepts exactly light or dark; a missing, empty, invalid or unreadable preference reaches the existing matchMedia fallback. The no-window branch still returns light. There is no storage deletion, probing, fallback storage provider or retry.

The effect retains the existing document-class update first. Only window.localStorage access and setItem are caught afterward. If persistence is unavailable, React state and the class still reflect the selection. A later theme change makes its ordinary one persistence attempt; this adds no background retry policy or persistence-success claim.

The root stylesheet now declares color-scheme: light, while html.dark declares color-scheme: dark. This follows the same selector that switches the existing custom properties. Colors, layout, transitions, responsive rules, markup, toggle logic and other CSS remain unchanged. Browser user overrides and forced-colors behavior are not certified.

[Mozilla's localStorage documentation](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage) describes SecurityError when an origin or browser policy prevents access. [Its color-scheme reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/color-scheme) explains the effect on browser-provided UI. Those references support the API boundaries, not a claim of local browser execution.

## Integration and scope limits

The original browser assumptions remain: matchMedia and document/classList must exist in the client environment. This patch does not add a system-preference change listener, cross-tab storage synchronization, an automatic system mode, root-class restoration on provider unmount or coordination among multiple providers. It does not claim to fix server/client hydration differences or first-paint theme flashes. Only the existing initializer and persistence effect are changed.

The untruncated 759-entry tree retains root App.tsx `9d90c939a186a17f5bc042b50191b554357b6f6c` alongside the new App.jsx, and package.json `f0325832d3e5150375bd22481e577d19cd148eb6`. Their complete bytes were already retained. The proposal's App.jsx is a separate placeholder application; production entrypoint resolution, stylesheet loading and integration into the existing application have not been established or supplied. No whole-screen or deployed feature completion is claimed.

The same tree identifies already-read CONTRIBUTING.md `1e015aa7e145db0cd0e306f7032cce130b8acbb8`, LICENSE `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` and README.md `374ffef680426f41b9f3e832059106839cfc72bd`, with no AGENTS.md or nearer instruction/license. CONTRIBUTING is a scaffold placeholder; root LICENSE is Apache 2.0 while README presents an MIT badge. Those discrepancies are retained. This packet republishes only an attributed patch and guide, not complete upstream modules or an invented licensing conclusion.

## Text verification

The serialized patch has 2 production paths and 4 hunks, +13/-4 lines. It applies exactly to both complete preimages and reverses exactly. The resulting identities are:

| Path | Postimage Git blob | UTF-8 bytes |
| --- | --- | --- |
| src/context/ThemeContext.jsx | f7d6cb77be85437fd42ee263f1ae0769775ecc0d | 1349 |
| src/index.css | d8d332fa6875d0d90ddee3f43cbd5545b97d50ab | 1379 |

Independent reasoning considered the supplied source contract and found no concrete ordering issue; that is not execution or acceptance. No production function, fixture, synthetic storage event, browser, DOM renderer, visual check, accessibility test, build or workflow ran. No actual stored preference, browser account, customer data, credentials, wallet or payment was accessed. Original authorship, assignment and upstream acceptance remain separate, and issue #285/PR #643 remain broader than this correction.
