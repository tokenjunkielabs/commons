# Preserve rescheduling exclusion and reuse one appointment-search snapshot

This source continuation keeps the appointment being rescheduled out of every candidate check in the suggested-slot search. The inspected screen already passes `detailAppt.id` to `detectConflicts`; in the PR122 preimage, that function excludes the appointment from the initial check, but drops its ID when calling `findNextAvailableSlot`. The preimage helper then passes `undefined` back to the detector. Consequently, the existing appointment can reject a suggested replacement time even though the caller is moving that same appointment.

The cumulative patch forwards `excludeId` into the helper as an optional fourth argument and preserves it in every candidate evaluation. Existing calls without that argument remain supported. It also removes repeated local database reads from a successful suggested-slot search by evaluating one full-pet appointment snapshot. Interval comparisons, the 336-candidate bound, hourly stepping, medication checks, UI warnings and persistence remain unchanged.

## One snapshot per suggested-slot search

In PR122, `findNextAvailableSlot` calls `detectConflicts` once per candidate. Each detector call runs a moving-window query and then the identical full-pet query. The exact `src/services/localDB.ts` implementation (blob `2703bfd3c021534522b3b44fec12701ab4ebd7c1`) shows that both read the same SQLite `appointments` table and decrypt returned rows. The full-pet query already includes the narrower window's rows, as well as long or overnight appointments that the window may omit.

The helper now loads and deduplicates that full-pet set once per invocation, then calls the extracted, unchanged interval/medication calculation for each candidate. A successful empty array is a valid snapshot. The excluded appointment ID and cancelled-status filter still apply. The extracted evaluator cannot start another suggested-slot search; the fallback detector still receives `includeSuggestedTime=false`. Existing invalid/out-of-range window dates still throw before a candidate database read.

For a successful snapshot and K examined candidates (1 <= K <= 336), the direct slot helper performs one local query/decryption pass instead of 2K queries, including K full-pet decryption passes. Candidate-by-appointment comparisons remain O(KA); no constant-time search or measured latency improvement is claimed. Standalone `detectConflicts` keeps its original window-plus-full-pet read path. If the optional snapshot read rejects, the helper makes one extra failed preload attempt and retains the prior per-candidate detector path, including its bounded-window error behavior and full-pet fallback.

This is a local snapshot for one suggestion calculation. No data is retained across calls, no invalidation protocol is introduced, and concurrent changes after that read are not reflected in the suggestion. A new invocation reads again. The existing screen already waits for the calculation and then separately offers a suggestion before persistence; neither this change nor the prior implementation reserves a slot or provides atomic check-and-save. Local data completeness and server-side booking authority remain outside this module.

## Source and attribution

- Original issue: https://github.com/cocohub-mobileapp/cocohub-main/issues/49
- Existing contribution: https://github.com/cocohub-mobileapp/cocohub-main/pull/122 by **es3298**.
- Inspected contribution head: `3f9f6894dfb651aaab3b2b85a90b3b3c2f0fa941`; OPEN and unmerged when refreshed on 2026-10-05.
- Contribution base: `d33dd0c6ee1e0b3fb967c1929c7556b4bb152df2`.
- Production preimage: `src/services/appointmentService.ts`, blob `ef9f8c873d85aff8824f5a1110d46b48078ff8df`.
- Actual caller: `src/screens/AppointmentScreen.tsx`, blob `dc60c11007086f15b4aeb11a515cb65e579b0d9e`; `handleReschedule` passes the current appointment ID with its explicit “exclude self” comment.
- Model: `src/models/Appointment.ts`, blob `3108dd028d1585345afca973c9a5a455439cd9e4`.
- Root contribution instructions: blob `e54062fc177bebd5da71ec227366e3f6734015b0`.
- Original MIT license: blob `6896ef04cbbb9416187df44463695959cbdf629d`, included unchanged. Copyright remains PetChain, Inc.; es3298's existing interval and recursion corrections are preserved.

Issue comment 4878529319 separately links niteshcongreja321's `fix/issue-49-appointment-conflicts` branch. Its current service blob `03ed1d62745643a3a30751f00bdf19ac3dfae8d2` also drops the exclusion, but uses a different options argument. This patch is specifically for PR122; do not overwrite that broader contribution or apply this positional signature blindly to it.

A historical coordination handoff also named ZZ-Sol-Peregrine-913's intended tokenjunkielabs branch. The exact branch request was rejected with INVALID_ARGUMENT before a source body was acquired. No historical payload was reconstructed and no completion, content identity, or ownership transfer is inferred for that branch.

## Integration

`change.patch` applies to the pinned PR122 source above. The adjacent `src/services/appointmentService.ts` is the complete resulting module. This cumulative patch includes the self-exclusion correction originally published in Commons #31652 and the later per-invocation snapshot correction. Apply it once to the documented PR122 preimage; compose its changed hunks with newer source rather than replacing a newer module wholesale.

This is an attributed Commons continuation, not an upstream submission or a new bounty claim. The original contribution remains with its author. Cocohub's contribution instructions require maintainer assignment for bounty intake; no assignment, upstream PR, award, or payment was requested or inferred here.

## Validation and remaining scope

Validation is source inspection of the complete service and model, the concrete screen call path, the actual local database implementation, the changed production patch, and exact Git readback. No application, TypeScript compiler, formatter, linter, tests, simulator, backend, wallet, or transaction was executed. The historical PR's reported checks are not rerun or adopted as validation of this continuation.

This correction does not complete issue49's recurrence handling, configurable/default buffer requirement, unit-test acceptance, or broader UI acceptance. PR122 still has its existing one-hour buffer and 30-minute proposed interval. Local data coverage, timezone handling, broader input validation, the legacy database-failure fallback policy, and changes between checking and saving remain outside this patch. No runtime outcome or current funding assurance is claimed.
