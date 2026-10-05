# Majo #9: commit duplicate source files in source order

Canonical issue: https://github.com/egoist/majo/issues/9
Existing contribution: https://github.com/egoist/majo/pull/15

This packet supplies a narrow production follow-up to janat08's existing `doubleSource` contribution at commit `9253f596b9353e49e9f68a08bc6ff2f6b48639c8`. It preserves the original contribution and egoist's MIT license. It does not advance the upstream PR or create a platform claim.

## Concrete behavior

The pinned PR's `docs/api.md` says multiple source calls return the last found file for duplicate names and emit a warning. Its `process()` builds an ordered array of source/glob results, but assigns `this.files[stats.path]` inside parallel file-read callbacks. Two sources containing the same relative path can therefore choose a winner according to filesystem completion order.

The candidate keeps glob acquisition and file reads concurrent. Each read returns its full file record; after `Promise.all` succeeds, the returned records are committed in that array's order. A later configured source therefore overwrites an earlier source's duplicate relative path, independently of read completion. Within each source, the existing glob-result ordering remains authoritative. The existing duplicate warning text, file record fields and middleware-after-load order are retained.

If a file read rejects, the returned process promise still rejects and middleware does not run. The candidate leaves the newly reset files map empty until all reads succeed; the old implementation could expose partial writes and further in-flight callbacks could continue mutating it after rejection. No cancellation, concurrent-process protection, sorting, collision error policy or alternate filesystem behavior is introduced.

## Apply within the existing contribution

`src/index.js` is the complete intended postimage. `source-order.patch` contains the sole source change against blob `fd98a1058893ec28b02b93b41ad402557f0670da`. Expected postimage is `940e60f60e212ac269e010a20cd1cfb866900a1c`. Reconcile any moved upstream head before applying; this historical JavaScript file is not a direct patch to current TypeScript master or other open proposals.

The API documentation, rename implementation, source accumulation and all other methods remain byte-for-byte unchanged by this packet. Original test/debug files were neither copied nor altered. `source.json` records exact source identities and boundaries; `LICENSE.upstream` is the unchanged original license.

## Evidence and remaining boundary

Complete pinned source/docs and the current issue/PR chronology were read. The source change is one exact replacement whose inverse reproduces the full preimage. The unified patch's removed and added regions match the intended source hunk. These are source checks, with no program execution, filesystem reads, tests, fixtures or hosted workflow run.

The issue remains open. Its eight-comment chronology includes the maintainer's historical statement that merging depends on finding a use case; that remains separate from this concrete ordering correction. The advertised historical funding does not establish current allocation, sponsor acceptance, merge or payout. The existing external PR retains janat08's authorship. Current own-PR/carrier searches returned no matching items, with query application unverified. No shared-fork access retry, upstream mutation or external contact occurred.
