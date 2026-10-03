# Indiana FSSA No Wrong Door: retained source and intake worklist

This is the October 3, 2026 source handoff for the existing **RFP 27-88284 / event 004980000088284** lead. The State board and its directly linked ZIP are retained here, together with the main RFP PDF, extracted text from eight selected official documents, and the outputs of the existing solicitation-ingest CLI.

**Original source and pursuit owner:** Z-Sol.  
**Original operation:** `IN-FSSA-NWD-MAC-2788284-PARTNER-FIRST-ZSOL-20260917`.  
**Original handoff:** [September 17 build-demand thread](https://tokenjunkielabs.slack.com/archives/C0BTRNE6Y58/p1789691547239749).

The original lead's missing-package-bytes item is now resolved for this captured generation. Its partner-first posture and unestablished prime qualifications remain. PCG, Maximus, Guidehouse and Sellers Dorsey remain the original research candidates; this packet does not select, qualify, commit or contact any firm. Vendor networking submissions are retained only inside the official ZIP and were not read for this handoff.

## Use the packet

Start with [the source review](source-review.md), then the generated [evidence worklist](compiled/gaps.md). [pack.json](pack.json) is the actual source input; [active_set.json](compiled/active_set.json) provides the normalized requirements and deadline. [selector.json](compiled/selector.json) uses the existing response-module solicitation schema for later evidence-supported module selection.

The actual compile returned **OWNER_REVIEW_READY / exit 0**, and the immediate verify returned **verified=true / exit 0**. [The runtime observation](runtime-observation.json) retains the exact inputs, command outcomes and runtime-source identities.

The ingest status describes whether the captured sources produce a usable owner-review worklist. It does not establish a qualified prime or partner, satisfy the worklist's **32 mandatory/scored evidence gaps**, or authorize a proposal. Every external and commercial authority flag remains false. No candidate module catalog, financial information, price, signature, registration, submission or outreach was supplied.

## Source findings that affect the next owner decision

- The main RFP cover and milestone table, reinforced by Attachment H, say **October 28, 2026 at 3:00 PM Eastern Time**. The packet normalizes Indianapolis local time to **19:00 UTC**. The board's `EST` abbreviation is preserved in the raw capture, not used to shift the RFP deadline by an hour.
- Three same/similar-service client references must reach the State directly from the clients by that deadline. Retaining a blank reference form is not evidence that anyone has supplied a reference.
- One respondent is responsible for performance. Proposed subcontractors need disclosed workshares, qualifications and an executed subcontract or signed agreement letter. The State can consider combined qualifications; no commitment is inferred from a networking form or research-candidate name.
- Financial stability remains an evidence request under Attachment E section 3, with a preferred D&B-report route and stated financial-statement alternatives. Section 14 is expressly removed. The capture does not create a universal two-year operating-history threshold.
- The attachment outline and filenames identify **L as AI questions** and **M as infrastructure overview**; the mandatory checklist reverses those titles. Both documents remain required and the discrepancy is retained.
- Questions are due October 7 and written responses/amendments are scheduled for October 14. This capture precedes that planned publication; a later source check is needed to consume any actual new answers or amendments.
- Hosting requirements are conditional on proposed scope. Attachment M places Policy P.05 compliance at implementation, while requiring an applicability/architecture response. No current certification or hosting approval is inferred.

## Coverage and next action

The archive contains **35 members**. This handoff reads the 20-page main RFP and the main-document text of Attachments E, F, H, J, K, L and M. The 37 normalized rows are a selected source worklist, not an exhaustive procurement or contract review.

The sample contract, cloud contract attachments, cost workbook, IVOSB form, conference deck, incorporated policies and networking submissions remain unreviewed here. Their bytes remain in the original ZIP where included; external policy documents are not captured by this packet. Extracted DOCX text does not establish table, checkbox, header/footer or embedded-object fidelity. No form has been filled, signed or altered.

The pursuit owner can use the worklist to decide whether an evidenced prime/teaming route exists, bind real company/team/reference/financial facts, and review the remaining incorporated documents. The scheduled October 14 answers are a source-follow-up point, not permission to contact the State or submit a response.

## Reproduce the retained generation

From repository root:

```bash
python -B -m revenue.procurement_solicitation_ingest.ingest compile \
  --pack revenue/procurement_solicitation_ingest/packets/in_fssa_nwd_mac_20261003/pack.json \
  --out-dir /tmp/fssa-nwd-current-source

python -B -m revenue.procurement_solicitation_ingest.ingest verify \
  --pack revenue/procurement_solicitation_ingest/packets/in_fssa_nwd_mac_20261003/pack.json \
  --selector /tmp/fssa-nwd-current-source/selector.json \
  --active-set /tmp/fssa-nwd-current-source/active_set.json \
  --gaps /tmp/fssa-nwd-current-source/gaps.json \
  --markdown /tmp/fssa-nwd-current-source/gaps.md \
  --readiness /tmp/fssa-nwd-current-source/readiness.json \
  --receipt /tmp/fssa-nwd-current-source/receipt.json
```

Use a new output directory because the CLI creates output files exclusively. The supplied evaluation timestamp was set from actual process UTC during this run. The seven-day source-age setting is a packet-processing parameter, not a buyer qualification rule. Recompiling or verifying these retained inputs proves their deterministic relationship; it does not fetch new sources or advance the source observation time.

## Exact sources

- [Current State board](https://secure.in.gov/idoa/procurement/current-business-opportunities/)
- [Official linked ZIP](https://secure.in.gov/idoa/proc/solicitations/files/004980000088284.zip)
- [Retained ZIP](raw/official-package.zip), [board](raw/buyer-page.html), and [main RFP](raw/main-rfp.pdf)
- [Source manifest](source_manifest.json): HTTP metadata, byte counts, SHA-256/Git identities, all archive members and selected-member bindings

The raw ZIP is **3,420,805 bytes**, SHA-256 `0bc2c4a47aa2cba6b5732b9308c6d581befd9df957dc03c22796349b5279b867`. Its HTTP Last-Modified header reports October 2, 2026. No earlier ZIP generation was retained, so no byte-level claim is made about what changed since the September 17 lead.
