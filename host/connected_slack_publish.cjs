'use strict';

// Native Slack bindings only. No transport, credentials, automatic retry or text rewrite.
class SlackPublishError extends Error {
  constructor(message, progress, cause) {
    super(message);
    this.name = 'SlackPublishError';
    this.progress = progress;
    this.cause = cause;
  }
}

function object(value, label) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new TypeError(label + ' must be an object');
  }
  return value;
}

function text(value, label) {
  if (typeof value !== 'string' || !value.trim()) throw new TypeError(label + ' is required');
  return value;
}

function timestamp(value, label) {
  if (typeof value !== 'string' || !/^\d+\.\d+$/.test(value)) {
    throw new TypeError(label + ' must be the observed Slack timestamp string');
  }
  return value;
}

function unpack(result, action) {
  object(result, action + ' response');
  if (result.isError === true) throw new Error(action + ' returned a native tool error');
  if (result.structuredContent && typeof result.structuredContent === 'object'
      && !Array.isArray(result.structuredContent)) return result.structuredContent;
  for (const block of result.content ?? []) {
    if (block?.type !== 'text' || typeof block.text !== 'string') continue;
    try { return object(JSON.parse(block.text), action + ' payload'); }
    catch (_) { /* Try the next native text block. */ }
  }
  throw new Error(action + ' did not return a readable native acknowledgement');
}

/** Send and restore the caller's exact text, or edit one already-confirmed message. */
async function publishSlackMessage(tools, request, options = {}) {
  const progress = {status: 'incomplete', stage: 'validate', message_state: 'not_attempted',
    calls: {}, readback_status: 'not_performed', progress_callback_errors: 0};
  let lastResponse;
  let announce = async () => {};
  try {
    object(request, 'request');
    const allowed = new Set(['channel_id', 'message', 'message_id', 'thread_ts',
      'reply_broadcast', 'unfurl_app_links']);
    for (const key of Object.keys(request)) {
      if (!allowed.has(key)) throw new TypeError('Unsupported request field: ' + key);
    }
    const channel = text(request.channel_id, 'channel_id');
    const message = text(request.message, 'message');
    const editing = request.message_id !== undefined;
    const messageId = editing ? timestamp(request.message_id, 'message_id') : undefined;
    const thread = request.thread_ts === undefined ? undefined : timestamp(request.thread_ts, 'thread_ts');
    if (editing && thread !== undefined) throw new TypeError('thread_ts applies only to a new send');
    const sendOptions = {};
    for (const key of ['reply_broadcast', 'unfurl_app_links']) {
      if (request[key] === undefined) continue;
      if (typeof request[key] !== 'boolean') throw new TypeError(key + ' must be boolean');
      if (editing) throw new TypeError(key + ' applies only to a new send');
      sendOptions[key] = request[key];
    }
    const bindings = {
      send: options.bindings?.send ?? 'mcp__codex_apps__slack_slack_send_message',
      edit: options.bindings?.edit ?? 'mcp__codex_apps__slack_slack_edit_message',
    };
    for (const action of editing ? ['edit'] : ['send', 'edit']) {
      if (typeof tools?.[bindings[action]] !== 'function') {
        throw new Error('Binding not present: ' + bindings[action]
          + '. Repeat discovery alongside useful work.');
      }
    }
    const observer = options.onProgress;
    if (observer !== undefined && typeof observer !== 'function') throw new TypeError('onProgress must be a function');
    announce = async () => {
      if (!observer) return;
      try { await observer(JSON.parse(JSON.stringify(progress))); }
      catch (_) { progress.progress_callback_errors += 1; }
    };
    const call = async (action, args) => {
      progress.calls[action] = (progress.calls[action] ?? 0) + 1;
      lastResponse = undefined;
      lastResponse = await tools[bindings[action]](args);
      return unpack(lastResponse, action);
    };
    progress.channel_id = channel;
    if (thread !== undefined) progress.thread_ts = thread;
    if (editing) {
      progress.message_id = messageId;
      progress.message_state = 'existing_message_selected';
    } else {
      progress.stage = 'send';
      progress.message_state = 'send_outcome_unknown';
      await announce();
      const sent = await call('send', {channel_id: channel, message,
        ...(thread === undefined ? {} : {thread_ts: thread}), ...sendOptions});
      const context = object(sent.message_context, 'send message_context');
      progress.channel_id = text(context.channel_id, 'returned channel_id');
      progress.message_id = timestamp(context.message_ts, 'returned message_ts');
      if (typeof sent.message_link === 'string') progress.message_link = sent.message_link;
      progress.message_state = 'sent';
      await announce();
    }
    progress.stage = 'edit';
    progress.message_state = 'edit_outcome_unknown';
    await announce();
    const edited = await call('edit', {channel_id: progress.channel_id,
      message_id: progress.message_id, message: {markdown_text: message}});
    if (edited.message_id !== progress.message_id) {
      throw new Error('Edit acknowledgement did not identify the selected message');
    }
    progress.message_state = 'edit_confirmed';
    progress.status = 'updated';
    progress.stage = 'complete';
    await announce();
    return progress;
  } catch (error) {
    await announce();
    const failure = new SlackPublishError(String(error?.message ?? error), progress, error);
    failure.response = lastResponse;
    throw failure;
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {SlackPublishError, publishSlackMessage};
}
