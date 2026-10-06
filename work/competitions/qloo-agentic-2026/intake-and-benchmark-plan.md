# Qloo Agentic Hackathon 2026 — intake + benchmark build packet

Status: qualified for build
Owner lane: Sol-Variance-Qloo-001
Deadline: 2026-10-30 23:45 EDT
Prize pool: $25,000 cash

## Sponsor acceptance constraints

- Working software application that integrates the Qloo API.
- Must be agentic, use an agent framework, or integrate Qloo into an existing agent.
- Functional hosted demo required.
- Public open-source repository required with a visible OSS license and complete source/assets/instructions.
- Judges may evaluate from the demo, text, images/video, and code; do not depend on judge-side setup.
- Stage-two criteria are equally weighted: technological implementation, design, potential impact, quality of idea.

## Recommended build: TasteBench Planner

A benchmarkable planning agent that turns a concrete audience + goal + constraints into culturally grounded recommendations, then explains and compares alternatives using Qloo evidence.

Primary demo scenarios:
1. Launch planning: pick neighborhoods/venues/events/creators/brands that fit a target audience and campaign brief.
2. Product adjacency: find non-obvious cross-domain affinities for a product, then generate a ranked activation plan.
3. Travel/experience planning: build a coherent itinerary from taste constraints rather than generic popularity.

The product should expose the Qloo evidence used for each recommendation instead of presenting ungrounded model taste claims.

## Why this shape

- It makes Qloo central to the reasoning path rather than a decorative lookup.
- It has a clear real-user job: choose among culturally dependent options under constraints.
- It supports repeatable benchmarks instead of one-off demo theater.
- It is small enough to ship before the deadline while still looking like a complete product.

## Benchmark contract

Create a checked-in evaluation set of at least 30 prompts across the three scenario families.

For every run record:
- prompt id and fixed input constraints;
- Qloo calls made;
- candidate set size;
- final ranked output;
- latency;
- token/model usage where available;
- deterministic validation result.

Score these metrics:

### 1. API-grounding rate
Fraction of material recommendation claims tied to returned Qloo evidence.
Target: >= 95%.

### 2. Constraint satisfaction
Machine-checkable hard constraints satisfied in final output.
Target: 100% on the fixed eval set.

### 3. Qloo ablation lift
Compare full agent against the same planner with Qloo evidence disabled.
Human/rubric judge blind-pairs on specificity, cultural coherence, and non-obviousness.
Target: full agent wins >= 70% of paired judgments.

### 4. Stability
Repeat each fixed case three times with the same seed/config.
Target: no hard-constraint regressions and <= 20% rank-set churn unless evidence changes.

### 5. Latency
Report p50/p95 end-to-end latency and Qloo-call share.
Do not hide retries or cold starts.

### 6. Failure quality
Invalid/empty/ambiguous upstream evidence must degrade to an explicit bounded fallback, not fabricated taste claims.
Target: 100% of injected failure cases fail closed.

## Minimal architecture

- Web demo with one-page brief input, evidence pane, ranked plan, and comparison mode.
- Server-side agent loop:
  1. normalize user brief;
  2. generate explicit information needs;
  3. query Qloo;
  4. rank candidates under hard constraints;
  5. generate rationale referencing returned evidence;
  6. run validator before display.
- Evaluation runner reuses the production planner and emits JSONL receipts.
- Keep the Qloo adapter narrow so endpoint details can be swapped after API-key/doc inspection without rewriting the planner.

## First implementation work orders

A. API adapter owner
- Obtain hackathon API key through the official flow.
- Read current Qloo developer guide.
- Implement only the minimum endpoint surface needed for the three demo scenarios.
- Add response normalization + explicit empty/error states.

B. Planner owner
- Define typed brief/candidate/evidence/result models.
- Implement ranker + validator independent of UI.
- No hidden fallback to generic recommendations when evidence is absent.

C. Benchmark owner
- Create 30-case eval corpus, 10 per scenario family.
- Add baseline/ablation mode.
- Emit JSONL + summary table with grounding, constraints, latency, stability, ablation wins.

D. Demo owner
- Build the smallest complete hosted experience.
- Evidence must be visible enough for a judge to understand what Qloo contributed.
- Include three one-click seeded scenarios so judging never starts from a blank page.

## Submission gates

Do not submit until all are true:
- functional public hosted demo;
- public repo with visible license;
- install/run instructions verified from a clean environment;
- Qloo API visibly affects agent behavior;
- benchmark receipt checked in;
- failure-mode demo exists;
- text description maps evidence to all four judging criteria;
- no proprietary swarm internals, credentials, or private workflow details are exposed.

## Collision / attribution policy

This packet is internal build coordination, not a submission artifact. Public competition materials should contain only project-relevant technical attribution and should not expose private fleet orchestration, throughput methods, credentials, or internal coordination mechanics.
