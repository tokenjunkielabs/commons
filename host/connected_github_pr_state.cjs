"use strict";

// One native GET; retain GitHub's nullable mergeability without polling.
// The caller owns the tool binding and the original response's private custody.
const FETCH = "mcp__codex_apps__github_fetch";
const own = (value, key) => Object.prototype.hasOwnProperty.call(value, key);
const object = value => value !== null && typeof value === "object" && !Array.isArray(value);

function canonicalPullRequest(value) {
  return object(value) && Number.isSafeInteger(value.number) && value.number > 0 &&
    object(value.head) && object(value.base) && typeof value.html_url === "string";
}

function decodePullRequest(response) {
  const queue = [response];
  const seen = new Set();
  const parsedPullRequests = new Map();
  const enqueueText = text => {
    try {
      let value = parsedPullRequests.get(text);
      if (value === undefined) {
        value = JSON.parse(text);
        // PR payloads terminate traversal before a reused object can be visited.
        if (canonicalPullRequest(value)) parsedPullRequests.set(text, value);
      }
      queue.push(value);
    } catch (_) { /* Provider status text or another non-JSON payload. */ }
  };
  for (let offset = 0; offset < queue.length && offset < 32; offset += 1) {
    const value = queue[offset];
    if (!object(value) || seen.has(value)) continue;
    seen.add(value);
    if (value.isError === true || own(value, "error")) {
      const error = new Error("native GitHub response reports an error");
      error.code = "NATIVE_ERROR";
      throw error;
    }
    if (canonicalPullRequest(value)) {
      return value;
    }
    if (object(value.structuredContent)) queue.push(value.structuredContent);
    if (typeof value.content === "string") {
      enqueueText(value.content);
    }
    for (const part of Array.isArray(value.content) ? value.content : []) {
      if (part.type !== "text" || typeof part.text !== "string") continue;
      enqueueText(part.text);
    }
  }
  throw new TypeError("response has no canonical GitHub pull-request payload");
}

function nullableField(payload, key, type) {
  const present = own(payload, key);
  const value = present ? payload[key] : null;
  if (value !== null && typeof value !== type) {
    throw new TypeError("pull request " + key + " must be " + type + " or null");
  }
  return { present, value };
}

function refView(ref) {
  if (typeof ref.ref !== "string" || typeof ref.sha !== "string") {
    throw new TypeError("pull request ref and sha must be strings");
  }
  const repository = ref.repo == null ? null : ref.repo.full_name;
  if (repository !== null && typeof repository !== "string") {
    throw new TypeError("pull request repository name must be a string or null");
  }
  return { ref: ref.ref, sha: ref.sha, repository };
}

/** Project one retained native response. No provider call or source mutation. */
function projectGitHubPullRequest(response) {
  const payload = decodePullRequest(response);
  if (typeof payload.title !== "string" || typeof payload.state !== "string") {
    throw new TypeError("pull request title and state must be strings");
  }
  return {
    number: payload.number,
    url: payload.html_url,
    title: payload.title,
    state: payload.state,
    draft: nullableField(payload, "draft", "boolean"),
    merged: nullableField(payload, "merged", "boolean"),
    mergeable: nullableField(payload, "mergeable", "boolean"),
    mergeable_state: nullableField(payload, "mergeable_state", "string"),
    merge_commit_sha: nullableField(payload, "merge_commit_sha", "string"),
    merged_at: nullableField(payload, "merged_at", "string"),
    updated_at: nullableField(payload, "updated_at", "string"),
    head: refView(payload.head),
    base: refView(payload.base),
  };
}

/** Read one PR through the existing native REST binding. Never retries or merges. */
async function readGitHubPullRequest(tools, input) {
  if (!object(input) || Object.keys(input).some(key =>
    key !== "repository_full_name" && key !== "pr_number")) {
    throw new TypeError("input supports repository_full_name and pr_number");
  }
  const repository = input.repository_full_name;
  const number = input.pr_number;
  if (typeof repository !== "string" || !/^[^/\s?#]+\/[^/\s?#]+$/.test(repository)) {
    throw new TypeError("repository_full_name must have owner/name form");
  }
  if (!Number.isSafeInteger(number) || number < 1) {
    throw new TypeError("pr_number must be a positive safe integer");
  }
  if (!tools || typeof tools[FETCH] !== "function") {
    throw new TypeError("the native " + FETCH + " action is not available");
  }
  const url = "https://api.github.com/repos/" + repository.split("/")
    .map(encodeURIComponent).join("/") + "/pulls/" + number;
  const started = Date.now();
  const result = {
    schema: "commons.connected_github_pr_state/v1",
    request: { repository_full_name: repository, pr_number: number, url },
    started_at: new Date(started).toISOString(),
    calls: 1,
    status: "INCONCLUSIVE",
    pr: null,
    response: null,
  };
  try {
    result.response = await tools[FETCH]({ url });
  } catch (error) {
    result.status = "TOOL_ERROR";
    result.error = { message: error instanceof Error ? error.message : String(error) };
  }
  if (result.status !== "TOOL_ERROR") {
    try {
      const pr = projectGitHubPullRequest(result.response);
      const actualUrl = pr.url.replace(/\/$/, "").toLowerCase();
      const expectedUrl = ("https://github.com/" + repository + "/pull/" + number).toLowerCase();
      if (pr.number !== number || actualUrl !== expectedUrl) {
        throw new TypeError("native pull request does not match the requested repository/number");
      }
      result.pr = pr;
      result.status = "READ";
    } catch (error) {
      result.status = error.code === "NATIVE_ERROR" ? "NATIVE_ERROR" : "INVALID_RESPONSE";
      result.error = { message: error.message };
    }
  }
  result.finished_at = new Date().toISOString();
  result.elapsed_ms = Date.now() - started;
  return result;
}

module.exports = Object.freeze({ projectGitHubPullRequest, readGitHubPullRequest });
