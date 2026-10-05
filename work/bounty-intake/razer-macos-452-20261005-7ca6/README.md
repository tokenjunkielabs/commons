# Razer macOS #452: automatic KVM reconnect and lighting restoration

This packet contains a production patch against **1kc/razer-macos at 27f8a770611c4d68d0387a980e55b79711a343f3**. It adds passive USB topology observation, serializes device refreshes, retains the last application-known lighting state while devices are absent, and refreshes open settings views.

**Status: source implementation complete; native build and physical KVM behavior unverified.** This is a reviewable source delivery in Commons. It does not represent an upstream pull request, a bounty submission, maintainer acceptance, or a payment.

Operation: `RAZER452-PASSIVE-KVM-RESTORE-20261005-7CA6`. Date: 2026-10-05.

## Files and application

- `razer-macos-452.patch` is a unified patch with 48 hunks across 13 production files: 800 added lines and 104 deleted lines relative to the pinned upstream source.
- `source/` contains every complete resulting production file, preserving upstream-relative paths.
- `source-manifest.json` records the exact upstream and result Git blob identities, byte lengths, submodule pins, verification scope, and remaining limits.
- `LICENSE` is the unchanged upstream GPL version 2 text, blob `d159169d1050894d3ea3b98e1c965c4058208fe1`. The upstream package declares `GPL-2.0-only`; upstream attribution and source comments are retained. The additions in this packet are supplied under the same license.

Apply the patch in a checkout of the recorded upstream commit, or copy the complete files from `source/` to their corresponding paths after comparing the manifest's preimages. The source uses the project's existing native add-on and build configuration. The package, dependency lockfile, submodule pins, and `binding.gyp` are unchanged. A rebuilt native add-on is needed for automatic topology detection; an older add-on without the new export retains manual refresh.

No build or application command was run to produce this packet. No proposed commands are presented as successful execution.

## Source problem and existing work

