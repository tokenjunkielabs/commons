# Gitea PR39280: nested delete-control clicks

This is a source-only continuation over [realuca660-pixel's existing PR39280](https://github.com/go-gitea/gitea/pull/39280), head `e2efbaf09c93257f18ef74f154fffea05a733595`. That external PR remains its author's OPEN/unmerged contribution; this packet does not select it over PR36862, mutate either branch, submit upstream, or claim acceptance, funding or payment.

## Actual source defect

`templates/repo/diff/commit_comments.tmpl` (`58d5480992a931c8f7b531b38cbb957f9c966f1f`) renders a `.delete-comment` control containing `svg "octicon-trash" 14`. The actual icon (`b52a439af775584a712372ec52e06f03b7716031`) contains a nested path. The SVG renderer/normalizer preserve that structure. The shipped SVG and relevant base/comment/repository/menu styles do not disable pointer events on this control's icon.

The delegated listener in `initRepoIssueCommentDelete` tests only `e.target.matches('.delete-comment')`. A click whose target is the rendered SVG or path therefore returns before confirmation, even though it belongs to the intended delete control. This independently qualifies the current-source concern raised in [automated comment3963734745](https://github.com/go-gitea/gitea/pull/39280#discussion_r3963734745); the comment itself is not maintainer approval or execution evidence.

## Narrow correction

Reuse the already-imported `addDelegatedEventListener(document, 'click', '.delete-comment', ...)`. The existing helper resolves `e.target.closest(selector)` and passes that control to the callback. Direct clicks still resolve the same control; nested SVG/path clicks now use its `data-locale`, `data-url` and `data-comment-id`. Unrelated clicks do not invoke the callback. Using the document listener's `currentTarget` would select `document`, not the control, and would be incorrect here.

The patch changes only listener registration and removes the redundant exact-target guard/assignment (+1/-3). It preserves `preventDefault` before any await, confirmation, POST wrapper and URL, response handling, comment and conversation cleanup, and pending-review counter behavior. It makes no transport/CSRF or server authorization change. The retained route/controller still applies its existing repository/sign-in and author/admin/code-write checks; this frontend fix confers no new authority.

## Integration

- Apply `change.patch` to the exact upstream head above, whose `web_src/js/features/repo-issue.ts` preimage is `bbf32b327c0c5c48beb55c4b8dbaaa5552242fa0`.
- The complete postimage is supplied at `web_src/js/features/repo-issue.ts`. If the carrier has moved, compose only this small listener hunk with the current source; do not overwrite newer work.
- Keep the separate PR36862/migration350/template-follow-up handoff distinct. This continuation does not repair PR39280's rename-coordinate issue, base conflicts, migrations, or other review feedback.
- MIT copyright/license is retained in `LICENSE`.

## Source evidence and remaining acceptance

Inspected at the same pinned head: deletion handler and its template/initialization route; `utils/dom.ts` helper `bceda40acc2e33d8fbda95bbe7486360b344e9b2`; SVG renderer `97e04792efb865dea4daa680b70c6043bc265e12` and normalizer `4fcb11a57d0c22bd75d4ada378a1e512b1f178d4`; CSS entrypoint and relevant SVG/base/comment/repository/menu styles; actual icon; common click handlers; Fomantic initialization; existing POST wrapper; and deletion route/controller. The tree was complete (7,660 entries, not truncated).

Current `AGENTS.md`, `CONTRIBUTING.md`, frontend guidelines, development guide and MIT license were read. Upstream's manual browser checks, lint/tests, screenshots, disclosure/review and submission requirements remain unperformed here. No executor, browser, synthetic event, test, fixture, package installation, build or workflow was run. The source reasoning establishes the target-selection defect and correction; it is not a runtime pass or complete feature acceptance.
