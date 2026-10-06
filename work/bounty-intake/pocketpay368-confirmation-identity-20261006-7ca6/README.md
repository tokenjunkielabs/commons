# PocketPay: bind confirmation settlement to its request

A superseded asynchronous confirmation can currently close and resolve the replacement confirmation. This packet fixes that request-identity error in `src/hooks/useConfirm.tsx`, without changing any contact, wallet, vault or payment action.

## Attribution and scope

Canonical source: [Stellar-PocketPay/pocketpay-mobile](https://github.com/Stellar-PocketPay/pocketpay-mobile), current observed main `c3a24abacb45030eb4fef41aabc46b312aaf54a3`.

The shared hook was introduced by giftexceed's [PR 383](https://github.com/Stellar-PocketPay/pocketpay-mobile/pull/383), head `b3faee0e4fd569e0519053cd3c0be351bf152fbb`, merged at `ffd5a5f60683902afb46ec08f7c66dddc497714b`. Original [issue 368](https://github.com/Stellar-PocketPay/pocketpay-mobile/issues/368) is closed and assigned to giftexceed; its three comments and current PR metadata were read. The completion bot reports the original contribution completed; this continuation neither reopens that assignment nor claims its points or acceptance.

The new source question arose while qualifying [issue 301](https://github.com/Stellar-PocketPay/pocketpay-mobile/issues/301). Current contacts callers already request a named destructive confirmation with Cancel, and mount the returned dialog. That feature is not recreated. The correction concerns the shared hook's separately documented supersession behavior.

## Source-established failure

The complete current hook accepts asynchronous `onConfirm` work and explicitly supports a second `confirm()` call superseding an open request. Its current documentation says the superseded promise resolves false.

The handler captures an earlier request before awaiting its callback. Its unconditional `finally` then calls a shared `settle(true)`, which reads whichever resolver is currently in `resolverRef` and clears whichever request is displayed. If a later call installed a replacement while the earlier callback awaited, the earlier completion can therefore resolve that replacement true and remove it without its own confirmation.

This conclusion is a static control-flow reading of the documented API, not a claim that the sequence was executed on a device. The modal's tap guard and busy state address its own events; they do not associate the hook's resolver with the asynchronous callback that started it.

## Correction

Each `confirm()` invocation creates a fresh internal wrapper containing the options and that invocation's promise resolver. State supplies the displayed request; an instance-local ref identifies the active wrapper.

- Replacing a request still resolves the superseded promise false.
- Confirm and Cancel handlers retain the wrapper from their render.
- A stale handler cannot invoke an obsolete request's callback.
- Settlement acts only if its expected wrapper remains active.
- Completion of already-started obsolete work cannot clear or resolve a replacement.
- Reusing the same options object for multiple calls still produces distinct identities.

The public request/result types, visible options, modal props and callback exception propagation remain unchanged. `ConfirmModal` itself is not modified or remounted. Its existing busy period can therefore continue until the outstanding callback settles.

[React's useRef reference](https://react.dev/reference/react/useRef) supports retaining instance-local mutable information between renders; the correction reads/writes that ref only in callbacks. Displayed content continues to come from state, consistent with the separate [useState contract](https://react.dev/reference/react/useState). No state object is mutated.

## Pinned source map

| Path | Before Git blob | After Git blob |
| --- | --- | --- |
| `src/hooks/useConfirm.tsx` | `e2578565b6abfa62ef949f228260358fbed751a6` | `132bf513f2fe2d555bd3b1f5e940bde0f70f48aa` |

Production delta: +28/-18, one source file.

Relevant unchanged inputs at the same sponsor commit:

| Path | Git blob | Qualification |
| --- | --- | --- |
| `src/components/ConfirmModal.tsx` | `6d6d68d41cef0d4dc3f72b47f29600cf124d449c` | Complete busy/async/handler source read |
| `docs/async-actions-and-confirmations.md` | `143ddd7d71b19c0f507488843ce007ab69d9f507` | Complete explicit supersession and async contract read |
| `src/components/ContactManagement.tsx` | `25874bf19b80318d69df03dfac70237abca01469` | Complete confirmation caller read |
| `app/contacts.tsx` | `9722843b217e96a17917dcfc2f87ea0abe6b5b81` | Exact handler/render excerpts transferred from retained complete source; not reread here |
| `CONTRIBUTING.md` | `d8493281d318b348f98a9bd999c2ffd6cc966d0d` | Current retained contribution instructions |

An independent reasoning review of the supplied request sequence agreed that both confirm/cancel handlers and post-await settlement need the same identity. That review involved no additional source retrieval or execution and was not an approval gate.

## Integration and limits

Apply `confirmation-identity.patch` only to the documented preimage, or compose the hunk with newer hook source. Keep the original giftexceed contribution and subsequent authors' work. The completed contacts-search packet [Commons 31783](https://github.com/woahwhattheheck/commons/pull/31783) touches a different file.

This is request-result isolation, not cancellation of an action that already started. A superseded request can resolve false while its callback later completes or rejects; that existing outcome convention is preserved. No rollback, transaction atomicity, unmount cleanup, hung-promise timeout, general reentrancy, custom mutable options, or new error-result semantics are claimed. Existing modal double-tap handling and rejection behavior remain as implemented.

Static validation covers complete hook/modal/document source, literal patch construction, source identities and exact publication readbacks. No synthetic request sequence, test, application, device, storage, account, wallet, network or transaction was executed. Upstream checks and UI/native acceptance remain pending for any eventual integration; this is not an upstream submission or whole-issue acceptance.

The observed complete sponsor tree contains no LICENSE file. Only this narrow attributed patch and integration guide are published; no full sponsor module or invented license grant is included. No bounty, award, payment or current-funding claim is made.
