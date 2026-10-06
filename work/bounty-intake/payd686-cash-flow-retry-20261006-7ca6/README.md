# Connect cash-flow retry to its error boundary

The current cash-flow route supplies `ErrorFallback` with an empty `onReset` callback. The fallback displays a Try Again button, but the surrounding `ErrorBoundary` never clears its `hasError` state. This patch gives an opt-in fallback renderer the boundary's own bound reset callback and connects this route's existing button to it.

## Source and attribution

- Canonical repository: [Protocol-Guild/PayD](https://github.com/Protocol-Guild/PayD).
- Existing carrier: [PR 686](https://github.com/Protocol-Guild/PayD/pull/686), authored by `woahwhattheheck`.
- Donor: `woahwhattheheck/PayD:sol56/payd489-cashflow-real-data-20261004`.
- Exact donor head: `7736cce69ada2434f54f23b3fef266519bcf64c1`.
- Observed base: `171c74b454daba241bfb75f36d10a0a3a77a68e5`.
- Related request: [issue 489](https://github.com/Protocol-Guild/PayD/issues/489), adding the cash-flow route and real API integration.

The current carrier already mounts the page, uses its live API adapter and avoids the empty-account mount request. Those implementations remain credited and unchanged. The issue is open and unassigned in the observed metadata; its one returned comment from `ranjeet150` asks for assignment and is not an award or acceptance.

The PR body separately notes textual overlap with PR 678's token work. That source was not reacquired, merged or reconciled for this packet. This focused patch requires the exact donor preimages below and makes no claim that arbitrary later carrier combinations apply automatically.

## Production identities

| Changed path | Complete preimage | Prepared postimage | Prepared UTF-8 bytes |
| --- | --- | --- | ---: |
| `frontend/src/components/ErrorBoundary.tsx` | `c57a9ff7bf87afea45f8d6a5ed54f407a9236725` | `c723af6494a34ece94f438f31dc7dedee83fa985` | 1032 |
| `frontend/src/App.tsx` | `5a1dd01504bbf5c3031b48bf9e1856260f835883` | `e9504713e7067f64fb5b9817a8bc9ce0b2c6c578` | 6832 |

The patch is relative to the repository root. It has ten added and three removed production lines across five hunks, including prominent dated modification notices.

## Reset contract

The existing `fallback: React.ReactNode` API remains accepted. An additional callback form receives `resetError: () => void` and returns a React node. The boundary invokes that form only when displaying its error fallback.

The boundary's class-arrow method calls `this.setState({ hasError: false })`. The function is bound to that boundary instance. On the next render, the boundary returns its children instead of the fallback, allowing the failed child subtree another mount/render attempt. If the child fails again, the existing error-state transition and Sentry reporting can return it to the fallback.

The cash-flow route changes only its fallback expression:

```tsx
fallback={(resetError) => <ErrorFallback onReset={resetError} />}
```

The existing Try Again button already calls `onReset`; its component, translated text, styling and home link are unchanged. Existing ReactNode fallback callers continue to receive their nodes exactly as before. Other routes with empty callbacks are not converted by this packet.

This is a retry connection, not a repair of the underlying thrown error. It does not catch asynchronous errors or errors thrown by the boundary/fallback itself, cancel work, reset shared stores, clear caches, guarantee route navigation, or prove successful data recovery. It does not introduce an automatic retry loop.

## Complete source evidence

| Read path | Git blob | UTF-8 bytes |
| --- | --- | ---: |
| `frontend/src/components/ErrorBoundary.tsx` | `c57a9ff7bf87afea45f8d6a5ed54f407a9236725` | 759 |
| `frontend/src/components/ErrorFallback.tsx` | `9af8bd18a15ae00176ed8e62d00e80dd07cf1b44` | 1699 |
| `frontend/src/App.tsx` | `5a1dd01504bbf5c3031b48bf9e1856260f835883` | 6743 |
| `frontend/src/pages/CashFlowForecast.tsx` | `073fa3485dcdc2345edd3bdc1c566cc269d84378` | 17497 |
| `frontend/src/services/cashFlowLiveApi.ts` | `4bdb9549e92dcb5b282ecfa24147dc6c7ac06828` | 2083 |

All five complete source texts were retained and independently hashed. The actual route, fallback button and boundary state transition establish the source mismatch; the full page and adapter establish the retained carrier context. They were not executed.

The changed-file response contains all seven paths reported by PR metadata. Together with its common base and the retained source-family tree, those changes leave the previously read root CONTRIBUTING, LICENSE and README identities unchanged: `1e015aa7e145db0cd0e306f7032cce130b8acbb8`, `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` and `374ffef680426f41b9f3e832059106839cfc72bd`. No new instruction or NOTICE path appears in that change set. The retained root license is Apache 2.0 and is copied exactly. The unchanged README has a conflicting MIT badge; this packet does not resolve that discrepancy.

## Verification and boundaries

Both source postimages were prepared once from the complete immutable preimages. Forward patch application and reverse reconstruction match exactly. Independent retained-source reasoning found no ordering or type-contract defect in the supplied callback union, class-arrow binding and selected route. This is source reasoning and byte identity, not compilation or React execution.

No browser, component, compiler, test, fixture, build, backend request, live financial input or deployment ran. The packet does not rerun the carrier's historical validations. The issue's full route, date-range, chart and API acceptance remains separate. Other application error-boundary usage and unrelated request races are not newly guaranteed.

The Commons deliverable contains the focused two-file patch, this guide and the exact root license, not the full donor modules. Fresh donor-head and Commons target guards are required before publication. Later source movement requires explicit reconciliation.

No upstream issue or PR was changed; no sponsor contact, assignment claim, account, credentials, employee records, wallet, chain, payment or reward action occurred. Original authors and external acceptance conditions remain intact.
