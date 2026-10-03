#!/usr/bin/env python3
"""Unique titanmcp get_setup_status KEEP remainder.

Live get_setup_status with empty arguments is HTTP 200 JSON, MCP
ok:true, catalog_count 500, subject unbound-agent, session_bound false,
bare true, wired_count 0, setup_complete false, authority
in-app-browser-session-required. Optional string subject (including
github or empty) stays unbound-agent. Extra need, extra query, extra
minutes, and extra id are MCP isError BAD_ARGUMENT hint
arguments.<name> is not allowed (need is required on request_setup;
query is the list_research_power filter; id=github is
OPTIONAL_CAPABILITY_NOT_FOUND on list_custom_tooling). Wrong-type
subject is MCP isError BAD_ARGUMENT hint arguments.subject must be
string, not JSON-RPC -32602. Commons /mcp KEEP has no
get_setup_status. Isolated classifier stays green without reminting pad
runtime, Latch titanmcp.html, setup-schema, SAVE/LOAD DRAFT, GET /mcp
identity, Origin pair, list_messages cursor, unknown after=,
create_play_token, consent-attach, get_operator,
MESSAGE_CURSOR_NOT_FOUND, get_connector, check_subscription,
list_connectors, list_research_power, or list_custom_tooling
batteries. leftover --bake/--deploy/--go REFUSED sent=0. No
competition resubmission.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from typing import Any


ID = "cursor-titanmcp-get-setup-status-20261003-01"
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
    "host/titanmcp_check_subscription.py",
    "host/titanmcp_list_connectors.py",
    "host/titanmcp_list_research_power.py",
    "host/titanmcp_list_custom_tooling.py",
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
    "p/cursor-titanmcp-list-connectors-20261003-01.md",
    "p/cursor-titanmcp-list-research-power-20261003-01.md",
    "p/cursor-titanmcp-list-custom-tooling-20261003-01.md",
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
        "User-Agent": "titanmcp-get-setup-status",
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
    consents = sc.get("consents") if isinstance(sc.get("consents"), dict) else {}
    cta = sc.get("cta") if isinstance(sc.get("cta"), dict) else {}
    ok = (
        status == 200
        and not err
        and result.get("isError") is not True
        and sc.get("ok") is True
        and sc.get("catalog_count") == 500
        and sc.get("subject") == "unbound-agent"
        and sc.get("session_bound") is False
        and sc.get("bare") is True
        and sc.get("wired_count") == 0
        and sc.get("setup_complete") is False
        and sc.get("authority") == "in-app-browser-session-required"
        and sc.get("setup_path_default") == "research"
        and consents.get("connectors") is False
        and consents.get("coordination") is False
        and consents.get("billing") is False
        and cta.get("label") == "SETUP"
        and cta.get("action") == "open_research"
        and err.get("code") != -32602
    )
    return {
        "ok": ok,
        "status": status,
        "jsonrpc_code": err.get("code"),
        "is_error": result.get("isError"),
        "sc_ok": sc.get("ok"),
        "catalog_count": sc.get("catalog_count"),
        "subject": sc.get("subject"),
        "session_bound": sc.get("session_bound"),
        "bare": sc.get("bare"),
        "wired_count": sc.get("wired_count"),
        "setup_complete": sc.get("setup_complete"),
        "authority": sc.get("authority"),
        "not_jsonrpc_32602": err.get("code") != -32602,
    }


def classify_subject_unbound(packet: dict[str, Any], status: int) -> dict[str, Any]:
    err = jsonrpc_error(packet)
    result = packet.get("result") if isinstance(packet.get("result"), dict) else {}
    sc = structured_content(packet)
    ok = (
        status == 200
        and not err
        and result.get("isError") is not True
        and sc.get("ok") is True
        and sc.get("subject") == "unbound-agent"
        and sc.get("catalog_count") == 500
        and sc.get("session_bound") is False
        and err.get("code") != -32602
    )
    return {
        "ok": ok,
        "status": status,
        "jsonrpc_code": err.get("code"),
        "is_error": result.get("isError"),
        "sc_ok": sc.get("ok"),
        "subject": sc.get("subject"),
        "catalog_count": sc.get("catalog_count"),
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
        "kind": "TITANMCP_GET_SETUP_STATUS",
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
            "get_connector, check_subscription, list_connectors, "
            "list_research_power, or list_custom_tooling KEEP. leftover "
            "bake/deploy sent=0."
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
                "clientInfo": {"name": "titanmcp-get-setup-status", "version": "1"},
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
    if "get_setup_status" not in names:
        errors.append("pad_tool")

    empty = _call("get_setup_status", {}, 3)
    empty_row = classify_empty(empty.get("packet") or {}, empty.get("status") or 0)
    if not empty_row["ok"]:
        errors.append("empty")

    extra_minutes = _call("get_setup_status", {"minutes": 1}, 4)
    extra_minutes_row = classify_not_allowed(
        extra_minutes.get("packet") or {}, extra_minutes.get("status") or 0, "minutes"
    )
    if not extra_minutes_row["ok"]:
        errors.append("extra_minutes")

    extra_need = _call("get_setup_status", {"need": "x"}, 5)
    extra_need_row = classify_not_allowed(
        extra_need.get("packet") or {}, extra_need.get("status") or 0, "need"
    )
    if not extra_need_row["ok"]:
        errors.append("extra_need")

    extra_query = _call("get_setup_status", {"query": "github"}, 6)
    extra_query_row = classify_not_allowed(
        extra_query.get("packet") or {}, extra_query.get("status") or 0, "query"
    )
    if not extra_query_row["ok"]:
        errors.append("extra_query")

    extra_id = _call("get_setup_status", {"id": "github"}, 7)
    extra_id_row = classify_not_allowed(
        extra_id.get("packet") or {}, extra_id.get("status") or 0, "id"
    )
    if not extra_id_row["ok"]:
        errors.append("extra_id")

    wrong_subject = _call("get_setup_status", {"subject": 1}, 8)
    wrong_subject_row = classify_must_be_string(
        wrong_subject.get("packet") or {}, wrong_subject.get("status") or 0, "subject"
    )
    if not wrong_subject_row["ok"]:
        errors.append("wrong_type_subject")

    github_subject = _call("get_setup_status", {"subject": "github"}, 9)
    github_subject_row = classify_subject_unbound(
        github_subject.get("packet") or {}, github_subject.get("status") or 0
    )
    if not github_subject_row["ok"]:
        errors.append("subject_unbound")

    commons_init = _rpc(
        COMMONS_MCP,
        {
            "jsonrpc": "2.0",
            "id": 10,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "titanmcp-get-setup-status", "version": "1"},
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
        or "get_setup_status" in commons_names
    ):
        errors.append("commons_keep")

    return {
        "kind": "TITANMCP_GET_SETUP_STATUS",
        "id": ID,
        "pad_initialize": {"name": info.get("name"), "version": info.get("version")},
        "commons_initialize": {
            "name": commons_info.get("name"),
            "version": commons_info.get("version"),
        },
        "pad_has_get_setup_status": "get_setup_status" in names,
        "commons_has_get_setup_status": "get_setup_status" in commons_names,
        "empty_arguments": empty_row,
        "extra_minutes": extra_minutes_row,
        "extra_need": extra_need_row,
        "extra_query": extra_query_row,
        "extra_id": extra_id_row,
        "wrong_type_subject": wrong_subject_row,
        "subject_unbound": github_subject_row,
        "did_not_remint": list(DO_NOT_REMINT),
        "sent": 0,
        "cash": 0,
        "errors": errors,
        "verdict": "MATCH" if not errors else "FINDER-FAILED",
        "note": (
            "Unique remainder after list_custom_tooling KEEP: "
            "get_setup_status empty arguments is 200 ok:true "
            "catalog_count 500 subject unbound-agent bare true. Extra need, "
            "query, minutes, and id are MCP isError BAD_ARGUMENT is not "
            "allowed. Wrong-type subject is MCP isError BAD_ARGUMENT must be "
            "string, not JSON-RPC -32602. Optional string subject=github "
            "stays unbound-agent. Commons /mcp KEEP has no get_setup_status. "
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
                        "kind": "TITANMCP_GET_SETUP_STATUS",
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
