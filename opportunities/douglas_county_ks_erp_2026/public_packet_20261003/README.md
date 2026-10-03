# Douglas County ERP: public packet retrieval, 3 October 2026

**Result: the public document manifest is retained; the public download action redirects to login, so controlling document contents remain unretained.** This completes the bounded anonymous-retrieval attempt requested by [#15862](https://github.com/woahwhattheheck/commons/issues/15862). It does not complete the controlling-packet dependency for [#15848](https://github.com/woahwhattheheck/commons/issues/15848).

The original six-file package from [#15853](https://github.com/woahwhattheheck/commons/pull/15853), its contributor credit, commercial ownership and qualification state are preserved.

## Captured source

Three anonymous page requests returned HTTP 200. A later anonymous GET to the page's top-level download action returned HTTP 302 to the login route. All four complete response bodies are retained: 175,626 bytes.

| Source | File | HTTP | Bytes | SHA-256 |
| --- | --- | ---: | ---: | --- |
| [County purchasing](https://www.dgcoks.gov/administration/purchasing) | [county-purchasing.html](county-purchasing.html) | 200 | 109,859 | `456b4e7425c8218c56b28286f6bb86687698f7871e524ca43fda1cd495c79c2a` |
| [Portal home](https://douglascountyks.bidsandtenders.net/) | [portal-home.html](portal-home.html) | 200 | 29,955 | `88aae8305e1ba44fb61af868728df25cbf340db39a066ee82f2bb12c4307e203` |
| [Tender detail](https://douglascountyks.bidsandtenders.net/Module/Tenders/en/Tender/Detail/75e76acb-87a3-4199-9fae-d5736d38e590) | [tender-detail.html](tender-detail.html) | 200 | 35,671 | `fa8709fc60a1f7bb48b07d6c1b66b3dadab66031ffdc24acd41058b278f93a78` |
| [Public download action](https://douglascountyks.bidsandtenders.net/Module/Tenders/en/Tender/DownloadBidDocuments/75e76acb-87a3-4199-9fae-d5736d38e590) | [download-all-response.html](download-all-response.html) | 302 | 141 | `32b9f70036afb6c3a52ad24a61afcc9b7712b376a6543b712f1530c7a06e28e3` |

[manifest.json](manifest.json) records exact requested/final URLs, per-request UTC start/completion, response metadata, byte lengths and Git blob identities. These hashes identify HTML responses, including the redirect body. They are not hashes of the RFP or its attachments.

The tender page identifies RFP-2026-0012 as open and lists closing at 2:00 p.m. CDT on 20 October 2026. Its question deadline is 4:00 p.m. CDT on 30 September 2026, already passed at capture. Submissions are online. [Source: retained tender detail](tender-detail.html).

## Document metadata in the anonymous response

The page's embedded Documents and Addendums stores contain these rows. Dates and page counts are transcribed metadata; document-row timestamps do not themselves state a timezone. A zero listed page count is displayed as unavailable. File formats are not inferred from friendly names.

| Group | Portal display name | Created date | Listed pages |
| --- | --- | --- | ---: |
| Document | RFP-2026-0012.pdf | 2026-09-15 | Not shown |
| Document | RFP-2026-0012 Enterprise Resource Planning (ERP) System | 2026-09-15 | 33 |
| Document | Attachment 11 (Data Conversions) | 2026-09-15 | 1 |
| Document | Attachment 12 (Project Staffing) | 2026-09-15 | 2 |
| Document | Attachment 13 (Functional Requirements) | 2026-09-15 | 21 |
| Document | Attachment 14 (Cost) | 2026-09-15 | 5 |
| Document | Attachment 15 (Business Process Documentation) | 2026-09-15 | 41 |
| Document | Attachments 1, 4-10 in Word Format | 2026-09-16 | 8 |
| Addendum | Addendum #2 | 2026-09-30 | 7 |
| Addendum | Addendum #1 | 2026-09-24 | 1 |

Exact document IDs and full portal timestamps are retained in [manifest.json](manifest.json). Both addenda are present in the directly captured response. This establishes the captured page's metadata, not full document or historical coverage.

## Measured access boundary

The raw page configures individual document/addendum download commands as hidden. It also contains registered-plan-taker notice panels configured as hidden. Those source declarations alone do not establish what a browser displayed or whether every download route is unavailable.

The page separately defines a top-level `Download Bid Documents` action that is not configured as hidden. An anonymous GET to that exact route at **2026-10-03T22:25:12.964082Z** returned **HTTP 302**, with **Location: /Module/Tenders/en/Login**. Capture completed at **2026-10-03T22:25:21.861041Z**. The full 141-byte redirect body is [retained here](download-all-response.html); the status and Location header are recorded in the manifest.

The redirect was not followed. No cookies, credentials, registration, sign-in, terms action, question or submission route was used. No hidden per-document endpoint was invoked. Their uninvoked backend behavior remains unknown. The request's no-login boundary therefore stops this retrieval attempt at the measured public download-action redirect.

## Handoff

The eight listed document payloads, including the controlling RFP, and two addendum payloads remain unretained. Teaming permission, qualifications, references, insurance, evaluation, pricing forms, signature requirements, security/privacy, integrations and conversion requirements therefore remain unresolved in the original package. No document-specific requirement or section/page extraction is claimed.

A future authorized owner can continue from these exact source identities and portal document IDs if an independently public source or permitted access route becomes available. Keep the original commercial package and its owner as the pursuit carrier. No County or partner contact, price commitment, proposal, spend, award or revenue occurred.

## Capture record

The initial three requests ran in 24.536913 seconds with a 4 MiB aggregate body bound and 17,280 KiB peak RSS. The later download-action request ran in 8.896964 seconds with an 8 MiB body bound and 15,872 KiB peak RSS. Each response was retained and hashed; all bodies completed. The existing bounded file exporter transferred the original source captures without another download. No process remains.

This was public source acquisition and metadata parsing. No test suite, model decision or buyer action was run.
