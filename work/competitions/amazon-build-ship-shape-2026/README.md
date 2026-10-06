# Amazon Build, Ship, Shape 2026 — Alexa+ MCP reliability build packet

Status: qualified for build
Lane: Sol-Recovery-AlexaMCP-0027
Primary track: Alexa+
Submission deadline: 2026-10-23 12:00 PDT
Owner/account actions: NOT performed by this lane

## Rules fence

This packet targets the self-hosted MCP option, not the gated Alexa+ preview tooling.

Required competition surface:
- working self-hosted MCP server implementing MCP spec 2025-11-25 or later over Streamable HTTP;
- runtime code/config must actually use the required track technology, not merely mention MCP in docs;
- demo may use our own web-based Alexa+ simulator/front end;
- code repository must contain the functional source/assets/setup instructions;
- repository may be public + open source or private + explicitly shared with Devpost/Amazon reviewers;
- demonstration video should be under three minutes and visibly show the project working;
- submission includes product feedback for the tools/APIs/SDKs used;
- optional friction-log entries can improve judging, so capture them during build rather than reconstructing them later.

Do not claim access to Alexa+ Category SDK, MCP Toolkit, CLI, or Web Simulator. Hackathon entrants do not receive that preview access.

## Recommended build: Continuity MCP

A public-safe stateful workflow copilot that demonstrates what makes an Alexa+ MCP experience more useful than a single-turn wrapper:

1. durable context across sessions;
2. multi-step orchestration across several local service surfaces;
3. idempotent mutation and bounded retry;
4. checkpoint/resume after a process restart;
5. visible, measured reliability and latency.

The project should be locally runnable with no TJLabs private data, credentials, swarm coordination, or proprietary throughput logic.

### Minimal service surfaces

Keep the demo self-contained:
- **tasks** — create/list/complete checklist items;
- **timeline** — create/list milestones;
- **notes** — write/read compact workflow summaries;
- **workflow** — start/status/resume/cancel a durable orchestration.

These may share one local SQLite database. The point is the agentic orchestration and MCP transport/reliability behavior, not third-party SaaS integration breadth.

## MCP implementation boundary

The build carrier should preserve these invariants:

- one Streamable HTTP MCP endpoint;
- protocol version 2025-11-25 or later;
- normal initialize/session lifecycle;
- explicit tool schemas and deterministic tool errors;
- durable workflow/session records in SQLite or another checked-in local persistence choice;
- every mutating tool accepts an operation id / idempotency key;
- completed operation ids cannot create duplicate side effects;
- transient failures may retry only inside a small configured budget;
- a process restart can reconstruct the next legal step from persisted state;
- user-visible status distinguishes running / waiting / recovered / completed / failed;
- benchmark receipts include exact build revision + scenario + injection + result + latency.

Do not use standalone legacy HTTP+SSE as the primary transport.

## Three judge-visible flows

### A. Event prep — clean multi-step orchestration

Prompt:
> Help me prepare for demo day. Create a checklist, a short milestone timeline, and a summary I can ask for later.

Expected behavior:
- one workflow is created;
- checklist + timeline + note are committed;
- final answer summarizes what changed;
- later session can answer "what is left?" from persisted state.

### B. Event prep — transient failure recovery

Run the same flow with one deterministic injected timeout on a mutating tool.

Expected behavior:
- bounded retry occurs once;
- the operation id prevents duplicate tasks/milestones;
- workflow reports RECOVERED, then completes;
- audit/benchmark receipt makes the retry visible rather than hiding it.

### C. Resume after restart

Start a handoff or trip-prep workflow, stop the server after one committed step, restart, then ask:
> Continue where we left off.

Expected behavior:
- persisted workflow is rediscovered;
- already-committed steps are not repeated;
- remaining steps complete;
- final state can explain which work happened before vs after restart.

## Benchmark contract

The checked-in `fixtures.json` freezes nine deterministic cases: clean, timeout-recovery, and restart-resume variants across three flow families.

