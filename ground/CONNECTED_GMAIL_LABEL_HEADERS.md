# Retained Gmail label headers

`host/connected_gmail_label_headers.cjs` projects a supplied successful native `mcp__codex_apps__gmail_list_labels` response. It makes no provider calls, reads no messages, and changes no mail or labels. Keep the original request and complete raw response alongside the projection.

```javascript
const {projectGmailLabelHeaders} = require('./host/connected_gmail_label_headers.cjs');
const view = projectGmailLabelHeaders(retainedNativeResponse, {
  indices: [0, 2],
  max_labels: 2,
  max_field_chars: 256,
  max_total_metadata_chars: 200,
});
```

Native `list_labels` accepts optional label display names in `label_names`. Use the returned literal `id` for a subsequent search's `label_ids`. This projection does not dispatch either operation or verify that an earlier filter was applied. The expected binding is documentary; a response alone does not authenticate its origin or account.

The supported envelope is `structuredContent.labels`, a dense array of objects. The helper validates the entire supplied array before selecting rows. Each selected row retains its zero-based source index and literal field paths. It selects `id`, `name`, `type`, `messageListVisibility`, `labelListVisibility`, `messagesTotal`, `messagesUnread`, `threadsTotal`, and `threadsUnread`. Other fields stay outside the projection.

Text fields return whole values or `limit_exceeded`; empty strings remain included literal values. Missing fields, nulls, and wrong types stay distinct. Counts return only nonnegative safe integers, including a literal zero. Missing, null, fractional, negative, nonfinite, unsafe, or string count values do not become zero. Message and thread counts remain separate. The helper neither sums overlapping labels nor derives total-mailbox counts, verification state, or completion of account setup.

| Option | Default | Range |
| --- | --- | --- |
| `indices` | First supplied rows within `max_labels` | Dense, unique indices below 10,000 and within the actual array |
| `max_labels` | 20 | 0–500 |
| `max_field_chars` | 256 | 0–4,096 UTF-16 code units per complete text field |
| `max_total_metadata_chars` | 4,000 | 0–64,000 UTF-16 code units across included text values |
| `max_response_chars` | 1,048,576 | 256–8,388,608 serialized JSON code units |

At most 10,000 source labels are accepted. Explicit indices must fit `max_labels`; duplicate, sparse, noninteger or negative selections are rejected. Invalid options throw before projection. Unsupported/error envelopes, source limits and out-of-range source indices return `REFUSED` with no projected rows. A nonempty supplied array with no selected rows is `EMPTY_SELECTION`; an empty supplied array is `EMPTY_SUPPLIED_ARRAY`. Neither status establishes an empty mailbox or complete label catalog.

Coverage reports supplied and selected rows, omitted rows, metadata characters and included/unavailable count fields. `all_supplied_labels_included` describes this supplied array only. No snapshot, observation timestamp, catalog completeness, request-filter application or account identity is inferred. The helper has no clock, filesystem, imports, authentication, retry or transport. The complete raw response is neither returned nor modified.

The initial activation consumed one retained native read requested for the system labels INBOX, SENT and UNREAD. Three actual rows were supplied; indices 0 and 2 were projected. The result included eight literal count fields and retained their exact native source paths. Complete retained request, response and options remained equal under JSON serialization. The activation made no additional provider operation and read no message body. This is a projection receipt, not a mailbox-wide completion claim or proof of a positive account verification email.
