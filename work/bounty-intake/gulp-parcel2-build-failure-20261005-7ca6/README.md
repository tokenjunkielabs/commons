# Gulp Parcel: terminate failed build promises

This is a small production follow-up to the existing [gulp-parcel PR #20](https://github.com/zacky1972/gulp-parcel/pull/20). It finishes failed Parcel builds through the Gulp transform callback and prevents a failed build from entering output processing.

## Source and attribution

Susumu Yamazaki's gulp-parcel is distributed under the included original MIT notice. JulesB40's PR #20 supplies the generated-asset traversal, relative asset URLs and nested output-path preservation. johnsmith507's earlier [PR #19](https://github.com/zacky1972/gulp-parcel/pull/19) supplies the earlier asset-emission proposal and already returns from its reported-build-error branch. This follow-up preserves PR #20's success path and adds terminal callback-error handling for both build failure forms. It does not replace either contributor's submission or claim their runtime results.

| Source | Immutable identity |
| --- | --- |
| Canonical master observed | `6e811cd565456017c69f3fe796562c520180eea6` |
| Canonical index.js | `5efbd9626b5e181e1f1b944f469d9900295644f8`, 4,282 bytes |
| PR #20 head / sole parent | `2ccd247030b3dd8a3162026bcefe8482085817b1` / canonical master above |
| PR #20 complete root tree | `042899b2e5ea8c1a1b6a7672e708ab009a887834` |
| Patch preimage, index.js | `cb880abdc5b7e8b967756cf0761867ef1a4cc2d7`, 5,437 bytes, mode 100644 |
| Complete patched index.js | `e3c797518f627e1ee59a8818d1c28d4df343d050`, 5,483 bytes, mode 100644 |
| Included original LICENSE | `64bae5f81a8a555fe31e12f5ad6f5237977f74ba`, 1,106 bytes |

The preimage and its tree were read directly from [the contributor's pinned commit](https://github.com/JulesB40/gulp-parcel/tree/2ccd247030b3dd8a3162026bcefe8482085817b1). Complete UTF-8 contents matched their Git blob identities. The complete root listing contains no AGENTS.md or CONTRIBUTING file; the repository README and original license were read. The license retains its literal HTML entities exactly as stored upstream.

## Failure paths and repair

The existing source calls `parcel.bundle().then(success)` without a rejection handler. A rejected build promise therefore has no path to complete the transform callback. When the promise fulfills while `parcel.errored` is set, the source emits an error and calls `cb(null, file)`, then continues into the output code. With an error listener installed, this can process an absent or failed bundle and attempt another callback.

The two-hunk change (+10/-6) introduces one local `failBuild` function. It retains the existing temporary-directory cleanup and generic `PluginError` message, then calls `cb(error)` without forwarding the failed input file. The reported-error branch invokes it and immediately returns. The same function is supplied as the promise rejection handler.

The second argument to `then` handles the build promise's rejection. It deliberately does not treat an exception thrown later by the success callback as another build-promise rejection.

## Preserved production behavior

The full source prefix before the changed promise section and the full successful-output body after the reported-error branch were compared byte for byte and are unchanged. This includes the relative `publicURL` default, generated-bundle traversal, nested destination mapping, Pug name adjustment, successful output callbacks, explicit-output-directory branch, and current watch/signal behavior. No dependency, parser, build configuration, fixture, test, or workflow file is included or changed.

This is a repair of build-promise settlement. Existing asynchronous filesystem error handling, explicit-output duplicate emission, partial-output behavior, temporary-directory isolation/cleanup implementation and signal-listener lifecycle were not redesigned. No general all-errors, atomic-output, watch-mode, browser, Windows, or runtime acceptance claim is made.

## Integration

The patch is relative to PR #20's exact index.js preimage, whose hash appears above. Apply `build-failure.patch` at that source root, or use the complete `source/index.js` postimage after reconciling any newer edits. It is not a drop-in patch for canonical master: the PR #20 asset changes are already part of this preimage. Existing contributor attribution and maintainer review remain in place.

The serialized patch was parsed independently, each removed/context line was compared with the full preimage, each hunk's old/new counts were checked, and its reconstructed file matched the complete postimage exactly. The complete CommonJS source was syntax-parsed without invocation. Parcel, Gulp, Node dependencies, filesystem behavior, tests, builds, hosted workflows, upstream submission, and platform actions were not executed in this continuation.

## Issue and delivery state

[Issue #2](https://github.com/zacky1972/gulp-parcel/issues/2) was observed OPEN and unassigned. Its [historical IssueHunt funding comment](https://github.com/zacky1972/gulp-parcel/issues/2#issuecomment-444370068) records $25; the later availability question has no maintainer answer in the four comments read. That historical amount is not a current funding, eligibility, acceptance, award, or payment confirmation.

PR #20 was observed OPEN at the pinned head; PR #19 remains a distinct external proposal. Exact own-PR and Commons `gulp-parcel` searches each returned zero; the complete bounded public Slack search returned only the two BATCH06 intake posts. Search results are observations, not a global ownership or exclusivity assertion.

This Commons packet publishes the source follow-up for integration. It does not create another upstream PR, contact either author or maintainer, claim a bounty, or perform a payment action.

Operation: `GULP-PARCEL2-BUILD-FAILURE-7CA6-20261005`.
