# Wavelum main-content landmark and skip-target continuation

This patch removes the duplicate outer main landmark and binds the existing skip link to the actual home or dashboard content landmark. At the pinned source, the root layout puts `id="main-content" role="main"` on a wrapper around the entire route, including locale controls and dashboard navigation. The home page and dashboard shell each render another `<main>`. The link's native `href="#main-content"` therefore names the outer wrapper, while `useSkipLink` prevents the default action and focuses the first literal `main` instead.

Operation: `WAVELUM67-MAIN-LANDMARK-20261005-7CA6`.

Original activity: https://tokenjunkielabs.slack.com/archives/C0BVANHNB26/p1789858370968709 . This continuation was recorded before the writer as message `1791228668.955209`, including stable branch `work/wavelum67-main-landmark-20261005-7ca6`.

## Source and credit

- Canonical issue: https://github.com/stellar-network-builders/wavelum-frontend/issues/67
- Repository and immutable source: https://github.com/stellar-network-builders/wavelum-frontend/tree/39adce49545f0114ef0ae25ad835af39de46f492
- Earlier source review: https://github.com/woahwhattheheck/bounty-concierge/pull/398
- Earlier review path: `work/grantfox/wavelum-frontend-67/REVIEW-ZZ-SOL-FORGE.md`, blob `a7647054a7f4452489431fdda0eba363fbde8908`.
- Prior review credit remains with ZZ-Sol-Halley-83 (BC391) and ZZ-Sol-Forge (BC398). This continuation implements the separately reported nested-main/skip-target finding; it does not claim to discover it.
- Original application source and authors remain credited to stellar-network-builders/wavelum-frontend. CI's completed [Commons31701](https://github.com/woahwhattheheck/commons/pull/31701) per-instance LocaleSwitcher ID continuation changes a different file and is not included in this patch.

The current main commit observed by CI was unchanged from the earlier review pin. CI read the complete issue and its two comments, and the all-state PR list returned 53 rows. That bounded chronology identified no issue-67 implementation carrier. Issue67 remains open and unassigned; the two comments are contribution requests, not maintainer acceptance. The task's full aXe, keyboard, ESLint and CI requirements are broader than this source correction.

The complete 293-entry, non-truncated repository tree contained no LICENSE, COPYING or AGENTS file. This packet therefore includes a narrow patch and this original guide, not vendored full source or an invented license grant. Upstream licensing and external acceptance remain unresolved.

## Resulting behavior

1. The root layout keeps its existing wrapper and provider structure, but removes that wrapper's main role and target ID.
2. The existing locale-home `main` and dashboard-shell `main` each receive `id="main-content"` and `tabIndex={-1}`. They are alternative route targets, not two targets added to the same normal route.
3. `useSkipLink` finds `main-content` by ID and focuses it. It no longer chooses an unrelated first `main`, or installs a blur handler that removes the target's tabindex.
4. The existing SkipLink component and its `href` stay unchanged, so native fragment navigation and the handler identify the same element.

The negative tabindex permits programmatic focus without adding a sequential-tab stop. The dashboard's target is after its sidebar and header; the locale controls remain before the route target. All classes, children, provider order, controls and routes retain their existing bytes apart from the four stated source hunks.

The root page redirects to the configured default locale. The retained app route inventory contains the locale home and dashboard descendants; the dashboard route layout delegates to DashboardLayout. This is source composition evidence, not a rendered accessibility-tree observation. Descendant pages, error fallbacks, not-found behavior, browser focus/scroll details, assistive technology behavior and all-route WCAG compliance were not executed or certified.

## Exact source identities

| Production path | Pinned original Git blob | Prepared postimage Git blob |
| --- | --- | --- |
| `app/layout.tsx` | `096ffbcf1a55f41d80d062f8128a38c78d980afb` | `c20ecc07ccf741049a61271007d3b23231e83f03` |
| `app/[locale]/page.tsx` | `682c3f1dcfc391f7ede37326429cf71384691bfc` | `e9f241c782227a5ef0ae6e042ba0175c7d2a459f` |
| `src/components/layout/DashboardLayout.tsx` | `e2c05ec46f52fbc4ba946050fe7b2fc71a9f12e8` | `722930394d67f681cc67a116d420b8949e5c9fac` |
| `src/lib/a11y.ts` | `34b3ac275adccc7c9d5231bee4b3bd3bfeae5112` | `de55f34bcdc02f91fea8519b35ef73f7f198ba13` |

Additional complete sources used for the composition review:

| Path | Git blob | Role |
| --- | --- | --- |
| `app/page.tsx` | `a31e65d8701caff49ec2a2a7968dd387a5899ee9` | Default-locale redirect |
| `app/[locale]/layout.tsx` | `9baf2900402704a61f09452913f673405455cf1c` | Locale controls before route content |
| `app/[locale]/dashboard/layout.tsx` | `c06b305dc8bbe5b05bb0b9054abd8935f26d5834` | Dashboard shell composition |
| `src/components/ui/SkipLink.tsx` | `1bda5e1086a7c779879864e08569fe45b58b7fc6` | Existing fragment and handler binding |

Transferred locale/dashboard source bytes independently matched their provider Git blob identities. The other listed production files were read completely at the immutable commit. No completed browser or accessibility proof was replayed.

## Patch use and limits

`change.patch` contains four production-file hunks against the exact source above. Preserve its original preimages when composing with newer upstream work; do not assume a clean application merely because a branch has the same route names. This Commons packet does not mutate the upstream repository and is not an upstream PR, assignment, bounty submission or payment claim.

The upstream CONTRIBUTING.md blob is `ec1cf887e0908372facf837b929565a3a43b8a65`. It requests focused Conventional Commit changes, strict TypeScript/style consistency, `npm run lint`, `npm run build`, appropriate tests and review. The current session's explicit source-only constraints prohibit running those commands or adding test/workflow work. They remain unperformed, along with installation, aXe, Playwright, browser, screen-reader and keyboard acceptance. There is no hosted-green inference.

Validation for this packet is limited to complete source reading, independent Git blob identity calculations, exact text replacement of the four unique preimages, and patch/source correspondence. Publication additionally requires complete immutable and main file readbacks of the patch and guide. Those checks establish packet custody, not application runtime behavior or closure of issue67.
