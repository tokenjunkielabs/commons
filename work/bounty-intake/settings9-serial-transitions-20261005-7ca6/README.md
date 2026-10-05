# Settings #9: serialize rapid tab transitions

This packet changes one production Swift file so a second tab request waits until the current AppKit transition finishes installing its destination constraints. Requests arriving during that interval replace one pending request; only the latest index and its animation preference are retained. This addresses the overlapping-transition source path in [Settings issue #9](https://github.com/sindresorhus/Settings/issues/9). It does not establish that every sizing report in that issue is resolved.

## Source and contents

The upstream base is [sindresorhus/Settings at f41475771f65379ca10852c95119a7f53f0de5a5](https://github.com/sindresorhus/Settings/tree/f41475771f65379ca10852c95119a7f53f0de5a5), tree `60615602487bebed9a5d63286e7eb224186dbbe1`. The repository was public, unarchived and readable, with upstream push permission false and a collaborators-only pull-request creation policy.

| Packet file | Role |
| --- | --- |
| `SettingsTabViewController.swift` | Complete production postimage for `Sources/Settings/SettingsTabViewController.swift`. |
| `transitions.patch` | Four unified hunks against the exact upstream preimage; 35 added and 17 removed lines. |
| `license` | Unchanged upstream MIT license, Git blob `fa7ceba3eb4a9657a9db7f3ffca4e4e97a9019de`. |
| `README.md` | Source, implementation, integration and validation boundaries. |

The preimage is 6,865 bytes, Git blob `82c47896a3be388d285b052f26aaf2e13ea10f70`. The postimage is 7,390 bytes, Git blob `7f66ab796eaab40286e0462c25264f6319aa07e1`.

The current package declares Swift tools 5.8 and macOS 10.13. The full production source, package manifest, two style controllers and their protocol were read. The style-controller source pins are `a2a58ed0002ccc4a776988542af3b7bce9f176af` (toolbar), `9e34ad596a0cab77d3c47d25711c90fd480057a9` (segmented control), and `892b82cd5007957c9e4993255dd56a17c249ce3f` (protocol).

## Changed behavior

Previously, `activateTab` started a transition and then updated `activeTab`, selection and title in a `defer`. Another request could start a second transition before the first completion ran. Each completion then installed constraints for its own captured destination.

The new path:

1. While busy, replace the pending `(index, animated)` tuple and return. This path performs no programmatic selection update.
2. When idle, capture the previous active index. An unchanged target refreshes selection/title and returns.
3. For a changed target, mark the controller busy and publish the active target before selection, title or view work can re-enter it.
4. Use the captured previous index as the explicit transition source. Initial display also remains busy until it finishes installing constraints and setting the initial frame.
5. In the transition completion, retain the existing toolbar refresh, install destination constraints, clear the busy state, take and clear the pending tuple, then activate that pending target.

There is no state-writing defer after the transition call. A synchronous completion can therefore drain a pending target without a returning outer activation overwriting it. Returning to the in-flight target as the latest request replaces an earlier pending different target; the subsequent same-target activation starts no extra transition.

This is a serialized latest-request policy, not a queue promising to display every intermediate click. Native controls can show their pending selection while the current transition finishes; title and active-controller state follow the transition being started. The controller continues to rely on normal AppKit-thread use and its existing completion contract. The patch adds neither cancellation/timeouts nor arbitrary cross-thread or reconfiguration support.

## Sizing and existing contributions

The complete `transition` override, `setWindowFrame`, toolbar delegate extension and fitting-size calculation are byte-identical to upstream. This packet does not introduce a fallback for zero `fittingSize`, alter macOS availability checks, or change the existing animated/nonanimated sizing behavior.

[LYY435939/Settings PR #1](https://github.com/LYY435939/Settings/pull/1) was read at head `aa7ddc0e593e1f9af8cd9ad44937a9429c08b53c`, based on the same upstream commit. It is open and unmerged. Despite queue wording remaining in its body, its actual current one-file diff adds `contentSize(for:)` with layout, preferred-content-size and bounds fallbacks. Its source blob is `55d06fff4a9b10fe0b8d295d0466917a7d0f9119`. That sizing work remains a separate contribution. The serialization hunks end before the sizing code, so an integrator can preserve that fallback when composing the two source changes, with a fresh exact-base comparison.

All 12 issue comments were read, including the historical zero-fitting-size report and references to prior PR #28. This packet does not replace those authorship records. The separately named upstream PR #140 endpoint returned 404 once; that exact route remains unresolved and was not retried. The all-state upstream `author:woahwhattheheck` PR search returned no rows at qualification time; this is the observed query result, not an exhaustive absence claim.

## Validation and remaining delivery

Static preparation verified the transferred preimage against its exact Git blob. An independent parser applied the serialized four-hunk patch to all 244 preimage lines and reproduced the complete 262-line postimage exactly. Full-string comparisons confirmed that the transition override and sizing/delegate suffix remain unchanged. These are text/identity and source-reasoning checks. No Swift compiler, macOS application, native animation, build or test suite was run; no runtime success is asserted.

For integration, use the exact base above and `transitions.patch`, or replace the named production file with the complete postimage after confirming the current source identity. If the base has moved, compare the changed activation/completion functions and preserve legitimate sizing changes before applying. macOS behavior and actual upstream delivery remain follow-through work for the existing authorized carrier.

The current issue advertises $60, with historical funding comment [482094920](https://github.com/sindresorhus/Settings/issues/9#issuecomment-482094920). This records advertised funding only: eligibility, acceptance, award and payment are not established. No external maintainer contact, upstream PR, IssueHunt claim or account action was performed.

Internal work order: [BATCH06 row 10](https://tokenjunkielabs.slack.com/archives/C0BU51F1PL3/p1791174382674659). Operation: `SETTINGS9-SERIAL-TAB-TRANSITIONS-20261005-7CA6`; [source claim](https://tokenjunkielabs.slack.com/archives/C0BU51F1PL3/p1791175048028419).
