# Sustainable service dependence

Owner instruction, 2026-10-06: make sure the fleet does not depend on services
that are only free trials, require payment to continue or shut off when their
usage credits run out. Prefer sustainable free capacity such as the actual
free products offered by Google, GitHub and other providers.

The owner's same-day correction explicitly excludes JEV. Keep JEV's existing
routing and ordinary usage unchanged; do not include it in trial-removal work.

## Routing and continuity

- Use existing infrastructure or an individually verified renewable free
  allowance. A provider's name, API key, successful login, remaining balance
  or successful one-off call does not establish a sustainable free plan.
- Do not make a free trial, one-time promotion, conditional zero price or
  metered wallet the only route for a critical fleet workflow. Do not turn
  trial expiry into a purchase, top-up, automatic reload or account rotation.
- Before routing recurring work onto a free allowance, record the exact
  account, product and method, its reset period, quota, expiry if any, and
  whether exhaustion stops free work or bills paid overage. Unknown plan
  terms stay unknown. Bound work to the free allowance and retain an existing
  sustainable alternative when a quota is exhausted.
- Keep source, configuration, durable state and valuable outputs recoverable
  independently of the temporary host. Export provider-only volumes and data
  before a cutover; preserve original jobs and operation IDs. Confirm the
  replacement handles the actual workflow before moving its default route.
- Keep already-available tools and direct shared credential access intact.
  This instruction changes dependency selection, not peer access. Optional
  experiments cannot become an unverified automatic fallback.

## Existing automatic fallback selector

`integrations/shared_equipment/services.py` exposes
`plan_capability_fallback`. Its free capacity decision must not select
`one_time_free` or `conditional_free` providers as READY. Renewable
`recurring_free` and `free_tier` observations also need the existing
`zero_net_spend_verified` fact. Verification belongs to the actual observed
method: rebinding a free Search/Fetch route to a metered Browser/Agent method
must not carry those free-method facts forward.

The selector remains a plan, not a provisioner or a caller. A landed source
change does not establish that a running gateway has adopted it. Read back
the replacement provider outcome and runtime route in the original work item.

## Current migration work

Railway is the identified expiring-host priority. The existing provider-runtime
activation work owns its TITAN services and TraceForge deployment; preserve
that work and its retained outputs during migration. TraceForge's authoritative
standard-library Python source is already retained in
`woahwhattheheck/public-commons-sprint-2026/traceforge-ai`; its Python analyze
and verify endpoints require a Python runtime. Copying its UI to static hosting
alone is not a working backend replacement. The public LDA transport is a
separate consumer and its existing owner stop on phone/router/reachability
checks remains in force.

TinyFish's metered browser/automation route is not a dependable free fallback.
Its separately observed Search/Fetch contract applies only to those methods.
Firecrawl's credit period still needs classification as a renewable allowance
or promotional grant before recurring dependency selection. Account-ready or
unprovisioned services are not evidence of production dependence.

This is an identified migration list, not a completed account/billing census or
a claim that Railway has been replaced. Continue through the existing resource
inventory and provider-runtime work item; keep unresolved live-host state visible.
