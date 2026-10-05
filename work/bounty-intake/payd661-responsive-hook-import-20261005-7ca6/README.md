# Match Layout's import to the responsive hook export

This is a source continuation for [Protocol-Guild/PayD issue #301](https://github.com/Protocol-Guild/PayD/issues/301) and SrvFernandes's existing [PR #661](https://github.com/Protocol-Guild/PayD/pull/661). The submitted Layout requests a named useResponsive export, while the submitted hook provides only a default export. One import-line correction connects the actual module pair.

## Provenance and exact source

The issue was observed OPEN and unassigned. Its two comments are third-party activity: a generic assignment proposal and the original author's PR link/claim. They do not establish maintainer assignment, acceptance or payment. PR #661 was OPEN/unmerged at `624f69b413d40ccc8dc9bf5c52a22e1789b1f980`, based on `171c74b454daba241bfb75f36d10a0a3a77a68e5`; its discussion and inline-comment collections were empty. The external PR remains separate and unchanged.

The complete source files read at that head are:

| Path | Git blob | Treatment |
| --- | --- | --- |
| src/components/Layout.jsx | 363caff94b6eb11500574e6c3204842fe48fe2d6 | One import line corrected |
| src/hooks/useResponsive.js | b01a97bcfdb825f63fb68c560a35100aba5cb95e | Unchanged |
| src/components/AdvancedDropdown.jsx | 711777754d56e6f617fd0423f8e8f423c5c87abc | Unchanged, separate component |

The original author added these components and a UI slice. This packet credits that work and addresses only the mismatched responsive-hook import.

## Correction

The hook defines useResponsive locally and ends with `export default useResponsive`. It does not declare a named export. Layout's braces request a named binding, so they do not match that actual export. The patch changes the import to `import useResponsive from '../hooks/useResponsive'`.

There is no need to add a second export or alter the hook's public shape. Every other byte of Layout remains unchanged, including the hook invocation, Redux selectors/dispatch, sidebar toggle, children and markup. The hook's resize subscription/cleanup and its viewport breakpoints are unchanged. No new routing, window fallback, state management or responsive-layout policy is introduced.

The one-hunk patch is +1/-1. It applies exactly to the full Layout preimage `363caff94b6eb11500574e6c3204842fe48fe2d6` and reverses exactly from postimage `13e50f6cc1f66c6df2ca1a4218df990525623748` (1166 UTF-8 bytes). Independent Git blob calculation matches the acquired preimage. The unchanged tail beginning at the Redux imports was compared exactly. These are source-text checks, not a rendered application or build result.

## Integration and retained limits

The untruncated 761-entry head tree identifies `src/App.tsx` at `9d90c939a186a17f5bc042b50191b554357b6f6c` and root `package.json` at `f0325832d3e5150375bd22481e577d19cd148eb6`, exactly the complete files already read in this lane. That App does not import or mount the proposed Layout, and the package does not declare react-redux or @reduxjs/toolkit. The patch neither wires the new Layout into the existing application nor supplies the new slice/provider integration or dependencies. It therefore does not make the whole external proposal runnable or resolve all of issue #301.

The separate AdvancedDropdown source has its own pagination/focus behavior; it is untouched. The responsive hook continues to read window.innerWidth directly, so server-rendering support is not established. No broader keyboard, accessibility, mobile, dropdown, Redux or design-system acceptance is claimed.

The same complete tree pins the already-read CONTRIBUTING.md `1e015aa7e145db0cd0e306f7032cce130b8acbb8`, LICENSE `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`, and README.md `374ffef680426f41b9f3e832059106839cfc72bd`. There is no AGENTS.md or nearer instruction/license in that tree. CONTRIBUTING.md is a scaffold placeholder. The Apache 2.0 LICENSE and MIT README badge disagree; the discrepancy remains explicit. Only this attributed patch and guide are published, with no full module republication or new licensing conclusion.

No React/Redux execution, dependency installation, build, tests, fixtures, browser, resize/keyboard interaction, real account or financial data, wallet, upstream contact/submission/claim, award or payment action occurred. Original author and external contribution/acceptance conditions remain separate.
