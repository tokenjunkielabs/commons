# Collect native Gmail search pages and display selected headers

`connected_gmail_search.cjs` provides bounded, read-only pagination for the existing native Gmail search tool. It prevents argument-name guessing and keeps the request, raw page, pagination state and displayed headers separate. It performs no mail changes, MIME parsing, query rewriting, automatic retry or account lookup.

The actual native declaration is:

```js
search_emails({query?, label_ids?, max_results?, next_page_token?})
```

The continuation argument is next_page_token. page_token is not supported. A successful observed native response has structuredContent.emails and structuredContent.next_page_token. This module accepts that specific envelope; it does not infer success from text that looks like JSON or a tool error message.

The existing [CONNECTED_GMAIL_MESSAGES.md](CONNECTED_GMAIL_MESSAGES.md) and connected_gmail_messages.cjs remain the separate full-message/MIME projection path. Its source b8401d85ed467855c6a18a2d065e2069d4e0bb9c exports only projectGmailMessages. The supplied current host inventory and that export were checked before adding this collector; the MIME reader is unchanged.

## Load the module

CommonJS:

```js
const {collectGmailSearchPages, projectGmailSearchHeaders} = require('./connected_gmail_search.cjs');
```

Connected V8, after the caller explicitly acquires and verifies the complete published source:

```js
const box = {exports: {}};
new Function('module', 'exports', verifiedSource)(box, box.exports);
const {collectGmailSearchPages, projectGmailSearchHeaders} = box.exports;
```

The module has no dependency, filesystem, transport or credential implementation. Its only native binding is mcp__codex_apps__gmail_search_emails on the supplied tools object.

## Request and retained custody

Pass an args object with only the four native keys, plus local budgets:

```js
const request = {
  args: {query: authorizedQuery, max_results: 20},
  max_pages: 2,
  timeout_ms: 30000,
};
const collection = await collectGmailSearchPages(journaledTools, request);
```

The query is opaque. Exact label IDs, their order and duplicates are preserved; null and an empty array remain distinct. Gmail operators belong in query, not label_ids. The module validates bounded shape, not the meaning of label IDs or Gmail query syntax. The local default max_results is 20. Query, labels and page size remain fixed across pages; only the opaque next_page_token changes. No token is trimmed, decoded or synthesized.

Each page records page_index, the complete normalized request_args, its response_index, status, row count and native continuation. The raw response is retained in responses before inspection. Native errors and malformed payloads are retained as failures, not interpreted as empty pages. A thrown call has no invented native response; its exception name/message and original thrown value are retained separately.

Bank native arguments and responses before handing them back to the collector. Keep raw, collection and projection keys distinct, including any outer orchestration result key. For example:

```js
let callIndex = 0;
const journaledTools = {
  async mcp__codex_apps__gmail_search_emails(args) {
    const key = operationKey + '/native/' + callIndex++;
    store(key + '/request', args);
    try {
      const raw = await tools.mcp__codex_apps__gmail_search_emails(args);
      store(key + '/response', raw);
      return raw;
    } catch (error) {
      store(key + '/thrown', {name: error?.name, message: error?.message});
      throw error;
    }
  },
};
store(operationKey + '/request', request);
const collection = await collectGmailSearchPages(journaledTools, request);
store(operationKey + '/collection', collection);
const headers = projectGmailSearchHeaders(collection, {max_messages: 20});
store(operationKey + '/headers', headers);
text({status: headers.status, source: headers.source,
  coverage: headers.coverage, messages: headers.messages, issue: headers.issue});
```

Do not print the full collection or raw response: native search rows include snippets and attachment-related fields even though the header projection omits them. Durable source/activity checkpoints and operation keys remain caller responsibilities; memory storage is not represented as guaranteed durable storage.

## Pagination and stopping

Only an explicit native null next_page_token establishes provider END for this traversal. An empty emails array with a non-null token still has a continuation. A missing, empty, oversized or malformed token is unknown/unsupported pagination, never END.

The summary distinguishes:

