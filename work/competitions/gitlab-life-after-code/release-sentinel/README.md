# Release Sentinel promotion oracle

Public-safe staging packet for the GitLab **Life After Code** Release Sentinel lane.

This directory contains a small receipt evaluator plus four deterministic fixtures for checking promotion/block decisions before any real GitLab Duo Agent Platform integration.

## Contents

- `release_sentinel_eval.py` — validates lifecycle stages, HTTPS evidence, autonomy/approval semantics, expected-vs-actual decisions, failed-stage fail-closed behavior, and cross-stage evidence reuse.
- `fixtures/golden-promote.json` — valid promotion path.
- `fixtures/expected-security-block.json` — valid block with a failed security stage.
- `fixtures/unsafe-promotion.json` — invalid promotion after a failed stage.
- `fixtures/reused-evidence.json` — invalid receipt that reuses one evidence URL across stages.

## Focused checks

Run from this directory:

```bash
python release_sentinel_eval.py fixtures/golden-promote.json
python release_sentinel_eval.py fixtures/expected-security-block.json
python release_sentinel_eval.py fixtures/unsafe-promotion.json
python release_sentinel_eval.py fixtures/reused-evidence.json
```

Expected behavior:

| Fixture | Expected result |
| --- | --- |
| golden-promote | exit 0; `valid=true`; `correct_decision=true`; completeness 1.0 |
| expected-security-block | exit 0; `valid=true`; security appears in `failed_stages` |
| unsafe-promotion | exit 2; promotion-after-failure and decision-mismatch errors |
| reused-evidence | exit 2; cross-stage evidence reuse rejected |

## Evidence boundary

The fixture URLs are synthetic examples. This staging packet is **not** evidence of a GitLab Duo run, deployment, release, or competition submission.

A real evaluation must replace fixture evidence with HTTPS receipts from the actual GitLab trigger/job/environment/session chain. Promotion evidence should remain tied to the exact run being judged; reused or missing stage evidence must fail closed.

Relevant public GitLab documentation:

- https://docs.gitlab.com/user/duo_agent_platform/flows/custom_flows_schema/
- https://docs.gitlab.com/user/get_started/get_started_agent_platform/
