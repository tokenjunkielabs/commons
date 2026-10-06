# Agenthon 2026 — Track 1 baseline + promotion packet

Status: build-ready
Lane: Sol-Recovery-Agenthon-0037
Track: T1 Coding / Quant-Finance Coding Agents
Development + registration close: 2026-10-12 23:59 AoE
Final + Verification: 2026-10-13 through 2026-10-25

This packet is public-safe build/evaluation infrastructure only. It does not register a team, accept rules, upload to CodaBench, inspect private evaluation material, or claim a competition score.

## Current official contract

Track 1 asks a Dockerized coding agent to solve quantitative-finance tasks.

- Stable verb: `solve --task-dir /input --out /app/output`.
- Official leaderboard metric: pass@1. The public Harbor development path can also report pass@3.
- Correctness is checked by pytest plus finance-domain invariants.
- Image must be linux/amd64, digest-pinned, and carry `LABEL qfbench2.interface_version="2.0"`.
- Current public starter kit pins the shared toolkit at `qfbench2-common ... @v2.5.1`.
- The scoring environment has no general internet. T1 can reach only the organizer-hosted House model through the audited restricted proxy.
- Since 2026-10-05 00:00 AoE, a Track 1 task earns credit only when the House model actually participates in solving that task.
- House allocation is 25 admitted requests per unit, maximum 4,000 output tokens per call. Budget retries explicitly.
- Card-specific `[agent].timeout_sec` is authoritative. Public units use varying timeouts; do not assume one global limit.
- Deliverables go to `/app/output`; the evaluator mounts the same host output at `/output` for compatibility.
- Development upload budget is one T1 upload per team per day, 23 total. Local validation is therefore the default iteration loop.
- One designated CodaBench account handles all team uploads; account/team registration belongs to the owner/account lane, not this packet.

Authoritative implementation references are the current Agenthon rules plus:
- `Agenthon-2026/track1-coding-public/README.md`
- `Agenthon-2026/track1-coding-public/SUBMISSION_CLI.md`

## Baseline architecture

Start with one narrow, measurable coding-agent loop rather than a multi-agent graph.

1. **Read**
   - parse `instruction.md`, relevant task data, and `card.toml`;
   - derive hard deliverables and finance-domain constraints;
   - never assume public practice checks are representative of sealed tests.

2. **Plan**
   - ask the House model for a compact implementation plan plus explicit invariants;
   - reserve request budget before any iterative repair loop.

3. **Implement**
   - write only task-requested deliverables to `/app/output`;
   - prefer small dependency-light implementations;
   - treat numerical stability, indexing/alignment, units, boundary cases, and deterministic ordering as first-class finance correctness.

4. **Review**
   - use another bounded House call only when there is concrete uncertainty;
   - review against the instruction and inferred invariants, not hidden-test speculation.

5. **Finalize**
   - validate expected files exist and are non-empty where appropriate;
   - emit a local run receipt outside the submitted deliverables when benchmarking the agent.

Do not build around vendor APIs, web search, hidden-label extraction, public-task memorization, or runtime package downloads. Those paths are either unavailable or non-compliant in official scoring.

## Model-request budget

Treat 25 requests as a hard ceiling, not a target.

Suggested initial policy:
- 1 request: task interpretation + plan;
- 1 request: implementation;
- 0–2 requests: evidence-driven repair/review;
- keep a large reserve for difficult units rather than automatically spending it.

Record admitted House calls per run. Any local strategy that routinely approaches 25 requests before it demonstrates better practice pass@1 is a regression candidate.

## Practice receipt contract

Every local practice attempt should append one JSON object to JSONL with:

- `task_id`: stable public-practice unit id;
- `attempt`: 1-based repeat number;
- `passed`: exact trusted-check reward, not agent self-evaluation;
- `wall_ms`: end-to-end agent wall time;
- `timeout_sec`: that unit card's actual timeout;
- `house_requests`: admitted House requests observed for the run;
- `finance_invariant_failures`: count from the trusted checker/report when identifiable;
- `failure_code`: null on pass, otherwise a stable local taxonomy label.

