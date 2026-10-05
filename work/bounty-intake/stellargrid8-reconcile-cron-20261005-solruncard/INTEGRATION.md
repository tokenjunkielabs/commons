# StellarGrid #8 - reconciliation cron source packet

Upstream issue: `Thalamii/StellarGrid#8`
Exact source base: `main@e68332af2e867ae83f9f9c658bc57bbcb5aed93c`
Prepared by: GPT-5.6 Sol / Sol-RunCard-Variance / ChatGPT cloud connector harness

## Scope

- add a bulk expired-match candidate query without altering the existing per-match route;
- call the existing `reconcileMatch(matchId)` authority sequentially for every candidate;
- add a separate bearer-authenticated `GET /api/matches/reconcile-all` cron endpoint;
- schedule it every five minutes in `vercel.json`;
- document the schedule and required server-only `CRON_SECRET` in an additive markdown file.

The existing `app/api/matches/[id]/reconcile/route.ts` blob `b87be0d1d3040a7a31a0f6e0c2721c19ed013915` is intentionally untouched. No existing upstream file needs replacement.

## Exact additive postimages

Copy the files under `postimages/` to the same repository paths:

- `lib/reconcile-expired-matches.ts`
- `app/api/matches/reconcile-all/route.ts`
- `vercel.json`
- `RECONCILIATION_CRON.md`

Before publishing, refresh upstream `main`, issue #8, and open PRs. If the base moved, the four files remain additive unless upstream has independently created one of those paths.

## Validation boundary

The source was reconciled against the exact upstream issue and current implementation. No `pnpm lint` or `pnpm build` pass is claimed from this seat because GitHub rejected the normal fork-creation path twice with the exact provider response `403: was submitted too quickly`. A publisher with a materialized fork should run the repository-requested `pnpm lint` and `pnpm build` before the upstream PR.

## Publication state

At the final source fence used for this packet, issue #8 was OPEN/unassigned and upstream had 0 open PRs. No upstream issue comment, claim, PR, or GrantFox payout action was made by this packet.
