# Preserve the logger sink and reset console-pattern scan state

This patch changes only `scripts/replace-console-statements.mjs` in the pinned
Stellar-Analysis/frontend source. It prevents the utility from converting its
own target logger and makes both existing pattern checks start at the beginning
of each file. No conversion has been run and no application source is changed
by this Commons packet.

## Exact source and connected contract

Repository: `Stellar-Analysis/frontend`.

Input commit: `482ee456369418ef82c4056718cb82d3468f762b`.

| Source | Git blob | UTF-8 bytes |
| --- | --- | ---: |
| `scripts/replace-console-statements.mjs` preimage | `89d67eb36bee3f419a0922ba3abab819fda09383` | 4,676 |
| Proposed utility postimage | `ef50fd47f98a0f72cfc7b7520751ee756980e705` | 4,966 |
| `src/lib/logger.ts`, read-only input | `7c99dbe969798e1b1b7a8a80a18c6c26110c4682` | 11,575 |
| `tsconfig.json`, read-only input | `16eae33a28d532523720d66061cf9ac4b85c69a7` | 1,000 |

The complete utility and logger were acquired by their immutable blobs.
The pinned `src/lib` directory independently identified the logger path and
blob. The complete TypeScript configuration maps `@/*` to `./src/*`, so the
utility's inserted `@/lib/logger` import resolves to that actual source.
All three complete input texts independently match the stated Git blob
identities. The proposed postimage adds seven lines and removes none.

The utility's own documented entrypoint is
`node scripts/replace-console-statements.mjs`; its existing `main()` invokes
`glob` with the repository root as cwd and absolute paths, then calls
`processFile` for each result. Its selected TypeScript source patterns include
the target logger's real path.

A one-row, path-scoped history response at the same commit identifies
[59fad72d9fbef9cfd6f47e215392da44488fcdc4](https://github.com/Stellar-Analysis/frontend/commit/59fad72d9fbef9cfd6f47e215392da44488fcdc4),
authored by christabel888, as the latest returned commit for this utility.
That commit describes moving the existing frontend tree to the repository root
and includes its own co-author attribution. This is attribution for the observed
relocation, not a claim that the relocation author originally wrote every line
of the utility or that the bounded history response is complete.

## Two demonstrated source defects

The actual logger exports `logger` and deliberately uses `console.debug`,
`console.info`, `console.warn`, and `console.error` inside its sink methods.
The utility currently scans that same file. Replacing the sink calls with
`logger.*` calls redirects those methods back into themselves when their
logging branches run. Existing environment checks do not make that a correct
sink transformation.

The patch returns the existing unmodified/unprocessed result for the exact
resolved logger path before reading or writing it. The comparison uses the
already imported `path` module and the existing module-relative repository
location. It does not depend on changing glob's exclusion semantics. It is a
lexical resolved-path comparison, not a filesystem identity or symlink
enforcement mechanism.

Separately, all five replacement patterns have the global flag. The detection
loop calls `pattern.test(content)`, then the replacement loop calls the same
pattern's `test` again. A successful first check advances the pattern's
`lastIndex`; the second check can start after the file's only occurrence and
skip its replacement.

The [ECMAScript RegExpBuiltinExec algorithm](https://tc39.es/ecma262/multipage/text-processing.html#sec-regexpbuiltinexec)
reads `lastIndex` for global matching and updates it to the match end.
[RegExp.prototype.test](https://tc39.es/ecma262/multipage/text-processing.html#sec-regexp.prototype.test)
delegates to that matching operation. The patch assigns `lastIndex = 0`
immediately before each of the two existing checks. Each presence check
therefore examines the complete current file, independently of an earlier
check. This is a source-derived explanation, not an executed reproduction.

## Exact scope

Only the utility is patched. The five mappings remain unchanged:
log/debug to debug, info to info, warn to warn, and error to error. Existing
file patterns, test/spec patterns, ignore list, root anchoring, sequential file
loop, import detection/insertion, replacement strings, writes, counters, summary
text, and caught-error behavior remain intact. No dependency, package, lockfile,
workflow, permission, configuration, or production logger edit is included.

This remains the existing regex-based converter. The patch does not establish
syntax-aware treatment of comments, strings, directives, shadowed names, import
aliases, or arbitrary console argument lists. In particular, the connected
logger's methods have their own typed message/metadata/error contracts; this
packet does not claim that every arbitrary console call can be converted without
semantic review. The original utility's request to review converted changes
remains relevant.

No conversion, filesystem write by the utility, logger call, environment or
credential lookup, Sentry call, backend call, application build, fixture,
test, benchmark, or workflow execution was performed. The exact utility
postimage was authored by text edits only. Validation is the complete source
chain, primary language semantics, exact narrow hunks, and artifact/source byte
identities. Runtime acceptance remains unperformed.

## Attribution and publication boundary

This is an attributed Commons source continuation, not an upstream submission
or acceptance claim. The original utility and logger remain the work of their
upstream contributors. The full modules are not republished here; the packet
contains only `change.patch` and this source note.

The donor tree's differently attributed MIT notices were already preserved
verbatim in the Commons packet
`work/bounty-intake/stellaranalysis-issue-generator-layout-20261006-7ca6/`:

- `upstream-licence-mclaughlin.md`:
  `57740b9d4d86aedf5d518f2f363d5cf192c54127`.
- `upstream-license-menke-laguna.md`:
  `af5411fa243cfcf2b61c79d081dbb6204e956041`.
- `upstream-license-de-wet.md`:
  `4a766e268772888af5df56c3f6c608f68558b789`.

Those retained notices are referenced without assigning any one notice a
repository-wide scope or rereading unrelated source. No upstream issue,
claim, PR, payment, account, or production action is performed by this packet.
