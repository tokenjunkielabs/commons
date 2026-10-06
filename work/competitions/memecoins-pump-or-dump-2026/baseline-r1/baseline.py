#!/usr/bin/env python3
"""Leakage-aware offline baseline for Kaggle Memecoins: Pump or Dump?.

This module intentionally uses only columns present in both train.csv and test.csv plus
features derived from decision-time timestamps. It trains from scratch on each run, applies
an explicit label-resolution embargo for walk-forward validation, optimizes the competition's
simulated PnL rather than classifier accuracy, and defaults to abstention when expected edge
is weak.

It is competition research code only. It does not place trades or connect to a wallet/exchange.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor

TP_GRID: tuple[float, ...] = (3.0, 4.0, 5.0, 7.5, 10.0)
FEE = 0.3

# Anything matching these tokens is forbidden even if it unexpectedly appears in test.csv.
# This is intentionally conservative: the baseline would rather drop a useful column than
# admit a post-snapshot or label-derived feature.
FORBIDDEN_FEATURE_TOKENS = (
    "max_x",
    "final_x",
    "future",
    "post_",
    "after_",
    "outcome",
    "label",
    "target",
    "sustained",
    "pnl",
    "take_profit",
    "profit",
)
IDENTIFIER_TOKENS = (
    "mint",
    "creator",
    "wallet",
    "signature",
    "fee_payer",
    "token_address",
    "txid",
    "transaction_id",
)
TIME_CANDIDATES = (
    "mt",
    "migration_ts",
    "migration_time",
    "migrated_at",
    "snapshot_ts",
    "snapshot_time",
)


@dataclass(frozen=True)
class PolicySettings:
    min_expected_pnl: float = 0.10
    max_take_fraction: float = 0.01


@dataclass
class FoldPrediction:
    day: str
    n_train: int
    n_valid: int
    tp: np.ndarray
    expected_pnl: np.ndarray
    max_x: np.ndarray
    final_x: np.ndarray


@dataclass
class FoldScore:
    day: str
    n_train: int
    n_valid: int
    takes: int
    pnl: float
    mean_take_pnl: float


class ConstantProbabilityModel:
    def __init__(self, p: float):
        self.p = float(min(1.0, max(0.0, p)))

    def predict_proba(self, x: pd.DataFrame) -> np.ndarray:
        p = np.full(len(x), self.p, dtype=float)
        return np.column_stack([1.0 - p, p])


class ConstantRegressor:
    def __init__(self, value: float):
        self.value = float(value)

    def predict(self, x: pd.DataFrame) -> np.ndarray:
        return np.full(len(x), self.value, dtype=float)


def _coerce_timestamp(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        finite = pd.to_numeric(series, errors="coerce")
        med = float(np.nanmedian(np.abs(finite.to_numpy(dtype=float)))) if finite.notna().any() else 0.0
        if med >= 1e17:
            unit = "ns"
        elif med >= 1e14:
            unit = "us"
        elif med >= 1e11:
            unit = "ms"
        else:
            unit = "s"
        return pd.to_datetime(finite, unit=unit, utc=True, errors="coerce")
    return pd.to_datetime(series, utc=True, errors="coerce")


def find_time_column(frame: pd.DataFrame) -> str:
    lower = {c.lower(): c for c in frame.columns}
    for candidate in TIME_CANDIDATES:
        if candidate in lower:
            return lower[candidate]
    # Last-resort names, but never silently pick created_ts as migration time.
    for c in frame.columns:
        lc = c.lower()
        if "migration" in lc and ("time" in lc or "ts" in lc or lc.endswith("at")):
            return c
    raise ValueError(
        "Could not find a migration/snapshot timestamp column. Expected one of: "
        + ", ".join(TIME_CANDIDATES)
    )


def decision_times(frame: pd.DataFrame) -> pd.Series:
    """Decision is exactly migration + 60 seconds."""
    col = find_time_column(frame)
    return _coerce_timestamp(frame[col]) + pd.Timedelta(seconds=60)


def label_resolved_times(frame: pd.DataFrame) -> pd.Series:
    """Outcome label is only fully knowable 60 minutes after the decision point."""
    return decision_times(frame) + pd.Timedelta(minutes=60)


def score_token(tp: float, max_x: float, final_x: float) -> float:
    if tp == 0:
        return 0.0
    if not (3.0 <= tp <= 100.0):
        raise ValueError(f"invalid tp={tp}; must be 0 or in [3, 100]")
    if max_x >= tp:
        return float(tp - 1.0 - FEE)
    return float(max(final_x - 1.0 - FEE, -1.0))


def score_policy(tp: np.ndarray, max_x: np.ndarray, final_x: np.ndarray) -> float:
    return float(sum(score_token(float(a), float(b), float(c)) for a, b, c in zip(tp, max_x, final_x)))


def _feature_allowed(name: str) -> bool:
    lc = name.lower()
    if any(tok in lc for tok in FORBIDDEN_FEATURE_TOKENS):
        return False
    if any(tok in lc for tok in IDENTIFIER_TOKENS):
        return False
    return True


def build_feature_frames(train: pd.DataFrame, test: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    """Build a conservative numeric feature surface from data available at decision time.

    No cross-token aggregation is performed, so this baseline cannot leak through a reputation
    or global groupby feature. Columns must exist in both train and test. Raw identifiers are
    excluded. Timestamp-derived hour/day and curve age are allowed because they are known at the
    decision point.
    """
    common = [c for c in train.columns if c in test.columns and _feature_allowed(c)]
    x_train = pd.DataFrame(index=train.index)
    x_test = pd.DataFrame(index=test.index)

    time_col = find_time_column(train)
    train_decision = decision_times(train)
    test_decision = decision_times(test)

    for c in common:
        if c == time_col:
            continue
        tr = pd.to_numeric(train[c], errors="coerce")
        te = pd.to_numeric(test[c], errors="coerce")
        # Avoid promoting mostly-text columns into an almost-all-NaN feature.
        if tr.notna().mean() < 0.50 and te.notna().mean() < 0.50:
            continue
        x_train[c] = tr.astype(float)
        x_test[c] = te.astype(float)

    x_train["decision_hour_utc"] = train_decision.dt.hour.astype(float)
    x_test["decision_hour_utc"] = test_decision.dt.hour.astype(float)
    x_train["decision_dow_utc"] = train_decision.dt.dayofweek.astype(float)
    x_test["decision_dow_utc"] = test_decision.dt.dayofweek.astype(float)

    # Safe per-token age feature when creation timestamp is present in both files.
    created = next((c for c in train.columns if c.lower() in {"created_ts", "created_at", "creation_ts"} and c in test.columns), None)
    if created:
        tr_created = _coerce_timestamp(train[created])
        te_created = _coerce_timestamp(test[created])
        x_train["curve_age_s"] = (train_decision - tr_created).dt.total_seconds()
        x_test["curve_age_s"] = (test_decision - te_created).dt.total_seconds()

    x_train = x_train.replace([np.inf, -np.inf], np.nan)
    x_test = x_test.replace([np.inf, -np.inf], np.nan)
    feature_names = list(x_train.columns)
    if not feature_names:
        raise ValueError("No safe numeric train/test features were found")
    return x_train, x_test, feature_names


def build_single_frame_features(frame: pd.DataFrame, feature_names: Sequence[str]) -> pd.DataFrame:
    """Recreate selected features for a fold from one dataframe."""
    out = pd.DataFrame(index=frame.index)
    dec = decision_times(frame)
    for name in feature_names:
        if name == "decision_hour_utc":
            out[name] = dec.dt.hour.astype(float)
        elif name == "decision_dow_utc":
            out[name] = dec.dt.dayofweek.astype(float)
        elif name == "curve_age_s":
            created = next((c for c in frame.columns if c.lower() in {"created_ts", "created_at", "creation_ts"}), None)
            if created is None:
                out[name] = np.nan
            else:
                out[name] = (dec - _coerce_timestamp(frame[created])).dt.total_seconds()
        else:
            out[name] = pd.to_numeric(frame[name], errors="coerce") if name in frame.columns else np.nan
    return out.replace([np.inf, -np.inf], np.nan)


def fit_models(x: pd.DataFrame, max_x: np.ndarray, final_x: np.ndarray, tp_grid: Sequence[float] = TP_GRID):
    models: dict[float, tuple[object, object]] = {}
    final_fail_payoff = np.maximum(final_x - 1.0 - FEE, -1.0)
    for tp in tp_grid:
        reached = np.asarray(max_x >= tp, dtype=int)
        if reached.min(initial=0) == reached.max(initial=0):
            reach_model: object = ConstantProbabilityModel(float(reached.mean()))
        else:
            reach_model = HistGradientBoostingClassifier(
                learning_rate=0.06,
                max_iter=80,
                max_leaf_nodes=15,
                min_samples_leaf=20,
                l2_regularization=0.5,
                random_state=17,
            )
            reach_model.fit(x, reached)

        fail_mask = reached == 0
        if int(fail_mask.sum()) < 30:
            fail_value = float(np.mean(final_fail_payoff[fail_mask])) if fail_mask.any() else -1.0
            fail_model: object = ConstantRegressor(fail_value)
        else:
            fail_model = HistGradientBoostingRegressor(
                learning_rate=0.06,
                max_iter=60,
                max_leaf_nodes=15,
                min_samples_leaf=20,
                l2_regularization=1.0,
                loss="squared_error",
                random_state=19,
            )
            fail_model.fit(x.loc[fail_mask], final_fail_payoff[fail_mask])
        models[float(tp)] = (reach_model, fail_model)
    return models


def expected_pnl_matrix(models, x: pd.DataFrame, tp_grid: Sequence[float] = TP_GRID) -> np.ndarray:
    cols = []
    for tp in tp_grid:
        reach_model, fail_model = models[float(tp)]
        p = np.asarray(reach_model.predict_proba(x))[:, 1]
        fail = np.clip(np.asarray(fail_model.predict(x), dtype=float), -1.0, 98.7)
        cols.append(p * (float(tp) - 1.0 - FEE) + (1.0 - p) * fail)
    return np.column_stack(cols)


def choose_unfiltered_policy(models, x: pd.DataFrame, tp_grid: Sequence[float] = TP_GRID) -> tuple[np.ndarray, np.ndarray]:
    ev = expected_pnl_matrix(models, x, tp_grid)
    best_i = np.argmax(ev, axis=1)
    best_ev = ev[np.arange(len(x)), best_i]
    best_tp = np.asarray([float(tp_grid[i]) for i in best_i], dtype=float)
    return best_tp, best_ev


def apply_settings(best_tp: np.ndarray, best_ev: np.ndarray, settings: PolicySettings) -> np.ndarray:
    out = np.zeros(len(best_tp), dtype=float)
    eligible = np.flatnonzero(best_ev >= settings.min_expected_pnl)
    if len(eligible) == 0:
        return out
    cap = max(1, int(math.ceil(len(best_tp) * settings.max_take_fraction)))
    if len(eligible) > cap:
        order = eligible[np.argsort(best_ev[eligible])[::-1][:cap]]
    else:
        order = eligible
    out[order] = best_tp[order]
    return out


def make_fold_predictions(train: pd.DataFrame, feature_names: Sequence[str], days: int = 7) -> list[FoldPrediction]:
    if "max_x" not in train.columns or "final_x" not in train.columns:
        raise ValueError("train.csv must contain max_x and final_x for exact competition scoring")
    dec = decision_times(train)
    resolved = label_resolved_times(train)
    day = dec.dt.floor("D")
    unique_days = sorted(pd.Series(day.dropna().unique()).tolist())
    fold_days = unique_days[-days:]
    folds: list[FoldPrediction] = []

    for fold_day in fold_days:
        cutoff = pd.Timestamp(fold_day)
        tr_mask = resolved < cutoff
        va_mask = day == cutoff
        if int(tr_mask.sum()) < 100 or int(va_mask.sum()) == 0:
            continue
        tr = train.loc[tr_mask]
        va = train.loc[va_mask]
        x_tr = build_single_frame_features(tr, feature_names)
        x_va = build_single_frame_features(va, feature_names)
        models = fit_models(
            x_tr,
            pd.to_numeric(tr["max_x"], errors="coerce").to_numpy(dtype=float),
            pd.to_numeric(tr["final_x"], errors="coerce").to_numpy(dtype=float),
        )
        best_tp, best_ev = choose_unfiltered_policy(models, x_va)
        folds.append(
            FoldPrediction(
                day=str(cutoff.date()),
                n_train=len(tr),
                n_valid=len(va),
                tp=best_tp,
                expected_pnl=best_ev,
                max_x=pd.to_numeric(va["max_x"], errors="coerce").to_numpy(dtype=float),
                final_x=pd.to_numeric(va["final_x"], errors="coerce").to_numpy(dtype=float),
            )
        )
    return folds


def _score_folds(folds: Sequence[FoldPrediction], settings: PolicySettings) -> list[FoldScore]:
    scores: list[FoldScore] = []
    for f in folds:
        tp = apply_settings(f.tp, f.expected_pnl, settings)
        pnl = score_policy(tp, f.max_x, f.final_x)
        takes = int(np.count_nonzero(tp))
        scores.append(
            FoldScore(
                day=f.day,
                n_train=f.n_train,
                n_valid=f.n_valid,
                takes=takes,
                pnl=round(pnl, 8),
                mean_take_pnl=round(pnl / takes, 8) if takes else 0.0,
            )
        )
    return scores


def select_settings(folds: Sequence[FoldPrediction]) -> tuple[PolicySettings, list[FoldScore], list[FoldScore]]:
    """Tune conservatism on older folds, preserve newest folds as untouched holdout."""
    if len(folds) < 3:
        default = PolicySettings()
        return default, _score_folds(folds, default), []
    split = max(1, len(folds) - 3)
    tune, holdout = list(folds[:split]), list(folds[split:])
    candidates = [
        PolicySettings(m, frac)
        for frac in (0.005, 0.01, 0.02)
        for m in (0.0, 0.10, 0.25, 0.50)
    ]

    def objective(settings: PolicySettings) -> tuple[float, float, float]:
        scores = _score_folds(tune, settings)
        pnls = np.asarray([s.pnl for s in scores], dtype=float)
        # Prefer robust positive days, then total PnL, then fewer takes as tie-breaker.
        positive_fraction = float(np.mean(pnls > 0.0)) if len(pnls) else 0.0
        total = float(pnls.sum())
        takes = float(sum(s.takes for s in scores))
        return (positive_fraction, total, -takes)

    best = max(candidates, key=objective)
    return best, _score_folds(tune, best), _score_folds(holdout, best)


def train_final_and_predict(train: pd.DataFrame, test: pd.DataFrame, settings: PolicySettings):
    x_train, x_test, feature_names = build_feature_frames(train, test)
    dec_test = decision_times(test)
    resolved_train = label_resolved_times(train)
    if dec_test.notna().any():
        test_day = dec_test.min().floor("D")
        allowed = resolved_train < test_day
        # Fail closed only if the inferred cutoff is meaningful; otherwise trust the organizer's
        # already-embargoed train.csv.
        if int(allowed.sum()) >= 100:
            train = train.loc[allowed].copy()
            x_train = x_train.loc[allowed].copy()
    models = fit_models(
        x_train,
        pd.to_numeric(train["max_x"], errors="coerce").to_numpy(dtype=float),
        pd.to_numeric(train["final_x"], errors="coerce").to_numpy(dtype=float),
    )
    best_tp, best_ev = choose_unfiltered_policy(models, x_test)
    tp = apply_settings(best_tp, best_ev, settings)
    return tp, best_ev, feature_names, len(train)


def validate_submission(sample: pd.DataFrame, submission: pd.DataFrame) -> None:
    if list(submission.columns) != ["mint", "tp"]:
        raise ValueError("submission must contain exactly columns: mint,tp")
    if submission["mint"].tolist() != sample["mint"].tolist():
        raise ValueError("submission mint order/set does not exactly match sample_submission.csv")
    tp = pd.to_numeric(submission["tp"], errors="coerce")
    valid = (tp == 0.0) | ((tp >= 3.0) & (tp <= 100.0))
    if tp.isna().any() or not bool(valid.all()):
        bad = submission.loc[~valid | tp.isna()].head(5).to_dict("records")
        raise ValueError(f"invalid tp values: {bad}")


def run(data_dir: Path, output_dir: Path) -> dict:
    train = pd.read_csv(data_dir / "train.csv")
    test = pd.read_csv(data_dir / "test.csv")
    sample = pd.read_csv(data_dir / "sample_submission.csv")
    if "mint" not in train or "mint" not in test or "mint" not in sample:
        raise ValueError("train/test/sample_submission must contain mint")

    # Build feature surface once so fold validation and final run use the same admitted columns.
    _, _, feature_names = build_feature_frames(train, test)
    folds = make_fold_predictions(train, feature_names, days=7)
    settings, tune_scores, holdout_scores = select_settings(folds)
    tp, expected_pnl, feature_names, n_final_train = train_final_and_predict(train, test, settings)

    pred = pd.DataFrame({"mint": test["mint"], "tp": tp})
    submission = sample[["mint"]].merge(pred, on="mint", how="left", validate="one_to_one")
    submission["tp"] = submission["tp"].fillna(0.0)
    validate_submission(sample[["mint"]], submission)

    output_dir.mkdir(parents=True, exist_ok=True)
    submission.to_csv(output_dir / "submission.csv", index=False)
    receipt = {
        "schema": "tjlabs.memecoins-pump-or-dump.baseline-r1.v1",
        "evidence_boundary": "offline walk-forward only; not Kaggle/bot/final-window performance and not real trading",
        "train_rows_input": int(len(train)),
        "train_rows_final_after_resolution_cutoff": int(n_final_train),
        "test_rows": int(len(test)),
        "feature_count": int(len(feature_names)),
        "features": feature_names,
        "tp_grid": list(TP_GRID),
        "settings": asdict(settings),
        "tuning_folds": [asdict(s) for s in tune_scores],
        "holdout_folds": [asdict(s) for s in holdout_scores],
        "holdout_total_pnl": round(float(sum(s.pnl for s in holdout_scores)), 8),
        "holdout_positive_days": int(sum(s.pnl > 0 for s in holdout_scores)),
        "holdout_days": int(len(holdout_scores)),
        "test_takes": int(np.count_nonzero(tp)),
        "test_expected_pnl_median_taken": (
            round(float(np.median(expected_pnl[tp > 0])), 8) if np.any(tp > 0) else None
        ),
    }
    (output_dir / "receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True, help="directory containing train.csv, test.csv, sample_submission.csv")
    parser.add_argument("--output", type=Path, default=Path("out"))
    args = parser.parse_args()
    receipt = run(args.data, args.output)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
