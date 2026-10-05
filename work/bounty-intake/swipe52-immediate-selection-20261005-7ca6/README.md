# SwipeableTabBarController #52: newer immediate selections supersede queued ones

This is a static production-source follow-up to [external PR #127](https://github.com/marcosgriselli/SwipeableTabBarController/pull/127) by **apples-kksk**. It addresses one ordering gap in that contribution's latest-request queue. It does not establish that the original rapid-swipe freeze is fully fixed or that an iOS device run succeeds.

## Concrete source-derived interleaving

PR #127 retains a `pendingSelection` while a transition is active. Its transition-completion handler dispatches `completePendingSelection()` asynchronously to the main queue. There is therefore a separate queued drain, rather than an atomic transition-completion-and-selection operation.

Consider an old queued choice A. The active transition finishes, and its completion schedules the drain. Before that drain runs, a newer valid request B reaches an immediate selection path with `transitionCoordinator == nil`. In the retained source, the immediate index setter, contained-view-controller setter and ordinary accepted tab tap can proceed without clearing A. The scheduled drain can then apply or requeue A after B, contrary to the stated latest-request policy.

The postimage clears `pendingSelection` before preparing each immediate index/controller transition, and before preparing an ordinary accepted tap. The tap change stays inside `!isApplyingPreparedSelection`, so internal prepared-selection callbacks do not discard a later queued request. A tap rejected by the existing active-transition guard continues to queue normally.

Clearing occurs before preparation or superclass setters that may re-enter selection. The already-scheduled handler flag is intentionally retained: that callback can no-op when nothing remains, or consume a genuinely later queued request. No callback cancellation, extra dispatch, timer, forced retry or transition protocol change is introduced.

This is an analysis of a possible ordering admitted by the source, not an executed UIKit reproduction. Existing valid selection behavior is the intended scope. Invalid-index handling, nil/foreign-controller pass-through, subclass overrides, controller-list replacement and the broad freeze report are not newly resolved by this packet.

## Immutable source and ownership

- Original issue: [#52](https://github.com/marcosgriselli/SwipeableTabBarController/issues/52), OPEN and assigned to maintainer **marcosgriselli** in the retained read. All 37 comments were read.
- External source carrier: PR #127 by apples-kksk, OPEN/unmerged at head `98e7199d0b956599ea5bc928411a973ea402e6b5`, recorded master base `f90f5142a9cd119f8929cec1bfcf78aa0a2f2e8f`.
- Complete preimage: [SwipeableTabBarController.swift](https://github.com/marcosgriselli/SwipeableTabBarController/blob/98e7199d0b956599ea5bc928411a973ea402e6b5/SwipeableTabBarController/SwipeableTabBarController.swift), Git blob `9f27797445cb89c27ff98803fcfb3a1e964c1418`.
- PR #125 by johnsmith507 remains an OPEN competing queue implementation. PR #126 by ncthuc2004 is CLOSED/unmerged, not an accepted fix. Their complete production diffs were read; their authorship and external carriers remain intact.
- The repository README, blob `1a752675c5b5978c17e37be501d87f3208eed8c6`, invites contributions. The issue's [owner comment 753678701](https://github.com/marcosgriselli/SwipeableTabBarController/issues/52#issuecomment-753678701) welcomes help and conditions the reward on a proven working fix. Maintainer assignment is preserved, not represented as a new exclusive claim by this packet.
- Historic funding comments [596511134](https://github.com/marcosgriselli/SwipeableTabBarController/issues/52#issuecomment-596511134) and [642121746](https://github.com/marcosgriselli/SwipeableTabBarController/issues/52#issuecomment-642121746) record $80 and $70. The current issue advertises $150 and requires IssueHunt submission for the reward. This establishes amount/source conditions, not current escrow, payout or our eligibility.
- Exact public `SwipeableTabBarController` + `52` search returned only the existing BATCH25-05 row. Native all-state own-account PR query returned an empty list. These bounded observations are not a universal ownership census.

## Files and verification

`source/SwipeableTabBarController/SwipeableTabBarController.swift` is the complete postimage, blob `ac13aa60ffe70c5026b472c4d5a99ad191807837`, 15,982 UTF-8 bytes. `supersede-queued-selection.patch` applies to the exact PR #127 head above: three hunks, +6/-0, adding three assignments and their comments. All other source bytes are unchanged. An independent serialized patch application reconstructed the full postimage exactly; full UTF-8 Git identities and publication readbacks bind the stored bytes.

The MIT `LICENSE` is copied exactly from blob `0e69fb6375ca308bf5e1b65d4126be9f75c9c784`. Original Marcos Griselli copyright and the upstream contributor implementation remain credited.

The upstream PR template, blob `621f7f100cb324386086cf318ad75b64983b1b9f`, asks for UI tests and README updates while allowing those follow-ups after opening a PR. No such upstream PR is opened here. The executor, compiler, iOS runtime, simulator and tests were not run. Prior PR authors' validation reports were read as their reports, not repeated or independently certified. No workflow, account, platform submission, maintainer contact, award or payment action occurred.

Operation: `SWIPE52-IMMEDIATE-SELECTION-SUPERSEDES-20261005-7CA6`; original internal activity C0BU51F1PL3 / `1791181236.972389`, following BATCH25-05 row 8.
