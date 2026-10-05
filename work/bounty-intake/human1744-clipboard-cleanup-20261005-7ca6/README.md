# Comment clipboard fallback cleanup

## Outcome and original contribution

This packet continues [AugmentSecurity's external Human-Connection PR 4560](https://github.com/Human-Connection/Human-Connection/pull/4560), pinned at `54aba061f1de63280da28c0a09df60eacd271562`. That author supplies the Copy link menu action, comment anchors, absolute links, clipboard handling, success/error toasts, localized messages and component coverage. Those features are already present in the external contribution.

The additional change is a single **+7/-5** hunk in `webapp/components/ContentMenu/ContentMenu.vue`. It puts the temporary textarea's removal in a finally block surrounding the existing fallback selection and copy operation. The complete modified component, its focused diff and the original MIT license are included.

This is a source lifecycle correction. No particular browser exception, observed leak, exception frequency or live clipboard failure is asserted.

## Why the cleanup placement matters

The fallback appends a textarea, selects its text, calls the existing copy command and then removes the element. In the original source, an abrupt completion during selection or copying skips the removal statement. The calling `copyResourceLink()` catches errors and displays the existing error toast, but that catch does not remove the temporary element.

The patch moves the same removal operation into finally. It is therefore attempted after normal copying, an unavailable/false copy result, or an exception from the protected operations. When removal succeeds, any original error continues to the existing toast handler. A failure in removal itself is not separately handled by this patch.

The modern `navigator.clipboard.writeText` branch remains byte-for-byte unchanged and returns before any temporary element is created. This change adds no clipboard API, permission request, polling, asynchronous fallback or extra copy attempt. It does not alter the copied URL, comment anchor, ownership controls, menu actions, translations or toast messages.

## Issue chronology and source scope

[Issue 1744](https://github.com/Human-Connection/Human-Connection/issues/1744) originally suggested clicking comment dates. Its full four-comment chronology includes collaborator [581410339](https://github.com/Human-Connection/Human-Connection/issues/1744#issuecomment-581410339), which changes the requested design to a Copy link content-menu action with clipboard success/error toasts. PR 4560 already follows that updated direction; this packet does not claim to originate or complete the overall feature.

The issue was open and unassigned in the observed record, with a historical EUR 30 label. The contribution guide requires a prior free approved-and-merged contribution before bounty participation, upstream coordination, tests and independent review. No current eligibility, assignment, funding, bounty claim, invoice or payment conclusion is made. Those upstream conditions are not fulfilled by publishing this separate Commons source packet.

The external PR was open and unmerged, with zero discussion or review comments. Its complete 14-path changed-file response was retained and read, including the author's existing test changes. The PR's listed execution commands are historical author statements, not runs performed for this packet. The actual component is retained in full; this is not a review of every application source file.

| Source | Exact identity |
| --- | --- |
| External PR head | `54aba061f1de63280da28c0a09df60eacd271562` |
| Original PR base and sole parent | `72a8f3d7f567442ca5e191672abfb47ea1b825a6` |
| Complete source tree | `d038ea2a13f8e1377c52f460ccdc741c2a89980b` |
| Original ContentMenu component, 8,113 bytes | `8f2e10309e4016bb668fde78834be500f1bac69f` |
| Modified ContentMenu component, 8,158 bytes | `1724537ec251dad22d818eda8bbdd50270dd2f8c` |
| Original CommentCard component, changed-path record | `18108f3e197ed23c78c409d0c88b4fa2d621bcb0` |
| Original CommentList component, changed-path record | `9d05fa28325832fb2c94850dbe6e6e4e35898e24` |
| Contribution guide | `ae1150aa6eba6b747a06a58202635df586c55424` |
| Original MIT license | `646ae3a6d4eb43273146cf8fef10819c14a82958` |
| Webapp package metadata | `eff2adfc37f68b8b967c8997e969aa07c7677f8f` |
| Root README | `998f722f0f8a4128b26268262437061c5215b080` |

The full recursive tree had 1,184 entries and `truncated: false`. It contained the root contribution guide and license, with no AGENTS file or nested contribution/license file governing this component. The README, contribution guide, license and webapp package metadata were read. Public demo account data from the README is not copied or used.

Primary sources:

- [Pinned ContentMenu component](https://github.com/Human-Connection/Human-Connection/blob/54aba061f1de63280da28c0a09df60eacd271562/webapp/components/ContentMenu/ContentMenu.vue)
- [Pinned contribution guide](https://github.com/Human-Connection/Human-Connection/blob/54aba061f1de63280da28c0a09df60eacd271562/CONTRIBUTING.md)
- [Pinned license](https://github.com/Human-Connection/Human-Connection/blob/54aba061f1de63280da28c0a09df60eacd271562/LICENSE.md)
- [Pinned package metadata](https://github.com/Human-Connection/Human-Connection/blob/54aba061f1de63280da28c0a09df60eacd271562/webapp/package.json)

## Application and validation

`clipboard-cleanup.patch` targets the exact external component preimage above. The serialized unified diff itself was parsed: header path, hunk start/counts, and every context/removal row matched the full preimage, and applying it yielded the exact complete postimage. Native source identity matched an independent Git blob calculation. All bytes outside the single replacement block are preserved, including the full modern clipboard branch.

No browser, application, clipboard, dependency installation, test suite, workflow, account or external contribution was executed or changed. No upstream approval, full issue completion, browser compatibility, focus restoration or successful live copy is claimed. The packet does not carry the external PR's other changed source, locales or tests; composing it requires that pinned contribution or a separately reviewed adaptation.

The narrow Commons PR query returned no matches with `incomplete_results: false`. The bounded public Slack query returned an empty rendering and provider end; query application was not independently established. These checks are coordination evidence, not universal clearance.

## Attribution and license

The original repository's MIT license identifies Human-Connection gGmbH, 2018. Its complete `LICENSE.md` is copied unchanged into this packet. AugmentSecurity retains credit for the comment-copy feature and the original fallback implementation. This packet adds only the cleanup placement described above.
