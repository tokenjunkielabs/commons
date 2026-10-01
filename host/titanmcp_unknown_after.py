#!/usr/bin/env python3
"""Unique titanmcp list_messages unknown after= KEEP remainder.

Peer transcript-cursor land claimed unknown after= is an explicit error.
Live list_messages with a string after= that matches no message id is
HTTP 200 JSON, MCP ok:true, full transcript (same ids as omitting after),
not JSON-RPC error, not isError. Empty string after= is the same.
Wrong-type after= (null / 0) is MCP isError BAD_ARGUMENT argument=after,
not JSON-RPC -32602. Isolated classifier stays green without reminting
pad runtime, Latch titanmcp.html, setup-schema, SAVE/LOAD DRAFT, GET /mcp
identity, Origin pair, or list_messages cursor batteries. leftover
--bake/--deploy/--go REFUSED sent=0. No competition resubmission.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from typing import Any


ID = "cursor-titanmcp-unknown-after-20261001-01"
PAD_MCP = "https://webmcp-pad.vercel.app/mcp"
UNKNOWN_AFTER = "does-not-exist-cursor"
REFUSE = ("--send", "--apply", "--go", "--autopilot", "--live", "--checkout", "--deploy", "--bake")
DO_NOT_REMINT = (
    "api/mcp.py",
    "commons_mcp.py",
    "titanmcp.html",
    "webmcp.html",
    ".github/workflows/webmcp-pad-production.yml",
    "host/titanmcp_setup_schema.py",
    "host/titanmcp_save_load_draft.py",
    "host/titanmcp_get_mcp_identity.py",
    "host/titanmcp_origin_pair.py",
    "host/titanmcp_list_messages_cursor.py",
    "p/cursor-titanmcp-setup-schema-20260929-01.md",
    "p/cursor-titanmcp-save-load-draft-20260930-01.md",
    "p/cursor-titanmcp-get-mcp-identity-20261001-01.md",
    "p/cursor-titanmcp-origin-pair-20261001-01.md",
    "p/cursor-titanmcp-list-messages-cursor-20261001-01.md",
)


def structured_content(packet: dict[str, Any]) -> dict[str, Any]:
    result = packet.get("result")
    if not isinstance(result, dict):
        return {}
    sc = result.get("structuredContent")
    return sc if isinstance(sc, dict) else {}


def jsonrpc_error(packet: dict[str, Any]) -> dict[str, Any]:
    err = packet.get("error")
    return err if isinstance(err, dict) else {}


def message_ids(packet: dict[str, Any]) -> list[str]:
    sc = structured_content(packet)
    rows = sc.get("messages") if isinstance(sc.get("messages"), list) else []
    out: list[str] = []
    for row in rows:
        if isinstance(row, dict) and row.get("id"):
            out.append(str(row.get("id")))
    return out


def _rpc(obj: dict[str, Any]) -> dict[str, Any]:
    req = urllib.request.Request(
        PAD_MCP,
        data=json.dumps(obj).encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "MCP-Protocol-Version": "2025-03-26",
            "Origin": "https://chatgpt.com",
            "User-Agent": "titanmcp-unknown-after",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return {"status": resp.status, "packet": json.loads(resp.read().decode("utf-8"))}
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        try:
            packet = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            packet = {"raw": raw[:200].decode("utf-8", "replace")}
        return {"status": exc.code, "packet": packet}


def _call(name: str, arguments: dict[str, Any], request_id: int) -> dict[str, Any]:
    return _rpc(
        {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        }
    )


def classify_unknown_after(
    packet: dict[str, Any],
    status: int,
    *,
    baseline_ids: list[str],
) -> dict[str, Any]:
    err = jsonrpc_error(packet)
    result = packet.get("result") if isinstance(packet.get("result"), dict) else {}
    sc = structured_content(packet)
    ids = message_ids(packet)
    ok = (
        status == 200
        and not err
        and result.get("isError") is not True
        and sc.get("ok") is True
        and bool(ids)
        and ids == baseline_ids
        and err.get("code") != -32602
        and err.get("code") != -32700
    )
    return {
        "ok": ok,
        "status": status,
        "jsonrpc_code": err.get("code"),
        "is_error": result.get("isError"),
        "sc_ok": sc.get("ok"),
        "count": sc.get("count"),
        "ids": ids,
        "explicit_error_absent": not err and result.get("isError") is not True,
    }


def classify_wrong_type(packet: dict[str, Any], status: int) -> dict[str, Any]:
    err = jsonrpc_error(packet)
    result = packet.get("result") if isinstance(packet.get("result"), dict) else {}
    sc = structured_content(packet)
    ok = (
        status == 200
        and not err
        and result.get("isError") is True
        and sc.get("ok") is False
        and sc.get("error") == "BAD_ARGUMENT"
        and sc.get("argument") == "after"
        and "must be string" in str(sc.get("hint") or "")
        and err.get("code") != -32602
    )
    return {
        "ok": ok,
        "status": status,
        "jsonrpc_code": err.get("code"),
        "is_error": result.get("isError"),
        "error": sc.get("error"),
        "argument": sc.get("argument"),
        "hint": sc.get("hint"),
        "not_jsonrpc_32602": err.get("code") != -32602,
    }


def refuse_payload(flag: str) -> dict[str, Any]:
    return {
        "kind": "TITANMCP_UNKNOWN_AFTER",
        "id": ID,
        "refused": flag,
        "sent": 0,
        "cash": 0,
        "invented_stripe_urls": False,
        "verdict": "REFUSED",
        "note": (
            f"{flag} REFUSED. Did not remint pad runtime, titanmcp.html, "
            "setup-schema, SAVE/LOAD DRAFT, GET /mcp identity, Origin pair, "
            "or list_messages cursor KEEP. leftover bake/deploy sent=0."
        ),
    }


def measure() -> dict[str, Any]:
    errors: list[str] = []
    init = _rpc(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "titanmcp-unknown-after", "version": "1"},
            },
        }
    )
    info = ((init.get("packet") or {}).get("result") or {}).get("serverInfo") or {}
    if info.get("name") != "titanmcp" or info.get("version") != "1.4.5":
        errors.append("pad_mcp")

    created = _call("create_room", {"name": "cursor-unknown-after", "topic": "unknown-after"}, 2)
    room_id = structured_content(created.get("packet") or {}).get("room_id")
    if not room_id:
        errors.append("create_room")

    baseline = _call("list_messages", {"room_id": room_id, "limit": 50}, 3)
    baseline_ids = message_ids(baseline.get("packet") or {})
    if not baseline_ids:
        errors.append("baseline")

    unknown = _call(
        "list_messages",
        {"room_id": room_id, "after": UNKNOWN_AFTER, "limit": 50},
        4,
    )
    unknown_row = classify_unknown_after(
        unknown.get("packet") or {},
        unknown.get("status") or 0,
        baseline_ids=baseline_ids,
    )
    if not unknown_row["ok"]:
        errors.append("unknown_after")

    empty = _call("list_messages", {"room_id": room_id, "after": "", "limit": 50}, 5)
    empty_row = classify_unknown_after(
        empty.get("packet") or {},
        empty.get("status") or 0,
        baseline_ids=baseline_ids,
    )
    if not empty_row["ok"]:
        errors.append("empty_after")

    null_call = _call("list_messages", {"room_id": room_id, "after": None, "limit": 50}, 6)
    null_row = classify_wrong_type(null_call.get("packet") or {}, null_call.get("status") or 0)
    if not null_row["ok"]:
        errors.append("after_null")

    num_call = _call("list_messages", {"room_id": room_id, "after": 0, "limit": 50}, 7)
    num_row = classify_wrong_type(num_call.get("packet") or {}, num_call.get("status") or 0)
    if not num_row["ok"]:
        errors.append("after_num")

    return {
        "kind": "TITANMCP_UNKNOWN_AFTER",
        "id": ID,
        "pad_initialize": {"name": info.get("name"), "version": info.get("version")},
        "unknown_after": unknown_row,
        "empty_after": empty_row,
        "after_null": null_row,
        "after_num": num_row,
        "did_not_remint": list(DO_NOT_REMINT),
        "sent": 0,
        "cash": 0,
        "errors": errors,
        "verdict": "MATCH" if not errors else "FINDER-FAILED",
        "note": (
            "Unique remainder after list_messages cursor KEEP: unknown "
            "string after= is 200 ok:true full list, not an explicit error. "
            "Wrong-type after= is MCP isError BAD_ARGUMENT argument=after, "
            "not JSON-RPC -32602. No competition resubmission."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--json", action="store_true")
    args, unknown = parser.parse_known_args(argv)
    del args
    for flag in unknown:
        if flag in REFUSE:
            print(json.dumps(refuse_payload(flag), sort_keys=True))
            return 2
        if flag.startswith("-"):
            print(
                json.dumps(
                    {
                        "kind": "TITANMCP_UNKNOWN_AFTER",
                        "verdict": "FINDER-FAILED",
                        "sent": 0,
                        "unknown": flag,
                        "note": f"{flag} FINDER-FAILED, never silent 0.",
                    },
                    sort_keys=True,
                )
            )
            return 1
    packet = measure()
    print(json.dumps(packet, indent=2, sort_keys=True))
    return 0 if packet["verdict"] == "MATCH" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
