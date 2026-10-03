#!/usr/bin/env python3
"""Unique titanmcp MESSAGE_CURSOR_NOT_FOUND KEEP remainder.

GET /mcp HTML hashes KEEP. Live list_messages with a string after= that
matches no message id reminted: HTTP 200 MCP isError
MESSAGE_CURSOR_NOT_FOUND with retained_count, not a full transcript, not
JSON-RPC -32602/-32700. Empty string after= still ok:true. Wrong-type
after= still BAD_ARGUMENT argument=after. assignment_result bubbles now
carry id. Isolated classifier stays green without reminting pad runtime,
Latch titanmcp.html, setup-schema, SAVE/LOAD DRAFT, GET /mcp identity,
Origin pair, or the prior list_messages cursor / unknown after= KEEP
files. leftover --bake/--deploy/--go REFUSED sent=0. No competition
resubmission.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from typing import Any


ID = "cursor-titanmcp-message-cursor-not-found-20261003-01"
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
    "host/titanmcp_unknown_after.py",
    "host/titanmcp_play_token.py",
    "host/titanmcp_consent_attach.py",
    "host/titanmcp_get_operator.py",
    "p/cursor-titanmcp-setup-schema-20260929-01.md",
    "p/cursor-titanmcp-save-load-draft-20260930-01.md",
    "p/cursor-titanmcp-get-mcp-identity-20261001-01.md",
    "p/cursor-titanmcp-origin-pair-20261001-01.md",
    "p/cursor-titanmcp-list-messages-cursor-20261001-01.md",
    "p/cursor-titanmcp-unknown-after-20261001-01.md",
    "p/cursor-titanmcp-play-token-20261002-01.md",
    "p/cursor-titanmcp-consent-attach-20261002-01.md",
    "p/cursor-titanmcp-get-operator-20261002-01.md",
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
            "User-Agent": "titanmcp-message-cursor-not-found",
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


def classify_unknown(packet: dict[str, Any], status: int) -> dict[str, Any]:
    err = jsonrpc_error(packet)
    result = packet.get("result") if isinstance(packet.get("result"), dict) else {}
    sc = structured_content(packet)
    ok = (
        status == 200
        and not err
        and result.get("isError") is True
        and sc.get("ok") is False
        and sc.get("error") == "MESSAGE_CURSOR_NOT_FOUND"
        and isinstance(sc.get("retained_count"), int)
        and sc.get("retained_count") >= 1
        and bool(sc.get("oldest_available_message_id"))
        and bool(sc.get("latest_available_message_id"))
        and err.get("code") != -32602
        and err.get("code") != -32700
        and not sc.get("messages")
    )
    return {
        "ok": ok,
        "status": status,
        "jsonrpc_code": err.get("code"),
        "is_error": result.get("isError"),
        "error": sc.get("error"),
        "retained_count": sc.get("retained_count"),
        "not_jsonrpc_32602": err.get("code") != -32602,
        "not_full_list": not sc.get("messages"),
    }


def classify_empty(packet: dict[str, Any], status: int) -> dict[str, Any]:
    err = jsonrpc_error(packet)
    result = packet.get("result") if isinstance(packet.get("result"), dict) else {}
    sc = structured_content(packet)
    ok = (
        status == 200
        and not err
        and result.get("isError") is not True
        and sc.get("ok") is True
        and sc.get("has_more") is False
        and bool(sc.get("next_after"))
        and isinstance(sc.get("omitted_before_count"), int)
    )
    return {
        "ok": ok,
        "status": status,
        "jsonrpc_code": err.get("code"),
        "is_error": result.get("isError"),
        "sc_ok": sc.get("ok"),
        "has_more": sc.get("has_more"),
        "next_after_present": bool(sc.get("next_after")),
        "omitted_before_count": sc.get("omitted_before_count"),
    }


def classify_assignment_ids(packet: dict[str, Any], status: int) -> dict[str, Any]:
    err = jsonrpc_error(packet)
    result = packet.get("result") if isinstance(packet.get("result"), dict) else {}
    sc = structured_content(packet)
    messages = sc.get("messages") if isinstance(sc.get("messages"), list) else []
    bubbles = [
        row for row in messages if isinstance(row, dict) and row.get("kind") == "assignment_result"
    ]
    bubble = bubbles[-1] if bubbles else {}
    coords = [row for row in messages if isinstance(row, dict) and "COORD RESULT" in str(row.get("text") or "")]
    coord = coords[-1] if coords else {}
    ok = (
        status == 200
        and not err
        and result.get("isError") is not True
        and sc.get("ok") is True
        and err.get("code") != -32700
        and bool(coord.get("id"))
        and bubbles
        and bool(bubble.get("id"))
    )
    return {
        "ok": ok,
        "status": status,
        "jsonrpc_code": err.get("code"),
        "is_error": result.get("isError"),
        "coord_result_id_present": bool(coord.get("id")),
        "assignment_result_has_id": bool(bubble.get("id")),
        "keyerror_absent": err.get("code") != -32700,
    }


def refuse_payload(flag: str) -> dict[str, Any]:
    return {
        "kind": "TITANMCP_MESSAGE_CURSOR_NOT_FOUND",
        "id": ID,
        "refused": flag,
        "sent": 0,
        "cash": 0,
        "invented_stripe_urls": False,
        "verdict": "REFUSED",
        "note": (
            f"{flag} REFUSED. Did not remint pad runtime, titanmcp.html, "
            "setup-schema, SAVE/LOAD DRAFT, GET /mcp identity, Origin pair, "
            "list_messages cursor KEEP file, or unknown after= KEEP file. "
            "leftover bake/deploy sent=0."
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
                "clientInfo": {"name": "titanmcp-message-cursor-not-found", "version": "1"},
            },
        }
    )
    info = ((init.get("packet") or {}).get("result") or {}).get("serverInfo") or {}
    if info.get("name") != "titanmcp" or info.get("version") != "1.4.5":
        errors.append("pad_mcp")

    created = _call("create_room", {"name": "cursor-cursor-not-found", "topic": "cursor-not-found"}, 2)
    room_id = structured_content(created.get("packet") or {}).get("room_id")
    if not room_id:
        errors.append("create_room")

    unknown = _call("list_messages", {"room_id": room_id, "after": UNKNOWN_AFTER, "limit": 50}, 3)
    unknown_row = classify_unknown(unknown.get("packet") or {}, unknown.get("status") or 0)
    if not unknown_row["ok"]:
        errors.append("unknown_after")

    empty = _call("list_messages", {"room_id": room_id, "after": "", "limit": 50}, 4)
    empty_row = classify_empty(empty.get("packet") or {}, empty.get("status") or 0)
    if not empty_row["ok"]:
        errors.append("empty_after")

    submitted = _call("submit_task", {"room_id": room_id, "task": "do the piece"}, 5)
    task_id = (structured_content(submitted.get("packet") or {}).get("task") or {}).get("task_id")
    planned = _call(
        "plan_task",
        {"room_id": room_id, "task_id": task_id, "pieces": ["one piece of work"]},
        6,
    )
    pieces = structured_content(planned.get("packet") or {}).get("pieces") or []
    piece_id = pieces[0].get("piece_id") if pieces and isinstance(pieces[0], dict) else None
    _call("invite_agent", {"room_id": room_id, "agent_name": "peer-worker", "role": "builder"}, 7)
    assigned = _call(
        "assign_piece",
        {"room_id": room_id, "piece_id": piece_id, "agent_name": "peer-worker"},
        8,
    )
    assignment_id = (structured_content(assigned.get("packet") or {}).get("assignment") or {}).get(
        "assignment_id"
    )
    claimed = _call(
        "claim_assignment",
        {"room_id": room_id, "assignment_id": assignment_id, "agent_name": "peer-worker"},
        9,
    )
    token = structured_content(claimed.get("packet") or {}).get("claim_token")
    _call(
        "report_assignment_result",
        {
            "room_id": room_id,
            "assignment_id": assignment_id,
            "agent_name": "peer-worker",
            "result": "landed piece",
            "claim_token": token,
            "status": "done",
        },
        10,
    )
    listed = _call("list_messages", {"room_id": room_id, "limit": 50}, 11)
    listed_row = classify_assignment_ids(listed.get("packet") or {}, listed.get("status") or 0)
    if not listed_row["ok"]:
        errors.append("assignment_result_id")

    return {
        "kind": "TITANMCP_MESSAGE_CURSOR_NOT_FOUND",
        "id": ID,
        "pad_initialize": {"name": info.get("name"), "version": info.get("version")},
        "unknown_after": unknown_row,
        "empty_after": empty_row,
        "assignment_result_id": listed_row,
        "did_not_remint": list(DO_NOT_REMINT),
        "sent": 0,
        "cash": 0,
        "errors": errors,
        "verdict": "MATCH" if not errors else "FINDER-FAILED",
        "note": (
            "Unique remainder after helper deploy SHIP: unknown string after= "
            "is MCP isError MESSAGE_CURSOR_NOT_FOUND, not a full list, not "
            "JSON-RPC -32602. assignment_result now has id. GET /mcp hashes "
            "KEEP. Did not remint prior KEEP files. No competition resubmission."
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
                        "kind": "TITANMCP_MESSAGE_CURSOR_NOT_FOUND",
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
