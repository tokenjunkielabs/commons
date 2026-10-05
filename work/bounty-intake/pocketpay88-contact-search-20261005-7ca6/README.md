# Local search on the PocketPay contacts screen

PocketPay issue [#88](https://github.com/Stellar-PocketPay/pocketpay-mobile/issues/88) asks for a local search input, matching contact names and public keys, a no-results state, and restoration of the full list when search is cleared. The current address-book route renders every contact directly and has no search input. This packet adds that behavior to the existing screen.

## Source and attribution

- Repository: `Stellar-PocketPay/pocketpay-mobile`.
- Observed source commit: `c3a24abacb45030eb4fef41aabc46b312aaf54a3`.
- Changed upstream path: `app/contacts.tsx`.
- Complete preimage: `9722843b217e96a17917dcfc2f87ea0abe6b5b81`, 18,217 UTF-8 bytes.
- Prepared postimage: `5251704233e2290c3504c79f0f863ac6e30dc850`, 19,221 UTF-8 bytes.
- Actual shared input source: `src/components/Input.tsx`, blob `d14d573ffc32202fc1fa948274bf239caac8f3bc`; it forwards native text-input props and retains its existing theme/style behavior.

The original screen and app remain the work of the upstream authors. The issue is OPEN and assigned to **Primex-hub**. All three current issue comments were read: requests by GBOYEE and Primex-hub, followed by the GrantFox bot's assignment to Primex-hub. No completed implementation or carrier was linked in those three comments. One bounded repository PR-body query for `88` returned zero results with `incomplete_results:false`; this is query-specific evidence, not a claim that no contribution exists elsewhere.

The send flow's separate `src/components/ContactPicker.tsx` already filters name/address in the `contactStore` model. This patch targets the address-book route's `useAppStore` name/publicKey model. It does not unify those stores or replace the picker. The accepted Commons #31766 recent-recipient label dependency repair remains a separate hunk, and the contemporaneous review-completion effect work remains separate.

CI's retained complete 374-entry upstream tree had no LICENSE or AGENTS file. This packet therefore publishes only the focused patch and this original source note, not a complete upstream module or a new license grant.

## Change

`change.patch` contains one file, two non-overlapping unified-diff hunks, with 27 added and 3 removed lines.

1. Keep the user's text in local `search` state and derive `searchQuery` with `trim().toLowerCase()`.
2. Recompute the filtered list when the contact list or normalized query changes. Empty or whitespace-only search returns the complete existing list. Otherwise match either the contact name or public key with a case-insensitive substring comparison.
3. Use the screen's existing `Input` component before the list. The visible label and explicit accessibility label identify both supported fields; capitalization and autocorrection are disabled.
4. Feed only the derived array to the existing `FlatList`. Keys, contact rows, deletion confirmation, form, save/update, and scanner callbacks keep their original bytes.
5. When saved contacts exist but none match, show `No contacts found` and suggest changing or clearing the query. With no saved contacts, preserve `No contacts yet` and the existing add/scan explanation.

Filtering is read-only and local. It does not persist the search, modify contact records, fetch a network resource, change addresses, or submit a transaction. The query remains in component state across list/form mode transitions; clearing its input restores the current complete contact list in its existing order. No accent folding, locale-specific collation, pagination, or cross-store search is added.

## Instructions and acceptance boundary

Relevant source instructions were read from the same commit:

| File | Blob | Relevance |
|---|---|---|
| `CONTRIBUTING.md` | `d8493281d318b348f98a9bd999c2ffd6cc966d0d` | Contributor workflow; transferred completely from retained CI custody |
| `docs/screen-test-matrix.md` | `6af9f58a8bcaa1594daf396995aaa1d8dff59313` | Existing Contacts row requires component/store/flow and visual checks |
| `docs/ui-states.md` | `c53acaa9238a52c5d5517ebe39d59034af5f4c21` | Preserve contacts' empty/add/scan and mutation states |
| `docs/accessibility.md` | `965dbee318bb12b75abdd7d62f839b18ea1443d6` | Visible/input labels, semantics and native accessibility acceptance |
| `docs/design-system.md` | `a94ed602b3cd9d2c88dc3366bddf83c6c8dcf994` | Reuse shared Input and existing theme tokens |

No new screen or reusable component is introduced, and no new colors or pixel sizes are added. The upstream required typecheck, lint, tests, device/simulator accessibility and visual review, CI, self-assessment, maintainer acceptance and campaign evaluation remain **unperformed** for this packet. This source-only Commons contribution does not satisfy those external acceptance conditions by itself. The existing screen's unrelated keyboard, scanner, state and accessibility limitations are not claimed repaired.

## Evidence and use

The complete source and actual Input implementation were inspected. The preimage and prepared postimage were independently assigned Git blob identities. The diff is anchored to the exact source above; a maintainer integrating it must reconcile any later changes to that path. No app, wallet, network, chain, browser, test suite, fixture, dependency installation or workflow was run. Source publication checks establish the exact patch and note bytes only; they are not runtime feature acceptance.

Publication in Commons preserves the upstream authors and Primex-hub assignment. It does not open an upstream PR, claim the issue, send a campaign message, contact maintainers, or claim funding, payment, ownership or full issue completion.
