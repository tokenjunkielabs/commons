# Native Slack text envelopes

Use `connected_slack_native_envelope.cjs` when a discovered Slack read returns
`{text: "{...}"}` rather than MCP `content` text blocks. It supplies a derived
text-block view for the existing [retained-page readers](CONNECTED_SLACK_PAGES.md).
It does not make another provider request or replace those readers.

## Read once, project the retained response

```javascript
const {asSlackTextBlocks} = require('./connected_slack_native_envelope.cjs');
const {projectSlackMessages} = require('./connected_slack_pages.cjs');

// request and nativeReadThread are the caller's retained request and
// already-discovered native binding, not a new provider or account route.
const original = await nativeReadThread(request.args);
const view = asSlackTextBlocks(original);
const projection = projectSlackMessages(view, request, {
  max_messages: 8,
  max_body_chars: 800,
});
// Retain {request, original} privately. Present the bounded projection, not
// duplicate full copies of both original and view.
```

The same adapter can precede `projectSlackSearchResults` for a native search
response with the same wrapper. It does not manufacture messages from search
snippets or repair an unsupported rendered layout.

For `collectSlackPages`, normalize at the return of the discovered native
binding and retain the original request/response pair separately. The
collector's `responses` then contain **derived views**, not original wire
envelopes. Keep original filters, cursor strings, and the existing
`next_request`; adaptation does not change or validate provider ordering.

## Preserved behavior and boundaries

The original object and `text` string remain unchanged. Existing `content`
blocks are retained first, and a matching text block is not added twice.
`structuredContent`, native failure flags, and other existing fields remain
available. Responses without top-level `text`, `Error` instances, responses with
`isError: true`, and non-object responses pass through unchanged.

Distinct representations stay visible to the existing projectors, which can
refuse disagreements and enforce their existing input/body limits. The adapter
itself does not decode JSON, inspect message instructions, infer completeness,
classify ownership, print private content, add a cooldown, or call a provider.
A non-string `text` or non-array existing `content` raises a `TypeError` without
including the private value in its diagnostic.

This does not fix provider cursor ordering, missing rendered results, or
unavailable native bindings. The established reader and its search-context
defaults remain unchanged. Both helper sources can also be loaded in an existing
code-mode session; this adapter has no package dependency.
