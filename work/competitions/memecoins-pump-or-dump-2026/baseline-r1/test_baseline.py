import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

import baseline


class BaselineTests(unittest.TestCase):
    def test_exact_pnl_rule(self):
        self.assertEqual(baseline.score_token(0.0, 100.0, 0.01), 0.0)
        self.assertAlmostEqual(baseline.score_token(5.0, 10.0, 0.5), 3.7)
        self.assertAlmostEqual(baseline.score_token(20.0, 10.0, 0.5), -0.8)
        self.assertEqual(baseline.score_token(20.0, 10.0, 0.0), -1.0)

    def test_resolution_embargo_is_one_hour_after_decision(self):
        df = pd.DataFrame({"mt": [1_700_000_000]})
        dec = baseline.decision_times(df).iloc[0]
        resolved = baseline.label_resolved_times(df).iloc[0]
        self.assertEqual((resolved - dec).total_seconds(), 3600)
        self.assertEqual((dec - pd.to_datetime(1_700_000_000, unit="s", utc=True)).total_seconds(), 60)

    def test_feature_gate_excludes_labels_ids_and_future_columns(self):
        train = pd.DataFrame({
            "mint": ["a", "b"],
            "mt": [1_700_000_000, 1_700_000_100],
            "created_ts": [1_699_999_000, 1_699_999_100],
            "pre_trades": [10, 20],
            "pre_failed": [1, 3],
            "future_signal": [99, 99],
            "max_x": [5, 2],
            "final_x": [1.2, 0.1],
        })
        test = train.drop(columns=["max_x", "final_x"]).copy()
        xtr, xte, names = baseline.build_feature_frames(train, test)
        self.assertIn("pre_trades", names)
        self.assertIn("pre_failed", names)
        self.assertIn("curve_age_s", names)
        self.assertNotIn("future_signal", names)
        self.assertNotIn("mint", names)
        self.assertEqual(list(xtr.columns), list(xte.columns))

    def test_submission_contract(self):
        sample = pd.DataFrame({"mint": ["a", "b"]})
        good = pd.DataFrame({"mint": ["a", "b"], "tp": [0.0, 7.5]})
        baseline.validate_submission(sample, good)
        bad = pd.DataFrame({"mint": ["a", "b"], "tp": [2.0, 7.5]})
        with self.assertRaises(ValueError):
            baseline.validate_submission(sample, bad)

    def test_small_end_to_end_is_deterministic_and_valid(self):
        rng = np.random.default_rng(42)
        rows = []
        start = pd.Timestamp("2026-08-01", tz="UTC")
        for day in range(12):
            for i in range(45):
                mt = start + pd.Timedelta(days=day, minutes=i * 20)
                signal = rng.normal()
                pre_trades = max(0.0, 30 + 10 * signal + rng.normal(0, 4))
                pre_failed = max(0.0, 5 - 2 * signal + rng.normal(0, 1))
                max_x = 7.0 if signal > 1.0 else (4.0 if signal > 0.4 else 1.5)
                final_x = 1.4 if signal > 0.8 else 0.2
                rows.append({
                    "mint": f"m{day}_{i}",
                    "mt": int(mt.timestamp()),
                    "created_ts": int((mt - pd.Timedelta(minutes=45 + i)).timestamp()),
                    "pre_trades": pre_trades,
                    "pre_failed": pre_failed,
                    "dev_balance": float(max(0.0, 0.4 - 0.1 * signal)),
                    "bundled_buys": float(max(0.0, 2.0 - signal)),
                    "max_x": max_x,
                    "final_x": final_x,
                })
        train = pd.DataFrame(rows)
        test = train.iloc[-45:].drop(columns=["max_x", "final_x"]).copy()
        # Move test to a new day so final training cutoff is meaningful.
        test["mt"] += 86400
        sample = pd.DataFrame({"mint": test["mint"], "tp": 0.0})

        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "data"
            out1 = Path(td) / "o1"
            out2 = Path(td) / "o2"
            data.mkdir()
            train.to_csv(data / "train.csv", index=False)
            test.to_csv(data / "test.csv", index=False)
            sample.to_csv(data / "sample_submission.csv", index=False)
            r1 = baseline.run(data, out1)
            r2 = baseline.run(data, out2)
            s1 = pd.read_csv(out1 / "submission.csv")
            s2 = pd.read_csv(out2 / "submission.csv")
            pd.testing.assert_frame_equal(s1, s2)
            baseline.validate_submission(sample[["mint"]], s1)
            self.assertEqual(r1["settings"], r2["settings"])
            self.assertGreaterEqual(r1["feature_count"], 4)


if __name__ == "__main__":
    unittest.main()
