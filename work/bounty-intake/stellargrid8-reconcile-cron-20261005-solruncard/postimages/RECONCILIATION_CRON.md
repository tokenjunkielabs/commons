# Match reconciliation cron

Staked matches can outlive both clients. `vercel.json` runs `GET /api/matches/reconcile-all` every five minutes so expired server-side deadlines are recovered without a connected browser.

The sweep selects:

- `active` matches whose `ends_at` is in the past; and
- `awaiting_stakes` matches whose `stake_deadline_at` is in the past.

Each candidate is passed to the existing idempotent `reconcileMatch(matchId)` path. Timed-out active matches therefore settle through the normal settlement authority, while incomplete stake windows refund through the existing timeout path. Candidates are processed sequentially to avoid a burst of escrow and Supabase operations when many matches expire together.

## Deployment

Configure a server-only Vercel environment variable named `CRON_SECRET` with a long random value. Vercel includes it on cron requests as `Authorization: Bearer <CRON_SECRET>`. The route returns an error when the secret is missing and rejects requests whose bearer value does not match.

The five-minute schedule keeps recovery bounded without turning settlement into a high-frequency poller. If the deployment plan uses a different cron-frequency limit, adjust only the `schedule` value in `vercel.json`; the endpoint itself is idempotent across repeated invocations.
