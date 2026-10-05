# Cocohub appointment conflict checks

This attributed continuation extends es3298's PR122 in place. Its cumulative patch preserves the rescheduled appointment's excluded ID, reuses one complete local snapshot for a suggested-slot search, supplies the requested configurable 30-minute appointment buffer, carries the actual proposed duration, makes incomplete local reads visible before saving, and keeps warning-modal reschedules on the established reschedule lifecycle.

The adjacent complete modules and `change.patch` are source artifacts for integration into the pinned contribution. No upstream branch was changed. This is not whole-issue acceptance or a bounty claim.

## Local data completeness and explicit save

In the preimage, a rejected full-pet read became an empty array. The detector then evaluated only its narrower window and could report no conflicts; both booking and rescheduling would save automatically on that result. The slot helper could likewise fall back to that partial detector and return an apparent available time. The actual local database helper also falls back to raw text after decryption and JSON parsing fail, while array readers suppress exceptions. Such unusable records must not be mistaken for an empty or fully checked set.

The additive `getAppointmentSnapshotByPetId<T>` reader now returns `{ appointments, unreadableRows }`. It uses the same SQL, ordering and legacy-compatible decryption helper as the original full-pet reader, but validates the record fields actually used by conflict evaluation: string ID/date, a usable start time under the existing date/time interpretation, and finite nonnegative duration with the existing 30-minute fallback. Raw fallback text, non-record values, invalid intervals and thrown decoding errors count as unreadable. Valid legacy JSON records remain usable. The same predicate filters the bounded fallback's candidates so its raw-text fallback cannot reach the interval evaluator. Readable appointments are retained without exposing ciphertext, row contents or provider exceptions. Query failures still reject. The existing `getAllAppointmentsByPetId<T>` and other legacy readers remain byte-for-byte unchanged; their current consumers do not adopt this conflict-specific validation.

`ConflictDetectionResult` adds `appointmentReadComplete` and optional `checkWarning`. `hasConflicts` still describes known conflicts, independently of whether appointment coverage was complete.

| Actual source outcome | Conflict result and suggestion behavior |
| --- | --- |
| Full-pet query succeeds and every row is usable by the conflict evaluator | The local appointment read is complete, including a successful empty set. |
| Full-pet query fails | Keep conflicts identifiable from the bounded read and supplied medication list; mark incomplete and omit a suggestion. |
| Full-pet query returns some undecodable or unusable rows | Keep its decoded appointments, merge other readable candidates, mark incomplete and omit a suggestion. |
| Bounded query fails but the full-pet snapshot succeeds without unreadable rows | Use the complete full-pet coverage; the narrower failure does not discard it. |
| Initial check finds conflicts, but the subsequent suggested-time search fails | Retain those known conflicts, return an explicit search warning and no suggested time. |

Both screen call paths open the existing warning modal when known conflicts exist **or** `appointmentReadComplete` is false. The modal distinguishes an incomplete check from known conflicts, displays the safe warning, and does not treat an empty partial result as an all-clear. The existing **Proceed Anyway** action remains available and records that the user chose to proceed despite incomplete local checking. **Pick a Different Time** remains available. This does not add an account, permission or save-authorization gate.

The direct `findNextAvailableSlot` helper now rejects with an explicit incomplete-check error if its full snapshot query fails or contains unreadable rows. It does not return a date from a partial fallback. Its normal `undefined` result still means that the bounded search found no candidate in the data it successfully checked. The detector catches a failed suggestion search and carries the warning to the existing caller.

Completeness here is specifically the local appointment read used by this calculation. It does not establish that local storage is synchronized with every server record, that the caller's supplied medication list is current or complete, or that data cannot change after the read. Validation of fields unused by the conflict evaluator, medication-source loading and server synchronization remain outside this change. No slot is reserved and no atomic check-and-save guarantee is added.

## One snapshot per suggested-slot search

The original helper called the detector for every candidate, running both a moving-window query and the identical full-pet query each time. The inspected `localDB.ts` (preimage blob `2703bfd3c021534522b3b44fec12701ab4ebd7c1`) shows that both query the same SQLite appointments table and decrypt rows. The full-pet read includes appointments omitted by the narrower start-time window, including long and overnight intervals.

