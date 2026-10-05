# Gitea #4898 / PR #36862 current-head blocker packet

Captured: 2026-10-05T14:35Z

## Ownership and money truth

- Marketplace: Algora
- Advertised amount: **$300**
- Funded/awarded/invoiced/received by this operation: **$0 / $0 / $0 / $0**
- Canonical issue: https://github.com/go-gitea/gitea/issues/4898
- Existing implementation: https://github.com/go-gitea/gitea/pull/36862
- Original implementation owner: **yuvrajangadsingh**
- Payment/submission rights remain with the original contributor. This packet creates no competing claim, attempt, source branch, or upstream PR.

## Fresh pinned state

| Item | State |
| --- | --- |
| Issue #4898 | OPEN, unassigned, `type/feature`, `issue/confirmed`, `💎 Bounty` |
| PR #36862 | OPEN, non-draft, 31 commits, 29 changed files, +1183/-30 |
| PR head | `b46f3c2d0d93e66ed03b63b0e9677d4c24ca3e99` |
| Upstream base observed by PR | `a52e5f53c096961b61e4016a35b693aa72b51339` |
| Merge state | `mergeable=false`, `mergeable_state=dirty`, `rebaseable=false` |
| Approval status | pending: `giteabot/lgtm` says “Needs two more approvals” |
| Last PR source push | 2026-08-21 |
| Latest PR conversation | 2026-08-25 |

The first actionable blocker is therefore not another feature implementation. It is to make the existing contributor's carrier current and reviewable.

## Changed-file surface on the retained PR

```text
modelmigration/migrations.go
modelmigration/v28/v350.go
models/activities/notification.go
models/activities/notification_list.go
models/activities/notification_test.go
models/repo/commit_comment.go
models/repo/commit_comment_test.go
routers/web/repo/commit.go
routers/web/repo/commit_comment.go
routers/web/repo/compare.go
routers/web/repo/pull.go
routers/web/user/notification.go
routers/web/web.go
services/convert/notification.go
services/gitdiff/gitdiff.go
services/repository/commit_comment.go
services/repository/delete.go
templates/repo/diff/blob_excerpt.tmpl
templates/repo/diff/box.tmpl
templates/repo/diff/commit_comment_form.tmpl
templates/repo/diff/commit_comments.tmpl
templates/repo/diff/commit_conversation.tmpl
templates/repo/diff/commit_conversation_row.tmpl
templates/repo/diff/new_commit_comment.tmpl
templates/repo/diff/section_split.tmpl
templates/repo/diff/section_unified.tmpl
tests/integration/repo_commit_comment_test.go
web_src/js/features/repo-issue.ts
web_src/js/features/repo-legacy.ts
```

## Review feedback reconciled with the retained source

Historical review comments are distinguished from the implementation present at the retained head:

1. **Resolve the dirty/rebase block first.** PR metadata reports both merge and rebase blocked against current upstream.
2. **Template data contract: existing follow-up available.** The latest inline review on `templates/repo/diff/section_split.tmpl` asks not to pass `root`. `marcusdytrich`'s existing [contributor-side PR #2](https://github.com/yuvrajangadsingh/gitea/pull/2), head `3f288d7879089416d7a4ed258eb2b9b69c33f106`, is based on the exact retained upstream head `b46f3c2d0d93e66ed03b63b0e9677d4c24ca3e99`. Its nine-file production patch supplies named template values, uses `ctx.RootData` for request-level data and synchronizes the POST render key as `Comments`. Preserve and reconcile that existing contribution after the upstream update; do not recreate it. The follow-up remains OPEN/unmerged.
3. **Migration-combine request: already implemented at this head.** Historical [review comment 3700162298](https://github.com/go-gitea/gitea/pull/36862#discussion_r3700162298) asked for one migration. Current `modelmigration/v28/v350.go`, blob `6581cea5e63a7730a683c5ddd02a7027eefd436b`, already defines both `CommitComment` and `Notification.CommitCommentID` and synchronizes them in one `SyncWithOptions` call. Current `modelmigration/migrations.go`, blob `9a345f221b0ff2627b1aa44482a417a5db3dade6`, registers that one migration as 350. This historical request is not a remaining combine task. Preserve its combined semantics when resolving any actual current-main migration conflict.
4. **Maintainability / reuse.** Maintainer discussion explicitly asks that new diff/comment templates reuse existing structures and avoid duplicated fragile template logic.
5. **Approval gate.** Even after conflicts and review items are resolved, the PR needs two maintainer approvals.

Earlier review discussion also raised permission parity, poster batch-loading, notifications/webhooks, and deletion-race semantics. Some of that was subsequently changed in the 31-commit carrier; re-check the current head before treating an old comment as still open.

## Exact next action for the retained carrier owner

1. In the original contributor fork, fetch current `go-gitea/gitea:main`.
2. Rebase or merge that exact main into `feat/commit-inline-comments`; record the actual conflict paths.
3. Resolve conflicts while preserving commit-comment ownership, attachment cleanup, notification linkage, and existing integration coverage.
4. Reconcile the existing explicit-template-data follow-up on the updated tree. Preserve the already combined migration; resolve actual upstream conflicts without repeating the historical combine task.
5. Run only the maintainer-relevant checks:
   - `git diff --check`
   - `make backend`
   - `go test -timeout 20m -run '^TestCommitInlineComment(OnExpandedContext)?$' gitea.dev/tests/integration`
6. Push to the **existing** PR head, verify the new SHA/statuses, then request the two approvals.

## Boundaries

No test pass is claimed here. The source reconciliation inspected the retained migration implementation/registration and all nine production patches of the existing template follow-up. It did not execute Gitea, replay the contributor's checks, mutate either contributor fork, post upstream, or create a competing implementation carrier. The packet is a durable current-state handoff for the original owner or an explicitly authorized collaborator.
