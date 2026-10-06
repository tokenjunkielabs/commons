#!/usr/bin/env python3
"""Deterministic acceptance scorer for the Alexa+ MCP reliability demo."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

ALLOWED_OUTCOMES = {"success", "recovered", "failed"}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, 1):
            line = raw.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number}: each result must be a JSON object")
            rows.append(value)
    return rows


def percentile(values: list[float], fraction: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * fraction
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def ratio(numerator: int, denominator: int) -> float | None:
    return None if denominator == 0 else numerator / denominator


def require_bool(row: dict[str, Any], key: str, case_id: str) -> bool:
    value = row.get(key)
    if not isinstance(value, bool):
        raise ValueError(f"{case_id}: result field {key!r} must be boolean")
    return value


def require_non_negative_int(row: dict[str, Any], key: str, case_id: str) -> int:
    value = row.get(key)
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{case_id}: result field {key!r} must be a non-negative integer")
    return value


def validate(fixtures: list[dict[str, Any]], results: list[dict[str, Any]]) -> dict[str, Any]:
    fixture_by_id: dict[str, dict[str, Any]] = {}
    for case in fixtures:
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            raise ValueError("every fixture requires a non-empty string id")
        if case_id in fixture_by_id:
            raise ValueError(f"duplicate fixture id: {case_id}")
        max_retries = case.get("max_retries")
        if not isinstance(max_retries, int) or isinstance(max_retries, bool) or max_retries < 0:
            raise ValueError(f"{case_id}: max_retries must be a non-negative integer")
        if not isinstance(case.get("expect_resume"), bool):
            raise ValueError(f"{case_id}: expect_resume must be boolean")
        injection = case.get("injection")
        if injection not in {"none", "tool_timeout", "process_restart"}:
            raise ValueError(f"{case_id}: unsupported injection {injection!r}")
        fixture_by_id[case_id] = case

    result_by_id: dict[str, dict[str, Any]] = {}
    for row in results:
        case_id = row.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            raise ValueError("every result requires a non-empty string case_id")
        if case_id in result_by_id:
            raise ValueError(f"duplicate result case_id: {case_id}")
        result_by_id[case_id] = row

    missing = sorted(set(fixture_by_id) - set(result_by_id))
    extra = sorted(set(result_by_id) - set(fixture_by_id))
    if missing or extra:
        raise ValueError(f"result set mismatch: missing={missing} extra={extra}")

    completed = 0
    recovered = 0
    injected = 0
    injected_recovered = 0
    resume_cases = 0
    resume_successes = 0
    retry_violations = 0
    duplicate_side_effect_cases = 0
    evidence_incomplete = 0
    latency_ms: list[float] = []

    for case_id, case in fixture_by_id.items():
        row = result_by_id[case_id]
        outcome = row.get("outcome")
        if outcome not in ALLOWED_OUTCOMES:
            raise ValueError(f"{case_id}: outcome must be one of {sorted(ALLOWED_OUTCOMES)}")

        wall_ms = row.get("wall_ms")
        if not isinstance(wall_ms, (int, float)) or isinstance(wall_ms, bool) or wall_ms < 0:
            raise ValueError(f"{case_id}: wall_ms must be a non-negative number")
        latency_ms.append(float(wall_ms))

        retry_count = require_non_negative_int(row, "retry_count", case_id)
        duplicate_side_effects = require_non_negative_int(row, "duplicate_side_effects", case_id)
        resumed = require_bool(row, "resumed", case_id)
        evidence_complete = require_bool(row, "evidence_complete", case_id)

        if outcome != "failed":
            completed += 1
        if outcome == "recovered":
            recovered += 1

        if case["injection"] != "none":
            injected += 1
            if outcome == "recovered":
                injected_recovered += 1

        if case["expect_resume"]:
            resume_cases += 1
            if resumed and outcome != "failed":
                resume_successes += 1

        if retry_count > case["max_retries"]:
            retry_violations += 1
        if duplicate_side_effects:
            duplicate_side_effect_cases += 1
        if not evidence_complete:
            evidence_incomplete += 1

    return {
        "cases": len(fixtures),
        "completion_rate": ratio(completed, len(fixtures)),
        "clean_or_recovered": completed,
        "recovered_cases": recovered,
        "injected_failure_cases": injected,
        "injected_failure_recovery_rate": ratio(injected_recovered, injected),
        "resume_cases": resume_cases,
        "resume_success_rate": ratio(resume_successes, resume_cases),
        "retry_budget_violations": retry_violations,
        "duplicate_side_effect_cases": duplicate_side_effect_cases,
        "evidence_incomplete_cases": evidence_incomplete,
        "latency_ms": {
            "p50": percentile(latency_ms, 0.50),
            "p95": percentile(latency_ms, 0.95),
            "max": max(latency_ms) if latency_ms else None,
        },
    }


def gate(metrics: dict[str, Any], args: argparse.Namespace) -> list[str]:
    failures: list[str] = []

    completion_rate = metrics["completion_rate"]
    if completion_rate is None or completion_rate < args.min_completion:
        failures.append(
            f"completion_rate {completion_rate!r} < required {args.min_completion:.3f}"
        )

    recovery_rate = metrics["injected_failure_recovery_rate"]
    if metrics["injected_failure_cases"] and (
        recovery_rate is None or recovery_rate < args.min_recovery
    ):
        failures.append(
            "injected_failure_recovery_rate "
            f"{recovery_rate!r} < required {args.min_recovery:.3f}"
        )

    resume_rate = metrics["resume_success_rate"]
    if metrics["resume_cases"] and (resume_rate is None or resume_rate < args.min_resume):
        failures.append(
            f"resume_success_rate {resume_rate!r} < required {args.min_resume:.3f}"
        )

    if metrics["retry_budget_violations"] > args.max_retry_violations:
        failures.append(
            f"retry_budget_violations {metrics['retry_budget_violations']} "
            f"> allowed {args.max_retry_violations}"
        )

    if metrics["duplicate_side_effect_cases"] > args.max_duplicate_side_effect_cases:
        failures.append(
            f"duplicate_side_effect_cases {metrics['duplicate_side_effect_cases']} "
            f"> allowed {args.max_duplicate_side_effect_cases}"
        )

    if metrics["evidence_incomplete_cases"] > args.max_evidence_incomplete:
        failures.append(
            f"evidence_incomplete_cases {metrics['evidence_incomplete_cases']} "
            f"> allowed {args.max_evidence_incomplete}"
        )

    if args.max_p95_ms is not None:
        p95 = metrics["latency_ms"]["p95"]
        if p95 is None or p95 > args.max_p95_ms:
            failures.append(
                f"latency p95 {p95!r}ms > allowed {args.max_p95_ms:.1f}ms"
            )

    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--min-completion", type=float, default=1.0)
    parser.add_argument("--min-recovery", type=float, default=1.0)
    parser.add_argument("--min-resume", type=float, default=1.0)
    parser.add_argument("--max-retry-violations", type=int, default=0)
    parser.add_argument("--max-duplicate-side-effect-cases", type=int, default=0)
    parser.add_argument("--max-evidence-incomplete", type=int, default=0)
    parser.add_argument("--max-p95-ms", type=float)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        fixture_document = load_json(args.fixtures)
        fixtures = fixture_document.get("cases")
        if not isinstance(fixtures, list):
            raise ValueError("fixtures document requires a top-level cases array")
        results = load_jsonl(args.results)
        metrics = validate(fixtures, results)
        failures = gate(metrics, args)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(metrics, indent=2, sort_keys=True))
    if failures:
        print("GATE: FAIL", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print("GATE: PASS", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
