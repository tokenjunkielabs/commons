# PayPal AI Hackathon 2026 — Integration Doctor intake + benchmark build packet

Status: qualified for build  
Submission deadline: 2026-11-12

Official source:
- https://paypalaihackathon.devpost.com/rules

Optional sponsor resources:
- https://paypalaihackathon.devpost.com/details/apimatic
- https://paypalaihackathon.devpost.com/details/postman
- https://paypalaihackathon.devpost.com/details/aggrid

## Sponsor constraints and judging

The official rules require a functioning project, a public open-source GitHub repository, clear setup/run instructions or a hosted interactive demo, and a public demonstration video under three minutes. Existing projects are eligible only when significantly updated during the competition period.

Judging is equally weighted across:

- Technological Implementation;
- Design;
- Potential Impact;
- Innovation / Idea;
- Presentation.

The prize table includes $12,000 / $8,000 / $5,000 grand prizes, $5,000 honorable-mention categories, and sponsor prizes.

## Recommended build: PayPal Integration Doctor

Build an AI-assisted developer tool that diagnoses broken PayPal integrations from **sanitized** request/response traces, webhook samples, test failures, and local project context.

Core flow:

1. ingest a failing sandbox trace, webhook sample, or test failure;
2. classify the failure stage;
3. retrieve the smallest relevant evidence set from trace + project source;
4. rank likely root causes;
5. abstain when evidence is insufficient;
6. propose the smallest bounded repair;
7. generate a focused regression artifact or Postman request;
8. rerun local/sandbox validation;
9. produce a before/after diagnostic receipt.

This keeps PayPal central to the product while making the result objectively benchmarkable.

## Acceptance contract

A demo build is not ready until it can:

- parse a stable sanitized trace schema;
- distinguish authentication, request-shape, idempotency, webhook/event, state-transition, and integration/config failures;
- cite the exact evidence supporting each diagnosis;
- explicitly abstain on ambiguous/incomplete evidence;
- emit a minimal suggested repair instead of a broad rewrite;
- generate one focused regression artifact;
- compare before/after validation behavior;
- redact credentials and sensitive integration material from captured output.

## Frozen benchmark corpus

Use at least 50 deterministic cases:

- 10 request-schema failures;
- 10 authentication/configuration failures;
- 10 webhook/event-processing failures;
- 10 duplicate/idempotency failures;
- 10 ambiguous or incomplete traces.

For every case preserve:

- fixture version/hash;
- expected failure class;
- expected evidence pointers;
- acceptable root-cause set;
- expected abstention state, if applicable;
- validation command;
- latency and tool-call receipt.

## Primary metrics

Track:

- root-cause top-1 accuracy;
- root-cause top-3 recall;
- false-confident diagnosis rate;
- focused repair success rate;
- generated-regression validity;
- p50/p95 diagnosis latency;
- p50/p95 repair-to-validation latency;
- files inspected before first relevant file;
- tool calls per solved case.

A stronger model/agent graph must improve repair success or diagnosis accuracy **without increasing false confidence**.

## Architecture

Keep the implementation narrow:

- **Trace normalizer** — stable sanitized PayPal request/response/event schema.
- **Failure classifier** — bounded failure taxonomy.
- **Evidence retriever** — trace + local-source evidence only.
- **Repair planner** — smallest proposed code/config change.
- **Regression generator** — focused test or Postman artifact.
- **Validator** — rerun and compare.
- **Benchmark runner** — JSON/JSONL receipts plus human-readable summary.

No broad ERP, accounting system, or generic “payments chatbot” is needed.

## Required failure behavior

The tool must:

- never present a low-evidence guess as a confirmed diagnosis;
- preserve unknown/ambiguous state when evidence is incomplete;
- never log credentials or raw sensitive integration values;
- never depend on private operational workflows for the public demo;
- distinguish provider/API failure evidence from local application failure evidence.

## Optional sponsor alignment

Only after the core benchmark is strong:

- **APIMatic**: A/B test whether Context Plugins measurably reduce API-grounding errors.
- **Postman**: export focused regression requests/collections for reproduced failures.
- **AG Grid**: use only if a richer diagnostics/evidence dashboard improves the demo enough to justify the UI cost.

Sponsor integration is optionality, not architecture.

## Work lanes

### PP-A — fixtures and taxonomy
Build the 50-case frozen failure corpus and stable failure taxonomy.

### PP-B — trace normalizer
Implement the sanitized input contract and redaction boundary.

### PP-C — evidence + diagnosis
Implement retrieval, ranked diagnosis, evidence pointers, and explicit abstention.

### PP-D — repair + regression
Generate the smallest repair suggestion and a focused validation artifact.

### PP-E — benchmark runner
Emit accuracy, false-confidence, repair-success, latency, and tool-call metrics.

### PP-F — demo surface
Show one clean failure, one ambiguous abstention, and one successful repair inside a sub-three-minute demo.

## Required ablations

Run the same frozen cases for:

1. single-prompt baseline;
2. baseline + bounded failure taxonomy;
3. baseline + evidence retrieval;
4. retrieval + repair planner;
5. best pipeline + optional API-grounding resource;
6. best pipeline with strict abstention threshold.

Do not add multi-agent orchestration unless it beats a simpler pipeline on repair success or latency.

## Internal promotion gate

Require:

- reproducible results on the frozen corpus;
- increased repair success over baseline;
- no regression in false-confident diagnoses;
- deterministic fixture replay;
- benchmark-backed p50/p95 latency;
- no secret material in output;
- every public performance claim traceable to the benchmark ledger.

## First experiment

Start with a 20-case single-agent baseline. Add evidence retrieval next. Promote retrieval only if top-1 accuracy or repair success increases without increasing false confidence. Add orchestration only after that result is measured.

## Submission gates

Do not submit until:

- the project is functional;
- the public repository is clean and documented;
- the demo can be reproduced from a fresh environment;
- the benchmark ledger is checked in;
- the three-minute demo shows real behavior rather than mock screens;
- no private coordination methods, credentials, or sensitive operational data is exposed.