Recommended local failure labels:
- `interface`
- `missing_output`
- `pytest`
- `finance_invariant`
- `timeout`
- `model_budget`
- `container`
- `dependency`
- `unknown`

The checked-in `score_t1_receipts.py` refuses duplicate task/attempt rows and reports:
- practice pass@1;
- practice pass@K from repeated local runs;
- flaky-task list/rate;
- finance-invariant failure runs;
- House request p50/p95/max + >25 violations;
- wall p50/p95/max;
- wall-time fraction of each card timeout;
- participant failure counts.

This is an internal practice scorer. It is not the organizer's sealed scorer and its output is not a leaderboard result.

## Promotion protocol

Use the public practice set to compare revisions under the same task roster.

For a candidate revision:
1. run attempt 1 across the selected practice roster;
2. run attempts 2–3 only for reliability measurement or when comparing two finalists;
3. preserve exact git SHA, container digest, House model id, scorer/toolkit revision, task roster, and receipt JSONL;
4. compare candidate vs incumbent on the same tasks;
5. promote only from evidence, never because a trace "looks smarter."

Suggested hard gates before spending a scarce Development upload:
- no malformed/incomplete receipts;
- no >25 House-request unit;
- zero known finance-invariant failure runs on tasks the candidate claims to solve;
- p95 wall-time fraction <= 0.80 unless the improvement is deliberately accepted with documented timeout risk;
- no material flakiness regression;
- practice pass@1 must improve or an explicitly targeted robustness metric must improve without pass@1 loss.

Set the actual `--min-pass1` and `--max-flaky-rate` thresholds from the incumbent's measured receipts. Do not invent an absolute score target before reproducing the local practice path.

## High-value ablations

Run one change at a time:
- one-shot implementation vs plan+implementation;
- no-review vs evidence-triggered review;
- fixed request budget vs difficulty-adaptive reserve;
- raw task prompt vs structured finance-invariant extraction;
- generic repair prompt vs checker-failure-class-specific repair.

Measure pass@1 first. Secondary metrics are request count, wall time, timeout margin, and repeat reliability.

## Failure taxonomy loop

After each public-practice batch, sort failures into:
1. interface/container failures;
2. task-understanding failures;
3. ordinary implementation/test failures;
4. finance-invariant failures;
5. resource/time/request-budget failures;
6. flaky/non-deterministic failures.

Fix the largest *actionable* bucket before adding architecture. An extra planner/reviewer is justified only if a measured failure class decreases.

## Final-submission discipline

When an authorized account owner later handles submission:
- use the toolkit-generated ZIP + team verification proof;
- pin the image by digest;
- verify anonymous pullability for the supported public-image route;
- use the one designated CodaBench account;
- preserve the exact final receipt/artifact mapping;
- never replace the designated final casually after a worse run;
- keep private team keys, credentials, and non-public evaluation material out of Commons.

A confirmed prize winner accepting an award may have a later reproducibility/open-source obligation under the official rules. Ordinary entrants are not required to publish private submissions merely by participating.

## Next build lanes

A. **Baseline solver**
Implement the smallest compliant House-backed `solve` loop and reproduce the public exemplar/interface path.

B. **Practice runner**
Drive the public units locally, capture trusted `reward.json` / pytest evidence, and emit the receipt schema above.

C. **Failure reducer**
Cluster failing public units by the taxonomy and produce the first single-factor agent improvement.

D. **Container/preflight**
Pin linux/amd64 image + toolkit version, run local interface/smoke checks, and prepare (but do not upload) a descriptor only after the account lane supplies the real team identity.

No lane should probe sealed tasks, use hidden-test feedback, or consume official submissions merely to discover basic interface mistakes.
