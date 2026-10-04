# Search issues and pull requests through native GitHub REST

[connected_github_issue_search.cjs](connected_github_issue_search.cjs) provides bounded issue and pull-request search through the existing native GitHub fetch action. It forwards the caller's exact GitHub query to `/search/issues` and retains the returned item fields. Its pure `projectGitHubIssueItems` companion provides bounded views of those retained bodies without another provider call.

This packages the existing route workaround for queue intake. During the October 3 Broker work, `github_search_issues` returned ordinary issue #1406 for a query containing `is:pr`. Direct metadata confirmed that item was an open issue. The identical query through the approved native REST route returned zero open Broker PRs. The route had already been shared in fleet coordination; this module supplies reusable pagination and coverage reporting.

The module uses the caller's connected tool object. It owns no credentials, network client, filesystem, or mutation action.

## Use from code mode

~~~javascript
const fetched = await tools.mcp__codex_apps__github_fetch_file({
  repository_full_name: "woahwhattheheck/commons",
  path: "host/connected_github_issue_search.cjs",
  ref: "main"
});
if (fetched.isError) throw new Error("Issue reader source was not retrieved");

const box = { exports: {} };
new Function("module", "exports", fetched.structuredContent.content)(
  box, box.exports
);
const result = await box.exports.searchGitHubIssues(tools, {
  query: "repo:woahwhattheheck/smb-showcase-inventory is:pr is:open broker",
  sort: "updated",
  order: "desc",
  per_page: 50,
  max_pages: 2,
  timeout_ms: 30000
});
store("broker-pr-query", result);
text({
  status: result.status,
  stats: result.stats,
  coverage: result.coverage,
  items: result.items.map(item => ({
    number: item.number,
    title: item.title,
    state: item.state,
    kind: item.pull_request ? "pull_request" : "issue",
    url: item.html_url
  }))
});
~~~

Pin the helper source ref when an operation needs a retained version. Supply repository, author, kind, state, date and other selectors in `query` as needed. The helper neither adds repository qualifiers nor rewrites the query. The current connector's approved resource access still applies.

Keep an explicit `is:issue` or `is:pr` selector for single-kind queues. GitHub documents that some GitHub App user-token searches require a kind qualifier. Use separate queries when both kinds are needed under those connections.

### Choose whether imported board records belong in the query

A technical keyword can also match issue-body transport metadata. In the Commons
intake, imported board records included carrier text such as `discord-connector`
and appeared in a search for `connector`. A keyword match alone therefore does
not identify a new tooling request.

When the caller intentionally wants open issues other than those labeled `board`,
put that choice in the native query:

~~~javascript
const result = await box.exports.searchGitHubIssues(tools, {
  query: "repo:woahwhattheheck/commons is:issue is:open connector -label:board",
  sort: "updated",
  order: "desc",
  per_page: 30,
  max_pages: 1
});
~~~

Keep board records in scope when their imported work is the intended source.
The `board` label is a convention observed in this repository, not a universal
issue kind or an ownership decision. Inspect the selected record and its current
source before deciding what work remains. The adapter forwards either query
exactly; it never adds this exclusion or classifies records on the caller's behalf.

In the actual October 4, 2026 intake, the same open-issue query without the label
exclusion advertised 6,284 matches; the explicitly scoped query returned 12 items.
Those are dated search observations, not a full inventory of work or a statement
that the excluded records lack useful tasks. The original native responses and
query strings were retained; no adapter change or repeat query was needed.

## Inputs and retained responses

| Input | Meaning |
| --- | --- |
| `query` | Required nonempty GitHub search string, forwarded without normalization. |
| `sort` | Optional supported GitHub sort: comments, reactions and its named variants, interactions, created, or updated. Omitted uses provider best-match order. |
| `order` | `asc` or `desc`; default `desc`. GitHub ignores it when sort is omitted. |
| `per_page` | 1–100; default 100. Reduce it when individual issue bodies make native responses too large. |
| `start_page` | Default 1. Starting later remains explicitly partial. |
| `max_pages` | Maximum native request attempts; default 4. |
| `timeout_ms` | Cooperative budget checked before each request; default 30,000 ms. Zero returns before a request. |
| `options.onResponse` | Optional awaited callback receiving `{page, url, response}` for each original native result, including native errors. |

