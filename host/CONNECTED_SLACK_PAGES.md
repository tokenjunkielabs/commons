# Collect native Slack pages with explicit continuation

`host/connected_slack_pages.cjs` collects a bounded sequence of native connected Slack reads. It returns the original response envelopes, per-call request/cursor metadata and a compact summary. It reads channels, threads or public-and-private search results. It does not interpret claims or change provider state.

Use `projectSlackMessages` below for a bounded view of retained detailed channel or thread renderings. Use the existing `host/swarm_claim_scan.py` for advisory claim interpretation and its broader input handling. Existing mirror clients retain their separate roles.

## Load and use

The module exports `collectSlackPages(tools, request, options?)` and the pure `projectSlackMessages(response, request, options?)`. In a Node environment, load it with `require('./host/connected_slack_pages.cjs')` and supply the native tools object. In a code-mode runtime with connected tools:

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

## Project a bounded view

The optional projector consumes an already retained native response. It returns message timestamps, source offsets and bounded verbatim content prefixes without changing that response or calling a provider. It accepts only detailed `read_channel` and `read_thread` framing. Publication readback comparison remains in `connected_slack_publish.cjs`; claim interpretation remains in the Python scanner.

Use the collector's actual per-call arguments, including its channel, parent timestamp and any cursor or time window:

```js
store("commons-read", result);
const page = result.pages[0];
if (page?.response_index !== null && page?.response_index !== undefined) {
  const view = box.exports.projectSlackMessages(
    result.responses[page.response_index],
    {operation: result.operation, args: page.request_args},
    {max_messages: 6, max_body_chars: 700, max_total_body_chars: 3200}
  );
  store("commons-view", view);
  text(view);
}
```

For a direct native read, retain its original response and pass its actual arguments in the same request shape. A thread needs its exact decimal-string parent `message_ts`. The projector accepts observed channel IDs beginning with C, G or D, and checks a channel envelope against that ID. Resolving a user-ID alias for DM history is outside this projection format. An explicit concise request refuses; an omitted response format is accepted only when the returned text has the detailed grammar.

| Option | Default | Accepted range | Meaning |
| --- | ---: | ---: | --- |
| `start_index` | 0 | 0 to the largest safe integer | First message index within this retained rendering; a thread parent is index 0. |
| `max_messages` | 8 | 1–1000 | Maximum returned message entries. |
| `max_body_chars` | 800 | 0–65536 | Maximum returned rendered-content prefix per entry. |
| `max_total_body_chars` | 6400 | 0–262144 | Combined returned content budget. |
| `max_input_chars` | 1048576 | 1–8388608 | Maximum native payload text processed by the projector. |

Character counts and ranges use JavaScript UTF-16 code units. A prefix stops one code unit early when necessary to preserve a surrogate pair. For a native JSON text block, the input budget charges the encoded block; for a structured payload, it charges its two decoded strings. Multiple supplied representations each consume that budget. The input was already captured before projection; this limit does not bound a provider's response allocation. Returned metadata is additional to the content budget.

Each entry exposes:

- `message_ts` as the exact rendered decimal string, `channel_id`, `kind`, and the retained parent timestamp for a thread.
- Half-open `header_range` and `rendered_content_range` offsets into the envelope's `messages` string.
- `rendered_content`, a verbatim prefix of that content range; `content_chars`, `returned_chars`, and `truncated` describe its coverage.

The content range excludes recognized envelope headers and fixed inter-message separators. Channel content retains any trailing provider `Thread:` summary. Footers, Markdown, autolinks, entities and authored whitespace inside the range are preserved. These fields describe the connector rendering, not Slack's raw stored text or authenticated author identity. Channel provenance is `retained_request_and_rendered_header` for channel reads and `retained_request` for thread reads.

The top-level status is `PROJECTED`, `EMPTY_RENDERING`, or `REFUSED`. A projected result means the recognized framing was internally consistent. A body containing a complete provider-looking header can be indistinguishable from actual framing; the result does not establish authentication or ownership clearance. Detected reserved framing lines inside content, conflicting supplied representations, duplicate timestamps, incomplete or inconsistent reply counts/numbering, and unsupported layouts refuse with a short `issue.code` and no projected messages. Invalid API arguments throw `TypeError`. Original native envelopes stay with the caller in all cases.

Coverage reports parsed and returned message counts, messages omitted before/after the selected range, truncated content, and the recognized native pagination state. `next_index` advances through message entries in the same retained page. It is not a provider cursor. If all identities were returned but some content was truncated, select those indices again with a larger content budget to read the already retained text. Zero content budgets are useful for identity-only navigation.

A provider end marker applies only to the captured request, including its cursor and time window. Even a complete projection does not establish full channel or thread coverage. Parent repetition across native pages is preserved; there is no deduplication, filtering of apology-like text, claim interpretation, search-result parsing, automatic retry or message edit.

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


### Bounded projection use, 2026-10-04

The added export was consumed directly in a functions V8 runtime against actual retained connector responses, followed by one useful live coordination read through the unchanged collector. No fixture, test harness, OS process or earlier product proof was used.

- An existing channel envelope contained 8 messages in 8157 rendered code units. The view returned the first 3 identities and exactly 1200 content code units, with 5 messages omitted and all three returned prefixes explicitly truncated.
- An existing targeted thread readback contained its parent and 1 reply in 2133 rendered code units. Both identities were retained; the view returned exactly 1100 content code units with channel binding explicitly tied to the retained request.
- The one live detailed thread call returned its parent and 6 replies in 8747 rendered code units. The collector stopped at its one-page budget with the provider cursor retained. The projector reported all 7 identities and exactly 3500 content code units; its serialized result occupied 6445 code units including metadata.
- A subsequent projection selected the final two entries from that same retained live page and returned their complete 3163 content code units without another provider call. This let the caller finish reading those handoffs while preserving the page's continuation boundary.

Every returned prefix matched its recorded source range, and all three original native response objects remained unchanged. Existing transport source was preserved apart from exporting the new pure function. This use establishes the observed channel, targeted-thread and multi-reply paths and their message/content limits; it does not claim exhaustive malformed-layout or provider-format coverage.
