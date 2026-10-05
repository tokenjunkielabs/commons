# Gitea #1872 / subgroup-stack merge-readiness handoff

Captured: 2026-10-05T15:31:59Z

## Ownership and money truth

- Marketplace: Algora
- Canonical issue: https://github.com/go-gitea/gitea/issues/1872
- Existing claim carrier: https://github.com/go-gitea/gitea/pull/35265
- Existing frontend/integrated carrier: https://github.com/go-gitea/gitea/pull/37630
- Both carriers belong to **GamerGirlandCo**. That contributor retains authorship, the active Algora claim, submission custody, and all payment rights.
- Advertised marketplace funding: **$980 total** across five visible offers ($500 + $250 + $100 + $80 + $50).
- Awarded / invoiced / received by this packet: **$0 / $0 / $0**.
- This operation creates no Algora attempt or claim, no source implementation, no upstream comment, no fork branch, and no competing PR.

## Fresh pinned state

| Item | PR #35265: models/API [1/3] | PR #37630: frontend/integration [2/3] |
| --- | --- | --- |
| Author | GamerGirlandCo | GamerGirlandCo |
| State | OPEN, non-draft | OPEN, **draft** |
| Head | `4ef5a231667525c1c544fba65c9793a713ced25c` | `d80be732155c4f18a777c8ffcee8757198f54a93` |
| Current upstream main observed | `e8d2c493bbdb4863e6aa73352167b2416d236c11` | `e8d2c493bbdb4863e6aa73352167b2416d236c11` |
| Last head activity | 2026-07-02 | 2026-07-02 |
| Merge metadata | mergeable=false; rebaseable=false; dirty | mergeable=false; rebaseable=false; dirty |
| Size | 117 commits; 147 files; +57,222/-1,301 | 237 commits; 214 files; +60,265/-2,930 |
| Reviews | 0 approvals; COMMENTED reviews only | no reviews |
| Gate | `lgtm/need 2`; pending `giteabot/lgtm` | `lgtm/need 2`; pending `giteabot/lgtm` |
| Head checks | 22 completed: 20 success, 2 skipped | 22 completed: 20 success, 2 skipped |

The successful checks are real historical receipts for the pinned July heads, not evidence that either branch reconciles cleanly with October main. GitHub currently reports both branches dirty and non-rebaseable.

## Dependency and review map

1. **PR #35265 is the first carrier.** Its body identifies it as part 1/3: models, permissions, path handling and API. PR #37630's body identifies the conceptual stack as `main -> #35265 -> #37630`.
2. **PR #37630 is cumulative and much larger.** It adds web routes, templates, group settings, dashboard filtering and the reorderable group/repository tree. It currently contains 237 commits and 214 files and remains draft.
3. **Maintainer review is not complete.** Neither carrier has an approving review, and both retain the two-approval label.
4. **Current review discussion must be triaged after synchronization.** On #35265, one human reviewer questioned the extra Swagger endpoint and the generic `Group` type name; bot review comments attached to the current head also identify path-parsing, URL-generation, permission-query and error-handling risks. These are review inputs, not accepted findings or proof of defects.
5. **Re-test the last reported UX edge.** The latest #37630 tester comment reported that filtering the parent-group dropdown removed keyboard selection and Enter created at root. Later commits exist at the same final July head, but the thread contains no subsequent tester confirmation for that exact keyboard flow. Treat it as a re-test target, not a confirmed current bug.
6. **Algora acceptance includes a demo-video requirement.** The marketplace bot's current issue instructions require a short demo video in the claiming PR. This packet supplies no video and does not alter the existing claim.

## Exact next action for the original carrier owner

1. Fetch current `go-gitea/gitea:main` and synchronize the original **part 1** branch first.
2. Record actual conflict paths. Resolve them on the original branch without flattening another contributor's authorship or moving the Algora claim.
3. Re-run the repository's normal current checks on the new part-1 head. Re-read each still-positioned review comment against the post-rebase source; close only comments whose underlying condition is actually gone.
4. Restack/synchronize the original **part 2** branch on the updated part-1 work, preserving the existing branch history and PR. Do not open a new #1872 implementation PR.
5. Exercise the known web flows, especially:
   - create root group and nested group;
   - move group to root and another parent;
   - reject self/descendant cycles;
   - create/move repository in a group;
   - organization dashboard “All” route;
   - parent-group dropdown filtering and keyboard-only selection;
   - group deletion;
   - clone, go-get, LFS, compare and issue/code links for grouped repository paths.
6. Push only to the existing carriers, verify fresh SHA/check results, attach the required short demo video to the existing Algora-claiming PR, mark #37630 ready only when appropriate, then request the two maintainer approvals.

## Evidence links

- Issue and bounty thread: https://github.com/go-gitea/gitea/issues/1872
- Part 1 PR: https://github.com/go-gitea/gitea/pull/35265
- Part 2 PR: https://github.com/go-gitea/gitea/pull/37630
- Part 1 latest DB/check run: https://github.com/go-gitea/gitea/actions/runs/28621926299
- Part 2 latest DB/check run: https://github.com/go-gitea/gitea/actions/runs/28624170501
- Last tester UX report on part 2: https://github.com/go-gitea/gitea/pull/37630#issuecomment-3027865774

## Boundaries

No local or hosted Gitea run was performed by this operation. No source mutation, rebase, conflict resolution, demo recording, acceptance, award or payment is claimed. The historical CI counts were read from GitHub at the pinned heads. Current merge metadata and review state were re-read before publication. This is a durable blocker/dependency handoff for the original author, not a competing deliverable.
