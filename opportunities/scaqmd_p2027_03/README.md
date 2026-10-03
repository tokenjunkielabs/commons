# South Coast AQMD P2027-03 pursuit recovery carrier

Operation `SCAQMD-P2027-03-RECOVERY-ZMQV5R9-20260916` recovers the unshipped Sep-14 pursuit while preserving original ZMA-K7Q4 opportunity/source/commercial credit.

The [October 3 capture](captures/20261003/README.md) retains the exact PDF and the official board page that linked it. Its dated source and packet are `RAW_BYTES_BOUND`; the existing CLI completed signing, compilation and verification at 2026-10-03 19:12:43 UTC and returned `HOLD_CONFERENCE_ATTENDANCE`. Conference status remains `NOT_REGISTERED`, projects remain empty, seven team gates remain `UNKNOWN`, and all 13 external-authority flags remain false.

`source.discovery.json`, `example.discovery.json` and `observations.json` preserve the September 16 history, when PDF downloading failed and `RAW_BYTES_UNBOUND` / `HOLD_SOURCE_BYTES_REQUIRED` were truthful. Use the dated October 3 input for the recovered generation. Its [source review](captures/20261003/source_review.json) maps the reread observations and corrects the past-project locator to Attachment D II.C.1; it does not claim a full new contract review or continuing source completeness.

## State ordering

1. `HOLD_SOURCE_BYTES_REQUIRED`
2. `HOLD_DEADLINE_PASSED`
3. `HOLD_CONFERENCE_ATTENDANCE`
4. `HOLD_PAST_PROJECT_QUALIFICATION`
5. `HOLD_CAPABILITY_PLAN`
6. `HOLD_TEAM_QUALIFICATION`
7. `READY_FOR_OWNER_PROPOSAL_REVIEW`

Even the strongest state is owner proposal review, never autonomous submission authority.

## Source boundary

`build_source_authority()` HMAC-binds the retained source record using a key unavailable in the packet. This protects the local retained-generation relationship; it does **not** prove buyer authenticity by cryptography. Buyer authenticity still depends on recovering the official source from the official AQMD route. Candidate packets cannot invent a different URL, page count, digest or raw status and still verify.

## Qualification boundary

The compiler requires at least three distinct comparable projects in the five-year window. Across those projects it requires evidence of a public/regulatory engagement, a >=$100,000 or >=12-month engagement, named core technology, client-verifiable references, and a documented challenge/corrective example. It separately requires mandatory conference attendance evidence and seven prime/team gates. `UNKNOWN` never becomes `PROVEN`.

## CLI

```bash
export SCAQMD_SOURCE_AUTHORITY_KEY_HEX='<64+ private hex chars>'
python -m opportunities.scaqmd_p2027_03.cli sign-source opportunities/scaqmd_p2027_03/captures/20261003/source.json scaqmd-source-authority.json --key-id owner-2026-10
python -m opportunities.scaqmd_p2027_03.cli compile opportunities/scaqmd_p2027_03/captures/20261003/packet.json scaqmd-source-authority.json scaqmd-assessment.json --key-id owner-2026-10
python -m opportunities.scaqmd_p2027_03.cli verify opportunities/scaqmd_p2027_03/captures/20261003/packet.json scaqmd-source-authority.json scaqmd-assessment.json --key-id owner-2026-10
```

Run from the repository root after checking the official source for later updates. Outputs are exclusive-create files. JSON parsing rejects duplicate keys and non-finite constants. Use the default process clock for a new assessment; `verify` reproduces a stored assessment's time and is not a live source refresh.

The captured CLI run used a private invocation-only acquisition key. Its retained MAC records local source-generation integrity; it is not an owner-held production trust root or an endorsement. That key was never published or written and cannot be reused. The commands above create a separate binding using the operator's private key.

## External authority

The compiler always returns `false` for conference registration, buyer contact, question/proposal submission, signature, certifications, preference claims, price/contract commitment, production access and award/payment/revenue claims.

The prior Sep-14 Varsun Muse clearance is explicitly dead. A later Muse production-correction message identified that exact decision as unsafe because `DO NOT SEND YET` had been converted to `Cleared ... Go`. Any future prime outreach must start with a fresh cross-provider dedupe and a new exact Muse election.
