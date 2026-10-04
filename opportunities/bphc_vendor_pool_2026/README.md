# BPHC Consultant Qualified Vendor Pool — Qualification Packet

The official BPHC listing is now **Closed**. This packet preserves the original owner’s response structure and qualification gaps. It does not assert eligibility or submit anything.

Original pursuit and accepted package: **Z-Fermion-913606-L5R8 / ZFER-L5R8**, [issue #13764](https://github.com/woahwhattheheck/commons/issues/13764), [PR #13785](https://github.com/woahwhattheheck/commons/pull/13785).

## Current source and execution status

[October 4 source update](source_updates/20261004/SOURCE_CURRENTNESS.md) binds the official listing, RFP and September 15 Q&A. The [dated source snapshot](source_updates/20261004/source_snapshot.json) is a separate generation; the original `source_snapshot.json` remains the truthful September 13 baseline. No historical Q&A bytes are available for a complete version comparison. Local PDF bytes and digests remain absent.

The Q&A resolves track count and Boston-local deadline interpretation. [PR #31041](https://github.com/woahwhattheheck/commons/pull/31041) aligns `preflight.py` with that dated source, including government-initiative experience, while preserving legacy snapshot behavior. Its actual October 4 invocation exited 0 and returned **DEADLINE_PASSED** using the unchanged incomplete owner template. See [execution.json](source_updates/20261004/execution.json) and the [complete output](source_updates/20261004/preflight-result.json). The source-resolved review blockers are gone; the deadline and missing vendor evidence remain.

## Opportunity

BPHC is creating a qualified consultant pool for Communications; Research, Evaluation & Assessment; Strategy & Planning; and Grant Writing. Q&A Q126 (p24) anticipates five years with a discretionary extension. Pool inclusion does not guarantee work. The unchanged source deadline, **Wednesday September 30, 2026 at 5:00 PM EST**, has passed. Q&A Q43 (p27) clarifies Boston local time. The September 30 deadline converts to 21:00 UTC; no date extension or reopened submission window is inferred.

Selected vendors may be considered for future program-specific scopes, budgets and timelines. BPHC requires prior public-health/nonprofit/government experience and two professional references. This repository does not assume those facts are true for us.

## Files

- `source_snapshot.json` — canonical URLs plus extracted source facts; no fake PDF digest.
- `requirements.json` — fail-closed hard gates and preferences.
- `owner_inputs.template.json` — owner-only facts that must be completed outside source control.
- `response_outline.md` — RFP-aligned response skeleton and page limits.
- `evidence_inventory.md` — explicit proof gaps / evidence needs.
- `preflight.py` — deterministic `HOLD` / `READY_FOR_OWNER_SUBMISSION_REVIEW` compiler.
- `test_preflight.py` — hostile and lifecycle coverage.

## Historical gate workflow

The original invocation below is retained as usage documentation. It is not a current readiness result and must not be replayed as proof. Current source interpretation is in the dated update; the completed October 4 preflight use and its passed-deadline result are retained with #31041.


1. Copy `owner_inputs.template.json` outside the repository to an owner-controlled location.
2. Fill it with current, supportable facts. Do not commit private reference contact details, secrets, or unsupported claims.
3. Use a separately dated source generation when terms change, preserving the original snapshot and source-custody limits.
4. Run:

```bash
python3 opportunities/bphc_vendor_pool_2026/preflight.py \
  --source opportunities/bphc_vendor_pool_2026/source_snapshot.json \
  --owner /path/to/private-owner-inputs.json \
  --trusted-now 2026-09-13T10:30:00Z
```

5. A `READY_FOR_OWNER_SUBMISSION_REVIEW` result means only that the deterministic completeness gates passed. Human owner review of qualifications, attachments, pricing, references, legal/compliance obligations, formatting and the final PDF is still required.

## Authority ceiling

The tool never sends email, registers with procurement, contacts references, certifies qualification, certifies SAM/living-wage status, commits pricing, accepts a contract, signs anything, or claims an award/revenue. All output authority flags remain false.

## Source freshness

The source snapshot expires for this gate after seven days. A stale snapshot returns `SOURCE_REFRESH_REQUIRED`. Deadline passage returns `DEADLINE_PASSED`. This is intentionally stricter than trusting a cached opportunity record.
