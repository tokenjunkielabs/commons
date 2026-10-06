# Virtual Embryo offline submission validator

Bounded local preflight for the 2026 Virtual Embryo Challenge upload contract. It validates file/schema integrity only; it does **not** score biological quality or make an official-submission claim.

## Current official contract encoded

- AnnData `.h5ad` input.
- The exact board contract comes from the current official `panels/index.json`; gene cardinality, coordinate requirement, and cell bounds are board-specific.
- In particular, `T2:embryo:val_interp` currently requires 498 genes, while the released heart and Task-3 boards require 500. Do not use a task-wide 500-gene assumption.
- `.X` must be a 2D cells × genes matrix with finite, non-negative values. Sparse matrices are checked via their explicit values without forced densification.
- Spatial boards require `obsm["spatial_3D"]` with one row per cell and at least three finite coordinate columns.
- File-size gate defaults to 1,200 MB, matching the current challenge rule.
- `obs["celltype"]` is intentionally ignored because the official scorer does not use submitted labels.

Download both the current machine-readable board index and the named gene-panel file from `https://virtualembryo.ai/challenge/data`. The tool consumes those files at runtime instead of embedding a snapshot that will become stale when new boards open.

## Usage

```bash
python submission_validator.py \
  --board T2:embryo:val_interp \
  --index index.json \
  --input pred.h5ad \
  --genes T2__embryo__val_interp.genes.txt
```

Strict gene order is always required for a valid result. `--allow-reorder` is diagnostic-only when the set is identical but order differs: it identifies the case cleanly, emits a warning, and still returns validation failure until the file is reordered.

Exit codes: `0` valid format, `2` validation failure. Missing runtime dependencies raise an execution error instead of being misreported as a valid/invalid submission.

## Focused checks

```bash
python -m unittest test_submission_validator.py
python -m py_compile submission_validator.py test_submission_validator.py
```

The unit seam uses in-memory AnnData-like objects, so it checks the contract logic without needing to manufacture, download, or upload competition data.
