# electron-reloader #2: ESM default-app restart with inherited stdio

This packet ports the issue's existing development-restart approach to current upstream `index.js`, which uses ESM and `import.meta`. It adds a process-creation failure path: the current app exits only after Node emits the replacement process's `spawn` event. A failed spawn leaves the current app alive and permits a later watched change to retry. Packaged/non-default-app launches retain the existing `app.relaunch(); app.exit(0)` path.

This is an internal source handoff. It has not been published upstream, run in Electron, accepted by the maintainer, or awarded a bounty.

## Source and target

- Issue: https://github.com/sindresorhus/electron-reloader/issues/2
- Upstream commit: `a40ac942d86bab1265ca673b2b6bd3f3e0e5c9c9`.
- Original `index.js`: `227a3002d56fcd0b55b471c4632b3a4d78652ba0`, 2,041 UTF-8 bytes.
- Production postimage: [index.js](index.js), `b1916af02a1b252663fa9eb43356a468da6e40d2`, 3,054 UTF-8 bytes.
- Apply [restart.patch](restart.patch) to that exact upstream preimage. The patch changes one import and the restart body only.
- Current `package.json`: `54553a3c11cbdd444140bacb01428ed171bc21d1`; `readme.md`: `63b83cca1dc7ee2bdbd3823ba1473b6a5f5ec4ba`. They identify the ESM API, Node >=22, and Electron 44 or later. No package, dependency, declaration, watcher option or renderer behavior is changed.
- The upstream MIT [license](license) is retained verbatim.

## Restart behavior

For an Electron default-app development run, the code invokes `spawn(process.execPath, process.argv.slice(1))` without a shell and with the current working directory, environment and inherited stdin/stdout/stderr. The existing duplicate-change flag is set before this work. It remains set while process creation is pending and after success.

If the current instance holds Electron's single-instance lock, it releases that lock before spawning so the replacement can acquire it. Synchronous setup/spawn failure and Node's asynchronous `error` event reset the duplicate-change flag, attempt to reacquire a previously held lock, and log the error. Failed lock reacquisition is logged separately; the current app remains running. This is a best-effort restoration, not an atomic lock handoff.

The `spawn` event establishes OS process creation, not successful Electron initialization, a rendered window, restored application state or a healthy application. If the child starts but later crashes, this patch does not resurrect the exited parent. Inherited descriptors preserve the output route supplied by the launching environment; they do not keep the original shell command alive or establish cross-platform terminal, process-group or supervisor behavior.

The existing watcher scope, ignore options, development-only guard, quit cleanup, ESM validation and packaged relaunch path remain unchanged. The current upstream restarts on every watched change; this packet does not reintroduce the old CommonJS renderer-only reload mechanism.

## Existing work and funding

The issue's currently listed submission is [LYY435939/electron-reloader PR #1](https://github.com/LYY435939/electron-reloader/pull/1), OPEN/unmerged when read, head `ba66777681ea6e41c6af50c000db63cb23d4b79b`, base `9ec0176bf2e1dd2cc43588f863086c1cca6cdab4`. Both PR base and head repositories are the contributor's fork. It adds inherited-stdio spawn to an older CommonJS implementation and immediately exits after calling spawn. It is not an upstream PR or a drop-in patch for the current ESM source.

The issue also contains prior inherited-stdio approaches from johnsmith507, Hmazo, zergzorg and whyujjwal. Credit for that approach stays with those existing contributors and the listed fork PR. This packet supplies the current ESM postimage and process-creation error handling; it claims no novelty or exhaustive competing-source coverage. One read of whyujjwal's named branch metadata returned tool-level HTTP 400 INVALID_ARGUMENT, with no provider source body. It was not retried or replaced with another route, so that branch's current source remains unobserved.

The complete issue and all 11 returned comments were read. [Funding comment 475146512](https://github.com/sindresorhus/electron-reloader/issues/2#issuecomment-475146512) records $40 on March 21, 2019 and instructs contributors to submit through IssueHunt. The current issue body still advertises $40. Neither is evidence of an award, payment, current escrow balance or guaranteed eligibility. Contributor comments report denied upstream PR creation. This lane observed upstream pull:true/push:false and an all-state `author:woahwhattheheck` upstream PR search returning zero; no upstream/fork creation, credentials, claim or bounty submission was attempted.

## Validation and remaining work

Only complete-source inspection, exact UTF-8 Git blob checks and serialized patch comparison were performed. No candidate code was invoked. No native Electron launch, operating-system process, terminal, single-instance or window behavior was exercised. No test, mock, fixture, package install, build or workflow was created or run.

The integration owner can apply the packet to the exact preimage, reconcile any newer upstream edits, and use an authorized application environment to assess actual restart/terminal behavior before any upstream submission or acceptance claim. This source delivery does not close the broad historical issue, whose discussion includes terminal detachment and multiple-window observations.

Primary API contracts used:
- Node.js [ChildProcess spawn/error events and stdio](https://nodejs.org/api/child_process.html#event-spawn): successful `spawn` precedes other child events; failure emits `error` instead. Application startup may still fail after `spawn`.
- Electron [relaunch/exit](https://www.electronjs.org/docs/latest/api/app#apprelaunchoptions) and [single-instance lock methods](https://www.electronjs.org/docs/latest/api/app#apphassingleinstancelock).

Operation: `ELECTRON-RELOADER2-ESM-STDIO-20261005-7CA6`. Original internal work order: [BATCH25-05 row 28](https://tokenjunkielabs.slack.com/archives/C0BU51F1PL3/p1791171038724239).
