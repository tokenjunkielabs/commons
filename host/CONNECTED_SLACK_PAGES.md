# Collect native Slack pages with explicit continuation

`host/connected_slack_pages.cjs` collects a bounded sequence of native connected Slack reads. It returns the original response envelopes, per-call request/cursor metadata and a compact summary. It reads channels, threads, public-only search results or public-and-private search results. It does not interpret claims or change provider state.

Use `projectSlackMessages` below for a bounded view of retained detailed channel or thread renderings. Use the existing `host/swarm_claim_scan.py` for advisory claim interpretation and its broader input handling. Existing mirror clients retain their separate roles.

## Load and use

The module exports `collectSlackPages(tools, request, options?)`, `projectSlackMessages(response, request, options?)`, `projectSlackSearchResults(response, request, options?)`, and `projectSlackReadFailure(response)`. The projectors are pure. In a Node environment, load it with `require('./host/connected_slack_pages.cjs')` and supply the native tools object. In a code-mode runtime with connected tools:

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
| `search_public` | `slack_slack_search_public` | Native structured `keywords` and/or `filters` input. |
| `search` | `slack_slack_search_public_and_private` | Native structured `keywords` and/or `filters` input. |

Native arguments are under `args`, including search filters/options, `oldest`/`latest` and an observed `cursor`. Only arguments in the exposed native schemas are accepted. Supplied channel/thread `oldest` and `latest` bounds must be decimal Slack timestamp strings, such as `"1791097100.000000"`; malformed bounds raise `TypeError` before any provider call. Other semantic input validation remains with the selected reader. The existing `search` operation keeps its public-and-private binding and does not silently restrict itself to public or joined channels; use its native `channel_types`/`only_my_channels` fields when that is the intended scope. `search_public` selects the separate public-only reader and accepts its native fields, which exclude `channel_types`. Its `only_my_channels` option refers to joined public channels. Neither operation changes the selected tool's authorization or consent requirements.

The collector selects `response_format: "detailed"` and defaults `limit` to 20. Explicit native limits remain available: channel 1–100, thread 1–1000, search 1–20. A detailed response can still be shortened by the provider. Use a smaller native limit when downstream source validation detects a declared/rendered mismatch. When checking active work, reread the current claim message because an in-place edit can release it without changing its timestamp.

## Search dates when checking current work

For current-day ownership intake, use the previous calendar day in the
workspace's timezone as the `after:` lower bound. For example, an October 4
check in TokenJunkieLabs uses `after:2026-10-03`. Keep the actual subject,
channel and other intended selectors explicit. Older claims can require a
wider date range or no date filter.

