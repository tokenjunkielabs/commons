# IMPO MTP 2055 bid-readiness compiler

Operation: `IMPO-MTP2055-BID-READINESS-ZERN6P2-20260914`

This package compiles a **non-authorizing owner-review** receipt and Markdown gate packet for the Indianapolis Metropolitan Planning Organization's 2055 Metropolitan Transportation Plan RFP. Candidate facts and evidence references are useful for structured review, but this package does not independently authenticate them and cannot mint external authority.

It does **not** contact IMPO, create or alter a vendor profile, register for the pre-bid meeting, sign a form, commit a price, transmit a proposal, accept a contract, or spend money. All external-authority bits are required to remain false; candidate JSON that attempts to set them true is rejected.

## Retained source capture — October 3, 2026

Use [captures/20261003/README.md](captures/20261003/README.md) for the dated official board, exact RFP and posted Addendum 1 bytes, source manifest, current-input binding, and actual compiler output. The original September input, page-reference catalog, public-source snapshot and owner decision packet remain historical records credited to their original owners.

The capture closes the missing base-PDF and posted-addendum byte gaps. Addendum 1 remains unsigned, and its date header conflicts with the RFP and current board; the capture keeps that discrepancy visible. The owner-review input retains the October 6, 2026, 5 PM Eastern deadline and all unresolved organization, staff, project, reference, document and commercial facts.

The RFP allows IMPO project examples while prohibiting IMPO references. The compiler counts experience and external-reference evidence separately; the dated input still supplies neither.

A saved receipt records its actual process-time evaluation. The existing current verifier expires receipts after five minutes; the published output is an observation of that run, not a reusable current-readiness credential. A later operator should compile the dated input into a new output directory and verify immediately, while separately refreshing source evidence when required.

## Why this opportunity is consequential

The published RFP states a $215,000 not-to-exceed budget, a September 16 question deadline, and an October 6 proposal deadline. The work covers a 20-24 month MTP update with regional engagement, survey work, performance measures, scenario/model integration, investment and project-scoring work, fiscal constraint, policy and implementation recommendations, public review, and editable final handoff.

Those requirements create a real owner-review problem: a persuasive narrative is useless without a supported lead entity, UEI, named and available staff, relevant projects and references, committed specialists, federal-certification posture, insurance posture, source/addenda review, and task-level price reconciliation. This compiler keeps those distinctions visible without turning caller assertions into buyer-facing authority.

## Trust model

- `compile` and `verify` are the **current** public CLI path. Current compilation owns process UTC; caller-supplied `as_of` cannot backdate current readiness.
- Current receipts are short-lived and `verify` rechecks current gate dispositions before accepting them.
- Library `compile_packet` / `verify_packet` preserve explicit-time deterministic replay only and label receipts `HISTORICAL_INTEGRITY_ONLY`.
- Candidate evidence remains `CANDIDATE_ASSERTIONS_ONLY`; an owner or separate trusted evidence system must authenticate facts outside this package.
- `submission_ready` is always `false`. This owner-review carrier does not authenticate sign, price, send, contract, or spend authority.
- Input reads bind retained-file generation metadata and visible-path identity; strict JSON rejects duplicate keys and non-finite numbers.

## Files

- `captures/20261003/input.owner-review.json` - the dated retained-source input; acknowledgment, qualification and commercial evidence remain unresolved.
- `input.owner-review.json` - truthful September initial state; preserved.
- `source_requirements.json` - original page-referenced source catalog; its historical hash field is unchanged. The new capture manifest binds the retrieved RFP generation separately.
- `questions.json` - owner-review question queue for the published question deadline; no send authority.
- `response_architecture.md` - 16-page allocation, delivery architecture, team shape, and commercial work breakdown.
- `schema.py` - strict validation with exact keys and bounded values.
- `engine.py` - historical/current compiler and verifier surfaces.
- `cli.py` - process-current compile/verify, strict bounded no-follow reads, and create-exclusive dirfd-relative output writes.

## Run

From repository root:

```bash
python -B -m opportunities.impo_mtp_2055.cli compile \
  opportunities/impo_mtp_2055/captures/20261003/input.owner-review.json \
  --output-dir /tmp/impo-mtp2055-packet

python -B -m opportunities.impo_mtp_2055.cli verify \
  opportunities/impo_mtp_2055/captures/20261003/input.owner-review.json \
  /tmp/impo-mtp2055-packet/receipt.json \
  /tmp/impo-mtp2055-packet/packet.md
```

`--require-submission-ready` deliberately returns exit code 3 for this package because owner-review analysis cannot authenticate submission authority.

## Status semantics

- `SOURCE_HOLD` - candidate source generation, freshness, addenda, or deadline review is blocked.
- `QUALIFICATION_HOLD` - required organization, team, experience, capability, or document review is blocked.
- `COMMERCIAL_HOLD` - task pricing, budget ceiling, or commercial review is blocked.
- `OWNER_REVIEW_READY` - candidate source, qualification, document, and commercial checks are reviewable; this is **not** buyer-facing or submission authority.

No `SUBMISSION_READY` state is produced by this owner-review-only carrier.

## Source notes

Primary source: IMPO, *Request for Proposals for Professional Services for Metropolitan Transportation Plan (MTP) 2055*, released September 9, 2026. The original September input leaves `source_sha256` empty because exact PDF bytes were unavailable to that build runtime. The October 3 capture supplies the exact retrieved RFP and posted addendum digests in a separate input. The compiler continues to label all input evidence as candidate assertions and does not authenticate external authority. Source capture does not supply a signed acknowledgment, firm qualifications, committed staff or approved pricing.
