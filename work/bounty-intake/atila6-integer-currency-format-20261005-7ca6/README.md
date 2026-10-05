# Atila integer currency formatting continuation

## Result

The exported `formatCurrency` helper converts an amount to an integer by first localizing the number and then parsing that display string. Grouping separators and localized digits make that an unsafe numeric intermediate. This patch replaces only that conversion line with finite numeric truncation. Non-finite inputs in this branch still become `NaN`.

This is a one-line correction to the existing optional `convertToInteger=true` API branch. The inspected CurrencyDisplay and convertCurrency call sites use the default false branch. No failing live caller, session, application or browser was observed.

## Source and prior completion

- Lead: https://github.com/atilatech/client-web-app/issues/14 — open, one returned comment, historical $50 title. It links to the component-library issue below; it is not current funding or acceptance evidence.
- Actual component issue: https://github.com/atilatech/atila-web-components-library/issues/6 — closed/completed by ademidun on 2022-02-23, zero comments and one close event.
- Original contribution: https://github.com/atilatech/atila-web-components-library/pull/8 — ademidun's merged currency-display work, head `589ca6f9b7c0fdae56705dab12a027fe2df72524`, merge/current master `d3c4a92a53b833f67af341efc903795f854c2bb7`. Its complete eleven-file change list and patches were read. This continuation does not replay or claim the original converter feature.
- Exact target: https://github.com/atilatech/atila-web-components-library/blob/d3c4a92a53b833f67af341efc903795f854c2bb7/src/services/utils/CurrencyUtils.ts
- Original target blob: `e4a24765824426654dfbfc8740121df700578d64` (1,409 UTF-8 bytes).
- Corrected target identity after applying the patch: `b9c9e8ddc0382974eba538bcc7fd34035b88ceb8` (1,418 UTF-8 bytes).

The complete current target, export barrel, CurrencyDisplay, currency model, README and package file were read. The recursive current tree returned all 41 entries with `truncated=false`; it contains no AGENTS, CONTRIBUTING or standalone license file. The README provides build/export guidance and the package is private with no license field. The client's separate formatter was also inspected; it is a different implementation and is not changed here.

## Why the correction is bounded

The old branch passes the result of `input.toLocaleString()` to `Number.parseInt`. MDN's directly read Number.toLocaleString reference explains its locale-sensitive representation and gives a U.S. English grouping example. A string containing a grouping separator does not preserve a complete integer when parsed that way. This is static source reasoning, not a reproduced browser observation.

The replacement works on the already parsed numeric value:

```ts
input = Number.isFinite(input) ? Math.trunc(input) : NaN;
```

Truncation removes the fractional part toward zero. The finite guard preserves the old non-finite-to-NaN behavior for integer conversion. Initial parseFloat behavior, the default false branch, currency selection, fractional display settings, final en-ca localization and all exchange-rate constants remain as supplied by the original source. No rate refresh, transaction, provider call or accounting policy is introduced.

## Patch and validation

`integer-format.patch` is a single production hunk with +1/-1 and eight complete context/change rows. Its context was matched against the complete retained 1,409-byte preimage, and applying the serialized hunk rows exactly produced the retained 1,418-byte postimage. Both Git blob identities were independently computed from those full texts.

No shell, TypeScript compiler, React application, browser, payment flow, test, fixture, synthetic example or external service ran. The check above establishes exact source transformation, not runtime acceptance. Package dependencies, component registration, Bit exports and application deployment were not changed.

The typed search_issues response unexpectedly included issue6 for an is:pr query, so it was not used as PR-absence evidence. A separate supported native GitHub issue-search response returned the actual merged PR8. The bounded Commons PR search returned zero items with incomplete_results=false; the bounded public Slack Atila search returned zero/provider end without proving global absence or query application.

## Documentation provenance

Successfully read: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toLocaleString

One attempted read of https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/trunc returned ServerError. That exact route remains held; it was not retried or replaced, and no successful read of that page is claimed.

## Attribution and distribution

The original helper and merged currency contribution are attributed to ademidun and Atila. Because no license grant was found in the complete inspected tree, package or README, this packet contains only the focused patch and this guide. It does not republish the full original module or invent a license. No upstream PR, comment, claim, bounty acceptance, contact or payment action was made.
