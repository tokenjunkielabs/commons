#!/usr/bin/env python3
"""Read scoped work declarations from retained Slack responses, without actions.

This is an advisory over supplied observations. It is not the canonical claims
ledger, an ownership decision, a provider client, or a message sender.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit

SCHEMA = "commons.slack_claim_scan/v1"
MAX_INPUT_BYTES = 64 * 1024 * 1024
STAMP = re.compile(r"[0-9]{1,12}\.[0-9]{1,6}\Z")
OPERATION = r"[A-Za-z0-9][A-Za-z0-9_.:/#-]{5,190}"
DECLARATION = re.compile(r"^(?:CLAIM|TAKE|RESUME|TAKING)\s+(" + OPERATION + r")(?=\s|$|[—–])", re.I)
TERMINAL = re.compile(r"^(LANDED|DONE|COMPLETED?|RELEASED?)\s+(" + OPERATION + r")(?=\s|$|[—–])", re.I)
TERMINAL_AFTER = re.compile(r"^(" + OPERATION + r")\s+(?:is\s+)?(LANDED|DONE|COMPLETED?|RELEASED?)\b", re.I)
HEADER = re.compile(
    r"^(?:=== THREAD PARENT MESSAGE ===|--- Reply [0-9]+ of [0-9]+ ---|"
    r"=== Message from .+? ===[^\n]*|### Result [0-9]+ of [0-9]+)\s*$", re.M)
MESSAGE_STAMP = re.compile(r"^Message(?: TS|_ts):\s*([0-9]+\.[0-9]+)\s*$", re.M)
CHANNEL = re.compile(r"(?:\(ID:\s*|\()([CGD][A-Z0-9]+)\)")
FILE_PATH = re.compile(
    r"(?<![A-Za-z0-9_./:-])((?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+\.[A-Za-z][A-Za-z0-9]{0,9})"
    r"(?=$|[^A-Za-z0-9_/-])")
BRACES = re.compile(r"((?:[A-Za-z0-9_.-]+/)+)\{([^{}\n]+)\}")


class ScanError(ValueError):
    pass


def _load(raw):
    def pairs(values):
        result = {}
        for key, value in values:
            if key in result:
                raise ScanError("duplicate JSON key: " + key)
            result[key] = value
        return result
    try:
        return json.loads(raw, object_pairs_hook=pairs)
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise ScanError("input is not an unambiguous UTF-8 JSON response") from exc


def _stamp(value):
    if not isinstance(value, str) or STAMP.fullmatch(value) is None:
        raise ScanError("message timestamp must retain its Slack string value")
    seconds, fraction = value.split(".")
    return str(int(seconds)) + "." + fraction.ljust(6, "0")


def _channel(value):
    if not isinstance(value, str) or re.fullmatch(r"[CGD][A-Z0-9]+", value) is None:
        raise ScanError("message channel is missing; supply --channel-id for a thread export")
    return value


def _workspace(value):
    if not value:
        return None
    parts = urlsplit(value)
    if (parts.scheme != "https" or not parts.hostname or parts.username or parts.password
            or parts.query or parts.fragment or parts.path not in ("", "/")
            or not parts.hostname.endswith(".slack.com") or parts.port is not None):
        raise ScanError("--workspace-url must be the HTTPS Slack workspace root")
    return "https://" + parts.hostname


def _message(row, fallback_channel, source):
    if not isinstance(row, dict) or not isinstance(row.get("text"), str):
        raise ScanError("Slack messages must contain text and an exact timestamp")
    channel = row.get("channel", fallback_channel)
    if isinstance(channel, dict):
        channel = channel.get("id")
    stamp = _stamp(row.get("ts"))
    return {"channel_id": _channel(channel), "message_ts": stamp,
            "text": row["text"].strip(), "source": source,
            "permalink": row.get("permalink") if isinstance(row.get("permalink"), str) else None}


def _pagination(page, source, count):
    info = page.get("pagination_info")
    cursor, terminal = None, None
    if isinstance(info, str):
        normalized = info.strip().replace("\\n", "").strip()
        if re.fullmatch(r"(?:There are no more messages (?:in this thread|available)\.?|"
                        r"End of results - No more pages available\.?)", normalized, re.I):
            terminal = True
        else:
            match = re.search(r"\bcursor\s*:?[ \t]*`([^`]+)`", normalized, re.I)
            if match:
                cursor, terminal = match[1], False
    else:
        metadata = page.get("response_metadata", {})
        if isinstance(metadata, dict) and isinstance(metadata.get("next_cursor"), str):
            cursor = metadata["next_cursor"] or None
        if cursor or page.get("has_more") is True:
            terminal = False
        elif page.get("has_more") is False:
            terminal = True
    return {"source": source, "message_count": count, "terminal_page": terminal,
            "next_cursor": cursor, "pagination_known": terminal is not None}


def _rendered(page, fallback_channel, source):
    text = page.get("messages", page.get("results"))
    if not isinstance(text, str):
        raise ScanError("rendered Slack response must contain a messages or results string")
    matches = list(HEADER.finditer(text))
    rows = []
    prefix = text[:matches[0].start()] if matches else text
    channel_match = CHANNEL.search(prefix)
    default_channel = channel_match[1] if channel_match else fallback_channel
    for index, heading in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[heading.end():end]
        stamp = MESSAGE_STAMP.search(block)
        if not stamp:
            raise ScanError("a rendered message header is missing its timestamp")
        meta = block[:stamp.start()]
        channel_match = CHANNEL.search(meta)
        channel = channel_match[1] if channel_match else default_channel
        body = block[stamp.end():].lstrip("\n")
        if heading[0].startswith("### Result"):
            marker = re.search(r"^Text:\s*\n?", body, re.M)
            if not marker:
                raise ScanError("rendered search result is missing its Text field")
            link = re.search(r"^Permalink: \[link\]\((https://[^)]+)\)", body[:marker.start()], re.M)
            permalink = link[1] if link else None
            body = body[marker.end():]
            body = re.sub(r"\n---\s*$", "", body)
        else:
            permalink = None
            body = re.sub(r"\n=== THREAD REPLIES \([^\n]*\) ===\s*$", "", body)
            body = re.sub(r"\nThread: [0-9]+ replies[^\n]*\s*$", "", body)
        rows.append(_message({"ts": stamp[1], "text": body, "channel": channel,
                              "permalink": permalink}, default_channel, source))
    if not matches and not re.search(r"(?:No results found|No messages|no messages)", text):
        # Some native empty-history responses carry an empty messages field.
        if text.strip():
            raise ScanError("unsupported rendered Slack message layout")
    return rows, _pagination(page, source, len(rows))


def read_responses(value, *, channel_id=None, source="input"):
    """Accept raw Slack pages or native MCP text/structured response envelopes."""
    messages, pages = [], []
    def visit(node, depth=0):
        if depth > 20:
            raise ScanError("response envelope nesting exceeds 20 levels")
        if isinstance(node, list):
            if not node:
                return False
            found = False
            for child in node:
                found = visit(child, depth + 1) or found
            return found
        if not isinstance(node, dict):
            return False
        if node.get("isError") is True or node.get("ok") is False:
            raise ScanError("source records a failed provider read")
        if isinstance(node.get("messages"), list):
            channel = node.get("channel", channel_id)
            rows = [_message(row, channel, source) for row in node["messages"]]
            messages.extend(rows)
            pages.append(_pagination(node, source, len(rows)))
            return True
        if isinstance(node.get("messages"), str) or isinstance(node.get("results"), str):
            rows, page = _rendered(node, channel_id, source)
            messages.extend(rows)
            pages.append(page)
            return True
        # Structured content takes precedence over its textual mirror.
        if "structuredContent" in node and visit(node["structuredContent"], depth + 1):
            return True
        if "content" in node:
            return visit(node["content"], depth + 1)
        if node.get("type") == "text" and isinstance(node.get("text"), str):
            content = node["text"].strip()
            if content.startswith(("{", "[")):
                return visit(_load(content), depth + 1)
        return False
    if not visit(value):
        raise ScanError("no supported Slack response found")
    return messages, pages


def _paths(text):
    # URL paths describe links, not a declaration's source-file scope.
    text = re.sub(r"https?://[^\s<>]+", "", text)
    expanded = []
    for match in BRACES.finditer(text):
        members = [member.strip(" `") for member in match[2].split(",")]
        if all(re.fullmatch(r"[A-Za-z0-9_.-]+\.[A-Za-z][A-Za-z0-9]{0,9}", member) for member in members):
            expanded.extend(match[1] + member for member in members)
    return sorted(set(expanded) | {match[1].removeprefix("./") for match in FILE_PATH.finditer(text)})


def _statement(text):
    first = text.lstrip(" *`\n")
    match = DECLARATION.match(first)
    if match:
        operation = match[1].rstrip(".:;")
        if "-" in operation or ":" in operation:
            return "declaration", operation
    match = TERMINAL.match(first)
    if match:
        return match[1].lower(), match[2].rstrip(".:;")
    match = TERMINAL_AFTER.match(first)
    if match:
        return match[2].lower(), match[1].rstrip(".:;")
    return None


def scan(messages, pages, *, workspace_url=None):
    workspace = _workspace(workspace_url)
    identities = defaultdict(dict)
    for message in messages:
        digest = hashlib.sha256(message["text"].encode("utf-8")).hexdigest()
        identities[(message["channel_id"], message["message_ts"])][digest] = message
    ambiguous, ordered = [], []
    for (channel, stamp), versions in identities.items():
        if len(versions) != 1:
            ambiguous.append({"channel_id": channel, "message_ts": stamp,
                              "observed_versions": len(versions)})
            continue
        message = dict(next(iter(versions.values())))
        if not message["permalink"] and workspace:
            message["permalink"] = f"{workspace}/archives/{channel}/p{stamp.replace('.', '')}"
        ordered.append(message)
    ordered.sort(key=lambda row: (int(row["message_ts"].split(".")[0]), row["message_ts"].split(".")[1], row["channel_id"]))
    operations = {}
    terminals, unparsed = [], []
    for message in ordered:
        statement = _statement(message["text"])
        if statement is None:
            if re.match(r"^(?:CLAIM|TAKE|RESUME|TAKING|LANDED|DONE|COMPLETED?|RELEASED?)\b", message["text"].lstrip(" *`\n"), re.I):
                unparsed.append({"channel_id": message["channel_id"], "message_ts": message["message_ts"], "permalink": message["permalink"]})
            continue
        kind, operation = statement
        reference = {key: message[key] for key in ("channel_id", "message_ts", "permalink", "source")}
        if kind == "declaration":
            row = operations.setdefault(operation, {"operation_id": operation,
                "observed_paths": [], "declarations": [], "terminal_observations": [],
                "state": "declaration_observed"})
            row["observed_paths"] = sorted(set(row["observed_paths"]) | set(_paths(message["text"])))
            row["declarations"].append(reference)
            row["state"] = "declaration_observed"
        else:
            terminal = {"operation_id": operation, "kind": kind, **reference}
            terminals.append(terminal)
            if operation in operations:
                operations[operation]["terminal_observations"].append(terminal)
                operations[operation]["state"] = "explicit_terminal_observed"
    by_path = defaultdict(list)
    for operation, row in operations.items():
        if row["state"] == "declaration_observed":
            for path in row["observed_paths"]:
                by_path[path].append(operation)
    overlaps = [{"path": path, "operation_ids": sorted(ops),
                 "declaration_links": sorted({declaration["permalink"] for op in ops
                    for declaration in operations[op]["declarations"] if declaration["permalink"]}),
                 "status": "possible_file_overlap"}
                for path, ops in sorted(by_path.items()) if len(ops) > 1]
    return {"schema": SCHEMA, "advisory_only": True,
        "scope": "Supplied Slack observations only. Declarations do not establish ownership; shared files can contain compatible work. Refresh the linked sources and existing ledger before acting.",
        "counts": {"messages_supplied": len(messages), "distinct_message_ids": len(identities),
                   "interpreted_message_ids": len(ordered), "operations": len(operations),
                   "declarations_without_exact_paths": sum(not row["observed_paths"] for row in operations.values()),
                   "possible_overlap_paths": len(overlaps), "unparsed_statement_headers": len(unparsed)},
        "coverage": {"provider_history_complete": False,
                     "basis": "Caller-supplied pages; terminal pages alone do not prove the history or all claims were supplied.",
                     "pages": pages, "pages_with_continuation": sum(page["terminal_page"] is False for page in pages),
                     "pages_with_unknown_pagination": sum(page["terminal_page"] is None for page in pages),
                     "ambiguous_message_versions": sorted(ambiguous, key=lambda row: (row["channel_id"], row["message_ts"])),
                     "unparsed_statement_headers": unparsed},
        "operations": [operations[key] for key in sorted(operations)],
        "terminal_observations": terminals,
        "possible_overlaps": overlaps,
        "unmatched_terminal_observations": [row for row in terminals if row["operation_id"] not in operations]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="Retained Slack JSON response paths; - reads stdin")
    parser.add_argument("--channel-id", help="Channel ID omitted by a native thread response")
    parser.add_argument("--workspace-url", help="Workspace root used to construct missing message links")
    args = parser.parse_args(argv)
    try:
        if args.inputs.count("-") > 1:
            raise ScanError("stdin can be read only once")
        if args.channel_id is not None:
            _channel(args.channel_id)
        _workspace(args.workspace_url)
        messages, pages, inputs = [], [], []
        for name in args.inputs:
            if name == "-":
                raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
            else:
                with Path(name).open("rb") as handle:
                    raw = handle.read(MAX_INPUT_BYTES + 1)
            if len(raw) > MAX_INPUT_BYTES:
                raise ScanError("input exceeds the 64 MiB per-response limit")
            rows, observed = read_responses(_load(raw), channel_id=args.channel_id, source=name)
            messages.extend(rows)
            pages.extend(observed)
            inputs.append({"source": name, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)})
        report = scan(messages, pages, workspace_url=args.workspace_url)
        report["inputs"] = inputs
        sys.stdout.write(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
        return 0
    except (ScanError, OSError, UnicodeError, RecursionError, ValueError) as exc:
        print("swarm-claim-scan: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
