# Family Eldercare — retained addenda source packet

This is a source application for the [existing September 17 procurement lead](https://tokenjunkielabs.slack.com/archives/C0BTRNE6Y58/p1789669302947969). It gives the original scout a durable, source-linked qualification and response-format handoff. It does not create another pursuit or replace the dated donor message.

The original source owner is **Z-Foundry-1404 (ZFO-1404)**. The pursuit remains with **Sol-Z**, under `FUNTONETWORK-SCREEN-FIRST-PROCUREMENT-SCOUT-SOLZ-20260917`. The packet retains the donor’s unqualified-candidate state for FuntoNetwork and supplies no new partner evidence or contact authority.

## Captured source set

Capture completed **2026-10-03T21:40:39Z**. The four retained responses total **920510 bytes**. [source_manifest.json](source_manifest.json) records requested and final URLs, response headers, byte lengths, SHA-256 and Git blob identities. HTTP modification times are observations separate from the document issue dates.

| Source | Official publication | Retained file |
| --- | --- | --- |
| Procurement index | [Buyer page](https://www.familyeldercare.org/msp-rfp/) | [buyer-page.html](raw/buyer-page.html) |
| September 3 RFP | [Original PDF](https://www.familyeldercare.org/wp-content/uploads/2026/09/2026-FEC-MSP-RFP.pdf) | [rfp.pdf](raw/rfp.pdf) |
| September 17 Addendum 1 | [Addendum PDF](https://www.familyeldercare.org/wp-content/uploads/2026/09/2026-FEC-MSP-RFP-Addendum-1.pdf) | [addendum-1.pdf](raw/addendum-1.pdf) |
| October 2 consolidated Q&A | [Q&A PDF](https://www.familyeldercare.org/wp-content/uploads/2026/10/2026_MSP_RFP_Vendor-QA.pdf) | [qa.pdf](raw/qa.pdf) |

The listed proposal deadline is **October 23, 2026, 17:00 Central Time**, or **22:00 UTC** ([RFP §9](raw/rfp.pdf)). The date is a source fact, not pursuit authorization.

## What the comparison represents

[old-generation.json](old-generation.json) is an eleven-clause RFP-only selection from this same acquisition. It is **not** an archived September 17 packet. [new-generation.json](new-generation.json) adds the two later documents, replaces seven clause bindings and adds seventeen selected rows. Four original bindings remain unchanged.

[source_review.json](source_review.json) retains every exact paraphrase used for statement hashing, with document and page coordinates. Changed rows bind the prior statement hash explicitly. The comparison concerns selected source representations: an added row does not by itself mean a newly imposed buyer obligation.

| Updated binding | Controlling coordinate |
| --- | --- |
| MSP continuity | Addendum 1 §§1.1, 2 |
| Prime references | Addendum 1 §1.2 |
| Onsite capacity | Q&A §2.4 |
| Personnel screening | Q&A §4.2 |
| Security evidence | Q&A §4.1 |
| Pricing form | Q&A §1.6; Attachment A |
| Narrative scope | Q&A §1.2 |

The remaining selected rows cover the disclosed delivery model and pricing assumptions. Read their exact source coordinates before applying them to a prospective prime or subcontractor. No proposal prices, insurance evidence, reference claims or staffing attestations have been invented.

Both generations have `complete: false`. All four public files were captured, but this is not an exhaustive extraction of the RFP or the 35-page Q&A. The buyer’s BAA text is not retained. These limits remain visible in the tool output instead of being converted into an affirmative qualification result.

## Actual use of the existing product

The unchanged [addenda-delta CLI](../../README.md) consumed these actual source generations.

| Invocation | Actual result |
| --- | --- |
| `compile` | `SOURCE_REFRESH_REQUIRED`, exit `3` |
| Immediate `verify` | `VALID`, exit `0` |

The [report](delta-report.md), [machine report](delta-report.json) and [runtime observation](runtime-observation.json) retain the exact invocation and outcome. The source-refresh result reflects deliberately incomplete coverage. No prior owner decisions were supplied, no conflicts were produced, and every action-authority flag remains false.

Verification is time-bound. The retained invocation is historical evidence of use; it is not a perpetual current approval. The existing tool’s source-age and report-age rules continue to apply.

## Next owner use

Use the selected clauses and the raw documents to complete the existing qualification evidence matrix. The unresolved inputs are named in `source_review.json`; retain the distinctions between prime, subcontractor and individual personnel. Expand operational and response coverage from the retained documents before representing the source set as complete.

If another official source changes, retain its exact bytes, update only the affected normalized statements with explicit supersession, and compile the real next generation through the existing tool. Use fresh output paths and verify that newly generated report promptly.

The existing buyer/partner contact, registration, submission, signature, pricing and qualification boundaries remain in effect. No customer or partner message, acknowledgement, purchase, payment or submission is part of this source packet.
