# Preserve URL state when changing language

The mounted language switcher replaces only the locale-stripped pathname. The current Corridors page uses the shared pagination hook, which reads `page` and `pageSize` from the query string and writes both into the URL. Selecting another language therefore discards pagination state and makes that hook use its defaults.

This source-only continuation captures the current query string and fragment in the existing click handler, appends them to the existing locale-stripped pathname, and passes that URL to the same locale-aware `router.replace` call. The locale choice, transition, preference update, cookie assignment, button labels, pending state, and route policy remain unchanged.

## Pinned production input

Repository: [Stellar-Analysis/frontend](https://github.com/Stellar-Analysis/frontend)  
Source revision: `482ee456369418ef82c4056718cb82d3468f762b`

| Source | Git blob | Role |
|---|---|---|
| [src/components/LanguageSwitcher.tsx](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/src/components/LanguageSwitcher.tsx) | `9d4e773e7230ed8eeee19604fca16c10e6a26835` | Complete edited source |
| [src/app/[locale]/layout.tsx](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/src/app/%5Blocale%5D/layout.tsx) | `1f016787657313d58504e79bccbe634a843ce8b5` | Mounts preference provider and Sidebar |
| [src/components/layout/sidebar.tsx](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/src/components/layout/sidebar.tsx) | `9b11a0dc39150a9d60f28b68071f1b336aff38ab` | Mounts LanguageSwitcher while expanded |
| [src/contexts/UserPreferencesContext.tsx](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/src/contexts/UserPreferencesContext.tsx) | `1f22b6a9354ebacf502df2472ddeb24e0006a4e6` | Existing preference storage interface |
| [src/i18n/navigation.ts](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/src/i18n/navigation.ts) | `fd8ba9aa80bb0d0dd56eb76a3891caa0afe0c803` | Existing createNavigation wrapper |
| [src/i18n/routing.ts](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/src/i18n/routing.ts) | `7a1c19fa17133fa33179f3381d115f8d2ee542f7` | en/es/zh, always-prefixed locales; no pathnames templates |
| [src/app/[locale]/corridors/page.tsx](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/src/app/%5Blocale%5D/corridors/page.tsx) | `a14fe86977c4071ad958ddc3f206b4f07134b072` | Actual mounted pagination consumer; relevant caller sections inspected |
| [src/hooks/usePagination.ts](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/src/hooks/usePagination.ts) | `e3e27c92a59f856545fc846c73d4f41226dd9e23` | Complete query reader/writer |

Production change: one file, +2/-1. Resulting LanguageSwitcher blob: `5aa7952aa65a5041e9f0bade99798a48a3002e9a`.

## Why this construction matches the current contract

The current routing configuration does not use localized pathname templates. The existing `usePathname` wrapper supplies the resolved pathname without its locale prefix. The existing pagination hook already passes a pathname-plus-query string to the same router wrapper.

The new handler reads `window.location.search` and `window.location.hash` synchronously after the unchanged same-locale guard, before entering the existing transition. Browser access is limited to the click handler, which already writes `document.cookie`; rendering gains no new browser access, hook, effect, or Suspense requirement. Query pairs are not parsed, decoded, reordered, or collapsed by this correction, so repeated query keys stay represented in the forwarded string. An absent query or fragment contributes the corresponding empty string. This is URL forwarding, not a claim that every destination consumes every parameter or contains a matching anchor.

Primary contracts read on 2026-10-06:
- [next-intl navigation](https://next-intl.dev/docs/routing/navigation): locale-aware router wrappers, locale override, pathname without locale prefix, and string URLs when no pathnames map is configured.
- [MDN Location.search](https://developer.mozilla.org/en-US/docs/Web/API/Location/search): query string includes its leading question mark when present and is not percent-decoded on read.
- [MDN Location.hash](https://developer.mozilla.org/en-US/docs/Web/API/Location/hash): fragment includes its leading hash when present.

These documents establish API semantics; they do not establish installed-package execution or a browser result.

## Apply and compose

Apply `language-switch-url-state.patch` only to the named source preimage, or manually compose its two changed lines with a newer source after reviewing that source. Do not replace a newer full module.

This packet changes only LanguageSwitcher. It composes independently with the completed [Navbar first-link correction](https://github.com/woahwhattheheck/commons/pull/31835) and [sidebar layout-offset correction](https://github.com/woahwhattheheck/commons/pull/31848); their source paths and behavior are not revalidated or modified here. Original upstream implementation and contributor credit remain with Stellar-Analysis/frontend. No original language-switching or pagination feature is claimed as newly authored.

## Scope and evidence

The complete edited source, routing and navigation wrappers, preference source, Sidebar and locale layout, and complete pagination hook were read. The Corridors file was retained in full and its relevant imports, hook call, and pagination controls were inspected. The complete storage hook was also read during qualification; its cross-tab removal and broader persistence behavior are outside this patch.

A precise public Slack query for Stellar-Analysis and LanguageSwitcher returned zero results/native END. One repository-local PR query for locale returned 28 records, all closed, with complete header projection and no LanguageSwitcher/user-preference/language-switch match in the retained bodies. This is bounded chronology, not proof that no other contribution exists. An initial broad body projection exceeded the display budget; the raw response was retained and the complete header inventory was projected from it without another provider request. No historical test claim was rerun or adopted.

The current source tree has no AGENTS/RULES paths. Its retained docs/CONTRIBUTING.md (`f66db3b0eece27eb6fa888948c31ee8c7eabcfd2`) contains EventSource-specific test/release instructions; this task authorizes neither tests nor package publication. No applicable repository-wide license was established from the differently attributed documentation notices, so the packet contains only a minimal contextual patch and this original guide, not a full source-module copy.

Validation is limited to complete source inspection, independent Git blob identities, exact forward/reverse text reconstruction, and publication readbacks. No application, browser, routing transition, storage/cookie operation, installation, TypeScript build, lint, synthetic test, or accessibility run was performed. No upstream branch/PR/comment, issue acceptance, assignment, reward, or payment action was taken. Existing held routes and author/maintainer conditions remain in force. This does not repair cross-tab preference reset, storage failure, navigation failure, unsaved form state, pagination validation, or language availability on mobile/collapsed Sidebar.
