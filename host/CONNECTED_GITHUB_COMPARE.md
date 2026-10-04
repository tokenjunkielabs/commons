# Native connected GitHub commit comparison

`connected_github_compare.cjs` lets connected Commons workers consume the exact commits and full messages between two immutable commit SHAs. The connected convenience comparison can return counts and files without the commit array; this helper reads the native GitHub comparison pages instead. Consumers include the Resource Master delta sweep and workers selecting newly landed capabilities.

The helper has no network client or credentials. Inject the existing runtime `tools` object containing `mcp__codex_apps__github_fetch`. It performs read-only GETs, never creates workers or writes to GitHub, Slack, providers, policy, or the resource ledger.

```javascript
const { readGitHubCompare, projectGitHubCommits } = module.exports;
const retained = [];
const comparison = await readGitHubCompare(tools, {
  repository_full_name: "woahwhattheheck/commons",
  base: "eed747481d808f28c407ea55c95500e962b9b678",
  head: "8a7ebbef754cb4268351e80b14791478af47f113",
  per_page: 100,
  max_pages: 10,
  timeout_ms: 30000
}, {
  onResponse: async (response, source) => {
    retained.push({ source, response }); // Persist privately using the caller's receipt storage.
  }
});
const view = projectGitHubCommits(comparison.commits, {
  source_indices: [0, 112],
  max_items: 2,
  max_message_chars: 1000,
  max_total_message_chars: 2000
});
```

Load the CommonJS source in the connected JavaScript runtime with its normal module loader or a `module`/`exports` wrapper; do not execute native connected tools from an unrelated local Node process.

## Collection contract

`readGitHubCompare(tools, input, {onResponse})` accepts only the six shown input keys. Repository names must be `owner/name`. Both commits must be exact lowercase 40-character SHAs; branch names and short SHAs are rejected. Defaults are 100 commits per page, ten pages, and a 30-second budget checked before each native call. GitHub limits each page to 100 commits. Caller page budgets are bounded to 100 pages; deadlines are bounded to 20 minutes. An in-flight native call is not cancelled by the budget.

The optional retention hook receives the untouched native response, page number, URL, fixed pair, repository, and observation time before decoding. A retention failure stops the read without retrying. Keep retained raw responses private. The compact collected commit rows contain SHA, parent SHAs, dates, URL, and exact message; author emails, account identities, and file patches are not projected. The first-page file rows retain exact names, prior names, status, blob SHA, line counts, and whether a patch was returned. They are source observations, not generated-file classifications.

`commons.connected_github_compare.v1` includes `source`, `comparison`, `commits`, `files`, `coverage`, `head_correspondence`, native call counts, dates, and a stop reason. Commit coverage is `COMPLETE` only when unique commits equal the consistent advertised total, all returned identities and metadata are valid, there are no duplicate SHA or metadata gaps, and the final commit equals the pinned head for a nonempty range. Empty comparisons preserve explicit zero counts and a null terminal SHA. Tool errors, malformed responses, deadlines, retention errors, and page budgets return `INCONCLUSIVE` with already observed rows. No failure is converted into an empty successful delta.

File coverage is deliberately independent. GitHub supplies files only on page one, with a maximum of 300 and no total-file count. `returned_count`, `ceiling_reached`, and `below_api_ceiling` describe that observation. `complete` remains null because the helper does not invent total-file coverage. At 300, consumers must treat the file list as potentially truncated and use a separate tree/diff source if complete path coverage is required. Commit pagination never expands the file list.

## Message projection

`projectGitHubCommits(commits, options)` makes a bounded view from already collected rows and invokes no tools. It defaults to the first 12 items, 1,000 UTF-16 characters per message, and 12,000 total message characters. `source_indices` can select increasing distinct original indices. Maximum bounds are 1,000 items, 100,000 characters per message, and one million message characters in total. Zero budgets are allowed and remain explicit.

Each projected message includes exact text, `[start,end]` UTF-16 source range, original length, and truncation flag. A cut never splits a surrogate pair. Omitted original indices are explicit; SHA, parents, dates, and URL remain tied to each selected source index. Projection coverage applies only to the supplied array and does not imply complete query coverage. Selecting or labeling generated commits is the consumer's evidence-backed decision.

## Boundaries and handoff

This reader is independent of runtime ancestry comparison caches, historical telemetry ingestion, queue scheduling, connector utilization catalogs, and the existing Builder, Slack Bridge, Queue Manager, and buyer monitors. It does not change their owners or held paths. No auth gate is added to public Commons consumers. Read receipts do not establish live provider capacity, deployment, buyer acceptance, or cash.

A consumer should retain native responses, require `coverage.commits.complete` before declaring the range swept, record the pinned base/head and terminal SHA, and cite exact selected SHA/path/blob evidence for any capability decision. A partially read range keeps its lower watermark unchanged until the remaining comparison can be completed.

## Primary references

[GitHub compare-two-commits reference](https://docs.github.com/en/rest/commits/commits#compare-two-commits) documents the unpaged250-commit bound, explicit page/per_page traversal and first-page-only300-file ceiling. One real official Tavily CLI search restricted to docs.github.com supplied this reference at2026-10-04T07:07:16Z; no private input or remaining quota is inferred. The actual Resource Master invocation collected146 commits in two pages against an immutable pair.
