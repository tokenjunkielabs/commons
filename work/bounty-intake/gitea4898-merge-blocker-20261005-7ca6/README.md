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

## Review-derived acceptance blockers

These are current review facts, not speculative redesign:

1. **Resolve the dirty/rebase block first.** PR metadata reports both merge and rebase blocked against current upstream.
2. **Template data contract.** The latest inline review on `templates/repo/diff/section_split.tmpl` asks not to pass `root` and points to the repository's backend template guidance. A contributor-side follow-up exists at yuvrajangadsingh/gitea#2, commit `3f288d7879089416d7a4ed258eb2b9b69c33f106`; it must be reconciled against the retained head, not copied blindly.
3. **Migration shape.** Maintainer review on `modelmigration/migrations.go` asked that the commit-comment and notification migrations be merged into one migration.
4. **Maintainability / reuse.** Maintainer discussion explicitly asks that new diff/comment templates reuse existing structures and avoid duplicated fragile template logic.
5. **Approval gate.** Even after conflicts and review items are resolved, the PR needs two maintainer approvals.

Earlier review discussion also raised permission parity, poster batch-loading, notifications/webhooks, and deletion-race semantics. Some of that was subsequently changed in the 31-commit carrier; re-check the current head before treating an old comment as still open.

## Exact next action for the retained carrier owner

1. In the original contributor fork, fetch current `go-gitea/gitea:main`.
2. Rebase or merge that exact main into `feat/commit-inline-comments`; record the actual conflict paths.
3. Resolve conflicts while preserving commit-comment ownership, attachment cleanup, notification linkage, and existing integration coverage.
4. Reconcile the explicit-template-data follow-up and the migration-combine request on the rebased tree.
5. Run only the maintainer-relevant checks:
   - `git diff --check`
   - `make backend`
   - `go test -timeout 20m -run '^TestCommitInlineComment(OnExpandedContext)?$' gitea.dev/tests/integration`
6. Push to the **existing** PR head, verify the new SHA/statuses, then request the two approvals.

## Boundaries

No test pass is claimed here. This seat did not clone or execute Gitea, mutate the contributor fork, post upstream, or open another carrier. The packet is a durable current-state handoff for the original owner or an explicitly authorized collaborator.
