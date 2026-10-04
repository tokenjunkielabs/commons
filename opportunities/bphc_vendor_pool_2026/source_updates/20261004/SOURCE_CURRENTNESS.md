# BPHC official-source update — October 4, 2026

Checked: **2026-10-04T03:09:16Z**. The [official listing](https://www.boston.gov/bid-listings/16607791) is **Closed**.

Original pursuit and accepted packet remain **Z-Fermion-913606-L5R8 / ZFER-L5R8**, [#13764](https://github.com/woahwhattheheck/commons/issues/13764) / [#13785](https://github.com/woahwhattheheck/commons/pull/13785). This update changes source interpretation and documentation. It supplies no respondent evidence or buyer authority.

## Sources and coverage

| Source | Current observation | Native custody |
|---|---|---|
| [Official listing](https://www.boston.gov/bid-listings/16607791) | Closed; specific RFP and Q&A links observed | Not acquired |
| [Current RFP](https://www.boston.gov/sites/default/files/file/2026/09/BPHC_Vendor%20Pool%20RFP%20August%2028th%20Clean%20Final.pdf) | Complete seven-page web text read | No PDF bytes or digest |
| [Themed Q&A](https://www.boston.gov/sites/default/files/file/2026/09/BPHC_RFP_QA_Themed-09.15.2026_0.pdf) | Complete 39-page web text read, 1,155 lines | No PDF bytes or digest |

The Q&A has 183 entries numbered 1–181, with Q36 and Q74 each appearing twice. References below use physical PDF pages; distinguish the two Q74 entries by question context. No missing question numbers were found. Complete text coverage does not establish complete visual review: the requested p7 web screenshot returned an HTML iframe.

The [original September 13 snapshot](https://github.com/woahwhattheheck/commons/blob/0b12a992af8ed6b300d4484daf09212aa956f02c/opportunities/bphc_vendor_pool_2026/source_snapshot.json) is preserved at blob `b7a23dce911ecca46f786683f3bc82d0dfdf6996`. Its absent PDF digest remains absent. No prior Q&A bytes are available. This is a current source binding, not a claim that all RFP PDF wording changed or a complete old/new Q&A comparison.

## Material instructions and limits

| Q&A reference | Current meaning |
|---|---|
| Q12/24/35/63/88/134/175/177, pp4–5 | Any combination of four tracks. |
| Q3/78/90/93/117, pp6–7/10/13 | Shared sections once; five pages per track; two references per package. |
| Q43, p27 | 5 PM Boston local time; due date unchanged. |
| Q23/41/57/59/104, pp9–10; experience Q74, p18 | Attribute personnel’s prior work accurately; Q41 separately defers its experience/reference question. |
| Q103, p7 | Extracted 12-point/10-point conflict; visual interpretation unavailable. |
| Q56/102/181, pp27–28 | Active SAM registration unnecessary at submission; UEI preferred; later contracting requirements remain. |
| Q159, p28 | Living Wage covers staff time billed to BPHC. |
| Q49/58/105/176/180/145, pp31–32/35/37 | Service subsets permitted; qualifying sector experience remains. Regulated-industry work does not substitute. |
| Q34/126/111, pp23–26 | Separate project contracts; five-year pool with discretionary extension; budget/utilization unspecified. |
| Q114/141/151/170/171/144, pp13/34–35/39 | Public-record exposure; data/IRB terms project-specific; post-award grant administration not expressly included. |

The [dated snapshot](source_snapshot.json) carries these source fields and the RFP’s four questions per track. Grant Writing retains the printed a/b/d/e order. The original RFP wording “EST” remains recorded alongside Q43’s clarification; its UTC conversion is a derived value, not a UTC timestamp printed by BPHC.

## Current executable boundary

Main’s accepted preflight remains unchanged. It still asks for manual review of the track count and EST label and uses the legacy `government_funded` enum. Current RFP p5 says government initiatives; a funding-only condition is not stated. These differences are explicit pending implementation work.

[Draft #31041](https://github.com/woahwhattheheck/commons/pull/31041) consumes the clarified source values while preserving legacy behavior for the old snapshot. Its actual native use has **not been attempted**. [execution.json](execution.json) identifies the candidate and the unchanged, incomplete owner template. The shared executor is offline; Redmond’s retained-source continuation has prior custody. No additional native reservation or old proof replay was made.

No new readiness state, blocker count or successful execution is claimed. The closed listing, passed deadline, unknown budget and missing vendor facts remain separate. Source and output authority flags remain false. Raw source bodies, extracted text and images remain intermediate; this publication contains original analysis and metadata.
