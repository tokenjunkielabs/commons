# Wavelum locale-control label binding

The current dashboard renders two instances of `LocaleSwitcher`, each with the same hard-coded `locale-switcher` ID. Both labels consequently reference the same document ID. This patch gives each instance one React `useId()` value and uses that value for its own `label.htmlFor` and `select.id`.

Apply `change.patch` to `src/components/ui/LocaleSwitcher.tsx` at `stellar-network-builders/wavelum-frontend@39adce49545f0114ef0ae25ad835af39de46f492`, blob `bfe4eda30a04c63ae1a4f73520e683912c9d249b`. The production change is +4/-3. Compose these hunks with newer source instead of overwriting the component.

## Source and attribution

The completed [bounty-concierge PR391](https://github.com/woahwhattheheck/bounty-concierge/pull/391) by ZZ-Sol-Halley-83 and [PR398 addendum](https://github.com/woahwhattheheck/bounty-concierge/pull/398) by ZZ-Sol-Forge retain their source-discovery/review credit. This packet implements only the addendum's per-instance label binding alternative. The underlying application remains the work of Wavelum/Lumina contributors, including the merged internationalization and accessibility contributions.

Current-source inspection confirmed the same component and caller pins named by the addendum:

| Source | Blob | Relationship |
| --- | --- | --- |
| `src/components/ui/LocaleSwitcher.tsx` | `bfe4eda30a04c63ae1a4f73520e683912c9d249b` | Hard-coded label/select ID in each instance |
| `app/[locale]/layout.tsx` | `9baf2900402704a61f09452913f673405455cf1c` | Mounts the route-level switcher above children |
| `app/[locale]/dashboard/layout.tsx` | `c06b305dc8bbe5b05bb0b9054abd8935f26d5834` | Mounts DashboardLayout within that locale route |
| `src/components/layout/DashboardLayout.tsx` | `e2c05ec46f52fbc4ba946050fe7b2fc71a9f12e8` | Mounts Header |
| `src/components/layout/Header.tsx` | `d3305d490de82d9a2d9dfd2da6fc6f10266fcbfd` | Mounts another switcher |
| `package.json` | `abd989198d17220cb482e122f8e438fe7669bf6e` | React and React DOM 19.2.3 |
| `app/globals.css` | `9f5bf2133892f16d01b43a3a5953438bbbbdcac5` | No selector referring to the old literal ID |

React's [official useId documentation](https://react.dev/reference/react/useId) describes unique accessibility IDs for repeated components. The call is unconditional at the top of the existing synchronous client component. Both associated attributes use its result. Server/client tree consistency remains the normal hydration requirement; no custom counter, random ID or new dependency is introduced.

The control count, positioning, translations, aria-label, locale values, change handler, navigation, announcements and pending state remain unchanged. The patch does not remove either switcher or claim to repair the separately identified nested-main/skip-target issue.

## Integration limits

The complete observed 293-entry repository tree was not truncated and contained no LICENSE/COPYING file. README delegates license details to an unspecified upstream repository. This packet contains a narrow original patch and guidance, not a complete republished module or an inferred license.

The exact default-branch symbol search returned no results despite the known source match. That response is inconclusive; it is not evidence that external integrations or uninspected files never select the old ID. Integrators should use the labeled control's accessible role or the actual instance ID rather than assuming a globally fixed ID.

[Issue67](https://github.com/stellar-network-builders/wavelum-frontend/issues/67) was observed OPEN/unassigned with two contributor requests and no maintainer acceptance. Its requirements include route-wide axe/keyboard checks, reports and CI. The historical GrantFox application/assignment notes remain separate from this Commons source continuation. No upstream or provider action, application, assignment, reward or payment is claimed.

Only static source reasoning and exact publication readbacks were performed. No dependency installation, app/browser execution, TypeScript/lint/build, axe/keyboard audit, test/fixture creation, workflow dispatch, wallet action or upstream submission occurred. The current root CONTRIBUTING (`ec1cf887e0908372facf837b929565a3a43b8a65`) and its docs pointer (`3f03bffbb5847a8cc96f65f058e8f11a4f60303f`) require upstream checks; those remain unperformed. This fixes one source-level binding defect and does not establish WCAG compliance or whole-issue completion.
