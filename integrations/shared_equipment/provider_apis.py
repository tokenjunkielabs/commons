"""Shared Groq and Exa API tools backed by the common secure credential reader.

Provider keys are fetched only at call time and remain in memory.  The outer
shared-equipment carrier owns request_id/call_id journaling and replay policy;
this adapter never retries a provider request.
"""

from __future__ import annotations

import copy
import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from .provider_io import redacted


GROQ_BASE = "https://api.groq.com/openai/v1"
EXA_BASE = "https://api.exa.ai"
MAX_RESPONSE_BYTES = 12 * 1024 * 1024
MAX_PROMPT_CHARS = 300_000
MAX_MESSAGES = 100
MAX_CHAT_COMPLETION_TOKENS = 8192
MAX_SEARCH_RESULTS = 10
MAX_CONTENT_URLS = 5


def _tool(name: str, description: str, properties: dict, required: list[str] | None = None) -> dict:
    return {
        "name": name,
        "description": description,
        "inputSchema": {
            "type": "object",
            "properties": properties,
            "required": required or [],
            "additionalProperties": False,
        },
    }


TOOLS = [
    _tool(
        "groq_list_models",
        "List models available to the shared Groq account. Uses the shared secure groq/api-key reference.",
        {},
    ),
    _tool(
        "groq_chat_completion",
        "Create one non-streaming Groq chat completion. Uses the shared secure groq/api-key reference and never retries a provider call.",
        {
            "model": {"type": "string", "minLength": 1, "maxLength": 200},
            "messages": {
                "type": "array",
                "minItems": 1,
                "maxItems": MAX_MESSAGES,
                "items": {
                    "type": "object",
                    "properties": {
                        "role": {"type": "string", "enum": ["system", "developer", "user", "assistant", "tool"]},
                        "content": {"type": "string"},
                        "name": {"type": "string"},
                        "tool_call_id": {"type": "string"},
                    },
                    "required": ["role", "content"],
                    "additionalProperties": True,
                },
            },
            "max_completion_tokens": {"type": "integer", "minimum": 1, "maximum": MAX_CHAT_COMPLETION_TOKENS},
            "temperature": {"type": "number", "minimum": 0, "maximum": 2},
            "top_p": {"type": "number", "exclusiveMinimum": 0, "maximum": 1},
            "stop": {
                "oneOf": [
                    {"type": "string", "maxLength": 256},
                    {"type": "array", "maxItems": 4, "items": {"type": "string", "maxLength": 256}},
                ]
            },
        },
        ["model", "messages"],
    ),
    _tool(
        "exa_search",
        "Search the web with Exa. Results contain URLs and metadata by default; request page text or highlights only when needed. Uses the shared secure exa/api-key reference.",
        {
            "query": {"type": "string", "minLength": 1, "maxLength": 2000},
            "num_results": {"type": "integer", "minimum": 1, "maximum": MAX_SEARCH_RESULTS},
            "include_text": {"type": "boolean"},
            "include_highlights": {"type": "boolean"},
        },
        ["query"],
    ),
    _tool(
        "exa_contents",
        "Retrieve page text and optional highlights for up to five HTTP(S) URLs using Exa's Contents API. Uses the shared secure exa/api-key reference.",
        {
            "urls": {
                "type": "array",
                "minItems": 1,
                "maxItems": MAX_CONTENT_URLS,
                "items": {"type": "string", "minLength": 8, "maxLength": 2048},
            },
            "include_text": {"type": "boolean"},
            "include_highlights": {"type": "boolean"},
        },
        ["urls"],
    ),
]


class ProviderToolError(RuntimeError):
    def __init__(self, result: dict[str, Any]):
        super().__init__(str(result.get("code", "provider_error")))
        self.result = result


