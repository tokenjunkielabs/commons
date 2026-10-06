# PayD report interface translation keys

The mounted report page hardcodes its headings, labels, column captions and messages even though the frontend already loads i18next. This source-only continuation routes that interface copy through the existing translation instance and adds eighteen English resource leaves. Column IDs, report data, date filtering and the export placeholder keep their existing contracts.

This is a scoped continuation of [Protocol-Guild/PayD issue 416](https://github.com/Protocol-Guild/PayD/issues/416), not completion of its frontend-wide coverage requirement. Apply the earlier [Commons #31914 date-label patch](https://github.com/woahwhattheheck/commons/pull/31914) first. Its two unconditional useId calls and matching input/label associations are retained.

## Canonical source and composition

Repository: Protocol-Guild/PayD. Current donor main was observed at `171c74b454daba241bfb75f36d10a0a3a77a68e5`. No donor branch or upstream PR is modified.

| Source path | Required preimage | Prepared postimage | UTF-8 bytes before → after |
|---|---|---|---:|
| `frontend/src/pages/CustomReportBuilder.tsx` | `da817b49f6f79fc9ed34a9f5047f483829a8f1bb` | `4fc17ecc9bcbf450f92f600f914ec31885217f2a` | 8,175 → 8,524 |
| `frontend/src/locales/en/translation.json` | `1188a937baa87a95fe955a5855a57632602b14be` | `30f4748d482f49013f9d77f9d09aaf41f4dfd2d6` | 9,104 → 9,926 |

Both source paths retain mode 100644. The original report module at donor main is `49cfb19b488c62a46a4bc2c8dba8e8a4b6a8bf7e` (7,918 bytes); the required report preimage above is the prepared postimage from #31914. The locale file starts directly from donor main. The patch is intentionally ordered after the date-label patch and is not an instruction to overwrite a sponsor module with a full copy.

The report hunk changes +27/-22 lines; the resource addition is +22/-0. Thirteen hunks contain 164 complete diff rows. The modified report header records the 2026-10-06 source change. This guide records the same date for the JSON resource addition, where comments would not be valid JSON.

## Existing caller and dependency contract

Complete source reads establish:

- `frontend/src/main.tsx`, blob `f84f187971ba135010c48e69fda10f0c0f71ebd9`, imports `./i18n` and renders App.
- `frontend/src/App.tsx`, blob `acc3dfc6f6d5c04ccb1ab693b3a0d5735b81c10c`, mounts CustomReportBuilder at `/reports` inside EmployerLayout.
- `frontend/src/i18n.ts`, blob `1c72db0c246bf567def7afdf55fcd061abc1f5a3`, loads the en/es translation resources, sets the initial and fallback language to English, and retains `escapeValue: false`.
- The issue's existing useTranslation example, `frontend/src/components/FeeEstimationPanel.tsx`, blob `6e1b6905f788b065d82479b0b9722799d7b39702`, uses the same imported hook, default translation namespace and interpolation pattern.
- `frontend/package.json`, blob `33e58d67eca11b200b6988835b1f8450f179d2c2`, and complete `frontend/package-lock.json`, blob `1b41ce5d700d3a51d0e9ba52418ea7b53c9479ab`, retain i18next 25.8.13, react-i18next 16.5.4, React and react-dom 19.2.0. Neither dependency file is modified.

The newly read caller/resource/package bytes and their complete independent Git blob identities are retained. The already completed #31914 report postimage is reused as the exact input; its label work is not rerun.

## Resulting source behavior

The component calls useTranslation unconditionally. ALL_COLUMNS keeps the same six stable IDs and stores resource keys instead of English captions; the captions are resolved during rendering and when constructing the existing export alert. A language change can therefore use the current translation function without translating column IDs or changing selected-column membership.

The eighteen new `customReport` leaves cover title/subtitle, date range/start/end, column-section title, export action, preview title, result-count message, two empty states, export-summary message, and six column captions. Dynamic fields use the same `records` and `columns` names in calls and resources. Existing English wording is retained, including the original “records” grammar. No new pluralization policy is introduced.

The existing English object is extended without replacing any previous key or value. Spanish and other translation files are unchanged; missing translated keys use the configured English fallback. This packet enables translation of this page's interface; it does not claim that new non-English translations were supplied.

Mock row values, including their status strings, dates, amounts, asset identifiers and worker IDs, remain literal data. Date formatting, number formatting, data localization and the alert's comma-separated list format are outside this correction. Filtering, initial dates, checkbox handlers, all useId associations, table-cell data access and the simulated export remain unchanged.

Primary documentation used only for the hook/default namespace, ordinary interpolation and fallback-language contract:
- https://react.i18next.com/latest/usetranslation-hook
- https://www.i18next.com/translation-function/interpolation
- https://www.i18next.com/principles/fallback

These current docs also describe later optional APIs; this patch uses only the string-key hook/interpolation forms already present in the pinned source. React text and the existing alert consume the translated strings; no HTML insertion is added.

## Attribution and current carrier boundary

Wilfred007 authored issue416; original Protocol-Guild/PayD contributors retain authorship of the report page, translations and application wiring. The complete Apache 2.0 license is included unchanged as `LICENSE`, blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` (11,357 bytes). The bounded current issue read was open with no assignee; all three returned comments were requests to be assigned. No assignment is claimed or changed.

The current repository-specific numeric PR query for 416 returned only PR462, whose body concerns webhook settings, adds its own translations and closes issue449. That returned carrier is outside this report-page change; its appearance is not a whole-repository ownership census. A separate bounded Commons PR query for PayD and i18n returned no matches. Neither observation establishes global absence of earlier work.

## Validation and limits

The two complete source strings and the generated patch are retained with full Git blob identities. Exact hunk forward/inverse materialization matches both preimages and both postimages. All old English resource values compare identically after adding the new subtree. One private edit-admission attempt stopped before banking or any provider write because a plain `Columns` token also occurred in identifiers; it was corrected to the exact JSX boundary. No application or translation engine was executed.

Only this minimal patch, attribution/contract guide and exact license are published. No lint, type build, test, browser, DOM, language-switch simulation, runtime, API, account, employee/payroll access, export/download, wallet, upstream submission or reward action occurred. Issue387 real-data/tenant integration and issue416 full primary-flow coverage remain unresolved. Existing source errors, dependency/tooling compatibility, translated layout behavior and deployment acceptance are not established by this packet.
