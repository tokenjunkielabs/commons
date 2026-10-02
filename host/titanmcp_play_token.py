#!/usr/bin/env python3
"""Unique titanmcp create_play_token KEEP remainder.

Live create_play_token with empty arguments is HTTP 200 JSON, MCP
ok:true, in-memory STUB_TOKEN, stripe:false, no Stripe charge.
Closed-schema extra property minutes is MCP isError BAD_ARGUMENT
argument=minutes hint arguments.minutes is not allowed, not JSON-RPC
-32602. Wrong-type plays string is MCP isError BAD_ARGUMENT
argument=plays hint arguments.plays must be integer, not JSON-RPC
-32602. Commons /mcp KEEP has no create_play_token. Isolated classifier
stays green without reminting pad runtime, Latch titanmcp.html,
setup-schema, SAVE/LOAD DRAFT, GET /mcp identity, Origin pair,
list_messages cursor, or unknown after= batteries. leftover
--bake/--deploy/--go REFUSED sent=0. No competition resubmission.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from typing import Any


ID = "cursor-titanmcp-play-token-20261002-01"
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
    "p/cursor-titanmcp-setup-schema-20260929-01.md",
    "p/cursor-titanmcp-save-load-draft-20260930-01.md",
    "p/cursor-titanmcp-get-mcp-identity-20261001-01.md",
    "p/cursor-titanmcp-origin-pair-20261001-01.md",
    "p/cursor-titanmcp-list-messages-cursor-20261001-01.md",
    "p/cursor-titanmcp-unknown-after-20261001-01.md",
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
        "User-Agent": "titanmcp-play-token",
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


def classify_mint(packet: dict[str, Any], status: int) -> dict[str, Any]:
    err = jsonrpc_error(packet)
    result = packet.get("result") if isinstance(packet.get("result"), dict) else {}
    sc = structured_content(packet)
    token = sc.get("token") if isinstance(sc.get("token"), dict) else {}
    subscription = sc.get("subscription") if isinstance(sc.get("subscription"), dict) else {}
    ok = (
        status == 200
        and not err
        and result.get("isError") is not True
        and sc.get("ok") is True
        and token.get("state") == "STUB_TOKEN"
        and token.get("kind") == "pay-per-play"
        and token.get("billing") == "in-memory"
        and token.get("stripe") is False
        and subscription.get("subscribed") is False
        and "No Stripe" in str(sc.get("note") or "")
        and err.get("code") != -32602
    )
    return {
        "ok": ok,
        "status": status,
        "jsonrpc_code": err.get("code"),
        "is_error": result.get("isError"),
        "sc_ok": sc.get("ok"),
        "state": token.get("state"),
        "kind": token.get("kind"),
        "billing": token.get("billing"),
        "stripe": token.get("stripe"),
        "subscribed": subscription.get("subscribed"),
        "token_id_omitted": True,
    }


def classify_extra_minutes(packet: dict[str, Any], status: int) -> dict[str, Any]:
    err = jsonrpc_error(packet)
    result = packet.get("result") if isinstance(packet.get("result"), dict) else {}
    sc = structured_content(packet)
    ok = (
        status == 200
        and not err
        and result.get("isError") is True
        and sc.get("ok") is False
        and sc.get("error") == "BAD_ARGUMENT"
        and sc.get("argument") == "minutes"
        and "is not allowed" in str(sc.get("hint") or "")
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


def classify_plays_string(packet: dict[str, Any], status: int) -> dict[str, Any]:
    err = jsonrpc_error(packet)
    result = packet.get("result") if isinstance(packet.get("result"), dict) else {}
    sc = structured_content(packet)
    ok = (
        status == 200
        and not err
        and result.get("isError") is True
        and sc.get("ok") is False
        and sc.get("error") == "BAD_ARGUMENT"
        and sc.get("argument") == "plays"
        and "must be integer" in str(sc.get("hint") or "")
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
        "kind": "TITANMCP_PLAY_TOKEN",
        "id": ID,
        "refused": flag,
        "sent": 0,
        "cash": 0,
        "invented_stripe_urls": False,
        "verdict": "REFUSED",
        "note": (
            f"{flag} REFUSED. Did not remint pad runtime, titanmcp.html, "
            "setup-schema, SAVE/LOAD DRAFT, GET /mcp identity, Origin pair, "
            "list_messages cursor, or unknown after= KEEP. leftover bake/deploy sent=0."
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
                "clientInfo": {"name": "titanmcp-play-token", "version": "1"},
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
    if "create_play_token" not in names:
        errors.append("pad_tool")

    mint = _call("create_play_token", {}, 3)
    mint_row = classify_mint(mint.get("packet") or {}, mint.get("status") or 0)
    if not mint_row["ok"]:
        errors.append("mint")

    extra = _call("create_play_token", {"minutes": 1}, 4)
    extra_row = classify_extra_minutes(extra.get("packet") or {}, extra.get("status") or 0)
    if not extra_row["ok"]:
        errors.append("extra_minutes")

    wrong = _call("create_play_token", {"plays": "1"}, 5)
    wrong_row = classify_plays_string(wrong.get("packet") or {}, wrong.get("status") or 0)
    if not wrong_row["ok"]:
        errors.append("plays_string")

    commons_init = _rpc(
        COMMONS_MCP,
        {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "titanmcp-play-token", "version": "1"},
            },
        },
        origin="",
    )
    commons_info = ((commons_init.get("packet") or {}).get("result") or {}).get("serverInfo") or {}
    commons_listed = _rpc(
        COMMONS_MCP,
        {"jsonrpc": "2.0", "id": 7, "method": "tools/list", "params": {}},
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
        or "create_play_token" in commons_names
    ):
        errors.append("commons_keep")

    return {
        "kind": "TITANMCP_PLAY_TOKEN",
        "id": ID,
        "pad_initialize": {"name": info.get("name"), "version": info.get("version")},
        "commons_initialize": {
            "name": commons_info.get("name"),
            "version": commons_info.get("version"),
        },
        "pad_has_create_play_token": "create_play_token" in names,
        "commons_has_create_play_token": "create_play_token" in commons_names,
        "mint": mint_row,
        "extra_minutes": extra_row,
        "plays_string": wrong_row,
        "did_not_remint": list(DO_NOT_REMINT),
        "sent": 0,
        "cash": 0,
        "errors": errors,
        "verdict": "MATCH" if not errors else "FINDER-FAILED",
        "note": (
            "Unique remainder after unknown after= KEEP: create_play_token "
            "empty args is 200 ok:true STUB_TOKEN stripe:false. Extra minutes "
            "is MCP isError BAD_ARGUMENT is not allowed, not JSON-RPC -32602. "
            "Wrong-type plays is BAD_ARGUMENT must be integer, not -32602. "
            "Commons /mcp KEEP has no create_play_token. No competition resubmission."
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
                        "kind": "TITANMCP_PLAY_TOKEN",
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
