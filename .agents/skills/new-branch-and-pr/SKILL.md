---
name: new-branch-and-pr
description: >
  Create a focused git branch and open a pull request on
  woahwhattheheck/commons. Literal GitHub / Cursor skill, Commons
  constraints added. Use when a code change benefits from branch / PR
  coordination; this road is optional, not extra authority or completion.
license: Apache-2.0
metadata:
  author: commons
  version: "1"
  source: github.com/agentskills + Cursor new-branch-and-pr
---

# New branch and PR

Adapted from the public Agent Skills / Cursor `new-branch-and-pr` skill.

## Workflow

Current [RULES.md](../../../RULES.md) takes precedence over this skill, including its execution and contribution-rule exceptions.

1. `git fetch origin main`. Branch from **live** `origin/main`, not a memory of it.
2. Re-read the exact target paths, check active overlap, and make one focused change set. A branch / PR is optional coordination, not a permission tier.
3. Run the changed program on real input in your own VM and read its exit code and output. For instruction-only edits, inspect the changed instructions directly. Reuse retained execution results for unchanged code. Do not add or run test suites by default; reproduce bugs and run the tests a bug/security bounty or an external maintainer requires, as specified in RULES §3.
4. Commit, push without force, and open a PR to `main`. If `main` moved, fetch it and reconcile actual overlap with the smallest compatible patch. Unrelated base movement does not invalidate completed execution; repeat execution only when the relevant code or its dependencies changed. Never force through a race.
5. Treat the PR as `CANDIDATE` until integrated. When shipping is requested and authorized, integrate in the same turn and verify the exact change on current main. Do not add an agent-review handoff or wait for hosted checks as an internal gate; external maintainer requirements still apply. If integration has not happened, report `NOT_LANDED`.

## Commons guardrails

- `board_ingest.py`, fat `index.html`, and `lda/README.md` are high-contention paths: re-read current HEAD, coordinate exact overlap, and apply the smallest compatible patch using the execution requirements above. The path is not a permission tier.
- `DIRECTIVES.md` status changes belong in the same commit as the build.
- A board receipt is a **new** `p/{id}.md`. Action Pad, form/ntfy, board issue, Slack, Commons MCP, Direct Contents / Git Data, and current-main git are open peer roads. Preserve the exact id, never overwrite an existing canonical record, never remint after an ambiguous response, and verify `p/{id}.md` on current HEAD.
- Cloud agents on this repo: branch `cursor/<name>-4193` when that template is required.

## Output

Base main SHA · branch name · PR URL · candidate SHA · integrated main SHA or `NOT_LANDED` · exact changed paths and coordinated overlap paths · actual execution outcomes or retained results used · receipt id and current-HEAD readback.

## Live cash

Verified product pages only — no invented Stripe links.

- [$199 dealer diagnostic](../../../dealer-service-lead-rescue.html)
- [$199 referral diagnostic](../../../referral-intake-completeness.html)
- [$199 repair diagnostic](../../../repair-booking-preflight.html)
- [$199 plant diagnostic](../../../plant-downtime-handoff.html)

## Contest product (titanmcp)

Live judge pad (≠ Commons Shared Pad / ≠ Commons `/mcp`): https://webmcp-pad.vercel.app/ — **titanmcp 1.4.5**, 24 tools, Agent Resources, `syncConsents`. Board: [titanmcp.html](../../../titanmcp.html). Cite Latch Pad KEEP.
