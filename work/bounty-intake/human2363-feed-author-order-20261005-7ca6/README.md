# Human Connection: content-first post order

[Issue 2363](https://github.com/Human-Connection/Human-Connection/issues/2363) specifies a post-page sequence of image, title, content, centered shout button, centered emotions, hashtags, categories, author information and unchanged comments. It also places feed author information after the existing category/count/menu footer.

[Commons31626](https://github.com/woahwhattheheck/commons/pull/31626) delivered the feed author movement, and [Commons31629](https://github.com/woahwhattheheck/commons/pull/31629) moved the post page's unchanged author/menu section immediately before comments. This continuation completes the remaining written source order: the existing shout and emotion controls precede hashtags and categories in separate centered rows. It removes the old two-column sizing wrappers and the page's obsolete mobile left-float rule.

The issue's separately linked smaller-mobile-emotions requirement (#2290) and floating action button (#2289) are not implemented here. This is source implementation of order and centering, not a visual or whole-redesign acceptance claim.

## Exact source and composition

The independently observed upstream master was `72a8f3d7f567442ca5e191672abfb47ea1b825a6`. Complete original templates were acquired before the prior relocations. This continuation uses their retained bytes and the exact released31629 postimage; the completed movements were not reimplemented or executed.

| Source | Exact Git blob |
| --- | --- |
| Original `webapp/components/PostTeaser/PostTeaser.vue` | `1626f66a2a27b51e604c274c78492cf12b4e83cf` |
| Unchanged31626 feed postimage | `b5d57358ca80185648f027bfab2f96ca47844347` |
| Original `webapp/pages/post/_id/_slug/index.vue` | `a8266d8442b604510301b88faa1d4af49ee1ab43` |
| Released31629 page preimage | `b1ea265aa4a101e4a6e84b36b124f4612798f3a2` |
| New complete page postimage | `2b30f884d438fc6a2b1bcb617885d3754264f54c` |
| Unchanged outer route `webapp/pages/post/_id.vue` | `92795606f1c88f9672c804953478d2a8ad659b70` |

Original path locators came from the retained1184-entry untruncated PR4560 tree `d038ea2a13f8e1377c52f460ccdc741c2a89980b` at `54aba061f1de63280da28c0a09df60eacd271562`; its changed paths exclude these templates. Selected source bytes were then acquired independently at the observed master and matched those identities. That historical tree is not claimed as a newly fetched current whole-tree inventory. The separate31623 clipboard continuation remains untouched.

Two additional complete components were read at the same pinned upstream commit to resolve the centering contract:

| Component | Git blob | Source fact |
| --- | --- | --- |
| `webapp/components/ShoutButton.vue` | `8974010c3f360a653f9ffddd1f565969a934674c` | Root spacer has the existing text-centering class; no fixed component width is imposed in this file. |
| `webapp/components/Emotions/Emotions.vue` | `e75c8848ddea697ab0ec9a07be64de4686e75ecb` | Root emotion-button group is a flex container with no fixed width in this file. |

The Emotions directory supplied its actual file identity before the full component read. Both complete source texts independently matched their native Git blobs. Their scripts and styles were read as source only; neither component is changed or executed.

## Change and static checks

The prior shared `ds-flex` row assigned75% to emotions and15%/22% to shout on larger breakpoints, with100% fallback sizes. Those sizing wrappers are removed entirely. Each unchanged control now sits in a native `post-interaction` wrapper. Page-scoped CSS supplies `display:flex` and `justify-content:center`; the old page-only `.shout-button { float:left; }` media rule is removed. This avoids carrying the previous side-by-side widths or left float into the requested rows.

Shout remains conditional on `post.author`, with exactly the same disabled, count, current-user and post-ID bindings. Emotions retains the same post prop. The complete hashtag and category/language blocks move intact. Image controls, title/content bindings, author date/edited/menu fields and comment list/form/blocked-user markup are unchanged. The entire4340-character script is byte-identical, as are all styles outside the explicit centering addition and obsolete float removal. The author-through-comments section is byte-identical. The feed source remains exactly the5231-byte31626 result.

The new page is9138 UTF-8 bytes. The continuation patch over31629 has four hunks,+26/-31. The cumulative patch over the two original upstream inputs has six hunks,+47/-52,5117 bytes, Git blob `5b450c93c3e5adde0c88f86866849058e856231b`. Parsing its actual serialized offsets, contexts, removals and additions reconstructed both complete postimages exactly. The continuation patch independently reconstructed the page from its31629 preimage. These are text and identity checks, not Vue compilation, browser rendering or interaction tests.

`change.patch` replaces31629's cumulative patch `27d1aedbe975ee42f3cffa3bf093ffc801035bfd`. Apply the new cumulative patch to the pinned original inputs, not on top of either previous patch.

## Requirement and contribution chronology

The full issue body and both comments were read during qualification. The issue was OPEN/unassigned; a stale-bot notice was followed by collaborator alina-beck's [comment578719189](https://github.com/Human-Connection/Human-Connection/issues/2363#issuecomment-578719189), asking to keep it open. No implementation, PR, commit or source file was supplied there. The written ordering is the requirement; the inspiration image was not fetched or visually inspected.

The retained exact PR query `repo:Human-Connection/Human-Connection is:pr 2363` returned four closed matches, incomplete_results:false: dependency updates2709/720/747 and disabled-posts WIP755. Exact public Human-Connection+2363 activity search returned zero/providerEND. These are bounded historical observations, not universal contribution clearance or a fresh current census. The same internal source operation continues; no upstream assignment, source, PR or discussion was changed.

Root read complete CONTRIBUTING.md `ae1150aa6eba6b747a06a58202635df586c55424` and transferred its normative requirements as a summary, not full-file bytes. Upstream work requires availability discussion, issue/branch coordination, tests and lint/backend/frontend/end-to-end checks, independent approval and coordination before changing another contributor's PR. Bounty eligibility requires a prior free approved-and-merged PR and the relevant compensation label; invoicing follows approved upstream merge. This separate Commons packet performs none of those upstream acceptance steps. The retained full tree contained no AGENTS or nested contribution/license files; no new policy census is asserted.

## Limits and attribution

The accepted31626/31629 evidence remains limited to their original movements. This continuation adds source order and centering; it does not retroactively broaden their validation. Mobile emotion resizing, floating-button behavior, device layout, focus/keyboard interaction, responsive overflow and actual visual spacing remain unverified or outside this source scope.

No Vue/Nuxt execution, browser, tests, lint, build, workflow, account or application network operation occurred. No upstream submission, current reward eligibility, payment or whole-issue completion is claimed. A bounty label is not a verified current offer.

Human-Connection gGmbH and original contributors retain credit. The exact complete MIT LICENSE.md `646ae3a6d4eb43273146cf8fef10819c14a82958`,1095 bytes, was transferred from root's read source, independently matched and remains unchanged. No old runtime evidence is relabeled as validation of these source changes.