class GroqExaEquipment:
    """Provider extension for Groq inference and Exa search/content calls."""

    def __init__(self, *, credential_sources=None, opener=None, timeout: float = 30):
        self.credential_sources = credential_sources
        self.opener = opener or urllib.request.urlopen
        self.timeout = min(60.0, max(1.0, float(timeout)))

    def tools(self, **_kwargs) -> list[dict]:
        return copy.deepcopy(TOOLS)

    def call(self, name: str, arguments: dict) -> dict:
        try:
            result = self._call(name, arguments)
            return {"isError": False, "result": result, "uncertain": False}
        except ProviderToolError as exc:
            return {"isError": True, **exc.result}
        except Exception as exc:
            # Do not put exception text, URLs, request bodies, or provider keys
            # into the shared journal or carrier response.
            return {
                "isError": True,
                "error": "provider_request_failed",
                "code": type(exc).__name__,
                "message": "Provider request failed before a usable response was received.",
                "uncertain": False,
            }

    def _call(self, name: str, args: dict) -> dict:
        if name == "groq_list_models":
            key = self._key("groq/api-key")
            return self._request("groq", "GET", GROQ_BASE + "/models", key=key)
        if name == "groq_chat_completion":
            key = self._key("groq/api-key")
            payload = self._groq_chat_payload(args)
            return self._request("groq", "POST", GROQ_BASE + "/chat/completions", key=key, payload=payload)
        if name == "exa_search":
            key = self._key("exa/api-key")
            payload = self._exa_search_payload(args)
            return self._request("exa", "POST", EXA_BASE + "/search", key=key, payload=payload)
        if name == "exa_contents":
            key = self._key("exa/api-key")
            payload = self._exa_contents_payload(args)
            return self._request("exa", "POST", EXA_BASE + "/contents", key=key, payload=payload)
        raise ProviderToolError({
            "error": "unknown_provider_tool",
            "code": "unknown_provider_tool",
            "message": "Unknown shared provider tool.",
            "uncertain": False,
        })

    def _key(self, reference: str) -> str:
        sources = self.credential_sources
        if sources is None:
            from .credential_transfer import CredentialSources
            sources = CredentialSources()
            self.credential_sources = sources
        try:
            value = sources.read(reference)
        except Exception:
            raise ProviderToolError({
                "error": "credential_unavailable",
                "code": "credential_unavailable",
                "provider": reference.split("/", 1)[0],
                "message": "The provider credential is not available from the shared secure credential facility.",
                "uncertain": False,
            }) from None
        if not isinstance(value, str) or not value.strip():
            raise ProviderToolError({
                "error": "credential_unavailable",
                "code": "credential_unavailable",
                "provider": reference.split("/", 1)[0],
                "message": "The provider credential is not available from the shared secure credential facility.",
                "uncertain": False,
            })
        return value.strip()

    @staticmethod
    def _groq_chat_payload(args: dict) -> dict:
        model = args.get("model")
        messages = args.get("messages")
        if not isinstance(model, str) or not model.strip() or len(model) > 200:
            raise ProviderToolError({"error": "invalid_arguments", "code": "invalid_model", "message": "model must be non-empty text up to 200 characters.", "uncertain": False})
        if not isinstance(messages, list) or not 1 <= len(messages) <= MAX_MESSAGES:
            raise ProviderToolError({"error": "invalid_arguments", "code": "invalid_messages", "message": "messages must contain between 1 and 100 items.", "uncertain": False})
        normalized = []
        content_size = 0
        for message in messages:
            if not isinstance(message, dict) or message.get("role") not in {"system", "developer", "user", "assistant", "tool"}:
                raise ProviderToolError({"error": "invalid_arguments", "code": "invalid_message", "message": "Each message needs a supported role and text content.", "uncertain": False})
            content = message.get("content")
            if not isinstance(content, str):
                raise ProviderToolError({"error": "invalid_arguments", "code": "invalid_message", "message": "Each message content must be text.", "uncertain": False})
            content_size += len(content)
            if content_size > MAX_PROMPT_CHARS:
                raise ProviderToolError({"error": "invalid_arguments", "code": "prompt_too_large", "message": "Combined message content exceeds the local request limit.", "uncertain": False})
            row = {"role": message["role"], "content": content}
            if isinstance(message.get("name"), str):
                row["name"] = message["name"]
            if isinstance(message.get("tool_call_id"), str):
                row["tool_call_id"] = message["tool_call_id"]
            normalized.append(row)
        payload = {"model": model.strip(), "messages": normalized, "stream": False}
        if "max_completion_tokens" in args:
            value = args["max_completion_tokens"]
            if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= MAX_CHAT_COMPLETION_TOKENS:
                raise ProviderToolError({"error": "invalid_arguments", "code": "invalid_max_completion_tokens", "message": "max_completion_tokens must be an integer from 1 to 8192.", "uncertain": False})
            payload["max_completion_tokens"] = value
        for field, low, high in (("temperature", 0, 2), ("top_p", 0, 1)):
            if field in args:
                value = args[field]
                if isinstance(value, bool) or not isinstance(value, (int, float)) or not low <= value <= high or field == "top_p" and value == 0:
                    raise ProviderToolError({"error": "invalid_arguments", "code": "invalid_" + field, "message": field + " is outside the supported range.", "uncertain": False})
                payload[field] = value
        if "stop" in args:
            stop = args["stop"]
            if isinstance(stop, str) and len(stop) <= 256:
                payload["stop"] = stop
            elif isinstance(stop, list) and len(stop) <= 4 and all(isinstance(item, str) and len(item) <= 256 for item in stop):
                payload["stop"] = stop
            else:
                raise ProviderToolError({"error": "invalid_arguments", "code": "invalid_stop", "message": "stop must be text or up to four short text values.", "uncertain": False})
        return payload

    @staticmethod
    def _exa_search_payload(args: dict) -> dict:
        query = args.get("query")
        if not isinstance(query, str) or not query.strip() or len(query) > 2000:
            raise ProviderToolError({"error": "invalid_arguments", "code": "invalid_query", "message": "query must be non-empty text up to 2000 characters.", "uncertain": False})
        count = args.get("num_results", 5)
        if isinstance(count, bool) or not isinstance(count, int) or not 1 <= count <= MAX_SEARCH_RESULTS:
            raise ProviderToolError({"error": "invalid_arguments", "code": "invalid_num_results", "message": "num_results must be an integer from 1 to 10.", "uncertain": False})
        for field in ("include_text", "include_highlights"):
            if field in args and not isinstance(args[field], bool):
                raise ProviderToolError({"error": "invalid_arguments", "code": "invalid_" + field, "message": field + " must be a boolean.", "uncertain": False})
        payload: dict[str, Any] = {"query": query.strip(), "type": "auto", "numResults": count}
        if args.get("include_text") or args.get("include_highlights"):
            contents: dict[str, Any] = {}
            if args.get("include_text"):
                contents["text"] = True
            if args.get("include_highlights"):
                contents["highlights"] = {"query": query.strip()}
            payload["contents"] = contents
        return payload

    @staticmethod
    def _exa_contents_payload(args: dict) -> dict:
        urls = args.get("urls")
        if not isinstance(urls, list) or not 1 <= len(urls) <= MAX_CONTENT_URLS:
            raise ProviderToolError({"error": "invalid_arguments", "code": "invalid_urls", "message": "urls must contain between 1 and 5 HTTP(S) URLs.", "uncertain": False})
        for field in ("include_text", "include_highlights"):
            if field in args and not isinstance(args[field], bool):
                raise ProviderToolError({"error": "invalid_arguments", "code": "invalid_" + field, "message": field + " must be a boolean.", "uncertain": False})
        safe_urls = []
        for value in urls:
            if not isinstance(value, str) or len(value) > 2048 or any(ord(char) < 32 for char in value):
                raise ProviderToolError({"error": "invalid_arguments", "code": "invalid_url", "message": "Each URL must be valid HTTP(S) text up to 2048 characters.", "uncertain": False})
            try:
                parsed = urllib.parse.urlsplit(value)
            except ValueError:
                parsed = None
            if parsed is None or parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.username or parsed.password:
                raise ProviderToolError({"error": "invalid_arguments", "code": "invalid_url", "message": "Each URL must be valid HTTP(S) text without embedded credentials.", "uncertain": False})
            safe_urls.append(value)
        payload: dict[str, Any] = {"urls": safe_urls}
        if args.get("include_text", True):
            payload["text"] = True
        if args.get("include_highlights"):
            payload["highlights"] = True
        return payload

    def _request(self, provider: str, method: str, url: str, *, key: str, payload: dict | None = None) -> dict:
        body = None if payload is None else json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        headers = {"Accept": "application/json"}
        if provider == "groq":
            headers["Authorization"] = "Bearer " + key
            headers["User-Agent"] = "CommonsSharedEquipment/1.0"
        else:
            headers["x-api-key"] = key
        if body is not None:
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            response = self.opener(request, timeout=self.timeout)
            with response:
                status = getattr(response, "status", None) or response.getcode()
                raw = response.read(MAX_RESPONSE_BYTES + 1)
                response_headers = response.headers
        except urllib.error.HTTPError as exc:
            body_read_failed = False
            try:
                raw = exc.read(MAX_RESPONSE_BYTES + 1)
            except Exception:
                raw = b""
                body_read_failed = True
            safe_body = None if body_read_failed else self._safe_error_body(raw, key)
            headers = exc.headers or {}
            raise ProviderToolError({
                "error": "provider_http_error",
                "code": "provider_http_error",
                "provider": provider,
                "http_status": int(exc.code),
                "provider_error": safe_body,
                "retry_after": headers.get("Retry-After"),
                "rate_limit_headers": self._rate_headers(headers),
                "provider_request_id": headers.get("x-request-id") or headers.get("request-id"),
                "message": "Provider rejected the request.",
                "uncertain": method == "POST" and int(exc.code) >= 500,
                "error_body_read_failed": body_read_failed,
            }) from None
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise ProviderToolError({
                "error": "provider_network_error",
                "code": type(exc).__name__,
                "provider": provider,
                "message": "Provider request failed at the network layer.",
                "uncertain": method == "POST",
            }) from None
        if len(raw) > MAX_RESPONSE_BYTES:
            raise ProviderToolError({
                "error": "provider_response_too_large",
                "code": "provider_response_too_large",
                "provider": provider,
                "http_status": int(status),
                "message": "Provider response exceeded the local response-size limit.",
                "uncertain": method == "POST",
            })
        try:
            parsed = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            raise ProviderToolError({
                "error": "provider_response_invalid",
                "code": "provider_response_invalid",
                "provider": provider,
                "http_status": int(status),
                "message": "Provider returned a non-JSON response.",
                "uncertain": method == "POST",
            }) from None
        return self._sanitize(parsed, key)

    @staticmethod
    def _safe_error_body(raw: bytes, key: str) -> dict | str | None:
        if len(raw) > MAX_RESPONSE_BYTES:
            return {"truncated": True}
        try:
            parsed = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            return None
        if isinstance(parsed, dict):
            error = parsed.get("error", parsed)
            if isinstance(error, dict):
                result = {}
                for field in ("code", "type", "message", "param"):
                    if isinstance(error.get(field), (str, int, float)):
                        result[field] = error[field]
                return GroqExaEquipment._sanitize(result, key)
            if isinstance(error, str):
                return {"message": GroqExaEquipment._sanitize(error, key)}
        return {"type": "provider_error"}

    @staticmethod
    def _sanitize(value: Any, key: str) -> Any:
        if isinstance(value, str):
            safe = value.replace(key, "[REDACTED]") if key else value
            return redacted(safe)
        if isinstance(value, list):
            return [GroqExaEquipment._sanitize(item, key) for item in value]
        if isinstance(value, dict):
            safe = {}
            for name, item in value.items():
                safe_name = str(name).replace(key, "[REDACTED]") if key else str(name)
                safe[str(redacted(safe_name))] = GroqExaEquipment._sanitize(item, key)
            return safe
        return value

    @staticmethod
    def _rate_headers(headers) -> dict[str, str]:
        allowed = (
            "retry-after",
            "x-ratelimit-limit-requests",
            "x-ratelimit-remaining-requests",
            "x-ratelimit-reset-requests",
            "x-ratelimit-limit-tokens",
            "x-ratelimit-remaining-tokens",
            "x-ratelimit-reset-tokens",
            "x-ratelimit-limit",
            "x-ratelimit-remaining",
            "x-ratelimit-reset",
        )
        return {name: value for name in allowed if (value := headers.get(name)) is not None}
