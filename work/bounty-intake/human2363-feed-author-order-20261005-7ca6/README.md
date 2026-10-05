# Human Connection: put feed author information after the content

[Issue 2363](https://github.com/Human-Connection/Human-Connection/issues/2363) explicitly lists the feed order as image, title, abstract, category/count/menu row, then author information. The current PostTeaser template instead places its client-only author block before the title. This packet moves that unchanged three-line block immediately after the existing footer.

This is the feed-order portion of the request. It adds no design assets, controls, data fetching, styles or handlers. The separate post-page rearrangement, centered shout/emotion presentation, mobile emotion sizing and future floating-action-button references remain outside this change.

## Bound source and actual change

Current upstream master was independently read as `72a8f3d7f567442ca5e191672abfb47ea1b825a6`. The complete source files were retained before parsing:

| Source | Exact blob | Role |
| --- | --- | --- |
| `webapp/components/PostTeaser/PostTeaser.vue` | `1626f66a2a27b51e604c274c78492cf12b4e83cf` | Complete 5231-byte input |
| This packet's complete PostTeaser | `b5d57358ca80185648f027bfab2f96ca47844347` | Complete 5231-byte postimage |
| `webapp/pages/post/_id/_slug/index.vue` | `a8266d8442b604510301b88faa1d4af49ee1ab43` | Complete post-page source inspected, unchanged |
| `webapp/pages/post/_id.vue` | `92795606f1c88f9672c804953478d2a8ad659b70` | Complete outer route inspected, unchanged |

These actual current blobs also match the paths transferred from root's retained 1184-entry, untruncated tree `d038ea2a13f8e1377c52f460ccdc741c2a89980b` at external PR4560 commit `54aba061f1de63280da28c0a09df60eacd271562`. That PR changes comment/content-menu/localization paths, not these post templates. Its tree was used as an existing path locator, not as a substitute for current source acquisition. The separate Commons31623 clipboard fallback remains unrelated and unmodified.

The moved block retains `client-only`, its user/date props and exactly the same component text. The hero-image slot, title, excerpt and existing footer all remain in their previous relative order. Footer categories retain their existing flex-grow and the counters/context menu retain their original markup. The entire script and style sections are byte-identical, including author checks, delete/pin actions, post navigation, image handling and all spacing rules.

`change.patch` has two hunks, +3/-3, 906 bytes, blob `f743bc3a23a417b509e85d41a8570fc154429596`. Reading the serialized hunk offsets, context, removals and additions reconstructs the complete postimage exactly. Removing the one moved block from each full source yields identical remaining bytes. This verifies a template relocation; it is not rendered-browser acceptance.

## Requirements and contribution chronology

The complete issue body and all two comments were read. The issue was OPEN/unassigned, created 2019-11-26. A stale-bot notice was followed by collaborator alina-beck's [comment 578719189](https://github.com/Human-Connection/Human-Connection/issues/2363#issuecomment-578719189), asking to keep it open. No implementation, PR, commit or source file was named there. The explicit layout order is the basis for this narrow change; the inspiration screenshot was not fetched or claimed visually inspected.

The exact repository PR query `repo:Human-Connection/Human-Connection is:pr 2363` returned four closed matches, incomplete_results false: dependency updates2709/720/747 and old disabled-posts WIP755. None of the returned title/body records supplies this redesign. This is a bounded query result, not universal contribution clearance. Exact public activity search for Human-Connection and2363 returned zero/provider END. No upstream claim, assignment, comment, PR or contact was made.

Root previously read complete CONTRIBUTING.md `ae1150aa6eba6b747a06a58202635df586c55424` and transferred its normative requirements as a summary, not as full-file bytes. They require upstream availability coordination/discussion, appropriate issue/branch ownership, tests and linter/backend/frontend/end-to-end checks, independent approval, and coordination before changing another contributor's PR. Bounty eligibility requires a prior free approved-and-merged PR and the relevant compensation label; invoicing follows an approved upstream merge. This separate Commons source packet does not perform or claim those upstream steps. The retained full tree had no AGENTS or nested contribution/license files; that historical tree observation is not a new current whole-repository scan.

The issue's bounty label supplies no numeric offer or current award. No funding, payment, reward eligibility or whole-issue completion is claimed.

## Limits and license

No Vue/Nuxt rendering, browser interaction, tests, lint, build, workflow, account or network application operation was executed. Source ordering is established; actual layout, visual spacing, focus/accessibility and mobile behavior remain unverified. The full post-page source was inspected only to distinguish the broader request; no post-page changes were invented.

Human-Connection gGmbH and original contributors retain credit. The complete MIT LICENSE.md was transferred from root's read source and independently matched to `646ae3a6d4eb43273146cf8fef10819c14a82958`, 1095 bytes. It is included unchanged. This source-only relocation is new here; no historical runtime evidence is relabeled as validation of it.
