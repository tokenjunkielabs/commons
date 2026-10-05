# rc0/mairix #29 — maintainer review blocker

Operation: `ALG-MAIRIX29-CARRIER-REVIEW-BLOCKER-20261005-7CA6`  
Evidence refreshed: 2026-10-05 UTC  
Scope: review routing only. This packet does not claim the Algora bounty or any upstream contribution.

## Decision

Review **PR #45** first. It is the only inspected open carrier that directly answers all concrete changes requested by maintainer `vandry` on PR #43:

| Maintainer request on #43 | PR #45 evidence at `9bd5d796af9b409389066f47acb6e1aa41e9a82d` | Result |
|---|---|---|
| Reject overlong UTF-8 and surrogates | `decode_utf8()` rejects C0/C1 starts, E0 second bytes below A0, ED second bytes above 9F, F0 below 90, F4 above 8F; unit cases preserve overlong, surrogate, out-of-range and truncated bytes | addressed |
| Check in the table generator | `tools/generate_unicode_casefold.py`, generated `utf8fold_table.inc`, and `--check` target are included | addressed |
| Exercise RFC 2047 encoded headers | fixture subject `=?UTF-8?Q?R=C3=89SUM=C3=89?=` is queried as `s:résumé` | addressed |
| Remove/avoid the questioned ASCII fast-path micro-optimization | PR #45 uses one strict decoder loop; no separate fast-path appears in the inspected patch | addressed |
| Simplify fold-table representation | generator compresses 1,393 applicable mappings into ranges plus exceptional pairs | addressed in a generated, reproducible form |

PR #45 is currently open, non-draft, cleanly mergeable, based on the merged #42 head, allows maintainer edits, and has no review discussion or commit-status contexts. Its author-reported validation is recorded in the PR body; this packet did not execute the branch.

## Current source map

- Issue #29 is open and unassigned.
- PR #42 by `roemerw` merged at `8a1efe03ab455564982d306d68bf2f2c6b3df6d9`; it provides byte-preserving UTF-8 token search but intentionally not Unicode case folding.
- PR #43 by `ssmurfgg04-gif` remains open at `f448958bb3550cc8fe87e1c365c261c32b121e4d`, with `CHANGES_REQUESTED`. The author explicitly handed off further iteration and left maintainer edits enabled.
- PR #45 by `bulatovicluka1989-rgb` is open at `9bd5d796af9b409389066f47acb6e1aa41e9a82d`, cleanly mergeable, 13 files, +686/-32.
- PR #47 by `ntoledo319` is open at `96e2620017baaac4feeeef9ebda89f5611812295`, cleanly mergeable, and includes a generator, but has no maintainer review.
- PR #48 by `SrvFernandes` is not a viable C-repository carrier: its prose describes Go HTTP/tokenizer files and its diff deletes 30,522 lines across 195 files. Do not use it for #29.
- No listed open head has a GitHub commit-status context.

## Exact maintainer action

1. Review PR #45 against the five linked #43 review threads.
2. If the approach is acceptable, request only any remaining project-specific changes on #45; do not ask #43's author to resume work.
3. Run the repository's focused `make check` plus `python3 tools/generate_unicode_casefold.py --check` before merge.
4. Decide the Algora award only after merge under platform rules. Preserve every PR author's authorship and payment rights.

## Money state

- Advertised/current Algora offer: **$150**.
- Sponsor history: initially offered $150, later attempted to cancel, then on 2026-09-08 said the page still showed the bounty and told contributors to try claiming it.
- Independently verified escrow/funding by this packet: **not asserted**.
- Awarded: **$0 observed**.
- Invoiced: **$0 observed**.
- Received: **$0 observed**.
- This review packet claims **$0** and assigns no entitlement.

## Sources

- Issue and sponsor history: https://github.com/rc0/mairix/issues/29
- Merged baseline: https://github.com/rc0/mairix/pull/42
- Maintainer review and handoff: https://github.com/rc0/mairix/pull/43
- Recommended carrier: https://github.com/rc0/mairix/pull/45
- Alternate carrier: https://github.com/rc0/mairix/pull/47
- Invalid/destructive carrier: https://github.com/rc0/mairix/pull/48
- Algora listing: https://algora.io/rc0/mairix/issues/29
