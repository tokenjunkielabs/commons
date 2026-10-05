# Bili PR635: preserve completed declaration bundles during cleanup

This packet corrects a cleanup defect in dicnunz's existing [egoist/bili PR635](https://github.com/egoist/bili/pull/635), the declaration-bundling contribution for [issue183](https://github.com/egoist/bili/issues/183). When separate TypeScript entries are processed sequentially, the cleanup for a later entry can unlink a declaration bundle completed by an earlier entry in the same run.

The change records each output path in the existing shared preservation set immediately after its successful rename. It adds one executable line and one explanatory comment. Emission, naming, Rollup invocation, cleanup filtering, and error propagation otherwise remain unchanged.

## Exact source and attribution

| Source | Immutable identity |
| --- | --- |
| Existing external author | dicnunz |
| PR635 head | `aa9a116c35cecbffc3f0bee125e62ab272013c58` |
| PR base and observed upstream master | `843a77ba327238cefe120d5a2f695b554c83a761` |
| Original `src/index.ts` | `7b3ddc7ff25d204f482b30ac1f462524899cdab0` (27,850 bytes) |
| Corrected `src/index.ts` | `7ea2020eac1b0ee80ce9ff1c356ad827d1f516b2` (27,969 bytes) |
| Exact upstream MIT license | `cdc1c83ce67e8a934352f2e9d1868e0c12b18c88` |

The complete corrected file is `source/src/index.ts`; `preserve-declarations.patch` applies to its original path at the exact PR635 head. EGOIST's copyright, the upstream MIT license and dicnunz's original declaration-bundling work remain attributed. This packet targets PR635 specifically. The separate modern-filename correction in Commons31509 targets PR634 and must not be treated as the same complete source postimage.

## Source reasoning

The fully read source establishes this sequence:

1. `run()` turns an array of input entry strings into separate source records.
2. It captures `existingDeclarationFiles` once, before the normal JavaScript builds.
3. After those builds it uses a waterfall to call `buildDtsBundle` for each declaration source, passing the same Set object each time.
4. Each call emits declarations and scans the output directory. Its cleanup excludes files in that shared Set, plus its own output and temporary output.
5. After writing and renaming the bundle, the original implementation does not add the completed output to the Set.

Consequently, for independent entries with distinct output basenames and an initially empty output directory, the first final bundle is new, differs from the second output, and is absent from the preservation set. The second cleanup includes it and unlinks it. This is a source-derived path, not an executed filesystem observation.

The added `existingDeclarationFiles.add(outputFile)` runs only after `fs.renameSync` succeeds. The current call already excludes its own output from its cleanup list. Subsequent calls see the newly preserved final path and exclude it through the existing membership check. A failed write or rename still throws before the Set is updated. Only completed output paths are added; transient declarations continue through the original cleanup.

## Validation and scope

The full original and authored postimage Git identities matched. Applying the serialized unified patch independently in memory reproduced the complete authored postimage exactly. The production change is one hunk, +2/-0, with every prior line and final newline retained.

No dependency install, TypeScript compiler, Rollup build, filesystem emission/deletion, watch process, test suite, native execution, or deployment occurred. Existing PR author reports of local validation remain their reports. The examples and conclusions here are static source reasoning, not runtime acceptance.

This correction prevents later cleanup from deleting a completed output. It does not isolate all declaration emission from shared output paths, prevent a later emitter from overwriting an earlier file, resolve colliding custom output names, or establish correctness of every TypeScript configuration. Those behaviors remain unchanged. It does not extend watch-mode declaration output or claim the entire upstream issue is accepted.

## Current contribution and funding context

Issue183 was open and unassigned; its four comments were fully read. PR635 was open/unmerged, with four issue comments and no inline review comments. The retained current PR comment includes the author's revalidation report, a Vercel team-authorization requirement and a dependency scanner notice; this packet does not act on those account or dependency workflows.

The canonical all-state own-account PR query returned zero results for this repository. The bounded public bili search contained the original intake records, with no observed source claim for this cleanup slice. These statements describe that read scope only.

The [IssueHunt funding comment](https://github.com/egoist/bili/issues/183#issuecomment-489961099) advertises $90 on 2019-05-07. Funding provenance is not acceptance, an award, current payout eligibility or money received. No upstream PR, IssueHunt submission, contact or account action was made. A maintainer can compose the exact patch with PR635 while preserving its author and any newer upstream changes; required runtime validation and commercial follow-through remain separate.
