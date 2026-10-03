# Wayne SMART API source register

This is an internal source record for RFP **WRESA-50-2026-2027-07**, first prepared on 2026-09-19 UTC and updated on 2026-10-03 UTC. It preserves AxialFin, Keystone, and predecessor contributions through the [original response-lab history](https://github.com/woahwhattheheck/commons/pull/16455). Source recovery does not establish bidder qualification, buyer acceptance, commercial readiness, or authority to contact anyone.

## Recovered primary sources

| ID | Official source | Source date and extent | Retrieval UTC | SHA-256 of retrieved bytes |
|---|---|---|---|---|
| RFP | [API Services RFP](https://www.resa.net/downloads/purchasing/rfp_wresa-50-2026-2027-07_api_services.pdf) | Printed issue date 2026-08-14 (p.2); 32 PDF pages, printed pages 2–32 after the cover | 2026-09-19T16:27:58.863507Z | `61376d559b4cc5aab02652073434e77459e489ec5ba82a984db37a6b7214cdb6` |
| A1 | [Addendum 1](https://www.resa.net/downloads/purchasing/addendum_1_-_smart_enterprise_integration_and_api_services.pdf) | One PDF page; no printed issuance date | 2026-09-19T16:28:04.214498Z | `757fc2800d23891e56f144cd5208a2ce03fed622b670d83561b1529cd7304197` |
| WEB | [September 19 purchasing/RFP snapshot](https://www.resa.net/administrative-support/purchasing/request-for-proposal/) | Live listing observed 2026-09-19; snapshot, not an immutable source | 2026-09-19T16:28:10.511259Z | `72f71bdd594c58efc21c39a5fdba7742ec4f99ca883194e94ce9a762903ad361` |
| XLSX | [Attachment A pricing template](https://www.resa.net/downloads/purchasing/attachment_a_-_pricing_schedule_api_services.xlsx) | One worksheet, `Attachment A - Pricing Schedule`, used range A1:F72; blank bidder fields | 2026-09-19T16:45:57.347092Z | `79d8cf422dbbc991ef90732b82243049afafd7f18d6eec2e4c03af6952d074ef` |
| TERMS | [General CoPro+ terms](https://www.resa.net/downloads/purchasing/coprocontracttermsandconditions.docx) | General consortium terms, sections 1–11; no API-specific issue date stated | 2026-09-19T16:46:02.660521Z | `5996db5c525e0c3db0725c446bd25ba1df05367be26a6be3e903b6b0e178aaa8` |
| WEB-20261003 | [Purchasing/RFP listing](https://www.resa.net/administrative-support/purchasing/request-for-proposal/) | Live snapshot observed October 3; links A2 | 2026-10-03T23:18:31.011776Z | `f73c708ed5540eef05b601807fc5da3e98d11d3f5d41b236e8ada993d1cf8faa` |
| A2 | [Addendum 2](https://www.resa.net/downloads/purchasing/addendum_2_-_smart_enterprise_integration_and_api_services.pdf) | 34 physical PDF pages; Q/A 1–150; no issue date inferred from metadata | 2026-10-03T23:18:42.902359Z | `2343b3a5266aeb47d440174f41adee5b167141c6c567bc44764581ed2a31e497` |

Retrieved byte sizes: RFP 710,008; A1 201,539; WEB 134,834; XLSX 20,531; TERMS 106,806. Local analysis copies and extraction metadata are in `source-work/`; these copyrighted source files are intermediate evidence, not proposed repository deliverables. Only the original Markdown analysis is intended for publication.

October 3 retained byte sizes: WEB-20261003 **135,151** and A2 **539,007**. Both GETs completed with HTTP 200; A2 matched its 539,007-byte Content-Length. The dated September 19 records remain historical evidence. Acquisition identities and the current review are in [October 3 Addendum 2 review](ADDENDUM_2_REVIEW_20261003.md).

Page citations in this packet use the RFP's **printed page number**, which equals its one-based PDF page position. The cover is PDF page 1 and has no printed number. A1 citations use its sole PDF page. A2 citations use **physical one-based PDF pages** and answer numbers.

## Document identity and dating

- RFP cover, body, footers, and official filename identify API Services, WRESA-50-2026-2027-07. Its embedded PDF title and keywords incorrectly describe WRESA-49 waste-removal services. Identification here follows the visible document, not that metadata.
- The RFP PDF creation/modification metadata correspond to 2026-08-17 UTC; they are not the printed issue date. A1 has September 11 UTC creation/modification metadata but no printed date; no issuance date is inferred from those metadata.
- XLSX metadata record creation on 2026-07-29 and modification on 2026-08-11; TERMS metadata record creation/modification on 2019-07-23. These are file metadata, not inferred procurement issuance dates or proof of inapplicability. TERMS is linked by the current official listing and referenced by RFP §3.8. Its precise applicability and reconciliation with the API RFP still require qualified review.
- The older `/about/purchasing/requests-for-proposals` address in historical work was not usable during recovery. WEB above is the official current listing reached for this review.

## Controlling date changes and unresolved source coverage

| Matter | Original RFP p.2 | Recovered controlling update | Status |
|---|---|---|---|
| Responses to questions | September 11, 2026 | A1 revision 1: September 18, 2026 | Revised date recovered |
| Proposal receipt deadline | September 16, 2026, noon | A1 revision 2: **October 16, 2026, noon Eastern Time**; WEB agrees | Revised date recovered; not a submission authorization |
| Q&A publication | RFP provides questions/addendum process | A1 announced A2 for September 18; it was absent from the September 19 snapshot | **Recovered and reviewed October 3**; the earlier absence is a dated observation. See [October 3 Addendum 2 review](ADDENDUM_2_REVIEW_20261003.md). |
| Implementation schedule | F.1 p.10 contains September/end-2026/January labels | A2 answers 6, 21, 39, 49, 59 and 109 now govern the calendar review | Retain the base labels as history; use the [October 3 Addendum 2 review](ADDENDUM_2_REVIEW_20261003.md) before proposing dates. No implementation schedule has been agreed. |

WEB labels some times “EST”; A1 explicitly uses “Eastern Time.” This packet preserves noon Eastern Time and does not invent a UTC conversion from conflicting seasonal shorthand.

The September 19 listing linked the base RFP, Attachment A pricing schedule, and A1. The October 3 snapshot also links the recovered A2. The workbook and separately linked general CoPro+ terms were subsequently recovered and inspected read-only; [ATTACHMENTS.md](ATTACHMENTS.md) maps their fields and relevant sections. **Blank template recovered does not mean a quote exists; general terms recovered does not mean their applicability has been legally resolved or accepted.** BidNet may contain further current instructions or attachments; no authenticated BidNet submission package was recovered. The source set is sufficient to ground a bounded internal lab, **not to certify the entire live solicitation package complete**.

## Lineage and contact boundary

- Continue [Commons issue 15914](https://github.com/woahwhattheheck/commons/issues/15914), operation `WRESA-SMART-ERP-API-RESPONSE-ZAXIALFIN2314-20260917`, with original contributor credit retained through [PR 16455](https://github.com/woahwhattheheck/commons/pull/16455).
- Historical merged [PR 11166](https://github.com/woahwhattheheck/commons/pull/11166) supplies the frozen 150-case shadow exercise (120 reconciled, 10 duplicate, 10 unknown, 10 unauthorized). That distribution is a synthetic predecessor fixture, **not an RFP-mandated benchmark or an accepted buyer test**.
- Preserve the [Dewpoint/Wayne do-not-route instruction](https://tokenjunkielabs.slack.com/archives/C0C2BE7K0KA/p1789715018120989): no second route, resend, follow-up, or direct Wayne contact. This packet grants no contact, pricing, signature, submission, or production authority.
- Read [REQUIREMENTS.md](REQUIREMENTS.md) for the source crosswalk and [SUBMISSION_READINESS.md](SUBMISSION_READINESS.md) for unresolved evidence and submission conditions. Architecture, proposed fixture semantics, workshare, and UAT remain distinct companion documents.
