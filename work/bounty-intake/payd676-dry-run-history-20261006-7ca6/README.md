# Forward migration dry runs use existing history

The current rollback carrier's forward `--dry-run` path opens its database connection but then unconditionally substitutes an empty applied-migration map. That makes every local file appear pending and prevents the existing checksum comparison from detecting recorded drift. This patch reads the tracking history when that table already exists, using the runner's existing helpers.

## Pinned source and credit

- Canonical repository: [Protocol-Guild/PayD](https://github.com/Protocol-Guild/PayD).
- Related request: [issue 507, Add database migration rollback strategy](https://github.com/Protocol-Guild/PayD/issues/507).
- Existing carrier: [PR 676, feat(db): add transactional migration rollbacks](https://github.com/Protocol-Guild/PayD/pull/676), authored by `woahwhattheheck`.
- Donor repository/branch: `woahwhattheheck/PayD:sol56/payd507-migration-rollback-20261004-v2`.
- Current immutable head: `a681e266132f82b6549b6f9a4d8dae90b5988c76`; observed base `171c74b454daba241bfb75f36d10a0a3a77a68e5`.
- Production path: `backend/src/db/migrate.ts`.
- Complete source preimage: `dc926fa673158691fb1aae121c27416164694d22`, 15,180 UTF-8 bytes.
- Prepared postimage: `e673b38c503ce68c3384903a8dec6daab4fa1ae0`, 15,371 UTF-8 bytes.

The existing migration/rollback implementation remains credited to its carrier authors. The PR body refers to an older retained source handoff and historical rollback validation; this packet is based on the actual current head above and does not rerun or adopt that validation as new evidence.

Issue 507 is open and unassigned in the observed metadata. Its one returned public comment is an implementation-interest request from `shobhamerabacha-star`, not an assignment or acceptance. The issue's full rollback and data-integrity acceptance criteria remain separate from this narrower source correction.

## Branch behavior

Immediately inside the existing protected `try`, the patch sets:

```ts
const hasTrackingTable = !isDryRun || (await trackingTableExists(client));
```

For a real forward run, short-circuit evaluation avoids an extra presence query. The existing bootstrap SQL still executes before the same history fetch.

For a dry run with an existing table, `fetchAppliedMigrations` reads the same `filename` and `checksum` records as the real run. The existing loop then skips matching applied files, records checksum drift, and reports only unrecorded files as candidates. The existing eventual drift error remains unchanged. The "Would bootstrap" message is emitted only when the dry-run presence check reports an absent tracking table.

For a dry run without the table, the applied map remains empty and the runner reports the existing would-bootstrap message. Neither bootstrap SQL nor migration SQL nor tracking-row writes is added to this branch. An unavailable or unreadable database still fails rather than being silently treated as empty history.

The existing `trackingTableExists` helper uses `to_regclass('schema_migrations')`; the existing history helper selects `filename, checksum` ordered by ID. No new query builder or dependency is introduced.

## Preservation and limits

All rollback function bytes, rollback catalog validation, SQL files, checksum algorithm, per-file execution transactions, recording/removal of migration rows, argument parsing and connection configuration remain unchanged. The real forward path's bootstrap and fetch order are preserved. The source includes a prominent dated modification notice for this change.

This is planning against observed history, not a consistent database snapshot or a concurrency control change. A table may change between the presence check and read; ordinary database errors propagate. The dry-run branch still needs the runner's existing database connection and environment configuration. Connection-acquisition cleanup, schema selection, transaction isolation, rollback reversibility, global drift policy and deployment readiness are not newly guaranteed.

The patch has six added and four removed production lines in three hunks, including the modification notice. Complete forward patch application and reverse reconstruction match the pinned source bytes. No migration, rollback, database connection, SQL statement, fixture, test, build, CLI command or account/payment action was executed for this packet.

## Source custody

| Read source | Git blob | UTF-8 bytes |
| --- | --- | ---: |
| `backend/src/db/migrate.ts` | `dc926fa673158691fb1aae121c27416164694d22` | 15180 |
| `backend/package.json` | `bd9001b64a3f5fd5732ce60c33e90aff3dca13c7` | 2964 |
| `CONTRIBUTING.md` | `1e015aa7e145db0cd0e306f7032cce130b8acbb8` | 142 |
| `LICENSE` | `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | 11357 |
| `README.md` | `374ffef680426f41b9f3e832059106839cfc72bd` | 7579 |

The nontruncated 794-entry tree shows no AGENTS/RULES or NOTICE file. Root CONTRIBUTING is the scaffold's short contribution placeholder. The actual root license is Apache 2.0 and is copied exactly beside the patch. Other metadata is inconsistent: the README badge says MIT and the backend package declares ISC; this packet does not rewrite or resolve those labels. It publishes a focused patch and guide, not the complete donor module.

The declared caller `db:migrate:dry-run` invokes `ts-node src/db/migrate.ts --dry-run`; the retained package declares `pg ^8.18.0`. No installed-version, module-loader or database compatibility result is inferred from those declarations.

## Use and external boundary

`dry-run-history.patch` is relative to the donor repository root and requires the exact preimage above. Later carrier changes require explicit reconciliation rather than assuming the patch still applies. The prepared full source, patch and artifact identities were retained before publication; the Commons publisher performs fresh target-path guards.

The original issue still requires rollback validation and preservation of data integrity. Those broader conditions, maintainer review and any assignment or reward remain external. No upstream PR update, issue claim, sponsor contact, deployment, credentials, employee data, wallet or chain action occurred. The public packet contains no live connection string or private database content.
