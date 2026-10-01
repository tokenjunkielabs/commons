#!/usr/bin/env python3
"""Unique titanmcp Origin pair KEEP remainder.

GET /mcp identity pin already covers chatgpt.com OPTIONS 204 vs example.com
403. Live pad also allows its own origin, denies chat.openai.com on
OPTIONS/GET/POST, and echoes ACAO + Vary=Origin on allowed GET/POST.
Commons /mcp KEEP ACAO=*. Isolated classifier stays green without reminting
pad runtime, Latch titanmcp.html, setup-schema, SAVE/LOAD DRAFT, or GET /mcp
identity batteries. leftover --bake/--deploy/--go REFUSED sent=0.
No competition resubmission.
"""
from __future__ import annotations

import argparse
import http.client
import json
import ssl
import sys
from typing import Any
from urllib.parse import urlparse


ID = "cursor-titanmcp-origin-pair-20261001-01"
PAD_MCP = "https://webmcp-pad.vercel.app/mcp"
COMMONS_MCP = "https://commons-spark-mcp.vercel.app/mcp"
ALLOWED_ORIGINS = (
    "https://chatgpt.com",
    "https://webmcp-pad.vercel.app",
)
DENIED_ORIGINS = (
    "https://chat.openai.com",
    "https://example.com",
)
PAD_ACAH = "Accept, Authorization, Content-Type, MCP-Protocol-Version, Mcp-Session-Id"
COMMONS_ACAH = "Accept, Content-Type, MCP-Protocol-Version, Mcp-Session-Id"
PAD_ACAM = "GET, HEAD, POST, OPTIONS, DELETE"
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
    "test_titanmcp_gpt_use_setup_schema.py",
    "test_titanmcp_gpt_use_save_load_draft.py",
    "p/cursor-titanmcp-setup-schema-20260929-01.md",
    "p/cursor-titanmcp-save-load-draft-20260930-01.md",
    "p/cursor-titanmcp-get-mcp-identity-20261001-01.md",
)
PACKET_ORIGIN_DENIED = {
    "jsonrpc": "2.0",
    "id": None,
    "error": {"code": -32000, "message": "Origin not allowed"},
}
INIT = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-03-26",
        "capabilities": {},
        "clientInfo": {"name": "titanmcp-origin-pair", "version": "1"},
    },
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
    }


def _decode_json(raw: bytes) -> dict[str, Any] | None:
    if not raw:
        return None
    try:
        obj = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError:
        return {"raw": raw.decode("utf-8", "replace")}
    return obj if isinstance(obj, dict) else {"raw": obj}


def _request(
    url: str,
    *,
    method: str,
    origin: str | None,
    body: bytes | None = None,
) -> dict[str, Any]:
    parsed = urlparse(url)
    conn = http.client.HTTPSConnection(parsed.netloc, timeout=20, context=ssl.create_default_context())
    headers = {"User-Agent": "titanmcp-origin-pair"}
    if method == "OPTIONS":
        headers["Access-Control-Request-Method"] = "POST"
        headers["Access-Control-Request-Headers"] = "content-type,mcp-protocol-version"
    elif method == "GET":
        headers["Accept"] = "application/json"
    else:
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json, text/event-stream"
        headers["MCP-Protocol-Version"] = "2025-03-26"
    if origin is not None:
        headers["Origin"] = origin
    conn.request(method, parsed.path or "/", body=body, headers=headers)
    resp = conn.getresponse()
    raw = resp.read()
    header_map = {k.lower(): v for k, v in resp.getheaders()}
    status = resp.status
    conn.close()
    return {
        "method": method,
        "origin": origin,
        "status": status,
        "acao": header_map.get("access-control-allow-origin"),
        "acah": header_map.get("access-control-allow-headers"),
        "acam": header_map.get("access-control-allow-methods"),
        "vary": header_map.get("vary"),
        "body": _decode_json(raw),
        "bytes": len(raw),
    }


def classify_allowed(row: dict[str, Any], *, expect_name: str | None) -> dict[str, Any]:
    origin = row["origin"]
    method = row["method"]
    acao_ok = row["acao"] == origin and row["acao"] != "*"
    vary_ok = row.get("vary") == "Origin"
    acah_ok = row.get("acah") == PAD_ACAH if method == "OPTIONS" else True
    acam_ok = row.get("acam") == PAD_ACAM if method == "OPTIONS" else True
    if method == "OPTIONS":
        status_ok = row["status"] == 204 and row["body"] is None
        name_ok = True
    elif method == "GET":
        body = row["body"] or {}
        status_ok = row["status"] == 200
        name_ok = body.get("name") == expect_name and body.get("open_door") is False
    else:
        info = ((row["body"] or {}).get("result") or {}).get("serverInfo") or {}
        status_ok = row["status"] == 200
        name_ok = info.get("name") == expect_name and info.get("version") == "1.4.5"
    ok = status_ok and acao_ok and vary_ok and acah_ok and acam_ok and name_ok
    return {
        "ok": ok,
        "pin": f"allowed-{method.lower()}-{origin}",
        "status": row["status"],
        "acao": row["acao"],
        "vary": row.get("vary"),
        "acao_star": row["acao"] == "*",
    }


