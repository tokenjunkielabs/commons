# Human Connection: put author information after post content

[Issue 2363](https://github.com/Human-Connection/Human-Connection/issues/2363) explicitly places feed author information after the category/count/menu footer, and post-page author information immediately before comments. The inspected current templates put author information before the title in both views.

[Commons 31626](https://github.com/woahwhattheheck/commons/pull/31626) moved the unchanged feed author block after its existing footer. This continuation moves the post page's existing author/menu section and following spacer intact to immediately before comments. It changes no props, slots, ownership checks, menu actions, scripts or styles.

This packet addresses author placement in the two stated views. It does not implement the rest of the post-page order, center or resize shout/emotion controls, reorder categories and hashtags, introduce a floating action button, or claim the whole redesign.

## Exact source and composition

Current upstream master was independently observed at `72a8f3d7f567442ca5e191672abfb47ea1b825a6`. Complete source was acquired and its bytes independently matched before either relocation.

| Source | Exact Git blob |
| --- | --- |
| Original `webapp/components/PostTeaser/PostTeaser.vue` | `1626f66a2a27b51e604c274c78492cf12b4e83cf` |
| Unchanged 31626 / current feed postimage | `b5d57358ca80185648f027bfab2f96ca47844347` |
| Original `webapp/pages/post/_id/_slug/index.vue` | `a8266d8442b604510301b88faa1d4af49ee1ab43` |
| New complete post-page postimage | `b1ea265aa4a101e4a6e84b36b124f4612798f3a2` |
| Unchanged outer route `webapp/pages/post/_id.vue` | `92795606f1c88f9672c804953478d2a8ad659b70` |

The path locators came from root's retained 1184-entry untruncated PR4560 tree `d038ea2a13f8e1377c52f460ccdc741c2a89980b` at commit `54aba061f1de63280da28c0a09df60eacd271562`. That PR's changed paths do not include these templates. Current selected source blobs were then acquired independently and matched the tree identities; the historical tree was not substituted for a current source read. The separate Commons31623 clipboard cleanup remains untouched.

The feed source remains exactly the 5231-byte result released in31626, head `3066e4d768ed82e8d9198cd035b0db0f2cec6b5b`, merge `51a6f45b8402ddd45471c9e70fe2d7eab130dcb9`. The new post-page source is 9417 bytes, the same length as its input. The original author/menu section keeps its date-time slot, edited marker, client-only content menu, ownership flag, resource, modal data and pin/unpin listeners. The adjacent existing small spacer moves with that section. Comment list/form markup and the blocked-user path remain unchanged.

For each source, removing the one moved block yields identical remaining bytes. The entire script and style sections are byte-identical. The hero-image slots, sensitive-image controls, title/content binding and all action implementations remain unchanged. This establishes a template relocation, not rendered-browser behavior.

`change.patch` is now the cumulative four-hunk +22/-22 patch over both original input files, 2923 bytes, Git blob `27d1aedbe975ee42f3cffa3bf093ffc801035bfd`. It includes the accepted feed +3/-3 movement and the new page +19/-19 movement. Its serialized hunk offsets, context, removals and additions reconstruct both complete postimages. It replaces31626's feed-only patch `f743bc3a23a417b509e85d41a8570fc154429596`; do not apply both patches.

## Requirement and contributor chronology

The issue's full body and all two comments were read. It was OPEN/unassigned, created2019-11-26. A stale-bot notice was followed by collaborator alina-beck's [comment578719189](https://github.com/Human-Connection/Human-Connection/issues/2363#issuecomment-578719189), asking to keep it open. No implementation, PR, commit or source file was named. The written layout orders supply the requirement; the inspiration screenshot was not fetched or visually inspected.

The exact PR query `repo:Human-Connection/Human-Connection is:pr 2363` returned four closed matches, incomplete_results false: dependency updates2709/720/747 and old disabled-posts WIP755. No returned title/body supplies this redesign. Exact public Human-Connection+2363 activity search returned zero/provider END. These bounded observations are not universal contribution clearance. The same internal operation continues; no upstream source, PR, assignment or contact was changed.

Root previously read complete CONTRIBUTING.md `ae1150aa6eba6b747a06a58202635df586c55424` and transferred its normative requirements as a summary, not as full-file bytes. Upstream work requires availability coordination/discussion, issue/branch ownership, tests, linter/backend/frontend/end-to-end checks, independent approval and coordination before modifying someone else's PR. Bounty eligibility requires a prior free approved-and-merged PR and the relevant compensation label; invoicing follows approved upstream merge. This Commons source packet performs none of those upstream acceptance steps. The retained full tree contained no AGENTS or nested contribution/license files; this is not a new current whole-tree policy scan.

## Limits and attribution

31626's original scope was feed-only. This continuation adds the separate post-page author placement; it does not retroactively broaden31626's validation. The remaining post-page category/tag/shout/emotion order, centering, mobile sizing and floating-action-button requirements remain outstanding. Visual spacing, keyboard/focus behavior and layout on actual devices are unverified.

No Vue/Nuxt execution, browser interaction, tests, lint, build, workflow, account or application network operation was performed. No upstream contribution, current reward eligibility, payment or whole-issue completion is claimed. The bounty label supplies no numeric current offer.

Human-Connection gGmbH and original contributors retain credit. The exact complete MIT LICENSE.md `646ae3a6d4eb43273146cf8fef10819c14a82958`, 1095 bytes, was transferred from root's read source, independently matched and remains unchanged. No old runtime evidence is relabeled as validation of these source movements.
