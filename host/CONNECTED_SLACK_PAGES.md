# Collect native Slack pages with explicit continuation

`host/connected_slack_pages.cjs` collects a bounded sequence of native connected Slack reads. It returns the original response envelopes, per-call request/cursor metadata and a compact summary. It reads channels, threads or public-and-private search results. It does not interpret claims or change provider state.

Use the existing `host/swarm_claim_scan.py` for message identity, declared/rendered reply-count checks and advisory claim interpretation. Existing mirror clients retain their separate roles.

## Load and use

The module exports `collectSlackPages(tools, request, options?)`. In a Node environment, load it with `require('./host/connected_slack_pages.cjs')` and supply the native tools object. In a code-mode runtime with connected tools:

```js
const source = await tools.mcp__codex_apps__github_fetch_file({
  repository_full_name: "woahwhattheheck/commons",
  path: "host/connected_slack_pages.cjs",
  ref: "main"
});
if (source.isError || source.structuredContent?.encoding !== "utf-8") {
  throw new Error("Readable native source is required");
}
const box = {exports: {}};
new Function("module", "exports", source.structuredContent.content)(box, box.exports);

const result = await box.exports.collectSlackPages(tools, {
  operation: "read_channel",
  args: {channel_id: "C0BRGMDQB6G", limit: 20},
  max_pages: 4,
  timeout_ms: 30000
}, {
  onResponse: async event => store("commons-page-" + event.page.call, event)
});
store("commons-read", result);
text(result.summary);
```

The example channel is this workspace's Commons channel. Use the actual observed ID for another channel or DM. Choose distinct storage keys for separate collections; local call numbers start at one for every invocation. Store the full result and print its summary, rather than sending entire message histories into a context window.

| `operation` | Native reader | Required native input |
| --- | --- | --- |
| `read_channel` | `slack_slack_read_channel` | `channel_id`; a supported user ID can select DM history. |
| `read_thread` | `slack_slack_read_thread` | `channel_id` and the exact decimal-string `message_ts` of the parent. |
| `search` | `slack_slack_search_public_and_private` | Native `query`, or the reader's structured keywords/filters input. |

Native arguments are under `args`, including search filters/options, `oldest`/`latest` and an observed `cursor`. Only arguments in the exposed native schemas are accepted. Semantic input validation remains with the selected reader. Search does not silently restrict itself to public or joined channels; use its native `channel_types`/`only_my_channels` fields when that is the intended scope.

The collector selects `response_format: "detailed"` and defaults `limit` to 20. Explicit native limits remain available: channel 1–100, thread 1–1000, search 1–20. A detailed response can still be shortened by the provider. Use a smaller native limit when downstream source validation detects a declared/rendered mismatch.

## Retain and resume

`responses` contains every original native response returned during the invocation, including error envelopes. A call that throws before returning has no response entry. `pages[].response_index` connects each call record to its envelope; `null` means none returned.

`pages` retains the actual requested arguments, the provider's pagination text, the next opaque cursor and any native/parser/callback diagnostic. The optional awaited `onResponse({page, response})` receives JSON copies after the original envelope is retained. Mutating a callback copy does not alter the returned source. A failed callback stops further reads; the returned result still contains the response.

On a budget stop, retain the result before passing `result.next_request` into the next invocation. The request keeps the same operation, filters, detailed format and limit, with the first unread cursor. The next invocation has a fresh caller budget. Preserve earlier results as part of that continued read.

For explicit thread windows, keep the same observed parent and `oldest`/`latest` across continuations. Channel reads do not expand thread replies. Search results do not read every surrounding thread or linked file.

## Interpret the stop reason

| `summary.stop_reason` | Meaning |
| --- | --- |
| `PROVIDER_END` | An exact recognized provider ending was observed for this cursor chain and request scope. `next_request` is null. |
| `PAGE_BUDGET` | The caller's native-call budget was consumed; use the retained continuation. |
| `TIME_BUDGET` | The cooperative elapsed-time budget ended before starting another call. |
| `NATIVE_ERROR` / `NATIVE_EXCEPTION` | The selected tool returned an error or threw; the failed request is retained for inspection and an explicit later retry. |
| `UNREADABLE_RESPONSE` / `UNKNOWN_PAGINATION` | The native payload or pagination format cannot be followed safely. Preserve the source and inspect it; no continuation is invented. |
| `CURSOR_REPEAT` | The provider returned a cursor already requested in this invocation. The loop stops without another request. |
| `CALLBACK_ERROR` | The response callback failed. Retain the returned response and its diagnostic before deciding whether to continue. |

The default budgets are four native calls and 30,000 ms. Both accept positive safe integers. Time is checked between calls; it does not cancel an in-flight tool call or callback. There are no retries, sleeps or background loops.

`successful_pages` counts decoded native pages without a tool error; it does not establish complete message rendering. `provider_end_observed` reports the native pagination signal only. `coverage` always reads `native_pagination_only`, and `snapshot` is always false. Edits, deletions, live ordering changes, omitted threads, channel membership and query filters can affect the observed source. Reaching the end of a bounded query is not a full-workspace coverage claim.

The recognized text endings and cursor form come from actual detailed native responses. An unfamiliar format remains unknown even if it might be an ending. The collector does not inspect message bodies for cursor instructions.

## Consume the original pages

Write `JSON.stringify(result.responses)` to a private local JSON file. Then use the existing scanner, for example:

```sh
python3 -B host/swarm_claim_scan.py retained-thread-pages.json \
  --channel-id OBSERVED_CHANNEL_ID \
  --workspace-url https://WORKSPACE.slack.com
```

For a thread whose rendered envelope omits its channel, supply the actual channel ID. Do not mix thread exports requiring different fallback IDs in one scanner command. Its existing validation still applies; a provider-error envelope is not a successful source page.

Responses, queries, cursors and diagnostics may contain private information. Keep them in the caller's authorized private source storage. This module performs no disk writes, exports, publication, credential handling, ownership decisions or telemetry activation. Do not commit private Slack source to a public repository.

## Native use in this change

Actual connected reads continued an existing merge-queue cursor for two six-message pages, stopping at the page budget with the next cursor retained. A bounded current coordination thread returned its parent and two replies and reported its end. An exact operation search returned its native ending. The first four native calls completed across those three invocations, with every response equal to its retained callback copy. The existing scanner consumed those original envelopes successfully: 16 supplied/distinct/interpreted message identities across four pages, two declared operations, known pagination on every page and explicit incomplete history.

After retaining cursor tokens directly from the original pagination string and recognizing nested native-error envelopes, the final source continued the next unread six-message queue page through the returned request. It again stopped at the caller's page budget with an opaque continuation. Five native reads were used in this change; earlier observations were not rerun. These observations establish the exercised native paths and continuation behavior, not full channel or workspace coverage.
