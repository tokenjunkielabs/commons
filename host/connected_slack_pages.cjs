'use strict';

// Native reads only. Responses remain private caller-owned data.
const OPERATIONS = {
  read_channel: {
    binding: 'mcp__codex_apps__slack_slack_read_channel',
    fields: ['channel_id', 'cursor', 'latest', 'limit', 'oldest', 'response_format'],
    maximumLimit: 100,
  },
  read_thread: {
    binding: 'mcp__codex_apps__slack_slack_read_thread',
    fields: ['channel_id', 'cursor', 'latest', 'limit', 'message_ts', 'oldest', 'response_format'],
    maximumLimit: 1000,
  },
  search: {
    binding: 'mcp__codex_apps__slack_slack_search_public_and_private',
    fields: ['after', 'before', 'channel_types', 'content_types', 'context_channel_id',
      'cursor', 'filters', 'include_bots', 'include_context', 'keywords', 'limit',
      'max_context_length', 'natural_language_query', 'only_my_channels', 'query',
      'response_format', 'sort', 'sort_dir'],
    maximumLimit: 20,
  },
};

function object(value, label) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new TypeError(label + ' must be an object');
  }
  return value;
}

function positive(value, label, maximum = Number.MAX_SAFE_INTEGER) {
  if (!Number.isSafeInteger(value) || value < 1 || value > maximum) {
    throw new TypeError(label + ' must be a positive integer no greater than ' + maximum);
  }
  return value;
}

function nonempty(value, label) {
  if (typeof value !== 'string' || !value.trim()) {
    throw new TypeError(label + ' must be a nonempty string');
  }
  return value;
}

function copy(value) {
  return JSON.parse(JSON.stringify(value));
}

function diagnostic(error) {
  return {name: String(error?.name ?? 'Error'),
    message: String(error?.message ?? error).slice(0, 1200)};
}

function payload(response) {
  if (response.structuredContent && typeof response.structuredContent === 'object'
      && !Array.isArray(response.structuredContent)
      && 'pagination_info' in response.structuredContent) return response.structuredContent;
  for (const block of response.content ?? []) {
    if (block?.type !== 'text' || typeof block.text !== 'string') continue;
    try {
      const value = JSON.parse(block.text);
      if (value && typeof value === 'object' && !Array.isArray(value)) return value;
    } catch (_) { /* Keep the original response; try another native text block. */ }
  }
  if (response.structuredContent && typeof response.structuredContent === 'object'
      && !Array.isArray(response.structuredContent)) return response.structuredContent;
  throw new Error('Native response has no readable JSON payload');
}

function pagination(value) {
  const info = value.pagination_info;
  if (typeof info !== 'string') return {known: false, info: null, next_cursor: null, end: false};
  const normalized = info.trim().replace(/\\n/g, '').trim();
  const cursors = new Set(Array.from(info.matchAll(/\bcursor\s*:?\s*\x60([^\x60]+)\x60/gi),
    match => match[1]));
  // Exact observed provider endings; message text is never inspected for cursors.
  const end = /^(?:There are no more messages (?:in this thread|available)\.?|End of results - No more pages available\.?)$/i.test(normalized);
  if (cursors.size === 1 && !end) {
    return {known: true, info, next_cursor: Array.from(cursors)[0], end: false};
  }
  if (cursors.size === 0 && end) return {known: true, info, next_cursor: null, end: true};
  return {known: false, info, next_cursor: null, end: false};
}

function argumentsAt(base, cursor) {
  const args = {...base};
  if (cursor !== null) args.cursor = cursor;
  return args;
}

/**
 * Collect one bounded native cursor chain. This does not interpret messages,
 * prove source completeness, open thread replies from a channel, or decide ownership.
 */
