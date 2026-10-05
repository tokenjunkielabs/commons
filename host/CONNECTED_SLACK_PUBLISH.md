# Publish exact text through connected Slack tools

`host/connected_slack_publish.cjs` packages the native send-and-edit sequence
used by cloud workers. The connected sender can append a generated footer;
the native editor accepts the caller's exact text through `markdown_text`.
This helper sends once, retains the returned channel/message/link, then edits
that same message once with the original text. It also supports an edit-only
continuation when the caller already has a confirmed message ID.

It uses the caller's discovered Slack bindings. It performs no discovery,
credential lookup, login, independent HTTP request, automatic retry or text
rewriting. The caller supplies the authorized destination and finished message.

## Use in a tool-enabled JavaScript session

Load the complete helper from the observed GitHub source and evaluate it in the
same tool-enabled session:

```javascript
const moduleBox = {exports: {}};
new Function('module', 'exports', helperSource)(moduleBox, moduleBox.exports);
const {publishSlackMessage} = moduleBox.exports;

const result = await publishSlackMessage(tools, {
  channel_id: observedChannelId,
  thread_ts: observedParentTimestamp,
  message: preparedMessage,
}, {
  onProgress: async progress => store('my-operation-slack', progress),
});
text(result);
```

For Node callers, use `require('./host/connected_slack_publish.cjs')` and supply
the actual native tool functions. Required default binding names are
`mcp__codex_apps__slack_slack_send_message` and
`mcp__codex_apps__slack_slack_edit_message`. Alternate exposed names can be
passed as `bindings: {send: observedSendName, edit: observedEditName}`.

`thread_ts` is optional. New sends also accept the native `reply_broadcast` and
`unfurl_app_links` boolean options. Unsupported fields fail before a provider
call. The helper does not split, truncate, trim or otherwise normalize the body.

For an existing message, provide its observed `message_id` and channel:

```javascript
const updated = await publishSlackMessage(tools, {
  channel_id: savedProgress.channel_id,
  message_id: savedProgress.message_id,
  message: preparedCompletion,
}, {
  onProgress: async progress => store('my-operation-slack', progress),
});
```

This path needs only the edit binding and never sends a second message.
New-send options are rejected on the edit-only path. Use the channel returned
by the provider; sending to a user ID can resolve to a different DM channel ID.

## Outcomes and interrupted operations

Success returns `status: updated`, `message_state: edit_confirmed`, the confirmed
message ID and channel, call counts, and the provider link when a new send
returned one. This means the editor acknowledged the selected message.
By default, `readback_status: not_performed` remains explicit. The optional
native readback below captures a bounded provider response after the edit;
it does not compare content by default. The pure opt-in comparator below can
inspect that captured rendering.

The send and edit are separate provider operations. A generated footer can be
visible between them; a failed edit can leave it in place. No operation is
automatically repeated. Failures throw `SlackPublishError` with operation metadata
available through `progress`, the original `cause`, and the last native
`response` for private inspection. Progress never contains the message body or
raw provider error text.

| Last message state | Required continuation |
| --- | --- |
| `not_attempted` | Resolve the input or missing binding; no send was attempted. |
| `send_outcome_unknown` | Read the intended channel/thread for the existing operation before any new send. An error or unreadable response may follow an accepted write. |
| `sent` or `edit_outcome_unknown` | Retain the returned channel and message ID. Inspect that message and, if needed, continue with the edit-only path. |
| `edit_confirmed` | The edit was acknowledged. Use the optional native readback or a read-only `readSlackPublication` continuation; do not resend because the read failed. |

The optional observer receives copied metadata before each write, after the
send acknowledgement and after completion or failure. Observer errors are
counted and do not block publication. Keep the stable operation ID in the
ordinary message and retain progress through the existing host. There is no
new journal, receipt file, dispatcher or approval step.

## Optional bounded native readback

Pass `readback: true` to capture one native read after the edit acknowledgement:

```javascript
const result = await publishSlackMessage(tools, {
  channel_id: observedChannelId,
  message: preparedMessage,
}, {
  readback: true,
  onProgress: async progress => store('my-operation-slack', progress),
});
const {readback_response, ...progress} = result;
store('my-operation-slack-read', readback_response);
text(progress);
```

