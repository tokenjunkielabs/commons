# Preserve display identity and read-only wallpaper lookup

This is a narrow source continuation of [jamilahmadzai/macos-wallpaper PR #1](https://github.com/jamilahmadzai/macos-wallpaper/pull/1), which implements per-display directory wallpaper resolution for [sindresorhus/macos-wallpaper #25](https://github.com/sindresorhus/macos-wallpaper/issues/25). It fixes two surrounding lookup defects in the existing contribution. The per-display SQL, path resolution and fallback feature remains the original contributor's work.

## Source and attribution

| Item | Exact source |
| --- | --- |
| Existing contributor | jamilahmadzai |
| Existing PR head | `0a6f94926734feba2085cf07d8d2d5d07067dcf3` |
| Existing PR base | `c003b5271d47a4727120df669a7dce0d95c417c7` |
| Production path | `Sources/wallpaper/Wallpaper.swift` |
| Complete original source | `b1ee4ed9dbf560425dededbf00d694ddabf7ea18`, 7,402 UTF-8 bytes |
| Complete resulting source | `eabfa6a18fb253eaa7a4af3c90682a7c6e910b70`, 7,499 UTF-8 bytes |
| Source tree mode | `100644` |
| Original license | MIT, Sindre Sorhus; unchanged license blob `fa7ceba3eb4a9657a9db7f3ffca4e4e97a9019de` |

The source was read in full at the immutable contributor head. The associated utilities, package manifest, resolved dependencies and README were also read. The full root listing and complete Sources tree contained no local AGENTS or contribution-instruction file. Existing tab indentation and LF endings are preserved.

The earlier [LYY435939/macos-wallpaper PR #1](https://github.com/LYY435939/macos-wallpaper/pull/1), head `4a7a3067b99e344a33772deb81f3431cf14a7390`, is a separate existing per-display attempt. Its complete production diff was reviewed for scope; this packet's preimage is the later jamilahmadzai contribution. It does not claim authorship of either feature.

## The two source defects

### Reading the desktop database could create it

The directory lookup used `Connection(dbURL.path)` solely to run SELECT queries. The exact pinned SQLite.swift 0.15.4 dependency, revision `392dd6058624d9f6c5b4c769d165ddd8c7293394`, defaults that initializer's `readonly` argument to false. Its [Connection.swift source](https://github.com/stephencelis/SQLite.swift/blob/392dd6058624d9f6c5b4c769d165ddd8c7293394/Sources/SQLite/Core/Connection.swift), blob `188ff80b2abd9a59c28505a8e4a306d27723a609`, selects READWRITE and CREATE in that case.

The one-line change supplies `readonly: true`. SQLite's [database-open contract](https://www.sqlite.org/c3ref/open.html) specifies that READONLY opens an existing database and returns an error if it is missing. The existing caller already catches lookup errors and returns the original directory URL. That fallback now also handles a missing database without asking SQLite to create the main database file.

This is a connection-mode correction. No claim is made that all platform sidecar, journal or filesystem behavior has been observed.

### Missing image URLs broke screen association during refresh

The public `get` method deliberately uses `compactMap`, omitting screens for which AppKit returns no wallpaper URL. The refresh helper previously obtained that shortened URL array, enumerated every selected screen again, and indexed the shortened array by the screen index. A missing URL can shift the remaining associations and leave a later index outside the array.

The refresh helper now snapshots each selected NSScreen together with that same screen's optional wallpaper URL. It performs all lookups before the first wallpaper change. Its mutation loop consumes those saved pairs, without enumerating the screen selection again or indexing a compacted array. A nil URL skips the comparison-dependent refresh for that screen; the later requested wallpaper assignment keeps its existing behavior.

The public `get` return type and omission behavior remain unchanged. Lookup errors still precede refresh writes. Empty selections produce an empty snapshot. This preserves identity for the captured screens; it does not promise that a display cannot disconnect after capture.

## Change and integration

The patch contains exactly two production hunks, **+6 / -4**. Every other source byte is unchanged, including the per-display SQL, global and legacy fallbacks, path handling, macOS 26 guard, scale options, existing refresh workaround and sleep duration.

- `source/Sources/wallpaper/Wallpaper.swift` is the complete resulting production file.
- `display-lookup.patch` is the exact unified patch against the immutable source above.
- `LICENSE` preserves the original MIT notice.

Apply the patch to the existing PR head or use the full resulting file with that contribution's other files. In particular, the contributor's displayUUID utility remains a required part of its implementation. This packet does not copy its tests, alter its package manifest, or replace its broader feature with an independent implementation.

## Validation and limits

Complete source and license contents were bound to their Git blob identities. The production source's regular-file mode was checked in the complete retained Sources tree. The actual serialized two-hunk patch was independently reconstructed against the full original text, including every context/deletion line and hunk count; the result exactly matched the full resulting source.

Validation is static source, dependency-contract and artifact-integrity work. No Swift compiler, macOS process, AppKit call, SQLite operation, device, fixture, test, build or workflow was run. The existing contributor's reported execution is attributed to that contributor and is not presented as this packet's validation.

The issue and both contributor PRs were open in the retained October 5, 2026 reads. All eight issue comments and the selected contributor PR's empty normalized comment timeline were retained. Existing reports describe upstream pull-request creation restrictions; this work makes no upstream write, platform submission, acceptance, whole-issue completion or historical $60 award claim.

The adjacent wallpaper #52 intake named PR #103, whose exact native fetch returned 404. That route is held without retry or replacement. This packet does not claim to inspect that missing contribution or eliminate the default-wallpaper flash.
