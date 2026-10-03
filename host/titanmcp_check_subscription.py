#!/usr/bin/env python3
"""Unique titanmcp check_subscription KEEP remainder.

Live check_subscription with empty arguments is HTTP 200 JSON, MCP
ok:true, in-memory stub, subscribed:false, stripe:false, tokens count 0,
no Stripe charge. Closed-schema extra properties minutes, plays,
subscribed, and room_id are MCP isError BAD_ARGUMENT hint arguments.<name>
is not allowed, not JSON-RPC -32602. Integer plays is not allowed (not
create_play_token must-be-integer). Commons /mcp KEEP has no
check_subscription. Isolated classifier stays green without reminting
pad runtime, Latch titanmcp.html, setup-schema, SAVE/LOAD DRAFT, GET
/mcp identity, Origin pair, list_messages cursor, unknown after=,
create_play_token, consent-attach, get_operator, MESSAGE_CURSOR_NOT_FOUND,
or get_connector batteries. leftover --bake/--deploy/--go REFUSED
sent=0. No competition resubmission.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from typing import Any


ID = "cursor-titanmcp-check-subscription-20261003-01"
PAD_MCP = "https://webmcp-pad.vercel.app/mcp"
COMMONS_MCP = "https://commons-spark-mcp.vercel.app/mcp"
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
    "host/titanmcp_message_cursor_not_found.py",
    "host/titanmcp_get_connector.py",
    "p/cursor-titanmcp-setup-schema-20260929-01.md",
    "p/cursor-titanmcp-save-load-draft-20260930-01.md",
    "p/cursor-titanmcp-get-mcp-identity-20261001-01.md",
    "p/cursor-titanmcp-origin-pair-20261001-01.md",
    "p/cursor-titanmcp-list-messages-cursor-20261001-01.md",
    "p/cursor-titanmcp-unknown-after-20261001-01.md",
    "p/cursor-titanmcp-play-token-20261002-01.md",
    "p/cursor-titanmcp-consent-attach-20261002-01.md",
    "p/cursor-titanmcp-get-operator-20261002-01.md",
    "p/cursor-titanmcp-message-cursor-not-found-20261003-01.md",
    "p/cursor-titanmcp-get-connector-20261003-01.md",
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


def _rpc(url: str, obj: dict[str, Any], *, origin: str = "https://chatgpt.com") -> dict[str, Any]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "MCP-Protocol-Version": "2025-03-26",
        "User-Agent": "titanmcp-check-subscription",
    }
    if origin:
        headers["Origin"] = origin
    req = urllib.request.Request(
        url,
        data=json.dumps(obj).encode("utf-8"),
        method="POST",
        headers=headers,
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
        PAD_MCP,
        {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        },
    )


def classify_empty(packet: dict[str, Any], status: int) -> dict[str, Any]:
    err = jsonrpc_error(packet)
    result = packet.get("result") if isinstance(packet.get("result"), dict) else {}
    sc = structured_content(packet)
    subscription = sc.get("subscription") if isinstance(sc.get("subscription"), dict) else {}
    tokens = sc.get("tokens") if isinstance(sc.get("tokens"), dict) else {}
    note = str(subscription.get("note") or "")
    ok = (
        status == 200
        and not err
        and result.get("isError") is not True
        and sc.get("ok") is True
        and sc.get("stripe") is False
        and sc.get("style") == "pay-per-play"
        and sc.get("model") == "subscription+api_tokens"
        and subscription.get("subscribed") is False
        and subscription.get("stripe") is False
        and subscription.get("billing") == "in-memory"
        and subscription.get("plan") == "none"
        and subscription.get("status") == "inactive"
        and subscription.get("subject") == "anonymous"
        and tokens.get("count") == 0
        and tokens.get("plays_remaining") == 0
        and "No subscription on file" in note
        and "Stub only" in note
        and err.get("code") != -32602
    )
    return {
        "ok": ok,
        "status": status,
        "jsonrpc_code": err.get("code"),
        "is_error": result.get("isError"),
        "sc_ok": sc.get("ok"),
        "stripe": sc.get("stripe"),
        "style": sc.get("style"),
        "model": sc.get("model"),
        "subscribed": subscription.get("subscribed"),
        "subscription_stripe": subscription.get("stripe"),
        "billing": subscription.get("billing"),
        "plan": subscription.get("plan"),
        "status_label": subscription.get("status"),
        "subject": subscription.get("subject"),
        "token_count": tokens.get("count"),
        "plays_remaining": tokens.get("plays_remaining"),
        "updated_at_omitted": True,
    }


def classify_not_allowed(packet: dict[str, Any], status: int, argument: str) -> dict[str, Any]:
    err = jsonrpc_error(packet)
    result = packet.get("result") if isinstance(packet.get("result"), dict) else {}
    sc = structured_content(packet)
    hint = str(sc.get("hint") or "")
    ok = (
        status == 200
        and not err
        and result.get("isError") is True
        and sc.get("ok") is False
        and sc.get("error") == "BAD_ARGUMENT"
        and sc.get("argument") == argument
        and f"arguments.{argument} is not allowed" in hint
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
        "kind": "TITANMCP_CHECK_SUBSCRIPTION",
        "id": ID,
        "refused": flag,
        "sent": 0,
        "cash": 0,
        "invented_stripe_urls": False,
        "verdict": "REFUSED",
        "note": (
            f"{flag} REFUSED. Did not remint pad runtime, titanmcp.html, "
            "setup-schema, SAVE/LOAD DRAFT, GET /mcp identity, Origin pair, "
            "list_messages cursor, unknown after=, create_play_token, "
            "consent-attach, get_operator, MESSAGE_CURSOR_NOT_FOUND, or "
            "get_connector KEEP. leftover bake/deploy sent=0."
        ),
    }


def measure() -> dict[str, Any]:
    errors: list[str] = []
    init = _rpc(
        PAD_MCP,
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "titanmcp-check-subscription", "version": "1"},
            },
        },
    )
    info = ((init.get("packet") or {}).get("result") or {}).get("serverInfo") or {}
    if info.get("name") != "titanmcp" or info.get("version") != "1.4.5":
        errors.append("pad_mcp")

    listed = _rpc(PAD_MCP, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    names = [
        row.get("name")
        for row in ((listed.get("packet") or {}).get("result") or {}).get("tools") or []
        if isinstance(row, dict)
    ]
    if "check_subscription" not in names:
        errors.append("pad_tool")

    empty = _call("check_subscription", {}, 3)
    empty_row = classify_empty(empty.get("packet") or {}, empty.get("status") or 0)
    if not empty_row["ok"]:
        errors.append("empty")

    extra_minutes = _call("check_subscription", {"minutes": 1}, 4)
    extra_minutes_row = classify_not_allowed(
        extra_minutes.get("packet") or {}, extra_minutes.get("status") or 0, "minutes"
    )
    if not extra_minutes_row["ok"]:
        errors.append("extra_minutes")

    extra_plays = _call("check_subscription", {"plays": 1}, 5)
    extra_plays_row = classify_not_allowed(
        extra_plays.get("packet") or {}, extra_plays.get("status") or 0, "plays"
    )
    if not extra_plays_row["ok"]:
        errors.append("extra_plays")

    extra_subscribed = _call("check_subscription", {"subscribed": True}, 6)
    extra_subscribed_row = classify_not_allowed(
        extra_subscribed.get("packet") or {}, extra_subscribed.get("status") or 0, "subscribed"
    )
    if not extra_subscribed_row["ok"]:
        errors.append("extra_subscribed")

    extra_room = _call("check_subscription", {"room_id": "x"}, 7)
    extra_room_row = classify_not_allowed(
        extra_room.get("packet") or {}, extra_room.get("status") or 0, "room_id"
    )
    if not extra_room_row["ok"]:
        errors.append("extra_room_id")

    commons_init = _rpc(
        COMMONS_MCP,
        {
            "jsonrpc": "2.0",
            "id": 8,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "titanmcp-check-subscription", "version": "1"},
            },
        },
        origin="",
    )
    commons_info = ((commons_init.get("packet") or {}).get("result") or {}).get("serverInfo") or {}
    commons_listed = _rpc(
        COMMONS_MCP,
        {"jsonrpc": "2.0", "id": 9, "method": "tools/list", "params": {}},
        origin="",
    )
    commons_names = [
        row.get("name")
        for row in ((commons_listed.get("packet") or {}).get("result") or {}).get("tools") or []
        if isinstance(row, dict)
    ]
    if (
        commons_info.get("name") != "commons"
        or commons_info.get("version") != "1.4.0"
        or "check_subscription" in commons_names
    ):
        errors.append("commons_keep")

    return {
        "kind": "TITANMCP_CHECK_SUBSCRIPTION",
        "id": ID,
        "pad_initialize": {"name": info.get("name"), "version": info.get("version")},
        "commons_initialize": {
            "name": commons_info.get("name"),
            "version": commons_info.get("version"),
        },
        "pad_has_check_subscription": "check_subscription" in names,
        "commons_has_check_subscription": "check_subscription" in commons_names,
        "empty_arguments": empty_row,
        "extra_minutes": extra_minutes_row,
        "extra_plays": extra_plays_row,
        "extra_subscribed": extra_subscribed_row,
        "extra_room_id": extra_room_row,
        "did_not_remint": list(DO_NOT_REMINT),
        "sent": 0,
        "cash": 0,
        "errors": errors,
        "verdict": "MATCH" if not errors else "FINDER-FAILED",
        "note": (
            "Unique remainder after get_connector KEEP: check_subscription "
            "empty arguments is 200 ok:true in-memory stub subscribed:false "
            "stripe:false tokens count 0. Extra minutes/plays/subscribed/"
            "room_id are MCP isError BAD_ARGUMENT is not allowed, not JSON-RPC "
            "-32602. Integer plays is not allowed. Commons /mcp KEEP has no "
            "check_subscription. No competition resubmission."
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
                        "kind": "TITANMCP_CHECK_SUBSCRIPTION",
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