The additional default binding is
`mcp__codex_apps__slack_slack_read_thread`; override it with
`bindings: {readback: observedReadName}` when discovery exposes an equivalent
native name. When readback is requested, a missing read binding is detected
before sending or editing. Neither mode performs its own discovery.

`readback_status: captured` means a readable native response was retained
as `result.readback_response`. This is the original tool response, including
rendered messages and pagination information. It is kept outside observer
metadata; `onProgress` still receives no message body or raw provider error.
Keep the response privately and inspect the intended message when the task
requires content confirmation. The native reader can present a URL as Slack
link markup or return an empty result. Capturing either response does not
prove the requested body was present or equal, and the helper never rewrites
or normalizes the retained response. The opt-in comparator operates on a separate
comparison value.

The request uses `limit: 1`. For a top-level message it reads that observed
message timestamp directly. For a new thread reply, it uses the retained
`thread_ts` as the parent and a timestamp interval immediately around the
confirmed reply ID. This avoids paging through the surrounding thread. The
native response may include the parent in addition to the selected reply.
`readback_request` records the exact native arguments. No next page is
automatically requested.

For an edit-only operation on a reply, supply the previously observed parent
as `readback_thread_ts` in options. The editor acknowledgement does not
supply that parent. This option must agree with `thread_ts` on a new send;
the helper never guesses a parent from a search result.

If the read fails, `SlackPublishError.progress` preserves
`status: updated` and `message_state: edit_confirmed`. A read that was
attempted has `readback_status: failed`; validation failures remain
`not_performed`. Its original native response, if any, is available through
the error's existing `response` field. The successful write is not repeated.

Resume only the read with the new export:

```javascript
const {readSlackPublication} = moduleBox.exports;
const result = await readSlackPublication(tools, savedProgress, {
  // For an edited reply whose parent was not already retained:
  readback_thread_ts: observedParentTimestamp,
  onProgress: async progress => store('my-operation-slack', progress),
});
store('my-operation-slack-read', result.readback_response);
```

The continuation requires the existing confirmed-edit metadata. It copies
call counts, preserves the selected channel/message/link and retained parent,
and makes one read call with no send or edit. Previously captured responses
are not copied into progress callbacks. The caller decides whether to resume
after inspecting an error; there is no retry loop, approval step or work gate.

## Compare the selected captured rendering

The pure, opt-in export `compareSlackPublication(result, expectedMessage, options)`
selects one message from the existing bounded native readback. It performs no
provider call and changes neither the publication result nor the expected text.
Existing send, edit, read, continuation and captured-status behavior is unchanged.

```javascript
const {compareSlackPublication} = moduleBox.exports;
const comparison = compareSlackPublication(result, preparedMessage, {
  normalization: 'slack_bare_urls_entities',
});
text(comparison); // Metadata only; no message body.
```

Omit options, or use `normalization: 'none'`, for literal comparison only.
The expected message is supplied separately because progress does not retain
message bodies. Invalid caller arguments or unsupported options raise TypeError.

| Status | Meaning |
| --- | --- |
| `exact` | The selected rendered body equals the expected text literally. |
| `presentation_match` | It equals the expected text only after the explicitly enabled transformations below. |
| `mismatch` | The body was selected unambiguously and differs under the requested comparison. |
| `uncomparable` | Capture, request identity, payload, target selection or framing is insufficient or ambiguous. |

`matches` is true for the first two outcomes, false for mismatch and null for
uncomparable. `literal_match` preserves the literal result separately. The
metadata includes the selected channel/message/parent IDs, the requested
normalization and counts of applied URL/entity transformations. An uncomparable
result carries a reason code; it does not turn the acknowledged write into a
failed send or authorize resending it.

The comparator requires a confirmed edit and captured response. It checks the
retained read request against the publisher's selected channel, parent, limit and
reply window. It accepts one recognized detailed thread payload (or identical
duplicate representations), then only the observed framing for a parent message alone or a parent with
one reply. The provider's exact no-replies trailer and section separators
are removed as envelope text. Body whitespace, newlines and literal backslashes
are preserved. Marker-like body lines, duplicate IDs, conflicting payloads,
unknown formats or broader thread renderings return uncomparable. It does not
page, trim, unescape literal backslash-n, or infer missing messages.

Channel binding is explicitly `retained_readback_request`: this native rendering
contains message timestamps but no channel ID. The result compares the captured
rendering supplied by the caller; it does not independently authenticate an author,
a channel or Slack's raw stored message representation.

