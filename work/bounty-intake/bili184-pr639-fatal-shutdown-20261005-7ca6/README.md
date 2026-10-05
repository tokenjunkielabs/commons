# Bili #184 — fatal watcher shutdown continuation

This packet is a narrow continuation of stevenmini2019's open [egoist/bili PR #639](https://github.com/egoist/bili/pull/639) at head `291d8b5c1b567f2a609b283dfbadda23f2680d11`.

## Problem left after PR #639

PR #639 correctly recognizes Rollup `FATAL` events and prints the fatal diagnostic, but it leaves the Rollup watcher running. That can preserve the issue's reported hang even after the error becomes visible.

## Candidate behavior

- Keep PR #639's `ERROR` and `FATAL` diagnostics.
- On the first `FATAL` event, close the watcher.
- Suppress duplicate close attempts from repeated fatal events.
- If watcher shutdown rejects, report that secondary failure without masking or replacing the original fatal diagnostic.
- Keep recoverable `ERROR` events and unrelated watch events unchanged.

The two complete postimage files and `change.patch` are pinned to PR #639's exact head. Apply this as a continuation on that branch or compose the two hunks onto a newer compatible head.

## Evidence and limits

Exact source/test preimages were read from PR #639, and each replacement matched exactly once before publication. The focused tests specify repeated-FATAL idempotence and close-rejection ordering. No Node dependency installation, Jest/TypeScript execution, Rollup process, Vercel workflow, upstream branch mutation, IssueHunt submission, sponsor acceptance, award, or payment is claimed.

Original PR author and IssueHunt submission rights remain with stevenmini2019. The issue currently advertises **$60 funded**; that is not an award or received amount.
