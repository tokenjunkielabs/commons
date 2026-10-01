#!/usr/bin/env python3
"""Unique titanmcp GET /mcp identity + Origin allowlist KEEP remainder.

Live pad OPTIONS is no longer ACA-Origin None. Origin https://chatgpt.com
returns 204 with ACAO exactly that origin. Other origins return HTTP 403
JSON-RPC -32000 Origin not allowed. ACAO is not *. Commons /mcp KEEP
open_door + ACAO=*. Isolated classifier stays green without reminting pad
runtime, Latch titanmcp.html, setup-schema, or SAVE/LOAD DRAFT batteries.
leftover --bake/--deploy/--go REFUSED sent=0. No competition resubmission.
"""
from __future__ import annotations

import argparse
import http.client
import json
import ssl
import sys
import urllib.request
from typing import Any
from urllib.parse import urlparse


ID = "cursor-titanmcp-get-mcp-identity-20261001-01"
PAD_MCP = "https://webmcp-pad.vercel.app/mcp"
COMMONS_MCP = "https://commons-spark-mcp.vercel.app/mcp"
CHATGPT_ORIGIN = "https://chatgpt.com"
DENIED_ORIGIN = "https://example.com"
REFUSE = ("--send", "--apply", "--go", "--autopilot", "--live", "--checkout", "--deploy", "--bake")
DO_NOT_REMINT = (
    "api/mcp.py",
    "commons_mcp.py",
    "titanmcp.html",
    "webmcp.html",
    ".github/workflows/webmcp-pad-production.yml",
    "host/titanmcp_setup_schema.py",
    "host/titanmcp_save_load_draft.py",
    "test_titanmcp_gpt_use_setup_schema.py",
    "test_titanmcp_gpt_use_save_load_draft.py",
    "p/cursor-titanmcp-setup-schema-20260929-01.md",
    "p/cursor-titanmcp-save-load-draft-20260930-01.md",
)
FIRST_PARTY_IDS = ("titan-hands", "harborline-origin", "peer-worker")
PAD_TOOL_COUNT = 24

PACKET_ORIGIN_DENIED = {
    "jsonrpc": "2.0",
    "id": None,
    "error": {"code": -32000, "message": "Origin not allowed"},
}


def classify_origin_denied(packet: dict[str, Any]) -> dict[str, Any]:
    err = packet.get("error") or {}
    return {
        "ok": (
            err.get("code") == -32000
            and err.get("message") == "Origin not allowed"
            and "isError" not in packet
            and packet.get("jsonrpc") == "2.0"
        ),
        "code": err.get("code"),
        "message": err.get("message"),
        "is_error": packet.get("isError"),
        "acao_star": False,
    }


def classify_pad_get(obj: dict[str, Any]) -> dict[str, Any]:
    research = obj.get("research") or {}
    fp = list(research.get("first_party") or [])
    tools = obj.get("tools") or []
    missing_fp = [row for row in FIRST_PARTY_IDS if row not in fp]
    return {
        "ok": (
            obj.get("name") == "titanmcp"
            and obj.get("version") == "1.4.5"
            and obj.get("open_door") is False
            and obj.get("toolCount") == PAD_TOOL_COUNT
            and len(tools) == PAD_TOOL_COUNT
            and not missing_fp
            and "peer-worker" in fp
        ),
        "name": obj.get("name"),
        "version": obj.get("version"),
        "open_door": obj.get("open_door"),
        "toolCount": obj.get("toolCount"),
        "first_party": fp,
        "missing_first_party": missing_fp,
        "auth": obj.get("auth"),
        "policy": obj.get("policy"),
    }


def classify_commons_get(obj: dict[str, Any]) -> dict[str, Any]:
    return {
        "ok": (
            obj.get("name") == "commons"
            and obj.get("version") == "1.4.0"
            and obj.get("open_door") is True
            and obj.get("auth") == "none"
            and obj.get("login") is False
            and "titanmcp" not in json.dumps(obj)
        ),
        "name": obj.get("name"),
        "version": obj.get("version"),
        "open_door": obj.get("open_door"),
        "auth": obj.get("auth"),
        "login": obj.get("login"),
        "toolCount": obj.get("toolCount"),
    }


def classify_options(
    *,
    origin: str | None,
    status: int,
    acao: str | None,
    body: bytes,
) -> dict[str, Any]:
    denied = None
    if body:
        try:
            denied = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            denied = {"raw": body.decode("utf-8", "replace")}
    if origin is None:
        ok = status == 204 and acao is None
        pin = "no-origin-204-acao-absent"
    elif origin == CHATGPT_ORIGIN:
        ok = status == 204 and acao == CHATGPT_ORIGIN and acao != "*"
        pin = "chatgpt-origin-204-acao-exact"
    else:
        row = classify_origin_denied(denied) if isinstance(denied, dict) else {"ok": False}
        ok = status == 403 and acao is None and row.get("ok") is True
        pin = "other-origin-403-minus-32000"
    return {
        "ok": ok,
        "pin": pin,
        "origin": origin,
        "status": status,
        "acao": acao,
        "acao_star": acao == "*",
        "body": denied,
    }