The search now reads and deduplicates one complete full-pet snapshot and evaluates every candidate against it. A successful empty snapshot is valid. It is kept only within that invocation; a later invocation reads again. A failed or partially decoded snapshot rejects instead of becoming empty data or starting repeated fallback checks.

For K examined candidates, with 1 <= K <= 336, a successful direct slot-helper call performs one local query/decryption pass instead of 2K queries, including K full-pet decryption passes. Candidate-by-appointment comparisons remain O(KA). No measured latency or constant-time-search claim is made. The initial standalone detector still attempts a bounded read and the full-pet snapshot. Existing invalid/out-of-range candidate-window checks run before a candidate database read. The search remains nonrecursive, advances hourly and examines at most 336 candidates.

## Configurable spacing and actual duration

Issue49 explicitly requires a configurable appointment buffer with a 30-minute default. `DEFAULT_APPOINTMENT_BUFFER_MINUTES` supplies that value. The booking and rescheduling forms expose **Appointment gap warning (minutes)** and pass it before saving. The value is local to this screen, starts at 30 and is not persisted or attached to the appointment.

Blank, negative, nondecimal, nonfinite and unrepresentable date-window inputs show an alert before the conflict check. Zero and decimal minutes are supported. The service independently rejects nonfinite or negative buffer minutes, including conversion to nonfinite milliseconds, before reading the database.

The threshold is compared once with the existing free gap between appointment intervals; it is not added to both appointments. The existing inclusive boundary remains: a gap equal to the threshold is warned about. Overlapping or touching intervals have zero gap and remain conflicts with a zero buffer.

The caller also passes its existing `Appointment.durationMinutes`, falling back to the model's 30 minutes. The same value reaches the initial evaluator and every suggested candidate. This corrects the preimage's fixed 30-minute proposed interval, which could be shorter than the appointment that rescheduling would save. No duration setting or new duration policy is introduced.

| Function | Appended optional arguments |
| --- | --- |
| `detectConflicts` | Sixth: appointment buffer minutes, default 30. Seventh: proposed duration minutes, default 30. |
| `findNextAvailableSlot` | Fourth: excluded appointment ID. Fifth: appointment buffer minutes, default 30. Sixth: proposed duration minutes, default 30. |

Existing positional callers remain valid. The current rescheduling caller forwards `detailAppt.id` through every suggested candidate, preserving self-exclusion. The one-hour `CONFLICT_BUFFER_MS` remains the medication proximity window and hourly search step. Buffer configuration does not change medication scheduling or supervision classification.

The computed suggestion already has a consumer: the screen displays it and **Use Suggested Time** explicitly saves the changed date/time while preserving other pending appointment fields. That action is offered only for a complete result with a suggestion. No automatic acceptance or duplicate suggestion control was added.

## Rescheduling after a warning

The preimage's warning-modal actions always called the generic appointment saver. A conflict-free reschedule instead used `doReschedule`, which cancels the old reminders and calendar event, calls the dedicated reschedule service, schedules the replacement reminders, syncs the calendar, and updates the detail view. The provisional warning record also retained the old `time` and changed the status to `PENDING`.

The modal now records whether its pending operation is a booking or reschedule. **Proceed Anyway** and **Use Suggested Time** dispatch accordingly. Booking keeps its existing saver. A reschedule passes the actual pending record and chosen date to the existing reschedule path, so the selected appointment ID and duration remain explicit even if detail state changes. The provisional record carries the proposed time and `RESCHEDULED` status. Completing or dismissing the modal clears its pending action.

