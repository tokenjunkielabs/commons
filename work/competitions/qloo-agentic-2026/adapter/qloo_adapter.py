from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence

JsonObject = Mapping[str, Any]
Transport = Callable[[str, Mapping[str, str], Mapping[str, Any], float], JsonObject]

SUPPORTED_FILTER_TYPES = frozenset(
    {
        "urn:entity:artist",
        "urn:entity:book",
        "urn:entity:brand",
        "urn:entity:destination",
        "urn:entity:movie",
        "urn:entity:person",
        "urn:entity:place",
        "urn:entity:podcast",
        "urn:entity:tv_show",
        "urn:entity:videogame",
        "urn:heatmap",
    }
)


class QlooAdapterError(RuntimeError):
    """Stable adapter failure with a machine-readable code."""

    def __init__(self, code: str, message: str, *, status: int | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.status = status


@dataclass(frozen=True)
class QlooEntity:
    entity_id: str
    name: str
    entity_type: str | None
    affinity: float | None
    properties: Mapping[str, Any]
    evidence: Mapping[str, Any]


@dataclass(frozen=True)
class QlooInsightsResult:
    state: str
    entities: tuple[QlooEntity, ...]
    duration_ms: float | None
    warning: str | None
    raw_query: Mapping[str, Any]


class QlooClient:
    """Narrow Qloo Insights adapter for the TasteBench planner.

    This boundary intentionally exposes only the endpoint/parameters needed by
    the three benchmark scenarios. It never falls back to generic, invented
    recommendations when Qloo returns no evidence.
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.qloo.com",
        timeout_seconds: float = 10.0,
        transport: Transport | None = None,
    ) -> None:
        if not api_key.strip():
            raise QlooAdapterError("missing_api_key", "Qloo API key is required")
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds
        self._transport = transport or _post_json

    def insights(
        self,
        *,
        filter_type: str,
        interest_entity_ids: Sequence[str] = (),
        interest_entity_queries: Sequence[str] = (),
        interest_tags: Sequence[str] = (),
        location_query: str | None = None,
        take: int = 10,
    ) -> QlooInsightsResult:
        if filter_type not in SUPPORTED_FILTER_TYPES:
            raise QlooAdapterError(
                "invalid_filter_type",
                f"Unsupported Qloo filter.type: {filter_type}",
            )
        if take < 1 or take > 50:
            raise QlooAdapterError("invalid_take", "Qloo take must be between 1 and 50")
        if not (
            interest_entity_ids
            or interest_entity_queries
            or interest_tags
            or (location_query and location_query.strip())
        ):
            raise QlooAdapterError(
                "missing_signal",
                "At least one Qloo interest or location signal is required",
            )

        payload: dict[str, Any] = {
            "filter.type": filter_type,
            "feature.explainability": True,
            "take": take,
        }
        if interest_entity_ids:
            payload["signal.interests.entities"] = list(interest_entity_ids)
        if interest_entity_queries:
            payload["signal.interests.entities.query"] = list(interest_entity_queries)
        if interest_tags:
            payload["signal.interests.tags"] = ",".join(interest_tags)
        if location_query and location_query.strip():
            payload["filter.location.query"] = location_query.strip()

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": self._api_key,
        }

        try:
            response = self._transport(
                f"{self._base_url}/v2/insights",
                headers,
                payload,
                self._timeout_seconds,
            )
        except QlooAdapterError:
            raise
        except Exception as exc:
            raise QlooAdapterError(
                "transport_error",
                f"Qloo request failed: {type(exc).__name__}",
            ) from exc

        if response.get("success") is False:
            raise QlooAdapterError("api_error", "Qloo returned an unsuccessful response")

        results = response.get("results")
        if not isinstance(results, Mapping):
            raise QlooAdapterError("malformed_response", "Qloo response is missing results")

        raw_entities = results.get("entities", [])
        if raw_entities is None:
            raw_entities = []
        if not isinstance(raw_entities, list):
            raise QlooAdapterError(
                "malformed_response",
                "Qloo results.entities must be a list",
            )

        entities = tuple(_normalize_entity(item) for item in raw_entities if isinstance(item, Mapping))

        raw_query = response.get("query")
        if not isinstance(raw_query, Mapping):
            raw_query = {}

        warning = _explainability_warning(raw_query)
        duration = response.get("duration")
        duration_ms = float(duration) if isinstance(duration, (int, float)) else None

        return QlooInsightsResult(
            state="ok" if entities else "empty",
            entities=entities,
            duration_ms=duration_ms,
            warning=warning,
            raw_query=raw_query,
        )


def _normalize_entity(raw: Mapping[str, Any]) -> QlooEntity:
    entity_id = raw.get("entity_id") or raw.get("id")
    if not isinstance(entity_id, str) or not entity_id:
        raise QlooAdapterError(
            "malformed_response",
            "Qloo entity is missing entity_id",
        )

    properties = raw.get("properties")
    if not isinstance(properties, Mapping):
        properties = {}

    name = raw.get("name") or properties.get("name") or entity_id
    if not isinstance(name, str):
        name = entity_id

    entity_type = raw.get("type") or raw.get("subtype")
    if not isinstance(entity_type, str):
        entity_type = None

    query = raw.get("query")
    if not isinstance(query, Mapping):
        query = {}

    affinity_raw = query.get("affinity", raw.get("affinity"))
    affinity = float(affinity_raw) if isinstance(affinity_raw, (int, float)) else None

    evidence = query.get("explainability")
    if not isinstance(evidence, Mapping):
        evidence = {}

    return QlooEntity(
        entity_id=entity_id,
        name=name,
        entity_type=entity_type,
        affinity=affinity,
        properties=dict(properties),
        evidence=dict(evidence),
    )


def _explainability_warning(query: Mapping[str, Any]) -> str | None:
    explainability = query.get("explainability")
    if not isinstance(explainability, Mapping):
        return None
    warning = explainability.get("warning")
    return warning if isinstance(warning, str) and warning else None


def _post_json(
    url: str,
    headers: Mapping[str, str],
    payload: Mapping[str, Any],
    timeout_seconds: float,
) -> JsonObject:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=dict(headers),
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            body = response.read()
    except urllib.error.HTTPError as exc:
        raise QlooAdapterError(
            "http_error",
            f"Qloo returned HTTP {exc.code}",
            status=exc.code,
        ) from exc
    except urllib.error.URLError as exc:
        raise QlooAdapterError("transport_error", "Qloo transport failed") from exc

    try:
        decoded = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise QlooAdapterError(
            "malformed_response",
            "Qloo returned non-JSON content",
        ) from exc

    if not isinstance(decoded, Mapping):
        raise QlooAdapterError(
            "malformed_response",
            "Qloo response root must be an object",
        )
    return decoded
