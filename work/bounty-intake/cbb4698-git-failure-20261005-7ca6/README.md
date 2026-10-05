# Preserve Git failures in the changelog generator

This source-only continuation over **eij0471**'s [PR 4698](https://github.com/claude-builders-bounty/claude-builders-bounty/pull/4698) makes required Git reads report their failure instead of appearing as an empty successful history.

## Source and integration

The exact external head is `17bcc3549867e38615a84a9d6bffe9b05b4b7ab2`, branch `feat-changelog-generator` in `eij0471/claude-builders-bounty`. The full `generate_changelog.py` preimage is blob `521956ed011a7b64ff9347d2e98282bdc4ba02a7`.

Apply `change.patch` to that file on the documented pin. The packet contains the complete corrected production postimage for comparison. When composing with a newer revision, preserve its changes and apply only the error-propagation hunk rather than overwriting the newer file.

The unchanged `changelog.sh` caller, blob `b2fc752a97a651be63cb04415d3b8f48c2c7e486`, invokes the Python program as its final command under `set -euo pipefail`. It therefore propagates this error outcome without a wrapper edit. The bundled MIT license is unchanged from blob `19f591c09faad54c09b87775128ada9d625ab1fa`.

## Concrete behavior

Previously `run_git` caught every `CalledProcessError` and returned an empty string. `get_commits` translated empty output into an empty list; `main` then printed its no-new-commits message and exited 0. A Git history failure, such as an invalid explicit `--since` reference, was consequently reported as successful absence.

Required reads now print a diagnostic naming the Git subcommand, its nonzero status and captured stderr, then exit with that status. This occurs before Markdown generation or file writing.

The expected optional `git describe` probe alone sets `allow_failure=True`, preserving the existing fallback to the sorted tag list. A successful empty tag list still falls back to `HEAD`; a successful Git log with no commits still follows the existing no-new-commits success path. Failure of the required tag-list or log command remains an error. The existing choice of a tag from another branch, categorization, message formatting and changelog update policy are unchanged.

## Acceptance limits

The entire production file, wrapper and contributed skill instructions were read as source. No skill or script was invoked. The executor is offline: no Git command, Python, shell, test, fixture, sample generation or workflow was run. The one-hunk patch was compared as text with the pinned source, and the full published source/patch/guide/license were read back.

Actual tagged, untagged, empty-history-range and Git-failure operation remains unperformed. The external PR's sample and self-reported checks are not evidence of execution by this lane.

[Issue 1](https://github.com/claude-builders-bounty/claude-builders-bounty/issues/1) requires `/opire try` before submission. No upstream claim, contact, mutation, sponsor acceptance or payment occurred. Its reported 2,289-comment discussion was not expanded, and this packet is not whole-bounty acceptance.

The pinned root README points to `skills/generate-changelog/`, while the supplied files are in the repository root and that directory is absent. This packet does not repair installation/skill discovery, verify the claimed real-repository sample, change repeat-run changelog behavior, or establish other issue1 acceptance criteria.
