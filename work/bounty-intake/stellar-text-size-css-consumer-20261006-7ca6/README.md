# Connect the existing Text Size control to root font sizing

The current Settings page mounts ThemeCustomizer. Its Small, Default and Large buttons call an existing handler that writes `--base-font-size` on the document root using the corresponding 13px, 14px and 16px presets. The only stylesheet in the retained complete source tree never consumes this variable or the accompanying `data-font-size` attribute. Clicking a choice updates its selected indicator and stored preference, but the variable has no font-sizing consumer.

This minimal source continuation adds one `html` rule:

```css
html {
  font-size: var(--base-font-size, 100%);
}
```

The existing explicit choice can then determine the root font size and sizes expressed in rem. With no custom value, 100% retains the browser-relative default rather than forcing a new fixed default. The rule precedes the existing body styles and print block; the later print `html, body` rule still sets 11pt with equal selector specificity. Existing preset values, event handlers and storage behavior remain unchanged.

## Exact source and caller custody

Repository: [Stellar-Analysis/frontend](https://github.com/Stellar-Analysis/frontend)  
Revision: `482ee456369418ef82c4056718cb82d3468f762b`

| Source path | Git blob | Evidence |
|---|---|---|
| `src/app/globals.css` | `a203da3d12c8a8b625ecf8c1e5253f4d3f42dfd5` | Complete retained stylesheet; edited input |
| `src/app/layout.tsx` | `d99613766c48f2be30014720edd01dc156d58696` | Imports globals.css |
| `src/app/[locale]/settings/page.tsx` | `7c8c98e8f38bc8b1bfec45e753381deac1d7f353` | Complete current caller mounts ThemeCustomizer |
| `src/components/ThemeCustomizer.tsx` | `00dff98f1f0e609897b5e725a2159bb544139887` | Complete actual presets, buttons and property writer |
| `src/contexts/ThemeContext.tsx` | `2c5d5fd59feb0d24c2d675b9e4ac97e6df6537ea` | Complete light/dark/system provider; does not apply text-size preferences |
| `src/contexts/UserPreferencesContext.tsx` | `1f22b6a9354ebacf502df2472ddeb24e0006a4e6` | Existing stored preference interface |
| `src/app/[locale]/layout.tsx` | `1f016787657313d58504e79bccbe634a843ce8b5` | Mounts the theme and preference providers |

The four-line addition changes only `src/app/globals.css` (+4/-0). Applied directly to the upstream input it yields blob `0433e06314cee5411ab9722f4e88653d5cac4d79`.

## Composition with the completed sidebar correction

[Commons31848](https://github.com/woahwhattheheck/commons/pull/31848) already supplies an independent offset correction in this stylesheet. Its complete retained postimage is `7e7a96025dfb8c52056a446c3aae4d427669bc8c`. Applying this same text-size patch to that postimage yields `19aeef1d358196eedc0efb9207d92fdd3dbc92a8`.

The patch text is identical against both inputs because its source context occurs before the separate offset hunk. Exact forward/reverse text reconstruction was performed against both retained real inputs. This is composition analysis, not a replay of the previous packet's application/runtime verification. Do not replace newer full source with an older module. Compose with a newer stylesheet if its exact input differs.

The Navbar first-link and LanguageSwitcher URL-state corrections are separate paths and remain unchanged. Upstream implementation and original contributor credit remain with Stellar-Analysis/frontend; this packet claims only the newly connected CSS consumer.

## Primary contracts

Official documentation read on 2026-10-06:
- [MDN font-size](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-size) describes root-relative rem units and percentage font sizing.
- [MDN var()](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/var) describes substitution and the fallback for an unset custom property.

Those contracts support the CSS interpretation. No documentation example or application code was executed.

## Deliberate limits

Root-relative layout dimensions can scale along with root-relative text. This is not a text-only zoom implementation, and fixed-pixel typography and the preset buttons' own inline preview sizes do not scale from this rule. Existing preset choices are retained exactly; the patch makes no contrast, minimum-text-size, accessibility, responsive-layout or browser acceptance claim.

The existing handler applies the property only when a choice is clicked. This patch does not restore a stored choice on a fresh document, synchronize the DOM after another tab changes preferences, alter accent color handling, implement reset controls, validate arbitrary persisted values or change the preference schema. The inspected Settings page exposes no resetPrefs action, so a separate cross-tab removal observation was not promoted into a reset-feature repair.

The exact public Slack query for Stellar-Analysis and ThemeCustomizer returned zero/native END; a repository-local PR search for ThemeCustomizer returned zero with incomplete_results=false. These are bounded chronology results, not an exhaustive absence claim. The complete current source shows the unconnected writer/consumer path.

The complete 959-entry tree had one CSS path and no AGENTS/RULES paths. Retained docs/CONTRIBUTING.md (`f66db3b0eece27eb6fa888948c31ee8c7eabcfd2`) contains EventSource-specific release/test directions; no package release or test execution is authorized in this source-only task. No applicable repository-wide license was established from the differently attributed documentation notices. Accordingly, this packet publishes only the small contextual patch and this original guide.

Evidence comprises full relevant source inspection, independent source/artifact Git blob identities, exact forward/reverse reconstruction, and publication readbacks. No application/browser/runtime, CSS compilation, installation, build, lint, synthetic test, storage operation or upstream repository action was performed. Original ownership, assignment and maintainer acceptance remain separate; no whole-issue completion, award or payment is claimed. All previously held source/provider routes remain held.
