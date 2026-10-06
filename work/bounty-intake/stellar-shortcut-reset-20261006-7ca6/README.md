# Restore default keyboard-shortcut inheritance

This packet fixes the existing per-row Reset to default control in Stellar-Analysis/frontend. The handler already copies customBindings and removes the selected ID, but then discards that copy and calls customizeBinding with the current default. That call writes an explicit custom override back into the map. The row consequently still displays Custom and continues to use the saved override if the registered default changes.

The patch submits the already prepared map through the existing setConfig API. It removes one override instead of persisting a snapshot of the default. Existing display and dispatch fallback expressions then select the registered default naturally.

## Exact source and attribution

The original implementation belongs to the Stellar-Analysis/frontend contributors. This is an attributed, source-only continuation over current main, not an upstream submission or a claim to the keyboard-shortcut feature.

- Repository: https://github.com/Stellar-Analysis/frontend
- Donor commit: `482ee456369418ef82c4056718cb82d3468f762b`
- Production path: `src/components/keyboard-shortcuts/ShortcutCustomizer.tsx`
- Original blob: `01c2e31cfe334ca54b89b66a35b117dd6357be04` (9,265 UTF-8 bytes)
- Patched blob: `9bbb50c6358840a85745c8eabc0b2d22c90647ad` (9,236 UTF-8 bytes)
- Patch: `reset-custom-binding.patch`
- Production diff: two hunks, +2/-1
- Modification date: 2026-10-06

The complete component and context were read as actual pinned source and independently matched their Git blob identities. A fresh donor-ref read still returned the donor commit before preparation. No external PR number is asserted for this direct-main continuation. A bounded current upstream PR search for shortcut returned two closed wallet-route proposals, neither about this control; the exact ShortcutCustomizer Commons PR query and public Slack query each returned no match. Those bounded searches do not prove a global absence of other work.

## Connected source contract

The retained `src/app/[locale]/settings/page.tsx` (blob `7c8c98e8f38bc8b1bfec45e753381deac1d7f353`) renders ShortcutCustomizer without a categories filter. The retained locale layout `src/app/[locale]/layout.tsx` (blob `1f016787657313d58504e79bccbe634a843ce8b5`) mounts KeyboardShortcutsProvider around this route. These actual callers distinguish this control from unused layout alternatives.

The complete `src/contexts/KeyboardShortcutsContext.tsx` (blob `e43badc17f6c0e374e0fac5e08a96a5496b87bd7`) exposes setConfig for Partial<ShortcutConfig>. Its implementation passes a functional updater to the existing local-storage hook and merges the previous top-level configuration with that partial update. Passing only customBindings therefore preserves enabled and disabledShortcuts.

The component renders Custom and the individual reset button from the presence of config.customBindings[id]. Both its binding display and the provider's keydown dispatch use the custom binding when present, otherwise action.defaultBinding. Deleting the override is therefore the supported reset representation. No new context method or persistence key is introduced.

## Narrow change

Destructure the existing setConfig from useKeyboardShortcuts. In resetShortcut, keep the current shallow copy and deletion, then call setConfig with that map. Leave customizeBinding for ordinary saved edits. Other custom entries, toggles, Reset All, recording, conflict checks, platform matching, registry behavior and keyboard dispatch are unchanged.

This preserves the existing rendered-snapshot update pattern for customBindings. It does not add cross-tab serialization or atomic merging of simultaneous binding edits. The existing storage hook's persistence and error behavior remain in force; a source correction is not proof that storage succeeded on a device. Category-filter conflict checking, recording focus/Tab behavior, accessibility completeness and browser-reserved key handling are outside this patch.

## Integration

Apply `reset-custom-binding.patch` to the exact donor component, or compose these two hunks into a newer component after checking its actual setter contract. Preserve newer source. The context, provider, settings and layout files are inputs only and are not replaced by this packet.

The earlier Commons Navbar, sidebar, locale, pagination, appearance and PWA continuations touch other source paths and remain independently attributed. This packet neither revalidates nor changes their artifacts.

## Instructions and validation boundary

The complete retained donor tree contained no AGENTS or RULES path. The observed `docs/CONTRIBUTING.md` blob `f66db3b0eece27eb6fa888948c31ee8c7eabcfd2` is headed Contributing to EventSource and includes test/release commands. No EventSource release is performed. The current authorized session excludes runtime, tests, browser/device actions and upstream publication.

No repository-wide license scope was established from the differently attributed documentation notices. Only a minimal patch and this original integration guide are published; no complete donor module or documentation is republished.

Source checks: full input identities, complete literal diff coverage, exact reverse reconstruction and independent postimage identity. Publication checks compare the complete patch and guide at the immutable Commons head and merge, inspect changed paths and parent identities, and compare the final named main. If named main equals the checked merge, those immutable checks serve that exact identity; otherwise full artifact reads at the observed later main are required. This is a predeclared read plan, not a claim that publication has already succeeded.

No application code, classifier, fixture, tests, build or browser ran. No upstream branch, issue, comment, account, key, transaction or payment was changed. No runtime, accessibility, upstream acceptance, assignment, bounty or payment claim is made.
