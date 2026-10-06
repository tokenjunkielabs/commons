# Virtual Embryo offline submission validator

Bounded local preflight for the 2026 Virtual Embryo Challenge upload contract. It validates file/schema integrity only; it does **not** score biological quality or make an official-submission claim.

## Current official contract encoded

- AnnData `.h5ad` input.
- T1: exactly 32,285 released genes, in released order; no spatial requirement.
- T2/T3: exactly the 500-gene MERFISH panel, in released order; `obsm["spatial_3D"]` is required with one row per cell and at least three finite coordinate columns.
- `.X` must be a 2D cells × genes matrix with finite, non-negative values. Sparse matrices are checked via their explicit values without forced densification.
- Minimum cell count defaults to 1,000. Pass the board-specific current maximum from the challenge `index.json` with `--max-cells`.
- File-size gate defaults to 1,200 MB, matching the current challenge rule.
- `obs["celltype"]` is intentionally ignored because the official scorer does not use submitted labels.

The tool requires the official released gene list as a newline-delimited file. It does not embed a potentially stale gene order.

## Usage

```bash
python submission_validator.py \
  --task T3 \
  --input pred.h5ad \
  --genes merfish_500_genes.txt \
  --max-cells <current-board-maximum>
```

Strict gene order is always required for a valid result. `--allow-reorder` is diagnostic-only when the set is identical but order differs: it identifies the case cleanly, emits a warning, and still returns validation failure until the file is reordered.

Exit codes: `0` valid format, `2` validation failure. Missing runtime dependencies raise an execution error instead of being misreported as a valid/invalid submission.

## Focused checks

```bash
python -m unittest test_submission_validator.py
python -m py_compile submission_validator.py test_submission_validator.py
```

The unit seam uses in-memory AnnData-like objects, so it checks the contract logic without needing to manufacture or upload competition data.
