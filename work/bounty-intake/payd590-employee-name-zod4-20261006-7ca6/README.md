# PayD: employee-name normalization and Zod 4 enum messages

The existing form-validation carrier checks employee fullName length on the raw string, although its submission handler later trims that value. Whitespace can therefore satisfy the existing length checks before becoming an empty submitted name. The same shared schema uses the former errorMap enum parameter despite the exact package lock selecting Zod 4.1.13.

This patch trims employee fullName before its unchanged minimum checks and expresses the three existing enum messages through Zod 4's error parameter. It preserves the existing validation machinery.

## Canonical source and attribution

The warm intake was [Protocol-Guild/PayD issue183](https://github.com/Protocol-Guild/PayD/issues/183). A bounded component-carrier query identified the more specific existing [PR590 for issue477](https://github.com/Protocol-Guild/PayD/pull/590). The numeric183 query alone returned no rows; it was not treated as proof that no form-validation work existed.

The actual donor is `waterWang/PayD:feat/zod-form-validation-477` at `0c4b10f80cfa4815ef5c624c012889fcf0a62db5`. The current PR is open and unmerged. It already introduces the shared schemas and validation in EmployeeEntry and PayrollScheduler. Original waterWang and PayD contributors retain authorship; their external branch and PR are unchanged.

Complete schemas.ts, EmployeeEntry.tsx and App.tsx were retained. The App mounts EmployeeEntry on /employee. The component uses employeeFormSchema.safeParse for blur feedback, its disabled submit button and the explicit submit guard. An invalid result returns before the existing wallet-generation branch. The later payload path already calls fullName.trim(). The new validation therefore applies at a connected source boundary; no application or form was run.

| Retained source | Git blob |
| --- | --- |
| frontend/src/schemas.ts | c01391e6c57401e214e8905a72fbcf929b16ba19 |
| frontend/src/pages/EmployeeEntry.tsx | 2cf168ecda5626caa3ec285152dd1c0b8004cc4c |
| frontend/src/App.tsx | 35d47f8f1e851aa546d6a6d39b0f9bb6b6ad29de |
| frontend/package.json | 33e58d67eca11b200b6988835b1f8450f179d2c2 |
| frontend/package-lock.json | 1b41ce5d700d3a51d0e9ba52418ea7b53c9479ab |
| LICENSE | 261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64 |

The exact donor tree is complete with 725 entries. It binds package, lock and license to the same complete bytes already retained from another donor head; those matching objects were reused without another content acquisition.

## Patch and supported API

Apply `employee-name-zod4.patch` to the immutable donor or reconcile its contexts against a later revision.

| Changed source | Preimage | Prepared postimage | Prepared bytes |
| --- | --- | --- | ---: |
| frontend/src/schemas.ts | c01391e6c57401e214e8905a72fbcf929b16ba19 | f0c233cab65e8b93afb63d97ba8fedab878c6360 | 1,576 |

The three-hunk source change is +5/-3, including its modification notice. The only employee-name change is insertion of .trim() between .string() and the original min(1)/min(2) checks. It does not invent a new minimum, maximum, alphabet, surname requirement or internal-space normalization. The existing caller consumes success/issues rather than result.data; the trim still governs validation, while the form state and existing payload code remain unchanged.

The role, currency and payroll-frequency enums keep their exact accepted values and fixed message strings. Their three former errorMap callbacks become supported error string parameters. The payroll name, amount, date, memo, wallet-address and email definitions are byte-for-byte unchanged.

The exact lock selects Zod 4.1.13 from the manifest range ^4.1.13. [Zod's string API](https://zod.dev/api) documents trim and minimum-length checks. [The primary Zod 4 migration guide](https://zod.dev/v4/changelog) replaces errorMap with error and supports literal error text. Those API contracts support this source correction; they do not prove the donor compiles or executes successfully.

## Boundaries

Only the employee form's complete connected caller was assessed. The current PR lists PayrollScheduler as a shared-schema consumer, but this packet does not claim a complete caller census or a runtime payroll flow. The payroll-frequency enum receives the same API-parameter correction because it resides in the shared imported schema module.

Other form behavior remains separate: source data loaded from drafts, touched/error refresh, error accessibility/localization, asynchronous submission ordering, API failures, wallet/address checksums, generated-key handling, all transaction/payment operations, numerical finiteness and date semantics. No whole issue183/477 or PR590 acceptance is claimed. Current source and package observations are not deployment or compiler evidence.

The external carrier's acceptance criteria and reported verification remain its author's statements. This packet runs no synthetic names, schema parser, wallet generator, API request, test, type checker, compiler, browser, application, dependency installation or workflow. It performs no account, credential, employee-data, wallet, payment, upstream or reward action.

## Source identity and distribution

The complete original schema has 1,555 UTF-8 bytes; the prepared schema has 1,576. Full forward patch materialization matches the prepared postimage, and reverse materialization restores the original exactly. The original absent final newline is preserved. Removing the four semantic edits and the modification notice restores every original byte.

Only the focused patch, this guide and the exact 11,357-byte Apache-2.0 LICENSE are published. The complete donor tree contains no separate NOTICE file. Existing source notices remain and the changed file gains a dated modification notice. Source byte checks and retained-contract review are distinct from runtime validation.
