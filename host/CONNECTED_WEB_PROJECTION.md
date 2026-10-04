# Project retained web source responses

Use [connected_web_projection.cjs](connected_web_projection.cjs) to inspect web-tool source responses without printing every returned page in full. The synchronous public API retains each detected source reference, title, URL and word limit, and puts explicit bounds on the returned content. It makes no provider calls and does not mutate the supplied response.

The caller retains the complete original response. Every range points back into one original text content item; selected previews are never treated as complete pages or complete search results.

## Public API

The module has no dependencies and works as CommonJS or through the existing in-memory module loader.

~~~js
const { projectWebSources } = require("./host/connected_web_projection.cjs");

const overview = projectWebSources(retainedResponse, {
  max_sources: 8,
  max_content_chars: 400,
  max_total_content_chars: 3200
});
~~~

Pass the actual web-tool CallToolResult with its content array. The supported source header rendering has a title and HTTP(S) URL on one line, followed by a returned search/view/fetch/news reference and a numeric word-limit marker. The adapter reads that rendering; it does not synthesize source IDs from URLs or interpret arbitrary prose as an empty result set.

A successful response has status PROJECTED and a sources array. Each source includes:

| Field | Meaning |
| --- | --- |
| source_index | Position across all parsed source blocks, in original content-item order |
| content_index | Index of the original text item in the supplied content array |
| reference_id, title, url, word_limit | Fields read directly from the supported rendered header |
| rendered_source_range | Entire source block, from its title to the next detected source header or text-item end |
| rendered_header_range | Title, URL, reference and word-limit prefix |
| rendered_content_range | Remaining source content, including returned crawl/publication metadata and page text |
| rendered_content | Bounded literal prefix of that content |
| returned_content_range | Exact range of the returned prefix |
| content_chars, returned_chars, truncated | Full content length, returned length and explicit truncation state |

All ranges are half-open UTF-16 code-unit offsets in response.content[content_index].text. They are **rendered response ranges**, not byte offsets in the original web page. CRLFs, entities, citations, line labels and separators are retained. The adapter does not decode HTML entities, remove link wrappers, normalize whitespace, or turn an open-result line label into a page byte offset. A prefix boundary backs up one code unit if necessary to avoid splitting a surrogate pair.

The rendered source block extends to the next header. Inter-source separator lines immediately before that header consequently remain at the end of the preceding content range.

## Continue within the retained response

For a contiguous view, use start_index and max_sources. coverage.next_index points to the next retained source index when more parsed sources remain. It is not a provider cursor or a command to search again.

~~~js
const next = projectWebSources(retainedResponse, {
  start_index: overview.coverage.next_index,
  max_sources: 4,
  max_content_chars: 1200,
  max_total_content_chars: 4800
});
~~~

Call this form only when next_index is a non-null integer. A metadata-only request can use max_sources: 0; its unchanged next_index is not forward progress.

After an overview, select exact observed source indices without spending the output budget on intervening bodies:

~~~js
const selected = projectWebSources(retainedResponse, {
  source_indices: selectedIndices,
  max_sources: selectedIndices.length,
  max_content_chars: 12000,
  max_total_content_chars: 24000
});
~~~

The indices must be distinct, nonnegative, strictly increasing and within the parsed response. max_sources must accommodate the entire list. An explicit start_index cannot accompany source_indices. Sparse selection returns null start_index and next_index, plus the full selected_source_indices and omitted_source_index_ranges. Omitted ranges are half-open source-index intervals.

Selection is a caller decision based on the actual overview. There is no domain, keyword, recency, authority or relevance filter in the adapter.

## Bounds

| Option | Default | Accepted range |
| --- | ---: | --- |
| start_index | 0 | Nonnegative safe integer within the parsed source count |
| max_sources | 8 | 0–100 |
| max_content_chars | 800 | 0–100,000 per selected source |
| max_total_content_chars | 6,400 | 0–1,000,000 across selected sources |
| max_input_chars | 1,048,576 | 1–8,388,608 across all text items |
| max_header_chars | 4,096 | 128–16,384 per title/URL/reference/word-limit prefix |

A source's title, URL and reference remain complete. An oversized header produces an explicit input-limit result instead of a shortened URL that might be mistaken for a usable source link. Content budgets cover rendered_content; they are not a token estimate or a bound on the complete JSON output, which also contains headers and coverage metadata.

All text is parsed before output selection. Limiting the returned sources does not imply that unselected input was never received or consumed. At most 4,096 content items are accepted.

## Coverage and non-success outcomes

The output always identifies its scope as retained_response_only, snapshot false, and provider_completeness not_inferred. It reports parsed source count, selected and omitted indices, selected/returned content lengths, and truncated source count.

Non-text items are identified by their original index and type; their payload is not decoded or represented as page text. Text before a recognized first header, and complete text items with no supported header, remain visible as unparsed_text_ranges. Duplicate rendered reference IDs are preserved as separate source entries and listed in duplicate_reference_ids; the adapter does not silently deduplicate them.

all_rendered_source_content_included means that all detected blocks were returned without content truncation. It does not assert completeness of the underlying pages, retrieval results, provider pagination or non-text payloads. all_input_text_has_source_headers describes only the absence of unparsed text ranges in this rendering.

| Status | Meaning |
| --- | --- |
| PROJECTED | Supported source blocks were parsed; inspect all coverage fields |
| PROVIDER_ERROR | The supplied envelope has isError true |
| UNSUPPORTED_REPRESENTATION | The envelope/content-item shape cannot be consumed |
| INPUT_LIMIT | A content-item, text or header bound was exceeded |
| UNSUPPORTED_RENDERING | A detected word-limit field cannot be represented safely |
| UNRECOGNIZED_RENDERING | No supported source headers were found |

A no-header result is **not** evidence that a search found zero results. It may be another native rendering, a provider notice or text that requires direct inspection. Invalid caller options throw TypeError or RangeError rather than silently changing selection.

## Evidence boundary

A requested domain filter does not establish that returned URLs satisfy it. The overview makes the observed URLs available to the caller, without filtering away mismatches.

A reference is labeled rendered_header identity. The parser cannot authenticate a web page, distinguish an exact header-shaped quotation from a renderer-issued header, validate a redirect, or establish source authority. Retain the original tool envelope and available citation references when attributing a claim. No provider fetch, screenshot, PDF-byte read, page completeness or factual verification is implied by projection.

The adapter preserves the returned word_limit metadata; it does not enforce quotation or source-use limits. Those limits still apply when writing from a source.

This helper is separate from [connected_slack_pages.cjs](connected_slack_pages.cjs), GitHub issue search, and retained HTTP-capture summaries. It adds no retrieval, credential, publication, execution or capacity policy.

## Actual intake use

The initial consumer was the October 4 R.O.A.D. Barbados source intake. The retained search response contained 35,134 UTF-16 code units and eight unrelated source headers despite the caller's requested domain. One actual API call returned all eight original references/URLs with 1,120 content code units and all eight truncation flags.

The next official-page open used the existing URL from the baseline README. Its fresh retained response contained 19,638 code units and one supported source. The consumer first read a 600-code-unit preview, then selected that observed source index for its complete 19,459-code-unit content. Both calls used the same retained response; no search/open operation was replayed.

These were calls to the exported API on actual tool responses. No synthetic input, fixture, new test, native process, screenshot or copied source-body artifact was used. The full responses and selections remain in the caller's session; this guide stores only the operating example and measured scope.
