# Restore saved appearance in the mounted preferences provider

A saved accent or text-size choice was read into preferences and displayed by the settings controls, but only the settings click handlers applied it to the document. A new document could therefore retain the choice without its CSS effects. This contextual patch moves the existing preset tables into the mounted UserPreferencesProvider module and reapplies a supported saved choice after client commit.

## Source and attribution

- Repository: https://github.com/Stellar-Analysis/frontend
- Immutable source: `482ee456369418ef82c4056718cb82d3468f762b`.
- This is a narrow continuation of the repository contributors' existing preference storage and customization implementation. It does not replace their authorship, identify a new bounty claimant, or claim the whole settings feature.
- It is current-main work, not a mutation of an external contributor PR. The precise public PR search for `repo:Stellar-Analysis/frontend is:pr "ThemeCustomizer"` returned zero records with incomplete_results=false. That bounded search is not a complete contributor census.
- The separate public Slack search for the exact repository name and ThemeCustomizer returned zero/native END. Root's retained completion inventory contains no known restoration carrier; the already delivered CSS consumer explicitly excluded restoration.
- The source-main guard still named the immutable source above before this work was published.

| Production path | Exact preimage blob | Intended postimage blob |
| --- | --- | --- |
| src/contexts/UserPreferencesContext.tsx | 1f22b6a9354ebacf502df2472ddeb24e0006a4e6 | 73d3d88093bd63cc98782e3d667df0d1e03b4998 |
| src/components/ThemeCustomizer.tsx | 00dff98f1f0e609897b5e725a2159bb544139887 | 9e16f102630fce41af928e0dab3bac194f917690 |

Production delta: +44/-23 across these two files, including moving the existing preset declarations. `saved-appearance.patch` contains the full contextual change. Apply it to these exact preimages or compose its hunks with newer source; do not overwrite newer modules with an old full copy.

## Actual connected source

The locale layout, blob `1f016787657313d58504e79bccbe634a843ce8b5`, mounts UserPreferencesProvider around its routes. The settings page, blob `7c8c98e8f38bc8b1bfec45e753381deac1d7f353`, mounts ThemeCustomizer. The provider merges stored preferences into defaults; the existing useLocalStorage hook, blob `96720ed34bd96b3e6aa8e441b97ce8d5d710d791`, reads the existing `stellar-user-prefs` JSON in its client state initializer and propagates non-null storage updates.

The complete customizer has six accent choices and three text sizes. Its click handlers set `--accent`, or `--base-font-size` and `data-font-size`, then merge the selected choice into stored preferences. The original provider and ThemeContext have no corresponding appearance restoration. ThemeContext's light/dark/system synchronization is a separate existing behavior and remains untouched.

## Change

- Export the same six accent presets and the same Small/Default/Large entries from the already imported preferences module. ThemeCustomizer imports these declarations, so display controls and restoration use one set of values.
- Add optional typed `accentColor` and `fontSize` fields to UserPreferences. Do not add defaults that would force a previously absent choice onto the document.
- Add one provider effect dependent on the two appearance values. It looks up each value in the existing preset table and applies only a found preset to the root.
- Keep the customizer's click handlers, persistence operation, theme controls and rendered controls unchanged. Replace its two unchecked preference-read casts with the now-declared optional fields.

The supported accent values remain #6366f1, #8b5cf6, #0ea5e9, #10b981, #f43f5e and #f59e0b. Text sizes remain sm=13px, md=14px and lg=16px. This patch introduces no arbitrary stored CSS interpretation or new appearance choices.

## Timing and lifecycle boundary

The effect runs after a client commit and again when a supported value changes in the existing preference state. It does not run during server rendering and is not a pre-paint restoration mechanism. A brief initial default appearance remains possible. The existing local-storage initialization and hydration behavior are not rewritten.

No cleanup removes the global preference when this provider unmounts: the existing click handlers already leave those root values in place, and route/settings teardown should not undo a selected appearance. The effect only performs repeatable assignments of the selected values; it registers no timer or listener. This is one mounted application provider, not a guarantee for competing providers controlling the same root.

Absent or unsupported persisted choices produce no root write. They do not actively clear an earlier inline value. Reset/removal synchronization, cross-tab clear events and malformed preference-schema repair remain outside this patch; the current settings source has no reset control. Existing non-null storage updates can cause supported choices to be reapplied through the same effect, without a new storage listener.

## Composition

https://github.com/woahwhattheheck/commons/pull/31859 supplies the distinct root-font-size CSS consumer. Compose its exact `text-size-css-consumer.patch` for the saved text-size variable to affect rem-based text and layout. This patch does not duplicate or alter that CSS change. It is also disjoint from the completed sidebar offset, navbar focus, locale URL-state and pagination patches.

The current CSS already consumes the accent custom property. This work does not promise that every hard-coded accent or pixel-sized element changes. Contrast, browser preferences, reduced motion, responsive layouts and broad accessibility acceptance are not asserted.

## Primary contracts and source-only checks

- React useEffect: https://react.dev/reference/react/useEffect — client-only setup after commit, reruns for changed dependencies; it is not a server-render or no-flash guarantee.
- CSSStyleDeclaration.setProperty: https://developer.mozilla.org/en-US/docs/Web/API/CSSStyleDeclaration/setProperty — assigning the existing root custom properties.

The two complete immutable source bodies were already retained as inputs to this new correction; their Git blob hashes matched independently before editing. Both contextual patches reconstructed the intended complete postimages exactly. The existing click-handler range remained byte-for-byte identical. These are source-construction checks, not TypeScript compilation, browser behavior, tests, storage access or runtime validation.

The complete repository tree had no AGENTS/RULES path. Its docs/CONTRIBUTING.md is specifically EventSource release guidance (blob `f66db3b0eece27eb6fa888948c31ee8c7eabcfd2`); no EventSource release, npm publication or test work was performed. Three differently attributed license notices under docs do not establish a repository-wide license for these modules. This Commons package therefore contains a minimal contextual patch and this original guide, not republished full production modules or an inferred license.

No upstream branch, issue or review was changed. No account, credential, browser, storage, wallet, network transaction, runtime or test action was performed. No upstream acceptance, assignment, reward, award or payment is claimed. Existing exact failed provider routes remain held.

Operation: STELLAR-SAVED-APPEARANCE-20261006-7CA6.
