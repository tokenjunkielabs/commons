# Normalize URL-backed client pagination

The mounted Corridors page reads `page` and `pageSize` through `usePagination`, slices the filtered array with the hook's indices, and sends its values to DataTablePagination. The hook currently uses unrestricted `parseInt` without checking positivity, finiteness, safe integer range or the current page count. The control assumes those invariants: its endpoint buttons are disabled by exact equality, and its jump input is bounded between one and the calculated page count. A malformed query can therefore reach the control as NaN or a nonpositive value; an otherwise valid page can also outlive the filtered result range and produce an empty slice despite matching records.

This source-only correction normalizes both URL numbers and clamps the derived current page to the existing finite total. It makes no automatic navigation or URL rewrite, so an initially empty loading state does not replace a bookmarked requested page in browser history.

## Current production source

Canonical repository: [Stellar-Analysis/frontend](https://github.com/Stellar-Analysis/frontend)  
Revision: `482ee456369418ef82c4056718cb82d3468f762b`

| Path | Git blob | Role |
|---|---|---|
| `src/hooks/usePagination.ts` | `e3e27c92a59f856545fc846c73d4f41226dd9e23` | Complete edited source |
| `src/components/ui/DataTablePagination.tsx` | `e68599b960e740b906988d367b862530514650e1` | Complete control contract |
| `src/app/[locale]/corridors/page.tsx` | `a14fe86977c4071ad958ddc3f206b4f07134b072` | Retained complete file; relevant imports, filtered-array length, hook call, slice and control sections inspected |
| `src/i18n/navigation.ts` | `fd8ba9aa80bb0d0dd56eb76a3891caa0afe0c803` | Existing locale-aware navigation wrapper |
| `src/i18n/routing.ts` | `7a1c19fa17133fa33179f3381d115f8d2ee542f7` | Existing en/es/zh route configuration |

Production change: one hook, +13/-7. Resulting source blob: `af78a3bedcdfd391ce27af2316dfb51e6fdd235f`.

## Behavior and compatibility

A private helper accepts a nonempty string composed entirely of ASCII decimal digits only when its numeric value is a positive safe integer. All other URL values fall back to the existing default: page one or the caller's defaultPageSize (ten when omitted). Leading zeros remain accepted; signed, fractional, exponent, whitespace and suffix forms no longer receive parseInt's partial interpretation.

The hook resolves pageSize first. It then derives the current page as the smaller of the normalized requested page and `max(1, ceil(totalItems / pageSize))`. The memo depends on the query, totalItems and pageSize, so filtering or a loaded result count immediately updates the derived range. This follows the control's existing minimum-one-page convention for an empty result set.

The source-supported caller supplies an array length as totalItems and uses the default page size. The shared API retains its existing assumption that a supplied defaultPageSize is a positive valid integer and totalItems is a finite nonnegative item count. This patch does not add validation or policy for arbitrary malformed programmatic arguments.

No effect writes a normalized URL. Until the user invokes an existing navigation control, the requested query value stays intact. Consequently a page temporarily clamped while totalItems is zero can become the requested page when loaded data permits it. Shrinking and later restoring filtered results similarly derives from the retained URL; the patch does not impose a new reset-on-filter policy.

Existing setPagination, query-copying, localized router.push, page-size-change reset to one, indices and returned API fields remain exact. The hook still accepts any positive safe-integer page size, rather than introducing a new maximum or restricting all callers to the control's four select options. The select may therefore have no matching option for an otherwise valid nonstandard URL size; that existing presentation policy remains outside this patch.

## Source and primary contract assessment

[MDN parseInt](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/parseInt) documents partial parsing, NaN and large-number precision limits. [MDN Number.isSafeInteger](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/isSafeInteger) documents the positive/negative safe-integer range and rejection of noninteger/nonfinite values. These primary references were read on 2026-10-06; no example was executed.

A precise public Slack query for Stellar-Analysis and usePagination returned zero/native END. A bounded repository-local pagination PR query returned three records: known backend cursor PR404, backend lint PR130 and API-contract PR119. None identified this client hook correction. The incidental known backend404 record was left parked; no backend PR/source expansion or retry of the separately held issue330 query was made. An exact code-symbol search returned zero with incomplete_results=true, so it was explicitly inconclusive and is not used to claim an exhaustive caller inventory.

This continuation is grounded in the actual Corridors caller, not a claim about every unseen consumer or the backend cursor implementation. It does not reopen completed Navbar, sidebar, language-switching, text-size or wallet work.

## Apply and limits

Apply `client-pagination-range.patch` to the exact source preimage, or manually compose it with newer source after inspection. Preserve upstream contributor ownership. This is a newly authored narrow normalization hunk, not a claim to the original pagination feature.

The complete source tree has no AGENTS/RULES paths. Its retained docs/CONTRIBUTING.md (`f66db3b0eece27eb6fa888948c31ee8c7eabcfd2`) is EventSource-specific; this task excludes its runtime/test/npm-release work. No applicable repository-wide license was established from the differently attributed documentation notices, so only a minimal contextual patch and this original guide are published.

Validation consists of complete hook/control inspection, actual caller reasoning, independent Git blob identities, exact forward/reverse source reconstruction and immutable publication readbacks. No hook execution, synthetic input, browser, React render, TypeScript/build/lint/test, storage/API request, upstream mutation or issue acceptance was performed. Original author/assignment/maintainer conditions and exact failed-route holds remain unchanged.

No server pagination, arbitrary caller validation, concurrent dataset snapshot, fetch cancellation, empty-count label correction, control-ID uniqueness, page-size select redesign, whole-app accessibility, financial interpretation, bounty or payment outcome is claimed.
