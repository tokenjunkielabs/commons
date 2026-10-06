# PayD local-setup clone command

The root README starts installation with a fenced shell command containing a placeholder repository and Markdown link syntax. This minimal documentation correction supplies the observed canonical repository URL and an explicit destination matching the following unchanged `cd payD` line.

Corrected command:
```bash
git clone https://github.com/Protocol-Guild/PayD.git payD
```

No clone, shell command, install, Docker operation or service startup was performed.

## Source and exact change

Canonical source: [Protocol-Guild/PayD](https://github.com/Protocol-Guild/PayD), donor main `171c74b454daba241bfb75f36d10a0a3a77a68e5`, root `README.md`, mode100644.

| Identity | Git blob | UTF-8 bytes |
|---|---|---:|
| Complete donor README | `374ffef680426f41b9f3e832059106839cfc72bd` | 7,579 |
| Prepared README | `4b4af5d52cb5010a6e38390981e30314c7751b81` | 7,550 |

Only the single clone line changes: +1/-1, one hunk containing eight complete rows. The destination argument is deliberately `payD`, matching the exact existing directory-change command instead of relying on the repository URL's case. The rest of the README is byte-identical, including its surrounding formatting, installation text and configuration placeholders.

The [official Git clone manual](https://git-scm.com/docs/git-clone) documents the repository argument followed by an optional destination directory. That ordinary positional form is all this correction uses. No flags, branches, authentication method or shallow-clone policy are added.

## Relation to the current issue

The public [issue177](https://github.com/Protocol-Guild/PayD/issues/177) asks for a complete local Docker Compose setup guide. Its current metadata is open with no assignee and three returned comments, all requests to work on that documentation. The bounded repository-specific numeric PR query returned only PR91, titled Contract Event Indexer; no body or source from that unrelated carrier was needed. A separate bounded Commons PR query for PayD and clone returned no matches. These observations are not an exhaustive ownership/history census.

This packet fixes one concrete prerequisite command found while qualifying issue177. It does not supply or claim the requested full-stack Compose setup. The bounded root directory contains no root Docker Compose file; the inspected infrastructure and docs directory headers do not establish whether a usable configuration exists deeper elsewhere. No missing configuration was reconstructed.

The surrounding README still has formatting and startup/configuration guidance that were not qualified as a runnable end-to-end procedure. In particular, this one-line repair does not make the whole installation block safe to copy as a single shell program. No frontend/backend/Postgres/Redis compatibility, environment readiness, migrations, image availability or service-health claim is made.

## Attribution and license

Original Protocol-Guild/PayD README contributors retain authorship. The source modification is dated 2026-10-06 and is identified completely by the two hashes above and `clone-command.patch`. Only the minimal patch, this attribution/contract guide and exact license text are published; the complete donor README is not republished.

`LICENSE` preserves the actual root license bytes, Git blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` (11,357 bytes), which contain Apache License 2.0. The original README's MIT badge was separately observed and is left untouched; it is not used as license authority here. No broader license-scope conclusion is inferred.

## Materialization and publication boundary

The full donor README was independently hashed. The serialized unified patch was applied in memory to that complete string and reversed from the prepared result; both identities matched exactly. This is artifact materialization only, not a Git/shell test or runtime reproduction. The old command was not executed and no fabricated command output is included.

No source branch, issue assignment or upstream pull request is changed. No credential, account, API key, wallet, payroll, container, package manager, workflow, test, runtime, upstream submission, acceptance or reward action occurred. The full issue177 remains unresolved.
