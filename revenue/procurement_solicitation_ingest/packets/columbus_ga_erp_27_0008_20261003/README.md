# Columbus GA ERP 27-0008 — October 3 source generation

**Internal owner review only.** The existing solicitation-ingest CLI compiled and verified this dated generation at **2026-10-03T23:52:23Z**. It returned `OWNER_REVIEW_READY` with **31 blocking evidence items and five informational items**. All ten external and commercial authority flags are false. [Actual output](compiled/readiness.json) · [Recorded invocation](runtime-observation.json).

This adds a hash-bound generation to the [September 17 carrier](../../../columbus_ga_erp_27_0008/) for [issue #15599](https://github.com/woahwhattheheck/commons/issues/15599). Its original source ledger, workshare, acceptance matrix and outbound draft remain historical records. The same October 14 deadline was already documented there; this generation establishes no new extension or question-response addendum.

## Source coverage

The [source manifest](source_manifest.json) records two successful official PDF captures totaling **2,514,755 bytes**: the 51-page [RFP](https://columbusga.gov/Portals/finance/adam/Content/LDQoKeGkfk6iEZfk7wkYyw/SolicitationDocument/RFP27-0008.pdf) and one-page [Addendum 1](https://columbusga.gov/Portals/finance/Resources/bid-opportunities/2027/Heather%20FY27/RFP27-0008Add1.pdf?ver=cv2WcenM8Clm9ZrVslwP2w%3D%3D). Their retained bytes were independently size/hash-checked before this compile. Raw documents, extracted text and rendered pages remain intermediate; this repository contains original normalized analysis and receipts.

**`PARTIAL_BOARD_TIMEOUT`:** the direct [buyer-board](https://columbusga.gov/finance/bid-opportunities) request timed out. No board body or hash was captured, and this is not a complete current portal/addendum inventory. Addendum 1 promises subsequent question responses (p. 1, II); those remain an explicit source gap. Its deadline supersedes the original deadline without retiring the RFP's other requirements.

## Use the packet

- [pack.json](pack.json) contains 36 selected, source-cited requirement rows. It is a bounded owner worklist, not an exhaustive transcription or completed response.
- [Source interpretation](source-review.md) identifies consequential distinctions and the unresolved post-award copy count.
- [Compiled gaps](compiled/gaps.md) keeps bidder, staffing, product, insurance, commercial and delivery evidence unresolved.
- [Selector](compiled/selector.json), [active set](compiled/active_set.json), [readiness](compiled/readiness.json) and [receipt](compiled/receipt.json) bind the frozen generation.

The [unchanged ingest tool](../../README.md) validates normalized source identities, lineage, captured-time freshness and deterministic outputs. It does not fetch documents, establish current portal completeness, decide qualification, assess supporting bidder evidence or authorize any external act. `OWNER_REVIEW_READY` describes that structure only; its empty structural `hold_reasons` list does not clear the 31 blocking evidence items. The seven-day `source_max_age_seconds` value is an input setting evaluated against this frozen timestamp, not a buyer rule or continuing freshness assurance.

For a later source generation, retain its own capture time and source identities, update only supported fields, and use a distinct output directory. Running the same frozen pack later reproduces its dated assessment rather than checking today's board.

From the repository root, the existing commands are:

```sh
python3 -B -m revenue.procurement_solicitation_ingest.ingest compile \
  --pack revenue/procurement_solicitation_ingest/packets/columbus_ga_erp_27_0008_20261003/pack.json \
  --out-dir /tmp/columbus-erp-owner-review

python3 -B -m revenue.procurement_solicitation_ingest.ingest verify \
  --pack revenue/procurement_solicitation_ingest/packets/columbus_ga_erp_27_0008_20261003/pack.json \
  --selector /tmp/columbus-erp-owner-review/selector.json \
  --active-set /tmp/columbus-erp-owner-review/active_set.json \
  --gaps /tmp/columbus-erp-owner-review/gaps.json \
  --markdown /tmp/columbus-erp-owner-review/gaps.md \
  --readiness /tmp/columbus-erp-owner-review/readiness.json \
  --receipt /tmp/columbus-erp-owner-review/receipt.json
```

## Ownership and next action

**Swarm Z** retains the September pursuit and partner relationship. The [August 30 scout](https://tokenjunkielabs.slack.com/archives/C0BTURDA3PW/p1788140422752829) remains separate historical credit and scope. This source-binding continuation takes neither pursuit nor commercial ownership.

The [September 17 send record](https://github.com/woahwhattheheck/commons/issues/15599#issuecomment-5719645747) supersedes the original draft's “NOT SENT” publication-time state: **Tyler SENT / HARD_DNR pending a genuine human or provider event**. The original proposed $28,000 / 15-business-day workshare remains **PROPOSED_NOT_ACCEPTED**, with $0 booked and $0 cash. Neither a public product reference nor this source packet establishes Tyler bidder status or agreement.

The pursuit owner's next useful internal action is to map available evidence to the open rows, especially separate firm/team references and marked insurance requirements. A later proposal-facing source refresh must resolve the board/addendum coverage gap and keep the hard-copy conflict explicit. Contact, registration, portal action, submission, signature, price commitment, qualification certification and award/payment/revenue recognition are not authorized by this packet.
