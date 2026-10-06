# Dispose the PWA hook's service-worker observers

The mounted settings PWA hook creates a 60-second service-worker update interval after registration resolves. Its original code returned a clearInterval function from the Promise callback, while React received a different effect cleanup that removed only window listeners. Leaving the settings page therefore did not release this interval or its registration/worker listeners, and a late registration could create them after effect cleanup.

This patch gives the effect ownership of those resources. It does not unregister the shared service worker, cancel browser registration, or change the installation, cache-clearing or update actions.

## Exact source and attribution

Repository: https://github.com/Stellar-Analysis/frontend

Immutable source commit: `482ee456369418ef82c4056718cb82d3468f762b`.

| Path | Preimage blob | Intended postimage blob |
| --- | --- | --- |
| src/hooks/useProgressiveWebApp.ts | c7b1b8a74c88e1c9f07da6deef246b5e71bc6f7a | a10651a73c7c35ad1c3d506fb4f0e5f8699ed39f |

Production delta: +22/-7 in one hook. Apply `pwa-observer-cleanup.patch` to the exact preimage above, or compose its hunks with newer source rather than replacing a newer complete module.

This is an attributed continuation of the repository contributors' existing PWA implementation. No original author, claimant or external assignment is replaced. The precise public PWA PR search returned one historical closed carrier, https://github.com/Stellar-Analysis/frontend/pull/115, whose body describes other PWA/SSR/status and accessibility changes; no interval cleanup was established from that returned body. Its implementation and accepted checks were not replayed. A separate public repository/hook-name Slack search returned zero/native END. Neither bounded query is a repository-wide completion census.

## Actual mounting and ownership

The retained locale layout, blob `1f016787657313d58504e79bccbe634a843ce8b5`, hosts the route. The settings page, blob `7c8c98e8f38bc8b1bfec45e753381deac1d7f353`, mounts ProgressiveWebApp with install, offline, update and cache-management controls enabled. The complete component, blob `2721d965007d40a1ff87d9e40f2dff3b463a0e52`, invokes useProgressiveWebApp directly.

The hook's initialization effect owns four window listeners, the registration promise, each installed observer callback and the recurring update check. Its original nested return is a Promise fulfillment value, not React's cleanup callback. The actual effect return can run before registration completes; clearing only a timer that already exists would not cover that ordering.

## Correction

- Keep an effect-local disposed flag, optional interval handle, and cleanup closures for this effect's service-worker observers.
- Return before attaching observers or starting the timer when registration settles after disposal.
- Retain exact named updatefound/statechange callback identities and their original event targets for removal.
- Guard the observer/timer callbacks against disposed effect work.
- In the actual React cleanup, mark disposed first, clear the interval when present, remove the recorded service-worker listeners, and then execute the existing four window-listener removals.
- Suppress registration-error state and storage-estimate state updates after this same initialization effect has been disposed. This does not cancel those promises.

The service-worker registration path, scope, 60-second cadence while active, update-available condition, messages and ordinary active-state behavior remain the same. The entire source from `// Install PWA` through the returned hook API is byte-for-byte unchanged, including install/dismiss/cache clearing/manual update actions and their existing policies.

The removals use the same event type, target and callback with the same default capture option as registration. They remove this hook instance's observers only, without disturbing other consumers. The late-registration guard also covers React's development setup-cleanup-setup ordering without introducing a shared global flag or a cross-instance cache.

## Limits

No service worker is unregistered by effect cleanup. A registration already requested can still complete in the browser; its late result is simply not attached to a disposed hook. An update request already started is not cancelled, and its existing logging may still run. This patch does not introduce a request timeout, abort, polling backoff, registration deduplication or multi-instance singleton.

The disposal flag governs the initialization effect only. Install/user-choice, cache clearing and update/reload actions are unchanged and are not claimed to become unmount-safe or transactional. Cache-estimate accuracy, origin-wide cache policy, already-waiting worker discovery, offline initialization and installation outcome semantics are separate existing behavior. None was exercised or broadened here.

## Primary contracts and source checks

- React useEffect: https://react.dev/reference/react/useEffect — React consumes the cleanup returned by the effect setup and invokes it for dependency changes/unmount; the provider's Promise callbacks are not separate effects.
- Promise.then: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/then — a callback's return value fulfills the Promise returned by then.
- EventTarget.removeEventListener: https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/removeEventListener — removal matches the event type, listener identity and capture option.

The complete immutable component and hook bodies were read as inputs to this new correction; independent Git blob calculations match both native source identities. The patch reconstructed the complete intended hook postimage exactly. The public action/API suffix remained exact. These are source-construction checks, not a TypeScript compile, browser run, synthetic test or demonstration of memory behavior.

The complete source tree previously qualified for this unchanged commit has no AGENTS/RULES paths. The retained docs/CONTRIBUTING.md, blob `f66db3b0eece27eb6fa888948c31ee8c7eabcfd2`, describes EventSource releases. No EventSource release, test or package publication was performed. The differently attributed notices under docs do not establish a license for these modules; this package contains only a minimal contextual patch and this original guide.

No browser, device, service-worker registration, cache/storage, network-update, runtime or test action was performed. No upstream branch, issue, review, acceptance, assignment, award or payment was changed or claimed. Known exact provider failures remain held.

Operation: STELLAR-PWA-OBSERVER-CLEANUP-20261006-7CA6.
