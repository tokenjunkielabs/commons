# Render removable dashboard cards from their existing context

This is a source continuation for [Protocol-Guild/PayD issue #319](https://github.com/Protocol-Guild/PayD/issues/319) and SrvFernandes's existing [PR #667](https://github.com/Protocol-Guild/PayD/pull/667). The submitted dashboard renders fixed cards while its remove buttons update a separate, empty context array. This patch connects the displayed cards to that state and resolves the submitted stylesheet imports.

## Provenance and scope

Issue #319 was observed OPEN and unassigned. Its body requests frontend components, state management and mobile responsiveness. The two comments are third-party activity: a generic assignment proposal and the original author's link/claim for #667. They do not establish maintainer assignment, acceptance or payment. PR #667 was OPEN/unmerged at `c534ab3fe2ce22b897fcbdc10dd96bf3a8f07117`, based on `171c74b454daba241bfb75f36d10a0a3a77a68e5`; the issue-comment and inline-comment collections on the PR were empty.

The original author supplied the dashboard, context, removable-card component and both stylesheets. This separate Commons packet credits that work and changes only the wiring needed for the submitted component bundle.

Three complete production files were read at that exact head, together with the complete root application:

| Path | Original Git blob | Patched Git blob |
| --- | --- | --- |
| src/components/Dashboard.jsx | a8e74857b3f64f0b4bc95f74236321202c6ea7ae | 40f806cd73e86c220c93606a32a0e87a9735d34f |
| src/components/DashboardCard.jsx | 29a1d971762ab3048987d8c766cca2dd4baf8ab5 | 872f5813c34bbdb7b62733c3aef67b84ce0cd4f3 |
| src/context/DashboardContext.jsx | 6f997e14d691f170a0392f86ee99cc3be569caee | acca65da2a46b4042abb4b77ab5b59ff69542112 |
| src/App.tsx | 9d90c939a186a17f5bc042b50191b554357b6f6c | Unchanged |

The native five-file PR diff contains the complete added stylesheet hunks, and the untruncated 761-entry head tree identifies `src/styles/Dashboard.css` at `9260a15d6eb8b69e26cfdd67b1c303637987851a` and `src/styles/DashboardCard.css` at `ae0bbc2a96f605d602fc1b25d4923373b1ff8162`. No stylesheet bytes are changed.

## State and import correction

Previously, DashboardProvider initialized `cards` to an empty array. Its existing `removeCard(title)` filters that array. Dashboard nevertheless rendered three hardcoded DashboardCard elements, so changing the array could not change those rendered elements.

The provider now accepts an optional `initialCards` prop, defaulting to the prior empty-array behavior for other callers. Dashboard passes its original three cards as a stable module-level seed: Overview, Analytics and Recent Activity, with their original paragraph content. A child beneath the provider reads `cards` from DashboardContext and maps that array to the rendered cards. Removing a title therefore changes the same collection used for rendering.

The seed is initial state only. There is no effect that resets the collection after deletion or overwrites later additions. A new provider mount starts from the seed again; persistence, restore controls and updates to an initialCards prop after mounting are outside this change. Existing addCard and removeCard implementations remain byte-identical. The original three titles are distinct and serve as the rendered keys. Arbitrary duplicate titles retain the original remove-by-title behavior, which removes all matching entries; this patch does not introduce a new identity model.

Dashboard also imports the original grid stylesheet from `../styles/Dashboard.css`. DashboardCard's import is corrected from the nonexistent adjacent `./DashboardCard.css` to the actual `../styles/DashboardCard.css`. The card markup, remove handler, default removable flag, accessible label and original CSS rules remain unchanged. Import resolution and state consumption are source-level findings; visual layout and accessibility acceptance were not exercised.

## Application boundary and checks

The complete `src/App.tsx` at the PR head does not import or mount this Dashboard. It retains the existing application routes and design-system usage. This packet does not invent a route or replace that application. It fixes the proposed component bundle if it is mounted; it does not claim that the currently routed product has a working removable dashboard or that all of issue #319 is resolved.

The three-file serialized patch has 3 hunks and +28/-19 production lines. It applies exactly to the complete retained preimages and reverses exactly to them. Independent Git blob calculations match the acquired preimage identities and the postimage identities above. Those are text and identity checks only: no React rendering, production-code execution, build, dependency installation, tests, fixtures, browser, responsive screenshot or keyboard interaction was performed.

The same head tree identifies the already-read root instruction/licensing files: CONTRIBUTING.md `1e015aa7e145db0cd0e306f7032cce130b8acbb8`, LICENSE `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`, and README.md `374ffef680426f41b9f3e832059106839cfc72bd`. No AGENTS.md or nearer instruction/license appears in that complete tree. CONTRIBUTING.md is a scaffold placeholder. LICENSE contains Apache 2.0 while README presents an MIT badge. The discrepancy is retained; only an attributed patch and this guide are published, with no full source-module republication or invented license resolution.

No upstream PR mutation/submission, issue assignment/claim, external contact, account, credential, customer/employee input, financial data, wallet, payment, award or native acceptance action occurred. The original PR and the project's external contribution conditions remain separate.
