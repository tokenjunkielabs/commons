# Bili PR634: retain both outputs with extensionless filenames

This packet corrects a filename collision in dicnunz's existing [egoist/bili PR634](https://github.com/egoist/bili/pull/634), which implements the legacy/modern output option requested by [issue182](https://github.com/egoist/bili/issues/182). A custom extensionless output template such as `[name]` or `bundle` is passed to both build tasks. The original modern suffix replacement only matches a terminal extension, so it leaves those filenames unchanged and directs both variants to the same path.

The production change makes that terminal extension group optional. It inserts `.modern` before a matched extension, or appends `.modern` when none is present. The source API comment documents both cases. All other existing PR634 production behavior is preserved.

## Source and attribution

| Source | Exact identity |
| --- | --- |
| Existing external author/carrier | dicnunz, egoist/bili PR634 |
| PR634 head | `026b4b5d0e632ea8f8e8a1f038438779df788a9e` |
| PR base and observed upstream master | `843a77ba327238cefe120d5a2f695b554c83a761` |
| Original `src/index.ts` | `905e118403cc1879fea3d80bb9cf9ed3b6126995` |
| Corrected `src/index.ts` | `e973e1000dc869e531946b13691e328993ed75f6` |
| Original `src/types.ts` | `02dbd0cdbe17d7d5361c4a7bb9b3882947c5ad35` |
| Corrected `src/types.ts` | `bef28da84fa8bd1fb24a7902126cb3175c1f94fb` |
| Current upstream README | `f6c7dd3bdee865c06f642e6fa49ce4845e588f01` |
| Exact upstream MIT license | `cdc1c83ce67e8a934352f2e9d1868e0c12b18c88` |

EGOIST's project copyright and dicnunz's modern-build implementation are preserved. The `source/` directory contains complete corrected files, `modern-filenames.patch` targets their original upstream paths, and `LICENSE` is the complete upstream MIT license.

## Concrete source contract

The fully read `ConfigOutput.fileName` declaration accepts a string or callback returning a filename template; it does not require an extension. The existing implementation constructs legacy and modern tasks for the same source and format, resolves the template, and passes it as Rollup's `entryFileNames` in the same output directory.

The prior expression is:

```ts
fileName = fileName.replace(/(\.[^./]+)$/, '.modern$1')
```

The corrected expression is:

```ts
fileName = fileName.replace(/(\.[^./]+)?$/, '.modern$1')
```

The optional group retains the original match and replacement when a terminal extension exists. When no extension matches, the end-of-string match inserts the suffix without removing filename text. The enclosing condition still applies only to a modern build whose original template did not contain `[modern]`.

Reasoned filename consequences, not executed bundle results:

| Custom template | Legacy filename | Modern filename |
| --- | --- | --- |
| `bundle` | `bundle` | `bundle.modern` |
| `[name]` | `[name]` | `[name].modern` |
| `chunks/[name]` | `chunks/[name]` | `chunks/[name].modern` |
| `bundle.js` | `bundle.js` | `bundle.modern.js` |
| `[name][modern].js` | `[name].js` | `[name].modern.js` |

Rollup still resolves `[name]` later. Legacy filenames, explicit-placeholder handling, Babel options, task scheduling, watch behavior and the existing external test files are unchanged. This packet does not establish that every other modern-output or bundling configuration is correct.

## Validation and limits

The complete retained source bodies were checked against their Git blob identities. Both independently applied serialized patch hunks reproduce the authored postimages exactly, with one runtime-source line changed and one API comment expanded: two hunks, +3/-2 overall. The rest of both source files is byte-for-byte preserved.

No dependencies were installed; no TypeScript compiler, Rollup/Babel build, watch process, test suite, native executor, or deployment was run. The filename examples above follow from the expression and surrounding source, rather than a runtime observation. Existing author reports of successful checks remain attributed to that author.

PR634 was open/unmerged with three issue comments and no inline review comments. The latest author comment reports local revalidation; the Vercel comment requires team authorization, which this work does not request or change. The exact all-state own-account PR query returned zero results, and the bounded public bili search contained the original intake only. These observations describe the read scope, not a universal ownership census.

## Funding and follow-through

The original [IssueHunt funding comment](https://github.com/egoist/bili/issues/182#issuecomment-489960827) records $90 on 2019-05-07. The current issue body continues to list that amount and PR634. This is advertised funding provenance, not confirmation of an award, escrow availability, current payout eligibility, or money received.

This internal Commons packet does not create or modify an upstream PR, submit through IssueHunt, contact a maintainer, or replace the external author. Any upstream composition should use the exact PR634 head or compare a newer source revision first. The distinct declaration-output PR635 and watch-error proposals remain separate contributions. Runtime validation, external acceptance and commercial follow-through remain unresolved.
