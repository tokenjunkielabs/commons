# TrafficFlowBench 2026 — Task 1 short-gap candidate

Public-safe work for the 2026 IEEE Big Data Traffic Flow Bench.

## Candidate

task1_shortgap.py changes one thing relative to the organizer's historical-mean Task 1 baseline:

1. Learn the same weekday/time-of-day profile from train.
2. For a masked target, use same-detector linear interpolation only when finite observations bound the complete missing run and that run is at most six 5-minute cells by default.
3. If either speed or flow lacks that bounded temporal estimate, use the complete organizer historical-mean pair.

The pairwise fallback is deliberate. Mixing a local speed estimate with an unrelated historical flow estimate can create an incoherent state and hurt the Task 3 physics score.

The candidate does not interpolate across long gaps such as withheld Task 2 horizons. Task 1 is explicitly offline in the public benchmark contract, so later observations from the same released masked period are permitted evidence.

## Exact A/B

Clone the organizer repository and unpack the official Kaggle release. Then run:

    python research/competitions/trafficflowbench2026/compare_task1.py \
      --official-repo /path/to/trafficflowbench-public \
      --release-root /path/to/kaggle_public \
      --candidate research/competitions/trafficflowbench2026/task1_shortgap.py \
      --panel D12_I5_N \
      --work-dir /tmp/tfb-shortgap

The runner invokes the organizer's own baseline builder and Task 1 scorer, then invokes the short-gap candidate and the same scorer. It emits receipt.json plus both score CSVs.

Start with one panel. Promote only after the organizer score improves. If it does, repeat on all ten panels and report the corridor-family aggregate before spending a leaderboard submission.

## Evidence boundary

No competition dataset or leaderboard submission is stored here. This carrier is source-complete but is not performance-validated until a data-bearing runner executes the exact A/B above.

Registration, Kaggle submission, final-package e-mail, and award claims are separate account-owner actions. Current public competition rules require award registration by October 25, 2026 and code/report reproducibility later in the schedule; those account actions are intentionally outside this source lane.
