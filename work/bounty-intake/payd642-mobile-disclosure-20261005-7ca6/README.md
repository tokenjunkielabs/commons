# PayD #287 / PR #642 — mobile disclosure state

This is an attributed source patch for the native menu button in SrvFernandes's open [Protocol-Guild/PayD PR #642](https://github.com/Protocol-Guild/PayD/pull/642), associated with [issue #287](https://github.com/Protocol-Guild/PayD/issues/287). It exposes the component's existing mobile-navigation state and identifies the mounted content region. It is not a production deployment or a claim that the broader UI/UX issue is complete.

## Exact source and attribution

The immutable donor head is `e8286ce5bd731a8d71135843538f0c2624e42af1`, on `SrvFernandes/PayD:feat/onlydust-fix-287-1790980654285`. The observed PR base field is `171c74b454daba241bfb75f36d10a0a3a77a68e5`. Current metadata at qualification reports OPEN and unmerged, with no PR discussion or inline-review comments. The issue has a separate contributor's assignment request and SrvFernandes's PR link/claim; neither establishes sponsor assignment, acceptance or current reward eligibility. The generic issue body asks for advanced React UI/state and mobile responsiveness; it does not specify a particular navigation design.

All four complete donor files were read:

| Path | Donor Git blob |
| --- | --- |
| src/App.jsx | 7f25aecdb67e0099a50d74f80e8a95eb1122d392 |
| src/components/ResponsiveCard.jsx | 0bcc1b874425495497490df7d8288073aed8d57c |
| src/hooks/useIsMobile.js | 8405b32d3196a225429d2cbe08a79bb6e8f5355d |
| src/store/uiStore.js | 6b1ab7adf6a96e18a417983fc077ca45549daedd |

Only `src/App.jsx` changes. Its complete postimage is Git blob `6681250f630729fc7b85ec428ab25fcfe6e821f5` (2,224 UTF-8 bytes). The original App, hook, card and store remain credited to the external contributor. No upstream branch, PR, issue, assignment, claim or account was modified.

## Concrete correction

The supplied button already has a native button element, an accessible label and the existing Zustand toggle callback. Its controlled links are conditionally inserted only when `mobileMenuOpen && isMobile`. The button previously exposed no expanded state.

The patch calls React's `useId` unconditionally at the component top level, derives `mobileMenuVisible` from exactly that existing condition, and uses it for both `aria-expanded` and conditional rendering. While the region is mounted, `aria-controls` points to its generated ID. When the region is absent, that optional association is omitted instead of naming a missing target.

The native button's click/keyboard behavior, visible label and glyph, the store callback, link targets, conditional mounting, CSS classes, breakpoint hook and card content are preserved. No ARIA menu roles, custom keyboard handler, focus movement or escape/outside-click behavior is added.

Primary conventions were checked directly:

- [W3C APG disclosure pattern](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/) describes an expanded-state boolean for the disclosure button and an optional association with its controlled content.
- [React useId reference](https://react.dev/reference/react/useId) documents a top-level hook for component-associated accessibility IDs. Multiple independent React roots still require their own prefix coordination where applicable; this patch does not configure roots.

These references support the attribute/ID contract; they are not evidence of this application's runtime behavior or broad accessibility conformance.

## Retained limits and publication terms

The complete 760-entry donor tree was untruncated. Its root `package.json` remains `f0325832d3e5150375bd22481e577d19cd148eb6`, already read in retained custody: it declares React ^19.2.0 but does not declare the imported Zustand package. This patch adds no dependency and does not claim an installed or working application. The tree also retains `src/App.tsx` at `9d90c939a186a17f5bc042b50191b554357b6f6c`. Selection of this added App.jsx by the actual entrypoint and generation of the utility CSS were not established.

The unchanged hook initializes from browser width and uses a default threshold of 768. The unchanged CSS uses `sm:hidden`; no CSS breakpoint equivalence, rendering, viewport or hydration result is asserted. The new state describes the existing React branch. It does not repair the hook's server/client initialization assumptions, synchronize menu state across viewport changes, alter the stored open flag, or validate links currently pointing to `#`. The component's default light theme, broader state management, responsive design and complete issue acceptance remain outside this patch.

The donor tree matches the previously fully read root CONTRIBUTING.md `1e015aa7e145db0cd0e306f7032cce130b8acbb8`, LICENSE `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` and README `374ffef680426f41b9f3e832059106839cfc72bd`. The contribution file is a short placeholder. The root license is Apache-2.0 while the README advertises an MIT badge; this packet preserves that discrepancy and does not resolve or replace upstream licensing. The qualified tree contains no AGENTS.md, RULES.md or nearer source license/instructions. Only the authored patch and this guide are published, with original provenance retained; no full external module is republished. Existing sponsor assignment, author, review and acceptance conditions remain external.

## Source-only validation

The patch has four hunks, +7/-3 production lines. Exact application to the complete pinned preimage reproduces the recorded postimage, and exact reverse application reproduces the original bytes. Independent Git blob identities match the source provider and the authored postimage. These are source-string and serialized-patch checks.

No browser, screen reader, device, React application, package install, typecheck, lint, build, unit or accessibility test was run. No real account, preference, wallet, chain, payment, deployment or upstream submission was used. Publication readbacks verify the Commons artifacts and their source identity, not native behavior.
