# Find workflow runs through the native GitHub collection

[connected_github_workflow_runs.cjs](connected_github_workflow_runs.cjs) reads the repository's Actions run collection through the existing native GitHub fetch action and selects a workflow by path or numeric ID, or all workflows at one exact commit. It supplies a compact run/source handoff when the current connector does not expose workflow-specific list routes.

The helper owns no network client, credentials, filesystem or mutation operation. It does not dispatch, retry, cancel, approve or rerun a workflow. It reads the supplied repository with the caller's existing connected tool surface.

## Use from code mode

The source is a standalone CommonJS module. Load it once in the current invocation, then pass the existing tools object:

~~~javascript
const fetched = await tools.mcp__codex_apps__github_fetch_file({
  repository_full_name: "woahwhattheheck/commons",
  path: "host/connected_github_workflow_runs.cjs",
  ref: "main"
});
if (fetched.isError) throw new Error("Workflow reader source was not retrieved");

const module = { exports: {} };
new Function("module", "exports", fetched.structuredContent.content)(
  module, module.exports
);
const result = await module.exports.findGitHubWorkflowRuns(tools, {
  repository_full_name: "woahwhattheheck/commons",
  workflow_path: ".github/workflows/pages-deploy.yml",
  filters: {
    branch: "main",
    event: "schedule",
    created: "2026-10-03T00:00:00Z..2026-10-03T15:40:00Z"
  },
  per_page: 100,
  max_pages: 10,
  timeout_ms: 30000
});
text(result);
~~~

Replace the explicit historical window with the period relevant to the operation. Pin the source ref when a retained operation needs the same helper version. A known workflow ID can replace the path:

~~~javascript
const result = await module.exports.findGitHubWorkflowRuns(tools, {
  repository_full_name: "woahwhattheheck/commons",
  workflow_id: 348059776,
  filters: {
    branch: "main",
    event: "schedule",
    created: "2026-10-03T00:00:00Z..2026-10-03T15:40:00Z"
  },
  stop_after_first: false
}, {
  onResponse: async ({ page, url, response }) => {
    // Retain the actual complete native result in the caller's existing record.
    store("pages-run-list-" + page, { url, response });
  }
});
text(result);
~~~

A path matches the exact returned path or that path followed by GitHub's optional `@ref` suffix. An ID avoids path changes across workflow history. When both selectors are supplied, both must match. Runs remain in provider order; the helper does not sort by update time or promise an immutable latest-run snapshot.

## Inputs

| Input | Meaning |
| --- | --- |
| `repository_full_name` | Required `owner/repository`; each component is URL-encoded. |
| `workflow_path`, `workflow_id` | At least one selector unless `all_workflows: true` is used. IDs accept a positive safe integer or a decimal string. |
| `all_workflows` | Opt-in selection of all workflows at a full pinned `filters.head_sha`; mutually exclusive with path/ID selectors. Default false. |
| `filters` | Optional GitHub filters: `actor`, `branch`, `check_suite_id`, `created`, `event`, `head_sha`, `status`. Unknown fields raise an input error instead of being silently ignored. |
| `per_page` | 1–100; default 100. |
| `start_page` | Default 1. Starting later is explicitly partial coverage. |
| `max_pages` | Maximum native read attempts in this invocation; default 10. Successful pages and calls are counted separately. |
| `timeout_ms` | Cooperative elapsed budget, default 30,000 ms. Zero returns before a read. |
| `stop_after_first` | Default true. False collects all matching runs within the stated budgets. |
| `options.onResponse` | Optional awaited callback receiving page, URL and complete native response, including native error results. Callback errors are retained without replaying a call. |

Text filter syntax is forwarded to GitHub after URL encoding. The helper does not maintain a second status/event vocabulary. It sets `exclude_pull_requests=true` to omit nested PR arrays from the response; **that parameter does not exclude pull-request-triggered runs**. Use the event filter when the operation needs a particular trigger.

The time budget cannot cancel an in-flight native tool call or a caller callback. Both may finish after the budget. There is no background process, sleep, retry loop or scheduled follow-up.

## Observe every workflow at one exact head

Use `all_workflows: true` when the operation needs all workflows associated
with one prepared commit, rather than a known workflow path or ID:

~~~javascript
const result = await module.exports.findGitHubWorkflowRuns(tools, {
  repository_full_name: observedRepository,
  all_workflows: true,
  filters: { head_sha: observedCommitSha },
  stop_after_first: false,
  per_page: 100,
  max_pages: 2,
  timeout_ms: 30000
}, {
  onResponse: ({ page, url, response }) =>
    store("current-head-runs-" + page, { url, response })
});
~~~

This opt-in mode requires `filters.head_sha` to be a complete lowercase
40-character commit SHA. It cannot be combined with `workflow_path` or
`workflow_id`; a non-boolean `all_workflows` value is invalid. These errors
are caught before provider calls. Omission or `false` preserves the existing
path/ID requirement and result shape.

Event selection remains caller-explicit. With the example's filter, the helper
adds no event restriction. Add `event: "pull_request"` only when that is the
intended scope; other supported filters still narrow the query as before.
The connected `fetch_commit_workflow_runs` wrapper advertises a fixed
pull-request-event filter and first-page-only response. This mode uses the
existing repository collection to express the broader query and its bounded
pagination; a previous PR-event-only observation does not establish the result
of this broader lookup.

The result identifies this selection as
`workflow: {path: null, id: null, all: true}`, while `filters.head_sha` records
the exact source. Every selected row must carry that same `head_sha`.
A missing or different returned head stops with `INVALID_RESPONSE` and
incomplete coverage; earlier matching rows remain available under the existing
positive-result rule. The helper does not relabel another run as the requested
source or infer that a workflow ran from its presence in a repository.

