# Memecoins: Pump or Dump? — leakage-aware baseline R1

Public-safe competition baseline for Kaggle's **Memecoins: Pump or Dump?** challenge. This is an offline simulated-PnL research pipeline only; it does **not** place real trades or connect to a wallet/exchange.

## What this carrier does

- trains from scratch on the attached rolling training window; no embedded fitted weights or pretrained model;
- uses only numeric columns present in both `train.csv` and `test.csv`, excludes identifiers and post-snapshot/label-like fields, and performs **no cross-token aggregation**;
- derives only decision-time hour/day and optional curve age from timestamps;
- enforces a historical label embargo: a training token is not eligible until **60 minutes after the migration+60s decision point**;
- fits separate reach-probability + failure-payoff models for a small TP grid (`3, 4, 5, 7.5, 10`), then selects the level with highest estimated competition PnL;
- abstains (`tp=0`) unless expected edge clears a tuned conservative margin and caps trade depth to a small daily fraction;
- tunes conservatism on older walk-forward folds and preserves the newest three folds as holdout evidence;
- writes `submission.csv` in exact `mint,tp` order and a machine-readable `receipt.json` with the evidence boundary.

The official competition payoff is used exactly: skip = `0`; reached TP = `tp - 1 - 0.3`; otherwise `max(final_x - 1 - 0.3, -1)`.

## Run

```bash
python baseline.py --data /kaggle/input/competitions/memecoins-pump-or-dump --output out
```

Expected files in `--data`:

- `train.csv`
- `test.csv`
- `sample_submission.csv`

The script does not need internet. It intentionally does not perform Kaggle submission or Telegram/bot account actions.

## Focused validation

```bash
python -m unittest -v test_baseline.py
```

The five focused checks cover: exact PnL semantics, one-hour outcome embargo, future/id feature rejection, submission shape/range, and deterministic end-to-end behavior on a synthetic rolling window.

## Evidence boundary

A local/synthetic green run only proves the pipeline mechanics. It is **not** a Kaggle score, league-bot score, future-window result, or evidence that this strategy is profitable in real markets. Promotion requires the actual attached competition data and the script's untouched walk-forward holdout receipt. If holdout days are mostly non-positive, keep or increase abstention rather than adding complexity first.

## Next performance slice

Once the CSV-only baseline has an honest positive walk-forward edge, add raw-tape features **one family at a time** by reading parquet day-by-day and selected columns only: curve executed-vs-failed flow, 0–15/15–30/30–60 AMM flow shape, wallet concentration, reserve/depth path, and price drawdown. Any cross-token reputation feature must remain unavailable until the source token's one-hour outcome is resolved.
