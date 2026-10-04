# Read canonical pull-request state once

`connected_github_pr_state.cjs` reads a single pull request through the existing
native `github_fetch` action and preserves GitHub's nullable fields. It also
projects an already retained native response without another provider call.

During integration of Commons PR #31205 on October 4, 2026, the compact
`get_pr_info` action reported `mergeable: false`. The canonical REST response
reported `mergeable: null` and `mergeable_state: "unknown"` for the same head.
The normal expected-head merge then succeeded. Treating the compact value as a
conflict would have created unnecessary source work or repeated checks.

GitHub documents three values for `mergeable`: `true`, `false`, and `null`.
`null` means its background calculation is pending. This helper does not
convert that observation to `false` or choose an integration action.

## Use in connected code mode

Fetch the helper once and retain its source for the current operation:

~~~javascript
const fetched = await tools.mcp__codex_apps__github_fetch_file({
  repository_full_name: "woahwhattheheck/commons",
  path: "host/connected_github_pr_state.cjs"
});
if (fetched.isError) throw new Error("PR reader source was not retrieved");
const box = { exports: {} };
new Function("module", "exports", fetched.structuredContent.content)(box, box.exports);

const result = await box.exports.readGitHubPullRequest(tools, {
  repository_full_name: "woahwhattheheck/commons",
  pr_number: 31205
});
store("current-pr", result);
text({ status: result.status, calls: result.calls, pr: result.pr });
~~~

Use the repository and PR number of the actual task. Pin the helper's source
`ref` when retaining a particular version matters. The helper makes one native
GET to `/repos/{owner}/{repo}/pulls/{number}`. It performs no polling, sleeping,
automatic retry, secondary search, credential lookup, or mutation. Reuse the
loaded module instead of fetching it for every PR. The initial module-source
fetch is separate from `result.calls`.

Retain the result privately: `response` contains the complete native envelope,
including bodies and other metadata that the compact view omits. A provider
error response also remains available there. Printing only `status`, `calls`,
and `pr` avoids repeating the full provider response in the working context.

## Interpret fields without losing information

Nullable fields have `{present, value}` descriptors:

| `mergeable` descriptor | Meaning |
| --- | --- |
| `{present: true, value: true}` | GitHub reported mergeable at this observation. |
| `{present: true, value: false}` | GitHub reported not mergeable at this observation. |
| `{present: true, value: null}` | GitHub has not provided a computed mergeability value. |
| `{present: false, value: null}` | The supplied payload omitted the field. |

Read `mergeable_state` separately and preserve its literal string. A missing
value is distinct from a present `null`. The same descriptors preserve
`draft`, `merged`, `merge_commit_sha`, `merged_at`, and `updated_at`.

`state`, `title`, `number`, the canonical URL, and both branch refs, SHAs and
repository names are included. A deleted head repository remains `null`.
Reviewers, status checks, labels, body and other provider fields stay in the
original `response`; this is a compact view, not their absence from GitHub.

These are observed fields, not a claim that the work is ready, authorized,
accepted, or paid. In particular, `merge_commit_sha` can identify a temporary
test merge before integration. Check `merged` and `merged_at` before describing
it as a completed merge. A provider-level `false` is not by itself a diagnosis
of the exact conflicting source paths.

## Read retained responses locally

~~~javascript
const view = box.exports.projectGitHubPullRequest(retainedNativeResponse);
text(view);
~~~

The projector accepts a canonical REST PR object or the native MCP envelopes
that contain it in `structuredContent`, JSON-text `content`, or text content
blocks. It does not mutate the original object or assign a new observation
time. Keep the original request and capture time beside retained data.

The flattened compact `get_pr_info` response is intentionally not treated as
canonical REST data: once `null` has been converted to `false`, the original
value cannot be reconstructed from that summary. Use a retained canonical
response, or replace the compact lookup with this one-read path.

## Errors and request accounting

The live reader returns `READ`, `TOOL_ERROR`, `NATIVE_ERROR`, or
`INVALID_RESPONSE`. On a failed read, `pr` stays null; failure does not become
"closed", "not mergeable", or "not found". `error.message` explains the local
classification. The original provider envelope remains in `response` when a
response was returned; thrown tool errors retain their message instead.

`calls: 1` counts the attempted native request, not a successful read. The
started/finished timestamps and elapsed milliseconds cover that invocation.
There is no timeout/retry wrapper or hidden continuation. Honor actual provider
cooldowns before a later deliberate request; this helper does not change quotas
or select another account or endpoint after rejection.

Invalid local inputs throw before a native call. Canonical payloads with
malformed typed fields or a different repository/PR identity return
`INVALID_RESPONSE` from the live reader; the original response remains
available for reconciliation. The standalone projector throws for malformed
payloads. It accepts absent nullable fields and makes their absence explicit.

## Actual use, October 4, 2026

The new module ran in the cloud VM with Node on the retained original PR
#31205 REST response. It exited zero and preserved the real open/unmerged state,
head `8c3da6665b7c218d174621dd40feff39c84d5139`, `mergeable: null`, and
`mergeable_state: "unknown"`. This projection made zero provider calls.

The live reader then ran with the actual connected native binding. Its single
GET returned `READ` in 441 ms and preserved the subsequently closed/merged
state, merge SHA `9027182da611ed83daf56eaef9988b3d145dd599`, merge time
`2026-10-04T11:48:30Z`, and the still-null mergeability field. The source's
earlier compact-then-REST lookup used two PR calls; this path obtains the
canonical fields in one. The source-module load is separate.

Those are individual observed calls and request counts, not a general latency
benchmark. No test suite, generated fixture, induced error, background task,
or repeated publication-validator run was used. The missing-field and error
branches are implemented as described but were not forced during this use.

Provider contract: [GitHub REST — get a pull request](https://docs.github.com/en/rest/pulls/pulls#get-a-pull-request).
Related helpers: [issue/PR search](CONNECTED_GITHUB_ISSUE_SEARCH.md),
[changed-file comparison](CONNECTED_GITHUB_COMPARE.md), and
[publication](CONNECTED_GITHUB_PUBLISH.md).
