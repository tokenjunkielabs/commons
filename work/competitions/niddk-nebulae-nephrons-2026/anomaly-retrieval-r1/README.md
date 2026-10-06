# NIDDK Kidney AI — Nebulae → Nephrons anomaly/retrieval floor (R1)

This directory contains a deterministic image-patch anomaly/retrieval baseline for the NIDDK Kidney Artificial Intelligence Discovery Challenge: From Nebulae to Nephrons.

## What it is

anomaly_retrieval.py computes an inspectable descriptor for each image patch: RGB histograms, gradient orientation, coarse local-binary-pattern texture, and grayscale/edge/tissue-proxy statistics. Descriptors are robust-scaled against an optional reference cohort using median + MAD. Each patch is scored by its median distance to the k nearest eligible reference patches.

Retrieval excludes patches from the same participant, reducing an obvious same-person leakage path. Output includes the nearest-neighbor evidence used for each score.

The result is deliberately simple: a discovery floor for judging whether later learned embeddings actually improve rare-pattern retrieval while retaining inspectable evidence.

## Evidence boundary

This code does not diagnose kidney disease, estimate a disease probability, establish a novel pathology finding, or replace pathologist/nephrologist review. Challenge-grade novelty requires domain-expert interpretation and validation of candidate anomalies. R1 has only focused synthetic tests; it has not been scored on the future common NIDDK challenge image set.

The challenge requires exclusive use of publicly available/open KPMP data. Do not feed controlled-access KPMP data into this packet.

## Input

Prepare a CSV manifest with these columns:

patch_path,sample_id,participant_id,slide_id,group

patch_path may be absolute or relative to the manifest. sample_id must be unique. The baseline operates on ordinary PNG/JPEG/TIFF patches; whole-slide tiling belongs upstream so the exact official image-release contract can be adopted without changing the scorer.

## Run

Example:

python anomaly_retrieval.py --manifest manifest.csv --output anomaly.jsonl --reference-group REFERENCE --k 5

Dependencies: Python 3.11+, NumPy, Pillow.

The command writes anomaly.jsonl plus a deterministic anomaly.jsonl.receipt.json binding the parameters, feature version, manifest/image bytes and output SHA-256.

## Promotion gate

When NIDDK releases the common eligible image set, keep this R1 frozen and compare any learned model against the same patch/cohort split. A learned candidate should be promoted only if it improves domain-expert-confirmed rare-pattern retrieval or another challenge-aligned discovery measure—not merely because its unsupervised scores have a wider numeric spread.

Recommended first real-data evidence:

1. Bind image release/version and every patch to participant + slide.
2. Group splits by participant.
3. Run R1 unchanged.
4. Review top anomaly/retrieval neighborhoods with qualified kidney pathology/nephrology expertise.
5. Record candidate finding, retrieval evidence, false-positive theme, and reviewer disposition.
6. Only then test learned embeddings or semi-supervised anomaly models against the frozen baseline.

## Public sources pinned during build

- NIH challenge page: https://www.nih.gov/challenges/kidney-artificial-intelligence-discovery-challenge-nebulae-nephrons
  - retrieved 2026-10-06
  - launch 2026-09-15
  - registration opens 2026-11-05
  - submissions 2026-11-05 through 2027-04-29
  - $100,000 purse
  - open KPMP data only
  - image-based anomaly discovery with human/domain-expert interpretation
- KPMP Kidney Tissue Atlas: https://atlas.kpmp.org/
  - retrieved 2026-10-06
  - exposes Light Microscopic Whole Slide Images plus segmentation/pathomics and other modalities
  - data availability changes over time, so current counts are not hard-coded as a competition contract

No registration, HeroX account action, submission, prize claim, or clinical-performance claim is made by this R1 packet.
