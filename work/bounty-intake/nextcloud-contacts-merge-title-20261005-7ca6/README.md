<!--
SPDX-FileCopyrightText: 2026 OpenAI
SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Match the merge tooltip to the existing contact eligibility check

This is a one-line source continuation in Nextcloud Contacts. The current merge button uses `canMergeSelected` to decide whether it is enabled, while `mergeActionTitle` still reads `areTwoEditable`. That property is not defined by the complete component, its RouterMixin, or the registered LegacyGlobalMixin. When two editable contacts are selected, the button can be enabled while its title still asks the user to select two editable contacts.

The correction makes the title use the same existing `canMergeSelected` computed property as the button. The existing condition remains exactly two selected contacts whose address books permit modification. Existing translations, disabled state, contact loading, merge execution, and CardDAV operations are unchanged. This is a source-derived defect and correction; no rendered browser behavior has been exercised.

## Canonical source and lineage

The source was encountered while qualifying [nextcloud/contacts issue #243](https://github.com/nextcloud/contacts/issues/243), which requests linking a contact to a user. This packet does not implement or close that feature. All nine issue comments were read. The latest maintainer comment states that this repository has no more bounties and Bountysource is down; the historical $70 badge is not current payment evidence.

Current immutable source: [nextcloud/contacts at 1fad7cab](https://github.com/nextcloud/contacts/tree/1fad7cab5ed5beef5b6b752d95882c4e1c1cd8ab).

| Source | Git blob |
| --- | --- |
| Original `src/components/ContactsList.vue` | `3f4185c1aa3d4b914491c0d5d1b6465370fc0d62` |
| Corrected complete component in this packet | `35faa12bcdc630ee091cebdcf95f69d6cd5be6b8` |
| `src/mixins/RouterMixin.js` | `988c965351fb4d6f55648b6cd00fd50ec8995a8d` |
| `src/mixins/LegacyGlobalMixin.js` | `8d40071069c8040542cd037376bc79c030062dc4` |
| `src/main.js` registering the global mixin | `1151d5dbad8e644e568c02e88db5255af08447f7` |
| Existing `src/components/ContactsList/Merging.vue` | `8d2a75aaefb8b8fcbcfb837fd768e2347e4e1ae5` |
| `AGENTS.md` contribution instructions | `f85c6facc47e0a9485c27ab63a618e90a742a570` |
| Original `COPYING`, included verbatim | `ea56f0adb16b03ab38bf737bcb10404939dc8315` |

The complete corrected component retains Nextcloud's original copyright and AGPL-3.0-or-later header. The included COPYING is the source repository's unchanged license. `merge-title.patch` describes the sole production edit: one addition and one removal.

## Account-linking and publication boundaries

The current merge implementation updates the first selected vCard and deletes the second. It does not create a persistent link to an account. The existing caller requires two editable cards. This packet does not relax that condition, identify users by matching names or email addresses, invent a vCard link property, or change the read-only system-address-book behavior. Account identity, persistence, unlinking, permission, and server interoperability requirements for issue #243 remain unresolved by this bounded source review.

A bounded issue-number PR query returned two unrelated dependency contributions. That is not a repository-wide proof that no implementation exists. The source is pinned to the observed current main and the packet is limited to the directly inspected title inconsistency.

Upstream instructions prohibit unsolicited commits and require human review, agent/model attribution and a real DCO sign-off for upstream contributions. This is an internal Commons source artifact under the existing delivery authorization, not an upstream commit, PR, issue reply, bounty claim, or submission. No DCO identity or human acceptance is invented. Any later upstream submission must separately satisfy those actual contribution conditions.

## Validation scope

The complete original component and dependencies were read, the exact one-line source change was inspected, and complete prepared text was bound to Git blob identities. The current-main preimage is checked again before publication. Publication readbacks establish the stored source artifact only.

No test, fixture, application, browser, native executor, package install, build, workflow, CardDAV operation, user login, account action, email or external contact was performed. There is no runtime or whole-feature acceptance claim.

Operation: `NEXTCLOUD-CONTACTS-MERGE-TITLE-20261005-7CA6`.
Prepared branch: `work/nextcloud-contacts-merge-title-20261005-7ca6`.
