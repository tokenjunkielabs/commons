# Massachusetts DDS IPMS RFI market-response compiler

This package implements the internal evidence-bound carrier for Massachusetts EOHHS/DDS solicitation `BD-27-1039-EHS01-ASHWA-133015` / `27EHSPMDDSIPMSRFI`.

It is intentionally fail-closed about buyer bytes and vendor facts. The compiler does **not** send a response, mutate COMMBUYS, claim TJLabs owns a production IPMS, invent legal/company/certification facts, invent prices, sign, spend, or claim an award/payment/revenue result.

## What it enforces

- strict source/amendment ledger with controlling vs. secondary authority, freshness, supersession and SHA-256 fields;
- immutable capability IDs and states `SUPPORTED | CONFIGURABLE | THIRD_PARTY | PLANNED | NOT_SUPPORTED | UNKNOWN`, with affirmative states evidence-bound to the exact capability subject;
- required responsible-AI/privacy facts, all evidence-bound when known;
- architecture and compatibility facts with explicit unknown/owner-input states;
- five-year TCO components separated by category, with owner/vendor-only input provenance and exact integer-cent arithmetic;
- deterministic question-to-answer response pack, canonical JSON, Markdown and tamper receipt;
- readiness limited to `RESEARCH_READY`, `RESPONSE_DRAFT_READY`, or `HOLD`;
- hostile validation for duplicate IDs/JSON keys, bool-int aliasing, unknown fields, malformed hashes/times, future/stale evidence, evidence transplant, source downgrade, unsupported affirmative capability claims, facial-recognition contradictions, missing privacy facts, TCO mismatch and receipt tamper.

## Source status on 2026-10-04

The [dated source update](SOURCE_UPDATE_2026-10-04.md) records the newly listed Q&A attachment and the elapsed October 1 opening. The notice's `Bid Type: OPEN` is a classification, not evidence of an active response window. No extension was observed.

`example_input.json` retains its September 15 evaluation and two-attachment generation. It is historical, incomplete input: attachment bytes and SHA-256 values remain unavailable. This documentation update does not refresh that generation or establish current readiness.

## CLI

```bash
python -m opportunities.mass_dds_ipms_rfi.compiler compile \
  opportunities/mass_dds_ipms_rfi/example_input.json \
  --json-out /tmp/mass-dds-response.json \
  --md-out /tmp/mass-dds-response.md \
  --receipt-out /tmp/mass-dds-receipt.json

python -m opportunities.mass_dds_ipms_rfi.compiler verify \
  opportunities/mass_dds_ipms_rfi/example_input.json \
  /tmp/mass-dds-response.json \
  /tmp/mass-dds-receipt.json
```

The checked-in example is deliberately incomplete and retains its documented `HOLD` posture; no compiler execution was performed for this source update. Any later reuse requires a separately acquired and reconciled current buyer-document generation, including amendments, plus company/contact/product identity, evidence for material capability/privacy/architecture/compatibility claims, owner/vendor TCO inputs, and required response fields. The elapsed RFI window is not reopened by an internal draft or receipt.

## Future RFR/RFQ reuse

The response JSON exposes source IDs, capability states, privacy values, five-year TCO totals and blockers in stable machine-readable form. When a later RFR/RFQ appears, carry forward only evidence whose source/currentness still validates; do not infer production behavior from this RFI research packet.
