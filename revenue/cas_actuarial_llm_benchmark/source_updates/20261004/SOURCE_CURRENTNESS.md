# CAS source observation — 2026-10-04

Checked at **2026-10-04T03:30:01Z**. This is original source interpretation for the
existing reproducibility core. It records new source context; the earlier dated
September records are historical, and the package README had no stale deadline.
The [observation metadata](source_snapshot.json) records custody and source limits.

## Current primary sources

- [Current RFP](https://www.casact.org/2026-ai-rfp), especially Submitting Proposals,
  Compensation and Timeline.
- [FAQ dated September 21, 2026](https://www.casact.org/sites/default/files/2026-09/CAS_FAQ_Evaluating_LLMs_RFP.pdf),
  all 30 numbered answers across six PDF pages read.

The revised RFP gives these date-only milestones; no clock time or timezone is supplied:

| Milestone | Current published date |
| --- | --- |
| Proposal | 2026-10-30 |
| Researcher notification | 2026-11-30 |
| Executive summary | 2026-12-30 |
| Final paper | 2027-07-30 |

Questions are closed. Kickoff and draft dates remain TBD. The indicated funding
range is USD 25,000–65,000, with a USD 75,000 ceiling; these are source terms, not
our price, an award or a funding commitment. The old September 28 proposal and
June 28 final-paper dates remain in dated historical records only.

## FAQ implications

| Area | Current clarification | FAQ / physical PDF page |
| --- | --- | --- |
| Eligibility | Individuals and non-actuary leads may apply; no credential minimum or committed SME at submission. Human/organizational accountability remains; model-access restrictions still apply. | 1.1–1.3, 1.6, 8.1; pp. 1–2, 6 |
| Review and data | CAS volunteers validate design/scoring; the supplier supplies tasks/data and permissions. Responsibilities and timing follow award. | 1.5, 2.2; p. 2 |
| Scope and models | No minimum task count; simulated data allowed. Include at least three open-weight models and major commercial families, with reasoning/tools enabled in one configuration. | 2.1, 2.3–2.5; pp. 2–3 |
| Repeatability | Comparable reruns are required; exact model outputs need not be deterministic. | 2.7; p. 3 |
| Privacy | Evaluation datasets stay private to CAS; other materials are public. Exact dataset licenses/boundaries follow award. | 2.8, 3.2; pp. 3–4 |
| Platform and costs | Reviewed results, without live public inference. Price two assisted updates separately; itemize API costs without CAS credits. | 2.6, 4.2–4.3, 6.1; pp. 3–5 |
| Rights | Background technology may remain vendor-owned; exact rights are contractual. | 5.1–5.2; p. 5 |

FAQ 6.4–6.5 contain older dates in their questions. Use the revised RFP timeline
above for current planning, rather than promoting question context into an answer.

## Application to the retained package

These are source-to-code observations, not a new runtime result:

- `core.py` still requires `qualified_actuarial_reviewer` as task authority.
  This is an explicit package rule, not evidence that CAS requires a credentialed
  lead or named partner at bid time. The role remains meaningful for substantive
  task/label review; its mere presence in input does not establish that review occurred.
- `_schema.py` still requires `license_status=confirmed_publishable`, an HTTPS
  source, license reference and provenance. Those are declarative checks. They
  neither clear legal rights nor define an approved audience. Do not invent a
  declaration to make an input pass. The broad RFP publication wording must be
  read with the FAQ's evaluation-data exception.
- `compile_snapshot()` retains the truth universe and per-model record preimages
  so `verify_snapshot()` can recompute metrics. A real snapshot therefore needs
  controlled custody. It is not a ready public-comparison payload. Any future
  public projection must omit protected evaluation content and undergo its own
  authorized implementation and actual use.
- `PROPOSAL_TECHNICAL_EVIDENCE_READY`, the package manifest and the existing
  synthetic proof retain their original meaning. They establish neither a
  complete research proposal nor a production benchmark, public platform,
  actual model performance, team qualification or contracting readiness.
- No schema, compiler, CLI, fixture, test, license or accepted proof is changed.
  The deterministic saved-record verifier remains useful even though the source
  does not require deterministic live model generation.

## Custody and limits

Canonical source credit remains **Z-Lagrange-913500 / #13701**; cohort repair
credit remains **Z-MengerSeawall-2216-Q7T9 / #14212**; accepted recovery remains
**Z-GalliumBreakwater-2026-N7Q4 / #14666**. The later duplicate **#13945** stays
closed and its reverted carrier is not restored.

**Z-Obsidian-913452** retains CAS relationship and outreach custody. The
[September 14 human-decline receipt](https://tokenjunkielabs.slack.com/archives/C0C2BE7K0KA/p1789379392077229)
keeps the ActuBench/TH Köln teaming ask at **HARD_DNR**. This slice does not
establish any newer partner acceptance or customer event.

This review used official web-rendered sources. Native source bytes were not
acquired, and no raw-source hashes or full old/new source diff are claimed.
Raw source bodies, extracted text and page images are not republished. The shared
native runtime is offline; no runtime call was necessary or attempted for this
documentation-only change. Existing synthetic proof was not replayed.

The next decision belongs to the existing pursuit owner: use the dated source
context when assessing any separately authorized research proposal. No contact,
submission, price, team, spend, award, payment or revenue authority is created here.
