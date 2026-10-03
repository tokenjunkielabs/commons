#!/usr/bin/env python3
"""Unique titanmcp list_connectors KEEP remainder.

Live list_connectors with empty arguments is HTTP 200 JSON, MCP ok:true,
catalog_count 500, default returned_count 50, matches 500, oauth_secrets
false, policy closed-door. q=github and query=github each return the
catalog GitHub row while catalog_count stays 500. q takes precedence
over query. Wrong-type q is MCP isError BAD_ARGUMENT hint arguments.q
must be string, not JSON-RPC -32602. Closed-schema extra minutes is MCP
isError BAD_ARGUMENT hint arguments.minutes is not allowed. limit=1
returns one row and still catalog_count 500. Commons /mcp KEEP has no
list_connectors. Isolated classifier stays green without reminting pad
runtime, Latch titanmcp.html, setup-schema, SAVE/LOAD DRAFT, GET /mcp
identity, Origin pair, list_messages cursor, unknown after=,
create_play_token, consent-attach, get_operator, MESSAGE_CURSOR_NOT_FOUND,
get_connector, or check_subscription batteries. leftover --bake/--deploy/--go
REFUSED sent=0. No competition resubmission.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from typing import Any


ID = "cursor-titanmcp-list-connectors-20261003-01"
PAD_MCP = "https://webmcp-pad.vercel.app/mcp"
COMMONS_MCP = "https://commons-spark-mcp.vercel.app/mcp"
REFUSE = ("--send", "--apply", "--go", "--autopilot", "--live", "--checkout", "--deploy", "--bake")
FEATURED = (
    "browser_computer_use",
    "desktop_computer_use",
    "facebook",
    "figma",
    "github",
    "lda_pfc_instruments",
    "notion",
    "openai",
    "shopify",
    "slack",
    "stripe",
    "vercel",
    "x",
)
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
    "host/titanmcp_check_subscription.py",
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
    "p/cursor-titanmcp-check-subscription-20261003-01.md",
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
        "User-Agent": "titanmcp-list-connectors",
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
    featured = sc.get("featured") if isinstance(sc.get("featured"), list) else []
    connectors = sc.get("connectors") if isinstance(sc.get("connectors"), list) else []
    ok = (
        status == 200
        and not err
        and result.get("isError") is not True
        and sc.get("ok") is True
        and sc.get("catalog_count") == 500
        and sc.get("returned_count") == 50
        and sc.get("count") == 50
        and sc.get("matches") == 500
        and sc.get("match_count") == 500
        and sc.get("oauth_secrets") is False
        and sc.get("policy") == "closed-door"
        and sc.get("catalog_source") == "connectors/catalog.json"
        and sc.get("tab") == "Agent Resources"
        and tuple(featured) == FEATURED
        and len(connectors) == 50
        and err.get("code") != -32602
    )
    return {
        "ok": ok,
        "status": status,
        "jsonrpc_code": err.get("code"),
        "is_error": result.get("isError"),
        "sc_ok": sc.get("ok"),
        "catalog_count": sc.get("catalog_count"),
        "returned_count": sc.get("returned_count"),
        "matches": sc.get("matches"),
        "oauth_secrets": sc.get("oauth_secrets"),
        "policy": sc.get("policy"),
        "catalog_source": sc.get("catalog_source"),
        "featured_count": len(featured),
        "not_jsonrpc_32602": err.get("code") != -32602,
    }


def classify_github_search(packet: dict[str, Any], status: int) -> dict[str, Any]:
    err = jsonrpc_error(packet)
    result = packet.get("result") if isinstance(packet.get("result"), dict) else {}
    sc = structured_content(packet)
    connectors = sc.get("connectors") if isinstance(sc.get("connectors"), list) else []
    first = connectors[0] if connectors and isinstance(connectors[0], dict) else {}
    ok = (
        status == 200
        and not err
        and result.get("isError") is not True
        and sc.get("ok") is True
        and sc.get("catalog_count") == 500
        and sc.get("returned_count") == 1
        and sc.get("count") == 1
        and sc.get("matches") == 1
        and sc.get("oauth_secrets") is False
        and first.get("id") == "github"
        and first.get("name") == "GitHub"
        and first.get("category") == "code"
        and first.get("oauth") == "stub"
        and first.get("status") == "catalog"
        and err.get("code") != -32602
    )
    return {
        "ok": ok,
        "status": status,
        "jsonrpc_code": err.get("code"),
        "is_error": result.get("isError"),
        "sc_ok": sc.get("ok"),
        "catalog_count": sc.get("catalog_count"),
        "returned_count": sc.get("returned_count"),
        "matches": sc.get("matches"),
        "first_id": first.get("id"),
        "first_oauth": first.get("oauth"),
        "not_jsonrpc_32602": err.get("code") != -32602,
    }


def classify_limit_one(packet: dict[str, Any], status: int) -> dict[str, Any]:
    err = jsonrpc_error(packet)
    result = packet.get("result") if isinstance(packet.get("result"), dict) else {}
    sc = structured_content(packet)
    connectors = sc.get("connectors") if isinstance(sc.get("connectors"), list) else []
    ok = (
        status == 200
        and not err
        and result.get("isError") is not True
        and sc.get("ok") is True
        and sc.get("catalog_count") == 500
        and sc.get("returned_count") == 1
        and sc.get("count") == 1
        and sc.get("matches") == 500
        and sc.get("match_count") == 500
        and sc.get("oauth_secrets") is False
        and len(connectors) == 1
        and err.get("code") != -32602
    )
    return {
        "ok": ok,
        "status": status,
        "jsonrpc_code": err.get("code"),
        "is_error": result.get("isError"),
        "sc_ok": sc.get("ok"),
        "catalog_count": sc.get("catalog_count"),
        "returned_count": sc.get("returned_count"),
        "matches": sc.get("matches"),
        "not_jsonrpc_32602": err.get("code") != -32602,
    }


def classify_must_be_string(packet: dict[str, Any], status: int, argument: str) -> dict[str, Any]:
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
        and f"arguments.{argument} must be string" in hint
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
        "kind": "TITANMCP_LIST_CONNECTORS",
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
            "consent-attach, get_operator, MESSAGE_CURSOR_NOT_FOUND, "
            "get_connector, or check_subscription KEEP. leftover bake/deploy sent=0."
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
                "clientInfo": {"name": "titanmcp-list-connectors", "version": "1"},
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
    if "list_connectors" not in names:
        errors.append("pad_tool")

    empty = _call("list_connectors", {}, 3)
    empty_row = classify_empty(empty.get("packet") or {}, empty.get("status") or 0)
    if not empty_row["ok"]:
        errors.append("empty")

    q_github = _call("list_connectors", {"q": "github"}, 4)
    q_github_row = classify_github_search(q_github.get("packet") or {}, q_github.get("status") or 0)
    if not q_github_row["ok"]:
        errors.append("q_github")

    query_github = _call("list_connectors", {"query": "github"}, 5)
    query_github_row = classify_github_search(
        query_github.get("packet") or {}, query_github.get("status") or 0
    )
    if not query_github_row["ok"]:
        errors.append("query_github")

    q_wins = _call("list_connectors", {"q": "github", "query": "slack"}, 6)
    q_wins_row = classify_github_search(q_wins.get("packet") or {}, q_wins.get("status") or 0)
    if not q_wins_row["ok"]:
        errors.append("q_precedence")

    wrong_q = _call("list_connectors", {"q": 1}, 7)
    wrong_q_row = classify_must_be_string(wrong_q.get("packet") or {}, wrong_q.get("status") or 0, "q")
    if not wrong_q_row["ok"]:
        errors.append("wrong_type_q")

    extra_minutes = _call("list_connectors", {"minutes": 1}, 8)
    extra_minutes_row = classify_not_allowed(
        extra_minutes.get("packet") or {}, extra_minutes.get("status") or 0, "minutes"
    )
    if not extra_minutes_row["ok"]:
        errors.append("extra_minutes")

    limit_one = _call("list_connectors", {"limit": 1}, 9)
    limit_one_row = classify_limit_one(limit_one.get("packet") or {}, limit_one.get("status") or 0)
    if not limit_one_row["ok"]:
        errors.append("limit_one")

    commons_init = _rpc(
        COMMONS_MCP,
        {
            "jsonrpc": "2.0",
            "id": 10,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "titanmcp-list-connectors", "version": "1"},
            },
        },
        origin="",
    )
    commons_info = ((commons_init.get("packet") or {}).get("result") or {}).get("serverInfo") or {}
    commons_listed = _rpc(
        COMMONS_MCP,
        {"jsonrpc": "2.0", "id": 11, "method": "tools/list", "params": {}},
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
        or "list_connectors" in commons_names
    ):
        errors.append("commons_keep")

    return {
        "kind": "TITANMCP_LIST_CONNECTORS",
        "id": ID,
        "pad_initialize": {"name": info.get("name"), "version": info.get("version")},
        "commons_initialize": {
            "name": commons_info.get("name"),
            "version": commons_info.get("version"),
        },
        "pad_has_list_connectors": "list_connectors" in names,
        "commons_has_list_connectors": "list_connectors" in commons_names,
        "empty_arguments": empty_row,
        "q_github": q_github_row,
        "query_github": query_github_row,
        "q_precedence": q_wins_row,
        "wrong_type_q": wrong_q_row,
        "extra_minutes": extra_minutes_row,
        "limit_one": limit_one_row,
        "did_not_remint": list(DO_NOT_REMINT),
        "sent": 0,
        "cash": 0,
        "errors": errors,
        "verdict": "MATCH" if not errors else "FINDER-FAILED",
        "note": (
            "Unique remainder after check_subscription KEEP: list_connectors "
            "empty arguments is 200 ok:true catalog_count 500 default "
            "returned_count 50 oauth_secrets false. q=github and query=github "
            "return catalog GitHub. q takes precedence over query. Wrong-type "
            "q is MCP isError BAD_ARGUMENT must be string, not JSON-RPC "
            "-32602. Extra minutes is not allowed. limit=1 still "
            "catalog_count 500. Commons /mcp KEEP has no list_connectors. "
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
                        "kind": "TITANMCP_LIST_CONNECTORS",
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