[Issue #452](https://github.com/1kc/razer-macos/issues/452) describes switching a KVM between a PC and Mac and having to refresh the device list and choose the lights again. At the pinned source, list refresh closes and reopens native devices, replaces the global animations, and reinitializes the state manager. It does not observe USB topology. A disconnected device disappears from the active list, so an active-list-only snapshot cannot preserve its state through an empty interval.

Two existing external changes were read before implementation:

| Existing contribution | Observed head | Relevant scope |
| --- | --- | --- |
| [PR #955](https://github.com/1kc/razer-macos/pull/955) | `dedb8a88b7ad3cc1fb0cd1220dc2579fb41a7d32` | USB attach/detach monitor and direct manager refresh; subsequent state application can use the old state-manager device list. |
| [PR #964](https://github.com/1kc/razer-macos/pull/964) | `51edc351c6e7dc4b34bdfdc9603d708ead45307e` | Current-state snapshot around manual refresh; no automatic observation and no cache spanning an empty active list. |

These are prior contributions and competing approaches. The source here was authored against the pinned upstream files; this packet does not claim ownership of either external PR. The last qualified own-PR search returned zero, with a complete provider page, before this operation's activity note.

The current upstream permission receipt allows reading and reports no push access. No writable fork or callable fork-creation contract was established. The separately inspected Gyroflow publication guide assumes an existing fork and separately authorized publishing credentials; it supplies no general fork-creation route. No upstream write, fork attempt, workflow, credential access, or blocked operation retry was made for this delivery.

## Behavior and design

### Passive observation

The native `getDeviceTopology()` export reads Razer USB device services through IOKit. It returns a product ID and a decimal-string registry ID for each observed service. It does not open USB devices, construct the library's device handles, or replace the live global device table.

Registry IDs remain 64-bit values through native sorting and become strings before crossing into JavaScript. The JS reader validates entries and duplicate registry IDs, then filters by the application's configured product IDs. Devices of the same product remain separate entries; product IDs are never used to deduplicate USB services.

The native code releases its iterator, service handles, and property dictionaries. It treats enumeration, property, registry-identity, conversion, and invalidated-iterator failures as failed observations. Such failures do not masquerade as an empty topology.

The monitor polls every 1,000 ms. A changed fingerprint must be observed again after a 300 ms settling interval before requesting refresh. Failed reconciliation backs off from one second to a maximum of ten seconds, with the settling observation on a subsequent attempt. Repeated identical error messages are suppressed until recovery or a changed error.

### One refresh transaction at a time

All application refresh requests enter one promise queue. Concurrent requests with identical state flags share their pending operation. A rejected operation does not poison the queue.

Each transaction:

1. Saves meaningful state from the currently accepted, uniquely identified application devices.
2. Stops the global color timers and clears the state manager's device references.
3. Obtains a passive topology snapshot, closes the old device generation, and opens the native table once.
4. Waits for every device initializer to settle before publishing the newly initialized list.
5. Compares the opened product multiset with the observed supported-product multiset **before** startup-state application or restoration.
6. Rebinds the state manager to the new objects and applies the state policy chosen by the caller.
7. Accepts the observation only after the whole operation succeeds, then updates the tray and open settings view.

A failed attempt invalidates and closes its device generation and clears its state-manager references. Its defaults or partially applied state cannot become the next attempt's saved state. The last good cache and pending automatic animation intent remain available. The monitor's accepted fingerprint is invalidated on failure, so a failed manual refresh can be retried even if the observed USB topology has not changed.

The passive snapshot and later opening are not an atomic hardware operation. Product counts catch a partial reopen. A same-product reconnect occurring during opening is detected by the next observation of registry IDs; no stronger atomicity claim is made.

### State policy and identity

Automatic topology refresh calls `refresh(false, true)`: it restores the last application-known state without applying the startup preset. Existing explicit startup, manual refresh, and power-event callers retain their state choices.

The cache stores deep copies of the mode and arguments plus the additional state already supplied by each device class, such as brightness, DPI, and polling rate. An absent device does not erase its entry. Mouse `ledEffect` is added to the existing state reset dispatch so that this existing mode is not silently omitted during restoration.

The native driver does not expose a physical serial identity. Cache keys therefore use `mainType:productId`, and restoration is skipped when identical products make a match ambiguous. Ambiguous entries are removed from the cache. This cannot distinguish a replacement physical device of the same unique model from the previously disconnected device; it follows the application's existing product-based settings model.

The cache is in memory. It restores states known to this process, not an arbitrary lighting state changed outside the application or a state from a previous process lifetime. Existing startup presets remain the mechanism already available across application restarts.

### Native handle lifetime

Device objects receive wrappers bound to a device-generation counter. Closing devices increments that counter before destroying effects or releasing native handles. Calls retained by an old menu, animation, or renderer object can no longer reach a replacement table through a reused internal index.

The manager retains and destroys pending objects as well as active objects. It uses `Promise.allSettled` so one failing initializer does not cause the native table to be released while another initializer is still using it. All seven derived device classes were inspected: their native getters are synchronous, and their asynchronous initialization proceeds through the base settings load rather than a native callback.

The add-on's `CloseAllDevices` clears its own pointer and size after the library closes the by-value structure. This removes the stale owning pointer left by the previous implementation and makes a repeated close skip the freed table. The patch does not rewrite every native setter; valid generation-bound use remains essential.

Application shutdown stops observation, stops global timers, clears the state-manager list, and destroys the device manager. Queued transaction entry, each asynchronous continuation, notification, and monitor restart all check application lifetime. A finishing refresh cannot restart monitoring after disposal.

### Animation cleanup

Ripple effects share one process-level keydown dispatcher. The map of active effects owns the per-effect listeners; stopping an effect removes its captured event array from that map. The native hook stops when the last active ripple effect stops. Refresh does not unload the process-wide hook that replacement effects still need.

Ripple and wheel intervals now convert their documented 0.05 seconds to 50 milliseconds. Their `start` methods clear a prior interval, and `stop` clears the interval and its stored handle.

Global custom and spectrum cycles retain their color configuration and index. Automatic refresh preserves whether a cycle should resume, including a successful interval with zero devices. A failed automatic attempt preserves pending cycle intent for the retry. Sequence progression resumes at the next configured index; exact elapsed timer phase, transient ripple events, and animation frames are not retained.

### Tray and settings windows

During refresh, the tray displays a refreshing state and still provides Quit. Menu callbacks are bound to the generation from which the menu was built. Device-setting IPC commands require the current generation, internal ID, product ID, and device type; stale controls cannot silently target a different device.

An existing device window rebinds to the unique matching current device after refresh. It displays a disconnected message while that device is absent, and asks the user to select a device when identical products are ambiguous. It does not open a new window merely because USB topology changes.

State and color views receive current data. Renderer listeners are removed on component unmount, and settings components remount with each fresh view revision. State creation safely handles a refresh that begins before a synchronous IPC request is processed. A saved state referencing an absent device can be viewed without dereferencing an undefined device. The startup-preset description now distinguishes manual refresh from automatic restoration.

## Verification performed

- Every changed existing file was acquired in full at the pinned upstream commit. Its UTF-8 Git blob identity was independently recomputed and matched the provider's blob.
- The ten changed main-process JavaScript files passed a V8 syntax parse after removing their import/export declarations. Their bodies were never invoked. This checks body syntax; it does not validate module resolution, Electron execution, or the pinned project's transpilation.
- An independent parser applied the **serialized unified patch** to all retained preimages. All 48 hunk ranges and counts matched, and all 13 resulting complete texts exactly matched the frozen source files, including final-newline distinctions. This was a text round-trip, not execution of `git apply`.
- Independent static review examined native IOKit ownership, stale native calls, shutdown, partial reopen, last-good cache preservation, and animation intent. A discovered partial-refresh cache overwrite path was corrected before freezing the source.
- Renderer JSX and C++ were read statically. Neither was compiled.

No tests, fixtures, mock devices, native-loader probes, package installation, hardware calls, permission dialogs, or CI workflow were run. The absence of those checks is explicit; syntax and source review are not substitutes for native or physical KVM verification.

## Remaining validation and publication boundary

A compatible macOS environment still needs to establish that the native add-on compiles and loads, that its existing USB permissions and supported-device library work, and that the observed KVM disconnect/reconnect restores the intended lighting and controls. Physical duplicate models, a partial reopen, application exit during settings initialization, and repeated reconnects are material integration cases identified by the code paths above. No result for these cases is claimed.

Upstream publication needs a legitimate writable fork or another established upstream contribution route. This source packet makes the implementation concrete and transferable while that route and hardware verification remain unresolved. The existing IssueHunt qualification is a source lead, not evidence that this delivery is accepted or payable.

## Source references

- [Pinned upstream tree](https://github.com/1kc/razer-macos/tree/27f8a770611c4d68d0387a980e55b79711a343f3) and [issue #452](https://github.com/1kc/razer-macos/issues/452).
- [Pinned native library](https://github.com/1kc/librazermacos/tree/325c96a62afd87debbaf4f51d8c9f569e45657bb), including its by-value close and device-opening behavior, retained in the native review.
- Apple API documentation consulted in the native review: [IOServiceGetMatchingServices](https://developer.apple.com/documentation/iokit/1514494-ioservicegetmatchingservices?preferredLanguage=occ), [IORegistryEntryCreateCFProperties](https://developer.apple.com/documentation/iokit/1514310-ioregistryentrycreatecfpropertie?changes=__1_8), [IORegistryEntryGetRegistryEntryID](https://developer.apple.com/documentation/iokit/1514719-ioregistryentrygetregistryentryi?language=objc), [IOIteratorIsValid](https://developer.apple.com/documentation/iokit/1514556-ioiteratorisvalid?language=objc), and [CFNumberIsFloatType](https://developer.apple.com/documentation/corefoundation/1543131-cfnumberisfloattype?changes=_5&language=objc). The native review retained successful indexed primary excerpts; the later root page opens exposed JavaScript-only shells. Previously unsuccessful raw-header and advertised-Markdown routes were not retried.
- [Existing-fork publication guide](https://github.com/woahwhattheheck/commons/blob/439ea39f2820425c4efbaf60c7d0c7e0feb85622/reports/bounties/gyroflow742-delivery-and-publication-route-20261004.md), read only for its actual prerequisites.
