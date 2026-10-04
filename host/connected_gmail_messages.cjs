'use strict';

// Pure retained-response projection. No provider calls, HTML rendering, or input mutation.
// Counts and limits use JavaScript UTF-16 code units; source paths refer to the input.
const DEFAULTS = Object.freeze({
  maxMessages: 10,
  maxBodyChars: 6000,
  maxTotalBodyChars: 18000,
  maxHeaderChars: 300,
  maxBodiesPerMessage: 8,
});
const own = (value, key) => Object.prototype.hasOwnProperty.call(value, key);
const record = value => value !== null && typeof value === 'object' && !Array.isArray(value);

function fail(code, path, detail) {
  const error = new TypeError(`${code} at ${path}: ${detail}`);
  error.code = code;
  error.source_path = path;
  throw error;
}

function clip(value, limit) {
  let end = Math.min(value.length, limit);
  if (end < value.length && end > 0 && /[\uD800-\uDBFF]/.test(value[end - 1])
    && /[\uDC00-\uDFFF]/.test(value[end])) end -= 1;
  return value.slice(0, end);
}

function header(part, name) {
  if (part.headers === undefined) return '';
  if (!Array.isArray(part.headers)) fail('UNSUPPORTED_MIME', '$.headers', 'headers must be an array');
  const found = part.headers.find(h => record(h) && typeof h.name === 'string'
    && h.name.toLowerCase() === name);
  if (!found) return '';
  if (typeof found.value !== 'string') fail('UNSUPPORTED_MIME', '$.headers', 'header value must be text');
  return found.value;
}

function omittedCounts() {
  return {
    headers: 0, header_chars: 0, body_chars: 0, body_parts: 0,
    attachments: 0, forwarded_messages: 0, alternative_branches: 0,
    related_parts: 0, unsupported_parts: 0,
  };
}

/**
 * Project native read_email / batch_read_email full MIME CallToolResults only.
 * Supported envelopes: structuredContent.{id,thread_id,payload}, or
 * structuredContent.responses[] containing those full message objects.
 * bodies[].text is plain text or explicitly labelled, unrendered HTML data.
 * Missing decoded content / external attachment_id bodies remain unavailable.
 * Encoded bodies and snippets are never substituted for exact body.content.
 */
