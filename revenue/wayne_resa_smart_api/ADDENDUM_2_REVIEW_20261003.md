# Wayne SMART API — Addendum 2 review, October 3

**A2 source review: complete. Submission readiness: HOLD.**

This continues [issue 15914](https://github.com/woahwhattheheck/commons/issues/15914) and `WRESA-SMART-ERP-API-RESPONSE-ZAXIALFIN2314-20260917`. The original AxialFin, Keystone, and predecessor work remains credited through [PR 11166](https://github.com/woahwhattheheck/commons/pull/11166) and [PR 16455](https://github.com/woahwhattheheck/commons/pull/16455).

The September 19 packet accurately recorded that its public snapshot did not expose A2. The October 3 acquisition now closes that particular source gap. The response owner still lacks a complete current BidNet package, actual bidder evidence, an authorized offer, and buyer acceptance.

## Primary-source recovery

| Source | Completed retrieval, UTC | Bytes | SHA-256 |
|---|---|---:|---|
| [Official listing](https://www.resa.net/administrative-support/purchasing/request-for-proposal/) | 2026-10-03T23:18:31.011776Z | 135,151 | `f73c708ed5540eef05b601807fc5da3e98d11d3f5d41b236e8ada993d1cf8faa` |
| [Addendum 2 PDF](https://www.resa.net/downloads/purchasing/addendum_2_-_smart_enterprise_integration_and_api_services.pdf) | 2026-10-03T23:18:42.902359Z | 539,007 | `2343b3a5266aeb47d440174f41adee5b167141c6c567bc44764581ed2a31e497` |

Both public GETs returned 200 and complete bodies; the PDF matched its Content-Length. The listing links the PDF directly. Its 34 physical pages yielded exactly one question and one answer for each number 1–150. Citations below use **answer number and physical PDF page**, not assumed printed page labels.

The PDF's HTTP Last-Modified was September 21, 2026, 13:48:30 GMT. Embedded creation/modification metadata also date to September 21. Those observations do not establish an issuance date or prove publication on A1's announced September 18 date. The older listing and five earlier source identities remain in [SOURCE_REGISTER.md](SOURCE_REGISTER.md).

## Material interpretations for the current packet

This compact map identifies where the older packet needs correction. The source references also identify the answer context that a response owner must retain.

| Topic | Current treatment | A2 reference |
|---|---|---|
| Experience and references | Assess assigned people; prior-employer and major-subcontract work can qualify. Evidence remains missing. | 1–3 p.1; 18 p.6; 90 pp.23–24 |
| Certification | Current SOC 2/ISO certification is not a minimum gate; control evidence remains necessary. | 25 p.8; 73 pp.19–20 |
| Schedule | Award and discovery govern dates; no fixed replacement launch date is established. | 6 p.2; 21 p.7; 39 p.11; 49 p.13; 59 p.16; 109 p.27 |
| Technical evidence | Scope covers API work and affected components; the 80% API and relevant ledger obligations remain. | 43 p.12; 52 p.14; 70 p.19; 120/123 p.29; 140 p.33 |
| Availability | 99.99% concerns contractor-controlled API components; measurement remains open. | 44 p.12; 51 p.14; 61 p.16; 85 p.22; 108 pp.26–27 |
| Warranty/support | Ninety days follows written acceptance; additional purchased support is optional. | 87 p.23; 118 p.28; 125 p.30; 137 p.32 |
| Award/funding | Single-vendor award; no funded purchase order at award. | 67 p.18; 96 p.24; 138 p.32 |
| Commercial inputs | Quantities remain unfinalized; cooperative purchases carry the 2% fee. | 4 p.2; 22/24 p.7; 79 p.21; 88 p.23 |

A138's plural vendor wording must be read alongside A67/A96. It does not support reclassifying the opportunity as a prequalified pool. Internally, keep prospective contract access separate from an actual funded order, staffing authorization, or revenue.

### Insurance schedule now available

A17 begins on p.4; the table occupies **pp.5–6**. Both table pages were visually inspected.

| Coverage | Stated minimum |
|---|---|
| General liability | $1,000,000 per occurrence |
| Workers' compensation | Applicable law |
| Employer liability | $500,000 each accident; disease policy limit; disease per employee |
| Automobile liability | $1,000,000 combined single limit per occurrence |
| Umbrella/excess | $2,000,000 per occurrence and aggregate |
| Technology/professional liability | $2,000,000 per claim and aggregate |
| Cyber/privacy liability | $2,000,000 per claim and aggregate |

The response owner needs the actual coverage documents and the required additional-insured endorsements for general and automobile liability, mapped to A17's coverage wording. A76 p.20 also remains part of contracting review. The old statement that no numeric schedule was recovered is obsolete; this review does not establish that any policy, endorsement, or timing requirement has been met.

## Crosswalk for remaining owner decisions

The following is an internal work map. It supplies references and evidence tasks, without manufacturing proposal values or treating discovery questions as completed work.

| Existing packet area | Additional A2 anchors | Evidence or decision still needed |
|---|---|---|
| Staffing, entity standing, subcontracting and work location | 14 p.4; 19/20 pp.6–7; 26/27 p.8; 68 p.18; 75/76 p.20; 89 p.23; 97 p.25 | Named team, role capacity, verified entity facts, proposed resource locations, and actual permissions. Remote delivery cannot establish an offshore approval. |
| SMART discovery, access and integrations | 5 p.2; 29–33 p.9; 46 p.13; 100 p.25; 150 p.34 | An authorized inventory of schemas, rules, consumers, sandbox access, data permissions and integration dependencies. Existing synthetic domain labels remain proposals. |
| Platforms, language and scope | 34 p.10; 56 p.15; 136 p.32; 143 p.33; 148/149 p.34 | A justified API design and a bounded deliverable list. Assess A149 in its question context alongside A56; do not erase the explicit pricing/support options elsewhere. |
| Hosting, operations, data location and recovery | 38 p.11; 45 p.12; 47/50 pp.13–14; 62 p.17; 71 p.19; 78 p.21; 85 p.22; 115/116 p.28; 124 pp.29–30 | Deployment responsibility matrix, costs, connectivity approval, measurement boundaries, recovery objectives and an evidence plan. No environment is supplied by this review. |
| Security assessment and development tools | 37 pp.10–11; 55 p.15; 73 pp.19–20; 80 p.21; 129 pp.30–31 | Documented control/assessment scope, qualified personnel, approval path and tool safeguards. The recovered source is not permission to disclose protected project material. |
| Custom artifacts and existing intellectual property | 41 pp.11–12; 57 pp.15–16 | Component inventory, provenance, applicable licenses and an authorized contract review. No rights are assigned here. |
| Pricing, optional units and cooperative use | 16 p.4; 24 p.7; 42 p.12; 47/48 p.13; 67 p.18; 79 p.21; 88 p.23; 136–138 p.32 | Owner-approved assumptions, quantities, inclusions, exclusions and funding evidence. Attachment A remains blank. |
| Deadline and full-package acknowledgment | 95 p.24; existing A1 record | Retain the existing October 16 noon Eastern record; verify the complete current submission package and obtain actual acknowledgment before any readiness promotion. |

The companion [REQUIREMENTS.md](REQUIREMENTS.md) retains original RFP text and section citations while pointing affected rows here. Its F.1 phase labels are historical source text. The [readiness checklist](SUBMISSION_READINESS.md) retains missing qualification, insurance, commercial, access and acceptance evidence.

## Actual review and retained evidence

Two public requests recovered **674,158 bytes** in one bounded acquisition; acquisition plus PDF inspection/extraction took **19.409230 seconds**, with a 16,640 KiB peak child process and 17,920 KiB wrapper. The acquisition ended at 2026-10-03T23:18:43.015919Z with no remaining process.

The complete 150-pair text was reviewed in two ranges, 1–50 and 51–150. A separate single retained-file read for the latter range confirmed its byte/SHA identity and all 100 assigned pairs. The table and uptime pages 5, 6 and 12 were rendered from the pinned PDF and inspected. Those three rendering calls exited 0 in 0.396376 seconds; their peak child usage was 11,008 KiB.

| Intermediate evidence | Bytes | SHA-256 |
|---|---:|---|
| Layout-preserving text | 107,912 | `894cfb83891fb1bd848ec4a41e950eb97c47f1b71b4d3f39e6c6332caf7a022b` |
| Page/number-indexed Q/A JSON | 130,404 | `a77000bb6c9b70692c345dc729e6076c733fe373c51fc3b82e4ae98d9c3eb549` |
| Acquisition receipt | 24,389 | `707b952d77846ccfb872e787f3a7e9b8a470848b7b28ea8b0548509740d2b6b4` |

The Q/A transfer used the shared file-chunk consumer with 11 parts and 12 actual calls, ending in a complete record and exit 0. It checked protocol ranges and exporter-reported pins; it did not independently recompute a JavaScript content digest. The retained native acquisition and reader supplied the content-identity checks. Raw buyer files, full extracted text, Q/A content and page images remain intermediate evidence under the existing source-publication policy.

This change updates five Markdown files. It adds no implementation, quotation, signature or submission artifact and claims no new execution of the historical lab.

## Contact boundary

The existing [Dewpoint/Wayne do-not-route instruction](https://tokenjunkielabs.slack.com/archives/C0C2BE7K0KA/p1789715018120989) remains in force. Source recovery does not authorize another route, resend, follow-up or direct buyer contact. An actual permitted provider/owner event is required to reconsider that boundary. The dated source review closes its own claim without closing the underlying opportunity or its remaining evidence work.
