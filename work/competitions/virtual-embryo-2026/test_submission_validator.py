import unittest
import numpy as np

from submission_validator import validate_anndata


class FakeAnnData:
    def __init__(self, x, genes, spatial=None):
        self.X = x
        self.n_obs, self.n_vars = x.shape
        self.var_names = genes
        self.obsm = {} if spatial is None else {"spatial_3D": spatial}


class SubmissionValidatorTests(unittest.TestCase):
    def setUp(self):
        self.genes = [f"g{i}" for i in range(500)]

    def test_t3_valid_contract(self):
        adata = FakeAnnData(
            np.zeros((4, 500), dtype=np.float32),
            self.genes,
            np.zeros((4, 3), dtype=np.float32),
        )
        result = validate_anndata(adata, task="T3", expected_genes=self.genes, min_cells=4)
        self.assertTrue(result.valid, result.errors)

    def test_gene_order_fails_strict_and_warns_when_explicitly_allowed(self):
        genes = self.genes.copy()
        genes[0], genes[1] = genes[1], genes[0]
        adata = FakeAnnData(np.zeros((4, 500)), genes, np.zeros((4, 3)))
        strict = validate_anndata(adata, task="T3", expected_genes=self.genes, min_cells=4)
        self.assertFalse(strict.valid)
        self.assertIn("gene order mismatch", strict.errors[0])
        relaxed = validate_anndata(
            adata, task="T3", expected_genes=self.genes, min_cells=4, allow_reorder=True
        )
        self.assertFalse(relaxed.valid)
        self.assertEqual(1, len(relaxed.warnings))
        self.assertTrue(any("reorder the file" in e for e in relaxed.errors))

    def test_rejects_nonfinite_negative_and_bad_spatial(self):
        x = np.zeros((4, 500), dtype=np.float32)
        x[0, 0] = -1
        x[1, 1] = np.nan
        spatial = np.zeros((4, 2), dtype=np.float32)
        adata = FakeAnnData(x, self.genes, spatial)
        result = validate_anndata(adata, task="T3", expected_genes=self.genes, min_cells=4)
        self.assertFalse(result.valid)
        self.assertTrue(any("NaN or infinity" in e for e in result.errors))
        self.assertTrue(any("negative" in e for e in result.errors))
        self.assertTrue(any("at least 3 columns" in e for e in result.errors))

    def test_t1_requires_whole_transcriptome_count_but_not_spatial(self):
        genes = [f"g{i}" for i in range(32_285)]
        adata = FakeAnnData(np.zeros((2, 32_285), dtype=np.float32), genes)
        result = validate_anndata(adata, task="T1", expected_genes=genes, min_cells=2)
        self.assertTrue(result.valid, result.errors)

    def test_cell_range_gate(self):
        adata = FakeAnnData(np.zeros((4, 500)), self.genes, np.zeros((4, 3)))
        low = validate_anndata(adata, task="T2", expected_genes=self.genes, min_cells=5)
        self.assertFalse(low.valid)
        high = validate_anndata(
            adata, task="T2", expected_genes=self.genes, min_cells=1, max_cells=3
        )
        self.assertFalse(high.valid)


if __name__ == "__main__":
    unittest.main()
