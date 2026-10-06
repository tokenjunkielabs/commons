# PayD: first-page history request lifetime

When debounced history filters change, the mounted transaction-history page starts another first-page request. The original effect has no cleanup. A slower prior request can therefore replace the newer request's rows, has-more value or error, and its finally block can clear the newer request's loading state. This focused source patch makes each effect instance stop writing state after its cleanup.

## Canonical source and attribution

Canonical repository: [Protocol-Guild/PayD](https://github.com/Protocol-Guild/PayD). Immutable donor commit: `171c74b454daba241bfb75f36d10a0a3a77a68e5`.

Changed source path: `frontend/src/pages/TransactionHistory.tsx`. The actual client mounting chain is `frontend/src/main.tsx` → `App` → the `/transactions` route under `EmployerLayout` → `TransactionHistory`. The complete current page and the complete imported `fetchHistoryPage` service were retained. No account, employee record, transaction payload or live service was requested.

This is an attributed continuation of the repository contributors' existing page. The latest path commit returned by the bounded donor-history request was `4f5dd01b31a0b7445e50408398b6fbe9b52d8f48`, a design-token/UI revision; that observation does not imply sole authorship. Existing upstream [PR 573](https://github.com/Protocol-Guild/PayD/pull/573), authored by waterWang, remains open and non-draft at `48c11ad3a9211967dd6752d1e13907d673f97050` on `waterWang/PayD:feat/474-table-skeletons`. Its complete eight-file diff changes the history page's skeleton declaration/import/rendering; it does not change the request effect. Its reported checks are third-party claims and were not repeated here. No upstream PR, branch, assignment, comment or acceptance state is changed.

The intake was [issue 282](https://github.com/Protocol-Guild/PayD/issues/282), whose title requests skeleton loading screens. The current page already contains a six-row skeleton. The issue remains open with no listed assignee in the bounded page and one generic assignment-request comment. A numeric PR query returned no matches; a separate page-name query found the existing skeleton carrier above, so the numeric query is not treated as an absence proof. This packet repairs a first-page loading-state lifetime problem; it does not claim to implement every skeleton or complete issue 282.

## Exact source identities

| Source | Git blob | UTF-8 bytes |
| --- | --- | ---: |
| Original history page | `ffa01e776eb57818efe9d2e4576a0a91aa1ef691` | 10,488 |
| Prepared history page | `9e82e3fd52b880df31e1f0090c5eaf1899811565` | 10,740 |
| Unchanged history service | `64a3a44f9fe83b2c41116c0308a4edcec5684f38` | 4,422 |

Apply `first-page-lifetime.patch` to the named donor source, or explicitly reconcile its exact contexts against a later version. The three-hunk production change is +14/−4, including a dated modification notice. It changes only the first-page effect and that notice:

- Each setup starts with an effect-local `active = true`.
- The successful awaited result checks that flag before either items or has-more is written.
- The catch and finally paths check the same flag before setting error or clearing loading.
- Cleanup sets the flag to false.

The initial synchronous loading/error reset remains. The 350ms filter debounce, page reset, dependency list, current skeleton, displayed rows, query arguments, service implementation, button and pagination code are unchanged. No new dependency, shared global state or request identifier is introduced.

## Contract and limits

React's official [useEffect reference](https://react.dev/reference/react/useEffect#fetching-data-with-effects) specifies cleanup before the replacement setup for changed dependencies and on unmount. Its data-fetching example uses an effect-local flag to ignore obsolete responses. This is the contract used here. The retained current entrypoint uses client `createRoot` and StrictMode; the source change also invalidates the prior effect in that development cleanup/setup cycle. These are source-derived statements, not an executed React or browser result.

This is suppression of state writes after effect cleanup, not cancellation of a fetch or contract-service initialization. Existing work can continue to completion. A filter edit is still subject to the existing debounce; cleanup does not happen merely because the raw input changed before the debounced dependency updates. The patch supplies no guarantee about a result that finishes before cleanup, same-filter manual refreshes, caching, server rendering, or network/API success.

The separate `loadMore` function is unchanged. It can still append a late page or alter pagination/error state around filter changes; overlapping pagination attempts and request-generation coordination remain separate work. The patch does not make the whole history screen race-free. It also leaves the service's repeated contract-event page, filtering/ordering/normalization, authentication, partial event reads, error/empty-state presentation and certificate behavior unchanged. No financial correctness, data completeness, cross-account isolation, production readiness or deployment assertion is made.

## Validation and distribution

The complete 10,488-byte source was retained before editing. Pure text transformation produced the prepared source and patch. Forward application reconstructs the 10,740-byte prepared source exactly; reverse application restores every original byte. Removing the modification notice and replacing the new effect with the original reproduces the whole original file, establishing that no other source changed. Independent Git blob identities bind the original, postimage and patch.

This validation does not execute the application or a synthetic request sequence. No compiler, tests, fixture, browser, dependency installation, workflow, API, wallet, payment, contract or upstream action occurred. The nongating independent review considered the stated effect-local ordering contract only.

The canonical Apache-2.0 license is retained verbatim as `LICENSE`, blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` (11,357 UTF-8 bytes), from the already retained matching source base. Its complete tree had no separate NOTICE file. Existing source notices are preserved and the changed file gains the dated modification notice. Only this focused patch, guide and license are published.
