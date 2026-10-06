# Stellar Analysis mobile navigation: focus the first link

Opening the mounted mobile navigation schedules focus on `firstMobileLinkRef`. The current component assigns that same object ref to every link in its mobile map. The ref can identify only one anchor, so this does not reliably implement the source's explicit first-link intent. This continuation gives the existing ref only to map index zero; the first entry is the About link.

## Apply and source identity

Apply `first-mobile-link.patch` to `src/components/navbar.tsx` in [Stellar-Analysis/frontend](https://github.com/Stellar-Analysis/frontend) at commit `482ee456369418ef82c4056718cb82d3468f762b`, or compose its two changed lines with newer source. Do not replace a newer full component.

| Identity | Git blob |
| --- | --- |
| Original Navbar | `1d519697311060e2d72c1a8fcaa59d1eb6148277` |
| Patched Navbar | `74b64ddf57cdeb94f681e5c40403e4a0d20d2643` |

The change is +2/-2 in two hunks: name the existing map index and attach `firstMobileLinkRef` only when that index is zero. No additional ref, state, effect or dependency is introduced. The desktop map has no ref and is unchanged.

## Actual mounted caller and locale contract

The complete `src/app/[locale]/layout.tsx` (`1f016787657313d58504e79bccbe634a843ce8b5`) mounts `Sidebar` and `Navbar` directly inside `NextIntlClientProvider`. The separate `MainLayout`/`Header` source is not the caller used in that layout.

Navbar and Sidebar already import `Link` and `usePathname` from `src/i18n/navigation.ts` (`fd8ba9aa80bb0d0dd56eb76a3891caa0afe0c803`), which exports `createNavigation(routing)`. The patch retains those components, every href, translation key, route-change close effect and menu state.

React's [DOM-ref documentation](https://react.dev/learn/manipulating-the-dom-with-refs) explains that an object ref's current field receives its corresponding DOM node during commit, and demonstrates focusing the node held by that ref. Assigning one ref to multiple links does not give it a stable first-link identity. Restricting it to index zero establishes that identity directly in the existing rendered list. This is a source-based inference, not a browser observation.

The [next-intl navigation documentation](https://next-intl.dev/docs/routing/navigation) describes the locale-aware Next.js Link wrapper and the unprefixed pathname returned by its helper. No localization change is needed for this correction. The actual package manifest `2b1c6ac1f83096666c7fd6d5ba3fd22780e6b8eb` declares React 19.2.7, Next.js 16.2.10 and next-intl ^4.13.2; no installation, lock resolution or runtime compatibility claim is made.

## Attribution and contribution boundary

The original component and layout remain the work of the Stellar-Analysis/frontend contributors. The latest returned path-history entry is christabel888's repository-flattening commit [59fad72d9fbef9cfd6f47e215392da44488fcdc4](https://github.com/Stellar-Analysis/frontend/commit/59fad72d9fbef9cfd6f47e215392da44488fcdc4); it records moving the prior frontend directory into the repository root. That is not evidence that this author originally wrote the focus-ref hunk.

The root README `a7546f7a6f85709fccd21e136cd8b12bae820652` was read fully; its package-manager and development guidance remain intact. The retained complete repository tree has 959 entries, is not truncated, and contains no AGENTS.md or RULES.md paths. The complete docs/CONTRIBUTING.md (`f66db3b0eece27eb6fa888948c31ee8c7eabcfd2`) was transferred from retained source and independently hash-matched; its heading and release commands are specifically for EventSource. This source-only UI patch is not that release workflow; no tests or npm publication are performed. Differently attributed MIT notices in documentation are not treated as a repository-wide license grant. This packet contains only a minimal contextual patch and this original guide, not a copy of the full source module or a relicensed document.

The bounded repository-local PR search for navbar returned zero with incomplete_results false; the explicit public Slack query for Stellar-Analysis plus navbar returned zero and native END. These are bounded observations, not a complete contribution census. An earlier keywords-only Slack response rendered an empty query and is not used as absence evidence. No dedicated upstream issue assignment or reward is claimed.

## Validation and limits

Complete actual Navbar, mounted locale layout, navigation helper, Sidebar, separate MainLayout/Header, README and manifest were inspected. The original source's native blob and independently calculated Git blob match; the patch's exact forward construction and reverse reconstruction are retained. Published artifact content and immutable Git identities are checked on the Commons carrier.

No app, browser, focus interaction, accessibility suite, build, lint, package install or test was run. This does not add a focus trap, restore focus to the menu button, cancel the existing focus timer, redesign breakpoint/scroll behavior, or establish full keyboard/menu accessibility. All such existing behavior is left as source. No upstream branch, issue, PR, assignment, sponsor or payment action is performed.
