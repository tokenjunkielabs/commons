# Keep employee sort updaters pure

This is an attributed, source-only continuation for [Protocol-Guild/PayD issue #277](https://github.com/Protocol-Guild/PayD/issues/277) and SrvFernandes's existing [PR #660](https://github.com/Protocol-Guild/PayD/pull/660). It corrects one state-update boundary in the submitted employee-directory component. The external PR, contributor claim, and broader integration remain separate.

## Exact source and chronology

PR #660 was observed OPEN and unmerged at head `9533adfbac502c08737a3462db39be8c9ce5f049`, with base `171c74b454daba241bfb75f36d10a0a3a77a68e5`. Its current discussion and inline-comment collections were empty. Issue #277 was OPEN, unassigned, and had two third-party comments: an assignment request and the original author's PR link/claim. Neither establishes maintainer assignment, acceptance or an award.

The complete edited source `src/App.tsx` is 4,012 bytes, Git blob `7d9ec5ca0b7bece0a2bb3d579fa68a59e7157f42`. The complete `src/main.tsx` is blob `a46835a4fc288594376924f7e83d723beb272478` and wraps App in StrictMode. The native PR diff supplies the actual EmployeeTable caller: each sortable table heading invokes its supplied `onSort(key)` from its click handler. App supplies `handleSort` as that prop.

A bounded recently-updated open-issue query provided the original #277 locator. Its connector rows omitted optional state/date/assignee metadata; these facts were established by the exact issue/PR reads instead. A separate `is:pr 277` connector query returned issue rows and was not treated as PR coverage. The actual issue comment supplied the exact #660 link. No global duplicate, funding, or repository coverage claim follows.

## Defect and correction

The submitted callback passes a function to `setSortField` that itself invokes `setSortDirection`. This schedules another state update while React is evaluating an updater. [React's useState reference](https://react.dev/reference/react/useState#setstate) requires updater functions to be pure, and [StrictMode guidance](https://react.dev/reference/react/StrictMode#fixing-bugs-found-by-double-rendering-in-development) includes updater functions in its development purity checks. The [useState troubleshooting explanation](https://react.dev/reference/react/useState#my-initializer-or-updater-function-runs-twice) distinguishes those checks from event handlers.

The patch schedules both updates directly from `handleSort`. Its functional direction updater only returns the next direction: it toggles the pending direction for the currently selected field, and returns ascending for a different field. The field setter receives the selected field value directly. Adding `sortField` to the callback dependency array keeps the selected-field comparison current after rendering.

This retains the existing intentional-click behavior: the same heading toggles direction; a different heading starts ascending. Search, filtering, comparison logic, table rendering and source data are unchanged. No exact double-toggle count, observed UI symptom or production double invocation is asserted. The source correction follows the documented purity requirement.

The sole production hunk is +7/-9. Its complete 3,973-byte postimage has Git blob `cd03f30c4dbcecf09b17094fabfc88da74ef9a08`. The serialized patch applies exactly to the full preimage, reverses exactly to it, and leaves all bytes outside this callback replacement unchanged. These are text and identity checks, not application execution.

## Scope and redistribution

The PR contains a broader replacement of root routing and package configuration. Its added API adapter maps GitHub issues into employee-shaped rows and synthesizes salary values with Math.random. This packet does not adopt that adapter as employee or financial evidence, repair those broader choices, restore removed routes, or establish that the whole PR is suitable for integration. PR-body promises such as debouncing and multi-select are not certified here.

The acquired untruncated recursive listing contains 767 entries and identifies root CONTRIBUTING.md and LICENSE, with no AGENTS.md or nearer source instruction file. Complete CONTRIBUTING.md (`1e015aa7e145db0cd0e306f7032cce130b8acbb8`) is a short scaffold placeholder. Complete LICENSE (`261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`) is Apache 2.0, whereas the complete README (`374ffef680426f41b9f3e832059106839cfc72bd`) displays an MIT badge. This packet preserves that conflicting declaration and contains only the narrow patch and guide, not a republished full application module. SrvFernandes retains credit for the submitted implementation; the callback change is identified above as this continuation.

A separate source scout read only the official React documentation and assessed the supplied updater/caller contract. That is documentary reasoning, not inspection or execution of the application by that scout.

No React/TypeScript/Node execution, browser interaction, tests, fixtures, dependency installation, build, workflow, account, employee-data access, wallet/transaction, upstream contact/claim/submission, award or payment action was performed. No acceptance, deployment, performance or full issue-resolution claim is made. Existing held routes remain held.
