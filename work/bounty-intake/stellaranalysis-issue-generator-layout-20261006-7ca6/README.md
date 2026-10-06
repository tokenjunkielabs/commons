# Source layout guard for the legacy Stellar issue generator

## Result

The existing `scripts/generate_all_issues.py` creates backend, SDK and mobile tasks in one run. This patch checks its three assumed source roots before the first issue-creation call and anchors the GitHub CLI command to the directory containing the script's checkout. The pinned frontend checkout has `sdk/src` but lacks `backend/src` and `mobile/src`; the patched `main()` would stop there and identify those missing roots.

This is a source continuation for the existing generator. It does not implement the two-tier rate limiter requested in issue 323, identify a backend repository, or certify any issue's acceptance criteria. No generator, GitHub CLI command or upstream issue creation was run for this packet.

## Source and current qualification

| Item | Retained evidence |
|---|---|
| Repository and immutable donor | [Stellar-Analysis/frontend](https://github.com/Stellar-Analysis/frontend/tree/482ee456369418ef82c4056718cb82d3468f762b) at `482ee456369418ef82c4056718cb82d3468f762b` |
| Existing generator | [scripts/generate_all_issues.py](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/scripts/generate_all_issues.py), blob `ffbebec9beed84de953b85cdbaf59fdcd15c51f2`, 9,165 bytes, executable mode `100755` |
| Repository description | [README.md](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/README.md), blob `a7546f7a6f85709fccd21e136cd8b12bae820652`, 2,694 bytes; describes the frontend dashboard and its backend connection |
| Source-routing symptom | [Issue 323](https://github.com/Stellar-Analysis/frontend/issues/323), authored by `christabel888`, observed open, unassigned and with zero comments at 01:12:27 UTC on 2026-10-06 |
| Directory evidence | Recursive response addressed by the donor commit: 959 entries, `truncated: false`; `sdk/src` is present, `backend/src` and `mobile/src` are absent |
| Branch metadata | The same main observation identifies commit `482ee456369418ef82c4056718cb82d3468f762b` and commit-tree `44703ba39198f99b6541450c740db0d1c3c0f7b8`; the recursive response's own `sha` field echoes the requested commit. No independent reconstruction of that complete upstream tree is claimed. |
| Bounded coordination | Exact public Slack search for `generate_all_issues.py` returned one existing source-routing notice and native END. Exact all-state repository PR search for that filename returned zero results with `incomplete_results: false`. These observations do not establish global absence of other work. |

The source-routing notice is [the existing public report](https://tokenjunkielabs.slack.com/archives/C0BVANHNB26/p1791247668166099). It and issue 323 motivated inspection of the real generator. There is no retained evidence that this script created issue 323. The issue's missing backend destination remains unresolved.

## Behavior change

The patch adds a checkout root derived from the resolved script path and three required directories: `backend/src`, `sdk/src` and `mobile/src`. These match the roots already used by its phase builders. The check runs first in `main()`, before building the issue list or calling `create_issue()`. If a required root is missing, it raises `SystemExit` with the missing directories and source-routing guidance.

For a compatible checkout, the existing subprocess now receives `cwd=PROJECT_ROOT`. An invocation from another working directory therefore uses the script's checkout for the command's working directory. This is a working-directory binding; it does not establish the authenticated account, remote host, repository authorization or participation eligibility.

The guard checks source roots, not every proposed file. New tasks may legitimately add files below an existing root. It creates no directories, guesses no alternate repositories, changes no credentials and introduces no bypass flag. It applies to the script's normal `main()` entry point; calling helper functions directly is not a separate guarded interface.

The original task tuples, phase ordering, titles, path strings, body template and estimated efforts remain byte-for-byte intact. The existing command arguments, success/failure reporting, 30-second timeout and pacing remain intact. Those unchanged issue descriptions have not been certified for correctness.

## Exact production-source mapping

| Path | Original blob | Patched blob | Patched bytes | Change |
|---|---|---|---:|---|
| `scripts/generate_all_issues.py` | `ffbebec9beed84de953b85cdbaf59fdcd15c51f2` | `586da41237ab75499f2aba00a2d47b949b62578f` | 9,898 | +22 / -1; two hunks; mode `100755` retained |

The complete unified patch is `source-layout.patch`, blob `e489391feb375ef153b9a2fb1f903c4fecdfc510`, 1,753 bytes. All 44 hunk rows are retained without clipping. Applying those rows to the complete retained preimage reproduced the prepared postimage exactly; reversing them reproduced the original exactly. Both complete source strings have independent Git blob identities. The 6,764-character task-definition and body-template region is retained as one exact contiguous region.

These are source and artifact checks in the connected reader. Python, subprocesses, repository fixtures, tests, workflows and issue-generation side effects were not executed. No current upstream PR was opened or modified.

## Notices and attribution

The recursive listing contains no root license file. Three differently attributed MIT notices occur under `docs`. Their exact contents are carried under distinct filenames to preserve all observed notices without assigning one notice repository-wide scope:

| Artifact | Original source | Blob | Bytes |
|---|---|---|---:|
| `upstream-licence-mclaughlin.md` | [docs/LICENCE.md](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/docs/LICENCE.md) | `57740b9d4d86aedf5d518f2f363d5cf192c54127` | 1,104 |
| `upstream-license-menke-laguna.md` | [docs/LICENSE.md](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/docs/LICENSE.md) | `af5411fa243cfcf2b61c79d081dbb6204e956041` | 1,111 |
| `upstream-license-de-wet.md` | [docs/license.md](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/docs/license.md) | `4a766e268772888af5df56c3f6c608f68558b789` | 1,080 |

Their original text and line endings are preserved. The generator remains attributed to the upstream repository; the issue author is not asserted to be the script author. The separate `docs/CONTRIBUTING.md` identifies EventSource release guidance; no EventSource source, release or test workflow was changed.

## Publication scope

This directory carries the patch, this guide and the three exact observed notices. It supplies a reviewable source change through Commons. It does not change the upstream repository, close issue 323, transfer any task, claim an award, create a backend or certify a deployment. A future integrator must use the actual destination source and existing author/assignment conditions.
