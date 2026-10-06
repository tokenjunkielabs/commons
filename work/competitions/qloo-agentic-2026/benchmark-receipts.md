# TasteBench benchmark receipt contract

This directory contains the internal benchmark harness for the Qloo Agentic 2026 build packet.

## Scorer

`score_receipts.py` is offline and deterministic. It does not call Qloo, a model provider, or any network service. It consumes one JSON object per line and reports:

- API-grounding rate;
- hard-constraint satisfaction;
- p50 / p95 / max end-to-end latency;
- Qloo call count;
- fail-closed quality for injected upstream failures;
- blind ablation win rate;
- rank-set stability across repeated runs.

The gate thresholds match `intake-and-benchmark-plan.md`: grounding >= 95%, constraints = 100%, full-agent ablation wins >= 70% of decisive pairs, failure quality = 100%, no repeated-run hard-constraint regressions, and rank-set churn <= 20%.

## Required receipt fields

Each line must include:

| Field | Type | Meaning |
| --- | --- | --- |
| `prompt_id` | string | Stable eval-case identifier. |
| `scenario` | string | Scenario family, currently launch / adjacency / travel. |
| `run_id` | string | Stable run identifier used to order repeats. |
| `material_claims` | number | Recommendation claims that require evidence. |
| `grounded_claims` | number | Material claims tied to returned Qloo evidence. |
| `hard_constraints` | number | Machine-checkable hard constraints in the case. |
| `constraints_satisfied` | number | Hard constraints satisfied in final output. |
| `latency_ms` | number | End-to-end wall latency for the run. |
| `ranked_ids` | string[] | Stable candidate IDs in final rank order. |
| `qloo_calls` | number | Qloo API calls issued by the production planner. |
| `failure_injected` | boolean | Whether this run intentionally degraded upstream evidence. |
| `fabricated_claims` | number | Unsupported taste claims emitted despite missing/invalid evidence. |

Optional `ablation_winner` is one of `full`, `ablation`, `tie`, or null after blind-pair judging.

## Example

```json
{"prompt_id":"travel-01","scenario":"travel","run_id":"full-01","material_claims":12,"grounded_claims":12,"hard_constraints":4,"constraints_satisfied":4,"latency_ms":1840,"ranked_ids":["q1","q7","q2"],"qloo_calls":3,"failure_injected":false,"fabricated_claims":0,"ablation_winner":"full"}
```

Run:

```bash
python work/competitions/qloo-agentic-2026/score_receipts.py receipts.jsonl \
  --json-out benchmark-summary.json \
  --markdown-out benchmark-summary.md
```

The scorer validates numeric bounds before aggregating and rejects malformed or internally inconsistent receipts rather than silently scoring them.
