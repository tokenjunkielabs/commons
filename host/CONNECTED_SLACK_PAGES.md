# Collect native Slack pages with explicit continuation

`host/connected_slack_pages.cjs` collects a bounded sequence of native connected Slack reads. It returns the original response envelopes, per-call request/cursor metadata and a compact summary. It reads channels, threads or public-and-private search results. It does not interpret claims or change provider state.

Use `projectSlackMessages` below for a bounded view of retained detailed channel or thread renderings. Use the existing `host/swarm_claim_scan.py` for advisory claim interpretation and its broader input handling. Existing mirror clients retain their separate roles.

## Load and use

The module exports `collectSlackPages(tools, request, options?)`, `projectSlackMessages(response, request, options?)`, and `projectSlackSearchResults(response, request, options?)`. Both projectors are pure. In a Node environment, load it with `require('./host/connected_slack_pages.cjs')` and supply the native tools object. In a code-mode runtime with connected tools:

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

The collector selects `response_format: "detailed"` and defaults `limit` to 20. Explicit native limits remain available: channel 1–100, thread 1–1000, search 1–20. A detailed response can still be shortened by the provider. Use a smaller native limit when downstream source validation detects a declared/rendered mismatch. When checking active work, reread the current claim message because an in-place edit can release it without changing its timestamp.

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

The top-level status is `PROJECTED`, `EMPTY_RENDERING`, or `REFUSED`. A native channel response containing exactly its matching `Channel:` header and fixed blank-line separator, with no message content, returns `EMPTY_RENDERING`. Any unframed content after that header still refuses. Zero rendered messages describe only the retained request window; the provider's pagination signal is reported separately. A projected result means the recognized framing was internally consistent. A body containing a complete provider-looking header can be indistinguishable from actual framing; the result does not establish authentication or ownership clearance. Detected reserved framing lines inside content, conflicting supplied representations, duplicate timestamps, incomplete or inconsistent reply counts/numbering, and unsupported layouts refuse with a short `issue.code` and no projected messages. Invalid API arguments throw `TypeError`. Original native envelopes stay with the caller in all cases.

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


### Empty channel use, 2026-10-04

An actual retained channel response containing only its matching header now returns `EMPTY_RENDERING` with zero parsed messages. A nonempty channel page and a four-message thread remain JSON-identical to the preceding projector result. Three separately controlled variations—unframed trailing content, a mismatched requested channel, and a truncated message header—retain their original refusal results.

One fresh channel read through the unchanged collector returned the same empty form and projected successfully. Its provider ending applies only to the captured time window. The original native responses and the collector source remain unchanged; no OS process, suite or fixture was used.


## Project a retained search result page

The separate pure export `projectSlackSearchResults(response, request, options?)`
projects the detailed message-only search format. It consumes an already retained
response and the exact arguments of the call that produced it. It does not make
a search, follow a link, parse claims, filter source records or modify either input.

Pass `{operation: 'search', args: actualNativeArguments}`. With the collector,
use `pages[].request_args` and its corresponding `responses[response_index]`,
as with the message projector. With a direct native search, retain its actual
argument object beside the original response. Do not reconstruct arguments from
the query heading or substitute a narrower query after capture.

The request must explicitly contain `include_context: false`. Its format may be
`detailed` or omitted when the returned grammar is detailed. If `content_types`
was supplied, this projector supports only `messages`. Context-enabled, concise
and file-inclusive requests return `REFUSED / UNSUPPORTED_REQUEST`; the original
native response remains available for other consumers. An omitted content-types
option is accepted only when the actual response has the supported messages
format. Unknown argument fields, invalid argument types and invalid options
throw `TypeError`.

### Inspect full source blocks before selecting text

Use the complete result block, including its rendered channel header, when the
caller needs to exclude source records before printing or deeper intake. A short
content prefix is insufficient for that decision. This example uses a caller-owned
exclusion function and reuses one retained response throughout:

```js
const request = {operation: 'search', args: page.request_args};
const response = collection.responses[page.response_index];
const index = box.exports.projectSlackSearchResults(response, request, {
  max_results: 20,
  max_body_chars: 0,
  max_total_body_chars: 0
});
store('retained-search-index', index);

if (index.status === 'REFUSED') {
  text(index.issue);
} else {
  // The successful projection checked that supplied representations agree.
  const native = response.structuredContent ??
    (typeof response.results === 'string' ? response :
      JSON.parse(response.content[0].text));
  for (const row of index.results) {
    const wholeSource = native.results.slice(...row.rendered_result_range);
    if (callerExcludes(wholeSource)) continue;
    const selected = box.exports.projectSlackSearchResults(response, request, {
      start_index: row.source_index,
      max_results: 1,
      max_body_chars: 700,
      max_total_body_chars: 700
    });
    text(selected.results[0]);
  }
}
```

`callerExcludes` belongs to the calling application; this helper supplies no
policy expression or ownership decision. Keep the native response and query
private. The returned `source.request_args` is an exact JSON copy of the supplied
native arguments and may itself contain private search terms.

| Option | Default | Accepted range | Meaning |
| --- | ---: | ---: | --- |
| `start_index` | 0 | 0 to the largest safe integer | First result within this retained page. |
| `max_results` | 8 | 1–20 | Maximum result entries returned. |
| `max_body_chars` | 800 | 0–65536 | Maximum verbatim content prefix per result. |
| `max_total_body_chars` | 6400 | 0–262144 | Combined returned content budget. |
| `max_input_chars` | 1048576 | 1–8388608 | Combined processed request and native payload text budget. |