~~~javascript
const result = await box.exports.searchGitHubIssues(tools, {
  query: "repo:woahwhattheheck/commons is:issue is:open tooling",
  sort: "updated",
  per_page: 20,
  max_pages: 2
}, {
  onResponse: async ({ page, url, response }) => {
    store("tooling-query-page-" + page, { url, response });
  }
});
~~~

`items` contains the first observed native item for each unique GitHub item ID. Its fields, including body, state, repository URL, and any `pull_request` object, are retained unchanged. Returned issue metadata is therefore available for the next useful read without another discovery search. The callback can retain the original MCP envelope and duplicate occurrences privately.

The helper counts ordinary issues and PRs from the returned `pull_request` marker. It does not infer mergeability, ownership, approval, current source state, or task completion from a search match. Read a selected record directly when those facts matter.

Unknown helper fields, invalid budgets, unsupported sort/order, invalid callbacks, or a missing native fetch binding throw before a provider call. GitHub receives the search expression itself and reports query validation or access errors.

## Coverage and stop reasons

| Result status | Interpretation |
| --- | --- |
| `FOUND` | At least one actual search item was retained. Remaining coverage may be partial or a later call may have failed. |
| `NOT_FOUND_IN_QUERY` | A complete observed search traversal returned no items. This is a result for this query, not proof of absence from a repository. |
| `INCONCLUSIVE` | No item was retained and the observed traversal is incomplete. |

`coverage.complete` requires traversal from page 1, a page end or advertised total, exactly that many unique IDs, and no provider incompleteness, changing counts, repeated IDs, or search-limit boundary. It describes the observed query response only. `search_index` is always true and `snapshot` is always false: indexed search and live offset pages cannot establish an immutable repository inventory. Equal-size substitutions and indexing lag need not change the advertised count.

GitHub exposes up to 1,000 results per search. The helper reports `SEARCH_RESULT_LIMIT` when the advertised result reaches that boundary and refuses to request an offset at or beyond it. Even an advertised total of exactly 1,000 remains conservatively incomplete. Narrow the query to inspect additional results; a larger local page budget does not remove the provider ceiling.

Each page records its actual URL, total count, `incomplete_results` flag, received count and newly retained count. The result also includes observed totals, repeated item IDs, request counts, issue/PR counts, and the next page. A provider `incomplete_results:true` sets `PROVIDER_INCOMPLETE_RESULTS` even if a short page is returned.

Other stop codes are `PAGE_BUDGET`, `DEADLINE`, `PAGINATION_END`, `ADVERTISED_TOTAL_REACHED`, `TOOL_ERROR`, `NATIVE_ERROR`, and `INVALID_RESPONSE`. Items obtained before an error remain usable. Compact diagnostics are limited to 1,200 characters; the callback retains the complete native response when supplied.

An in-flight provider call or callback can finish after the cooperative deadline. Callback failures are recorded and do not cause a provider replay. The helper has no retry loop, background process, or scheduled continuation.

## Continue a useful partial query

Retain the original query, sort, order and page size, then supply `coverage.next_page` in a later deliberate invocation:

~~~javascript
const nextPage = result.coverage.next_page;
if (nextPage !== null) {
  const continuation = await box.exports.searchGitHubIssues(tools, {
    query: result.query,
    sort: result.sort,
    order: result.order,
    per_page: result.coverage.per_page,
    start_page: nextPage,
    max_pages: 2
  });
  store("tooling-query-continuation", continuation);
}
~~~

A page number is an offset into a live search, not a snapshot cursor. A later invocation reports `STARTED_AFTER_FIRST_PAGE` and cannot certify earlier pages. Preserve prior observations when combining results. On an invalid item or failed request, `next_page` remains the attempted page; a caller may need to reread that page and reconcile repeated IDs.

Coverage is information for intake. It does not create a work reservation or a publication requirement.

## Actual native use, October 3, 2026

