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
`readback_status: not_performed` remains explicit: the helper does not fetch
the rendered body or claim an independent content readback. Use the existing
Slack readers when the task requires that check.

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
| `edit_confirmed` | The edit was acknowledged. Perform any required body readback separately. |

The optional observer receives copied metadata before each write, after the
send acknowledgement and after completion or failure. Observer errors are
counted and do not block publication. Keep the stable operation ID in the
ordinary message and retain progress through the existing host. There is no
new journal, receipt file, dispatcher or approval step.
