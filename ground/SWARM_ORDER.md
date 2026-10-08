# Commons swarm order — owner directive, 2026-09-12

GPTs are the principal builders and leads. Every seat uses the existing command
center and claims. There is no agent peer review: agents don't review, approve
or gate each other's work, and nobody waits on a review before merging
(owner, 2026-09-22). This replaces the 2026-09-12 GPT-pass requirement. It
doesn't change shared tool access, credentials or public read access.

## Owner-controlled communications

All outward communication accounts and channels belong to Bryce. Do not publish
an assistant/model identity, title prefix, signature, bot heading, or generated
provider footer. The exact standalone terms `Codex`, `Claude`, `Opus`,
`Fable`, `Astra`, `Sol`, and `Grok` are blocked only in explicitly mapped
final outward fields. Private gateway envelopes, operation IDs, source/code,
file contents, paths, fixtures, and provider responses are not recursively
scanned; copying any of them into an outward field makes that field subject to
the check.

A hold is private and non-incident: make zero provider mutations, do not create a
fallback issue/comment/email/chat/ticket/receipt, and return
`matched_fields`, `matched_terms`, and the remove-and-retry instruction to
the invoking agent. Do not start an asynchronous outward operation without a
verified private response channel. A disclosure requirement or injected
provider identity/footer makes that sender route unavailable; do not submit
through Bryce's account.

## Owner blockers go to Bryce's email the day they're found

Owner directive, 2026-09-22. When work stops on something only Bryce can do
(a decision, signature, submission, wallet address, payment, credential or
approval), email Bryce **the same day it's found**. Don't leave it in a PR, a
board card, a `HOLD` state or a digest item and wait for him to read it.

