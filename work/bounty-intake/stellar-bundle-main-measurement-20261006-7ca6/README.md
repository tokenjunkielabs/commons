# Stellar Analysis bundle measurement correction

This is an attributed source patch for the existing `scripts/analyze-bundle.mjs` caller in [Stellar-Analysis/frontend](https://github.com/Stellar-Analysis/frontend), prepared on 2026-10-06. It makes the script measure its documented gzip budget, prevents an absent main match from being reported as a passing zero-byte measurement, and prevents directory enumeration order from selecting only the last main match.

The packet contains a patch and this note. It does not publish a complete upstream module, run a build or compressor, or submit an upstream contribution. Original project and source credit remains with Stellar Analysis and its contributors.

## Bound source and actual callers

The source reference is commit `482ee456369418ef82c4056718cb82d3468f762b`. A fresh named-main read during qualification returned that same commit. These are full-file acquisitions with native and independently computed Git blob identities:

| Path | Git blob | UTF-8 bytes |
| --- | --- | ---: |
| `scripts/analyze-bundle.mjs` | `9eec92f8a224053babb329a6e7fdf46035e9b055` | 2,026 |
| `package.json` | `2b1c6ac1f83096666c7fd6d5ba3fd22780e6b8eb` | 3,119 |
| `README.md` | `a7546f7a6f85709fccd21e136cd8b12bae820652` | 2,694 |
| `next.config.ts` | `ba087f7a3a205121f825f1d3944df139ecf7ca69` | 5,062 |
| `docs/PERFORMANCE.md` | `222eb092fc700a2308078a2a06d8d8102d7edd45` | 2,209 |
| `docs/performance-optimization.md` | `cd5849e75b4373fd8f5dc4e029d8c3183a1edc28` | 14,016 |

The retained recursive tree pins the script as mode `100755`. The patch preserves that mode. The actual package command is `ANALYZE=true next build && node scripts/analyze-bundle.mjs`; the root README lists `pnpm analyze` as the bundle inspection command. Both performance documents describe a main-bundle gzip budget of at most 200 KB. The Next config separately sets raw webpack asset and entrypoint limits to 500 × 1024 bytes; those limits are not changed here.

The bounded path-history request returned one row: [christabel888's flattening commit](https://github.com/Stellar-Analysis/frontend/commit/59fad72d9fbef9cfd6f47e215392da44488fcdc4), which moved the nested frontend to the repository root. This attributes the observed relocation, not original authorship of every script line. A repository-specific PR search for the literal `analyze-bundle` returned zero rows with `incomplete_results:false`; that narrow search is not a complete ownership or contribution census.

## Source correction

The existing script chooses top-level names ending in `.js` from `.next/static/chunks`. Within that set, it calls a filename containing `main` a main bundle. This filename heuristic is preserved.

Previously, each main match replaced `mainBundleSize` with its raw filesystem size. A later smaller match could replace an earlier larger value. If no filename matched, the initial zero remained and satisfied the main-bundle condition. The comparison also used raw bytes and strict less-than despite the gzip/inclusive wording in the documentation.

The patch:

1. Reads each existing main-match file and obtains its gzip byte length with Node's built-in `gzipSync`, using its default compression options.
2. Counts those matches and retains the largest gzip length. The resulting decision does not depend on their enumeration order.
3. Requires at least one match before the existing main-bundle check can pass. With no match, the displayed measurement explicitly says it was not observed, and the existing final failure branch exits nonzero.
4. Uses `<= 200 * 1024`, retaining the script's existing 1024-based interpretation of the displayed KB unit.
5. Labels the measurement as gzipped and as the largest of the observed matching files.

The [official Node.js zlib API](https://nodejs.org/api/zlib.html#zlibgzipsyncbuffer-options) documents `gzipSync` as the synchronous gzip operation on a buffer. No new package dependency is introduced. No gzip operation was executed during this work.

The raw total, raw top-ten chunk sizes, existing 100 KB chunk warnings, code-splitting count, directory selection, build-directory error, and final nonzero failure path retain their existing behavior. Read/compression exceptions are not converted into a pass or a zero measurement. The script's existing filesystem-error behavior remains throwing.

## Scope and limitations

This is a correction to the script's existing per-file main-name heuristic. The maximum of the matching files is not their sum, an initial-route bundle total, a complete App Router asset graph, or an actual HTTP transfer measurement. Gzip uses local Node defaults; a deployed server may use different compression settings or another content encoding. No compression ratio, timing improvement, production size, deployment, or runtime success is claimed.

No generated `.next` directory was acquired, fabricated, or replayed. Compatibility of the existing `main` naming heuristic with every Next.js or bundler configuration remains unverified. A build layout with no matching filename now produces an explicit failed measurement instead of a passing zero. Recursive chunk discovery, bundler selection, old `cd frontend` documentation, CI routing/enforcement, and the warning-only 100 KB chunk policy are separate concerns and remain unchanged.

The independently qualified migration wrappers stop at their missing `../backend` directory under `set -e` before a migration command. They receive no patch here. The earlier generator, close/recreate wrapper, gas parser and folder-size publications are separate completed work.

## Patch identity and validation boundary

Apply `change.patch` to the exact pinned preimage:

- Before: `9eec92f8a224053babb329a6e7fdf46035e9b055`, 2,026 UTF-8 bytes, mode `100755`.
- After: `d9edfa93b12b60f37fa0f261d1c1a73fc9829164`, 2,439 UTF-8 bytes, mode `100755`.
- Scope: one upstream path, 11 added and 4 removed lines.

The complete preimage and authored postimage were retained privately. The patch's source reconstruction and both identities were checked as text. No Node/Next process, shell, migration, database, compressor, fixture, test, benchmark, workflow or upstream write was invoked. Runtime and upstream acceptance remain unperformed. The described absent/multiple-file consequences follow from source control flow; they are not reported execution results.

Root's retained complete donor tree has no root contribution/agent instructions or repository-wide license declaration. Separately attributed MIT notices from that tree were preserved in the earlier generator packet under `work/bounty-intake/stellaranalysis-issue-generator-layout-20261006-7ca6/`: `upstream-licence-mclaughlin.md` (`57740b9d4d86aedf5d518f2f363d5cf192c54127`), `upstream-license-menke-laguna.md` (`af5411fa243cfcf2b61c79d081dbb6204e956041`), and `upstream-license-de-wet.md` (`4a766e268772888af5df56c3f6c608f68558b789`). Those different notices are not assigned a repository-wide scope here. This packet supplies only the narrow attributed patch and this original note.