async function collectSlackPages(tools, request, options = {}) {
  object(request, 'request');
  for (const key of Object.keys(request)) {
    if (!['operation', 'args', 'max_pages', 'timeout_ms'].includes(key)) {
      throw new TypeError('Unsupported request field: ' + key);
    }
  }
  const operation = request.operation;
  if (!Object.prototype.hasOwnProperty.call(OPERATIONS, operation)) {
    throw new TypeError('operation must be read_channel, read_thread or search');
  }
  const spec = OPERATIONS[operation];
  const suppliedArgs = object(request.args, 'args');
  for (const key of Object.keys(suppliedArgs)) {
    if (!spec.fields.includes(key)) throw new TypeError('Unsupported native argument: ' + key);
  }
  const args = copy(suppliedArgs);
  if (operation !== 'search') nonempty(args.channel_id, 'channel_id');
  if (operation === 'read_thread') {
    nonempty(args.message_ts, 'message_ts');
    if (!/^[0-9]+\.[0-9]+$/.test(args.message_ts)) {
      throw new TypeError('message_ts must retain the observed decimal Slack string');
    }
  }
  if (args.cursor === '') delete args.cursor;
  if (args.cursor !== undefined) nonempty(args.cursor, 'cursor');
  args.limit = positive(args.limit ?? 20, 'limit', spec.maximumLimit);
  if (args.response_format !== undefined && args.response_format !== 'detailed') {
    throw new TypeError('This collector retains detailed native responses');
  }
  args.response_format = 'detailed';
  const maxPages = positive(request.max_pages ?? 4, 'max_pages');
  const timeout = positive(request.timeout_ms ?? 30000, 'timeout_ms');
  if (typeof tools?.[spec.binding] !== 'function') {
    throw new Error('Binding not present: ' + spec.binding
      + '. Repeat discovery alongside useful work.');
  }
  if (options.onResponse !== undefined && typeof options.onResponse !== 'function') {
    throw new TypeError('onResponse must be a function');
  }
  const initialCursor = args.cursor ?? null;
  delete args.cursor;
  const start = Date.now();
  const result = {
    schema: 'commons.connected_slack_pages/v1',
    operation, binding: spec.binding,
    request: {operation, args: argumentsAt(args, initialCursor),
      max_pages: maxPages, timeout_ms: timeout},
    started_at: new Date(start).toISOString(),
    pages: [], responses: [], next_request: null,
    summary: {calls: 0, successful_pages: 0, retained_responses: 0,
      started_with_cursor: initialCursor !== null, provider_end_observed: false,
      next_cursor: initialCursor, stop_reason: null, snapshot: false,
      coverage: 'native_pagination_only'},
  };
  const seen = new Set();
  let cursor = initialCursor;
  let mayContinue = true;
  while (result.summary.calls < maxPages) {
    if (Date.now() - start >= timeout) {
      result.summary.stop_reason = 'TIME_BUDGET';
      break;
    }
    const requested = argumentsAt(args, cursor);
    const page = {call: result.summary.calls + 1, request_args: copy(requested),
      response_index: null, pagination_info: null, next_cursor: null,
      provider_end_observed: false};
    result.pages.push(page);
    result.summary.calls += 1;
    seen.add(cursor);
    let response;
    try {
      response = await tools[spec.binding](requested);
    } catch (error) {
      page.error = diagnostic(error);
      result.summary.stop_reason = 'NATIVE_EXCEPTION';
      break;
    }
    page.response_index = result.responses.length;
    result.responses.push(response);
    result.summary.retained_responses = result.responses.length;
    if (!response || typeof response !== 'object' || response.isError === true) {
      page.error = {name: 'NativeToolError', message: 'Native tool returned an error or non-object response'};
      result.summary.stop_reason = 'NATIVE_ERROR';
    } else {
      try {
        const decoded = payload(response);
        if (decoded.isError === true || decoded.ok === false) {
          const error = new Error('Native payload reports a failed read');
          error.name = 'NativeReadError';
          throw error;
        }
        const state = pagination(decoded);
        page.pagination_info = state.info;
        page.next_cursor = state.next_cursor;
        page.provider_end_observed = state.end;
        result.summary.successful_pages += 1;
        if (!state.known) {
          mayContinue = false;
          result.summary.next_cursor = null;
          result.summary.stop_reason = 'UNKNOWN_PAGINATION';
        } else if (state.end) {
          mayContinue = false;
          result.summary.provider_end_observed = true;
          result.summary.next_cursor = null;
          result.summary.stop_reason = 'PROVIDER_END';
        } else if (seen.has(state.next_cursor)) {
          mayContinue = false;
          result.summary.next_cursor = state.next_cursor;
          result.summary.stop_reason = 'CURSOR_REPEAT';
        } else {
          cursor = state.next_cursor;
          result.summary.next_cursor = cursor;
        }
      } catch (error) {
        page.error = diagnostic(error);
        if (error?.name === 'NativeReadError') {
          result.summary.stop_reason = 'NATIVE_ERROR';
        } else {
          mayContinue = false;
          result.summary.next_cursor = null;
          result.summary.stop_reason = 'UNREADABLE_RESPONSE';
        }
      }
    }
    if (options.onResponse) {
      try { await options.onResponse({page: copy(page), response: copy(response)}); }
      catch (error) {
        page.callback_error = diagnostic(error);
        result.summary.stop_reason = 'CALLBACK_ERROR';
      }
    }
    if (result.summary.stop_reason) break;
  }
  if (!result.summary.stop_reason) result.summary.stop_reason = 'PAGE_BUDGET';
  if (mayContinue) {
    result.next_request = {operation, args: argumentsAt(args, cursor),
      max_pages: maxPages, timeout_ms: timeout};
  }
  result.finished_at = new Date().toISOString();
  result.elapsed_ms = Date.now() - start;
  return result;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {collectSlackPages};
}
