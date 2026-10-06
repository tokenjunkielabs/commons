# AI4S Organ-on-a-Chip QC benchmark R1

This directory is the first benchmark contract for an evidence-bound microscopy experiment-QC assistant. It is public-safe competition infrastructure only. It does **not** contain clinical evidence, a trained model, organizer data, credentials, or a competition submission.

## What R1 measures

For the same frozen cases, compare a deterministic QC layer with an agent-triage layer on:

- pooled defect precision, recall, and F1;
- clean-case false-flag rate;
- evidence-citation validity;
- abstention accuracy;
- median and nearest-rank p95 latency.

Every receipt names the evidence keys available to that case. A predicted defect without at least one citation is invalid for the citation metric. A citation outside the case evidence catalog is also invalid.

## Provenance gate

`synthetic_manifest.jsonl` is deliberately synthetic and exists only to exercise the schema. Synthetic rows must use `repository://` provenance plus a generator tag. When real public microscopy data is introduced, each `public` manifest row must use an http(s) source URL, a non-empty license identifier, and an immutable lowercase SHA-256. The scorer rejects incomplete provenance.

The included synthetic fixture is released under CC0-1.0. Its values are hand-authored metric-contract examples, not microscopy measurements.

## Receipt schema

Each `(case_id, system)` pair must appear exactly once for both systems:

- `expected_defects` / `predicted_defects`: unique defect labels;
- `evidence_catalog`: evidence keys made available for that case;
- `cited_evidence`: the subset actually cited by the result;
- `expected_abstain` / `abstained`: explicit unsupported-input behavior;
- `latency_ms`: non-negative end-to-end latency for that system/case.

Both systems must cover exactly the same manifest cases.

## Run the contract smoke

```bash
python work/competitions/ai4s-organ-on-chip-2026/qc-benchmark-r1/score_qc_receipts.py \
  --manifest work/competitions/ai4s-organ-on-chip-2026/qc-benchmark-r1/synthetic_manifest.jsonl \
  --receipts work/competitions/ai4s-organ-on-chip-2026/qc-benchmark-r1/synthetic_receipts.jsonl
```

The checked fixture intentionally gives the deterministic side one false flag and two misses while the agent side is perfect, solely so the scorer exercises non-zero A/B deltas. Expected plumbing values include deterministic F1 `0.666666...`, agent F1 `1.0`, deterministic clean false-flag rate `0.333333...`, deterministic p50/p95 `12.5/16 ms`, and agent p50/p95 `40/52 ms`. These numbers are **not competition, microscopy, model, or product performance**.

## Promotion gate for real work

Do not present a result as competition evidence until all of these are true:

1. a frozen licensed public subset is recorded with immutable hashes;
2. held-out blur, exposure, illumination, and metadata defects are represented;
3. deterministic QC and agent triage run on identical cases;
4. the scorer emits precision/recall/F1, false-flag, citation, abstention, and p50/p95 receipts;
5. any improvement is reported together with its latency cost and failure cases;
6. raw-source provenance and licenses are publishable;
7. wording remains non-clinical unless a separate validation regime supports stronger claims.

Next source lane: implement the minimal deterministic image/metadata QC core, then generate real receipts through this contract. Registration, Kaggle submission, demo video, and technical-report publication remain separate owner actions.
