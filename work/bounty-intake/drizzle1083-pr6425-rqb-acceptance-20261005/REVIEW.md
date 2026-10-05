# Drizzle #1083 / PR #6425 acceptance review

Status: **BLOCKED — nested relational selections bypass the new mapper**

This is an independent review packet. It does not claim or modify the upstream implementation, Algora submission, or payout rights. Those remain with PR author **aipd506**.

## Frozen review inputs

- Issue [drizzle-team/drizzle-orm#1083](https://github.com/drizzle-team/drizzle-orm/issues/1083) is open and unassigned.
- Algora advertises a **$30** bounty and says payment follows a reward: [issue comment 1806855209](https://github.com/drizzle-team/drizzle-orm/issues/1083#issuecomment-1806855209).
- Reviewed carrier: [PR #6425](https://github.com/drizzle-team/drizzle-orm/pull/6425), open and mergeable at head `8522a4aa21252029272f7cb095a0e0bed83a1e72`, author `aipd506`.
- Reviewed base: `15454dbe49d827c6081f3d0231e2e7985e517295`.
- Reviewed SQLite dialect blob: `5a50d4aa724150b3adbf209c9d546d09191ee999`.
- Reviewed test blob: `11f3000578262d919c9f2f5206c929df05229b6b`.
- Competing carriers exist, including [#5746](https://github.com/drizzle-team/drizzle-orm/pull/5746), [#5437](https://github.com/drizzle-team/drizzle-orm/pull/5437), [#6292](https://github.com/drizzle-team/drizzle-orm/pull/6292), and [#6394](https://github.com/drizzle-team/drizzle-orm/pull/6394). This packet reviews #6425 only.

## Acceptance blocker

PR #6425 says it covers relational query builder flows, but its eight new tests exercise ordinary selects, a join, PostgreSQL `returning()`, SQL generation for five dialects, and a direct call to `mapFromDriverValue`. The test file contains none of `db.query`, `findMany`, `relations(`, or `buildRelationalQuery`.

More importantly, the current PR head leaves SQLite's nested relational serialization path unchanged. In `drizzle-orm/src/sqlite-core/dialect.ts`, lines 846–858 in blob `5a50d4aa...`, the `nestedQueryRelation` branch builds `json_array(...)` by mapping each `SQLiteColumn` directly to `sql.identifier(this.casing.getColumnCasing(field))`.

The new `mapColumnSelection(field, columnSql)` helper is not called there. PR #6425 wires `selectFromDb` only into `buildSelection()`. That helper is used when the final SELECT list is rendered, but nested relation values have already been embedded into `json_array(...)`. The outer selection sees a JSON SQL expression, not the original custom column, so it cannot apply the custom mapper later.

### Concrete failing shape

A query shaped like `db.query.parents.findMany({ with: { children: true } })` is the relational use case required by #1083. If `children.payload` is a SQLite custom type whose `selectFromDb` returns `json_extract(column, '$.value')`, the nested JSON builder emits the child column identifier directly inside `json_array(...)`, not the configured wrapper. The opt-in transform is skipped for nested relational results.

That contradicts both issue #1083's relational-query requirement and PR #6425's stated solution.

## Required repair and proof

Before acceptance:

1. Add a focused SQLite relational-query SQL-generation regression with a parent/child relation and a nested custom column.
2. Assert the nested JSON SQL contains the configured wrapper exactly once and uses the relation alias.
3. Route nested `SQLiteColumn` values through the same mapper used by ordinary selections before adding them to `json_array(...)`.
4. Audit PostgreSQL and MySQL relational JSON construction for the same direct-column serialization pattern and add equivalent coverage where applicable.
5. Preserve behavior for custom types without `selectFromDb`, ordinary decoding, casing, aliases, one/many relations, and nullable relations.
6. Run the focused SQL-generation/type checks plus the relevant dialect suite.

A minimal SQLite repair should apply the mapper to correctly qualified nested column SQL where each JSON item is constructed. Avoid double-wrapping root selections or changing expressions already represented as `SQL.Aliased`.

## Money and ownership state

- Advertised: **$30** for issue #1083.
- Promised/payable route: Algora says the bounty was created and payment occurs after reward.
- Independently verified escrow/funded balance: **not evidenced by the available issue/PR record**.
- Awarded: **$0 evidenced**.
- Invoiced: **$0 evidenced**.
- Received: **$0 evidenced**.
- Implementation/submission/payment owner: **aipd506**, unchanged.
- This packet owner: acceptance review only.

## Decision

**Do not treat PR #6425 as satisfying issue #1083's relational-query acceptance requirement yet.** The SQLite nested relational path is a source-proven gap, and the claimed relational coverage has no corresponding test.
