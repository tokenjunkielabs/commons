#!/usr/bin/env python3
"""Score evidence-bound microscopy QC receipts.

This is a competition benchmark contract, not a medical/clinical evaluator.
Inputs are JSONL so deterministic QC and an agent triage layer can be compared
under the same frozen cases.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
from pathlib import Path
from typing import Any

SYSTEMS = ("deterministic_qc", "agent_triage")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, 1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_no}: each row must be an object")
            rows.append(row)
    if not rows:
        raise ValueError(f"{path}: no rows")
    return rows


def _str_list(row: dict[str, Any], key: str) -> list[str]:
    value = row.get(key)
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise ValueError(f"{row.get('case_id', '<unknown>')}: {key} must be a list of non-empty strings")
    if len(value) != len(set(value)):
        raise ValueError(f"{row.get('case_id', '<unknown>')}: {key} contains duplicates")
    return value


def _load_manifest(path: Path) -> dict[str, dict[str, Any]]:
    rows = _load_jsonl(path)
    manifest: dict[str, dict[str, Any]] = {}
    for row in rows:
        case_id = row.get("case_id")
        kind = row.get("kind")
        source_url = row.get("source_url")
        license_name = row.get("license")
        if not isinstance(case_id, str) or not case_id:
            raise ValueError("manifest: case_id must be a non-empty string")
        if case_id in manifest:
            raise ValueError(f"manifest: duplicate case_id {case_id}")
        if kind not in {"synthetic", "public"}:
            raise ValueError(f"{case_id}: manifest kind must be synthetic or public")
        if not isinstance(source_url, str) or not source_url:
            raise ValueError(f"{case_id}: source_url is required")
        if not isinstance(license_name, str) or not license_name:
            raise ValueError(f"{case_id}: license is required")
        if kind == "synthetic":
            if not source_url.startswith("repository://"):
                raise ValueError(f"{case_id}: synthetic source_url must use repository://")
            if not isinstance(row.get("generator_tag"), str) or not row["generator_tag"]:
                raise ValueError(f"{case_id}: synthetic generator_tag is required")
        else:
            digest = row.get("sha256")
            if not source_url.startswith(("https://", "http://")):
                raise ValueError(f"{case_id}: public source_url must be http(s)")
            if not isinstance(digest, str) or not HEX64.fullmatch(digest):
                raise ValueError(f"{case_id}: public rows require lowercase sha256")
        manifest[case_id] = row
    return manifest


def _percentile_nearest_rank(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("cannot score an empty latency set")
    ordered = sorted(values)
    index = max(0, math.ceil(q * len(ordered)) - 1)
    return ordered[index]


def _score_system(rows: list[dict[str, Any]]) -> dict[str, Any]:
    tp = fp = fn = 0
    clean_cases = false_flag_cases = 0
    citation_valid_cases = abstention_correct = 0
    latencies: list[float] = []

    for row in rows:
        expected = set(_str_list(row, "expected_defects"))
        predicted = set(_str_list(row, "predicted_defects"))
        evidence_catalog = set(_str_list(row, "evidence_catalog"))
        cited = set(_str_list(row, "cited_evidence"))

        expected_abstain = row.get("expected_abstain")
        abstained = row.get("abstained")
        latency_ms = row.get("latency_ms")
        if not isinstance(expected_abstain, bool) or not isinstance(abstained, bool):
            raise ValueError(f"{row['case_id']}: abstention fields must be booleans")
        if not isinstance(latency_ms, (int, float)) or isinstance(latency_ms, bool) or latency_ms < 0:
            raise ValueError(f"{row['case_id']}: latency_ms must be a non-negative number")

        tp += len(expected & predicted)
        fp += len(predicted - expected)
        fn += len(expected - predicted)

        if not expected:
            clean_cases += 1
            false_flag_cases += int(bool(predicted))

        citations_ok = cited.issubset(evidence_catalog) and (not predicted or bool(cited))
        citation_valid_cases += int(citations_ok)
        abstention_correct += int(expected_abstain == abstained)
        latencies.append(float(latency_ms))

    precision = tp / (tp + fp) if tp + fp else 1.0
    recall = tp / (tp + fn) if tp + fn else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    return {
        "cases": len(rows),
        "defect_tp": tp,
        "defect_fp": fp,
        "defect_fn": fn,
        "defect_precision": precision,
        "defect_recall": recall,
        "defect_f1": f1,
        "clean_false_flag_rate": false_flag_cases / clean_cases if clean_cases else 0.0,
        "citation_validity_rate": citation_valid_cases / len(rows),
        "abstention_accuracy": abstention_correct / len(rows),
        "latency_ms": {
            "p50": statistics.median(latencies),
            "p95": _percentile_nearest_rank(latencies, 0.95),
        },
    }


def score(manifest_path: Path, receipts_path: Path) -> dict[str, Any]:
    manifest = _load_manifest(manifest_path)
    receipts = _load_jsonl(receipts_path)
    grouped: dict[str, list[dict[str, Any]]] = {name: [] for name in SYSTEMS}
    seen: set[tuple[str, str]] = set()

    for row in receipts:
        case_id = row.get("case_id")
        system = row.get("system")
        if not isinstance(case_id, str) or case_id not in manifest:
            raise ValueError(f"receipt references unknown case_id {case_id!r}")
        if system not in grouped:
            raise ValueError(f"{case_id}: system must be one of {SYSTEMS}")
        key = (case_id, system)
        if key in seen:
            raise ValueError(f"duplicate receipt for case/system {key}")
        seen.add(key)
        grouped[system].append(row)

    expected_cases = set(manifest)
    for system, rows in grouped.items():
        actual_cases = {row["case_id"] for row in rows}
        missing = sorted(expected_cases - actual_cases)
        extra = sorted(actual_cases - expected_cases)
        if missing or extra:
            raise ValueError(f"{system}: case coverage mismatch missing={missing} extra={extra}")

    systems = {name: _score_system(grouped[name]) for name in SYSTEMS}
    baseline = systems["deterministic_qc"]
    candidate = systems["agent_triage"]
    return {
        "schema_version": 1,
        "case_count": len(manifest),
        "systems": systems,
        "agent_minus_deterministic": {
            "defect_f1": candidate["defect_f1"] - baseline["defect_f1"],
            "clean_false_flag_rate": candidate["clean_false_flag_rate"] - baseline["clean_false_flag_rate"],
            "citation_validity_rate": candidate["citation_validity_rate"] - baseline["citation_validity_rate"],
            "abstention_accuracy": candidate["abstention_accuracy"] - baseline["abstention_accuracy"],
            "p50_latency_ms": candidate["latency_ms"]["p50"] - baseline["latency_ms"]["p50"],
            "p95_latency_ms": candidate["latency_ms"]["p95"] - baseline["latency_ms"]["p95"],
        },
        "evidence_boundary": "Metrics describe only the supplied frozen receipts; they are not clinical-validity claims.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--receipts", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = score(args.manifest, args.receipts)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
