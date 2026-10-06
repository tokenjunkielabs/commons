# Quote CSV fields without changing export values

This source continuation repairs field quoting in `generateCSV`, in `src/lib/export-utils.ts` at **Stellar-Analysis/frontend@482ee456369418ef82c4056718cb82d3468f762b**. The existing implementation quotes only string values containing a comma. It leaves embedded quotes unescaped, leaves line breaks unquoted, and joins column labels without field escaping.

The patch adds one local field encoder and applies it to both column labels and the formatted row values. It encloses fields containing a comma, double quote, carriage return or line feed, and doubles embedded double quotes. The source change is **+7 / -2 lines**, in two hunks. This is an attributed Commons patch packet, not a change to the upstream branch.

## Source and actual export connection

| File or proposed artifact | Git blob | UTF-8 bytes |
| --- | --- | ---: |
| Original `src/lib/export-utils.ts` | `dcbf1e6e10be89b6b871c51f3da0d745a9f79147` | 13,242 |
| Proposed `src/lib/export-utils.ts` | `06166ec2e0bd0df466072ecc7463f00cc0bf8943` | 13,392 |
| `src/app/[locale]/analytics/export/page.tsx` | `e60172711db5a9f5cc5cf71ae924ab24da15c989` | 7,849 |
| Inspected `src/components/ExportDialog.tsx` | `f8eb21ce2495525d168ac1d0e5a2cf1075904c30` | 13,363 |
| `csv-field-quoting.patch` | `77c9b684c77c005c67a66935b1afc24c9f702c22` | 1,015 |

All three original files were acquired completely at the named donor commit. Their native file identities and independently computed UTF-8 Git-blob identities match. The complete donor `src` tree entry, transferred from the concurrent source worker, identifies the utility as mode `100644`; the patch preserves that mode.

The actual analytics export route imports `generateCSV` from `@/lib/export-utils`. Its Download CSV button calls `handleExport("csv")`; that branch passes `previewData` and the selected column IDs and labels to the utility. The function's declared `ExportRow` values include strings, numbers, booleans, null and undefined.

The observed route currently supplies date/numeric mock rows and fixed labels. No corrupt downloaded real-world row was observed, and no new mock row was generated or executed. The correction covers the utility's existing string-input contract; it does not replace the page's mock data or establish live analytics integration.

The separately inspected ExportDialog imports only the Excel generator. Its CSV option uses the server export endpoint, so it is not counted as a client-side `generateCSV` consumer. That dialog remains unchanged.

Source links:

- [Utility](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/src/lib/export-utils.ts)
- [Analytics export route](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/src/app/%5Blocale%5D/analytics/export/page.tsx)
- [Separate export dialog](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/src/components/ExportDialog.tsx)

## Format contract and behavior

[RFC 4180, section 2](https://www.rfc-editor.org/info/rfc4180/) documents a common CSV format. It describes header fields using the same format as data fields, enclosing fields that contain commas, quotes or line breaks, and escaping an embedded double quote by doubling it. The RFC is informational, not an Internet Standards Track specification.

The local encoder converts each supported scalar to its textual value, uses an empty field for nullish input, then applies that field-quoting rule. It is applied after the existing date and success-rate formatting, so those conversions retain their original order and output. The regex used for the quoting decision has no global flag or mutable cross-call position.

The existing record separator remains LF, and no byte-order mark, terminal newline, or additional format policy is introduced. This packet therefore makes a field-quoting claim, not a claim of complete RFC conformance or universal spreadsheet interoperability.

The public function signature, column order, row order, selected values, filename, MIME type, Blob construction and download call remain unchanged. JSON, Excel, PDF, ZIP construction, CRC code and download-resource handling are byte-for-byte unchanged. No other source file is modified.

## Source review and publication scope

The complete serialized patch was parsed against the exact preimage and reconstructed the proposed file byte for byte. Reverse application reconstructed the original. Both hunks and all 23 hunk rows were reviewed without truncation. An exact comparison of the entire source from the JSON section onward confirms that the other export paths and shared download helper remain unchanged.

These are checks of the actual source edit and artifact bytes. The CSV generator, date formatting, mock-data generator, DOM download path, application, browser, spreadsheet program and network were not executed. No CSV fixture, test suite, compiler, lint, dependency installation, workflow or upstream submission was run.

The bounded Commons query `"export-utils" "CSV"` and public Slack query `"export-utils.ts" "CSV"` returned no matches. They are limited overlap observations, not proof of exhaustive coverage or exclusive ownership. A local unsupported `count` argument was rejected before the first Slack request; the documented `limit` argument was then used for the initial native search. No failed provider request was retried.

## Attribution and included notices

The upstream project and its contributors retain authorship of the source and export page. Current-path history returned the root-relocation commit [59fad72d9fbef9cfd6f47e215392da44488fcdc4](https://github.com/Stellar-Analysis/frontend/commit/59fad72d9fbef9cfd6f47e215392da44488fcdc4), associated with christabel888. That identifies the relocation, not original or sole authorship of the utility. This packet claims only the narrow field-quoting continuation.

Three case-distinct MIT notices from the donor are included unchanged:

| Donor path | Included file | Git blob |
| --- | --- | --- |
| `docs/LICENCE.md` | `upstream-licence-mclaughlin.md` | `57740b9d4d86aedf5d518f2f363d5cf192c54127` |
| `docs/LICENSE.md` | `upstream-license-menke-laguna.md` | `af5411fa243cfcf2b61c79d081dbb6204e956041` |
| `docs/license.md` | `upstream-license-de-wet.md` | `4a766e268772888af5df56c3f6c608f68558b789` |

Those files preserve Michael Mclaughlin, Romain Menke and Antonio Laguna, and Declan de Wet's respective notices. Including them does not assign any particular utility line to those authors. No acceptance, award, payment or production deployment is claimed.
