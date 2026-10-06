# Qualified extension identity in sync comparisons

The existing installed-extension merger identifies an extension by its lowercased `publisher.name`, while the missing/deleted comparisons in the same carrier still compare only `name`. Two publishers can therefore supply different extensions with the same name and be treated as the same installed item. This patch makes both comparisons use the carrier's existing `InstalledExtensionsService.GetExtensionFullName` helper.

For example, from the source predicates, local `publisherA.example` previously suppressed installation of remote `publisherB.example`; conversely, the presence of remote `publisherB.example` could incorrectly retain local `publisherA.example` during deletion selection. These are explanatory source cases, not executed test inputs.

## Source and attribution

- Canonical project: [shanalikhan/code-settings-sync](https://github.com/shanalikhan/code-settings-sync).
- Original request: [issue 143, Considering disabled extensions](https://github.com/shanalikhan/code-settings-sync/issues/143).
- Current source carrier: [pull request 1476, Feature: Support syncing disabled extensions](https://github.com/shanalikhan/code-settings-sync/pull/1476), by **s6pa1rta3n-lab**.
- Source repository and branch: `s6pa1rta3n-lab/code-settings-sync:feature/sync-disabled-extensions`.
- Immutable head: `67c68fa28cc24c590a1668abe9ba613349c29fc8`; observed base: `eb332ba5e8180680e613e94be89119119c5638d1`.
- Production path: `src/service/plugin.service.ts`.
- Prior public review locator supplied by the technical handoff: [PR 1476 comment 6005837375](https://github.com/shanalikhan/code-settings-sync/pull/1476#issuecomment-6005837375). The retained handoff identifies this same residual; this packet does not claim a new discovery or independently reread that review's complete discussion.
- Original project copyright and MIT license remain in the accompanying exact `LICENSE`.

The observed carrier is open and unmerged, with one reported discussion comment and seven changed files. Issue 143 is open and unassigned in the observed metadata. Its historical funding banner and submitted-PR links are not evidence of current eligibility, an award, or maintainer acceptance. The complete 55-comment issue history was not acquired.

## Change

`GetMissingExtensions` computes the installed qualified IDs once, then tests each remote extension with the same helper. `GetDeletedExtensions` computes the remote qualified IDs once and tests each local extension identically. The helper already normalizes to lowercase, so comparison now agrees with the disk/API merger's identity rule. Version and disabled flags remain outside extension identity.

The patch preserves the existing bare-name `ignoredExtensions` policy, the `code-settings-sync` self-exclusion, JSON parsing, extension discovery, disabled flags, notifications, and installation/uninstallation command bodies. In particular, it does not reinterpret an existing ignore entry as a publisher-qualified rule. It also does not implement disabled-state restoration or establish completion of the broader issue.

There are 12 added and 2 removed production lines in three hunks. Original CRLF line endings remain in the complete prepared postimage; unchanged source bytes are preserved.

## Exact source identities

| Path at the immutable carrier head | Git blob | UTF-8 bytes |
| --- | --- | ---: |
| `src/service/plugin.service.ts` | `203f306abc8a399d37151ebcd223ab08388e8cee` | 5743 |
| `src/service/installedExtensions.service.ts` | `e8cb5d6392594ed44e296673f35a3c01263987a2` | 5924 |
| `src/models/extensionInformation.model.ts` | `7dcfb7eab1643486586e390c6ac32c3838b67d48` | 2295 |
| `CONTRIBUTING.md` | `5f04c34639985acbc3ba87798ff436182ca1baeb` | 3995 |
| `LICENSE` | `3c0206dfac7a006db1957bba0c8dd8cad42d4e17` | 1077 |
| `package.json` | `6c870bc50002be4640284871da92cabff9f4d07e` | 5793 |

Prepared `src/service/plugin.service.ts` postimage: `f3f59cccb4d5a75ca96341da54ec1965d643686d`, 6087 UTF-8 bytes.

The full production module, its helper and model were read from the pinned head. The complete source tree response was not truncated; it contained the root contribution and license files and no additional AGENTS/RULES file. The helper's actual body supplies the normalization contract; no new dependency is introduced.

## Applying the patch

`qualified-extension-identity.patch` is relative to the donor repository root and targets the exact source preimage above. Apply it only to that preimage, or reconcile later changes explicitly. The original donor PR, branch, and author attribution remain separate from this Commons continuation.

The full prepared text and patch were retained before publication. The three hunks were checked by source-text forward application and reverse reconstruction against the complete original, and independent Git blob identities were compared with the provider identities. These are text and identity checks, not compilation or extension execution.

## Validation and limits

No VS Code session, filesystem extension scan, installation/uninstallation command, account/Gist synchronization, dependency installation, build, lint, test, or browser action was performed. The package declares the historical VS Code and TypeScript constraints; no compatibility with a currently installed runtime is asserted. Ordinary existing metadata objects are assumed. Missing or malformed publisher/name fields, JSON-schema validation, duplicate input records, and concurrent changes during synchronization are not newly addressed.

The retained `CONTRIBUTING.md` requests upstream version-branch targeting and tests, and links further contribution guidance. Those upstream submission requirements are not represented as satisfied by a source-only Commons artifact. No upstream PR update, review, registration, claim, sponsor contact, or payment action occurred. The packet contains a patch, this guide, and the unchanged MIT license; it does not change the upstream repository or imply whole-PR readiness.
