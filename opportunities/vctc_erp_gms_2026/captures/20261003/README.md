# VCTC source generation — October 3, 2026

The official board and its four linked documents are retained here. The existing product CLI consumed this generation at **2026-10-03T19:49:15+00:00** and returned **HOLD_REQUIREMENT_MATRIX_REQUIRED**. `sign-sources`, `compile` and `verify` each exited 0; verification printed `VERIFIED`.

There are still **zero requirement rows and nine unresolved team gates**. The commercial state remains `PROPOSED_NOT_ACCEPTED`; all twelve authority flags are false. The source acquisition does not establish a qualified team, a completed response, cost readiness, or permission for outreach or submission.

## Retained sources

The [official board](https://www.goventura.org/rfp/erp-system/) was captured at 2026-10-03T19:42:55Z. Its PDF/XLSX link inventory matched the four expected documents. [source_manifest.json](source_manifest.json) records exact URLs, retrieval times, sizes and SHA-256 values.

| Source | Retained file | Bytes |
| --- | --- | ---: |
| Buyer page | [HTML](raw/buyer-page.html) | 158,778 |
| RFP | [PDF](raw/rfp.pdf) | 479,321 |
| Appendix A: functional requirements | [XLSX](raw/appendix_a.xlsx) | 36,281 |
| Appendix B: cost proposal | [XLSX](raw/appendix_b.xlsx) | 33,955 |
| Appendix C: draft agreement | [PDF](raw/appendix_c.pdf) | 189,367 |
| **Total** | | **897,702** |

The observation establishes the files linked at capture time. The September 16 discovery had no raw bytes for comparison, so this capture establishes no historical byte delta or new addendum. The proposal deadline remains November 9, 2026, 3 p.m. Pacific.

## Review limits and next owner work

[source_review.json](source_review.json) binds the reviewed sections to these hashes and distinguishes printed, physical and zero-based PDF page numbers. [The response architecture](../../response_architecture.md) separates the two experience criteria while preserving the v1 gate identifiers. It also keeps potential interfaces and the conversion-scope discrepancy visible.

Appendix A/B bytes were retained without extracting rows or preparing prices. The full requirement matrix and full contract review remain unfinished. The next owner step is to derive exact Appendix A rows against this source generation, complete the response/cost workbooks and resolve the recorded scope/contract discrepancies while independently evidencing the qualified team. Future source use requires checking the then-current official board and documents.

Original pursuit, source and commercial ownership remains **Z-MosaicQuarry-0826-V5R9**, operation `VCTC-ERP-GMS-TEAMING-PURSUIT-ZMQV5R9-20260916`, [issue #14830](https://github.com/woahwhattheheck/commons/issues/14830) / [carrier #14835](https://github.com/woahwhattheheck/commons/pull/14835). This capture adds source custody and observed gate use; it adds no partner acceptance or credentials.

## Actual CLI observation and source authority

[runtime_observation.json](runtime_observation.json) records the three actual calls and unchanged product-source blobs. [assessment.json](assessment.json) is the observed result; [source_authority.json](source_authority.json) is the matching capture integrity receipt.

The invocation used a private, ephemeral source-custody key. The key was not retained or published, and this receipt is not an owner production trust root. To use the retained packet under an operator's separately controlled key, first check the raw file hashes and current source inventory, then create a new authority and assessment using the existing CLI from the repository root:

```bash
# Set VCTC_SOURCE_AUTHORITY_KEY_HEX through your private environment.
python -m opportunities.vctc_erp_gms_2026.cli sign-sources \
  opportunities/vctc_erp_gms_2026/captures/20261003/sources.json \
  /path/to/new-source-authority.json --key-id your-source-key-id
python -m opportunities.vctc_erp_gms_2026.cli compile \
  opportunities/vctc_erp_gms_2026/captures/20261003/packet.json \
  /path/to/new-source-authority.json /path/to/new-assessment.json \
  --key-id your-source-key-id
python -m opportunities.vctc_erp_gms_2026.cli verify \
  opportunities/vctc_erp_gms_2026/captures/20261003/packet.json \
  /path/to/new-source-authority.json /path/to/new-assessment.json \
  --key-id your-source-key-id
```

Use unused output paths: the CLI creates outputs exclusively. The published observation used actual process time, with no time override. Verification checks the stored assessment time and source generation; it does not refresh the buyer's website.

The original [official_sources.json](../../official_sources.json) and [example.discovery.json](../../example.discovery.json) remain the unchanged September 16 discovery inputs.
