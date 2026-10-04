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

/**
 * Project a detailed read_channel/read_thread envelope without changing it.
 * Content and ranges refer to the connector rendering, not Slack stored text.
 */
function projectSlackMessages(response, request, options = {}) {
  object(request, 'projection request');
  object(options, 'projection options');
  const operation = request.operation;
  if (!['read_channel', 'read_thread'].includes(operation)) {
    throw new TypeError('projection operation must be read_channel or read_thread');
  }
  const args = object(request.args, 'projection request.args');
  const channel = nonempty(args.channel_id, 'projection channel_id');
  const stamp = /^[0-9]{1,16}\.[0-9]{1,16}$/;
  if (!/^[CGD][A-Z0-9]{1,127}$/.test(channel)) throw new TypeError('invalid projection channel_id');
  if (args.response_format !== undefined && args.response_format !== 'detailed') {
    throw new TypeError('projection does not accept a concise request');
  }
  if (operation === 'read_thread' && (typeof args.message_ts !== 'string' || !stamp.test(args.message_ts))) {
    throw new TypeError('projection requires an exact decimal-string parent message_ts');
  }
  const defaults = {start_index: 0, max_messages: 8, max_body_chars: 800,
    max_total_body_chars: 6400, max_input_chars: 1048576};
  const ceilings = {start_index: Number.MAX_SAFE_INTEGER, max_messages: 1000,
    max_body_chars: 65536, max_total_body_chars: 262144, max_input_chars: 8388608};
  for (const key of Object.keys(options)) {
    if (!Object.prototype.hasOwnProperty.call(defaults, key)) throw new TypeError('unknown projection option: ' + key);
  }
  const limits = {...defaults, ...options};
  for (const [key, value] of Object.entries(limits)) {
    if (!Number.isSafeInteger(value) || value < (['max_messages', 'max_input_chars'].includes(key) ? 1 : 0) ||
        value > ceilings[key]) throw new TypeError('invalid projection option: ' + key);
  }
  const result = {schema: 'commons.connected_slack_message_projection/v1', status: 'REFUSED',
    source: {operation, channel_id: channel,
      parent_message_ts: operation === 'read_thread' ? args.message_ts : null,
      content_basis: 'connector_rendered_content', message_identity: 'rendered_header',
      channel_binding: 'retained_request', representations: 0, input_chars: 0},
    limits, coverage: {scope: 'retained_response_only', snapshot: false}, messages: [], issue: null};
  const refuse = (code, detail) => {
    result.issue = {code, detail}; return result;
  };
  const bad = (code, detail) => { throw {projection: true, code, detail}; };
  let charged = 0;
  const charge = value => {
    charged += value.length;
    result.source.input_chars = charged;
    if (charged > limits.max_input_chars) bad('INPUT_LIMIT', 'Native payload text exceeds max_input_chars.');
  };
  try {
    if (!response || typeof response !== 'object' || Array.isArray(response) || response.isError === true) {
      bad('NATIVE_ERROR', 'Expected a successful retained native response.');
    }
    const representations = [];
    const accept = value => {
      if (!value || typeof value !== 'object' || Array.isArray(value) ||
          Object.keys(value).length !== 2 || typeof value.messages !== 'string' ||
          typeof value.pagination_info !== 'string') {
        bad('UNSUPPORTED_PAYLOAD', 'Expected only string messages and pagination_info fields.');
      }
      representations.push(value);
    };
    if (Object.prototype.hasOwnProperty.call(response, 'messages')) {
      if (typeof response.messages === 'string') charge(response.messages);
      if (typeof response.pagination_info === 'string') charge(response.pagination_info);
      accept(response);
    } else {
      if (Object.prototype.hasOwnProperty.call(response, 'structuredContent')) {
        const value = response.structuredContent;
        if (typeof value?.messages === 'string') charge(value.messages);
        if (typeof value?.pagination_info === 'string') charge(value.pagination_info);
        accept(value);
      }
      if (Object.prototype.hasOwnProperty.call(response, 'content')) {
        if (!Array.isArray(response.content) || response.content.length === 0) {
          bad('UNSUPPORTED_PAYLOAD', 'Native content must contain JSON text blocks.');
        }
        for (const block of response.content) {
          if (!block || block.type !== 'text' || typeof block.text !== 'string') {
            bad('UNSUPPORTED_PAYLOAD', 'Non-text native content is outside this projection format.');
          }
          charge(block.text);
          let value;
          try { value = JSON.parse(block.text); } catch (_) {
            bad('UNREADABLE_PAYLOAD', 'Native text is not a JSON envelope.');
          }
          accept(value);
        }
      }
    }
    if (!representations.length) bad('UNSUPPORTED_PAYLOAD', 'No rendered messages envelope was retained.');
    result.source.representations = representations.length;
    const page = representations[0];
    if (representations.some(value => value.messages !== page.messages || value.pagination_info !== page.pagination_info)) {
      bad('CONFLICTING_REPRESENTATIONS', 'Retained native representations disagree.');
    }
    const rendered = page.messages;
    result.source.rendered_chars = rendered.length;
    const nativePage = pagination(page);
    result.coverage.native_pagination_recognized = nativePage.known;
    result.coverage.provider_end_observed = nativePage.end;
    result.coverage.next_cursor_available = Boolean(nativePage.next_cursor);
    const rows = [];
    const ids = new Set();
    const add = (header, bodyStart, bodyEnd, id, kind) => {
      if (!stamp.test(id)) bad('UNSUPPORTED_LAYOUT', 'A message timestamp is outside the exact decimal format.');
      if (ids.has(id)) bad('DUPLICATE_IDENTITY', 'The rendered page repeats a message timestamp.');
      if (bodyEnd < bodyStart) bad('UNSUPPORTED_LAYOUT', 'Message framing overlaps.');
      ids.add(id);
      rows.push({source_index: rows.length, channel_id: channel, message_ts: id, kind,
        parent_message_ts: operation === 'read_thread' ? args.message_ts : null,
        header_range: [header.index, bodyStart], rendered_content_range: [bodyStart, bodyEnd]});
    };
    const boundary = (end, suffix) => {
      if (rendered.slice(end - suffix.length, end) !== suffix) {
        bad('UNSUPPORTED_LAYOUT', 'Expected a detailed-message separator.');
      }
      return end - suffix.length;
    };
    if (rendered === '') {
      result.coverage.declared_replies = null;
    } else if (operation === 'read_channel') {
      const prefix = /^Channel: [^\n]+ \(([CGD][A-Z0-9]+)\)\n\n/.exec(rendered);
      if (!prefix || prefix[1] !== channel) bad('CHANNEL_MISMATCH', 'Rendered channel header does not match the retained request.');
      result.source.channel_binding = 'retained_request_and_rendered_header';
      const pattern = /^=== Message from [^\n]+ at [^\n]+ ===[ \t]*\nMessage TS: ([0-9]+\.[0-9]+)\n/gm;
      const headers = Array.from(rendered.matchAll(pattern));
      const markerCount = (rendered.match(/^=== Message from /gm) || []).length;
      if ((headers.length === 0 && rendered !== prefix[0]) ||
          (headers.length > 0 && headers[0].index !== prefix[0].length) ||
          markerCount !== headers.length) {
        bad('UNSUPPORTED_LAYOUT', 'Channel message headers are incomplete or ambiguous.');
      }
      for (let i = 0; i < headers.length; i++) {
        const header = headers[i];
        const end = i + 1 < headers.length ? boundary(headers[i + 1].index, '\n\n') : rendered.length;
        add(header, header.index + header[0].length, end, header[1], 'channel_message');
      }
      result.coverage.declared_replies = null;
    } else {
      const parent = /^=== THREAD PARENT MESSAGE ===\nFrom: [^\n]+\nTime: [^\n]+\nMessage TS: ([0-9]+\.[0-9]+)\n/.exec(rendered);
      if (!parent || parent[1] !== args.message_ts) {
        bad('PARENT_MISMATCH', 'Detailed thread parent does not match the retained request.');
      }
      const separators = Array.from(rendered.matchAll(/\n\n=== THREAD REPLIES \(([0-9]+) total\) ===\n\n/g));
      if (separators.length > 1) bad('AMBIGUOUS_LAYOUT', 'The rendering repeats the thread-replies separator.');
      if (!separators.length) {
        const end = boundary(rendered.length, '\n\nNo thread messsages\n');
        add(parent, parent[0].length, end, parent[1], 'thread_parent');
        result.coverage.declared_replies = 0;
      } else {
        const separator = separators[0];
        const count = Number(separator[1]);
        if (!Number.isSafeInteger(count) || count < 1) bad('UNSUPPORTED_LAYOUT', 'Invalid declared reply count.');
        const pattern = /^--- Reply ([1-9][0-9]*) of ([1-9][0-9]*) ---\nFrom: [^\n]+\nTime: [^\n]+\nMessage TS: ([0-9]+\.[0-9]+)\n/gm;
        const headers = Array.from(rendered.matchAll(pattern));
        const markers = (rendered.match(/^--- Reply /gm) || []).length;
        result.coverage.declared_replies = count;
        result.coverage.observed_reply_headers = headers.length;
        if (headers.length !== count || markers !== count ||
            headers[0]?.index !== separator.index + separator[0].length) {
          bad('REPLY_COUNT_MISMATCH', 'Declared replies and complete rendered reply headers differ.');
        }
        add(parent, parent[0].length, separator.index, parent[1], 'thread_parent');
        for (let i = 0; i < headers.length; i++) {
          const header = headers[i];
          if (Number(header[1]) !== i + 1 || Number(header[2]) !== count) {
            bad('REPLY_SEQUENCE_MISMATCH', 'Rendered reply numbering is inconsistent.');
          }
          const end = i + 1 < headers.length ? boundary(headers[i + 1].index, '\n\n') : boundary(rendered.length, '\n');
          add(header, header.index + header[0].length, end, header[3], 'thread_reply');
        }
      }
    }
    // Marker-like body lines cannot be distinguished from connector framing.
    for (const row of rows) {
      const body = rendered.slice(...row.rendered_content_range);
      if (/^(?:=== THREAD (?:PARENT MESSAGE|REPLIES)|--- Reply |=== Message from |Message TS:)/m.test(body)) {
        bad('AMBIGUOUS_LAYOUT', 'Rendered content contains reserved message-framing lines.');
      }
    }
    const from = Math.min(limits.start_index, rows.length);
    const until = Math.min(rows.length, from + limits.max_messages);
    let used = 0;
    let full = 0;
    let truncated = 0;
    for (const row of rows.slice(from, until)) {
      const [start, end] = row.rendered_content_range;
      let length = Math.min(end - start, limits.max_body_chars, limits.max_total_body_chars - used);
      if (length > 0 && length < end - start &&
          rendered.charCodeAt(start + length - 1) >= 0xd800 && rendered.charCodeAt(start + length - 1) <= 0xdbff &&
          rendered.charCodeAt(start + length) >= 0xdc00 && rendered.charCodeAt(start + length) <= 0xdfff) length--;
      const clipped = length < end - start;
      result.messages.push({...row, rendered_content: rendered.slice(start, start + length),
        content_chars: end - start, returned_chars: length, truncated: clipped});
      full += end - start; used += length; truncated += clipped ? 1 : 0;
    }
    Object.assign(result.coverage, {parsed_messages: rows.length, start_index: from,
      returned_messages: result.messages.length, omitted_before: from, omitted_after: rows.length - until,
      next_index: until < rows.length ? until : null, selected_content_chars: full,
      returned_content_chars: used, truncated_messages: truncated,
      all_rendered_messages_included: from === 0 && until === rows.length && truncated === 0});
    result.status = rows.length ? 'PROJECTED' : 'EMPTY_RENDERING';
    return result;
  } catch (error) {
    if (!error?.projection) throw error;
    result.messages = [];
    return refuse(error.code, error.detail);
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {collectSlackPages, projectSlackMessages};
}
