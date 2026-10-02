#!/usr/bin/env python3
"""Unique titanmcp get_operator KEEP remainder.

Live get_operator with empty arguments is HTTP 200 JSON, MCP isError
BAD_ARGUMENT argument=arguments hint arguments does not satisfy any
allowed argument shape, not JSON-RPC -32602. role=builder returns
operator id BUILDER. Unknown id is MCP isError OPERATOR_NOT_FOUND.
list_operators count=5 store=roles_and_operators_in_mcp_not_harness.
Commons /mcp KEEP has no get_operator. Isolated classifier stays green
without reminting pad runtime, Latch titanmcp.html, setup-schema,
SAVE/LOAD DRAFT, GET /mcp identity, Origin pair, list_messages cursor,
unknown after=, create_play_token, or consent-attach batteries.
leftover --bake/--deploy/--go REFUSED sent=0. No competition
resubmission.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from typing import Any


ID = "cursor-titanmcp-get-operator-20261002-01"
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
    "p/cursor-titanmcp-setup-schema-20260929-01.md",
    "p/cursor-titanmcp-save-load-draft-20260930-01.md",
    "p/cursor-titanmcp-get-mcp-identity-20261001-01.md",
    "p/cursor-titanmcp-origin-pair-20261001-01.md",
    "p/cursor-titanmcp-list-messages-cursor-20261001-01.md",
    "p/cursor-titanmcp-unknown-after-20261001-01.md",
    "p/cursor-titanmcp-play-token-20261002-01.md",
    "p/cursor-titanmcp-consent-attach-20261002-01.md",
)
OPERATOR_IDS = ("COORDINATOR", "BUILDER", "PROBER", "SETUP", "ACCURACY")


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
        "User-Agent": "titanmcp-get-operator",
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
    ok = (
        status == 200
        and not err
        and result.get("isError") is True
        and sc.get("ok") is False
        and sc.get("error") == "BAD_ARGUMENT"
        and sc.get("argument") == "arguments"
        and "does not satisfy any allowed argument shape" in str(sc.get("hint") or "")
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


def classify_builder(packet: dict[str, Any], status: int) -> dict[str, Any]:
    err = jsonrpc_error(packet)
    result = packet.get("result") if isinstance(packet.get("result"), dict) else {}
    sc = structured_content(packet)
    operator = sc.get("operator") if isinstance(sc.get("operator"), dict) else {}
    ok = (
        status == 200
        and not err
        and result.get("isError") is not True
        and sc.get("ok") is True
        and sc.get("product") == "titanmcp"
        and operator.get("id") == "BUILDER"
        and operator.get("role") == "builder"
        and str(operator.get("header") or "").endswith("BUILDER")
        and isinstance(operator.get("prompt"), str)
        and len(str(operator.get("prompt"))) > 20
    )
    return {
        "ok": ok,
        "status": status,
        "jsonrpc_code": err.get("code"),
        "is_error": result.get("isError"),
        "sc_ok": sc.get("ok"),
        "product": sc.get("product"),
        "operator_id": operator.get("id"),
        "operator_role": operator.get("role"),
        "prompt_omitted": True,
    }


def classify_not_found(packet: dict[str, Any], status: int) -> dict[str, Any]:
    err = jsonrpc_error(packet)
    result = packet.get("result") if isinstance(packet.get("result"), dict) else {}
    sc = structured_content(packet)
    ok = (
        status == 200
        and not err
        and result.get("isError") is True
        and sc.get("ok") is False
        and sc.get("error") == "OPERATOR_NOT_FOUND"
        and sc.get("id") == "no-such-op"
        and err.get("code") != -32602
    )
    return {
        "ok": ok,
        "status": status,
        "jsonrpc_code": err.get("code"),
        "is_error": result.get("isError"),
        "error": sc.get("error"),
        "id": sc.get("id"),
        "not_jsonrpc_32602": err.get("code") != -32602,
    }


def classify_list(packet: dict[str, Any], status: int) -> dict[str, Any]:
    err = jsonrpc_error(packet)
    result = packet.get("result") if isinstance(packet.get("result"), dict) else {}
    sc = structured_content(packet)
    rows = sc.get("operators") if isinstance(sc.get("operators"), list) else []
    ids = [row.get("id") for row in rows if isinstance(row, dict)]
    ok = (
        status == 200
        and not err
        and result.get("isError") is not True
        and sc.get("ok") is True
        and sc.get("product") == "titanmcp"
        and sc.get("store") == "roles_and_operators_in_mcp_not_harness"
        and sc.get("count") == 5
        and len(ids) == 5
        and tuple(ids) == OPERATOR_IDS
    )
    return {
        "ok": ok,
        "status": status,
        "jsonrpc_code": err.get("code"),
        "is_error": result.get("isError"),
        "sc_ok": sc.get("ok"),
        "store": sc.get("store"),
        "count": sc.get("count"),
        "ids": ids,
    }


def refuse_payload(flag: str) -> dict[str, Any]:
    return {
        "kind": "TITANMCP_GET_OPERATOR",
        "id": ID,
        "refused": flag,
        "sent": 0,
        "cash": 0,
        "invented_stripe_urls": False,
        "verdict": "REFUSED",
        "note": (
            f"{flag} REFUSED. Did not remint pad runtime, titanmcp.html, "
            "setup-schema, SAVE/LOAD DRAFT, GET /mcp identity, Origin pair, "
            "list_messages cursor, unknown after=, create_play_token, or "
            "consent-attach KEEP. leftover bake/deploy sent=0."
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
                "clientInfo": {"name": "titanmcp-get-operator", "version": "1"},
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
    if "get_operator" not in names or "list_operators" not in names:
        errors.append("pad_tool")

    empty = _call("get_operator", {}, 3)
    empty_row = classify_empty(empty.get("packet") or {}, empty.get("status") or 0)
    if not empty_row["ok"]:
        errors.append("empty_arguments")

    builder = _call("get_operator", {"role": "builder"}, 4)
    builder_row = classify_builder(builder.get("packet") or {}, builder.get("status") or 0)
    if not builder_row["ok"]:
        errors.append("role_builder")

    missing = _call("get_operator", {"id": "no-such-op"}, 5)
    missing_row = classify_not_found(missing.get("packet") or {}, missing.get("status") or 0)
    if not missing_row["ok"]:
        errors.append("operator_not_found")

    listed_ops = _call("list_operators", {}, 6)
    list_row = classify_list(listed_ops.get("packet") or {}, listed_ops.get("status") or 0)
    if not list_row["ok"]:
        errors.append("list_operators")

    commons_init = _rpc(
        COMMONS_MCP,
        {
            "jsonrpc": "2.0",
            "id": 7,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "titanmcp-get-operator", "version": "1"},
            },
        },
        origin="",
    )
    commons_info = ((commons_init.get("packet") or {}).get("result") or {}).get("serverInfo") or {}
    commons_listed = _rpc(
        COMMONS_MCP,
        {"jsonrpc": "2.0", "id": 8, "method": "tools/list", "params": {}},
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
        or "get_operator" in commons_names
        or "list_operators" in commons_names
    ):
        errors.append("commons_keep")

    return {
        "kind": "TITANMCP_GET_OPERATOR",
        "id": ID,
        "pad_initialize": {"name": info.get("name"), "version": info.get("version")},
        "commons_initialize": {
            "name": commons_info.get("name"),
            "version": commons_info.get("version"),
        },
        "pad_has_get_operator": "get_operator" in names,
        "commons_has_get_operator": "get_operator" in commons_names,
        "empty_arguments": empty_row,
        "role_builder": builder_row,
        "operator_not_found": missing_row,
        "list_operators": list_row,
        "did_not_remint": list(DO_NOT_REMINT),
        "sent": 0,
        "cash": 0,
        "errors": errors,
        "verdict": "MATCH" if not errors else "FINDER-FAILED",
        "note": (
            "Unique remainder after consent-attach KEEP: get_operator empty "
            "arguments is MCP isError BAD_ARGUMENT argument=arguments shape, "
            "not JSON-RPC -32602. role=builder returns BUILDER. Unknown id is "
            "OPERATOR_NOT_FOUND. list_operators count=5. Commons /mcp KEEP has "
            "no get_operator. No competition resubmission."
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
                        "kind": "TITANMCP_GET_OPERATOR",
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
