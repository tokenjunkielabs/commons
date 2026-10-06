# Own the offline-status reconnection timeout

The current useOfflineStatus hook starts a new four-second timeout on every online event without retaining its handle. Neither the offline handler nor effect cleanup cancels it. If a later offline-to-online transition occurs while the earlier timeout is pending, that older callback can clear the later justReconnected flag. A pending callback also survives removal of the hook's event subscriptions.

This packet gives each hook instance one tracked reconnection timeout. The existing online handler clears the prior timer before scheduling its replacement; offline transitions and subscription cleanup clear it too. The callback resets the handle when it fires. The public state shape, initial hydration behavior, online/offline assignments and configured 4,000 ms delay remain unchanged.

## Exact source and attribution

The original hook and UI belong to the Stellar-Analysis/frontend contributors. This is an attributed source-only continuation over main, not a claim to their offline feature or an upstream submission.

- Repository: https://github.com/Stellar-Analysis/frontend
- Donor commit: `482ee456369418ef82c4056718cb82d3468f762b`
- Production path: `src/hooks/useOfflineStatus.ts`
- Mode: `100644`
- Original blob: `9c6fb14a17f045f91ad7fb5826594465ebf86799`, 2,058 UTF-8 bytes
- Patched blob: `d4997b15aa46a83e857b8995bb1bf6b2ae1823b3`, 2,579 UTF-8 bytes
- Patch: `reconnect-timeout-ownership.patch`
- Production diff: four hunks, +19/-5
- Modification date: 2026-10-06

A current donor-ref read returned the same commit. The actual complete src tree `67ce0689f0d10058648c9780e182f5edc50d9087` returned 494 entries with truncated=false and supplied the exact hook/consumer entries. No missing source was reconstructed.

The complete settings page, hook and banner were read as actual immutable source and independently matched their native blob identities. A public Slack search for useOfflineStatus returned no match. A bounded upstream offline PR query returned seven records; none names this hook-timeout correction. Those results do not establish global absence of other work, nor do their historical completion/test claims become evidence for this patch.

## Connected visible consumer

The settings page `src/app/[locale]/settings/page.tsx`, blob `7c8c98e8f38bc8b1bfec45e753381deac1d7f353`, imports useOfflineStatus for its inline OfflineStatusBadge. That badge consumes isOnline/offlineSince, not justReconnected.

The distinct complete `src/components/OfflineBanner.tsx`, blob `7d140f7331e2f979f1974317c37953c69f69f36e`, consumes all three fields and computes visibility from (!isOnline || justReconnected) && !dismissed. The retained locale layout blob `1f016787657313d58504e79bccbe634a843ce8b5` mounts this banner. Thus clearing justReconnected can remove the banner's reconnection state.

The banner already cleans its own four-second dismissal timer and its offline elapsed-time interval. Neither timer is modified. The defect here is the separate timeout inside useOfflineStatus. These independent timing and dismissal policies mean this patch does not promise that the banner is visibly present for exactly four seconds in every event/render sequence.

## Minimal implementation

Add a ref holding the existing setTimeout return type or null, plus a stable clearReconnectTimeout callback. It calls clearTimeout only for a stored handle and sets the ref to null. The handlers use this stable callback:

1. Online: cancel the previous timeout, retain the existing state assignments, and store the replacement four-second timeout. When it fires, clear the handle and perform the existing flag reset.
2. Offline: cancel the pending timeout, then retain the existing offline state, timestamp and false reconnection flag assignments.
3. Subscription cleanup: remove the same online/offline listeners and cancel the instance's remaining timeout.

The useCallback and useEffect dependency lists include the stable cleanup callback. No timer work occurs during render. Multiple hook consumers continue to own separate state/listeners/timers; this does not introduce a singleton or a cross-component synchronization policy.

The initial isOnline=true state and mount effect that reads navigator.onLine are exact. The existing SSR/hydration policy is preserved. No change is made to offlineSince Date creation, the exported interface, network-event detection, fetches, storage, retry policy or PWA installation.

## Primary contracts

Read on 2026-10-06:

- React useEffect: https://react.dev/reference/react/useEffect
  Cleanup runs before a changed effect is set up again and when the component is removed; subscriptions and timers are external resources the effect can own.
- MDN clearTimeout: https://developer.mozilla.org/en-US/docs/Web/API/Window/clearTimeout
  Cancels the pending timeout identified by the value returned by setTimeout.

These contracts support cancellation and lifecycle ownership. They do not certify this application's runtime or browser scheduling. Clearing a pending timer is not rollback of an already executed callback, and the browser's configured delay is not an exact wall-clock guarantee.

## Integration and preserved scopes

Apply the patch to the pinned hook, or integrate the four exact hunks into a newer hook after inspecting its event/timer policy. Preserve newer source. Settings, OfflineBanner and the locale layout are source inputs only; no complete module is republished.

The hook explicitly exists separately from useProgressiveWebApp. Completed Commons PWA31882/31910 and shortcut31916/31917 packets stay untouched. Root's API-client HeadersInit work, reconciliation documentation and every data-sync behavior are separate. The banner's existing text about syncing remains its original UI copy; this correction neither starts reconciliation nor proves that a network is reachable.

## Instructions, packaging and validation limits

The retained complete donor tree contained no AGENTS/RULES path. The observed `docs/CONTRIBUTING.md` blob `f66db3b0eece27eb6fa888948c31ee8c7eabcfd2` gives EventSource-specific test/release guidance. This session authorizes source publication and excludes runtime, tests, browser/device actions and upstream publication. No repository-wide license is inferred from the differently attributed documentation notices. The packet contains only a minimal patch and this original guide.

Performed source checks: three complete input blob identities, full literal diff coverage, exact forward/reverse text reconstruction and independent postimage identity. These are text checks, not a simulated event sequence. No hook/component, timer, browser, synthetic fixture, test, build or workflow was executed.

Publication checks use both complete artifacts at the immutable Commons head and merge, changed-path/parent metadata and the final named main reference. If final main equals the checked merge, the immutable full reads cover that exact identity; otherwise complete artifact reads at the observed later main are required. No success is asserted by that plan before actual readback.

No upstream branch/issue/comment, credential, account, wallet, transaction, award or payment was changed. Browser behavior, accessibility, native acceptance and bounty/payment outcomes remain unclaimed.
