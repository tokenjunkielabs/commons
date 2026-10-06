# PayD: report date-label associations

The mounted Custom Report Builder displays Start Date and End Date labels beside two controlled date inputs, but the labels neither wrap their inputs nor provide htmlFor targets. This focused patch gives each field its own useId value and connects its visible label to that input.

The correction is limited to those two source associations. Issue387's separate request to replace mock report data remains unresolved by this packet.

## Source and attribution

Canonical repository: [Protocol-Guild/PayD](https://github.com/Protocol-Guild/PayD).
Immutable donor: `171c74b454daba241bfb75f36d10a0a3a77a68e5`.
Warm intake: [issue387](https://github.com/Protocol-Guild/PayD/issues/387).
Original PayD contributors retain authorship of the report builder and surrounding application. This is a current-main source continuation; it does not claim an external donor PR or modify an upstream branch, issue, assignment or acceptance state.

The bounded numeric387 PR query returned no rows. That result is not an exhaustive contribution or ownership census. The complete page and App source were inspected before preparation and establish a /reports route under EmployerLayout. The page's date controls are rendered unconditionally; useId is called at the top level of that component.

| Source examined | Git blob |
| --- | --- |
| frontend/src/pages/CustomReportBuilder.tsx | 49cfb19b488c62a46a4bc2c8dba8e8a4b6a8bf7e |
| frontend/src/App.tsx | acc3dfc6f6d5c04ccb1ab693b3a0d5735b81c10c |
| frontend/src/components/EmployerLayout.tsx | 5cd117fcdaf260873f1e9f8655787857a3288ca2 |
| frontend/package.json | 33e58d67eca11b200b6988835b1f8450f179d2c2 |
| frontend/package-lock.json | 1b41ce5d700d3a51d0e9ba52418ea7b53c9479ab |
| LICENSE | 261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64 |

The complete donor tree bound the package, lock and license to then-retained full bytes. The lock selects React19.2.0. No dependencies were installed or executed. The packet is distributed as a focused patch and exact Apache license, not a complete copy of the application.

## Change

Apply `report-date-labels.patch` to the immutable donor or reconcile its contexts against a later revision.

| Production path | Preimage | Prepared postimage | Prepared bytes |
| --- | --- | --- | ---: |
| frontend/src/pages/CustomReportBuilder.tsx | 49cfb19b488c62a46a4bc2c8dba8e8a4b6a8bf7e | da817b49f6f79fc9ed34a9f5047f483829a8f1bb | 8175 |

The four-hunk production patch is +8/-3, including a dated modification notice. It imports useId, creates startDateId and endDateId unconditionally at component top level, and pairs each label's htmlFor with its input's id. The IDs are DOM associations, not data or list keys.

[React's useId reference](https://react.dev/reference/react/useId) documents generated accessibility IDs. [The input reference](https://react.dev/reference/react-dom/components/input) documents matching input id and label htmlFor when the input is not nested in its label. These primary API contracts support the source change; no browser or assistive-technology result is asserted.

Removing only the six exact replacements restores every original byte. Controlled values, onChange handlers, date filtering, column selection, mock rows, default date strings, export alert, table, styling and routing are unchanged. The checkbox labels already contain their inputs and are untouched.

## Boundaries

The current page still contains MOCK_DATA and an alert-only export. Its original issue asks for real payroll data scoped to the logged-in organization. The inspected page/layout did not establish that organization identity or a truthful mapping for its setup-date and expected-payout-date columns. The separately inspected backend payroll route requires orgPublicKey and tenant middleware. This packet does not invent a data mapping, bypass authorization, add an endpoint, fetch payroll/account records or imply that issue387 is complete.

Date ordering, timezone/range semantics, data integration, export behavior, validation messages, translations and all other accessibility concerns remain separate. No broad accessibility, screen-reader, hydration, deployment, type-check or compilation verdict follows from static source review.

No application, browser, wallet, employee account, API, database, transaction, test, synthetic fixture, build, dependency installation, workflow or upstream submission was run. No acceptance, grant or payment is claimed.

## Identity and state-loss recovery

The complete source is 7918 UTF-8 bytes before the patch and 8175 afterward. Before publication, the private execution store was lost. No GitHub publisher or mutation had been dispatched for this packet. The source and license were reacquired by their exact immutable blob IDs solely to finish this unpublished work; failed requests and the old advisory-message read were not repeated.

Full independent hashes reproduce the original preimage, prepared postimage and frozen patch identity `1045ded1072b3a4db51e04a555d79e23efb9fe04` (2,044 bytes). Forward/reverse materialization and the six-replacement inverse match complete strings. The prior App/layout/dependency assessment remains a surviving source observation; this guide does not claim that its old raw private records survived the store loss. The guide was rewritten to disclose that distinction.

Only this focused patch, guide and exact 11,357-byte Apache-2.0 LICENSE are published. The complete donor tree inspected before the loss contained no separate NOTICE file. Existing source notices remain and the changed file receives a dated modification notice. These are source/byte-identity checks, not execution tests.
