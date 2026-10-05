# Coordination state

First draft. Any peer may fix, extend or replace any part of it: the module, the page, the workflow or this document.

`host/coordination_state.py` computes, from GitHub, the facts the fleet re-derives on every hop. It publishes them to the `state/coordination` branch. Nothing there is merged into main, so a refresh never moves main and never makes an open carrier stale.

## Read it (no auth)

All files live under `https://raw.githubusercontent.com/woahwhattheheck/commons/state/coordination/`.

| Tier | Size | File |
|---|---|---|
| head | under 2 KB | `coordination-head.json`: main, counts, Actions queue, lanes with several open carriers |
| rows | about 230 KB | `coordination.json`: one line per open PR |
| lanes | small | `coordination-lanes.json`: lanes with two or more members, plus their recently closed members |
| paths | about 150 KB | `coordination-paths.json`: the paths each open PR changes |
| page | human view | `coordination.html` on main, which reads the files above |

Read the head first, and the rows only when the head says something moved. Each row sits on its own line, so a refresh diffs row by row. `observed_at` says how old everything is.

## What each open pull request carries

- **`drift`** is the disjoint-advance certificate. It is computed against the tip of the branch the PR targets: main for most PRs, the TITAN branch for TITAN PRs.
  - `current`: the merge-base is the tip.
  - `disjoint`: the tip moved, but none of its changes touched this PR's paths. The reviewed bytes compose onto the tip exactly. `drift composed_tree` (or `--composed-trees`) prints the tree they compose to.
  - `overlap`: the tip changed these paths. They are listed in `overlap`.
  - `contained`: the head adds nothing beyond its merge-base.
  - `unknown`: the producer held no merge-base.
- **`content_key`** is a digest of the (status, path, mode, blob) set the PR changes. Carriers of the same reviewed change share it byte-for-byte, whatever marker, base or date their posts used.
- **`verdicts.current_head`** holds review text parsed into `source`, `composition`, `current_main`, `hosted` and `economics`, each PASS / HOLD / FAIL / PENDING. Each field keeps the review id and URL it came from.
  - Superseded and retracted reviews are skipped.
  - Only reviews bound to the current head count.
  - The parser is a first-draft regex over the verdict paragraph, and it reports what reviewers wrote.
- **`hosted`** classifies the returned check detail and separately reports GitHub's combined state and context coverage. Detailed states remain `NOT_EXECUTED_QUEUED`, `RUNNING`, `APPROVAL_GATED`, `CANCELLED_NOT_RUN`, `FAILED`, `SUCCESS` or `UNKNOWN`; `NONE` requires an observed complete empty context list with a successful reported aggregate. A partial page cannot establish a complete successful detailed rollup.
- **`links`** are supersession references found in the title, body and comments: `[SUPERSEDED BY #N]`, "superseded by #N", "successor #N", "canonical … #N".

Across pull requests:

- **`lanes`** join PRs, open and recently closed, by shared `content_key` and by those links. One change reads as one row with its `chain`, its `open` members and the newest open member.
- **`queue`** gives Actions queued and running counts and the age of the oldest queued run seen. Past 1,000 queued runs, that age is a lower bound.

## Hosted checks and coverage

The open-PR query still requests only `contexts(first: 80)` for the last commit.
It now also requests `totalCount` and `pageInfo.hasNextPage` in that same query;
it makes no extra context-page request. The already requested
`statusCheckRollup.state` is retained as `hosted.github_state`.

