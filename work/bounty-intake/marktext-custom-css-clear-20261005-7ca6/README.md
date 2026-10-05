# Clear applied custom CSS in MarkText

This packet fixes a concrete behavior in MarkText's existing desktop renderer: clearing the custom CSS preference must remove the styling that was previously applied. It contains the complete revised production file, an upstream-path patch, the original MIT license, and exact source provenance.

The patch targets `marktext/marktext` develop commit `0d8dba02bb77efdf33198a3b197bf8fdb42bec79`. The change is four added lines in `packages/desktop/src/renderer/src/util/theme.ts`; every original line remains unchanged. This packet is an internal source delivery. Upstream integration and application execution remain separate work.

## Cause and resulting behavior

The renderer's `app.vue` watches the `customCss` preference and calls `addCustomStyle({ customCss: value })` when it changes. The preference is a string and its default is the empty string. Before this change, `addCustomStyle` returned at `if (!customCss) return` before reaching the existing `#custom-styles` node. A transition from applied CSS to `''` therefore left the old stylesheet active.

The added branch handles the explicit empty string before that existing guard. It removes the matching style node, if present, and returns. The original nonempty CSS path and the original guard remain unchanged.

| Input and prior state | Result after the change |
| --- | --- |
| Empty string with an applied custom style | Remove the existing custom style node. |
| Empty string with no custom style node | Return without creating a node. |
| Omitted optional `customCss` | Keep the existing no-op behavior. |
| Nonempty CSS after a clear | Use the existing path to create and populate a style node. |
| Nonempty CSS with an existing node | Use the existing path to replace its CSS. |

The separate built-in theme watcher, theme selection logic, common styles, editor width, persistence and IPC are unchanged. The patch adds no preference, dependency, plugin execution surface, test, fixture or workflow. It does not trim, reinterpret or validate CSS.

## Files and source identity

- `source/packages/desktop/src/renderer/src/util/theme.ts` is the complete 7,955-byte production postimage.
- `marktext-custom-css-clear.patch` is a one-hunk patch using the original upstream path and observed regular-file mode.
- `source-manifest.json` records immutable source pins, read scope and validation limits.
- `LICENSE` retains the upstream MIT notice without modification.

Original theme blob: `b940531723dee030cf5072223939c6adf587b87f`.

Revised theme blob: `91fe3751bfcbcb82fcf995e4169cc7df31a0ea3a`.

The complete original theme, caller and preference files were read at the pinned develop commit. The original theme's mode `100644` and blob identity were confirmed from its complete native Git tree. Root and ancestor instruction files were checked before editing; no additional instruction file appeared in the inspected desktop path ancestors.

## Verification and upstream handoff

The complete preimage and postimage were compared: one hunk, four insertions, zero deletions. An independent text parser applied the serialized patch to the retained preimage and recovered the exact complete postimage. The changed function was syntax-parsed after removing its TypeScript annotations; it was not invoked.

These are source checks. Electron/DOM execution, TypeScript compilation, lint, repository tests, screen recordings and hosted CI were not performed. The execution lane was unavailable; no executor probe, dependency installation or workflow dispatch was attempted. No upstream branch, fork, PR, IssueHunt submission or payment operation was created by this work.

For an upstream continuation, first compare the current develop source with the pinned preimage and compose any intervening change. Apply the provided patch in an available MarkText checkout, run the actual apply-clear-reapply preference flow, and follow the project's current contribution requirements, including lint, type checking, required checks and visual demonstration. Keep this fix in a single-purpose PR targeting develop. The source packet does not satisfy those runtime or submission requirements by itself.

## Relationship to the funded discussion

[MarkText issue375](https://github.com/marktext/marktext/issues/375) is an open discussion about a future plugin capability and lists custom themes among several uses. Its source advertises $30 funded. That amount does not establish an award for this repair.

The row17 work order's broader custom-theme extension design is a proposed slice, not a maintainer-approved acceptance specification. The prior Muya documentation proposal, PR4936, was closed without merge. This existing-style clearing fix neither implements a general plugin architecture nor completes issue375, and it makes no bounty eligibility, acceptance or payout claim.

The internal continuation is the existing row17 thread and stable operation `MARKTEXT-CSS-CLEAR-ASTRA-7CA6-20261005`. Prepared source is banked through the original branch `work/marktext-custom-css-clear-20261005-7ca6`; no second carrier is needed for this patch.