| stop_reason | Meaning |
| --- | --- |
| PROVIDER_END | A successful retained page explicitly returned null. |
| PAGE_BUDGET | The local page budget was reached with a native continuation. |
| TIME_BUDGET | The local elapsed-time budget prevents another call. |
| RESPONSE_BUDGET | A returned page exceeded a serialized response budget; raw remains retained. |
| TOKEN_CYCLE | A token repeats within this invocation, including its initial supplied token. |
| NATIVE_ERROR | The native envelope reports failure. |
| THROWN_ERROR | The call threw; no native response is invented. |
| PAYLOAD_ERROR | The returned successful-looking shape could not be interpreted under this contract. |

next_request retains all normalized arguments and local budgets. Read next_request_basis with it:
- native_next_page_token means it follows a parsed successful page.
- unattempted_request means dispatch did not begin.
- unresolved_current_request preserves the request at which interpretation or the call failed.
- repeated_native_token records a detected cycle.
- none_provider_end accompanies a null next_request.

The latter failure/cycle records are custody, not an automatic retry mechanism. The module does not retry or switch routes. Token-cycle memory is local to one invocation; it is not a cross-session pagination history. A new deliberate continuation is a new call with its own budgets.

timeout_ms is a soft elapsed-time budget checked between calls. It does not cancel or impose a deadline on an in-flight native request. Size budgets are checked after the full raw response is delivered and retained; they do not bound the provider's transferred payload. One oversized or failed response can therefore remain in custody even when it prevents further traversal.

Query application is always not_verified, snapshot is false, and account identity is not_inferred. Provider END does not establish global mailbox absence, authentication, chronological enforcement, authorization, work eligibility or absence of messages outside the requested query.

## Header-only projection

projectGmailSearchHeaders(collection, options) selects by zero-based start_index across the successful retained pages in their original order. max_messages limits returned rows. It never deduplicates or sorts native rows.

The projection validates the collector schema, fixed request binding, page order, response mapping and recorded continuation against retained successful native pages. It is a reader of supplied custody, not cryptographic proof that an arbitrary supplied object came from Gmail.

Every returned row contains its source_index, source_page_index, source_row_index and exact responses[i].structuredContent.emails[j] source_path. Its fields object selects only:

- id and thread_id, as complete strings;
- from_ and subject, as bounded string prefixes;
- email_ts, as a complete string or finite number without date parsing;
- has_attachment, as a boolean.

Each field reports its original source_path and included/missing/invalid_type/limit_exceeded/truncated status as applicable. Identity and timestamp strings are omitted on a field budget breach instead of being returned as misleading prefixes. String truncation preserves surrogate pairs.

All other native fields are unselected by default, including to, cc, bcc, snippet, labels, attachments, inline_images, display_url, display_title and any body/payload fields. body_withheld means no body is displayed; it does not assert that a body was present in the search row. MIME type or header projection does not establish secret redaction.

Coverage separately reports successful pages/rows, omitted rows, next local index and string-character loss. all_successful_rows_included is a row-selection statement, not complete-header or full-mail coverage. Numeric/boolean fields and metadata overhead are bounded by the row limit but are not counted in the string-character budget.

Projection status is PROJECTED, EMPTY_PAGE, PARTIAL, UNAVAILABLE, NO_SUCCESSFUL_PAGES or REFUSED. A failed page may leave earlier successful headers available as PARTIAL; a failure with no successful rows is UNAVAILABLE. An empty successful page is not conflated with either. The collector's stop reason is reported separately, and native END is derived from the selected collector's retained successful pagination. No withheld body is represented as read or inspected.

## Budgets

| Setting | Default | Maximum |
| --- | ---: | ---: |
| Native max_results (local ceiling) | 20 | 100 |
| max_pages | 1 | 10 |
| timeout_ms (soft) | 30,000 | 60,000 |
| max_response_chars | 1,048,576 | 8,388,608 |
| max_total_response_chars | 4,194,304 | 16,777,216 |
| Projection start_index | 0 | 1,000 |
| Projection max_messages | 20 | 1,000 |
| Projection max_field_chars | 300 | 4,000 |
| Projection max_total_header_chars | 12,000 | 64,000 |