function projectGmailMessages(response, options = {}) {
  if (!record(options)) fail('INVALID_OPTIONS', '$.options', 'expected an object');
  const limits = { ...DEFAULTS };
  for (const [key, value] of Object.entries(options)) {
    if (!own(DEFAULTS, key) || !Number.isSafeInteger(value) || value < 0) {
      fail('INVALID_OPTIONS', `$.options.${key}`, 'expected a supported nonnegative integer limit');
    }
    limits[key] = value;
  }
  if (!record(response) || response.isError === true || response.error != null
    || !record(response.structuredContent)) {
    fail('UNSUPPORTED_GMAIL_RESPONSE', '$', 'expected a successful native full-MIME structuredContent response');
  }
  const structured = response.structuredContent;
  if (structured.isError === true || structured.error != null || structured.error_code != null) {
    fail('GMAIL_ERROR_RESPONSE', '$.structuredContent', 'error responses cannot be projected as messages');
  }
  const batch = own(structured, 'responses');
  if (batch && !Array.isArray(structured.responses)) {
    fail('UNSUPPORTED_GMAIL_RESPONSE', '$.structuredContent.responses', 'expected an array of full messages');
  }
  const inputs = batch ? structured.responses : [structured];
  const sourceOf = index => batch ? `$.structuredContent.responses[${index}]` : '$.structuredContent';
  // Validate even omitted message envelopes, so raw/search/error entries are explicit failures.
  for (let index = 0; index < inputs.length; index += 1) {
    const item = inputs[index];
    if (!record(item) || item.isError === true || item.error != null || item.error_code != null
      || typeof item.id !== 'string' || !item.id || item.id.length > 1024
      || typeof item.thread_id !== 'string' || !item.thread_id || item.thread_id.length > 1024
      || !record(item.payload) || typeof item.payload.mime_type !== 'string') {
      fail('UNSUPPORTED_GMAIL_MESSAGE', sourceOf(index), 'expected id, thread_id and a full MIME payload, without an error');
    }
  }

  const result = {
    format: 'gmail-mime-projection-v1',
    source_shape: batch ? 'batch' : 'single',
    message_count: inputs.length,
    messages: [],
    omitted: { messages: Math.max(0, inputs.length - limits.maxMessages), body_chars: 0, header_chars: 0, body_parts: 0 },
    limits,
  };
  let remaining = limits.maxTotalBodyChars;
  for (let index = 0; index < Math.min(inputs.length, limits.maxMessages); index += 1) {
    const item = inputs[index];
    const source = sourceOf(index);
    const omitted = omittedCounts();
    const message = { id: item.id, thread_id: item.thread_id, subject: '', from: '', date: '', bodies: [], unavailable_bodies: [], omitted };
    let selectedHeaders = 0;
    for (const name of ['subject', 'from', 'date']) {
      const value = header(item.payload, name);
      if ((item.payload.headers || []).some(h => record(h) && typeof h.name === 'string' && h.name.toLowerCase() === name)) selectedHeaders += 1;
      message[name] = clip(value, limits.maxHeaderChars);
      omitted.header_chars += value.length - message[name].length;
    }
    omitted.headers = (item.payload.headers || []).length - selectedHeaders;

    let nodes = 0;
    const visited = new Set();
    function select(part, path, depth) {
      if (!record(part) || typeof part.mime_type !== 'string' || !part.mime_type) {
        fail('UNSUPPORTED_MIME', path, 'expected a MIME part with mime_type');
      }
      if (depth > 32 || ++nodes > 4096 || visited.has(part)) {
        fail('MIME_STRUCTURE_LIMIT', path, 'MIME tree is cyclic, too deep, or exceeds 4096 visited parts');
      }
      visited.add(part);
      const mime = part.mime_type.split(';')[0].trim().toLowerCase();
      if ((typeof part.filename === 'string' && part.filename.trim())
        || /^\s*attachment(?:\s*;|\s*$)/i.test(header(part, 'content-disposition'))) {
        omitted.attachments += 1;
        return [];
      }
      if (mime === 'message/rfc822' || mime === 'message/global') {
        omitted.forwarded_messages += 1;
        return [];
      }
      if (mime.startsWith('multipart/')) {
        if (!Array.isArray(part.parts)) fail('UNSUPPORTED_MIME', path + '.parts', 'multipart requires parts');
        if (mime === 'multipart/related' && part.parts.length) {
          const start = /(?:^|;)\s*start\s*=\s*(?:"([^"]*)"|([^;\s]+))/i.exec(header(part, 'content-type'));
          let chosen = 0;
          if (start) {
            const cid = (start[1] || start[2]).replace(/^<|>$/g, '');
            chosen = part.parts.findIndex(child => record(child)
              && header(child, 'content-id').trim().replace(/^<|>$/g, '') === cid);
            if (chosen < 0) fail('UNSUPPORTED_MIME', path, 'multipart/related start does not identify a child');
          }
          omitted.related_parts += part.parts.length - 1;
          return select(part.parts[chosen], `${path}.parts[${chosen}]`, depth + 1);
        }
        const children = part.parts.map((child, childIndex) => select(child, `${path}.parts[${childIndex}]`, depth + 1));
        if (mime === 'multipart/alternative') {
          const chosen = children.find(parts => parts.some(body => body.mime_type === 'text/plain'))
            || children.find(parts => parts.some(body => body.mime_type === 'text/html'));
          omitted.alternative_branches += Math.max(0, children.length - (chosen ? 1 : 0));
          return chosen || [];
        }
        return children.flat();
      }
      if (mime !== 'text/plain' && mime !== 'text/html') {
        omitted.unsupported_parts += 1;
        return [];
      }
      if (!record(part.body)) fail('UNSUPPORTED_MIME', path + '.body', 'text part requires a body object');
      return [{ mime_type: mime, source_path: path + '.body', body: part.body }];
    }

    const selected = select(item.payload, source + '.payload', 0);
    for (let bodyIndex = 0; bodyIndex < selected.length; bodyIndex += 1) {
      const selectedBody = selected[bodyIndex];
      const body = selectedBody.body;
      const path = selectedBody.source_path;
      const external = typeof body.attachment_id === 'string' && body.attachment_id.length > 0;
      const inline = !external && typeof body.content === 'string';
      if (!inline) {
        if (bodyIndex < limits.maxBodiesPerMessage) {
          message.unavailable_bodies.push({
            mime_type: selectedBody.mime_type,
            source_path: external ? path + '.attachment_id' : own(body, 'content') ? path + '.content' : path,
            reason: external ? 'external_attachment_id' : 'decoded_content_unavailable',
          });
        } else omitted.body_parts += 1;
        continue;
      }
      const content = body.content;
      if (bodyIndex >= limits.maxBodiesPerMessage) {
        omitted.body_parts += 1;
        omitted.body_chars += content.length;
        continue;
      }
      const text = clip(content, Math.min(limits.maxBodyChars, remaining));
      const lost = content.length - text.length;
      remaining -= text.length;
      omitted.body_chars += lost;
      message.bodies.push({ mime_type: selectedBody.mime_type, text, source_path: path + '.content', original_chars: content.length, omitted_chars: lost, truncated: lost > 0 });
    }
    result.messages.push(message);
    result.omitted.body_chars += omitted.body_chars;
    result.omitted.header_chars += omitted.header_chars;
    result.omitted.body_parts += omitted.body_parts;
  }
  return result;
}

module.exports = { projectGmailMessages };