The final source ran directly in code mode with the real connected GitHub fetch action. Four useful reader operations made six native requests:

| Operation | Native outcome |
| --- | --- |
| Current open Broker PR query | One page, zero items, `NOT_FOUND_IN_QUERY`, complete observed query. |
| Closed Broker titles, one item per page, two-page budget | Two actual PRs: #2122 and #2119. Six results advertised; `PAGE_BUDGET` and next page 3. |
| Continue the same history from page 3 for two pages | Actual PRs #2115 and #2104. `STARTED_AFTER_FIRST_PAGE`, `PAGE_BUDGET` and next page 5; two advertised items remain unread. |
| Open Goodwood issue query | One ordinary issue, #1406, with its open state and original metadata. Complete observed query. |

Each returned item matched the corresponding original native object exactly; callback errors were empty. The first two bounded history windows intentionally did not exhaust the query. The Broker keyword also matches the customs-broker title, as the explicit query requests.

Observed operation durations were 430 ms, 907 ms, 856 ms, and 503 ms respectively. These are individual native lookup observations, not a general throughput claim. There was no VM process, install, generated input, fixture, provider mutation, or replay of a prior product proof.

This exercise covered real issue/PR distinction, native metadata retention, an empty result, page-budget stopping and continuation. Provider timeout, rate-limit, malformed-response and 1,000-result boundary handling are implemented conservatively; no induced provider failure or synthetic response was used.

