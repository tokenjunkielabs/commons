# Keep the mounted Stellar layout aligned with its sidebar

The current locale layout mounts the fixed Sidebar and Navbar directly. Sidebar uses the saved `sidebarCollapsed` preference to choose `w-20` or `w-64`, and is hidden below `md`. The content separately hardcodes `ml-20 lg:ml-64`. Navbar already reads `--sidebar-offset`, but the stylesheet supplies a constant 5rem desktop value. These independent values disagree with the rendered sidebar.

The default preference is `sidebarCollapsed: false` (expanded). Between `md` and `lg`, a 16rem sidebar therefore accompanies a 5rem content margin. Collapsing on a large viewport leaves a 16rem content margin beside the 5rem sidebar. Below `md`, the hidden sidebar still leaves the content's unprefixed 5rem margin. These are source-derived layout consequences, not screenshot or browser observations.

## Apply this continuation

Apply `sidebar-layout-offset.patch` to [Stellar-Analysis/frontend](https://github.com/Stellar-Analysis/frontend) at `482ee456369418ef82c4056718cb82d3468f762b`, or compose these hunks into newer source. Do not replace newer full files.

| Production path | Original blob | Patched blob | Lines |
| --- | --- | --- | --- |
| `src/app/[locale]/layout.tsx` | `1f016787657313d58504e79bccbe634a843ce8b5` | `205adc494199257e07d8aad3b799f4e2f1a7aa72` | +2/-2 |
| `src/app/globals.css` | `a203da3d12c8a8b625ecf8c1e5253f4d3f42dfd5` | `7e7a96025dfb8c52056a446c3aae4d427669bc8c` | +19/-0 |
| `src/components/layout/sidebar.tsx` | `9b11a0dc39150a9d60f28b68071f1b336aff38ab` | `21541af89b92961aa81bec8cc0de35fc57454a30` | +1/-0 |

Total production delta: +22/-2. The patch changes three existing files:

- The actual locale wrapper gains `terminal-layout`; its main element loses the independent fixed margin classes.
- Sidebar exposes the same existing collapsed value as a data attribute. Width classes, preference updates, navigation and semantics remain unchanged.
- Wrapper-scoped CSS sets `--sidebar-offset` to zero below `md`, 5rem for the rendered collapsed sidebar, and 16rem for the expanded sidebar. The main margin consumes this variable; the existing Navbar consumes the inherited value without any Navbar change.

No new React state, effect, storage access, resize listener, client boundary or provider wrapper is added. The earlier [first-link ref correction, Commons31835](https://github.com/woahwhattheheck/commons/pull/31835), changes Navbar and is independently composable.

## Source contracts

Complete current caller sources were read. `src/app/layout.tsx` (`d99613766c48f2be30014720edd01dc156d58696`) imports globals.css. `UserPreferencesContext.tsx` (`1f22b6a9354ebacf502df2472ddeb24e0006a4e6`) defaults the sidebar to expanded and only provides state; it does not synchronize layout styles. Sidebar and Navbar are direct descendants through the actual locale layout, so the custom property is inherited by Navbar even though the nav itself uses fixed positioning.

The actual manifest (`2b1c6ac1f83096666c7fd6d5ba3fd22780e6b8eb`) declares Tailwind 4.1.18. The complete global stylesheet imports Tailwind, with no `--breakpoint` override or `@config` directive. [Tailwind's responsive-design documentation](https://tailwindcss.com/docs/responsive-design) specifies the default `md` threshold at 48rem; the added media query uses that same threshold. The selected 5rem/16rem values match the existing `w-20`/`w-64` sidebar widths under the source's default spacing scale.

MDN documents [parent selection by :has()](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:has) and [inheritance of custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascading_variables/Using_custom_properties). The new selectors are constrained to a direct Sidebar child of this layout. The existing stylesheet already uses `:has()` for the landing page.

The existing landing selector `body:has(.stellar-landing) main.flex-1` remains more specific than the new `.terminal-layout > main` rule, so its zero-margin treatment is preserved. Existing print margin resets remain `!important`. The old root variable remains available to other layouts; the new variable is scoped to the mounted locale wrapper. Existing sidebar and content transition durations remain unchanged; no animation-synchronization guarantee is added.

## Attribution, instructions and scope

The underlying layout, preferences, Sidebar, Navbar and stylesheet belong to the Stellar-Analysis/frontend contributors. The known current path-history flattening commit by christabel888 is not treated as evidence of original authorship of these particular hunks. No original attribution is replaced.

The retained complete 959-entry repository tree is not truncated and contains no AGENTS.md/RULES.md paths. The full root README `a7546f7a6f85709fccd21e136cd8b12bae820652` and EventSource-specific docs/CONTRIBUTING.md `f66db3b0eece27eb6fa888948c31ee8c7eabcfd2` were read for the preceding UI continuation and reused here. This is not the EventSource test/release/npm-publish workflow. Differently attributed documentation notices do not establish a repository-wide license for full-module republication. Only this original guide and the minimal contextual patch are published.

A repository-local sidebar PR search returned nine carriers, all closed, with incomplete_results false; their body topics concern navigation groups, routes and panels, with no offset repair identified. Historical test and acceptance statements were not replayed. A public Slack search for the repository, sidebar and offset returned no result and native END; both are bounded chronology observations. An earlier exact code-symbol search returned zero with `incomplete_results: true`, so it is not used to claim absence. The defect is instead established by the complete actual imported source.

## Validation and limits

Native blob identities and independent Git hashes match the retained full preimages. All three patch postimages have exact reverse reconstruction to those preimages. Published patch and guide are checked at immutable Commons head and merge identities; the final observed main identity is recorded separately.

No browser, app, responsive viewport, screenshot, accessibility suite, build, package install, lint or test was run. Existing modern CSS support, preference hydration, transition timing and other page layout behavior are not certified by this source correction. There is no upstream branch mutation, submission, issue assignment, sponsor acceptance or bounty/payment claim. Existing provider/source holds and the separate backend work remain untouched.
