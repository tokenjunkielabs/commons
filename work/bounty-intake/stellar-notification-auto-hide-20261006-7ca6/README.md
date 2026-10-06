# Honor Auto Hide in the mounted in-app toast renderer

Turning off the saved Auto Hide preference currently leaves both automatic removal mechanisms active: each nonpersistent toast schedules dismissal, and NotificationSystem excludes nonpersistent records after 30 seconds. This patch makes the existing preference govern those two in-app presentation paths.

## Exact source and attribution

Source repository: https://github.com/Stellar-Analysis/frontend

Donor main and patch base: `482ee456369418ef82c4056718cb82d3468f762b`. A new main-ref read for this task returned that same commit. This is a narrow continuation of the existing Stellar-Analysis contributors' notification implementation. No external PR is being replaced, submitted, claimed, or described as accepted.

| Source path | Donor Git blob | Role |
| --- | --- | --- |
| `src/components/notifications/NotificationSystem.tsx` | `749f53329262d19055229fa8c096c9a6562bc8f5` | Production patch target |
| `src/components/notifications/Toast.tsx` | `6a2a62d02b3327743045906c020d645c63357a18` | Existing persistent flag disables its dismissal timer and progress bar |
| `src/components/notifications/ToastContainer.tsx` | `dbd32c68115de137d110af405885d0e457f6792a` | Passes mapped notifications to Toast; retains priority ordering and cap |
| `src/contexts/NotificationContext.tsx` | `8a05dbf6fb720af3f876baef6b14f035d02b6c51` | Stores preferences and notifications; merges saved preferences |
| `src/types/notifications.ts` | `ab97b18fd0e9c78562181659141660e8a92c21ec` | Declares autoHide:boolean and optional persistent |
| `src/components/notifications/NotificationPreferences.tsx` | `fd1482e38a34d706b675e6a2038e57101e4a3ffc` | Actual Auto Hide toggle and Save control |
| `src/components/notifications/NotificationBell.tsx` | `8e17fc08741d51bda9d0b3169a4b563fd528e89b` | Opens the preference controls |
| `src/components/notifications/index.ts` | `812d23234012d75770a798e7ad4f6c7be77b1e58` | Resolves the Navbar's NotificationBell import |
| `src/components/navbar.tsx` | `1d519697311060e2d72c1a8fcaa59d1eb6148277` | Mounted notification-menu consumer |
| `src/app/[locale]/layout.tsx` | `1f016787657313d58504e79bccbe634a843ce8b5` | Previously retained mount of provider, Navbar and NotificationSystem |

The complete newly needed modules were read as source, including the barrel. The locale-layout mount is reused retained evidence. The separate notification demo page was identified as a demo; its alert actions are not the basis for this change. A public Slack search for the exact NotificationSystem symbol and two bounded repository PR searches (autoHide, and notification in title) returned no matching carrier; these observations are not repository-wide absence or maintainer-selection claims.

## Change

`respect-auto-hide.patch` changes only NotificationSystem, one hunk, +4/-3:

- With Auto Hide disabled, the age predicate admits retained notification records without applying its 30-second cutoff.
- Each displayed copy derives `persistent` from the record's existing persistent value or the disabled Auto Hide preference. The existing Toast effect consequently does not schedule its ordinary timer, and its progress bar is suppressed.
- The memo depends on autoHide so saving a changed preference updates that presentation.

No context record is mutated. Explicitly persistent records remain persistent. Auto Hide enabled retains the original age cutoff and configured delay. Manual dismiss buttons, priority/date sorting, five-toast display cap, provider history retention, IDs, contents, categories, sound and transport remain as implemented.

The setting does not promise that every historical notification is simultaneously visible: the existing cap and sorting still apply. Disabling Auto Hide may make retained older records eligible for presentation; this follows directly from removing the age cutoff under that preference. Turning it back on restores the original cutoff and timed behavior. A toast whose existing dismissal callback has already begun its exit transition is not resurrected and its queued 300ms removal is not cancelled by this patch. Desktop-notification behavior is separate and unchanged.

## Applying and composing

Apply the patch to the exact donor source above. The production preimage is 1,831 UTF-8 bytes, blob `749f53329262d19055229fa8c096c9a6562bc8f5`; the postimage is 1,932 bytes, blob `65831bbd1e5083f27ff0e5ec542109f006c9164f`. Both preserve the original absence of a final newline and file mode 100644.

Inspect and compose with newer upstream work rather than replacing a newer module. This target is disjoint from the completed Navbar, locale forwarding, sidebar, preferences appearance, pagination, shortcut, PWA, offline-hook and API-header packets. It does not replace those changes. No other source module is included or edited.

## Source inspection and limits

The complete literal source edit and its inverse reconstruct the stated production identities. The complete serialized unified hunk is retained in the patch. These are string/source integrity checks, not TypeScript compilation, application execution, timers exercised against a fake clock, synthetic fixtures, UI tests or browser observation. No notification, sound, permission prompt, network event or storage operation was performed.

This correction uses the declared valid boolean preference and existing Toast contract. It adds no persisted-state migration or malformed-preference normalization; it does not fix custom per-toast duration propagation, action callbacks, already-started exit transitions, provider history cleanup, desktop dismissal or broader accessibility behavior. No runtime, device, full-feature, sponsor, bounty, payment, approval or upstream acceptance claim is made.

## Instructions and distribution boundary

The retained complete donor tree had no AGENTS.md or RULES.md. Its observed `docs/CONTRIBUTING.md` (`f66db3b0eece27eb6fa888948c31ee8c7eabcfd2`) contains EventSource-specific release/test guidance; this is not an EventSource release. Current task instructions prohibit tests, runtime and package publication, so none was performed.

The differently attributed MIT notices under donor documentation do not establish repository-wide licensing for these production modules. This Commons packet contains only the focused patch and this original integration guide, not a full republished source module. Original contributor ownership, external contribution conditions and any future upstream review remain with the source project.
