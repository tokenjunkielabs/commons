import csv
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from anomaly_retrieval import extract_features, load_manifest, run, score_records


class NebulaeBaselineTests(unittest.TestCase):
    def _write_image(self, path: Path, kind: str) -> None:
        h = w = 64
        yy, xx = np.mgrid[:h, :w]
        if kind == "soft":
            base = 180 + 10 * np.sin(xx / 8.0)
            arr = np.stack([base + 5, base, base - 8], axis=-1)
        elif kind == "soft2":
            base = 176 + 8 * np.cos(yy / 9.0)
            arr = np.stack([base + 7, base + 1, base - 5], axis=-1)
        elif kind == "checker":
            checker = ((xx // 4 + yy // 4) % 2) * 220 + 20
            arr = np.stack([checker, 255 - checker, checker], axis=-1)
        else:
            raise AssertionError(kind)
        Image.fromarray(
            np.clip(arr, 0, 255).astype(np.uint8), "RGB"
        ).save(path)

    def _fixture(self, root: Path) -> Path:
        specs = [
            ("r1.png", "r1", "p1", "s1", "REFERENCE", "soft"),
            ("r2.png", "r2", "p2", "s2", "REFERENCE", "soft2"),
            ("r3.png", "r3", "p3", "s3", "REFERENCE", "soft"),
            ("x.png", "x", "p4", "s4", "CKD", "checker"),
        ]
        manifest = root / "manifest.csv"
        with manifest.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow([
                "patch_path", "sample_id", "participant_id", "slide_id", "group"
            ])
            for filename, sid, pid, slide, group, kind in specs:
                self._write_image(root / filename, kind)
                writer.writerow([filename, sid, pid, slide, group])
        return manifest

    def test_anomaly_ranks_checker_first_and_is_deterministic(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manifest = self._fixture(root)
            a = root / "a.jsonl"
            b = root / "b.jsonl"
            receipt_a = run(manifest, a, "REFERENCE", k=2, image_size=64)
            receipt_b = run(manifest, b, "REFERENCE", k=2, image_size=64)
            self.assertEqual(a.read_bytes(), b.read_bytes())
            self.assertEqual(
                receipt_a["output_sha256"], receipt_b["output_sha256"]
            )
            rows = [
                json.loads(line) for line in a.read_text().splitlines()
            ]
            self.assertEqual(rows[0]["sample_id"], "x")
            self.assertEqual(rows[0]["anomaly_percentile"], 1.0)
            self.assertIn("not a diagnosis", rows[0]["interpretation"])

    def test_same_participant_is_excluded_from_neighbors(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manifest = self._fixture(root)
            records = load_manifest(manifest)
            records[-1] = type(records[-1])(
                records[-1].patch_path,
                records[-1].sample_id,
                records[0].participant_id,
                records[-1].slide_id,
                records[-1].group,
            )
            features = np.vstack([
                extract_features(r.patch_path, 64) for r in records
            ])
            rows = score_records(records, features, "REFERENCE", k=2)
            x = next(row for row in rows if row["sample_id"] == "x")
            self.assertNotIn(
                "r1", [n["sample_id"] for n in x["neighbors"]]
            )

    def test_manifest_rejects_duplicate_sample_ids(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manifest = self._fixture(root)
            lines = manifest.read_text().splitlines()
            manifest.write_text("\n".join(lines + [lines[1]]) + "\n")
            with self.assertRaisesRegex(
                ValueError, "sample_id values must be unique"
            ):
                load_manifest(manifest)


if __name__ == "__main__":
    unittest.main()