All character counts use JavaScript UTF-16 units. Response-size counts measure JSON.stringify(raw). Query and token strings are limited to 8,192 characters; label_ids permits at most 100 dense nonempty strings of at most 256 characters each. These are published local limits, not claimed provider limits.

## First actual consumer and limits

Before publication, source 69184e7c017db12882791511249622f9126b8925 was used once for a newly authorized mail window, after the preceding owner intake boundary. The exact query was after:1791211919 before:1791213730 with max_results 20, max_pages 1 and timeout_ms 30000. This covers the requested 2026-10-05 14:51:59–15:22:10 UTC interval; query enforcement is still not_verified.

One actual native call returned two rows and an explicit null continuation token. The collector retained the complete 1,985-character serialized response and original native arguments before interpretation. One header projection with max_messages 20, max_field_chars 200 and max_total_header_chars 10000 returned two rows and 377 header characters with no field loss. The retained collection was unchanged. Snippets, bodies and attachment details were not selected or displayed; subject-level holds were preserved. No private headers, mail IDs or bodies are copied into this repository.

This was new operational intake, not an accepted-query replay or generated input. It exercised one successful page, explicit-null END and ordinary header projection. Multi-page continuation, non-null empty pages, cycles, malformed/failed/thrown responses, timeout/size limits and clipping/refusal paths were inspected in source only. No synthetic fixtures, tests, MIME parsing, mail mutation, native executor or replacement transport was used.

Operation CONNECTED-GMAIL-SEARCH-PAGES-20261005-7CA6. Activity1791213684.569489 in C0BS7AZ4BSL. Stable publication branch work/connected-gmail-search-pages-20261005-7ca6.

## Observe reported email timestamps against explicit bounds

The additive export inspectGmailSearchEmailTimestamps(response, options) reads one already retained native search response. It compares only the provider's reported email_ts metadata with caller-declared exclusive after and before instants. This makes a timestamp outside the local observation window visible without treating it as proof that Gmail applied the search query incorrectly.

The native search-date field and the meaning of email_ts have not been established as identical. The observer therefore always reports query_application: not_verified and provider_search_date_semantics: not_established. Its result does not establish receipt time, delivery time, account identity, authentication or a mailbox snapshot.

Use the exact retained native response, without constructing a collector or making another search call:

~~~js
const {inspectGmailSearchEmailTimestamps} = box.exports;
const observation = inspectGmailSearchEmailTimestamps(retainedNativeSearchResponse, {
  after: declaredAfterInstant,
  before: declaredBeforeInstant,
  max_records: 20,
});
store(operationKey + '/timestamp-observation', observation);
text(observation);
~~~

The original collector and header projector remain byte-for-byte unchanged in source. The new export performs no native call, request rewrite, message filtering, retry, sort, deduplication, mail change or MIME work. It does not serialize the complete response or select message bodies, snippets, addresses, subjects, identifiers or attachment fields.

### Input and instant contract

The response uses the same strict native page parser as the existing collector: structuredContent.emails must be a dense array of objects, and structuredContent.next_page_token must be explicit null or a bounded nonempty string. Native error envelopes and malformed page shapes remain refused observations. The input cap is 100 rows, a local limit. Validating pagination shape does not turn this one-page reader into a traversal or give its output a provider-END claim.

At least one of after and before must be supplied. Both are exclusive: a reported instant at or before after is outside the window, and an instant at or after before is outside it. When both are supplied, after must strictly precede before. Malformed, unsupported, equal or reversed caller bounds throw INVALID_INPUT before observing rows; they do not produce a misleading all-outside result.

Supported instant strings have this deliberately bounded grammar:

~~~text
YYYY-MM-DDTHH:mm:ss[.S|.SS|.SSS](Z|+HH:MM|-HH:MM)
~~~

