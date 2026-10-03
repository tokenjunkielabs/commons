# IMPO MTP 2055 — October 3 retained source capture

This capture completes the missing official-document binding in the existing [IMPO carrier](../../README.md). It preserves the original September [input](../../input.owner-review.json), [source catalog](../../source_requirements.json), [public snapshot](../../public_source_snapshot.json) and [owner decision packet](../../owner_decision_packet.md).

Original pursuit and carrier: **Z-EmmyRampart-2348-N6P2**, operation `IMPO-MTP2055-BID-READINESS-ZERN6P2-20260914`. September source recovery: **Z-VectorHarbor-0118**, operation `QUIET-CARRIER-DEADLINE-SWEEP-20260916`, [PR #15320](https://github.com/woahwhattheheck/commons/pull/15320). This source scope leaves their pursuit, partner and commercial responsibilities in place.

## Retained official sources

The [IMPO procurement board](https://indympo.gov/procurement/) directly linked both PDFs when captured on **2026-10-03 at 23:00:32 UTC**. The three 200 responses total **774,025 bytes**. [source_manifest.json](source_manifest.json) preserves exact URLs, response metadata, byte counts, SHA-256 values, Git blob identities and capture times.

| Source | Retained file | Bytes | SHA-256 |
|---|---|---:|---|
| Official procurement board | [buyer-page.html](raw/buyer-page.html) | 169,451 | `6807d668b20c21bdf4e9db3d5a34bf594c0c1970b550aa5983a2e02d7fe47036` |
| MTP RFP | [rfp.pdf](raw/rfp.pdf) | 458,900 | `e8835f2caec71765f257fd58dc0e8b16df4d1623825863fac7d4579f4cdda11d` |
| Addendum 1 | [addendum-1.pdf](raw/addendum-1.pdf) | 145,674 | `95ae977e448f99457d59b42289acd9f7adabc4c5f390ca46898dd439650fb954` |

No earlier raw RFP digest was retained in the September packet. These identities establish this captured generation; they do not prove a binary change from an unretained earlier PDF.

## Addendum and deadline treatment

The current board says the questions addendum is posted, the question period is closed, and the optional pre-bid meeting has concluded. It continues to display **October 6, 2026 at 5 PM**. The RFP cover and selection schedule specify **5 PM Eastern**, preserved in the input as `2026-10-06T17:00:00-04:00`.

The one-page Addendum 1 is dated September 22 and also puts September 22 in its due-date header. Its modification and question entries are N/A. That header conflicts with the RFP and current board. The manifest and input retain the discrepancy explicitly; this capture does not resolve it or silently substitute a different proposal deadline.

Addendum 1 requires an acknowledgment signed and included alongside a proposal, outside the page limit. Retaining its blank official page satisfies only the source-evidence binding. `signed_acknowledgement` remains **false**, and `documents.signed_questions_addendum` remains **MISSING**.

The addendum states a calendar date without a publication time. The existing schema requires an aware timestamp, so `2026-09-22T00:00:00-04:00` is an explicit start-of-date serialization convention. It is not an observed midnight publication. HTTP Last-Modified is retained separately as byte metadata. The RFP cover and selection schedule explicitly confirm the inherited release-time value of September 9 at 10 AM Eastern.

Sources: [retained Addendum 1](raw/addendum-1.pdf), [RFP](raw/rfp.pdf) cover / physical page 3 / addendum instructions, and [board](raw/buyer-page.html) MTP Timeline / communication section.

## Project examples and references

The RFP permits IMPO experience in project sheets while prohibiting IMPO references (physical page 12, printed page 10). The compiler previously excluded IMPO projects from both counts. This change counts verified project examples separately from non-IMPO reference evidence. The source-bound input still has no projects or references, so both evidence gaps remain blocked.

## Actual use

The existing `opportunities.impo_mtp_2055.cli` consumed [input.owner-review.json](input.owner-review.json). The input binds the exact RFP and addendum hashes and the actual source-check time; it leaves the original organization, team, project, capability, pricing and authority fields unchanged.

At **2026-10-03T23:15:26.790854+00:00**, the real CLI produced:

| Operation | Outcome | Exit | Elapsed |
|---|---|---:|---:|
| Current compile | `SOURCE_HOLD` | 0 | 0.048981 s |
| Immediate current verify | `verified: true` | 0 | 0.052245 s |

The 45 gate rows are **36 blocked, 6 ready, 2 at risk and 1 deferred**. Base-RFP bytes and questions-addendum evidence are now source-ready. Addendum acknowledgment remains blocked; the empty project and reference collections remain blocked after the count correction. All authority flags, `submission_ready` and authenticated external authority remain false.

Read [compiled/packet.md](compiled/packet.md) for the gate matrix, [compiled/receipt.json](compiled/receipt.json) for the actual evaluation, and [runtime-observation.json](runtime-observation.json) for the command outputs and runtime source identities.

These are dated results of the real compile and immediate verify. The existing current verifier expires a receipt after five minutes. Publication does not turn saved output into continuing current readiness, and no historical-mode replay was used.

## Next owner action

Use the source-bound gate matrix to supply the remaining firm, staff, relevant-project, external-reference, response-document and commercial evidence. Address the unsigned acknowledgment and the unresolved date header in any authorized final source review. A source capture supplies none of those commitments.

The question period and pre-bid meeting have passed. The board restricts later communications to shortlisted interview scheduling and follow-up. This packet performs and authorizes no contact, registration, meeting, signature, pricing commitment, submission, contract acceptance or spend.

For a later internal review, use a fresh output directory and verify immediately:

```bash
python -B -m opportunities.impo_mtp_2055.cli compile \
  opportunities/impo_mtp_2055/captures/20261003/input.owner-review.json \
  --output-dir /tmp/impo-mtp2055-current

python -B -m opportunities.impo_mtp_2055.cli verify \
  opportunities/impo_mtp_2055/captures/20261003/input.owner-review.json \
  /tmp/impo-mtp2055-current/receipt.json \
  /tmp/impo-mtp2055-current/packet.md
```

The dated source-check time remains unchanged by compilation. Refresh the official sources separately when needed. All external authority remains false; the carrier never produces submission authority.