`doReschedule` forwards the existing duration (or the model's 30-minute default) to the service's already-supported fourth argument. It retains the existing reminder/calendar cleanup and recreation, service fallback and detail refresh. For a warning choice, the returned rescheduled record goes through the existing note-aware `saveAppointment` once to retain the user's explanation; the outer fallback no longer appends that note itself. This can add an update request after the reschedule request. It is not an atomic operation or a server-side reservation, and it does not change the existing best-effort reminder/calendar error handling. No reschedule endpoint, request field, permission or recurrence rule is invented.

## Consistent local date and time for rescheduling

The dedicated reschedule endpoint receives separate `date` and `time` fields. The retained `Appointment` model defines them as `YYYY-MM-DD` and `HH:MM`, and the service's local fallback stores that pair unchanged. Conflict evaluation reconstructs a date-only record as local date plus local clock.

The screen previously took the calendar day from `toISOString()` (UTC) and the clock from `toTimeString()` (local). Those components can describe a different day than the user's selected `Date` near a local/UTC day boundary. It now derives the year, month and day with local getters and keeps the existing local-clock extraction. The screen's outer reschedule fallback saves the same separate pair, rather than reverting to a full ISO datetime. Normal reschedules and both warning-modal choices share this conversion.

The adjacent booking, provisional and suggested-choice records still carry their existing full ISO instant until their established persistence route is chosen; the immediate checks and pending reschedule routing parse that instant. This narrow correction does not change those representations, general list/display interpretation, input parsing, timezone selection, daylight-saving ambiguity policy, stored-record migration or server behavior. IDs, duration, conflict calculations, explicit save choices and reschedule lifecycle remain as documented above. No server, simulator, timezone experiment or native scheduling operation was executed.

## Source and attribution

- Original issue: https://github.com/cocohub-mobileapp/cocohub-main/issues/49
- Existing contribution: https://github.com/cocohub-mobileapp/cocohub-main/pull/122 by **es3298**.
- Immutable contribution head: `3f9f6894dfb651aaab3b2b85a90b3b3c2f0fa941`; OPEN and unmerged when refreshed on 2026-10-05.
- Contribution base: `d33dd0c6ee1e0b3fb967c1929c7556b4bb152df2`.
- `src/services/appointmentService.ts`: `ef9f8c873d85aff8824f5a1110d46b48078ff8df`.
- `src/screens/AppointmentScreen.tsx`: `dc60c11007086f15b4aeb11a515cb65e579b0d9e`.
- `src/services/localDB.ts`: `2703bfd3c021534522b3b44fec12701ab4ebd7c1`.
- `src/models/Appointment.ts`: `3108dd028d1585345afca973c9a5a455439cd9e4`.
- Settings/schema inspected, unchanged: `src/screens/SettingsScreen.tsx`, `df7f2585b237a5acb1cda51bd919252178968180`; `src/models/User.ts`, `b4e2a00a3f7c9d7861094d8ce117225ac3382ffa`.
- Root contribution instructions: `e54062fc177bebd5da71ec227366e3f6734015b0`.
- Included unchanged MIT license: `6896ef04cbbb9416187df44463695959cbdf629d`. Copyright remains PetChain, Inc.; es3298's existing interval and recursion corrections are preserved.

Issue comment4878529319 separately links niteshcongreja321's `fix/issue-49-appointment-conflicts` branch. Its inspected service `03ed1d62745643a3a30751f00bdf19ac3dfae8d2` uses a different options signature. This patch targets PR122; do not overwrite that broader contribution or apply these positional arguments blindly to it.

An older coordination handoff named ZZ-Sol-Peregrine-913's intended tokenjunkielabs branch. Its exact request was rejected with INVALID_ARGUMENT before source acquisition. No historical payload was reconstructed, and no content identity, completion or ownership transfer is inferred for it.

## Integration and remaining scope

Apply `change.patch` once to the pinned PR122 source. The adjacent complete service, caller and local database modules are the resulting source. This cumulative patch composes the exclusion correction from Commons31652, snapshot reuse from31660, configurable buffer from31664, duration propagation from31669, the incomplete-read warning flow from Commons31683, the warning-modal reschedule routing from Commons31687 and consistent local reschedule date/time fields. With newer source, compose these hunks instead of replacing entire modules.

The inspected appointment model has no recurrence frequency, series identifier, exceptions or rule contract. The current user/settings schema likewise has no persistent appointment-buffer preference. Recurrence and any persistent setting require a separate concrete model; this continuation invents neither.

Validation is source inspection of the retained production paths and their actual data contracts, changed-source reasoning and exact Git readback. No application, TypeScript compiler, formatter, linter, tests, simulator, backend, wallet or booking operation was run. Historical reported checks are not rerun or adopted. Native UI and maintainer acceptance remain outstanding.

Cocohub's contribution instructions require maintainer assignment for bounty intake. The original contributors retain their work and claims. No assignment, upstream submission, award or payment was requested or inferred.
