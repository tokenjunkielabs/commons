# Publish a source change with native GitHub tools

`host/connected_github_publish.cjs` packages the connected-tool publication path
used by cloud sessions: current base → exact file-version comparison → blobs →
tree → commit → new branch → pull request → optional merge → source readback.
It needs no Git checkout, shell command, credential export, package install, or
network client. The caller supplies the actual discovered GitHub tool bindings.

Use this for an already-authorized change to regular source files. Existing
repository rules, source ownership, permission boundaries, and required product
execution still apply. The helper does not grant permission or decide whether a
change is ready. It does not discover tools, merge another worker's patch,
delete files or branches, update existing refs, run tests, or deploy anything.

## Call contract

Read the current native tool definitions before first use. The shipped adapter
uses the installed `mcp__codex_apps__github_*` schemas for `fetch`, `fetch_file`,
`create_blob`, `create_tree`, `create_commit`, `create_branch`,
`create_pull_request`, and optionally `merge_pull_request`. A caller may supply
`options.bindings` to map these action names to equivalent observed bindings;
their argument and result contracts must remain the same. A partial discovery
is not an account-permission verdict: keep doing useful independent work and
repeat discovery until the required bindings are present.

From a Node host that already has those native tool bindings:

```javascript
const {publishGitHubChange} = require('./host/connected_github_publish.cjs');
const result = await publishGitHubChange(tools, {
  repository_full_name: 'OWNER/REPOSITORY',
  base_branch: 'main',
  branch_name: 'work/YOUR-UNIQUE-OPERATION',
  title: 'Describe the resulting behavior',
  body: preparedPullRequestDescription,
  commit_message: 'Describe the source change',
  files: preparedFiles,
  merge: true,
  merge_method: 'merge',
}, {onProgress: state => retainOperationProgress(state)});
```

`preparedFiles` is a nonempty array of:

| Field | Meaning |
|---|---|
| `path` | Repository-relative regular-file path. |
| `content` | Complete UTF-8 source string, or base64-encoded binary bytes. |
| `encoding` | `utf-8` by default; `base64` is also supported. |
| `expected_blob_sha` | Exact Git blob SHA read before editing; explicitly `null` for a new file. |
| `mode` | Optional `100644` or `100755`; otherwise retain the existing mode, or use `100644` for a new file. |

Pass actual prepared source, not excerpts. The expected SHA identifies the
**previous** file; the native blob writer supplies the new SHA. Base64 input
must use ordinary padded encoding without line breaks. UTF-8 input rejects
unpaired surrogate characters instead of silently changing them.

`merge` defaults to `false`, leaving a normal open PR when that is the requested
outcome. For Commons work that is already authorized to land under `RULES.md`,
pass `merge: true`; this is a call option, not an added review gate. The helper
uses the newly created commit as `expected_head_sha`. Merge methods are `merge`,
`squash`, or `rebase`, subject to the repository's existing settings.

In a code-mode runtime without filesystem imports, first fetch the complete,
trusted source through the connected file reader and verify its returned Git
blob identity, as with any source loaded into that runtime. The file contains
no imports and can then be loaded in that isolate:

```javascript
const {publishGitHubChange} = new Function(
  trustedCompletePublisherSource + '\nreturn {publishGitHubChange};'
)();
const result = await publishGitHubChange(tools, preparedChange, {
  onProgress: state => store('my-operation-publish-progress', state),
});
text(result); // Source content and the PR body are not copied into progress.
```

## What it preserves

The helper reads the current base branch once, then traverses its exact,
nonrecursive Git trees. Every required tree must be complete. It compares every
source file with the caller's expected version **before the first write**. This
lets unrelated main-branch changes compose naturally while stopping an obsolete
postimage from overwriting a changed file. A mismatch gives the path and the
expected/observed SHA; read the changed source and compose deliberately.

All provider writes are sequential. The commit has the observed base as its
parent. Existing file modes are retained. The branch primitive creates a new
branch; use a unique operation name. There is no force-update or overwrite path
for an existing branch. Identical source/mode changes return
`status: no_source_changes` without a tree, commit, branch, or PR.

Readback compares each changed file's native Git blob SHA at the returned merge
commit, or at the published commit when the PR stays open. `readback_ref` names
that exact source snapshot. It does not claim that a later current-main tip is
unchanged, that a running service reloaded it, or that it is deployed. Source
execution and product acceptance remain the caller's work.

## Failures and continuation

No provider error is automatically retried. The helper throws
`GitHubPublishError` with `progress`, the original `cause`, and the last native
`response` when one is available. Progress records the stage, call counts,
previous/new file SHAs, tree/commit, branch creation, PR, merge result, and all
readback outcomes. It does not include source contents or the PR description.

```javascript
try {
  const result = await publishGitHubChange(tools, preparedChange, options);
  text(result);
} catch (error) {
  store('my-operation-publish-progress', error.progress);
  text({message: error.message, progress: error.progress});
  // Inspect error.cause / error.response privately when needed.
}
```

**Do not blindly rerun a failed publication.** A timeout can occur after a
provider accepts a write. Reconcile the named branch, PR, or merge before
continuing with the existing native tools. For example, a readback failure after
`merge_result.merged: true` does not mean the merge failed; finish the readback.
A branch-creation failure does not authorize replacing that branch. An account
or integration-scope error is specific to the observed operation, not a reason
to invent a new login or declare all tools unavailable.

The optional `onProgress` callback receives copied metadata after completed
steps. Its errors are collected in `progress_callback_errors` and do not block
the already-authorized publication. This is an observer, not a dispatch or
approval mechanism. Durable execution/restart is not built in; retain progress
using the existing host and reconcile provider truth after interruption.
