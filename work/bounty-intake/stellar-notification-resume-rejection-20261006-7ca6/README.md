# Retain notification audio-resume failures

This packet changes one call in `src/hooks/useNotificationSound.ts`: attach a
rejection handler to the existing `AudioContext.resume()` Promise and send its
failure to the hook's existing warning sink. It preserves the synchronous
`playSound` interface and the existing sound scheduling.

## Exact source and caller

Repository: `Stellar-Analysis/frontend`.

Observed main and immutable input commit:
`482ee456369418ef82c4056718cb82d3468f762b`.

| Source | Git blob | UTF-8 bytes |
| --- | --- | ---: |
| Complete hook preimage | `5fc9fe895921224065cfd0f3ea4441d0d824fc9e` | 3,919 |
| Proposed hook postimage | `2dd1c2f3701ed85dfc9195b545a0aab8bc106974` | 4,022 |

The hook was acquired once by its immutable native blob locator and its complete
text independently matched that identity. A separate current main observation
still matched the input commit. The patch is +3/-1 and touches no other source
path.

The actual connected caller is `src/contexts/NotificationContext.tsx`, blob
`8a05dbf6fb720af3f876baef6b14f035d02b6c51`, at the same commit. Its complete
`showToast` function and hook-use contract were transferred from the CI lane's
already acquired full source. It destructures `playSound`, calls it only when
`preferences.sound.enabled`, and passes those settings plus the notification
type and priority. It returns the toast ID synchronously and does not await a
sound Promise. The default settings enable sound at volume 0.5 with the default
sound type.

The retained types in `src/types/notifications.ts`, blob
`ab97b18fd0e9c78562181659141660e8a92c21ec`, define enabled/volume/soundType,
with the four sound types default/subtle/alert/critical and priorities
low/medium/high/critical. This packet does not alter that contract.

The one-row path history at the exact input commit returned
[59fad72d9fbef9cfd6f47e215392da44488fcdc4](https://github.com/Stellar-Analysis/frontend/commit/59fad72d9fbef9cfd6f47e215392da44488fcdc4),
authored by christabel888, for relocation of the existing frontend tree to the
repository root. That is attribution for the observed relocation, not a claim
that this author originally wrote every hook line or that the bounded history
is complete.

## Demonstrated error boundary

The original hook checks whether its context is suspended, calls
`audioContext.resume()`, then continues building and scheduling the existing
oscillators. Its surrounding synchronous catch already logs setup exceptions,
but it does not handle later rejection of the returned Promise.

The [Web Audio API resume algorithm](https://webaudio.github.io/web-audio-api/#dom-audiocontext-resume)
returns a Promise and explicitly specifies rejection, including failure during
resource acquisition. The acquired primary source is the public editor's draft;
its normative API description establishes this asynchronous error boundary,
not a successful browser execution or compatibility result.

The patch attaches `.catch` immediately and uses the exact warning message and
logger call already present in the hook's outer catch. The `void` expression
makes the existing non-awaited calling convention explicit. A synchronous throw
from invoking resume still reaches the existing outer catch. A rejected resume
Promise now reaches the same warning sink instead of being left unhandled.

This preserves the existing logger behavior; it does not make that sink
infallible or provide durable error storage. The patch does not wait for resume
before scheduling tones, retry resume, prompt for permissions, or claim that
audio successfully started.

## Scope and remaining limits

The enabled/SSR checks, context construction and reuse, priority mapping, sound
configuration, volume clamp, oscillator/gain construction, timing, critical
second-tone timeout, caller interface, and synchronous setup catch remain
unchanged. No notification type, sound preference, desktop notification, toast
dismissal, or Auto Hide behavior is edited.

The exported cleanup callback remains unchanged. The acquired caller does not
destructure or invoke it; this packet does not claim a resource-lifecycle fix.
Its existing close Promise and delayed critical-tone callback have separate
boundaries that are not repaired or exercised here. No timer cancellation,
unmount safety, stale-setting cancellation, audio permission, browser lifecycle,
or wider notification reliability claim is made.

No browser, audio device, AudioContext, permission prompt, notification,
application, conversion, build, lint, fixture, test, or workflow was run.
Validation is complete hook inspection, retained actual caller/type contracts,
primary Promise-return semantics, exact narrow source edits, source/artifact
identities, and ordinary publication readbacks. Runtime acceptance remains
unperformed.

## Attribution and publication

This is an attributed Commons source continuation, with a patch and this guide.
The complete upstream hook and caller are not republished. Original source
credit remains with their upstream contributors; CI supplied retained caller
evidence and independently owns the disjoint NotificationSystem Auto Hide hunk.

The donor tree's differently attributed MIT notices are already preserved
verbatim under
`work/bounty-intake/stellaranalysis-issue-generator-layout-20261006-7ca6/`:

- `upstream-licence-mclaughlin.md`:
  `57740b9d4d86aedf5d518f2f363d5cf192c54127`.
- `upstream-license-menke-laguna.md`:
  `af5411fa243cfcf2b61c79d081dbb6204e956041`.
- `upstream-license-de-wet.md`:
  `4a766e268772888af5df56c3f6c608f68558b789`.

Those retained notices are referenced without assigning one notice a
repository-wide scope. No upstream claim, PR, submission, account, payment,
permission change, or production action is performed.