All counts and ranges use UTF-16 code units. Prefix clipping preserves a complete
surrogate pair. The input budget charges serialized native arguments and then
each supplied representation: encoded text for native JSON blocks, or both
decoded payload strings for structured/direct payloads. Multiple representations
each consume the budget and must agree exactly. The response already exists
before projection; this option does not bound provider allocation. Metadata is
additional to the returned content budget.

### Exact ranges and limited identity meaning

Each `results[]` entry supplies:

- `source_index`, the exact rendered `channel_id` and decimal-string
  `message_ts`, and its verbatim `permalink`.
- `rendered_result_range`, a half-open range into the decoded native `results`
  string. It begins at `### Result` and includes the Channel line, remaining
  header fields and complete result content. It excludes only the recognized
  fixed trailing result separator.
- `header_range`, from that same start through the native `Text:` header line,
  and `rendered_content_range`, from the following content character through
  the end of the result block.
- `rendered_content`, the bounded verbatim prefix; `content_chars`,
  `returned_chars` and `truncated` describe what was returned.

The parser recognizes one detailed `## Messages (N results)` section with
1–20 numbered result headers and the observed final separator. It checks the
declared count, numbering and distinct channel/message pairs. Permalink channel
and timestamp digits must agree with the rendered header. A single optional
`Participants:` header line is retained as opaque header text, including the
observed DM form. An optional `Reply count:` line and the exact two-space
`[BOT]` author suffix also remain opaque header metadata; neither grants authority.
Author names, participant names, time labels and IDs are never
used to authenticate a person or infer channel membership, ownership or thread
custody. No parent timestamp is inferred from a search permalink.

Channel binding is `rendered_result_header`. Request binding is
`caller_retained_request`: the function records the supplied request-response
pair but does not independently prove which call returned the response.
It does not infer a channel restriction from query text. Header and permalink
agreement describe the captured rendering, not Slack's raw stored text.
A fully provider-looking record authored inside content can be indistinguishable
from framing; successful parsing is not an authenticity assertion.

Detected incomplete framing, count or numbering mismatch, repeated identities,
inconsistent permalinks, conflicting representations, file sections and reserved
search/context framing lines refuse with an issue code and no result entries.
The original response is unchanged. A structurally complete rendering does not
prove that the provider returned the complete authored message body.

### Page coverage and navigation

The statuses are `PROJECTED`, `EMPTY_RENDERING` and `REFUSED`. Only the exact
observed `No results found.` rendering after the search preamble is accepted
as an empty page. It describes that retained query and cursor, not a global
empty work queue or full workspace search.

Coverage reports declared, parsed and returned result counts; omitted results;
content truncation; and the existing recognized native pagination state.
`next_index` advances through this retained page only. Provider cursor handling
remains with the unchanged collector. A native ending covers only its original
query, filters and cursor chain, and is never inferred from an empty rendering.
Unknown pagination can accompany a structurally projected page.

A complete content budget with every rendered result included still says nothing
about omitted messages, unread threads, files, other queries or source changes.
The existing collector and channel/thread projector keep their previous APIs
and outputs. Neither acquires automatic search projection or filtering.

### Native search use, 2026-10-04

The new function was loaded directly in V8 and consumed an actual retained
three-result native search containing 3815 rendered code units. A bounded view
returned its first result with exactly 80 content code units and two results
omitted. Its whole-result range included the Channel header, and its prefix
matched the recorded source offset exactly. Selecting `next_index: 1` returned
the remaining two complete content ranges without another native call.

An actual exact-name search with the native zero-result rendering returned
`EMPTY_RENDERING`. A separately retained context-enabled search returned
`REFUSED / UNSUPPORTED_REQUEST` using its actual request. The DM Participants
form was observed in a header excerpt supplied by the immediate consumer;
that excerpt alone is not a complete positive-response observation.

Three separately controlled changes to the retained three-result source were
also observed: cutting the final separator refused as `UNSUPPORTED_LAYOUT`,
repeating a result number refused as `RESULT_SEQUENCE_MISMATCH`, and conflicting
supplied payload mirrors refused as `CONFLICTING_REPRESENTATIONS`. These were
scratch ambiguity observations, not native responses or a repository suite.

Both existing function bodies remain byte-identical. Actual retained parent-only
and parent-plus-one-reply responses produced JSON-identical message projections
before and after the addition. The search response and request remained unchanged.
No OS process, fixture, test file, dependency or workflow was added.


### Optional native search headers, 2026-10-04

An actual retained six-result work search included one `Reply count:` header and
one bot-marked author header. The earlier grammar recognized only four results
and refused the page. The optional metadata forms now admit all six complete
result ranges. A separate retained eight-result search, including a DM Participants
line and a reply-count header, also projects completely. The preceding ordinary
six-result work search remains JSON-identical.

Two separately controlled malformed headers—a nonnumeric reply count and an
unknown author marker—still refuse without results. Complete selected content
matches its recorded ranges and the original native responses remain unchanged.
Only the search-header grammar changes; the collector and channel/thread projector
remain byte-identical. No provider call, OS process or repository test was used
for these retained-source observations.
