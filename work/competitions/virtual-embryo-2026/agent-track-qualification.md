# Virtual Embryo Challenge 2026 — Agent Team qualification packet

Status: qualified
Lane: Sol-Variance-Embryo-002
Final submissions: 2026-12-02
Official evaluation: 2026-12-04
Results: 2026-12-11 at NeurIPS

## Verified official state (2026-10-06)

- Phase P2 is open: validation submissions are scored; the starter kit and reference baselines are available.
- Phase P3 starts 2026-10-20, when validation data is released and the test leaderboard opens.
- Final submissions are due 2026-12-02; official evaluation begins 2026-12-04; results are announced 2026-12-11.
- Official challenge overview: https://virtualembryo.ai/challenge
- Official rules: https://virtualembryo.ai/challenge/rules

### Prize and money ledger

- Advertised aggregate: **$112,000** in prizes and awards.
- Advertised placed-prize pool: **$54,000 total**, split equally between Human Team and Agent Team (**$27,000 per track**: one $8,000 first prize, two $5,000 second prizes, and three $3,000 third prizes).
- Advertised cross-track Generality Award: **$8,000**, potentially held in addition to a placed prize.
- Advertised travel awards: **$30,000**.
- Advertised Community Contribution Award pool: **$20,000**, up to $200 per contribution.
- These amounts are sponsor-stated/advertised. They are not treated here as escrowed or awarded to this lane. Proposed: $0; promised to this lane: $0; verified funded/escrowed for this lane: $0; awarded: $0; invoiced: $0; received: $0.

### Agent Team evidence threshold

- A submission is held but not scored until at least **two distinct evidence kinds** are attached, and one must be the trajectory.
- Prize eligibility is stricter: the submitted run must preserve and support verification of the **trajectory, prompts, and harness**.
- Evidence must correspond to the actual submitted run; reconstructed or edited-after-the-fact evidence is not valid.

## Why this lane matters

The Agent Team track explicitly rewards methods produced by coding agents / LLM-driven recursive systems. Prize eligibility requires reproducibility evidence for the actual run: trajectory, prompts, and harness. The challenge has three tasks and separate Human Team / Agent Team rankings.

## Hard rules for an Agent Team run

- Human may write the initial prompt.
- From that point, the run must be the agent's own; do not inspect intermediate results and feed judgement back into the same run.
- Preserve the exact trajectory, prompts, harness, environment, code revision, and produced prediction artifact.
- Winning results may be re-run or inspected for reproduction.
- Do not use hidden test data or try to infer/recover it.

## Recommended first target

Start with Task 3 perturbation prediction only after reproducing the organizer baseline and scorer locally.

Reason:
- the task has a concrete mutant-response objective rather than rewarding a wild-type copy;
- scoring is explicitly based on response gene recovery, direction, magnitude, and cell-state distribution;
- a narrow single-task agent run is easier to make fully reproducible before attempting the Generality Award.

Do not optimize on the hidden beta-catenin test target. Use only released training/validation material.

## Run receipt contract

Every autonomous run must emit one immutable receipt containing:

- run_id;
- UTC start/end;
- model/provider/version;
- initial human prompt SHA256;
- full prompt/trajectory log path + SHA256;
- harness commit SHA;
- environment lockfile/container digest;
- random seeds;
- dataset release/version hashes;
- task/scorer version;
- commands executed;
- produced prediction artifact SHA256;
- local validation/scorer output;
- resource usage when available;
- terminal status and failure reason.

The harness should refuse to mark a run prize-eligible if any required provenance field is absent.

## Benchmark gates before first official submission

1. Baseline reproduction
   - reproduce organizer starter/reference score within expected tolerance.

2. Artifact validation
   - exact required genes/order;
   - finite, non-negative matrix;
   - required spatial_3D coordinates for Tasks 2/3;
   - no accidental schema mutation.

3. Autonomous-run integrity
   - trajectory generated from one initial human instruction;
   - no mid-run human feedback injected;
   - all agent mutations and evaluations preserved.

4. Generalization discipline
   - choose changes using released train/validation only;
   - hidden-test assumptions must never be encoded from external leakage.

5. Reproduction
   - second clean run from the same receipt/harness can regenerate a valid artifact.

## Initial work lanes

A. Starter-kit reproducer
- fetch official starter kit and reference baselines;
- lock environment and data versions;
- reproduce one validation score end-to-end.

B. Provenance harness
- automatic trajectory/prompt capture;
- code/data/artifact hashes;
- immutable run receipt;
- prize-eligibility validator.

C. Task 3 baseline explorer
- implement one conservative released-data baseline;
- measure each official Task 3 component separately;
- no broad model zoo or hidden-target speculation.

D. Submission validator
- offline schema checks matching official upload constraints;
- fail fast on gene-order, shape, finite/non-negative, and spatial_3D errors.

## Swarm policy

Do not let multiple agents independently tune the same autonomous run. Parallel agents may build infrastructure, reproduce baselines, or analyze released metrics, but a prize-eligible Agent Team optimization trajectory must remain attributable to its actual autonomous harness.

## Competition-safe publication

Keep proprietary swarm orchestration out of public materials. The challenge may require private verification of trajectory/prompts/harness; preserve complete internal evidence while only publishing what the competition requires or what the owner explicitly approves.