Provider contract: [GitHub REST — search issues and pull requests](https://docs.github.com/en/rest/search/search#search-issues-and-pull-requests), read October 3, 2026. The page ceiling, search limit, incompleteness flag and token-specific kind requirement inform this adapter; the connector qualifier mismatch and supported route above are actual session observations.

Related connected capabilities: [path lookup](CONNECTED_GITHUB_PATHS.md), [workflow runs](CONNECTED_GITHUB_WORKFLOW_RUNS.md), [source materialization](CONNECTED_GITHUB_SOURCE.md), and [publication](CONNECTED_GITHUB_PUBLISH.md).


## Read selected bodies without repeating the search

The same module also exports the synchronous function
`projectGitHubIssueItems(items, options)`. Pass the retained native item
array, either `result.items` from `searchGitHubIssues` or
`retainedNativePayload.items` from a captured REST search page. It does not
call a tool, fetch a page, sort or deduplicate items, mutate the input, or claim
that the supplied records came from GitHub. Keep the complete original response
and its request context with the caller.

Use a bounded overview before selecting full bodies:

~~~javascript
const view = box.exports.projectGitHubIssueItems(result.items, {
  max_items: 12,
  max_body_chars: 240,
  max_total_body_chars: 2880
});
text({
  query: result.query,
  search_coverage: result.coverage,
  view
});
~~~

The overview retains item IDs, numbers, issue/PR kind, titles, state, API and
HTML URLs. When supplied, it also retains repository URL, creation/update/close
times and comment count. Other native fields, including author, labels,
assignees, reactions and the full `pull_request` object, remain in the
original items. This is a projection of selected fields, not a complete copy.

Select the next useful records by their original zero-based array indices:

~~~javascript
const selected = box.exports.projectGitHubIssueItems(result.items, {
  source_indices: [1, 4, 16],
  max_items: 3,
  max_body_chars: 10000,
  max_total_body_chars: 20000
});
text(selected);
~~~

These indices are caller choices from the first observed array, not GitHub issue
numbers or a recommendation to inspect those positions in every query. A sparse
selection preserves their increasing original order. To read a contiguous later
window, supply `start_index` instead and use the returned
`selection.next_index`. Neither form requests another provider page.

### Projection inputs and bounds

| Option | Default | Accepted values |
| --- | --- | --- |
| `start_index` | 0 | Safe integer from 0 through the supplied array length; cannot be supplied with `source_indices`. |
| `source_indices` | Omitted | Increasing, distinct, in-range zero-based indices; length cannot exceed `max_items`. |
| `max_items` | 12 | Safe integer from 0 through 100. |
| `max_body_chars` | 500 | Safe integer from 0 through 100,000; applies separately to each selected text body. |
| `max_total_body_chars` | 6,000 | Safe integer from 0 through 1,000,000; consumed in selected-item order. |
| `max_metadata_chars` | 4,096 | Safe integer from 0 through 65,536; applies to the selected metadata fields of every supplied item before projection. |

The input must be an array with at most 1,000 entries. This is a local projection
bound; it neither changes the search reader nor establishes query completeness.
Every input item is checked using the existing native ID/number/URL/PR-marker
contract. Title and state must be strings; optional metadata fields must have
their documented string/null or nonnegative-integer shape. Metadata character
count is the sum of these primitive values' string lengths, with null counting
as zero. It excludes JSON syntax and field names. Metadata is never silently
truncated.

All input rows are checked, including omitted rows. Non-array input, excessive
input length, unknown options, incompatible selectors, malformed records, or
invalid budgets throw `TypeError` or `RangeError` before any
projection is returned. The function has no provider side effects. A zero
metadata budget therefore only accommodates an empty input array. A zero
item budget returns no items; for a nonempty remaining contiguous window its
next index is unchanged, so repeating that same call will not advance.

### Literal bodies and visible omissions

For a text body, `body` is a literal prefix of the supplied string.
There is no Unicode, whitespace, line-ending, Markdown, HTML-entity or link
normalization. Limits and ranges use JavaScript UTF-16 code units, not UTF-8
bytes or rendered characters. A truncation boundary moves back by one code unit
if needed to keep a valid surrogate pair together.

Each selected item includes:

- `source_index`: its original position in the supplied array;
- `body_state`: `text`, `null` or
  `missing`, preserving those different input states;
- `body_chars`: the full supplied text length, or null when no text
  body was supplied;
- `returned_body_chars`: the returned prefix length;
- `body_range`: the half-open prefix interval
  `[0, returned_body_chars]`, or null for a null/missing body;
- `truncated`: whether supplied body text was omitted, or null
  for a null/missing body.

An empty string remains a text body with length zero and range
`[0, 0]`. A null or missing body does not establish that the issue has
no description or work remaining. Exhausting a text budget does not drop a
selected item's metadata; its remaining body is explicitly truncated.

Coverage records supplied, selected and omitted item counts; half-open omitted
index ranges; text/null/missing body counts; full supplied and selected text
lengths; returned text length; and the number of truncated text bodies. The
`all_*` flags concern selection and text strings in this supplied array
only. They do not include unprojected native fields, uncaptured pages or absent
body text.

The projector does not evaluate search coverage. Retain and display the original
query and `result.coverage` separately; a fully projected captured page
may still belong to an incomplete search. Sparse selection has no automatic
next index. For empty input, the selection flags are vacuously true, without
making any provider-level absence claim.

Indices refer to the exact array passed to this call. The search reader already
retains the first observation of each unique item ID; projecting that result
does not restore duplicate occurrences from native pages. Use the original
`onResponse` captures when individual occurrences matter. The projector
itself preserves all supplied entries, including repeated IDs, in their original
positions.

### Actual retained-page use, October 4, 2026

The first real input was a captured REST search page for
`repo:woahwhattheheck/commons is:issue is:open -label:board`, sorted by
oldest update, with 20 items per page. It advertised 80 matches and supplied
20 issue objects with 82,594 UTF-16 body code units. That first page alone did not
exhaust the query. An unbounded body print exceeded the output window.

The new public API then ran directly in connected V8 on that retained array:

| Read | Actual returned body scope |
| --- | --- |
| Contiguous overview | First 12 items, 240 code units each, 2,880 total; all 12 bodies explicitly truncated and original indices 12–19 omitted. |
| Sparse full-body selection | Indices 1, 4 and 16, corresponding to issues #14805, #14864 and #15661; all 13,490 selected body code units returned, 17 other items omitted. |

The complete input array remained unchanged. Both reads made zero provider
calls; there was no second search or old product-proof replay. The observation
covers these actual issue-body selections and their omission accounting.
PR-marker, null/missing body, surrogate-boundary and error handling are
implemented as described, without an induced provider failure, generated
fixture or synthetic check run.
