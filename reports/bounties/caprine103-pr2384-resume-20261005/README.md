# Caprine #103: noninteractive resume follow-through for PR #2384

This packet changes the connectivity wait in the existing [upstream PR #2384](https://github.com/sindresorhus/caprine/pull/2384). That PR calls the startup helper `ensureOnline()` after resume. The helper opens a Wait/Quit dialog after 15 seconds offline and calls `app.quit()` if Quit is selected. A normal wake with a slow network should not enter that startup exit flow.

The packet contains a full candidate `source/index.ts` and an exact two-hunk `resume.patch` against PR head `8bd020aef9812a0c2d81fc051e991944fb5b79e9`. It is a source handoff through Commons. It has not been applied to the external contributor's branch or submitted upstream.

## Exact source custody

| Source | Immutable identity |
| --- | --- |
| Upstream main / version 2.61.0 | `c3cbcf94e0c2f964fc9a709a8192625e57ce5206` |
| Main `source/index.ts` | `078ee81c49155fe9b8186465c0a9de8816837b07` |
| Existing PR #2384 head | `8bd020aef9812a0c2d81fc051e991944fb5b79e9` |
| Existing PR `source/index.ts` preimage | `c1c1bfaef8994bdfa57ae39f80f2e23514e6ab02` |
| Main `source/ensure-online.ts` | `4a014c1ded51a6535cfc6d30450804c32aae634a` |
| Main `package.json` | `b9fdaab8fe1b3d0fc19e73c9310cea827640967d` |

The complete current PR file was read. Removing its sole resume block and `powerMonitor` import reproduces the complete main file exactly. The candidate adds only the existing `is-online` dependency import and replaces that resume block. Reversing those two authored replacements reproduces the PR preimage byte-for-byte. No dependency, startup helper, renderer or configuration source is changed.

## Resulting behavior

Only a real `powerMonitor` resume event requests recovery; ordinary focus changes do not. There is at most one `isOnline()` call in flight. A negative result or rejected promise retries after one second without a dialog, application exit, new credential or change to startup behavior.

Each resume gets a new epoch. Suspend, a replacing main-frame navigation, or window close cancels pending recovery and its retry timer. A response from an older epoch cannot reload the current page. A newer resume arriving during an older check waits until that check settles before starting another check. Window close also removes this packet's power and navigation listeners.

Once connectivity is reported, the callback consumes its one pending recovery. It reloads only while the application is not quitting, the window and web contents are live, and a main-frame load is not already in progress. Reload itself keeps the existing PR's semantics. The connectivity library retains its own per-call behavior; this change does not cancel an already running network check. A check that never settles stalls later checks rather than permitting parallel checks.

The navigation listener uses Electron 29's documented deprecated positional `did-start-navigation` arguments. The exact [v29.0.1 API source](https://github.com/electron/electron/blob/v29.0.1/docs/api/web-contents.md) documents those arguments and `isLoadingMainFrame()`, `isDestroyed()` and `reload()`.

## Remaining behavior and delivery boundaries

This does **not** establish safe automatic recovery of an unfinished Messenger draft, pending attachment, in-flight send, call or opaque page state. A reload can still lose such state. It does not prove that general network connectivity means Messenger itself is reachable, nor that reloading repairs the reported failure. The [2016 maintainer objection](https://github.com/sindresorhus/caprine/issues/103#issuecomment-220992542) about unfinished replies remains material. The [2017 interim guidance](https://github.com/sindresorhus/caprine/issues/103#issuecomment-301242072) accepts waiting for connectivity before reload; it is not complete acceptance of this candidate.

The [existing automated review](https://github.com/sindresorhus/caprine/pull/2384#discussion_r3069322492) identified the startup dialog problem. This packet independently bound that finding to the complete current helper and PR patch; it is not maintainer approval.

At the observed source window on 2026-10-05, issue #103 and PR #2384 were open and unassigned/unmerged respectively. Upstream PR creation was `collaborators_only`, with this connection reporting pull permission and no push permission. The separate [OMGletmein/caprine PR #1](https://github.com/OMGletmein/caprine/pull/1), head `9ccae769bd50bbfe97f5ff7b3a635527b306745c`, is an IssueHunt-linked submission inside that contributor's fork; it is not upstream PR #1. Both external carriers and their authorship are preserved.

The [official IssueHunt listing](https://oss.issuehunt.io/r/sindresorhus/caprine/issues/103) displays $100 funded; the [January 9, 2019 receipt](https://github.com/sindresorhus/caprine/issues/103#issuecomment-452771767) identifies the dated funding. Neither is an award or payment receipt. The complete returned issue-comment page contained 24 comments while issue metadata reported 23; that discrepancy was retained.

## Verification actually performed

Verification is static source inspection, exact preimage/candidate transformation, and publication content/identity readbacks. No TypeScript build, lint, test, Electron execution, network-resume exercise, Messenger session, draft-preservation test or hardware run was performed. No external comment, PR, assignment, platform claim, account action or payment action was made.

Activity: `CAPRINE103-2384-NONINTERACTIVE-RESUME-20261005-7CA6`, [original work-order thread](https://tokenjunkielabs.slack.com/archives/C0BU51F1PL3/p1791165000776759?thread_ts=1791164486.648779&cid=C0BU51F1PL3). The activity label grants no exclusive ownership and does not supersede the external carrier's custody.
