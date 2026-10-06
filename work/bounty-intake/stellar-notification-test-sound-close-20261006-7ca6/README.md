# Close each completed notification test tone's private audio context

The mounted Notification Preferences panel has a Test Sound button. Each invocation allocates a new AudioContext, oscillator and gain node, then schedules the oscillator to stop after 0.2 seconds. The original handler never closes that private context after the tone ends. This patch attaches completion cleanup before starting the oscillator.

## Donor and attribution

Repository: https://github.com/Stellar-Analysis/frontend

Exact donor main: `482ee456369418ef82c4056718cb82d3468f762b`; the current main-ref guard for this new task returned that commit.

| Path | Donor blob | Evidence |
| --- | --- | --- |
| `src/components/notifications/NotificationPreferences.tsx` | `fd1482e38a34d706b675e6a2038e57101e4a3ffc` | Complete actual button, private allocation, graph setup and scheduled stop; patch target |
| `src/components/notifications/NotificationBell.tsx` | `8e17fc08741d51bda9d0b3169a4b563fd528e89b` | Settings button mounts the preference panel |
| `src/components/notifications/index.ts` | `812d23234012d75770a798e7ad4f6c7be77b1e58` | Resolves the actual Navbar import |
| `src/components/navbar.tsx` | `1d519697311060e2d72c1a8fcaa59d1eb6148277` | Renders NotificationBell |
| `src/app/[locale]/layout.tsx` | `1f016787657313d58504e79bccbe634a843ce8b5` | Retained mounted Navbar/provider evidence |
| `src/lib/logger.ts` | `7c99dbe969798e1b1b7a8a80a18c6c26110c4682` | Complete actual warning API; no backend call in warn |

This continues the original Stellar-Analysis contributors' implementation and preserves their authorship. No new upstream PR, assignment, maintainer acceptance, reward or payment is claimed. A bounded public search for NotificationPreferences plus AudioContext returned zero results. The preceding repository notification-title PR search also returned zero; these limited queries do not prove global absence. Infra confirmed its separate completed source scope changes only useNotificationSound resume rejection, not this panel.

## Primary API contract

- [MDN: AudioScheduledSourceNode ended event](https://developer.mozilla.org/en-US/docs/Web/API/AudioScheduledSourceNode/ended_event) states that the event fires when a source stops, including its scheduled stop time, and supports the onended handler property.
- [MDN: AudioContext close](https://developer.mozilla.org/en-US/docs/Web/API/AudioContext/close) documents release of system audio resources and a returned Promise. Closing a context is not a guarantee that every associated JavaScript object has been collected.

Those contracts establish a completion point for this source-owned context. No sample, audio API, browser, permission prompt or application code was run.

## Source change

`close-test-sound-context.patch` has two hunks, +7/-0. It imports the already existing logger and installs an onended callback before the existing oscillator.start and oscillator.stop calls. That callback closes only the AudioContext captured by this Test Sound invocation. A rejected close promise is handled with a fixed warning string, without logging preference values or an error payload and without adding a backend request.

The 800 Hz sine tone, volume envelope, 0.2-second stop, original platform selection, enabled guard, and button behavior are unchanged. Concurrent clicks have their own contexts and callbacks; this patch does not introduce shared ownership or close the provider's separate notification-audio context.

The original warning helper may suppress warnings according to its existing environment configuration. This is a cleanup attempt on the actual ended event, not a guarantee of audible output or successful resource release on every platform. No change is made to context construction/setup exceptions, suspended contexts whose scheduled audio time does not progress, resume/autoplay policy, permission handling, component-unmount cancellation, or the broader shared hook's cleanup behavior.

## Applying and composition

Target: `src/components/notifications/NotificationPreferences.tsx`, mode 100644.

Preimage: `fd1482e38a34d706b675e6a2038e57101e4a3ffc`, 15,996 UTF-8 bytes.

Postimage: `083079fe5bf4cb532dd614b6ae9a95594ae21af6`, 16,207 UTF-8 bytes.

The original absence of a final newline is preserved. Apply the exact patch to the pinned donor and compose with any newer panel edits; do not overwrite a newer module. The completed Auto Hide renderer patch (#31934) and audio resume patch (#31935) affect different source files. Existing Navbar and other completed UI packets remain independent.

## Integrity, instructions and limits

Complete literal forward/inverse replacement and serialized patch reconstruction are checked against the stated source bytes and Git identities. These are source integrity operations only. No TypeScript/compiler, lint, tests, fixture, sound, runtime, device or UI accessibility validation was performed.

The retained complete donor tree had no AGENTS.md or RULES.md. Its observed `docs/CONTRIBUTING.md` (`f66db3b0eece27eb6fa888948c31ee8c7eabcfd2`) gives EventSource-specific test/release guidance; this task is not that release workflow. Session instructions prohibit execution, tests and publication to upstream/package registries.

The donor's differently attributed documentation MIT notices do not establish a repository-wide licence for this production module. This Commons packet includes only the focused patch and this original integration guide, not the full source. Preserve original contributor rights and any external acceptance conditions.