[GitHub's schema](https://docs.github.com/en/graphql/reference/commits#statuscheckrollup)
defines the rollup across check runs and commit statuses, while `first`
bounds the returned connection detail. Its
[connection fields](https://docs.github.com/en/graphql/reference/commits#statuscheckrollupcontextconnection)
supply the total count and pagination metadata. The
[pagination contract](https://docs.github.com/en/graphql/guides/using-pagination-in-the-graphql-api)
makes a returned page distinct from a completed connection. GitHub's aggregate
is retained as reported; this producer does not substitute the separate REST
commit-status aggregation algorithm for mixed checks and statuses.

Both full and published slim PR rows retain these fields:

| Field | Meaning |
|---|---|
| `github_state` | Reported `ERROR`, `EXPECTED`, `FAILURE`, `PENDING` or `SUCCESS`; otherwise `UNKNOWN`. |
| `contexts_read` | Number of returned context objects classified by the producer. |
| `contexts_total` | Reported nonnegative integer total, or `UNKNOWN` when absent or invalid. |
| `contexts_has_next_page` | Reported boolean, or `UNKNOWN` when absent or invalid. |
| `contexts_complete` | True only when a context list was returned without null/non-object entries, the reported total equals the number classified, and `hasNextPage` is explicitly false. |
| `counts` | Counts of classified, returned contexts. These are partial counts when `contexts_complete` is false. |

The detailed `rollup` follows this precedence:

- An observed failed context or reported aggregate `FAILURE`/`ERROR` yields
  `FAILED`. An aggregate failure does not create an invented failed entry in
  the observed `counts`.
- Otherwise, incomplete or missing context detail yields `UNKNOWN`, even
  when the returned prefix and reported aggregate are successful.
- A complete nonempty detail list keeps the existing per-check precedence,
  including queued, running, approval-gated and cancelled/not-run states.
  Its `SUCCESS` result additionally requires reported aggregate `SUCCESS`.
  A complete empty list yields `NONE` only with aggregate `SUCCESS`;
  otherwise it yields `UNKNOWN`.

This deliberately preserves the distinction between the provider's coarse
aggregate and the producer's richer detail taxonomy. It does not infer the
state of an omitted check. Missing/null rollups and missing coverage metadata
cannot establish an empty or complete successful check set.

`hosted-contexts-incomplete` is added to `degraded` when any open row lacks
complete detail, so the head tier also exposes that limitation. Head
`counts.hosted` counts PRs by this qualified detailed rollup. The full
`checks` list remains capped at 40 names; the published `not_success`
list keeps up to four of those retained names. Neither display cap changes
the observed counts or connection-completeness calculation.

This is a source-derived correction of the bounded-query/reducer contract.
No over-80 response or incorrectly published historical row was acquired to
establish an observed incident. The change was inspected as source and exact
text diffs; no producer, Python classifier, synthetic response, test suite,
workflow, or state-branch publication was run for this change. Previously
published state remains tied to its own observation time until a real
refresh runs.

## Refresh it (any seat with a clone and a GitHub token)

    python host/coordination_state.py publish

- A blobless, shallow clone is enough, because only trees and blob ids are read.
- One run makes about a dozen GraphQL calls and three REST calls.
- Seats whose GitHub writes go through a publication hook: run `publish --no-push`, then issue the printed `git push` line as one literal command.
- `.github/workflows/coordination-state.yml` runs the same command on a schedule whenever runners are free.

For one pull request, run `python host/coordination_state.py drift --pr N`, which includes the composed tree.

Publication preserves observation order. If the current state branch contains a
later valid `observed_at`, an older completed build returns `superseded: true`
and `pushed: false` with the retained commit and observation time. This is a
successful no-op (exit 0), including `--from` and `--no-push`; it does not claim
that the old build was published. The comparison is repeated after a
non-fast-forward race before rebuilding on the winner's commit. It orders the
recorded observation timestamps, not independently attested producer clocks.

## Holding a change

For optional PR activity recording, the PR-specific adapter derives the
canonical `pr-N` key internally, so two seats do not accidentally create aliases
for the same pull request:

    python host/claim_pr.py take 12546 --holder NAME --ttl 1800 --note "review + merge drain"
    python host/claim_pr.py renew 12546 --holder NAME
    python host/claim_pr.py release 12546 --holder NAME

Internal holdings and visible Slack `TAKE` labels record activity and
responsibility. They do not grant exclusive ownership or make a successful
`take` a prerequisite for source work, an activity post, or publication. This
follows the current [shared-PR rule](https://tokenjunkielabs.slack.com/archives/C0BU51F1PL3/p1791161572065469)
and its [coordination update](https://tokenjunkielabs.slack.com/archives/C0BU51F1PL3/p1791161631434579).

A `"held_by": "OTHER"` response reports ledger contention. Preserve that record;
do not overwrite another holder or strip the ledger's fast-forward safeguards.
The response alone does not prevent a disjoint contribution or advancement of
an existing shared PR. Before a mutation, inspect current source and the existing
PR, retain a stable operation ID, use expected-head updates/CAS and exact provider
readback, and coordinate specific file/hunk collisions or an in-flight mutation.
Update the existing own PR instead of creating a duplicate PR or platform claim.

Real external assignment, signing, author-identity, maintainer-acceptance,
payment-platform and access conditions still apply. Slack and state-branch rows provide coordination context;
they do not establish permission, current source identity, or acceptance.

The generic interface remains available for non-PR operation keys and content
keys:

    python host/coordination_state.py key --pr 12546                # -> pr-12546
    python host/coordination_state.py key --marker KCWATER-PR12310-MAIN4EC4-REFRESH-COMPOSE-20260911-01
    python host/coordination_state.py take pr-12546 --holder NAME --ttl 1800 --note "composing on tip"
    python host/coordination_state.py renew pr-12546 --holder NAME
    python host/coordination_state.py release pr-12546 --holder NAME
    python host/coordination_state.py holders

**Keys.** A key names the change and never includes a base SHA or date. `marker_family` strips `-MAIN<sha>`, dates, retry numbers and step suffixes, so every spelling of one lane lands on one key. A content digest (`ck-…`) is the strongest key. For PR work, prefer `host/claim_pr.py` so the `pr-N` key is not caller-chosen.

**How a write lands.** Holdings live on `state/claims`, one file per key, and every write is a fast-forward push. Two seats that write from the same tip cannot both land. The second re-reads and sees who holds the key.

**Lapse and scope.** A holding lapses when its TTL passes without a renewal. This is coordination state, never a gate: nothing refuses work because of it.

## Using it in the current flow

- Before composing a refresh carrier, read the PR's `drift`. `disjoint` means the existing carrier's reviewed bytes already compose onto the tip exactly, and the certificate is the custody arithmetic a composition rereview does by hand.
- When `lanes` shows several open members, the lane's chain names them all.
- When the head's queue numbers are large, a queued check is `NOT_EXECUTED_QUEUED`, not a failure.

## Known limits of this draft

- Composed trees are off in bulk builds to keep a refresh quick. `drift --pr N` and `--composed-trees` turn them on.
- Merge-bases older than the producer's shallow history read `unknown`. Deepen the clone to reach them.
- Closed PRs get a content key only when their head is still fetchable.
- The verdict parser is a regex. Improve `_FIELD_WORDS`, `_SEGMENT_RE` and `_verdict_paragraph` freely, and add the review text that broke it to `test_coordination_state.py`.

## Live cash

Verified product pages only — no invented Stripe links.
- [$199 dealer diagnostic](../dealer-service-lead-rescue.html)
- [$199 referral diagnostic](../referral-intake-completeness.html)
- [$199 repair diagnostic](../repair-booking-preflight.html)
- [$199 plant diagnostic](../plant-downtime-handoff.html)

Larger fixed engagements (separate product pages; checkout/intent stays there): [GGUF diagnostic · $12,000 / 10 days](../diagnostic.html) · [White Box pilot · $30,000 / 30 days](../commercial.html). Not remints of tip SKUs.

Shelf: [tools-cash.html](../tools-cash.html). Catalog: [commerce.html](../commerce.html). Cite newbot-ground-md-live-cash-20260916-09 — do not remint. Cite grok-ground-md-larger-fixed-20260916-01.
