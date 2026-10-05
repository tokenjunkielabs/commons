# Gitea PR39280: parent path for renamed-file old-side comments

Source continuation over [realuca660-pixel's existing PR39280](https://github.com/go-gitea/gitea/pull/39280), head `e2efbaf09c93257f18ef74f154fffea05a733595`. The external PR remains its author's OPEN/unmerged work. This packet does not select a carrier, mutate a contributor branch, submit upstream, or claim an award/payment.

## Actual path chain

- `templates/repo/diff/box.tmpl` puts `DiffFile.Name`, the displayed new filename, in `data-path`. `repo-issue.ts` sends that path and converts the left control to `side=previous`.
- The controller requires a positive submitted line and a recognized side, then converts previous-side lines to negative. The service uses the commit's first parent and resolves the full commit SHA.
- Before this change, `commitCommentPatch` passes the displayed new path to both `GetFileDiffCutAroundLine` and its parent-blob fallback. The former constrains Git's diff to that one path. For a renamed file, the displayed new name does not identify the old file in the parent tree; the old coordinate can therefore be rejected or looked up under the wrong parent filename.
- Displayed threads and replies intentionally use the stored new `TreePath`: `LoadCommitComments` groups by it and matches `DiffFile.Name`; the reply form reuses it. Changing that stored key to the old name would break that association.

This independently qualifies the source concern in [automated comment3963734736](https://github.com/go-gitea/gitea/pull/39280#discussion_r3963734736). The automated finding itself is not maintainer approval or runtime evidence.

## Correction

Only `services/repository/commit_comment.go` changes (+36/-2). For a negative line with a parent, the existing `gitdiff.GetDiffTree` API supplies the exact parent-to-commit rename map using the same configured rename-similarity threshold. A record must have status `renamed` and its decoded `HeadPath` must equal the submitted displayed path before its `BasePath` is used. There is no new client-supplied old path.

The local decoder follows the pinned `modules/git/parse.go` pattern: quoted Git path fields use `strconv.Unquote`; unquoted paths pass through unchanged. [Git's raw diff-tree documentation](https://git-scm.com/docs/git-diff-tree#_raw_output_format) documents source/destination fields and quoted unusual pathnames without `-z`. This decodes metadata; it does not invent or normalize a filesystem path.

For a matched rename, the service skips the misleading one-path diff and uses the existing parent-blob context generator on the mapped original path. This intentionally stores a context snapshot, not a reconstructed two-file rename diff. `CommentAsDiff` parses that stored patch's first file/sections without requiring its header path to equal the comment's display key. The persisted `TreePath`, signed line, full SHA, IDs and attachments remain unchanged. Positive-side and successful non-rename paths keep the existing diff/fallback flow.

## Integration and composition

Apply `change.patch` over the exact external head, whose service preimage is `1323c86a8ab48a7e6e2d94cc11b0bc02f7d76c41`. The complete postimage is included at `services/repository/commit_comment.go`. If the carrier has moved, compose this hunk with its current source rather than overwriting it.

The [separate delegated-delete continuation](../gitea39280-delete-target-20261005-7ca6/README.md) changes a TypeScript listener and composes independently. Keep PR36862's different storage/migration/template contribution separate from PR39280. MIT copyright and license are retained in `LICENSE`.

## Source evidence and acceptance limits

Pinned source read: service above; request/controller, box/form/reply templates and browser payload; diff model/parser, comment grouping and patch reader in `services/gitdiff/gitdiff.go` (`e9f15b9838356d6857aaefa93231742d4bc074e5`); raw diff API in `modules/git/diff.go` (`86b25cc8860ee564dc675dad1bd5d35ca99417c5`); rename-map API/parser `services/gitdiff/git_diff_tree.go` (`7708be20682bffeeec34114344d847454ad7266f`); quoted-name decoding precedent `modules/git/parse.go` (`045caf0bedb50258d6f72fc68f7b99e56a3b53be`). Current AGENTS, contribution/development/backend guidance and MIT license were read.

This adds one raw diff-tree operation to old-side comment creation, including ordinary non-renames; no timing or capacity claim is made. Mapping/read/decoding errors propagate instead of falling back to a guessed path. The existing context generator's line-range and patch-formatting behavior is inherited, not redesigned here. Copy detection, alternate merge parents, expanded-diff rendering, base conflicts, migration/review decisions and complete feature acceptance remain outside this correction.

Root-commit rejection, submitted side/line validation, existing permission checks, transaction/attachment behavior and stored grouping keys remain unchanged. No build, Go formatter, lint, test, fixture, browser, native Git/DB call, workflow or upstream action was performed. Native behavior, upstream manual/check/screenshot/disclosure requirements and acceptance remain unperformed.
