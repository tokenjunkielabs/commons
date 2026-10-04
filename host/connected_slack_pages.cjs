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
  search_public: {
    binding: 'mcp__codex_apps__slack_slack_search_public',
    fields: ['after', 'before', 'content_types', 'context_channel_id', 'cursor',
      'filters', 'include_bots', 'include_context', 'keywords', 'limit',
      'max_context_length', 'natural_language_query', 'only_my_channels', 'query',
      'response_format', 'sort', 'sort_dir'],
    maximumLimit: 20,
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
    throw new TypeError('operation must be read_channel, read_thread, search or search_public');
  }
  const spec = OPERATIONS[operation];
  const suppliedArgs = object(request.args, 'args');
  for (const key of Object.keys(suppliedArgs)) {
    if (!spec.fields.includes(key)) throw new TypeError('Unsupported native argument: ' + key);
  }
  const args = copy(suppliedArgs);
  if (!['search', 'search_public'].includes(operation)) {
    nonempty(args.channel_id, 'channel_id');
    for (const field of ['oldest', 'latest']) {
      if (args[field] !== undefined &&
          (typeof args[field] !== 'string' || !/^[0-9]+\.[0-9]+$/.test(args[field]))) {
        throw new TypeError(field + ' must be a decimal Slack timestamp string');
      }
    }
  }
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
    if (key !== 'source_indices' && !Object.prototype.hasOwnProperty.call(defaults, key)) {
      throw new TypeError('unknown projection option: ' + key);
    }
  }
  const limits = {...defaults, ...options};
  for (const [key, value] of Object.entries(limits)) {
    if (key === 'source_indices') continue;
    if (!Number.isSafeInteger(value) || value < (['max_messages', 'max_input_chars'].includes(key) ? 1 : 0) ||
        value > ceilings[key]) throw new TypeError('invalid projection option: ' + key);
  }
  let sourceIndices = null;
  if (Object.prototype.hasOwnProperty.call(options, 'source_indices')) {
    if (Object.prototype.hasOwnProperty.call(options, 'start_index')) {
      throw new TypeError('source_indices and start_index are mutually exclusive');
    }
    if (!Array.isArray(options.source_indices) || options.source_indices.length > limits.max_messages) {
      throw new TypeError('source_indices must be an array with at most max_messages entries');
    }
    sourceIndices = options.source_indices.slice();
    for (let i = 0; i < sourceIndices.length; i++) {
      if (!Number.isSafeInteger(sourceIndices[i]) || sourceIndices[i] < 0 ||
          (i > 0 && sourceIndices[i] <= sourceIndices[i - 1])) {
        throw new TypeError('source_indices must contain distinct increasing nonnegative safe integers');
      }
    }
    limits.source_indices = sourceIndices;
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
      const pattern = /^=== Message (?:from [^\n]+ )?at [^\n]+ ===[ \t]*\nMessage TS: ([0-9]+\.[0-9]+)\n/gm;
      const headers = Array.from(rendered.matchAll(pattern));
      const markerCount = (rendered.match(/^=== Message (?:from |at )/gm) || []).length;
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
    if (sourceIndices !== null) {
      result.coverage.parsed_messages = rows.length;
      if (sourceIndices.some(index => index >= rows.length)) {
        bad('SOURCE_INDEX_OUT_OF_RANGE', 'A requested source index is outside the parsed retained page.');
      }
    }
    const selected = sourceIndices === null ? rows.slice(from, until) : sourceIndices.map(index => rows[index]);
    let used = 0;
    let full = 0;
    let truncated = 0;
    for (const row of selected) {
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
    if (sourceIndices === null) {
      Object.assign(result.coverage, {parsed_messages: rows.length, start_index: from,
        returned_messages: result.messages.length, omitted_before: from, omitted_after: rows.length - until,
        next_index: until < rows.length ? until : null, selected_content_chars: full,
        returned_content_chars: used, truncated_messages: truncated,
        all_rendered_messages_included: from === 0 && until === rows.length && truncated === 0});
    } else {
      const omittedRanges = [];
      let cursor = 0;
      for (const index of sourceIndices) {
        if (cursor < index) omittedRanges.push([cursor, index]);
        cursor = index + 1;
      }
      if (cursor < rows.length) omittedRanges.push([cursor, rows.length]);
      const first = sourceIndices.length ? sourceIndices[0] : null;
      const last = sourceIndices.length ? sourceIndices[sourceIndices.length - 1] : null;
      Object.assign(result.coverage, {parsed_messages: rows.length, selection_mode: 'source_indices',
        selected_source_indices: sourceIndices.slice(), start_index: null, next_index: null,
        navigation: 'caller_selected_indices', returned_messages: result.messages.length,
        omitted_messages: rows.length - selected.length, omitted_before: first === null ? 0 : first,
        omitted_interior: first === null ? 0 : last - first + 1 - selected.length,
        omitted_after: last === null ? rows.length : rows.length - last - 1,
        omitted_source_index_ranges: omittedRanges, source_index_range_end: 'exclusive',
        selected_content_chars: full, returned_content_chars: used, truncated_messages: truncated,
        all_rendered_messages_included: selected.length === rows.length && truncated === 0});
    }
    result.status = rows.length ? 'PROJECTED' : 'EMPTY_RENDERING';
    return result;
  } catch (error) {
    if (!error?.projection) throw error;
    result.messages = [];
    return refuse(error.code, error.detail);
  }
}