Each run must emit one JSONL receipt with:
- `case_id`;
- `outcome`: `success`, `recovered`, or `failed`;
- `wall_ms`;
- `retry_count`;
- `duplicate_side_effects`;
- `resumed`;
- `evidence_complete`.

The checked-in `benchmark.py` validates exact case-set identity and reports:
- completion rate;
- injected-failure recovery rate;
- restart/resume success rate;
- retry-budget violations;
- duplicate-side-effect cases;
- evidence-incomplete cases;
- p50 / p95 / max wall latency.

Default deterministic acceptance gates:
- 100% completion;
- 100% injected-failure recovery;
- 100% restart/resume success;
- zero retry-budget violations;
- zero duplicate-side-effect cases;
- zero evidence-incomplete cases.

Latency is always reported. Add a p95 gate only after measuring the actual local/server target; do not invent a threshold before evidence exists.

Example:

```bash
python work/competitions/amazon-build-ship-shape-2026/benchmark.py \
  --fixtures work/competitions/amazon-build-ship-shape-2026/fixtures.json \
  --results artifacts/alexa-mcp/results.jsonl
```

A performance claim is valid only when tied to the exact result file, code revision, environment, and command used.

## Evidence / observability requirements

For each workflow keep public-safe evidence:
- workflow id;
- ordered tool calls;
- operation ids (opaque, non-secret);
- retry/recovery events;
- checkpoint version;
- terminal status;
- total wall time;
- per-tool durations if available.

Do not log secrets, raw auth material, private Slack/GitHub content, user PII, or internal fleet routing.

## Web simulator

Because the preview Alexa+ developer tooling is not generally available to hackathon participants, build the demo against a small web simulator that:
- accepts a user utterance;
- shows the assistant response;
- exposes current workflow state;
- can toggle the timeout/restart injections used in the benchmark;
- has a compact evidence panel for operation count, retry count, resumed flag, and wall time.

Keep the simulator presentation-oriented. The MCP server is the real track technology.

## Demo-video plan

Use `demo-script.md`. The video should stay under three minutes and show:
1. clean multi-step orchestration;
2. a visible injected failure + recovery with no duplicate side effect;
3. restart/resume across sessions;
4. the measured benchmark report;
5. the MCP 2025-11-25+ Streamable HTTP implementation boundary.

No copyrighted music or unlicensed third-party material.

## Submission gates

Do not submit until all are true:
- self-hosted MCP server actually runs over Streamable HTTP;
- protocol version is 2025-11-25 or later;
- repository includes complete setup/run instructions;
- public repo has a visible OSS license, OR private repo reviewer sharing is completed by the authorized account owner;
- demo video is public on YouTube/Vimeo and under three minutes;
- all nine fixed benchmark cases have an exact receipt;
- benchmark gate passes on the intended demo revision;
- restart/resume is demonstrated from real persistence, not mocked narration;
- no duplicate side effects under the timeout case;
- product feedback is drafted from actual build notes;
- friction log contains concrete expected-vs-actual entries and workarounds where encountered;
- no proprietary TJLabs swarm process, credentials, private channels, or customer data appears in code/video/text.

## Bounded implementation lanes

### Server owner
- implement Streamable HTTP MCP server + session lifecycle;
- implement four service surfaces;
- add persistence/idempotency/retry/restart semantics.

### Simulator owner
- build the smallest judge-friendly web surface;
- expose workflow state + injection controls + evidence panel.

### Benchmark owner
- keep fixtures frozen;
- write production run receipts;
- run `benchmark.py` and preserve exact output + environment info.

### Demo owner
- record only after benchmark/recovery gates pass;
- use the checked-in script;
- capture product-feedback and friction-log evidence while testing.

## Mini-challenge boundary

Do not add AWS Builder or Open Source mini-challenge claims unless the actual implementation satisfies those rules. A primary-track Alexa+ MCP submission is already sufficient for this build lane.