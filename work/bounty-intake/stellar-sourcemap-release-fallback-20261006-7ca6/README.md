# Align the sourcemap uploader's browser release fallback

This attributed source patch aligns two existing release-selection expressions in Stellar Analysis. When `NEXT_PUBLIC_APP_VERSION` is unset or empty, the browser SDK configuration selects `unknown`, while the manual uploader currently selects a Git commit abbreviation. The patch makes the uploader use the browser configuration's existing fallback. Explicit, nonempty versions continue to pass through unchanged.

It is a source consistency correction, not evidence of a deployed Sentry integration or a successful upload. No credentials, environment values, build artifacts, Sentry account state or external event data were acquired.

## Source and caller custody

Repository: [Stellar-Analysis/frontend](https://github.com/Stellar-Analysis/frontend). All listed sources were fully acquired at immutable commit `482ee456369418ef82c4056718cb82d3468f762b`, retained, and identified by both the returned Git blob SHA and an independent computation over their full UTF-8 text.

| Path | Git blob | UTF-8 bytes |
| --- | --- | ---: |
| `scripts/upload-sourcemaps.sh` | `c6b678a1dc35c4ca4d862051d4bd76abb0792065` | 1,001 |
| `sentry.client.config.js` | `af4412c6af16c6b6a119c693c9d16b84fe56ca25` | 3,774 |
| `sentry.server.config.js` | `2b9e90069acdef337ed523a3f68aa25512112a33` | 731 |
| `docs/SENTRY_INTEGRATION.md` | `f96cdef5244a34273a5a146db85d63c19aca1ab5` | 5,883 |

The guide documents the manual uploader and tells operators to match the release version to `NEXT_PUBLIC_APP_VERSION`. The uploader sends `.next/static`; the browser configuration names that same environment variable for release tracking. The server configuration separately selects `APP_VERSION || "unknown"` and is not modified.

Previously qualified complete `package.json` (`2b1c6ac1f83096666c7fd6d5ba3fd22780e6b8eb`) has no upload script hook, and `next.config.ts` (`ba087f7a3a205121f825f1d3944df139ecf7ca69`) has no Sentry wrapper. This work relies on the guide's manual caller, and does not adopt its claim that every build automatically uploads maps. It does not establish whether every SDK initialization path is wired into the current Next.js app.

A bounded repository-specific PR search for the literal `sourcemap` returned zero rows with `incomplete_results:false`. That is narrow chronology evidence, not a repository-wide ownership or contribution census. No unavailable source, prior failed route or private carrier was recovered.

## Exact change

The browser expression is `process.env.NEXT_PUBLIC_APP_VERSION || "unknown"`. The uploader's previous shell expression used `git rev-parse --short HEAD` whenever the variable was unset or empty. Those two fallbacks produce different release identifiers from the same missing/empty setting.

The replacement is `RELEASE="${NEXT_PUBLIC_APP_VERSION:-unknown}"`, with a comment pointing to the browser configuration. Bash's existing unset-or-empty default condition is preserved; only the fallback value changes. A nonempty string is not trimmed, shortened or otherwise transformed.

This also removes the fallback's incidental dependency on the invocation directory's Git checkout. No Git command or environment lookup was executed to prepare the patch. It does not add an authentication check, permission requirement, SDK event, release-creation call or upload operation.

The existing checks for the three named Sentry configuration variables, release-create `|| true`, upload command, URL prefix, finalization and success message remain unchanged. The broad release-create error suppression was observed but is not changed without its own qualified error/idempotency contract.

## Scope and acceptance boundary

The repair aligns the configured browser and manual-uploader fallback identifiers. It does not require a new version value, change the browser's fallback policy, or invent a Git-derived version for the client. Deployments should still use explicit meaningful versions as described by the existing guide.

Build-time and upload-time environment values can differ; this patch cannot reconcile those separate inputs. Nor does it guarantee generated map availability, correct URL-prefix matching, SDK initialization, authentication, release uniqueness, deployed HTTP paths or readable production stack traces. The guide's old `./frontend/scripts/...` path and automatic-upload wording remain separate documentation concerns. No server-release policy is inferred from the browser upload script.

The complete retained tree pins the upstream script as executable mode `100755`; the patch preserves it. Source identity:

- Before: `c6b678a1dc35c4ca4d862051d4bd76abb0792065`, 1,001 UTF-8 bytes.
- After: `56e6c81207c1357ebf08e3b9374a53d053fc299a`, 1,040 UTF-8 bytes.
- One upstream path, two added lines and one removed line.

The patch and source identities were checked as text. No shell, Git CLI, Sentry CLI/API, credential/environment inspection, source-map upload, release creation/finalization, build, SDK execution, tests, fixtures, workflow or upstream submission was performed. Runtime and upstream acceptance remain unperformed.

## Attribution and packaging

Original project and source credit remains with Stellar Analysis and its contributors. This Commons packet contains only the minimal attributed patch and this original note, not a full upstream module.

The retained complete donor tree did not establish a repository-wide license or root contribution/agent instructions. Separately attributed MIT notices were already preserved under `work/bounty-intake/stellaranalysis-issue-generator-layout-20261006-7ca6/`: McLaughlin `57740b9d4d86aedf5d518f2f363d5cf192c54127`, Menke/Laguna `af5411fa243cfcf2b61c79d081dbb6204e956041`, and de Wet `4a766e268772888af5df56c3f6c608f68558b789`. Those different notices are not assigned repository-wide scope here.
