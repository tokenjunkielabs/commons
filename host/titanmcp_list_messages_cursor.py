#!/usr/bin/env python3
"""Unique titanmcp list_messages cursor KEEP remainder.

Peer webmcp-pad squash-merged transcript cursor work to pad main. Live
list_messages after report_assignment_result is HTTP 200 JSON, not
JSON-RPC -32700 Parse error KeyError. COORD RESULT rows carry id.
The assignment_result bubble is still listed without id; list_messages
still succeeds. Isolated classifier stays green without reminting pad
runtime, Latch titanmcp.html, setup-schema, SAVE/LOAD DRAFT, GET /mcp
identity, or Origin pair batteries. leftover --bake/--deploy/--go
REFUSED sent=0. No competition resubmission.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from typing import Any


ID = "cursor-titanmcp-list-messages-cursor-20261001-01"
PAD_MCP = "https://webmcp-pad.vercel.app/mcp"
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
    "p/cursor-titanmcp-setup-schema-20260929-01.md",
    "p/cursor-titanmcp-save-load-draft-20260930-01.md",
    "p/cursor-titanmcp-get-mcp-identity-20261001-01.md",
    "p/cursor-titanmcp-origin-pair-20261001-01.md",
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
            "User-Agent": "titanmcp-list-messages-cursor",
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


def classify_list_after_result(packet: dict[str, Any], status: int) -> dict[str, Any]:
    err = jsonrpc_error(packet)
    result = packet.get("result") if isinstance(packet.get("result"), dict) else {}
    sc = structured_content(packet)
    messages = sc.get("messages") if isinstance(sc.get("messages"), list) else []
    ids = [row.get("id") for row in messages if isinstance(row, dict)]
    result_rows = [
        row
        for row in messages
        if isinstance(row, dict) and "COORD RESULT" in str(row.get("text") or "")
    ]
    bubbles = [
        row
        for row in messages
        if isinstance(row, dict) and row.get("kind") == "assignment_result"
    ]
    bubble = bubbles[-1] if bubbles else {}
    coord = result_rows[-1] if result_rows else {}
    not_keyerror = err.get("code") != -32700 and "KeyError" not in json.dumps(packet)
    ok = (
        status == 200
        and not err
        and result.get("isError") is not True
        and sc.get("ok") is True
        and not_keyerror
        and bool(coord.get("id"))
        and bubbles
        and not bubble.get("id")
    )
    return {
        "ok": ok,
        "status": status,
        "jsonrpc_code": err.get("code"),
        "is_error": result.get("isError"),
        "count": sc.get("count"),
        "message_ids_present": sum(1 for item in ids if item),
        "message_ids_missing": sum(1 for item in ids if not item),
        "coord_result_id": coord.get("id"),
        "assignment_result_kind": bubble.get("kind"),
        "assignment_result_has_id": bool(bubble.get("id")),
        "keyerror_absent": not_keyerror,
    }


def classify_after_cursor(packet: dict[str, Any], status: int) -> dict[str, Any]:
    err = jsonrpc_error(packet)
    sc = structured_content(packet)
    messages = sc.get("messages") if isinstance(sc.get("messages"), list) else []
    leftover = [
        row
        for row in messages
        if isinstance(row, dict) and row.get("kind") == "assignment_result" and not row.get("id")
    ]
    ok = (
        status == 200
        and not err
        and sc.get("ok") is True
        and err.get("code") != -32700
        and leftover == messages
    )
    return {
        "ok": ok,
        "status": status,
        "count": sc.get("count"),
        "jsonrpc_code": err.get("code"),
        "leftover_assignment_result_without_id": len(leftover),
    }


def refuse_payload(flag: str) -> dict[str, Any]:
    return {
        "kind": "TITANMCP_LIST_MESSAGES_CURSOR",
        "id": ID,
        "refused": flag,
        "sent": 0,
        "cash": 0,
        "invented_stripe_urls": False,
        "verdict": "REFUSED",
        "note": (
            f"{flag} REFUSED. Did not remint pad runtime, titanmcp.html, "
            "setup-schema, SAVE/LOAD DRAFT, GET /mcp identity, or Origin pair KEEP. "
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
                "clientInfo": {"name": "titanmcp-list-messages-cursor", "version": "1"},
            },
        }
    )
    info = ((init.get("packet") or {}).get("result") or {}).get("serverInfo") or {}
    if info.get("name") != "titanmcp" or info.get("version") != "1.4.5":
        errors.append("pad_mcp")

    created = _call("create_room", {"name": "cursor-list-cursor", "topic": "list-cursor"}, 2)
    room_id = structured_content(created.get("packet") or {}).get("room_id")
    if not room_id:
        errors.append("create_room")

    submitted = _call("submit_task", {"room_id": room_id, "task": "do the piece"}, 3)
    task_id = ((structured_content(submitted.get("packet") or {}).get("task") or {}).get("task_id"))
    planned = _call(
        "plan_task",
        {"room_id": room_id, "task_id": task_id, "pieces": ["one piece of work"]},
        4,
    )
    pieces = structured_content(planned.get("packet") or {}).get("pieces") or []
    piece_id = pieces[0].get("piece_id") if pieces and isinstance(pieces[0], dict) else None
    _call("invite_agent", {"room_id": room_id, "agent_name": "peer-worker", "role": "builder"}, 5)
    assigned = _call(
        "assign_piece",
        {"room_id": room_id, "piece_id": piece_id, "agent_name": "peer-worker"},
        6,
    )
    assignment_id = (structured_content(assigned.get("packet") or {}).get("assignment") or {}).get(
        "assignment_id"
    )
    claimed = _call(
        "claim_assignment",
        {"room_id": room_id, "assignment_id": assignment_id, "agent_name": "peer-worker"},
        7,
    )
    token = structured_content(claimed.get("packet") or {}).get("claim_token")
    reported = _call(
        "report_assignment_result",
        {
            "room_id": room_id,
            "assignment_id": assignment_id,
            "agent_name": "peer-worker",
            "result": "landed piece",
            "claim_token": token,
            "status": "done",
        },
        8,
    )
    listed = _call("list_messages", {"room_id": room_id, "limit": 50}, 9)
    after_result = classify_list_after_result(listed.get("packet") or {}, listed.get("status") or 0)
    if not after_result["ok"]:
        errors.append("list_after_result")

    cursor_id = after_result.get("coord_result_id")
    after = _call("list_messages", {"room_id": room_id, "after": cursor_id, "limit": 50}, 10)
    after_row = classify_after_cursor(after.get("packet") or {}, after.get("status") or 0)
    if not after_row["ok"]:
        errors.append("after_coord_result")

    return {
        "kind": "TITANMCP_LIST_MESSAGES_CURSOR",
        "id": ID,
        "pad_initialize": {"name": info.get("name"), "version": info.get("version")},
        "report_ok": structured_content(reported.get("packet") or {}).get("ok") is True,
        "list_after_result": after_result,
        "after_coord_result": after_row,
        "did_not_remint": list(DO_NOT_REMINT),
        "sent": 0,
        "cash": 0,
        "errors": errors,
        "verdict": "MATCH" if not errors else "FINDER-FAILED",
        "note": (
            "Unique remainder after pad transcript-cursor land: list_messages "
            "after report_assignment_result is 200 not JSON-RPC -32700; COORD "
            "RESULT has id; assignment_result bubble still has no id. "
            "No competition resubmission."
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
                        "kind": "TITANMCP_LIST_MESSAGES_CURSOR",
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