`all_workflows` describes the workflow selector, not a completeness guarantee.
The existing `stop_after_first` default is still `true`; pass `false`, as in
the example, to collect every matching run within the stated page/time budgets.
All run identity checks, duplicate/total-change reporting, offset-page limits,
native errors and the filtered 1,000-result ceiling remain unchanged. A pinned
commit does not make the run collection immutable: new runs or changing run
states can still appear for that head. Use `coverage.complete` and the stop
reason, with `snapshot: false`, to describe the actual observed scope.

This operation still only reads. Run status is separate from source
verification, required-job coverage, maintainer approval and acceptance. It
does not rerun a failed job, approve a fork workflow, dispatch work or recover
a disconnected local runtime.

## Read the result

Each match retains the run ID, workflow ID/path, run number and attempt, trigger, status/conclusion, source branch/SHA, timestamps, and run/jobs/logs/artifact URLs. Actor profiles, commit messages and nested repository payloads are omitted from this compact projection. The optional callback can retain the complete native response.

| Status | Interpretation |
| --- | --- |
| `FOUND` | At least one actual matching row was read. Inspect coverage and stop reason for the remaining history. |
| `NOT_FOUND_IN_SCOPE` | No match was observed after a complete, consistent traversal of the specified query from page 1. It says nothing about other periods, branches, triggers or repositories. |
| `INCONCLUSIVE` | No match was read and the query's coverage remains incomplete. |

`FIRST_MATCH` is a successful early stop and deliberately leaves `coverage.complete=false`. The result includes every attempted page URL, observed total counts, rows received/examined, first/last examined IDs, duplicate IDs, and a next page/zero-based row position. Those positions describe the unread region; they are not an opaque resumable snapshot. A new invocation with a later start page cannot certify earlier pages.

`coverage.complete` requires all of the following: start at page 1; reach the advertised total or page end; observe exactly that many unique IDs; observe no total-count changes or repeated IDs; and remain below the filtered-search ceiling. `snapshot` is always false. Offset pagination is live: deletion, equal-size substitutions or changing status filters can change the collection without an observable total-count change. A closed creation-time window reduces movement from new runs but does not make provider history immutable.

The documented GitHub search ceiling is **1,000 results per filtered query**. A filtered traversal reaching that boundary remains incomplete, including when the reported total is exactly 1,000. Narrow the explicit creation window or another relevant filter to inspect additional history. Increasing the page budget cannot remove this provider boundary. An unfiltered query has no search ceiling imposed by this helper, but still has the caller's page/time budgets.

Other stop reasons include `PAGE_BUDGET`, `DEADLINE`, `FILTERED_SEARCH_LIMIT`, `TOOL_ERROR`, `NATIVE_ERROR` and `INVALID_RESPONSE`. Positive matches already obtained survive a later failure. Native diagnostics are truncated to 1,200 characters in the compact result; preserve the callback's full response when needed. Invalid input or a missing native fetch action throws before any tool call.

## Actual native use, October 3, 2026

The motivating delivery was [referral Pages issue #30515](https://github.com/woahwhattheheck/commons/issues/30515). Workflow-specific run-list URLs returned `INVALID_ARGUMENT` in this connector, while the documented repository collection returned actual scheduled runs. The existing local [workflow_surface.py](workflow_surface.py) reads workflow recipes; it does not provide this native run-history capability.

Two real reader operations used the closed interval 00:00:00–15:40:00 UTC, branch main and event schedule:

| Operation | Calls / rows examined | Result |
| --- | --- | --- |
| Path selection, first match, five rows/page | 4 calls / 18 examined of 20 received | Run 250 found on page 4; 60 runs advertised; remaining history explicitly partial. Elapsed 1.919 s. |
| ID selection, full bounded collection, 100 rows/page | 1 call / all 60 rows | Three matching runs; complete observed query, no duplicate IDs or changing total. Elapsed 1.687 s. |

The first operation exercised the unchanged first-match path before the final filtered-ceiling stop-reporting adjustment. The complete-collection operation executed the final source. These are native lookup elapsed times, not workflow execution times or a general performance benchmark.

| Run | ID | Selected source | Created UTC |
| --- | --- | --- | --- |
| 250 | 37121288206 | `34c9e5d6acb8e7e4a2c0423208de8a0aa3bcefcd` | 11:57:13 |
| 249 | 37103378655 | `135b5c625bbb1ed40252d58d53b79f5e6db0c27d` | 06:32:04 |
| 248 | 37084850155 | `12dc86a51c650deb81df6308fbe89137c03806d3` | 01:07:07 |

All three observed records were completed successfully. Their selected source generations differ. A workflow success does not by itself establish current public behavior; issue #30515 separately records the deployed receipt and actual checkpoint/replay outcome.

## Continue with the returned identity

Use the returned exact run ID with the existing native run/jobs/logs readers. Decide any subsequent action from that run's source and state plus the task's current ownership. The helper creates no workflow operation and never substitutes rerunning an older successful generation for publication of newer source.

Related native capabilities: [path lookup](CONNECTED_GITHUB_PATHS.md), [source materialization](CONNECTED_GITHUB_SOURCE.md), and [guarded source publication](CONNECTED_GITHUB_PUBLISH.md).

Provider contract: [GitHub REST — list workflow runs for a repository](https://docs.github.com/en/rest/actions/workflow-runs#list-workflow-runs-for-a-repository), read October 3, 2026. The documented query ceiling, parameters and optional path ref suffix inform this adapter; connector route availability is the actual session observation above.