### Limited presentation normalization

`slack_bare_urls_entities` transforms only the observed body, leaving expected
text untouched. It first removes an HTTP(S) link wrapper when the label is absent,
equals the complete target, or equals that target with only its leading
`http://` or `https://` removed. The exact target is retained. Arbitrary or
truncated labels, other schemes, Markdown links, mentions and emoji are not
normalized. No URL decoding or whitespace normalization occurs.

It then decodes `&amp;`, `&lt;` and `&gt;` in one nonrecursive pass. Links are
recognized before that pass, so escaped angle brackets cannot introduce a new
link match. Slack documents the link and three-entity representations in its
[message formatting guide](https://docs.slack.dev/messaging/formatting-message-text/).
This limited presentation result is distinct from literal equality; it is not a
general Markdown or visual-equivalence claim.

The retained native examples used during this continuation were an exact
parent-only claim and two replies whose bodies differed only by one bare-URL
wrapper with a scheme-less label. A new live claim reproduced that URL form.
These observations exercise real native framing and URL handling; they do not
establish every formatting or entity branch.

### Optional fragment-label normalization

`slack_bare_urls_entities_fragment_labels` includes the preceding URL/entity
transformations and additionally recognizes one observed native label form:
the complete scheme-less target through its first `#`, followed by exactly
`…` (U+2026). The target must contain a nonempty fragment. The label retains
the full host, path and query; only its fragment display is elided. The complete
HTTP(S) target, including that fragment, remains the comparison value.

```javascript
const comparison = compareSlackPublication(result, preparedMessage, {
  normalization: 'slack_bare_urls_entities_fragment_labels',
});
```

This mode adds `normalizations_applied.fragment_labels`, counting the eligible
fragment labels among `bare_url_wrappers`. Existing modes and their result
shape are unchanged. A different target still mismatches the expected URL.
Arbitrary labels, shortened hosts/paths/queries, empty fragments, ASCII `...`,
and other ellipsis forms are not added to the accepted label forms. Request
identity, framing, payload ambiguity, whitespace, single-pass entity handling
and no-resend behavior retain the preceding contract.

The concrete native observation was the Drayage issue-comment handoff on
2026-10-04, Slack reply `1791081085.531469`: the reader retained the exact
GitHub comment URL but rendered its label with `#…`. The old modes keep their
literal/mismatch outcomes for that rendering. Enabling this new mode reports
a presentation match with one URL wrapper and one fragment label. This is a
comparison of the captured rendering, not a claim about Slack's raw storage
or a general rule for every truncated display label.

### Optional www-and-final-slash label normalization

`slack_bare_urls_entities_www_slash_labels` includes the base URL/entity
transformations and additionally recognizes one observed native display label.
After removing only the HTTP(S) scheme, the target must start with literal
`www.`, end with `/`, and contain neither `?` nor `#`. The label must equal
that complete scheme-less target after removing exactly the initial `www.`
and one terminal slash. The comparison substitutes the unchanged full target,
including its scheme, `www.` and final slash.

```javascript
const comparison = compareSlackPublication(result, preparedMessage, {
  normalization: 'slack_bare_urls_entities_www_slash_labels',
});
```

This mode adds `normalizations_applied.www_slash_labels`, counting those labels
among `bare_url_wrappers`. A presentation match still requires the complete
remaining body to equal the separately prepared text, with `literal_match: false`.
Existing modes and their result shapes remain unchanged; this option does not
enable fragment-label elision. Arbitrary or ellipsized labels, shortened paths,
and this label transformation on targets containing a query or fragment are
not accepted. There is no URL decoding, general label stripping, whitespace
normalization, new provider call or claim about Slack's raw stored text.

The motivating retained native sales reply on 2026-10-04 contains three
Upwork link wrappers with this exact display form. The earlier base mode
reports a mismatch for those labels. Apply the new comparison to the retained
captured response and separately prepared text; publication and readback do not
need to be repeated.

### Optional independent www-prefix and final-slash omission

`slack_bare_urls_entities_www_or_slash_labels` is a separate opt-in mode.
It includes the base URL/entity transformations and accepts three exact display
forms of an HTTP(S) target after removing its scheme:

- Remove the initial literal `www.` and preserve every remaining character.
- Remove exactly one terminal `/` and preserve every preceding character.
- Remove both that initial `www.` and that one terminal slash.

The target must have the respective prefix or suffix and contain neither
`?` nor `#`. Recognition uses literal string comparison: no URL decoding,
case folding, internal-slash changes, path shortening, ellipsis, arbitrary
label stripping or whitespace normalization. The wrapper is replaced by its
unchanged full target, including the original scheme, prefix and slash.
A different target or any other difference in the remaining body still
mismatches the separately prepared text.

```javascript
const comparison = compareSlackPublication(nextPublishedResult, nextPreparedMessage, {
  normalization: 'slack_bare_urls_entities_www_or_slash_labels',
});
```

Only this mode adds `normalizations_applied.www_prefix_omissions` and
`normalizations_applied.terminal_slash_omissions`. A wrapper omitting both
increments each omission counter once and `bare_url_wrappers` once.
An exact literal match leaves the counters zero. A normalized whole-body
match reports `presentation_match` with `literal_match: false`.

The default, base, fragment-label and existing
`slack_bare_urls_entities_www_slash_labels` modes retain their earlier behavior
and result shapes. In particular, the existing www-and-slash mode still
requires both omissions. This new mode does not enable fragment-label elision.
Selection, framing/ambiguity refusal and single-pass entity handling are
unchanged; the comparator performs no provider calls or mutation.

The motivating 2026-10-04 native publications contained these independent
forms: `https://prizeproblems.org/problems/170/` displayed without its scheme
and final slash, while `https://www.mit.edu/~asah/papers/2402.17995.pdf`
displayed without its scheme and initial `www.`. Their earlier helper
mismatches and completed manual dispositions remain preserved. The new mode
was source-inspected only at publication; those accepted bodies were not
retrieved or compared again, and no fixture or execution result is claimed.

### Optional immutable GitHub blob-label normalization

`slack_bare_urls_entities_github_blob_labels` is a separate opt-in mode for
one observed native display form. It includes the base URL/entity transformations
and additionally recognizes an HTTPS target on literal `github.com` with
`/<owner>/<repo>/blob/<commit>/<path>/<filename>`, where the commit is exactly
40 lowercase hexadecimal characters. The path may have zero or more directory
segments. Owner, repository, directory segments and filename must each be
nonempty and contain only ASCII letters, digits, underscore, dot or hyphen.
The label must equal `github.com/<owner>/<repo>/blob/…/<filename>` exactly,
with the same owner, repository and final filename and one U+2026 ellipsis.

```javascript
const comparison = compareSlackPublication(nextPublishedResult, nextPreparedMessage, {
  normalization: 'slack_bare_urls_entities_github_blob_labels',
});
```

Recognition replaces the wrapper with the unchanged complete target, including
the original commit and every omitted directory segment. A different target or
any difference in the remaining body still mismatches the separately prepared
message. This mode adds only `normalizations_applied.github_blob_labels` to
the base counters; each recognized blob label also counts once in
`bare_url_wrappers`. A literal match leaves all counters zero.

This mode does not accept shortened owner/repository/filename labels, ref
aliases, other hosts, HTTP blob targets, percent-encoded path segments,
query/fragment suffixes, ASCII `...`, other ellipsis positions or arbitrary
labels. It does not combine the fragment-label or www/slash omission modes.
There is no URL decoding, path resolution, case folding, general label stripping
or whitespace normalization. Existing modes retain their earlier behavior and
result shapes; selected-message binding, framing, ambiguity refusal and the
single entity pass are unchanged. No provider call, send/edit/read retry or
claim about raw Slack storage is introduced.

The actual motivating observation is the 2026-10-05 Commons #31608 claim
publication, activity `1791205149.358139`. Its native rendering retained this
complete target:

```text
https://github.com/ThatOpen/web-ifc-viewer/blob/1f5c975ad6d019e7355c8759369f318f9fa3e339/viewer/src/components/ifc/ifc-manager.ts
```

The displayed label was
`github.com/ThatOpen/web-ifc-viewer/blob/…/ifc-manager.ts`.
The original helper mismatch and the caller's completed exact retained-byte
disposition remain preserved. This new mode was source-inspected only at
publication: that accepted message was not fetched or compared again, no
copied fixture was created, and no executable acceptance is claimed. First
use is reserved for a future necessary comparison. The separate Desktop #31610
release used an ordinary complete scheme-less label already supported by the
base mode; it does not supply evidence for this new label form.

## Compare one exact fenced payload

`compareSlackFencedPayload(result, expectedPayload)` selects the same bounded
native message as the whole-message comparator, then compares the raw characters
inside one triple-backtick delimiter pair. Supply the prepared payload separately.
This is useful when an original PR-body handoff has an intact fenced payload but
Slack's rendered envelope differs from the authored whole message.

```javascript
const {compareSlackPublication, compareSlackFencedPayload} = moduleBox.exports;
const wholeMessage = compareSlackPublication(result, preparedMessage, {
  normalization: 'slack_bare_urls_entities',
});
const payload = compareSlackFencedPayload(result, separatelyPreparedBody);
text({wholeMessage, payload});
```

The two results describe different spans. A payload result never changes,
upgrades or replaces a whole-message `mismatch`. Prefixes, suffixes, links and
other text outside the fence are not compared by this export. Its metadata
states `evidence_scope: single_fenced_payload`, `normalization: none` and
`whole_message_comparison: not_performed`; the latter refers only to this
function. Keep the existing whole-message result when that evidence is needed.

### Exact span and supported delimiters

The selector reuses the existing request identity, payload consistency, target
message and native framing checks. Within that selected message it requires
exactly two runs of exactly three backticks. The opening run must begin the
message or follow an LF; the closing run must end the message or precede an LF.
Multiple pairs, nested backtick fences, longer backtick runs, tilde-fence lines
and unsupported delimiter placement return `uncomparable`. Inline single or
double backticks remain ordinary payload characters. This is a deliberately
bounded delimiter format, not a general Markdown parser.

Every character between the two delimiter runs participates in literal equality,
including any leading or trailing LF, spaces, language-label text, entities and
URL markup. The function does not trim, remove a fence-adjacent newline, strip
a language label, decode entities, rewrite links or interpret Markdown.
Consequently, a rendering that retains boundary LFs differs from a separately
prepared body that lacks those LFs. Do not trim either input to turn that result
into a match. The native rendering can also elide the authored boundary LFs;
in that case the retained raw interior is compared exactly as returned.

| Status | Meaning |
| --- | --- |
| `exact` | The raw interior equals the separately supplied payload literally. |
| `mismatch` | One supported fence pair was selected, but its interior differs. |
| `uncomparable` | Capture, message selection or fence boundaries are unavailable or ambiguous. |

`matches` and `literal_match` are true for exact, false for mismatch and null
for uncomparable. The result includes the selected channel/message/parent IDs.
Once a supported pair is found, `fence.opening`, `fence.payload` and
`fence.closing` contain start/end offsets into the selected rendered message
body. Offsets and `expected_length`/`observed_length` use JavaScript UTF-16 code
units; ranges are half-open, with the end excluded. The metadata states this
origin, unit and range convention explicitly. No message or payload text is
returned. Invalid caller arguments raise TypeError.

This pure operation makes no provider call and mutates neither input. It does
not independently authenticate a message or author, establish raw Slack storage
identity, compare the outer envelope, or grant permission to update the upstream
PR body. An exact Slack payload leaves any separate GitHub publication or
maintainer-action boundary unchanged.

## Read a confirmed publication at its native reported parent

A send addressed to a reply can be routed by Slack to the canonical parent of
that reply's thread. The original `thread_ts` then differs from the parent
needed by the thread reader. The default publisher and `readSlackPublication`
continue to use their existing explicit-parent contract. They do not silently
adopt a URL, repeat a send/edit, or retry a read at another parent.

For a new, necessary read, the additive export
`readSlackPublicationAtNativeParent(tools, published, retainedSendResponse, options)`
selects the parent reported by the original native send acknowledgement.
It requires confirmed-edit publication metadata and that send's original
retained response. Keep the original requested configuration, previous
observations and comparisons separately; this function does not replace them.

~~~javascript
const routed = await moduleBox.exports.readSlackPublicationAtNativeParent(
  tools,
  savedConfirmedPublication,
  retainedNativeSendResponse,
  {
    onProgress: value => store('operation-routed-read', value),
  }
);
store('operation-routed-response', routed.observation.readback_response);
const comparison = moduleBox.exports.compareSlackPublication(
  routed.observation,
  separatelyPreparedMessage,
  {normalization: 'slack_bare_urls_entities'}
);
text({routing: routed.routing, comparison});
~~~

The return shape is `{schema, routing, observation}`, with schema
`commons.connected_slack_native_parent_readback/v1`.
`observation` is a fresh ordinary read result whose `thread_ts` and
`readback_thread_ts` both name the selected native parent. Pass this nested
observation to the existing whole-message or fenced-payload comparator.
The original publication object and native acknowledgement remain unchanged.

### Bind the route to the confirmed message

The native acknowledgement must identify the same channel, message timestamp
and complete `message_link` as the supplied publication metadata. A missing
retained link, conflicting acknowledgement, native error or identity mismatch
refuses before any read. This export accepts the exact native payload containing
`message_link` and `message_context`, or its MCP `structuredContent` and/or
JSON text-block representations. Multiple representations must agree on all
three identity values. Unknown payload/context fields, non-text blocks and
unreadable JSON are refused rather than selecting a convenient representation.

Only a narrow literal permalink shape is supported:

- HTTPS, one ASCII workspace label followed by `.slack.com`, with no userinfo
  or port.
- `/archives/<confirmed-channel>/p<confirmed-message-digits>`, where the path's
  digits exactly equal the acknowledged timestamp with its decimal point removed.
- Exactly one `thread_ts` and one `cid` query parameter, in either order.
  The channel query must match both the path and native acknowledgement.
- Native message and parent timestamps have six fractional digits, with the
  reported parent no later than the message.

There is no percent-decoding, URL normalization, fragment handling, shortened
link resolution or general URL trust. Encoded, duplicate, unknown or ambiguous
query fields are refused. Fixed bounds are eight text blocks of at most 4,096
UTF-16 code units each, a 2,048-code-unit link, an 80-code-unit channel ID and
at most sixteen digits before each timestamp's decimal point. These are limits
of this explicit route selector, not changes to the old publication API.

`routing` retains the native link, acknowledgement representation paths,
confirmed channel/message, original `requested_thread_ts`, previous
`prior_readback_thread_ts`, and selected `native_parent_thread_ts`.
An absent original/prior parent is represented as null. The source is
`caller_retained_native_send_acknowledgement`; authority is only
`reported_routing_metadata` and authentication is `not_performed`.
The helper binds supplied evidence consistently; it does not independently
authenticate Slack, a workspace, an author or permission to act.

### One read, with original observations preserved

Options are `bindings`, `onProgress` and optional
`readback_thread_ts`. An explicitly supplied parent must equal the native
parent; a conflict refuses before a provider call. Calling this separately
named export is the explicit choice to make a new observation at the native
parent, even if the saved publication's earlier read used the requested parent.
That earlier choice remains in the routing metadata and original saved input.

The function delegates once to the existing reader, with the same selected
channel/message, `limit: 1` and exact reply timestamp window. Only the read
binding is needed. No send/edit binding, fallback, pagination or automatic
retry is added. Call counts inherit the original publication's counts and
increase the readback count for this one read.

Progress callbacks receive copied, body-free `{routing, observation}`
metadata. Pre-read input/routing errors throw without a provider call.
A delegated read failure retains the existing `SlackPublishError.progress`,
`cause` and native `response`, and adds copied `error.routing`.
A readable response can still omit the selected message or have unsupported
framing; `captured` never promises a match. The unchanged comparator keeps
all request, message selection, framing, ambiguity and full-body checks.

### Actual motivation and execution boundary

A completed native publication on 2026-10-05 used requested reply timestamp
`1791169091.858809`, while its send acknowledgement's permalink reported
canonical parent `1790851459.659859` for message `1791181593.279659` in
`C0BU51F1PL3`. The original requested-parent read did not contain the selected
message. A separately authorized bounded read at the reported parent located
it, and the caller retained both observations and its exact comparison.
No write was repeated.

That already-completed publication motivated this API; its body and comparison
were not replayed to exercise the new code. At this publication, the new route
selector and wrapper were source-inspected only. Their first useful invocation
is reserved for future real readback work. No generated inputs, fixtures,
tests, native process or current-message re-send/edit is part of this delivery.
All pre-existing publisher, reader and comparator function bytes are unchanged.
