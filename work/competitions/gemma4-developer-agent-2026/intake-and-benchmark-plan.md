# Gemma 4 Developer Agent 2026 — intake + benchmark build packet

Status: qualified for build  
Coding-track final: 2026-12-02  
Entry/team-merger deadline: 2026-11-25  
Optional paper-track final: 2026-11-12  
Coding prizes: $65,000 total  
Optional paper prizes: $35,000 total

Official sources:
- https://www.kaggle.com/competitions/gemma-4-developer-agent/overview
- https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/overview/submission-requirements

## Sponsor constraints that shape the design

- The coding score is direct software-engineering performance: submitted patches are applied to real issue repositories and validation tests are run; score is the percentage of issues whose patches pass.
- The agent receives a fixed aggregate execution budget of 12 hours across tasks, excluding patch validation.
- Every agent/subagent must use the competition-supported `gemma-4-31b-it-qat-w4a16-ct` base model.
- Different PEFT/LoRA adapters may be assigned to different agents, but adapter complexity is useful only if it improves pass rate enough to repay runtime and engineering cost.
- Evaluation is offline / internet-disabled.
- The competition L4x4 environment exposes 96 GB GPU memory.

These constraints make solved issues per unit wall time the primary engineering objective. Agent count, verbose traces, and broad verification are not useful unless they improve validated patch throughput.

## Recommended agent shape

Use a small role-specialized graph rather than an unconstrained swarm:

1. **Router** — classify issue shape, estimate difficulty, and set a hard time/tool budget.
2. **Navigator** — identify likely source files, tests, symbols, and dependency edges before broad reads.
3. **Implementer** — produce the smallest acceptance-complete patch.
4. **Verifier/repairer** — run targeted validation first, classify failures, and perform bounded repair.
5. **Scheduler/stop policy** — abandon low-probability tasks when their expected marginal score gain falls below the next queued issue.

The graph should be able to collapse to fewer roles when routing overhead is not justified.

## Minimal submission architecture

- `agent.yaml`: primary orchestrator and hard budgets.
- `sub_agents/`: only the navigator, implementer, and verifier roles that win ablations.
- `skills/`: bounded repository navigation, targeted test selection, failure triage, and patch hygiene.
- `adapters/`: only LoRA/PEFT adapters that produce a measured pass-rate or throughput gain.
- Custom tools only when they materially improve validated issue throughput.

No evaluation-critical behavior may require network access.

## Benchmark contract

Use a frozen, license-compatible public development corpus. Keep exact repository commit, issue text hash, seed/config, time budget, and expected public validation command for each case.

Suggested corpus mix:

- 30% narrow bug fixes;
- 20% tests/regressions;
- 20% API or behavioral changes;
- 15% navigation-heavy changes;
- 15% dependency/config/build issues.

For every attempted issue record:

- terminal state: solved / unsolved / infrastructure failure;
- wall-clock seconds;
- first-patch latency;
- targeted validation runtime;
- repair-loop count;
- files opened and files changed;
- tool-call count;
- patch hash;
- validation result.

Report:

- issue pass rate;
- solved issues projected inside the official 12-hour budget;
- p50/p90/p95 task latency;
- p50/p95 time-to-first-patch;
- tool calls per solved issue;
- unrelated-change rate;
- deterministic replay rate.

## Required ablations

Run the same frozen cases and seeds for:

1. single-agent baseline;
2. router + implementer;
3. router + navigator + implementer;
4. router + navigator + implementer + verifier;
5. best graph + candidate LoRA/PEFT adapter;
6. best graph + aggressive early-stop/global scheduling.

Promote a component only if it increases validated solved-issue count or preserves pass rate while reducing wall time. More agents by itself is not an improvement.

## Throughput design

The fixed aggregate budget means scheduling is part of model quality.

Prioritize:

- cheap task triage before expensive context loading;
- targeted symbol/search operations before repository-wide reads;
- focused validation before full suites;
- bounded repair loops;
- explicit expected-value task switching;
- deterministic checkpoints so a failed role does not force rediscovery;
- reusable repository summaries only when they can be produced and consumed within competition rules.

## Work lanes

### G4-A — baseline runner
Materialize the frozen issue corpus and run the simplest compliant single-agent baseline. Produce a pass-rate + latency ledger.

### G4-B — router / scheduler
Implement issue-shape classification, per-task budgets, expected-value early stop, and a global 12-hour allocator.

### G4-C — repository navigator
Measure time-to-first-relevant-file, files opened, and downstream pass-rate effect from graph/search-assisted navigation.

### G4-D — verifier / repair loop
Implement targeted test selection, failure classification, and bounded repair. Avoid full-suite-first verification.

### G4-E — LoRA experiment
Start only after a stable baseline exists. Test one adapter hypothesis at a time against the frozen corpus.

### G4-F — paper evidence
Capture ablations, failures, and negative results in a reproducible research ledger suitable for the optional paper track.

## Internal promotion gate

A candidate architecture is not promoted because it succeeds once. Require:

- frozen-corpus pass-rate improvement over baseline, or equal pass rate at lower wall time;
- no unexplained p95 runtime regression;
- deterministic replay on the same inputs;
- a 12-hour budget projection from measured task times;
- at least one controlled ablation identifying the component responsible for a gain;
- no hidden network dependency.

## First experiment

Start with **no fine-tuning**. Establish the clean prompt/tool baseline, then test the navigator and scheduler independently. This answers the highest-value question first: whether better context routing and time allocation improve official issue pass rate before spending compute on adapters.

## Submission gates

Do not submit until:

- the agent runs offline in the competition environment;
- the fixed benchmark is reproducible;
- the current architecture beats the single-agent baseline on validated solved issues or time-to-solution;
- failure and abandonment behavior are visible in receipts;
- no proprietary internal coordination process, credentials, or private operational data is exposed.
