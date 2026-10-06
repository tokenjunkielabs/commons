#!/usr/bin/env python3
"""Score TasteBench Planner JSONL evaluation receipts.

No network access is performed. The scorer treats receipts as evidence and
fails loudly when required fields are missing or internally inconsistent.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

REQUIRED_FIELDS = {
    "prompt_id", "scenario", "run_id", "material_claims", "grounded_claims",
    "hard_constraints", "constraints_satisfied", "latency_ms", "ranked_ids",
    "qloo_calls", "failure_injected", "fabricated_claims",
}

def load_jsonl(path: Path) -> list[dict[str, Any]]:
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
            missing = REQUIRED_FIELDS - row.keys()
            if missing:
                raise ValueError(f"{path}:{line_no}: missing required fields: {sorted(missing)}")
            validate_row(row, path, line_no)
            rows.append(row)
    if not rows:
        raise ValueError(f"{path}: no receipts")
    return rows

def validate_row(row: dict[str, Any], path: Path, line_no: int) -> None:
    for key in ("material_claims", "grounded_claims", "hard_constraints",
                "constraints_satisfied", "latency_ms", "qloo_calls",
                "fabricated_claims"):
        value = row[key]
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
            raise ValueError(f"{path}:{line_no}: {key} must be a non-negative number")
    if row["grounded_claims"] > row["material_claims"]:
        raise ValueError(f"{path}:{line_no}: grounded_claims exceeds material_claims")
    if row["constraints_satisfied"] > row["hard_constraints"]:
        raise ValueError(f"{path}:{line_no}: constraints_satisfied exceeds hard_constraints")
    if not isinstance(row["ranked_ids"], list):
        raise ValueError(f"{path}:{line_no}: ranked_ids must be a list")
    if not isinstance(row["failure_injected"], bool):
        raise ValueError(f"{path}:{line_no}: failure_injected must be boolean")
    if "ablation_winner" in row and row["ablation_winner"] not in ("full", "ablation", "tie", None):
        raise ValueError(f"{path}:{line_no}: ablation_winner must be full/ablation/tie/null")

def ratio(num: float, den: float) -> float | None:
    return None if den == 0 else num / den

def percentile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("percentile requires at least one value")
    if len(ordered) == 1:
        return ordered[0]
    rank = (len(ordered) - 1) * p
    lo, hi = math.floor(rank), math.ceil(rank)
    if lo == hi:
        return ordered[lo]
    weight = rank - lo
    return ordered[lo] * (1.0 - weight) + ordered[hi] * weight

def jaccard_churn(a: Iterable[str], b: Iterable[str]) -> float:
    left, right = set(a), set(b)
    union = left | right
    return 0.0 if not union else 1.0 - len(left & right) / len(union)

def stability(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_prompt: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_prompt[str(row["prompt_id"])].append(row)
    churns: list[float] = []
    hard_regressions = 0
    repeated_prompts = 0
    for prompt_rows in by_prompt.values():
        prompt_rows.sort(key=lambda item: str(item["run_id"]))
        if len(prompt_rows) < 2:
            continue
        repeated_prompts += 1
        baseline = prompt_rows[0]
        for current in prompt_rows[1:]:
            churns.append(jaccard_churn(baseline["ranked_ids"], current["ranked_ids"]))
            if current["constraints_satisfied"] < current["hard_constraints"]:
                hard_regressions += 1
    return {
        "repeated_prompts": repeated_prompts,
        "comparisons": len(churns),
        "mean_rank_set_churn": statistics.fmean(churns) if churns else None,
        "max_rank_set_churn": max(churns) if churns else None,
        "hard_constraint_regressions": hard_regressions,
    }

def _count(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    out: dict[str, int] = defaultdict(int)
    for row in rows:
        out[str(row[field])] += 1
    return dict(out)

def _at_least(value: float | None, threshold: float) -> bool | None:
    return None if value is None else value >= threshold

def _at_most(value: float | None, threshold: float) -> bool | None:
    return None if value is None else value <= threshold

def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total_material = sum(row["material_claims"] for row in rows)
    total_grounded = sum(row["grounded_claims"] for row in rows)
    total_constraints = sum(row["hard_constraints"] for row in rows)
    total_satisfied = sum(row["constraints_satisfied"] for row in rows)
    latencies = [float(row["latency_ms"]) for row in rows]
    failures = [row for row in rows if row["failure_injected"]]
    closed_failures = [
        row for row in failures
        if row["fabricated_claims"] == 0
        and row["constraints_satisfied"] == row["hard_constraints"]
    ]
    judged = [row for row in rows if row.get("ablation_winner") in ("full", "ablation", "tie")]
    full_wins = sum(row.get("ablation_winner") == "full" for row in judged)
    decisive = sum(row.get("ablation_winner") in ("full", "ablation") for row in judged)
    metrics = {
        "receipt_count": len(rows),
        "prompt_count": len({row["prompt_id"] for row in rows}),
        "scenario_counts": dict(sorted(_count(rows, "scenario").items())),
        "api_grounding_rate": ratio(total_grounded, total_material),
        "constraint_satisfaction_rate": ratio(total_satisfied, total_constraints),
        "latency_ms": {
            "p50": percentile(latencies, 0.50),
            "p95": percentile(latencies, 0.95),
            "max": max(latencies),
        },
        "qloo_calls": {
            "total": sum(row["qloo_calls"] for row in rows),
            "mean_per_receipt": statistics.fmean(row["qloo_calls"] for row in rows),
        },
        "failure_quality_rate": ratio(len(closed_failures), len(failures)),
        "failure_cases": len(failures),
        "ablation": {
            "judged_pairs": len(judged),
            "decisive_pairs": decisive,
            "full_wins": full_wins,
            "full_win_rate_decisive": ratio(full_wins, decisive),
        },
        "stability": stability(rows),
    }
    metrics["gates"] = {
        "grounding_ge_95pct": _at_least(metrics["api_grounding_rate"], 0.95),
        "constraints_100pct": _at_least(metrics["constraint_satisfaction_rate"], 1.0),
        "ablation_full_wins_ge_70pct": _at_least(metrics["ablation"]["full_win_rate_decisive"], 0.70),
        "failure_quality_100pct": _at_least(metrics["failure_quality_rate"], 1.0),
        "stability_no_hard_regressions": metrics["stability"]["hard_constraint_regressions"] == 0,
        "stability_churn_le_20pct": _at_most(metrics["stability"]["max_rank_set_churn"], 0.20),
    }
    return metrics

def markdown(summary: dict[str, Any]) -> str:
    def pct(value: float | None) -> str:
        return "n/a" if value is None else f"{value * 100:.1f}%"
    lat, abl, stab = summary["latency_ms"], summary["ablation"], summary["stability"]
    rows = [
        ("Receipts", str(summary["receipt_count"])),
        ("Prompts", str(summary["prompt_count"])),
        ("API grounding", pct(summary["api_grounding_rate"])),
        ("Constraint satisfaction", pct(summary["constraint_satisfaction_rate"])),
        ("Failure quality", pct(summary["failure_quality_rate"])),
        ("Ablation full-agent wins", pct(abl["full_win_rate_decisive"])),
        ("Latency p50", f"{lat['p50']:.1f} ms"),
        ("Latency p95", f"{lat['p95']:.1f} ms"),
        ("Max rank-set churn", pct(stab["max_rank_set_churn"])),
        ("Hard-constraint regressions", str(stab["hard_constraint_regressions"])),
    ]
    out = ["| Metric | Value |", "| --- | ---: |"]
    out.extend(f"| {name} | {value} |" for name, value in rows)
    out.extend(["", "### Gates", ""])
    for name, value in summary["gates"].items():
        marker = "PASS" if value is True else "FAIL" if value is False else "N/A"
        out.append(f"- **{marker}** `{name}`")
    return "\n".join(out) + "\n"

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipts", type=Path, help="JSONL evaluation receipts")
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--markdown-out", type=Path)
    args = parser.parse_args()
    summary = summarize(load_jsonl(args.receipts))
    rendered_json = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    rendered_md = markdown(summary)
    if args.json_out:
        args.json_out.write_text(rendered_json, encoding="utf-8")
    if args.markdown_out:
        args.markdown_out.write_text(rendered_md, encoding="utf-8")
    if not args.json_out and not args.markdown_out:
        print(rendered_json, end="")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
