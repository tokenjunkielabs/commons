"use strict";

// Use the approved native REST route without translating GitHub query syntax.
// The caller supplies the connected tool surface; this module owns no network
// client, credentials, filesystem, scheduler, or mutation operation.
const FETCH = "mcp__codex_apps__github_fetch";
const SEARCH_LIMIT = 1000;
const SORTS = new Set([
  "comments", "reactions", "reactions-+1", "reactions--1", "reactions-smile",
  "reactions-thinking_face", "reactions-heart", "reactions-tada",
  "interactions", "created", "updated",
]);

function object(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function positiveInteger(value, name) {
  if (!Number.isSafeInteger(value) || value < 1) {
    throw new TypeError(name + " must be a positive safe integer");
  }
  return value;
}

function configFor(input) {
  if (!object(input)) throw new TypeError("input must be an object");
  const keys = new Set([
    "query", "sort", "order", "per_page", "start_page", "max_pages", "timeout_ms",
  ]);
  for (const key of Object.keys(input)) {
    if (!keys.has(key)) throw new TypeError("unknown input field: " + key);
  }
  if (typeof input.query !== "string" || !input.query.trim()) {
    throw new TypeError("query must be a nonempty GitHub search string");
  }
  const sort = input.sort ?? null;
  if (sort !== null && !SORTS.has(sort)) throw new TypeError("unsupported sort");
  const order = input.order ?? "desc";
  if (order !== "asc" && order !== "desc") {
    throw new TypeError("order must be asc or desc");
  }
  const perPage = positiveInteger(input.per_page ?? 100, "per_page");
  if (perPage > 100) throw new TypeError("per_page exceeds GitHub's maximum of 100");
  const startPage = positiveInteger(input.start_page ?? 1, "start_page");
  const maxPages = positiveInteger(input.max_pages ?? 4, "max_pages");
  const timeout = input.timeout_ms ?? 30000;
  if (typeof timeout !== "number" || !Number.isFinite(timeout) || timeout < 0) {
    throw new TypeError("timeout_ms must be a finite nonnegative number");
  }
  return { query: input.query, sort, order, perPage, startPage, maxPages, timeout };
}

function decode(response) {
  const candidates = [response && response.structuredContent, response];
  for (const candidate of candidates) {
    if (!object(candidate)) continue;
    if (Array.isArray(candidate.items)) return candidate;
    if (typeof candidate.content === "string") {
      const parsed = JSON.parse(candidate.content);
      if (object(parsed)) return parsed;
    }
  }
  for (const item of response && Array.isArray(response.content) ? response.content : []) {
    if (item.type !== "text" || typeof item.text !== "string") continue;
    try {
      const parsed = JSON.parse(item.text);
      if (object(parsed) && Array.isArray(parsed.items)) return parsed;
    } catch (_) {
      // Ordinary provider status text is not a search payload.
    }
  }
  throw new TypeError("native response has no issue-search payload");
}

function diagnostic(value) {
  if (value instanceof Error) return value.message.slice(0, 1200);
  if (value && Array.isArray(value.content)) {
    return value.content.filter(item => item.type === "text")
      .map(item => item.text).join("\n").slice(0, 1200);
  }
  return String(value).slice(0, 1200);
}

function itemIdentity(row) {
  if (!object(row)) throw new TypeError("search item must be an object");
  let id;
  if (typeof row.id === "number") id = String(positiveInteger(row.id, "item.id"));
  else if (typeof row.id === "string" && /^[1-9][0-9]*$/.test(row.id)) id = row.id;
  else throw new TypeError("item.id must be a positive integer or decimal ID string");
  positiveInteger(row.number, "item.number");
  if (typeof row.url !== "string" || typeof row.html_url !== "string") {
    throw new TypeError("search item URLs are missing");
  }
  if (row.pull_request != null && !object(row.pull_request)) {
    throw new TypeError("item.pull_request must be an object when present");
  }
  return id;
}

/**
 * Read native issue/PR search pages with the caller's exact GitHub query.
 *
 * Items retain their original native fields, including pull_request metadata.
 * onResponse can retain each original MCP response privately. Completeness is
 * limited to this observed search traversal, never a repository inventory.
 */
async function searchGitHubIssues(tools, input, options = {}) {
  const config = configFor(input);
  if (!tools || typeof tools[FETCH] !== "function") {
    throw new TypeError("the native " + FETCH + " action is not available");
  }
  if (!object(options) || Object.keys(options).some(key => key !== "onResponse")) {
    throw new TypeError("options supports only onResponse");
  }
  if (options.onResponse !== undefined && typeof options.onResponse !== "function") {
    throw new TypeError("onResponse must be a function");
  }
  const started = Date.now();
  const seen = new Set();
  const repeated = new Set();
  const totals = new Set();
  const result = {
    schema: "commons.connected_github_issue_search/v1",
    status: "INCONCLUSIVE",
    query: config.query,
    sort: config.sort,
    order: config.order,
    items: [],
    coverage: {
      complete: false,
      search_index: true,
      snapshot: false,
      pagination: "live_offset_pages",
      start_page: config.startPage,
      per_page: config.perPage,
      api_search_limit: SEARCH_LIMIT,
      end_observed: false,
      provider_incomplete: false,
      pages: [],
      total_counts: [],
      repeated_item_ids: [],
      next_page: config.startPage,
      gaps: config.startPage === 1 ? [] : ["STARTED_AFTER_FIRST_PAGE"],
    },
    stats: {
      calls: 0, pages_read: 0, items_received: 0,
      unique_items: 0, issues: 0, pull_requests: 0,
    },
    callback_errors: [],
    started_at: new Date(started).toISOString(),
  };
  const gap = code => {
    if (!result.coverage.gaps.includes(code)) result.coverage.gaps.push(code);
  };
  function finish(code, detail = {}) {
    result.coverage.total_counts = [...totals];
    result.coverage.repeated_item_ids = [...repeated];
    result.stats.unique_items = seen.size;
    result.stop = { code, ...detail };
    result.finished_at = new Date().toISOString();
    result.elapsed_ms = Date.now() - started;
    result.status = result.items.length > 0 ? "FOUND"
      : result.coverage.complete ? "NOT_FOUND_IN_QUERY" : "INCONCLUSIVE";
    return result;
  }
  let page = config.startPage;
  while (result.stats.calls < config.maxPages) {
    if (Date.now() - started >= config.timeout) return finish("DEADLINE");
    const offset = (page - 1) * config.perPage;
    if (!Number.isSafeInteger(offset) || offset >= SEARCH_LIMIT) {
      gap("SEARCH_RESULT_LIMIT");
      return finish("SEARCH_RESULT_LIMIT");
    }
    const query = {
      q: config.query,
      ...(config.sort === null ? {} : { sort: config.sort }),
      order: config.order,
      per_page: String(config.perPage),
      page: String(page),
    };
    const url = "https://api.github.com/search/issues?" + Object.entries(query)
      .map(([key, value]) => encodeURIComponent(key) + "=" + encodeURIComponent(value))
      .join("&");
    result.coverage.next_page = page;
    result.stats.calls += 1;
    let response;
    try {
      response = await tools[FETCH]({ url });
    } catch (error) {
      return finish("TOOL_ERROR", { url, native_message: diagnostic(error) });
    }
    if (options.onResponse) {
      try {
        await options.onResponse({ page, url, response });
      } catch (error) {
        result.callback_errors.push({ page, message: diagnostic(error) });
      }
    }
    if (response && response.isError) {
      return finish("NATIVE_ERROR", { url, native_message: diagnostic(response) });
    }
    let payload;
    try {
      payload = decode(response);
      if (!Array.isArray(payload.items) ||
          !Number.isSafeInteger(payload.total_count) || payload.total_count < 0 ||
          typeof payload.incomplete_results !== "boolean" ||
          payload.items.length > config.perPage) {
        throw new TypeError("invalid items, total_count, incomplete_results, or page length");
      }
    } catch (error) {
      return finish("INVALID_RESPONSE", { url, native_message: diagnostic(error) });
    }
    const rows = payload.items;
    totals.add(payload.total_count);
    if (totals.size > 1) gap("TOTAL_COUNT_CHANGED");
    if (payload.total_count >= SEARCH_LIMIT) gap("SEARCH_RESULT_LIMIT");
    if (payload.incomplete_results) {
      result.coverage.provider_incomplete = true;
      gap("PROVIDER_INCOMPLETE_RESULTS");
    }
    const observation = {
      page, url, total_count: payload.total_count,
      incomplete_results: payload.incomplete_results,
      received: rows.length, retained: 0,
    };
    result.coverage.pages.push(observation);
    result.stats.pages_read += 1;
    result.stats.items_received += rows.length;
    for (let index = 0; index < rows.length; index += 1) {
      const row = rows[index];
      let id;
      try {
        id = itemIdentity(row);
      } catch (error) {
        return finish("INVALID_RESPONSE", { url, row_index: index, native_message: diagnostic(error) });
      }
      if (seen.has(id)) {
        repeated.add(id);
        gap("REPEATED_ITEM_ID");
        continue;
      }
      seen.add(id);
      result.items.push(row);
      observation.retained += 1;
      if (row.pull_request == null) result.stats.issues += 1;
      else result.stats.pull_requests += 1;
    }
    result.coverage.next_page = page + 1;
    const shortPage = rows.length < config.perPage;
    const observedTotal = config.startPage === 1 && seen.size >= payload.total_count;
    if (shortPage || observedTotal) {
      result.coverage.end_observed = true;
      result.coverage.next_page = null;
      if (config.startPage === 1 && seen.size !== payload.total_count) {
        gap("ADVERTISED_TOTAL_MISMATCH");
      }
      result.coverage.complete = config.startPage === 1 &&
        result.coverage.gaps.length === 0 && seen.size === payload.total_count;
      return finish(shortPage ? "PAGINATION_END" : "ADVERTISED_TOTAL_REACHED");
    }
    if (offset + rows.length >= SEARCH_LIMIT) {
      gap("SEARCH_RESULT_LIMIT");
      return finish("SEARCH_RESULT_LIMIT");
    }
    page += 1;
  }
  return finish("PAGE_BUDGET");
}

module.exports = { searchGitHubIssues };
