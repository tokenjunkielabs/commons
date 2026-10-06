# Native keyboard-shortcut edit trigger

This follow-on makes the existing shortcut-edit action a native button. In the pinned component, a kbd element has an onClick handler but no tabIndex, keyboard handler or button role. The enabled editing action therefore has no native keyboard-focus/activation control of its own. A kbd label is still useful for displaying a key binding, so it becomes the button's child.

The same onClick expression still starts the same recorder. The new button explicitly has type=button, disabled follows the existing disabled-shortcut state, and its accessible name identifies both the action and the current displayed binding. Existing presentation classes are retained on the button with a focus-visible ring. This fixes the edit-entry control only; it is not a full accessibility or recording-workflow acceptance claim.

## Source lineage and composition

- Original repository: https://github.com/Stellar-Analysis/frontend
- Original donor commit: `482ee456369418ef82c4056718cb82d3468f762b`
- Production path: `src/components/keyboard-shortcuts/ShortcutCustomizer.tsx`
- Original upstream blob: `01c2e31cfe334ca54b89b66a35b117dd6357be04`
- Required local predecessor: https://github.com/woahwhattheheck/commons/pull/31916
- Predecessor merge: `86011ed4099bf178c0c87be9dac03ee867517a03`
- Predecessor patch: `reset-custom-binding.patch`, Git blob `275bb932521de8e2322d1497676ec5307e93fe51`
- This patch's exact preimage: `9bbb50c6358840a85745c8eabc0b2d22c90647ad`, 9,236 UTF-8 bytes
- This patch's exact postimage: `c309d4b2f5af4125eaa801d0b40661cce4447f41`, 9,491 UTF-8 bytes
- Incremental patch: `keyboard-edit-trigger.patch`, one hunk, +7/-4
- Modification date: 2026-10-06

The preimage is the retained source postimage prepared for 31916, not a claim that the upstream main contains that change. Apply reset-custom-binding.patch first, then keyboard-edit-trigger.patch. Both resulting source changes compose in one module. For a newer source version, integrate the actual reset and edit-control hunks after inspecting that version; do not overwrite unrelated changes.

Original implementation credit remains with Stellar-Analysis/frontend contributors. No upstream source PR is claimed for this direct-main continuation. Existing author, assignment and acceptance rights are unchanged. The prior packet's patch and README are preserved byte for byte; this publication adds only the incremental patch and this guide.

## Actual mounted consumer and handler contract

The already read settings page `src/app/[locale]/settings/page.tsx`, blob `7c8c98e8f38bc8b1bfec45e753381deac1d7f353`, mounts ShortcutCustomizer without a category filter. The locale layout blob `1f016787657313d58504e79bccbe634a843ce8b5` mounts KeyboardShortcutsProvider around that route.

The complete context `src/contexts/KeyboardShortcutsContext.tsx`, blob `e43badc17f6c0e374e0fac5e08a96a5496b87bd7`, supplies the same shortcut list, configuration and dispatch behavior. The trigger's existing startRecording sets the editing ID, clears the recorded binding/error and schedules focus on the existing recording input. None of those statements changes.

The new button is unavailable when the shortcut is disabled, matching the previous guarded onClick intent. The displayed binding remains the exact formatBinding(binding, platform) result. The accessible name includes that same display string plus the shortcut name and edit action. No new keydown handler duplicates native activation, and type=button avoids accidental form submission if the component is embedded in a form.

## Primary browser/accessibility contracts

Read on 2026-10-06:

- W3C WAI Button Pattern: https://www.w3.org/WAI/ARIA/apg/patterns/button/
  Describes action buttons, accessible names and Enter/Space activation when focused.
- MDN button element: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/button
  Documents native activation, disabled interaction and the non-submit button type.

These sources support the native-element choice. They are not evidence of this application's browser, assistive-technology or visual behavior being exercised.

## Exact limits

The existing recording effect captures document keydown events and prevents their default handling while editing. This patch does not change its Tab capture, reserved-key policy, save/cancel keyboard navigation, focus restoration, timer cleanup or stale scheduled focus. The provider's existing global shortcut interception also stays exact. Consequently the claim is a semantic, focusable edit-entry control, not completion of the entire keyboard customization flow.

No shortcut value, conflict rule, category filter, persistence API, reset behavior, registry action, locale, routing, theme or PWA logic changes. Native disabled controls leave the focus order while disabled; the existing enabled checkbox remains the way to enable that shortcut. Browser rendering, target size, focus-ring contrast and assistive-technology presentation were not evaluated.

## Instructions, packaging and checks

The retained complete donor tree has no AGENTS or RULES path. Its `docs/CONTRIBUTING.md` blob `f66db3b0eece27eb6fa888948c31ee8c7eabcfd2` is EventSource-specific test/release guidance. Current authorization excludes runtime, tests, browser/device actions and upstream publication. No repository-wide license is inferred from differently attributed documentation notices; this packet contains only a minimal patch and original guide.

A new donor main read still returned the pinned commit. The current public ShortcutCustomizer chronology query returned no matches; earlier bounded source-carrier searches found no matching edit-control carrier. Neither search establishes a repository-wide absence of other work.

Checks are source-only: exact retained preimage identity, one complete literal diff, forward and reverse text reconstruction, independently computed postimage hash, and confirmation that the reset correction remains in the composed source. Publication uses full patch/guide reads at the new immutable head and merge, exact changed-path/parent metadata, and the final named main reference. If named main equals the checked merge, those immutable reads cover that identical tree; a different later main requires complete artifact reads at its actual identity.

No application code, fixture, test, build, workflow or browser was executed. No upstream PR/comment, account, key, wallet, transaction, award or payment action was performed.
