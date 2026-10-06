# PayD tour completion when optional storage fails

The existing onboarding callback first writes its completion marker to localStorage, then closes the local tour and calls the parent completion callback. A synchronous storage exception interrupts both close calls. This patch catches only that optional persistence write, allowing the existing close sequence to continue.

## Canonical carrier and attribution

Intake: [Protocol-Guild/PayD issue487](https://github.com/Protocol-Guild/PayD/issues/487). The actual connected source is [open PR595](https://github.com/Protocol-Guild/PayD/pull/595), authored by waterWang, branch `waterWang/PayD:feat/487-onboarding-tour`, immutable head `a6e738579ac9840df88e1b54c6d6324ed3539dd6`. Its base is `860705c2ecbe53aa26c332f945d884ad815aa577`.

Complete current PR metadata and its five-path change listing were retained at the selected head. The PR is open, unmerged and not a draft. The complete App.tsx mounts OnboardingTour after its routes, supplies navigateTo, and supplies an onComplete callback that sets showTour(false). The complete component establishes the affected completion branch. This packet is a source continuation of that existing contribution; it does not recreate the tour or assert its upstream acceptance.

Original waterWang and PayD contributors retain authorship. No external branch, PR, issue, comment, assignment, claim or account was changed. Earlier sponsor-main observations of an unconnected tour concern a different source revision and do not replace the actual PR595 caller qualification.

| Retained source at the donor head | Git blob |
| --- | --- |
| frontend/src/App.tsx | 1f6b31f470ffe05b487dc00a75217cbe26643fb5 |
| frontend/src/components/OnboardingTour.tsx | 89ab9b2f13a91bfddccad35fd8ce1c9d4842bb35 |
| frontend/package.json | 33e58d67eca11b200b6988835b1f8450f179d2c2 |
| frontend/package-lock.json | 1b41ce5d700d3a51d0e9ba52418ea7b53c9479ab |
| LICENSE | 261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64 |

## Exact production change

Apply `tour-completion-storage.patch` to that immutable donor or reconcile its exact contexts against a later revision.

| Production path | Preimage | Prepared postimage | Prepared UTF-8 bytes |
| --- | --- | --- | ---: |
| frontend/src/components/OnboardingTour.tsx | 89ab9b2f13a91bfddccad35fd8ce1c9d4842bb35 | 0bff792114244eb90b22ca0450a260128c993678 | 4,191 |

The two-hunk change is +6/-1, including a dated modification notice. Inside the unchanged FINISHED/SKIPPED branch, only localStorage.setItem is enclosed by try/catch. The unchanged setInternalRun(false), onComplete() and return remain outside that catch, in their original order. No storage exception or copied application data is logged.

[MDN's Storage.setItem documentation](https://developer.mozilla.org/en-US/docs/Web/API/Storage/setItem) identifies a synchronous QuotaExceededError when a value cannot be stored. The source-level interruption and correction follow directly from that documented failure boundary and the complete existing callback. No storage probe or failure simulation was performed.

Successful persistence still writes the same key and value. Failed persistence means the completion preference may not survive; a later visit can show the tour again. The patch does not report persistence success or create a fallback persistence mechanism.

## Boundaries and unresolved behavior

The App's initial getItem/authentication check is unchanged and can still fail independently. The once-mounted authentication effect, restart events, navigation timing, target availability, Back behavior, controlled index movement, theme, copy, steps and all other callbacks are unchanged. Exceptions from onComplete are not swallowed by the storage catch. There is no cross-tab synchronization, storage-event handler, account partitioning, retention policy or guaranteed completion under unrelated errors.

The complete package locks react-joyride 2.9.3 and React 19.2.0. The Joyride lock entry declares React and React DOM peer ranges of 15 through 18; the manifest separately contains overrides to the root React dependencies. Those source facts do not establish installed compatibility. No dependency was changed, installed or executed, and no whole-application or whole-PR readiness claim is made.

The exact version-specific callback documentation URL, https://docs.react-joyride.com/callback, returned a timeout. It remains held without retry or alternate acquisition. Current v3 documentation uses a different event interface and was not used to establish the locked v2 callback contract. The proposed navigation/Back correction was not prepared or published. This packet only preserves the callback's existing admission checks and changes the independent storage-exception boundary inside them.

## Source validation and distribution

The complete original component has 3,982 UTF-8 bytes; the prepared component has 4,191. Independent Git identities bind both. Forward application reproduces the entire prepared source and reverse application restores every original byte. Removing the catch expansion and modification notice restores the original component. Both source and postimage retain the original absence of a final newline.

The first local patch-materialization comparison exposed that the inherited comparison helper always appended a newline. That comparison failed before publication. The two edited hunks precede the untouched tail; materialization was corrected to preserve the actual input's terminal-newline convention, after which complete forward and reverse identities matched. No production function, synthetic callback, storage failure, fixture, test, compiler, application, browser or dependency runtime was executed.

Only the focused patch, this guide and the exact Apache-2.0 license are published. The complete 724-entry donor tree was not truncated and contains the root LICENSE but no separate NOTICE file. The license is retained verbatim, 11,357 UTF-8 bytes; existing source notices are preserved and the changed component gains a dated modification notice.

There was no wallet, authentication, credential, payment, employee/account data, clipboard, transaction, upstream submission or reward action. Source custody and static ordering checks are not runtime acceptance.