def classify_denied(row: dict[str, Any]) -> dict[str, Any]:
    body = row["body"] if isinstance(row["body"], dict) else {}
    denied = classify_origin_denied(body)
    ok = (
        row["status"] == 403
        and row["acao"] is None
        and denied["ok"] is True
        and row["acao"] != "*"
    )
    return {
        "ok": ok,
        "pin": f"denied-{row['method'].lower()}-{row['origin']}",
        "status": row["status"],
        "acao": row["acao"],
        "denied": denied,
        "acao_star": False,
    }


def classify_commons(row: dict[str, Any], *, method: str) -> dict[str, Any]:
    if method == "OPTIONS":
        ok = (
            row["status"] == 204
            and row["acao"] == "*"
            and row.get("acah") == COMMONS_ACAH
            and "Authorization" not in (row.get("acah") or "")
        )
        name = None
    elif method == "GET":
        body = row["body"] or {}
        ok = (
            row["status"] == 200
            and row["acao"] == "*"
            and body.get("name") == "commons"
            and body.get("open_door") is True
        )
        name = body.get("name")
    else:
        info = ((row["body"] or {}).get("result") or {}).get("serverInfo") or {}
        ok = (
            row["status"] == 200
            and row["acao"] == "*"
            and info.get("name") == "commons"
            and info.get("version") == "1.4.0"
        )
        name = info.get("name")
    return {
        "ok": ok,
        "pin": f"commons-{method.lower()}-acao-star-keep",
        "status": row["status"],
        "acao": row["acao"],
        "acah": row.get("acah"),
        "name": name,
        "authorization_header_allowed": "Authorization" in (row.get("acah") or ""),
    }


def refuse_payload(flag: str) -> dict[str, Any]:
    return {
        "kind": "TITANMCP_ORIGIN_PAIR",
        "id": ID,
        "refused": flag,
        "sent": 0,
        "cash": 0,
        "invented_stripe_urls": False,
        "verdict": "REFUSED",
        "note": (
            f"{flag} REFUSED. Did not remint pad runtime, titanmcp.html, "
            "setup-schema, SAVE/LOAD DRAFT, or GET /mcp identity KEEP. "
            "leftover bake/deploy sent=0."
        ),
    }


def measure() -> dict[str, Any]:
    errors: list[str] = []
    allowed_rows: list[dict[str, Any]] = []
    denied_rows: list[dict[str, Any]] = []
    init_body = json.dumps(INIT).encode("utf-8")

    for origin in ALLOWED_ORIGINS:
        for method, body in (("OPTIONS", None), ("GET", None), ("POST", init_body)):
            raw = _request(PAD_MCP, method=method, origin=origin, body=body)
            row = classify_allowed(raw, expect_name="titanmcp")
            row["acah"] = raw.get("acah")
            row["acam"] = raw.get("acam")
            allowed_rows.append(row)
            if not row["ok"]:
                errors.append(row["pin"])

    for origin in DENIED_ORIGINS:
        for method, body in (("OPTIONS", None), ("GET", None), ("POST", init_body)):
            raw = _request(PAD_MCP, method=method, origin=origin, body=body)
            row = classify_denied(raw)
            denied_rows.append(row)
            if not row["ok"]:
                errors.append(row["pin"])

    commons_rows = []
    example = "https://example.com"
    for method, body in (("OPTIONS", None), ("GET", None), ("POST", init_body)):
        raw = _request(COMMONS_MCP, method=method, origin=example, body=body)
        row = classify_commons(raw, method=method)
        commons_rows.append(row)
        if not row["ok"]:
            errors.append(row["pin"])

    recorded = classify_origin_denied(PACKET_ORIGIN_DENIED)
    if not recorded["ok"]:
        errors.append("recorded_origin_denied")

    chatgpt_ok = any(r["ok"] and r["pin"].endswith("https://chatgpt.com") for r in allowed_rows)
    pad_origin_ok = any(
        r["ok"] and r["pin"].endswith("https://webmcp-pad.vercel.app") for r in allowed_rows
    )
    openai_denied = any(
        r["ok"] and r["pin"].endswith("https://chat.openai.com") for r in denied_rows
    )
    if not (chatgpt_ok and pad_origin_ok and openai_denied):
        errors.append("origin_pair_incomplete")

    return {
        "kind": "TITANMCP_ORIGIN_PAIR",
        "id": ID,
        "allowed": allowed_rows,
        "denied": denied_rows,
        "commons": commons_rows,
        "recorded_origin_denied": recorded,
        "allowed_origins": list(ALLOWED_ORIGINS),
        "denied_origins": list(DENIED_ORIGINS),
        "pad_acah_includes_authorization": True,
        "commons_acah_includes_authorization": False,
        "did_not_remint": list(DO_NOT_REMINT),
        "sent": 0,
        "cash": 0,
        "errors": errors,
        "verdict": "MATCH" if not errors else "FINDER-FAILED",
        "note": (
            "Unique remainder after GET /mcp identity: allowed Origins are "
            "chatgpt.com and webmcp-pad.vercel.app; chat.openai.com is 403 "
            "JSON-RPC -32000 on OPTIONS/GET/POST; ACAO exact + Vary=Origin. "
            "Commons /mcp KEEP ACAO=*. No competition resubmission."
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
                        "kind": "TITANMCP_ORIGIN_PAIR",
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
