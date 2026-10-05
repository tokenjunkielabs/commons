# Keep dropdown selection within the visible option page

This is a distinct source continuation of [Protocol-Guild/PayD issue #301](https://github.com/Protocol-Guild/PayD/issues/301) and SrvFernandes's [PR #661](https://github.com/Protocol-Guild/PayD/pull/661). It repairs the submitted AdvancedDropdown's focus, committed selection and page boundaries. It composes with the separate [Layout import correction #31741](https://github.com/woahwhattheheck/commons/pull/31741), whose patch and guide are unchanged.

## Source custody and original contribution

The canonical source repository is Protocol-Guild/PayD. PR #661 was OPEN/unmerged at `624f69b413d40ccc8dc9bf5c52a22e1789b1f980`, with base `171c74b454daba241bfb75f36d10a0a3a77a68e5`. The original author is SrvFernandes. Issue #301 was OPEN and unassigned, with third-party assignment/claim comments rather than maintainer acceptance. The PR discussion and inline-comment collections were empty when qualified.

The complete `src/components/AdvancedDropdown.jsx` was retained at blob `711777754d56e6f617fd0423f8e8f423c5c87abc`. This work uses that actual source, not a recreated widget or a replay of the earlier import correction. The external author's added Layout, responsive hook and UI slice remain separate. No upstream branch or PR is modified.

## Observed source behavior

The original component uses focusedOption both for hover/keyboard focus and the header label. Merely hovering or arrowing changes that label, while a click need not have been preceded by mouse-enter. Search and pagination change currentOptions without clearing focusedOption. Enter checks only whether that old object is truthy, so it can submit an option excluded by the current filter or page.

With no focus, findIndex returns -1; the original ArrowUp formula then points to the penultimate option for a page with multiple options. Empty results have zero total pages, yet currentPage starts at one and the Next equality check is false. Option-list shrinkage can also leave the page beyond the last available page. Finally, keydown bubbles from the actual pagination buttons to the parent's Enter selection handler, which prevents their native activation.

These are source-derived paths, not observed browser failures or reproduced user interactions.

## Coherent selection and pagination correction

A separate selectedOption stores the last selection submitted through the existing onChange callback. The header uses that committed value; hover and arrow movement only change focusedOption. A shared selectOption function serves click and Enter, invoking onChange before committing the local selection/focus and closing, preserving the callback-before-close ordering. No new controlled-value prop, persistence or data fetching is added.

Enter selects only when the focused object is present in currentOptions, using the existing object-identity semantics. Filtering and explicit page navigation clear focus. If new option objects replace the old objects, the membership guard also prevents the stale object from being submitted. A previously committed label is retained until another selection; this patch does not invent an external-value synchronization or automatic selection-removal policy.

Both arrow branches check that the current page is nonempty. ArrowDown from no focus reaches the first option; ArrowUp from no focus or the first option reaches the last. Empty-page arrow and Enter paths produce no selection. Opening by Enter or Space prevents that key's default action.

The displayed page and slice use an immediately clamped page number. The page count is at least one, so an empty filtered list presents page one of one with both navigation buttons disabled. A pure page-state update in an effect keeps the stored page clamped as the page count shrinks. Navigation uses the displayed page and inclusive boundary checks; search still resets to page one.

The open dropdown's Enter handler returns for the actual button or a descendant before preventing default or selecting an option. Pagination buttons explicitly have type=button, so their native keyboard activation remains a local page action rather than a form submission. Their click handlers retain page navigation and also clear focus. Escape and the existing outside-mousedown listener/cleanup remain unchanged.

The existing caller assumptions still apply: options is an array of objects with string labels and stable unique values, onChange is callable, and pageSize is a positive integer (default five). Invalid page sizes and malformed prop data are not newly validated. The component remains browser-oriented. This change does not claim complete combobox roles, active-descendant announcements, DOM focus management, assistive-technology behavior or whole-widget accessibility acceptance.

## Text checks and integration boundary

The serialized single-file patch contains 7 hunks, +45/-17 lines. It applies exactly to the complete preimage and reverses exactly from postimage `de436d73482bfe9e2c29674bc880dee882f6239d` (4911 UTF-8 bytes). Independent Git blob identities match. Only source text was transformed and checked; no production function, fixture, synthetic event, React renderer, browser, keyboard test or build was executed.

The retained untruncated 761-entry tree pins root App.tsx `9d90c939a186a17f5bc042b50191b554357b6f6c` and package.json `f0325832d3e5150375bd22481e577d19cd148eb6`, whose complete bytes were already read. The App does not mount this proposed dropdown or Layout; the package omits the submitted Layout's Redux dependencies. No app routing/provider/dependency integration is supplied or claimed.

The same tree identifies already-read CONTRIBUTING.md `1e015aa7e145db0cd0e306f7032cce130b8acbb8`, LICENSE `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` and README.md `374ffef680426f41b9f3e832059106839cfc72bd`, with no AGENTS.md or nearer instruction/license. CONTRIBUTING.md is a scaffold placeholder. Root LICENSE is Apache 2.0 while README presents an MIT badge. The discrepancy is retained; this packet publishes only an attributed patch and guide, with no full source module or invented licensing conclusion.

Original author, assignment and upstream acceptance conditions remain separate. No real option/account/customer/financial input, wallet, payment, upstream contact/submission/claim, runtime, tests or award action occurred. This correction does not establish whole issue #301 or PR #661 completion.
