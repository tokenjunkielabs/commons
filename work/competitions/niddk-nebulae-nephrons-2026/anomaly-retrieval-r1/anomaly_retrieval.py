#!/usr/bin/env python3
"""Deterministic image-patch anomaly/retrieval baseline for the NIDDK
"From Nebulae to Nephrons" discovery challenge.

This is a discovery aid, not a clinical diagnostic system. It intentionally
uses simple, inspectable image descriptors and emits nearest-neighbor evidence
alongside each anomaly score.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np
from PIL import Image

FEATURE_VERSION = "nebulae-r1-rgb16-grad8-lbp16-stats-v1"
EPS = 1e-9


@dataclass(frozen=True)
class Record:
    patch_path: Path
    sample_id: str
    participant_id: str
    slide_id: str
    group: str


def _safe_unit_hist(values: np.ndarray, bins: int, lo: float, hi: float,
                    weights: np.ndarray | None = None) -> np.ndarray:
    hist, _ = np.histogram(values, bins=bins, range=(lo, hi), weights=weights)
    hist = hist.astype(np.float64)
    total = float(hist.sum())
    if total > 0:
        hist /= total
    return hist


def extract_features(path: Path, size: int = 128) -> np.ndarray:
    """Extract a compact, deterministic, inspectable patch descriptor."""
    with Image.open(path) as im:
        im = im.convert("RGB")
        im.thumbnail((size, size), Image.Resampling.BILINEAR)
        rgb = np.asarray(im, dtype=np.float64) / 255.0

    if rgb.ndim != 3 or rgb.shape[2] != 3 or min(rgb.shape[:2]) < 3:
        raise ValueError(f"image too small or invalid RGB image: {path}")

    feats: list[np.ndarray] = []
    for c in range(3):
        feats.append(_safe_unit_hist(rgb[..., c], 16, 0.0, 1.0))

    gray = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    gy, gx = np.gradient(gray)
    mag = np.hypot(gx, gy)
    angle = (np.arctan2(gy, gx) + math.pi) % math.pi
    feats.append(_safe_unit_hist(angle, 8, 0.0, math.pi, weights=mag))

    center = gray[1:-1, 1:-1]
    neighbors = [
        gray[:-2, :-2], gray[:-2, 1:-1], gray[:-2, 2:],
        gray[1:-1, 2:], gray[2:, 2:], gray[2:, 1:-1],
        gray[2:, :-2], gray[1:-1, :-2],
    ]
    lbp = np.zeros(center.shape, dtype=np.uint8)
    for bit, neigh in enumerate(neighbors):
        lbp |= ((neigh >= center).astype(np.uint8) << bit)
    feats.append(_safe_unit_hist(lbp, 16, 0.0, 256.0))

    sat = rgb.max(axis=2) - rgb.min(axis=2)
    tissue_fraction = np.mean((sat > 0.05) & (gray < 0.95))
    summaries = np.array([
        float(gray.mean()), float(gray.std()),
        float(np.quantile(gray, 0.10)), float(np.quantile(gray, 0.50)),
        float(np.quantile(gray, 0.90)), float(mag.mean()), float(mag.std()),
        float(tissue_fraction),
    ], dtype=np.float64)
    feats.append(summaries)
    return np.concatenate(feats)


def load_manifest(path: Path) -> list[Record]:
    required = {"patch_path", "sample_id", "participant_id", "slide_id", "group"}
    rows: list[Record] = []
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"manifest missing columns: {sorted(missing)}")
        for i, row in enumerate(reader, start=2):
            if any(not (row.get(k) or "").strip() for k in required):
                raise ValueError(f"blank required value at manifest row {i}")
            p = Path(row["patch_path"]).expanduser()
            if not p.is_absolute():
                p = (path.parent / p).resolve()
            rows.append(Record(
                p, row["sample_id"].strip(), row["participant_id"].strip(),
                row["slide_id"].strip(), row["group"].strip()
            ))
    if len(rows) < 3:
        raise ValueError("need at least 3 patches")
    ids = [r.sample_id for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("sample_id values must be unique")
    return rows


def robust_scale(x: np.ndarray, ref_mask: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    ref = x[ref_mask]
    if ref.shape[0] < 2:
        raise ValueError("reference cohort must contain at least 2 patches")
    med = np.median(ref, axis=0)
    mad = np.median(np.abs(ref - med), axis=0)
    scale = 1.4826 * mad
    fallback = np.std(ref, axis=0)
    scale = np.where(scale > EPS, scale, fallback)
    scale = np.where(scale > EPS, scale, 1.0)
    return (x - med) / scale, med, scale


def _eligible_neighbor_indices(records: Sequence[Record], target_i: int,
                               ref_indices: np.ndarray) -> np.ndarray:
    target = records[target_i]
    keep = [
        j for j in ref_indices.tolist()
        if j != target_i and records[j].participant_id != target.participant_id
    ]
    return np.asarray(keep, dtype=np.int64)


def score_records(records: Sequence[Record], features: np.ndarray,
                  reference_group: str | None, k: int) -> list[dict]:
    if k < 1:
        raise ValueError("k must be >= 1")
    groups = np.asarray([r.group for r in records], dtype=object)
    ref_mask = np.ones(len(records), dtype=bool)
    if reference_group is not None:
        ref_mask = groups == reference_group
        if int(ref_mask.sum()) < 2:
            raise ValueError(
                f"reference group {reference_group!r} has fewer than 2 patches"
            )
    z, _, _ = robust_scale(features, ref_mask)
    ref_indices = np.flatnonzero(ref_mask)

    raw: list[dict] = []
    for i, record in enumerate(records):
        eligible = _eligible_neighbor_indices(records, i, ref_indices)
        if eligible.size == 0:
            raise ValueError(
                f"no eligible reference neighbors for {record.sample_id}; "
                "participant exclusion removed the full reference cohort"
            )
        distances = np.linalg.norm(z[eligible] - z[i], axis=1)
        order = np.argsort(distances, kind="stable")
        take = order[: min(k, len(order))]
        chosen = eligible[take]
        chosen_dist = distances[take]
        neighbors = [{
            "sample_id": records[j].sample_id,
            "participant_id": records[j].participant_id,
            "slide_id": records[j].slide_id,
            "group": records[j].group,
            "distance": float(d),
        } for j, d in zip(chosen.tolist(), chosen_dist.tolist())]
        raw.append({
            "sample_id": record.sample_id,
            "participant_id": record.participant_id,
            "slide_id": record.slide_id,
            "group": record.group,
            "anomaly_score": float(np.median(chosen_dist)),
            "neighbors": neighbors,
        })

    order = sorted(
        range(len(raw)),
        key=lambda i: (raw[i]["anomaly_score"], raw[i]["sample_id"])
    )
    denom = max(1, len(raw) - 1)
    for rank, i in enumerate(order):
        raw[i]["anomaly_percentile"] = float(rank / denom)
    for item in raw:
        item["feature_version"] = FEATURE_VERSION
        item["interpretation"] = (
            "discovery-only anomaly/retrieval evidence; not a diagnosis, "
            "disease probability, or clinical recommendation"
        )
    return sorted(raw, key=lambda x: (-x["anomaly_score"], x["sample_id"]))


def fingerprint_manifest(records: Sequence[Record]) -> str:
    h = hashlib.sha256()
    for r in records:
        for value in (r.sample_id, r.participant_id, r.slide_id, r.group):
            h.update(value.encode())
            h.update(b"\0")
        with r.patch_path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
    return h.hexdigest()


def run(manifest: Path, output: Path, reference_group: str | None,
        k: int, image_size: int) -> dict:
    records = load_manifest(manifest)
    feats = np.vstack([extract_features(r.patch_path, image_size) for r in records])
    scored = score_records(records, feats, reference_group, k)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as fh:
        for row in scored:
            fh.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")

    receipt = {
        "feature_version": FEATURE_VERSION,
        "patch_count": len(records),
        "reference_group": reference_group,
        "reference_count": (
            sum(r.group == reference_group for r in records)
            if reference_group is not None else len(records)
        ),
        "k": k,
        "image_size": image_size,
        "manifest_data_sha256": fingerprint_manifest(records),
        "output_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "top_anomaly_sample_id": scored[0]["sample_id"],
        "evidence_boundary": (
            "image-patch retrieval/anomaly baseline only; output is not "
            "pathologist/nephrologist validation and is not a clinical diagnosis"
        ),
    }
    receipt_path = output.with_suffix(output.suffix + ".receipt.json")
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8"
    )
    return receipt


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--reference-group", default=None)
    p.add_argument("--k", type=int, default=5)
    p.add_argument("--image-size", type=int, default=128)
    return p


def main() -> int:
    args = build_parser().parse_args()
    receipt = run(
        args.manifest, args.output, args.reference_group, args.k, args.image_size
    )
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
