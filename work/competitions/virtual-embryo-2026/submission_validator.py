#!/usr/bin/env python3
"""Offline schema validator for Virtual Embryo Challenge AnnData submissions.

This validates file-format constraints only. It does not score biological quality.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Sequence

import numpy as np

TASK_GENE_COUNTS = {"T1": 32_285, "T2": 500, "T3": 500}
DEFAULT_MIN_CELLS = 1_000
DEFAULT_MAX_FILE_MB = 1_200.0


@dataclass
class ValidationReport:
    valid: bool
    task: str
    n_cells: int
    n_genes: int
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)


def load_expected_genes(path: str | os.PathLike[str]) -> list[str]:
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    genes = [line.strip() for line in lines if line.strip() and not line.lstrip().startswith("#")]
    if not genes:
        raise ValueError("expected gene list is empty")
    if len(set(genes)) != len(genes):
        raise ValueError("expected gene list contains duplicates")
    return genes


def _data_values(matrix: Any) -> np.ndarray:
    """Return explicit matrix values without densifying scipy sparse matrices."""
    if hasattr(matrix, "tocsr") and hasattr(matrix, "data"):
        return np.asarray(matrix.data)
    return np.asarray(matrix)


def _matrix_is_2d(matrix: Any) -> bool:
    shape = getattr(matrix, "shape", None)
    return shape is not None and len(shape) == 2


def _first_gene_mismatch(expected: Sequence[str], received: Sequence[str]) -> str:
    for idx, (want, got) in enumerate(zip(expected, received)):
        if want != got:
            return f"gene order mismatch at index {idx}: expected {want!r}, received {got!r}"
    if len(expected) != len(received):
        return f"gene count mismatch: expected {len(expected)}, received {len(received)}"
    return "gene lists differ"


def validate_anndata(
    adata: Any,
    *,
    task: str,
    expected_genes: Sequence[str],
    min_cells: int = DEFAULT_MIN_CELLS,
    max_cells: int | None = None,
    allow_reorder: bool = False,
) -> ValidationReport:
    task = task.upper()
    if task not in TASK_GENE_COUNTS:
        raise ValueError(f"unsupported task {task!r}; expected T1, T2, or T3")

    errors: list[str] = []
    warnings: list[str] = []
    n_cells = int(getattr(adata, "n_obs", getattr(getattr(adata, "X", None), "shape", (0, 0))[0]))
    n_genes = int(getattr(adata, "n_vars", getattr(getattr(adata, "X", None), "shape", (0, 0))[1]))

    required_gene_count = TASK_GENE_COUNTS[task]
    if len(expected_genes) != required_gene_count:
        errors.append(
            f"official gene list for {task} must contain {required_gene_count} names; got {len(expected_genes)}"
        )

    received_genes = [str(name) for name in getattr(adata, "var_names", [])]
    if len(received_genes) != n_genes:
        errors.append(f"var_names length {len(received_genes)} does not match X columns {n_genes}")
    if len(set(received_genes)) != len(received_genes):
        errors.append("var_names contains duplicate genes")

    if received_genes != list(expected_genes):
        same_gene_set = len(received_genes) == len(expected_genes) and set(received_genes) == set(expected_genes)
        if allow_reorder and same_gene_set:
            warnings.append("gene names match but are not in official order; diagnostic only")
            errors.append("gene order differs from official upload order; reorder the file before upload")
        else:
            errors.append(_first_gene_mismatch(expected_genes, received_genes))

    x = getattr(adata, "X", None)
    if x is None:
        errors.append("missing X expression matrix")
    elif not _matrix_is_2d(x):
        errors.append("X must be a 2D cells x genes matrix")
    else:
        shape = tuple(int(v) for v in x.shape)
        if shape != (n_cells, n_genes):
            errors.append(f"X shape {shape} does not match AnnData dimensions {(n_cells, n_genes)}")
        values = _data_values(x)
        if not np.isfinite(values).all():
            errors.append("X contains NaN or infinity")
        if np.any(values < 0):
            errors.append("X contains negative values")

    if n_cells < min_cells:
        errors.append(f"cell count {n_cells} is below minimum {min_cells}")
    if max_cells is not None and n_cells > max_cells:
        errors.append(f"cell count {n_cells} exceeds board maximum {max_cells}")

    if task in {"T2", "T3"}:
        obsm = getattr(adata, "obsm", {})
        if "spatial_3D" not in obsm:
            errors.append('missing obsm["spatial_3D"]')
        else:
            spatial = np.asarray(obsm["spatial_3D"])
            if spatial.ndim != 2:
                errors.append('obsm["spatial_3D"] must be a 2D matrix')
            else:
                if spatial.shape[0] != n_cells:
                    errors.append(
                        f'obsm["spatial_3D"] rows {spatial.shape[0]} do not match cell count {n_cells}'
                    )
                if spatial.shape[1] < 3:
                    errors.append(
                        f'obsm["spatial_3D"] must have at least 3 columns; got {spatial.shape[1]}'
                    )
                elif not np.isfinite(spatial[:, :3]).all():
                    errors.append('obsm["spatial_3D"] first three columns contain NaN or infinity')

    return ValidationReport(
        valid=not errors,
        task=task,
        n_cells=n_cells,
        n_genes=n_genes,
        errors=errors,
        warnings=warnings,
    )


def validate_file(
    input_path: str | os.PathLike[str],
    *,
    task: str,
    expected_genes: Sequence[str],
    min_cells: int = DEFAULT_MIN_CELLS,
    max_cells: int | None = None,
    max_file_mb: float = DEFAULT_MAX_FILE_MB,
    allow_reorder: bool = False,
) -> ValidationReport:
    path = Path(input_path)
    if path.suffix.lower() != ".h5ad":
        return ValidationReport(False, task.upper(), 0, 0, ["submission must be an .h5ad file"])
    if not path.is_file():
        return ValidationReport(False, task.upper(), 0, 0, [f"file does not exist: {path}"])

    size_mb = path.stat().st_size / 1_000_000
    if size_mb > max_file_mb:
        return ValidationReport(
            False,
            task.upper(),
            0,
            0,
            [f"file size {size_mb:.2f} MB exceeds {max_file_mb:.2f} MB limit"],
        )

    try:
        import anndata as ad  # lazy: unit tests exercise the validator without this optional dependency
    except ImportError as exc:
        raise RuntimeError("anndata is required to read .h5ad files; install it in the competition environment") from exc

    adata = ad.read_h5ad(path)
    return validate_anndata(
        adata,
        task=task,
        expected_genes=expected_genes,
        min_cells=min_cells,
        max_cells=max_cells,
        allow_reorder=allow_reorder,
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, choices=["T1", "T2", "T3"])
    parser.add_argument("--input", required=True, help="submission .h5ad")
    parser.add_argument("--genes", required=True, help="official gene list, one gene per line in released order")
    parser.add_argument("--min-cells", type=int, default=DEFAULT_MIN_CELLS)
    parser.add_argument("--max-cells", type=int, default=None, help="board maximum from current index.json")
    parser.add_argument("--max-file-mb", type=float, default=DEFAULT_MAX_FILE_MB)
    parser.add_argument(
        "--allow-reorder",
        action="store_true",
        help="diagnose an identical gene set in the wrong order; still fails validation until the file is reordered",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    expected = load_expected_genes(args.genes)
    report = validate_file(
        args.input,
        task=args.task,
        expected_genes=expected,
        min_cells=args.min_cells,
        max_cells=args.max_cells,
        max_file_mb=args.max_file_mb,
        allow_reorder=args.allow_reorder,
    )
    print(report.to_json())
    return 0 if report.valid else 2


if __name__ == "__main__":
    raise SystemExit(main())
