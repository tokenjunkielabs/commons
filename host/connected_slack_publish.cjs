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


function readbackBinding(tools, options) {
  const name = options.bindings?.readback ?? 'mcp__codex_apps__slack_slack_read_thread';
  if (typeof tools?.[name] !== 'function') {
    throw new Error('Binding not present: ' + name
      + '. Repeat discovery alongside useful work.');
  }
  return name;
}

function readbackArguments(progress, options) {
  const channel = text(progress.channel_id, 'confirmed channel_id');
  const target = timestamp(progress.message_id, 'confirmed message_id');
  const parent = timestamp(options.readback_thread_ts ?? progress.readback_thread_ts
    ?? progress.thread_ts ?? target, 'readback thread timestamp');
  const args = {channel_id: channel, message_ts: parent, limit: 1};
  if (parent !== target) {
    // Read only the selected reply's timestamp window, not the surrounding feed.
    const [seconds, fractional] = target.split('.');
    const precision = Math.max(6, fractional.length);
    const ticks = BigInt(seconds + fractional.padEnd(precision, '0'));
    const format = value => {
      const digits = String(value).padStart(precision + 1, '0');
      return digits.slice(0, -precision) + '.' + digits.slice(-precision);
    };
    args.oldest = format(ticks > 0n ? ticks - 1n : 0n);
    args.latest = format(ticks + 1n);
  }
  return args;
}

/** Capture one native read for a confirmed edit; never repeat its send or edit. */
async function readSlackPublication(tools, published, options = {}) {
  const progress = {status: 'incomplete', stage: 'validate_readback',
    message_state: 'not_selected', calls: {}, readback_status: 'not_performed',
    progress_callback_errors: 0};
  let lastResponse;
  let announce = async () => {};
  try {
    object(published, 'published progress');
    // Provider bodies stay outside observer metadata, including on continuation.
    for (const key of ['status', 'stage', 'message_state', 'readback_status',
      'progress_callback_errors', 'channel_id', 'message_id', 'message_link',
      'thread_ts', 'readback_thread_ts', 'readback_request']) {
      if (published[key] !== undefined) progress[key] = published[key];
    }
    progress.calls = {...object(published.calls ?? {}, 'published call counts')};
    progress.stage = 'validate_readback';
    progress.readback_status = 'not_performed';
    if (progress.message_state !== 'edit_confirmed') {
      throw new TypeError('Readback continuation requires a confirmed edit');
    }
    const observer = options.onProgress;
    if (observer !== undefined && typeof observer !== 'function') {
      throw new TypeError('onProgress must be a function');
    }
    announce = async () => {
      if (!observer) return;
      try { await observer(JSON.parse(JSON.stringify(progress))); }
      catch (_) { progress.progress_callback_errors += 1; }
    };
    const binding = readbackBinding(tools, options);
    const args = readbackArguments(progress, options);
    progress.readback_request = args;
    progress.readback_thread_ts = args.message_ts;
    progress.stage = 'readback';
    progress.readback_status = 'pending';
    await announce();
    progress.calls.readback = (progress.calls.readback ?? 0) + 1;
    lastResponse = await tools[binding](args);
    unpack(lastResponse, 'readback');
    progress.readback_status = 'captured';
    progress.stage = 'complete';
    await announce();
    return {...progress, readback_response: lastResponse};
  } catch (error) {
    if (progress.readback_status === 'pending') progress.readback_status = 'failed';
    await announce();
    const failure = new SlackPublishError(String(error?.message ?? error), progress, error);
    failure.response = lastResponse;
    throw failure;
  }
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
    if (options.readback !== undefined && typeof options.readback !== 'boolean') {
      throw new TypeError('readback must be boolean');
    }
    if (options.readback_thread_ts !== undefined) {
      timestamp(options.readback_thread_ts, 'readback_thread_ts');
      if (thread !== undefined && options.readback_thread_ts !== thread) {
        throw new TypeError('readback_thread_ts differs from the new message thread');
      }
    }
    if (options.readback === true) readbackBinding(tools, options);
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
    if (options.readback === true) return await readSlackPublication(tools, progress, options);
    progress.stage = 'complete';
    await announce();
    return progress;
  } catch (error) {
    if (error instanceof SlackPublishError) throw error;
    await announce();
    const failure = new SlackPublishError(String(error?.message ?? error), progress, error);
    failure.response = lastResponse;
    throw failure;
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {SlackPublishError, publishSlackMessage, readSlackPublication};
}