- The subject says what's needed and by when, e.g. `BLOCKER: RFP submit
  decision needed by 2026-09-22 5pm ET`.
- The first line of the body says what he has to do. Keep it short.
- If the item has a deadline, email again at 72 hours, 24 hours and the morning
  of the deadline until he answers.
- If the send fails or the confirmation times out, retry once, then use Slack
  #commons or ntfy. An unsent email is still an open blocker.

Origin: the Invest Appalachia Framer LMS RFP (due 2026-09-22 5pm ET) was held
for owner authority for days and first reached Bryce one hour before the
deadline. It lapsed. Don't repeat that.

## One operation, one working queue

Use `command.html` and `integrations/command_center/`, not a replacement board.
Open PRs are the code queue. `state/coordination` is a derived snapshot;
`state/claims` is the existing atomic claim ledger. PRs, exact artifacts and
provider receipts remain authoritative. Stale snapshots never authorize a merge.

Every active seat, including GPT, starts a work unit by reading the command
center and claiming one stable operation key. Keep the same key through retries,
carrier changes and handoffs. Record the actual seat, model family, current
head/artifact, evidence, next action and heartbeat. Use existing
`command_center_work_item` / `/api/work/item` for observed work and
`host/coordination_state.py take|renew|release` for claims. If the running app is
unreachable, use these repository roads and mark that limitation; do not report
a tool call, dashboard view or deployment that did not happen.

Renew during meaningful progress and before a 30-minute claim expires. Expiry
permits reconciliation, not blindly starting another process. Check the existing
PID/provider task and output first. Retain completed cells, losses, original
archive identities and raw artifacts; a successor resumes only missing work.
An idle seat can keep this ledger current.

## Paid bounty intake and payout follow-through

**Always demand payment for third-party bug work.** Bug discovery, diagnosis, proposed solutions, repair instructions, patches and validation are compensated work. Never offer or deliver them as free labor. Explicitly request payment for each contribution and establish the applicable bounty or agreed compensation route before outward delivery; where no reward is advertised, propose paid terms instead of silently donating the work. Only Bryce's explicit instruction for the specific work can authorize an unpaid exception. Preserve every existing claim while the sponsor decides, and distinguish requested compensation from an award or payment actually received.

**Owner correction — preserve claims (2026-10-06).** Never forfeit, disclaim or waive Bryce's authorship, assignment, bounty, reward or payment claim, or publish “this is not a claim,” “no bounty or assignment claim,” or equivalent surrender language without his explicit instruction for that exact claim. Explicitly claim delivered work and request assignment and applicable payment using the original claimant and verified appropriate payout details. Pending eligibility, award or payment is a pending decision, never a waiver. Correct authorized prior disclaimers while preserving source, attribution and history. Read [RULES.md](../RULES.md#claim-and-payment-preservation--owner-correction-2026-10-06); it supersedes older templates and prompts.

Use the sponsor's current contribution and reward rules before implementation.
In the existing work item, retain the funded issue/listing, claimant, required
application or assignment acknowledgment (or the sponsor's statement that none
is required), and a reference to the configured payout route. Reuse known
account setup; do not collect credentials or private wallet material in the
work item. Account verification, a connected wallet, advertised value and
escrow funding are different facts; none alone is an approved reward.

The builder completes ordinary sponsor intake. If a prerequisite needs only
Bryce, use the owner-blocker email rule above immediately; otherwise resolve it
without a routine owner or peer approval loop. While an item awaits required
sponsor acknowledgment, work on another eligible item rather than accumulating
speculative funded work or stopping the whole queue. Do not invent application
IDs, acknowledgments, assignment, funding or retroactive eligibility.

Carry the same work item through submission, merge, reward adjudication and
payment. Keep those states and their amounts separate: a merged PR is not a
payout approval, and an advertised amount is not money received. Name one
worker and the next concrete payout action. For already-merged work with
unresolved eligibility, reconcile through the existing sponsor case and ask
for its disposition; do not create duplicate PRs, claims or support threads.
This uses the existing queue, not a new gate, receipt system or test framework.

**BountyHub:** The PR author must be the same GitHub identity used for BountyHub login. Publishing a PR does not register a provider claim: open its bounty listing, use **Submit Claim**, attach the PR URL and verify the claim record. After merge, refresh that claim for creator review; record acceptance and actual payout separately. Do not duplicate an existing claim. Source: https://www.bountyhub.dev/en/docs/claim-bounty


**Settlement truth + anti-waiver — owner correction (2026-10-07).** Bryce has confirmed historical bounty/reward payments were received. Never infer global/lifetime `$0` or “no proof of payment” from missing chat/GitHub receipts. Before asserting a lane is unpaid, `received $0`, or that “no payment or award arrived,” inspect the applicable sponsor/platform state and the actual receiving rail (including RTC and Stellar/USDC wallets for those routes, or the applicable PayPal/Stripe/bank/provider rail). If that rail was not checked, say `settlement not verified in this run` or omit the field; unknown is not zero. On live paid/bounty surfaces, never publish waiver-like phrases such as `no payment claim`, `no bounty claim`, `no payment expected`, `no award/payment claimed`, or `no payment or network submission occurs`. When describing a local technical action, use: “This technical step moved no funds; the compensation claim remains active and payment is requested through the existing bounty/reward route.” Repair waiver-like text under the original author/claimant with fresh readback. Canonical rule: [RULES.md](../RULES.md#settlement-truth-and-anti-waiver--owner-correction-2026-10-07).

## No agent peer review

Owner directive, 2026-09-22. Agents don't review, approve or gate each other's
work. There is no GPT pass, review batch, review packet or review verdict
before merge or release, and no hosted-green prerequisite. Build the change,
run it, land it. `host/swarm_review.py` is no longer part of the merge road.

## TITAN continuity

V3.1's submitted archive `5db3921f85efbc7596e5a1e7e198fc5f4644ceea43d8e8323c74ded7b4ba4361`
ran the R04 whole policy. A package that omits its active route is a policy
replacement, even when raw canonical source contains similarly named features.
Never infer submitted behavior from unshipped source or a passive-opponent test.

Use the existing V5 promotion/release transaction, champion ratchet and native
evidence; do not create another release queue. An R04 restoration must contain
the complete closure. A replacement
must explicitly say so and still pass the existing V3.1 champion comparison.
Required members are checked against captured archive bytes before promotion.
Nothing overrides failed economics, missing native evidence or the existing
release-origin interlock.

Current recovery is experimental: #13468 fixes the production-v2 lazy import
failure in production-v3 `20f201161b14af7755146b08207593f9fa5df641d2f31e680792ea62c0e24239`.
The latest one-seed native sample still has an Apex own-score deficit of 237
against exact V3.1. This is not champion clearance. Preserve existing SPARK PID
3264489 and its actual archive/adapter identity until the owner reconciles it.
Future unstarted cells use the corrected candidate; do not restart completed
panels or relabel old results. See the existing selective-carrot/native-9901
artifacts and the owning #sim-data thread TS1789245175.177299.

## Live cash

Verified product pages only — no invented Stripe links.
- [$199 dealer diagnostic](../dealer-service-lead-rescue.html)
- [$199 referral diagnostic](../referral-intake-completeness.html)
- [$199 repair diagnostic](../repair-booking-preflight.html)
- [$199 plant diagnostic](../plant-downtime-handoff.html)

Larger fixed engagements (separate product pages; checkout/intent stays there): [GGUF diagnostic · $12,000 / 10 days](../diagnostic.html) · [White Box pilot · $30,000 / 30 days](../commercial.html). Not remints of tip SKUs.

Shelf: [tools-cash.html](../tools-cash.html). Catalog: [commerce.html](../commerce.html). Cite newbot-ground-md-live-cash-20260916-09 — do not remint. Cite grok-ground-md-larger-fixed-20260916-01.