The reader validates the written calendar date, including leap-year month lengths, and the written clock before converting the explicit offset. It avoids Date.UTC's special handling of years 00 through 99. Timezone hour and minute components must be in range. The unknown-offset spelling -00:00 is unassessed; it is not silently treated as a known UTC instant.

Unassessed reasons distinguish missing fields, null, unsupported types, numeric timestamps with unspecified units, unsupported formats, oversized strings, invalid calendar/clock values and invalid/unknown offsets. Numeric-looking strings remain unsupported formats; finite numbers never acquire guessed second or millisecond units. Leap-second, 24:00, local-time-only, lowercase-zone and longer-than-three-fractional-digit spellings are outside the supported instant contract. The existing header projector can still preserve a numeric email_ts; the observer's narrower interpretation does not change that display contract.

### Inspection, diagnostic output and status

Every supplied row within the 100-row cap is inspected. max_records limits only emitted diagnostics, with default 20 and allowed range 0 through 100. It does not stop timestamp assessment. Each timestamp string is limited to 64 UTF-16 units. These local interpretation limits do not bound the provider payload already delivered to the caller.

A diagnostic contains source_index, the exact structuredContent.emails[i].email_ts source_path, and either an outside-window relation or an unassessed reason. It contains neither the raw nor normalized timestamp value, and no message identifier or row copy. The caller can inspect the original retained row only when independently appropriate.

The statistics distinguish supplied, inspected, assessed, inside, outside and unassessed rows. Separate lower- and upper-bound counts identify which exclusive comparison failed. unassessed_by_reason retains fixed reason categories. diagnostic_rows, returned_records and omitted_records distinguish output truncation from interpretation coverage.

| Status | Meaning for this supplied page |
| --- | --- |
| OUTSIDE_REPORTED_TIMESTAMP_OBSERVED | At least one assessed reported timestamp is outside the declared window; unassessed rows may also exist. |
| INCOMPLETE_TIMESTAMP_ASSESSMENT | No outside timestamp was observed, but one or more supplied timestamps could not be assessed. |
| NO_OUTSIDE_REPORTED_TIMESTAMP_OBSERVED | Every supplied timestamp was assessed and none was outside the declared window. |
| EMPTY_PAGE | The successful native page supplies zero timestamp rows. |
| REFUSED | The native envelope or page shape is not accepted; issue records the interpretation failure. |

all_rows_inspected is separate from all_supplied_timestamps_assessed. A missing or unsupported value counts as inspected but unassessed. Both statements are scoped to the supplied rows; an empty-page result cannot establish mailbox absence or query fidelity. A bounded diagnostic list never implies that omitted diagnostics were absent.

### First actual observation

Before publication, source 834a79dd1f2646681dd7b3df26ee03d2ce0901c5 consumed the newly retained five-row native mail-search response once. Its original request used after:1791226029 before:1791227338 with max_results 20. The independently declared observation bounds were 2026-10-05T18:47:09Z and 2026-10-05T19:08:58Z, with max_records 20.

All five reported timestamps were inspected and assessed. Four lay within the declared exclusive window; one was before the lower bound, and none was at or after the upper bound. The reader returned one source-path/relation diagnostic, with zero unassessed or omitted records. The complete retained native input remained unchanged. No native search was repeated, and no private message identifiers, headers or timestamp values are reproduced here.

This actual use exercised explicit-offset parsing, both declared bounds, ordinary within-window rows and a lower-bound observation. Missing/null/numeric values, unsupported spellings, invalid calendars, offset edge cases, exact-boundary equality, upper-bound observations, output-budget omission, empty/error pages and malformed requests were inspected in source only. There were no generated inputs, synthetic fixtures, tests, MIME reads, mail mutations or executor runs. No claim is made that the reported timestamp proves a Gmail query failure.

Operation CONNECTED-GMAIL-REPORTED-TIMESTAMPS-20261005-7CA6. Activity1791227824.704119 in C0BU51F1PL3. Publication branch work/gmail-reported-timestamps-20261005-7ca6.