/**
 * Project detailed message search results from an already retained response.
 * Context stays in the retained source; only matched text consumes the body budget.
 */
function projectSlackSearchResults(response, request, options = {}) {
  object(request, 'search projection request');
  object(options, 'search projection options');
  const operation = request.operation;
  if (!['search', 'search_public'].includes(operation)) {
    throw new TypeError('search projection operation must be search or search_public');
  }
  const args = object(request.args, 'search projection request.args');
  const withContext = args.include_context !== false;
  const booleanFields = ['include_bots', 'include_context', 'only_my_channels'];
  for (const [key, value] of Object.entries(args)) {
    if (!OPERATIONS[operation].fields.includes(key)) throw new TypeError('unknown search argument: ' + key);
    if (key === 'keywords') {
      if (!Array.isArray(value) || value.some(item => typeof item !== 'string')) {
        throw new TypeError('search keywords must be an array of strings');
      }
    } else if (booleanFields.includes(key)) {
      if (typeof value !== 'boolean') throw new TypeError('search ' + key + ' must be boolean');
    } else if (key === 'limit' || key === 'max_context_length') {
      if (!Number.isSafeInteger(value) || value < (key === 'limit' ? 1 : 0) ||
          (key === 'limit' && value > 20)) throw new TypeError('invalid search ' + key);
    } else if (typeof value !== 'string') {
      throw new TypeError('search ' + key + ' must be a string');
    }
  }
  const defaults = {start_index: 0, max_results: 8, max_body_chars: 800,
    max_total_body_chars: 6400, max_input_chars: 1048576};
  const ceilings = {start_index: Number.MAX_SAFE_INTEGER, max_results: 20,
    max_body_chars: 65536, max_total_body_chars: 262144, max_input_chars: 8388608};
  for (const key of Object.keys(options)) {
    if (key !== 'source_indices' && !Object.prototype.hasOwnProperty.call(defaults, key)) {
      throw new TypeError('unknown search projection option: ' + key);
    }
  }
  const limits = {...defaults, ...options};
  for (const [key, value] of Object.entries(limits)) {
    if (key === 'source_indices') continue;
    if (!Number.isSafeInteger(value) || value < (['max_results', 'max_input_chars'].includes(key) ? 1 : 0) ||
        value > ceilings[key]) throw new TypeError('invalid search projection option: ' + key);
  }
  let sourceIndices = null;
  if (Object.prototype.hasOwnProperty.call(options, 'source_indices')) {
    if (Object.prototype.hasOwnProperty.call(options, 'start_index')) {
      throw new TypeError('source_indices and start_index are mutually exclusive');
    }
    if (!Array.isArray(options.source_indices) || options.source_indices.length > limits.max_results) {
      throw new TypeError('source_indices must be an array with at most max_results entries');
    }
    sourceIndices = options.source_indices.slice();
    for (let i = 0; i < sourceIndices.length; i++) {
      if (!Number.isSafeInteger(sourceIndices[i]) || sourceIndices[i] < 0 ||
          (i > 0 && sourceIndices[i] <= sourceIndices[i - 1])) {
        throw new TypeError('source_indices must contain distinct increasing nonnegative safe integers');
      }
    }
    limits.source_indices = sourceIndices;
  }
  const result = {schema: 'commons.connected_slack_search_projection/v1', status: 'REFUSED',
    source: {operation, request_args: null, request_binding: 'caller_retained_request',
      content_basis: 'connector_rendered_content', message_identity: 'rendered_header',
      channel_binding: 'rendered_result_header', rendered_query: null,
      rendered_query_range: null, search_preamble_range: null,
      query_application: 'not_verified', representations: 0, input_chars: 0},
    limits, coverage: {scope: 'retained_response_only', snapshot: false}, results: [], issue: null};
  const bad = (code, detail) => { throw {searchProjection: true, code, detail}; };
  let charged = 0;
  const charge = value => {
    charged += value.length;
    result.source.input_chars = charged;
    if (charged > limits.max_input_chars) bad('INPUT_LIMIT', 'Retained request and native payload text exceed max_input_chars.');
  };
  try {
    const serializedArgs = JSON.stringify(args);
    charge(serializedArgs);
    result.source.request_args = JSON.parse(serializedArgs);
    if ((args.response_format !== undefined && args.response_format !== 'detailed') ||
        (args.content_types !== undefined && args.content_types !== 'messages')) {
      bad('UNSUPPORTED_REQUEST', withContext ? 'Projection requires detailed message results.'
        : 'Projection requires detailed message results with explicit include_context:false.');
    }
    if (withContext) result.source.context_projection = 'matched_text_only';
    if (!response || typeof response !== 'object' || Array.isArray(response) || response.isError === true) {
      bad('NATIVE_ERROR', 'Expected a successful retained native search response.');
    }
    const representations = [];
    const accept = value => {
      if (!value || typeof value !== 'object' || Array.isArray(value) ||
          Object.keys(value).length !== 2 || typeof value.results !== 'string' ||
          typeof value.pagination_info !== 'string') {
        bad('UNSUPPORTED_PAYLOAD', 'Expected only string results and pagination_info fields.');
      }
      representations.push(value);
    };
    if (Object.prototype.hasOwnProperty.call(response, 'results')) {
      if (typeof response.results === 'string') charge(response.results);
      if (typeof response.pagination_info === 'string') charge(response.pagination_info);
      accept(response);
    } else {
      if (Object.prototype.hasOwnProperty.call(response, 'structuredContent')) {
        const value = response.structuredContent;
        if (typeof value?.results === 'string') charge(value.results);
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
    if (!representations.length) bad('UNSUPPORTED_PAYLOAD', 'No rendered search envelope was retained.');
    result.source.representations = representations.length;
    const page = representations[0];
    if (representations.some(value => value.results !== page.results || value.pagination_info !== page.pagination_info)) {
      bad('CONFLICTING_REPRESENTATIONS', 'Retained native representations disagree.');
    }
    const rendered = page.results;
    result.source.rendered_chars = rendered.length;
    const nativePage = pagination(page);
    Object.assign(result.coverage, {native_pagination_recognized: nativePage.known,
      provider_end_observed: nativePage.end, next_cursor_available: Boolean(nativePage.next_cursor)});
    const prefix = /^# Search Results for: ([^\r\n]*)\n\n/.exec(rendered);
    if (!prefix) bad('UNSUPPORTED_LAYOUT', 'Expected the detailed search preamble.');
    const queryStart = '# Search Results for: '.length;
    result.source.rendered_query = prefix[1];
    result.source.rendered_query_range = [queryStart, queryStart + prefix[1].length];
    result.source.search_preamble_range = [0, prefix[0].length];
    const rows = [];
    let declared = 0;
    if (rendered !== prefix[0] + 'No results found.\n') {
      const section = /^## Messages \(([1-9][0-9]?) results\)\n/.exec(rendered.slice(prefix[0].length));
      if (!section || Number(section[1]) > 20) {
        bad('UNSUPPORTED_LAYOUT', 'Expected one bounded detailed messages section.');
      }
      declared = Number(section[1]);
      const pattern = /^### Result ([1-9][0-9]*) of ([1-9][0-9]*)\nChannel: [^\r\n]+ \(ID: ([CGD][A-Z0-9]{1,127})\)\n(?:Participants: [^\r\n]+\n)?From: [^\r\n]+ \(ID: [UW][A-Z0-9]{1,127}\)(?: |  \[BOT\])?\nTime: [^\r\n]+\nMessage_ts: ([0-9]{1,16}\.[0-9]{1,16})\n(?:Reply count: [0-9]{1,16}\n)?Permalink: \[link\]\((https:\/\/[^\s()]+)\)\nText: \n/gm;
      const headers = Array.from(rendered.matchAll(pattern));
      const markers = (rendered.match(/^### Result\b/gm) || []).length;
      result.coverage.declared_results = declared;
      result.coverage.observed_result_headers = headers.length;
      if ((!withContext && headers.length !== declared) ||
          (withContext && (headers.length === 0 || headers.length > declared)) ||
          markers !== headers.length ||
          headers[0]?.index !== prefix[0].length + section[0].length ||
          (args.limit !== undefined && declared > args.limit)) {
        bad('RESULT_COUNT_MISMATCH', 'Declared results and complete rendered headers differ.');
      }
      const separator = '\n\n---\n\n';
      const ids = new Set();
      for (let i = 0; i < headers.length; i++) {
        const header = headers[i];
        const resultNumber = Number(header[1]);
        if (Number(header[2]) !== declared ||
            (!withContext && resultNumber !== i + 1) ||
            (withContext && (resultNumber > declared ||
              (i > 0 && resultNumber <= Number(headers[i - 1][1]))))) {
          bad('RESULT_SEQUENCE_MISMATCH', 'Rendered result numbering is inconsistent.');
        }
        const end = i + 1 < headers.length ? headers[i + 1].index : rendered.length;
        if (rendered.slice(end - separator.length, end) !== separator) {
          bad('UNSUPPORTED_LAYOUT', 'Expected the complete detailed-result separator.');
        }
        const bodyStart = header.index + header[0].length;
        const bodyEnd = end - separator.length;
        if (bodyEnd < bodyStart) bad('UNSUPPORTED_LAYOUT', 'Result framing overlaps.');
        const id = header[3] + ':' + header[4];
        if (ids.has(id)) bad('DUPLICATE_IDENTITY', 'The rendering repeats a channel/message identity.');
        ids.add(id);
        const link = /^https:\/\/[^/]+\/archives\/([CGD][A-Z0-9]+)\/p([0-9]+)(?:\?[^\s]*)?$/.exec(header[5]);
        if (!link || link[1] !== header[3] || link[2] !== header[4].replace('.', '')) {
          bad('PERMALINK_MISMATCH', 'Rendered permalink and result identity differ.');
        }
        let contentEnd = bodyEnd;
        const contextSections = [];
        if (withContext) {
          const body = rendered.slice(bodyStart, bodyEnd);
          const contexts = Array.from(body.matchAll(/^Context (before|after):[ \t]*\n/gm));
          if (contexts.length > 2 ||
              (contexts.length === 2 && (contexts[0][1] !== 'before' || contexts[1][1] !== 'after'))) {
            bad('AMBIGUOUS_LAYOUT', 'Context sections are repeated or out of order.');
          }
          if (contexts.length) contentEnd = bodyStart + contexts[0].index;
          for (let j = 0; j < contexts.length; j++) {
            const context = contexts[j];
            const start = bodyStart + context.index;
            const textStart = start + context[0].length;
            const end = j + 1 < contexts.length ? bodyStart + contexts[j + 1].index : bodyEnd;
            if (!/^- (?:From: |\[See result above\] From: )/.test(rendered.slice(textStart, end))) {
              bad('UNSUPPORTED_CONTEXT', 'Expected native context list framing.');
            }
            contextSections.push({kind: context[1], header_range: [start, textStart],
              rendered_content_range: [textStart, end], content_chars: end - textStart});
          }
        }
        const body = rendered.slice(bodyStart, contentEnd);
        if (/^(?:# Search Results for:|## (?:Messages|Files)\b|### Result\b|Context (?:before|after):)/m.test(body)) {
          bad('AMBIGUOUS_LAYOUT', 'Result content contains reserved search or context framing.');
        }
        const row = {source_index: i, channel_id: header[3], message_ts: header[4],
          permalink: header[5], rendered_result_range: [header.index, bodyEnd],
          header_range: [header.index, bodyStart], rendered_content_range: [bodyStart, contentEnd]};
        if (withContext) Object.assign(row, {result_number: resultNumber,
          context_sections: contextSections, context_chars: bodyEnd - contentEnd});
        rows.push(row);
      }
    }
    const from = Math.min(limits.start_index, rows.length);
    const until = Math.min(rows.length, from + limits.max_results);
    if (sourceIndices !== null) {
      result.coverage.parsed_results = rows.length;
      if (sourceIndices.some(index => index >= rows.length)) {
        bad('SOURCE_INDEX_OUT_OF_RANGE', 'A requested source index is outside the parsed retained page.');
      }
    }
    const selected = sourceIndices === null ? rows.slice(from, until) : sourceIndices.map(index => rows[index]);
    let full = 0;
    let used = 0;
    let truncated = 0;
    for (const row of selected) {
      const [start, end] = row.rendered_content_range;
      let length = Math.min(end - start, limits.max_body_chars, limits.max_total_body_chars - used);
      if (length > 0 && length < end - start &&
          rendered.charCodeAt(start + length - 1) >= 0xd800 && rendered.charCodeAt(start + length - 1) <= 0xdbff &&
          rendered.charCodeAt(start + length) >= 0xdc00 && rendered.charCodeAt(start + length) <= 0xdfff) length--;
      const clipped = length < end - start;
      result.results.push({...row, rendered_content: rendered.slice(start, start + length),
        content_chars: end - start, returned_chars: length, truncated: clipped});
      full += end - start; used += length; truncated += clipped ? 1 : 0;
    }
    if (sourceIndices === null) {
      Object.assign(result.coverage, {declared_results: declared, parsed_results: rows.length,
        start_index: from, returned_results: result.results.length, omitted_before: from,
        omitted_after: rows.length - until, next_index: until < rows.length ? until : null,
        selected_content_chars: full, returned_content_chars: used, truncated_results: truncated,
        all_rendered_results_included: from === 0 && until === rows.length && truncated === 0});
    } else {
      const omittedRanges = [];
      let cursor = 0;
      for (const index of sourceIndices) {
        if (cursor < index) omittedRanges.push([cursor, index]);
        cursor = index + 1;
      }
      if (cursor < rows.length) omittedRanges.push([cursor, rows.length]);
      const first = sourceIndices.length ? sourceIndices[0] : null;
      const last = sourceIndices.length ? sourceIndices[sourceIndices.length - 1] : null;
      Object.assign(result.coverage, {declared_results: declared, parsed_results: rows.length,
        selection_mode: 'source_indices', selected_source_indices: sourceIndices.slice(),
        start_index: null, next_index: null, navigation: 'caller_selected_indices',
        returned_results: result.results.length, omitted_results: rows.length - selected.length,
        omitted_before: first === null ? 0 : first,
        omitted_interior: first === null ? 0 : last - first + 1 - selected.length,
        omitted_after: last === null ? rows.length : rows.length - last - 1,
        omitted_source_index_ranges: omittedRanges, source_index_range_end: 'exclusive',
        selected_content_chars: full, returned_content_chars: used, truncated_results: truncated,
        all_rendered_results_included: selected.length === rows.length && truncated === 0});
    }
    if (withContext) Object.assign(result.coverage, {
      unrendered_results: declared - rows.length,
      rendered_result_numbers: rows.map(row => row.result_number),
      selected_context_chars: selected.reduce((total, row) => total + row.context_chars, 0),
      returned_context_chars: 0,
      all_declared_results_included: rows.length === declared && result.coverage.all_rendered_results_included,
    });
    result.status = rows.length
      ? (withContext && rows.length < declared ? 'PARTIAL' : 'PROJECTED')
      : 'EMPTY_RENDERING';
    return result;
  } catch (error) {
    if (!error?.searchProjection) throw error;
    result.results = [];
    result.issue = {code: error.code, detail: error.detail};
    return result;
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {collectSlackPages, projectSlackMessages, projectSlackSearchResults};
}