def refuse_payload(flag: str) -> dict[str, Any]:
    return {
        "kind": "TITANMCP_GET_MCP_IDENTITY",
        "id": ID,
        "refused": flag,
        "sent": 0,
        "cash": 0,
        "invented_stripe_urls": False,
        "verdict": "REFUSED",
        "note": (
            f"{flag} REFUSED. Did not remint pad runtime, titanmcp.html, "
            "setup-schema, or SAVE/LOAD DRAFT KEEP. leftover bake/deploy sent=0."
        ),
    }


def _rpc(url: str, obj: dict[str, Any]) -> dict[str, Any]:
    req = urllib.request.Request(
        url,
        data=json.dumps(obj).encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "MCP-Protocol-Version": "2025-03-26",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        packet = json.loads(resp.read().decode("utf-8"))
        info = (packet.get("result") or {}).get("serverInfo") or {}
        return {"status": resp.status, "name": info.get("name"), "version": info.get("version")}


def _get_json(url: str) -> tuple[int, dict[str, Any]]:
    req = urllib.request.Request(
        url,
        method="GET",
        headers={"Accept": "application/json", "User-Agent": "titanmcp-get-mcp-identity"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def _options(url: str, origin: str | None) -> tuple[int, str | None, bytes]:
    parsed = urlparse(url)
    conn = http.client.HTTPSConnection(parsed.netloc, timeout=20, context=ssl.create_default_context())
    headers = {
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type,mcp-protocol-version",
        "User-Agent": "titanmcp-get-mcp-identity",
    }
    if origin is not None:
        headers["Origin"] = origin
    conn.request("OPTIONS", parsed.path or "/", headers=headers)
    resp = conn.getresponse()
    raw = resp.read()
    header_map = {k.lower(): v for k, v in resp.getheaders()}
    acao = header_map.get("access-control-allow-origin")
    status = resp.status
    conn.close()
    return status, acao, raw


def measure() -> dict[str, Any]:
    errors: list[str] = []
    pad_status, pad_obj = _get_json(PAD_MCP)
    pad_get = classify_pad_get(pad_obj)
    pad_get["http_status"] = pad_status
    if pad_status != 200 or not pad_get["ok"]:
        errors.append("pad_get")

    commons_status, commons_obj = _get_json(COMMONS_MCP)
    commons_get = classify_commons_get(commons_obj)
    commons_get["http_status"] = commons_status
    if commons_status != 200 or not commons_get["ok"]:
        errors.append("commons_get")

    options_rows = []
    for origin in (None, CHATGPT_ORIGIN, DENIED_ORIGIN):
        status, acao, body = _options(PAD_MCP, origin)
        row = classify_options(origin=origin, status=status, acao=acao, body=body)
        options_rows.append(row)
        if not row["ok"]:
            errors.append(f"pad_options:{row['pin']}")

    commons_opt_status, commons_acao, _commons_body = _options(COMMONS_MCP, DENIED_ORIGIN)
    commons_options = {
        "ok": commons_opt_status == 204 and commons_acao == "*",
        "status": commons_opt_status,
        "acao": commons_acao,
        "origin": DENIED_ORIGIN,
        "pin": "commons-acao-star-keep",
    }
    if not commons_options["ok"]:
        errors.append("commons_options")

    denied_recorded = classify_origin_denied(PACKET_ORIGIN_DENIED)
    if not denied_recorded["ok"]:
        errors.append("recorded_origin_denied")

    pad = _rpc(
        PAD_MCP,
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "titanmcp-get-mcp-identity", "version": "1"},
            },
        },
    )
    if pad.get("name") != "titanmcp" or pad.get("version") != "1.4.5":
        errors.append("pad_mcp")
    commons = _rpc(
        COMMONS_MCP,
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "titanmcp-get-mcp-identity", "version": "1"},
            },
        },
    )
    if commons.get("name") != "commons" or commons.get("version") != "1.4.0":
        errors.append("commons_keep")

    return {
        "kind": "TITANMCP_GET_MCP_IDENTITY",
        "id": ID,
        "pad_get": pad_get,
        "commons_get": commons_get,
        "pad_options": options_rows,
        "commons_options": commons_options,
        "recorded_origin_denied": denied_recorded,
        "pad_initialize": pad,
        "commons_initialize": commons,
        "did_not_remint": list(DO_NOT_REMINT),
        "sent": 0,
        "cash": 0,
        "errors": errors,
        "verdict": "MATCH" if not errors else "FINDER-FAILED",
        "note": (
            "Unique remainder: GET /mcp JSON identity + Origin allowlist "
            "(chatgpt.com 204 exact ACAO; other origin 403 -32000). "
            "ACAO is not *. Commons /mcp KEEP. No competition resubmission."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--json", action="store_true")
    args, unknown = parser.parse_known_args(argv)
    for flag in unknown:
        if flag in REFUSE:
            print(json.dumps(refuse_payload(flag), sort_keys=True))
            return 2
        if flag.startswith("-"):
            print(
                json.dumps(
                    {
                        "kind": "TITANMCP_GET_MCP_IDENTITY",
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
