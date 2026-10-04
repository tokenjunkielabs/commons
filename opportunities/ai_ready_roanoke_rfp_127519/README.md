# AI Ready Roanoke RFP-127519 pursuit carrier

A retained partner-first response-production package for Botetourt County Economic Development Authority RFP-127519. As of October 4, 2026, the package's last retained proposal deadline has passed. This carrier is held for retrospective source reconciliation; it is not a live invitation to prepare, contact or submit.

See [the dated source disposition](SOURCE_DISPOSITION_20261004.md) for the unread later-addenda leads, measured official-access limit and preserved owner/contact boundaries.

## Current posture and retained history

- Commercial posture: `PARTNER_FIRST_PRIME_HOLD` for TJLabs.
- Last retained proposal deadline: **2026-10-02 23:59 ET**, per the September 13 Addendum 1 mirror record; **passed**. A current official source generation has not been recovered.
- Buyer fixed-price ceiling: **$250,000**.
- First prime hypothesis: Camoin Associates.
- Historical Camoin outreach: **SENT_NOT_ACCEPTED**, Gmail receipt `1a09b2684d2a2040`; no fresh mailbox result is claimed. Preserve the existing no-repeat boundary and the separate TEConomy HARD_DNR.
- Buyer submission: **NOT_SUBMITTED**.
- Award/payment/revenue: **NONE CLAIMED**.

## Why fail closed

The RFP/addendum content is publicly readable through a document mirror, but this carrier has not independently retained exact buyer-hosted PDF bytes. That supports internal historical research; it creates no current outreach authority and is **not enough** for `READY_FOR_OWNER_SUBMISSION_REVIEW`. The engine requires exact official bytes + current addenda, evidence-backed qualification gates, valid budget, and owner release before it can produce a submission-review state.

`SENT_NOT_ACCEPTED` is only provider transport truth. It cannot confirm a partner, workshare, bid, customer acceptance, award, payment or revenue.

## Run

```bash
python -m unittest opportunities.ai_ready_roanoke_rfp_127519.test_engine
python -O -m unittest opportunities.ai_ready_roanoke_rfp_127519.test_engine
python -m opportunities.ai_ready_roanoke_rfp_127519.acceptance
```

## Components

- `engine.py` — source/addenda, qualification, deadline, partner/outreach and submission-preflight state machine.
- `budget.py` — exact-cent buyer-ceiling and milestone arithmetic; never invents rates or approval.
- `source_manifest.json` — retained September 13 source transport/authority record; later addenda are not incorporated.
- `current_evidence.json` — retained prime hypothesis/outreach record and nonclaims; no new partner response is inferred.
- `partner_brief.md` — commercial workshare hypothesis and counterpart questions.
- `response_architecture.md` — buyer-weighted proposal production outline.
- `acceptance.py` / `test_engine.py` — mixed real-state acceptance + hostile coverage.

## Authority ceiling

This package does not submit, sign, price, certify, contact the buyer, accept a contract, spend, claim an award, receive money or recognize revenue. Any external action needs separate authority/evidence. The strongest output means only **owner submission review readiness**.