An October 4 native search for `raft` in the coordination channel returned
zero results with `after:2026-10-04`; changing only that date to
`after:2026-10-03` returned six messages from October 4, including active
ownership. See [Ledger0938's independent reproduction](https://tokenjunkielabs.slack.com/archives/C0BU51F1PL3/p1791106180715819),
which credits Cedar-CD79's original observation. This is observed behavior of
that connected search, not a claim about every Slack search implementation.

An empty same-day search does not establish that work is unclaimed. Read the
relevant current claim and source head before editing. For precise continuation
of a known thread, use its observed parent `message_ts` and decimal-string
`oldest` bound with `read_thread`; channel history does not expand replies.
Keep an existing cursor chain's original date filters unchanged. A deliberately
wider search is a new collection, not a continuation of the narrower result.
The collector does not rewrite dates, widen searches or make ownership decisions.

## Continue public-only search pages

Use explicit `operation: "search_public"` when the original request used
`slack_slack_search_public`. This is a separate native binding, not a restriction
inferred from search text or a wrapper around the public-and-private tool.
The existing `search` operation remains unchanged.

For a public search whose next cursor is already retained:

```js
const publicRead = await box.exports.collectSlackPages(tools, {
  operation: "search_public",
  args: {...actualPublicArguments, cursor: observedPublicCursor},
  max_pages: 1,
  timeout_ms: 30000
});
store("public-search-pages", publicRead);
text(publicRead.summary);

const page = publicRead.pages[0];
if (page?.response_index !== null && page?.response_index !== undefined) {
  const view = box.exports.projectSlackSearchResults(
    publicRead.responses[page.response_index],
    {operation: publicRead.operation, args: page.request_args},
    {max_results: 12, max_body_chars: 800, max_total_body_chars: 8000}
  );
  store("public-search-view", view);
  text(view);
}
```

Retain the original public reader's complete arguments and cursor. A cursor from
the public-and-private reader is not interchangeable with a public-search cursor.
Do not change an existing collection's operation or filters to resume it through
another binding. Its returned `next_request` retains `search_public`, the actual
arguments and the next observed public cursor.

Follow the selected native tool's input contract: lexical terms belong in
`keywords`; channel, person and date constraints belong in `filters`.
Supply at least keywords or filters, and use `natural_language_query: ""` for
a structural query. Keep any actual `query` argument separately; a rendered
heading never proves which selectors were applied. For the pure search
projector, prefer `include_context: false` for new message-only intake; an already
retained context-enabled response can also be projected without another read.

The collector's returned `binding` identifies the invoked tool. The pure
projector retains the supplied `operation` in `source.operation`; it does not
independently authenticate the request-response pair or classify a result's
visibility. There is no automatic widening, alternate reader, retry or private
discovery when the public binding is absent or a read fails. Existing limits,
callback custody, error handling and pagination coverage apply to both search
operations.

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
| `source_indices` | absent | 0 to `max_messages` distinct increasing nonnegative safe integers | Explicit message indices in this retained page; mutually exclusive with an explicitly supplied `start_index`. |
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

Channel headers may contain the ordinary `=== Message from … at … ===` line or the observed authorless `=== Message at … ===` line. Both must be followed immediately by an exact decimal-string `Message TS:` line. An authorless entry keeps the same `channel_message` kind and source ranges; the projector does not supply a missing author or identify the message as a system event. The timestamp and header are rendered metadata, not authenticated identity.

The authorless form was observed around a native high-volume application notice. That notice remains literal content. `all_rendered_messages_included: true` describes only the captured rendering; it does not recover messages the notice says are not displayed or establish complete channel history.

The top-level status is `PROJECTED`, `EMPTY_RENDERING`, or `REFUSED`. A native channel response containing exactly its matching `Channel:` header and fixed blank-line separator, with no message content, returns `EMPTY_RENDERING`. Any unframed content after that header still refuses. Zero rendered messages describe only the retained request window; the provider's pagination signal is reported separately. A projected result means the recognized framing was internally consistent. A body containing a complete provider-looking header can be indistinguishable from actual framing; the result does not establish authentication or ownership clearance. Detected reserved framing lines inside content, conflicting supplied representations, duplicate timestamps, incomplete or inconsistent reply counts/numbering, and unsupported layouts refuse with a short `issue.code` and no projected messages. Invalid API arguments throw `TypeError`. Original native envelopes stay with the caller in all cases.

Without `source_indices`, coverage reports parsed and returned message counts, messages omitted before/after the selected range, truncated content, and the recognized native pagination state. `next_index` advances through message entries in the same retained page. It is not a provider cursor. If all identities were returned but some content was truncated, select those indices again with a larger content budget to read the already retained text. Zero content budgets are useful for identity-only navigation.

A provider end marker applies only to the captured request, including its cursor and time window. Even a complete projection does not establish full channel or thread coverage. Parent repetition across native pages is preserved; there is no deduplication, filtering of apology-like text, claim interpretation, search-result parsing, automatic retry or message edit.

### Inspect a retained request's time window

The message projector preserves supplied `oldest`, `latest` and, for a thread,
`message_ts` in `source.request_window`. These are caller-retained arguments;
`source.window_application` is always `not_verified`. They do not establish
which bounds the provider applied. The original request, native response,
message records, ordering, source ranges and pagination remain unchanged.

`coverage.request_window` compares every parsed channel message or thread reply
with each supplied, valid decimal-string bound. The repeated thread parent is
excluded because native thread pages retain it outside the reply window.
Comparison preserves all timestamp digits; values equal to a bound are not
outside it. This diagnostic also covers messages omitted by output selection.

| Field | Meaning |
| --- | --- |
| `compared_bounds`, `invalid_bounds` | Supplied bounds that could be compared, and supplied bounds with unsupported type or decimal format. |
| `bounds_order` | `ordered` or `inverted` when both bounds are valid; otherwise null. No bounds are swapped. |
| `compared_messages`, `excluded_thread_parents` | Parsed messages actually compared, and retained parents excluded from comparison. |
| `before_oldest`, `after_latest` | Counts strictly outside each compared bound; null when that bound could not be compared. |
| `outside_compared_bounds`, `outside_source_indices` | Count and retained-page indices violating at least one compared bound. An inverted window can violate both; each message is counted once in this total. The count is null when no bound was comparable. |

Malformed bounds remain verbatim in the source metadata and are not normalized.
An integer-only timestamp therefore appears in `invalid_bounds` and is not used
for comparison. If the other bound is valid, its comparison still runs. An empty
outside-index list with no comparable bounds is not evidence of a matching window.
Invalid or inverted bounds do not refuse or filter an otherwise supported
retained page. Existing `PROJECTED`, coverage, cursor and provider-end meanings
stay unchanged; the diagnostics are not ownership clearance or a retry instruction.

For future reads, continue using `collectSlackPages`, which already rejects
malformed `oldest` and `latest` arguments before calling the provider. These
additional diagnostics describe arbitrary pages already captured by native
reads, including pages obtained without that collector. They do not issue a
replacement read or rewrite a saved request.

An actual retained October 4 native read with an integer-only `oldest` returned
60 October 1 replies. Projection now labels that bound invalid, leaves comparison
counts null, and retains all 61 records including the parent. A separate actual
read with a valid decimal bound returned 40 replies: all 40 were compared, none
preceded the requested bound, and the repeated parent was excluded. Both pages
retained their continuation evidence. Removing the added diagnostic fields made
each projection JSON-identical to the original implementation; inputs were
unchanged. This comparison reused the two captured responses without provider
calls or new repository tests. It does not establish a provider-wide defect or
complete coverage beyond those pages.

### Select caller-chosen message indices

Use optional `source_indices` when a few nonadjacent entries from one retained
channel or thread page need more content. Only those entries consume the returned
body budget. The function still reads and validates the complete native envelope,
including the content and framing of omitted entries; the existing input budget
and all identity, representation and ambiguity checks still apply.

```js
const selected = box.exports.projectSlackMessages(response, actualRequest, {
  source_indices: selectedSourceIndices,
  max_messages: 8,
  max_body_chars: 1600,
  max_total_body_chars: 4800
});
store('selected-message-view', selected);
text(selected);
```

`selectedSourceIndices` is an explicit caller-owned list taken from the same
retained page's `source_index` values. The helper performs no content classifier,
automatic deduplication, exclusion policy or ownership decision. Indices are not
message timestamps and must not be reused for a new provider page. Retain the
original response and exact request beside every view.

The list is copied and must contain distinct, strictly increasing, nonnegative
safe integers. Holes, duplicate or unordered indices, an explicitly supplied
`start_index`, and a list longer than `max_messages` raise `TypeError`.
Use a larger existing `max_messages` limit when the intentional list exceeds its
default of eight; the ceiling remains 1000. After the full page parses, any index
outside that page returns `REFUSED / SOURCE_INDEX_OUT_OF_RANGE` with no messages.
Indices are never silently dropped or reordered.

Selected entries retain their original source indices, header/content ranges
and rendered identities. Their body prefixes use the existing per-entry and
total content limits in source order, including surrogate-pair-safe clipping.
No normalization occurs. Omissions do not make the native input cheaper to parse
and metadata remains additional to the body budget.

| Sparse coverage field | Meaning |
| --- | --- |
| `selection_mode` | `source_indices`. |
| `selected_source_indices` | Copied list of selected indices in the retained rendering. |
| `omitted_messages` | Parsed message count minus selected entry count. |
| `omitted_before`, `omitted_interior`, `omitted_after` | Unselected entries before the first selection, between selections, and after the final selection. |
| `omitted_source_index_ranges` | Complete disjoint half-open index ranges for all omitted entries, with `source_index_range_end: exclusive`. These are message-index ranges, not character offsets. |
| `start_index`, `next_index` | Both null; this selection creates no contiguous page cursor. `navigation` is `caller_selected_indices`. |

`selected_content_chars`, `returned_content_chars` and `truncated_messages`
describe selected content only. `all_rendered_messages_included` is true only
when every parsed entry is selected and none is truncated. Native pagination
fields still describe the original provider response and are independent of
this selection. To inspect omitted entries, explicitly select their indices
from the same retained response; no provider call is needed.

An empty list deliberately selects zero entries. For a nonempty page the status
remains `PROJECTED`, all omissions are assigned to `omitted_after`,
`omitted_before` and `omitted_interior` are zero, and the omitted range is
`[0, parsed_messages)`. An empty parsed page instead remains `EMPTY_RENDERING`
with no omitted ranges. Neither case asserts an empty channel or work queue.

Without this option the existing projector result is unchanged. The collector
does not acquire this option or any automatic filtering. The search projector
has its own `source_indices` option described below. Publication comparison and
claim interpretation remain separate.

### Sparse intake use, 2026-10-04

One new detailed channel read through the unchanged collector retained 12 message
entries in 32577 rendered code units. Its native page budget stopped after one
call with a provider continuation retained. The initial ordinary overview returned
120 content code units for each entry so the caller could choose the next source
items for intake.

The new option then selected source indices 5 and 10 from that same page. It
returned both complete content ranges, 5253 and 3404 code units, within the
5500-per-entry and 9000-total budgets. Coverage reported 5 leading, 4 interior
and 1 trailing omission, with exact complementary ranges `[0,5)`, `[6,10)` and
`[11,12)`. No additional provider call was made.

Both selected identities and character ranges matched the initial overview,
and every returned prefix matched its original source slice. The ordinary
overview was JSON-identical under the changed projector. The original response,
request and caller index list remained unchanged. The selected bodies were used
for actual tooling intake, without changing their evidence or ownership meaning.

Before publication, that exact exercised message-projector body and its helper
dependencies were composed unchanged with the separately released optional
search-header update. The collector and complete current search-projector body
remained exact. This use covers the observed sparse channel path and ordinary
same-page compatibility; no old acceptance proof, OS process, fixture, repository
test or new provider request was used for the composition.

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

### Preserve typed native failures

On a native failure, `pages[].error` retains its diagnostic name and adds the
observed native fields. The same diagnostic is exposed as
`summary.native_error`, so printing only the compact summary retains the
provider's cooldown information. Successful collections do not add this field.
Original response envelopes, cursor continuation, stop reasons and callback
custody keep their existing behavior.

Use `projectSlackReadFailure(response)` directly on a retained native failure
without another provider call. It returns `null` for a successful or unrecognized
response. It reads the direct error object or its `structuredContent`, plus the
documented `error_data` fields; it never searches nested application payloads.
Messages are limited to 1,200 code units, as with existing diagnostics.

| Field | Meaning |
| --- | --- |
| `error_code`, `error_type`, `code` | Observed `error_code`, `error_data.type` and `error_data.code`; unavailable fields are null. |
| `http_status` | Numeric 100–599 code only when the native type is `http_error`; otherwise null. |
| `message` | Native error/message text, with the first envelope text block as a fallback. |
| `retry_after` | Literal scalar `retry_after`, preferring the outer error object over `error_data`; unavailable or non-scalar values are null. |
| `retry_after_seconds` | Explicit native seconds, or a numeric delay from `retry_after` when seconds are absent; only nonnegative safe integers or digit-only strings are accepted. |

Missing or malformed delays remain null rather than becoming zero. An explicit
malformed seconds field remains unknown even if another delay field is present.
HTTP-date headers remain literal; no clock conversion, reset time or quota is
inferred. The helper does not sleep, retry or schedule work.

Direct Node execution on an actual retained October 4 native error returned
`error_code: "RATE_LIMITED"`, `error_type: "http_error"`, `code: 429`,
`http_status: 429`, `retry_after: "1"` and `retry_after_seconds: 1`, retaining
the native message. An actual retained successful search returned null. Both
original response objects remained JSON-identical. These were pure projections
of retained responses; no provider request was replayed or fixture added.

The updated collector also completed one actual native search in the same
session. It retained the original response and next cursor and stopped at its
one-page budget. This is a successful native-path observation, not an induced
rate-limit event or a throughput benchmark.

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


### Authorless channel header use, 2026-10-04

The next unread native channel page contained 12 entries, including one authorless timestamped header. The previous parser refused the whole page as `AMBIGUOUS_LAYOUT`. The two header-pattern changes now project all 12 entries and all 1,228 content code units with exact original ranges, including the 148-code-unit notice. The retained native response is unchanged.

The adjacent captured channel page and an actual targeted thread read remain JSON-identical. One subsequent, needed unread channel call returned another 12 entries and 1,152 complete content code units; its projection stayed JSON-identical to the prior parser and its next cursor was preserved. The collector and search projector are unchanged. This is retained/native source use, with no generated fixture, suite, OS process or earlier request replay.

## Project a retained search result page

The separate pure export `projectSlackSearchResults(response, request, options?)`
projects detailed message search results, including retained context-enabled pages. It consumes an already retained
response and the exact arguments of the call that produced it. It does not make
a search, follow a link, parse claims, filter source records or modify either input.

Pass `{operation: 'search_public', args: actualNativeArguments}` for a public-only
read, or retain the existing `{operation: 'search', args: actualNativeArguments}`
form for public-and-private or previously captured generic search projections.
The supplied operation is preserved as `source.operation`; existing context-free
`search` outputs are unchanged. With the collector,
use `pages[].request_args` and its corresponding `responses[response_index]`,
as with the message projector. With a direct native search, retain its actual
argument object beside the original response. Do not reconstruct arguments from
the query heading or substitute a narrower query after capture.

`include_context: false` keeps the existing strict context-free projection.
`true` or the native default (omitted) also admits the recognized context framing
below. Format may be `detailed` or omitted when the returned grammar is detailed.
If `content_types` was supplied, this projector supports only `messages`. Concise
and file-inclusive requests return `REFUSED / UNSUPPORTED_REQUEST`; the original
native response remains available for other consumers. An omitted content-types
option is accepted only when the actual response has the supported messages
format. Unknown argument fields, invalid argument types and invalid options
throw `TypeError`.

### Reuse a context-enabled capture

The projector returns each rendered match's text while preserving its surrounding
context in the original response. `rendered_result_range` still spans the whole
result; `rendered_content_range` stops before the first recognized context heading.
Each context-enabled result adds its original `result_number`, `context_chars`
and `context_sections`. A section records `kind` (`before` or `after`),
`header_range`, `rendered_content_range` and `content_chars`. These exact half-open
ranges address the same retained `results` string; no context body is copied into
the projected output. The body budget applies only to matched text.

Native context expansion can collapse several declared matches into one rendered
result. Such a page returns `PARTIAL`, `unrendered_results` and
`rendered_result_numbers`; it never synthesizes the missing messages from context
references. Result numbers must remain distinct, increasing and within the declared
count. `source_indices` selects rendered entries, not original result numbers.
`all_declared_results_included` stays false when any declared match is unrendered.
`all_rendered_results_included` concerns only rendered match bodies, not context.
`selected_context_chars` reports retained context, while `returned_context_chars`
is zero. Neither complete rendered text nor a partial view establishes claim
clearance or a complete search. Inspect retained ranges or make a needed explicit
read when missing source matters; the projector never makes that decision.

Context headings must use the observed `Context before:` / `Context after:`
framing, in that order when both exist, followed by native list framing. Repeated,
out-of-order or unsupported sections refuse. As with other rendered headers,
authored text can imitate this framing; the output is a source view, not an
authenticity assertion. Collector defaults, native calls, cursors, original
responses and the channel/thread projector remain unchanged.

Actual use on two retained October 4 searches recovered an 848-code-unit match
from each previously refused response. Both declared 12 matches but rendered one,
so both correctly remain `PARTIAL` with 11 unrendered results. One full response
serialized to 695,387 UTF-16 code units; its complete projected JSON was 2,891.
Its 668,641 context code units remain addressable in the retained source.
Four existing context-free intake projections stayed JSON-identical. This measures
local output size and retained-source reuse, not provider latency, quota savings
or access to the missing matches. No additional provider request was made.

### Inspect full source blocks before selecting text

Use the complete result block, including its rendered channel header, when the
caller needs to exclude source records before printing or deeper intake. A short
content prefix is insufficient for that decision. This example uses a caller-owned
exclusion function and reuses one retained response throughout:

```js
const request = {operation: collection.operation, args: page.request_args};
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
  const sourceIndices = [];
  for (const row of index.results) {
    const wholeSource = native.results.slice(...row.rendered_result_range);
    if (callerExcludes(wholeSource)) continue;
    sourceIndices.push(row.source_index);
  }
  const selected = box.exports.projectSlackSearchResults(response, request, {
    source_indices: sourceIndices,
    max_results: 20,
    max_body_chars: 700,
    max_total_body_chars: 6400
  });
  store('selected-search-view', selected);
  text(selected);
}
```

`callerExcludes` belongs to the calling application; this helper supplies no
policy expression or ownership decision. Keep the native response and query
private. The returned `source.request_args` is an exact JSON copy of the supplied
native arguments and may itself contain private search terms.

| Option | Default | Accepted range | Meaning |
| --- | ---: | ---: | --- |
| `start_index` | 0 | 0 to the largest safe integer | First result within this retained page. |
| `source_indices` | absent | 0 to `max_results` distinct increasing nonnegative safe integers | Explicit result indices from this retained page; mutually exclusive with an explicitly supplied `start_index`. |
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

Detected incomplete framing, invalid counts or numbering, repeated identities,
inconsistent permalinks, conflicting representations, file sections and reserved
framing inside matched text refuse with an issue code and no result entries.
The context-free count check remains strict; only context-enabled pages admit
the explicitly partial rendered-result form described above.
The original response is unchanged. A structurally complete rendering does not
prove that the provider returned the complete authored message body.

### Read the rendered search query separately

The search projection keeps the caller's exact `source.request_args` and
separately exposes the query text printed in the native search preamble:

| Source field | Meaning |
| --- | --- |
| `rendered_query` | Literal text following `# Search Results for: ` on the recognized heading line. An empty heading remains `""`; no requested keyword or filter is substituted. |
| `rendered_query_range` | Half-open UTF-16 range of that text in the decoded native `results` string. An empty heading has an empty range. |
| `search_preamble_range` | Half-open range of the complete recognized heading and its fixed two-newline separator. |
| `query_application` | Always `not_verified`. The projector does not establish which selectors the provider applied. |

The three rendered fields start as `null` and are populated only after a
consistent native representation and recognized preamble are available. They
may remain available as source diagnostics if later result framing refuses.
A null value is not an observed empty heading.

Keep requested selectors and rendered text separate. A heading can be empty
even when the caller supplied keywords or filters; it can also accompany
returned messages. Neither an empty heading nor matching text proves that the
provider ignored or applied the request. Do not rebuild the original request,
infer a missing search restriction, or declare an ownership search complete
from this heading. Native pagination and retained-page coverage keep their
existing, limited meanings.

There is no trimming, decoding, query rewrite or normalization beyond reading
the already-decoded envelope string. The original native response remains
unchanged. The preamble is charged by the existing input budget; its returned
metadata is additional to the body budget and can contain private search terms.
The collector, result identities, body selection and provider calls are unchanged.

The actual October 4 intake included a retained keyword/filter response with an
empty heading. Its new metadata was `rendered_query: ""`, query range
`[22,22]` and preamble range `[0,24]`, alongside the original requested
arguments. Another already-projected retained response kept every previous
field JSON-identical after excluding these four added source fields.
One subsequent, needed public tooling search returned a nonempty heading and
zero results; the new query and preamble ranges matched its original rendering
exactly. Both empty-result outcomes remain scoped to those captured responses.
Inputs were unchanged; no request was replayed, fixture created or OS process run.

### Page coverage and navigation

The statuses are `PROJECTED`, `PARTIAL`, `EMPTY_RENDERING` and `REFUSED`.
`PARTIAL` means a context-enabled page rendered fewer matches than it declared.
Only the exact observed `No results found.` rendering after the search preamble is accepted
as an empty page. It describes that retained query and cursor, not a global
empty work queue or full workspace search.

Coverage reports declared, parsed and returned result counts; omitted results;
content truncation; and the existing recognized native pagination state.
`next_index` advances through this retained page only. Provider cursor handling
remains with the unchanged collector. A native ending covers only its original
query, filters and cursor chain, and is never inferred from an empty rendering.
Unknown pagination can accompany a structurally projected page.

With `source_indices`, the helper parses the complete retained page once and then
returns the selected entries in their original order. Only their content consumes
the output budget. Input charging, framing, identity checks, source ranges and
surrogate-safe clipping still cover the full source. This avoids invoking the
projector separately for each nonadjacent result.

The selector is copied. Holes, duplicate or unordered indices, negative or unsafe
integers, too many entries, and an explicitly supplied `start_index` raise
`TypeError`. After full source parsing, an index outside that page returns
`REFUSED / SOURCE_INDEX_OUT_OF_RANGE` with no results and the parsed result count.
Indices belong only to this retained response; they are not message timestamps
or provider cursors and must not be reused for a different page.

Sparse coverage adds `selection_mode: source_indices`, a copied
`selected_source_indices`, `omitted_results`, `omitted_interior` and complete
half-open `omitted_source_index_ranges` with `source_index_range_end: exclusive`.
It reports `start_index: null`, `next_index: null` and
`navigation: caller_selected_indices`. Leading and trailing omissions remain in
`omitted_before` and `omitted_after`; content counts describe selected entries.
An empty selector is valid: a nonempty page remains `PROJECTED`, all omissions
are assigned to `omitted_after`, and its omitted range is `[0, parsed_results)`.
An empty source remains `EMPTY_RENDERING`. Native pagination is independent of
the selection, and no selector preserves the previous contiguous result shape.

Actual bounty intake used indices `[0,1,6]` from a retained 12-result response.
One selection returned all 8,857 selected content code units with omitted ranges
`[[2,6],[7,12]]`; the previous per-result path required three projector calls for
the identical entries. The ordinary overview remained JSON-identical, and no
additional provider read was made. This measures parsing calls, not wall time.

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
`EMPTY_RENDERING`. At that initial implementation, a separately retained
context-enabled search returned `REFUSED / UNSUPPORTED_REQUEST` using its actual
request; the later context projection above extends that unsupported case. The DM Participants
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


### Public search continuation use, 2026-10-04

The new operation consumed the next still-unread cursor from an actual public
tooling-intake search. One connected call selected only
`slack_slack_search_public`, retaining the original query arguments and native
response. It returned 12 detailed results in 37,526 rendered code units and
stopped at the one-page budget with the next public cursor preserved.

Projection retained `source.operation: search_public`, all 12 rendered
identities and exact source ranges. It returned 13,820 content code units;
10 bodies were explicitly truncated. Every returned prefix matched its original
source slice. The callback copy matched the retained native response, and the
request and response stayed unchanged.

The existing `search` projection of this same newly obtained page was
JSON-identical under the previous and current source. Source composition
preserved all earlier behavior except the explicit additional operation,
its field validation and its projected operation label. The schema check used
the current exposed public tool definition; no private search, old provider
request replay, OS process, fixture or repository test was run.
