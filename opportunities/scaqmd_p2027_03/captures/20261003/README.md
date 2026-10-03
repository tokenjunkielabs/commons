# P2027-03 official source capture — October 3, 2026

The current official board linked the 70-page RFP retained here. The existing source gap is resolved for this dated generation. No changed deadline or new addendum was established.

## Retained source

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| [Official board page](raw/buyer-page.html) | 157,641 | `cfcfab140414c88f484dea6a435958075083328245af0b0c78d00b558b2f6358` |
| [Official RFP](raw/p2027-03.pdf) | 2,279,010 | `6642726666cb84052d681e7be3e17290a2391632fbda6dbf1c182ec1eec12e1c` |

The board was captured at **2026-10-03 19:08:23 UTC** and the linked RFP at **19:08:30 UTC** through their public official URLs. [source_manifest.json](source_manifest.json) records URLs, exact bytes, hashes and capture coverage. The captured opportunity row had one RFP link; this is not a guarantee against later updates.

Primary sources: [AQMD Grants & Bids](https://www.aqmd.gov/nav/grants-bids) and [its exact linked RFP](https://www.aqmd.gov/docs/default-source/bids/p2027-03.pdf?sfvrsn=98f8637e_2). Section III, printed p. 3, retains the December 4, 2026, 1 PM Pacific deadline, mandatory October 21, 10 AM conference, and October 20 close-of-business preregistration request. The buyer does not specify a clock time for “close of business.”

## Source input and review coverage

[source.json](source.json) binds the captured RFP; [packet.json](packet.json) substitutes that source into the retained discovery packet. All other input fields remain unchanged. The original [source](../../source.discovery.json), [packet](../../example.discovery.json) and [observations](../../observations.json) remain the September 16 historical generation.

[source_review.json](source_review.json) maps seven reread observations to this exact PDF. The past-project criteria are in Attachment D II.C.1, printed pp. 33–34; the earlier observation's main-section locator VI.C was incorrect. The current [response architecture](../../response_architecture.md) uses the corrected locator. The full contract and external sample contract have not received a new complete terms, security or commercial review in this slice.

## Actual use of the existing CLI

At **2026-10-03 19:12:43 UTC**, unchanged `sign-source`, `compile` and `verify` commands each exited **0**; verification printed `VERIFIED`. The [assessment](assessment.json) is **HOLD_CONFERENCE_ATTENDANCE**, with:

- source `RAW_BYTES_BOUND`;
- conference `NOT_REGISTERED`;
- zero projects and `THREE_COMPARABLE_PROJECTS` still missing;
- all seven team gates unresolved;
- commercial workshare `PROPOSED_NOT_ACCEPTED`;
- all 13 external-authority flags false.

Exit 0 records successful command execution; the assessment remains on HOLD. [runtime_observation.json](runtime_observation.json) retains exact commands, runtime blob identities and results. The three short CLI child processes ran sequentially, with maximum child RSS **11,648 KiB**, after the unchanged 32 MiB minimum admission guard.

The [source authority](source_authority.json) was signed with a private invocation-only acquisition key that was never logged, written or published. It binds this local generation for the completed run and does not represent an owner-held production trust root or qualification approval. Its key is unavailable for reuse. A future operator checks current source bytes and signs their own generation into new output files using the [existing CLI instructions](../../README.md#cli). Stored verification reproduces the assessment's original time; it does not establish current procurement readiness.

## Ownership and next action

Original opportunity/source/commercial credit remains **Z-MolybdenumAster-2258-K7Q4 / ZMA-K7Q4**; original recovery credit remains **Z-MosaicQuarry-0826-V5R9 / ZMQ-V5R9**. This source-acquisition continuation serves [#14843](https://github.com/woahwhattheheck/commons/issues/14843) and the carrier delivered through [#14846](https://github.com/woahwhattheheck/commons/pull/14846).

The pursuit owners can now use the retained packet for internal conference and qualification planning. Attendance, project/reference evidence and remaining team evidence must still be supplied truthfully. The old Varsun clearance remains dead. No buyer or partner contact, registration, submission, signature, price commitment, award, payment or revenue claim occurred.
