# Preserve the FX rate's calendar date

This packet supplies a two-line source continuation for the existing [PayD #696 proposal](https://github.com/Protocol-Guild/PayD/pull/696), by `woahwhattheheck`, associated with [issue #533](https://github.com/Protocol-Guild/PayD/issues/533). The issue requests five-minute FX-rate caching and cache invalidation behavior. This continuation corrects the date projected into the FX response and cache; it does not change the monetary rate or volatility calculation.

## Source and original work

The public PR was observed open and unmerged at `0e0b0da481e9410b8cd7863fe7256ad2e547c2f8`, with zero conversation and inline-review comments. The issue's single comment is an external assignment request, not maintainer acceptance or award authority. Original PR/cache authorship remains credited. The existing employee-cache generation change and separate tenant/controller invalidation work are preserved.

Complete source was acquired at that immutable head:

| Path | Git blob |
| --- | --- |
| backend/src/services/forecasting/fxRateService.ts | cd7ba9e1b7021e6456cecd372b15d4b13eaa85f6 |
| backend/src/services/forecasting/forecastingService.ts | 0daef6e057cbe5c724bfb2d40186c6b4cb72a895 |
| backend/src/db/migrations/019_create_fx_rates.sql | dc02e991be986f4c5d5205cd2fde03366ac0261c |
| backend/src/config/database.ts | bd58cc3d8087fb6148d9d82f29411842713e4a09 |
| backend/src/services/rateLimitService.ts | 23ce8d8be96d221a8db8124bc5af4e2ccda8c114 |
| backend/package.json | 746a535b08bf0c6ce9c4a96f7d75c76e0bbacb95 |

The FX preimage is 2962 bytes; the prepared full postimage is 2982 bytes with blob `0c28ec73975970ce9171907455c49088a9d6d7f7`. The full postimage is retained for exact text reconciliation, not republished as a full module.

## Concrete date boundary

The schema declares `rate_date DATE NOT NULL`. The shown pool configuration supplies only a connection string to node-postgres, and the package declares `pg ^8.18.0`. The actual forecast caller requests a rolling ninety-day range with ISO calendar-date strings and returns the points from this service.

The [official node-postgres data-type documentation](https://node-postgres.com/features/types) states that DATE values are parsed into JavaScript Date objects using the Node process's local time. The existing mapper then applies `toISOString().slice(0, 10)`, which selects the UTC calendar day. For a positive-offset local midnight, that UTC day can be the preceding day. This is an inference from the source and documented conversion, not an observed deployed failure or a timezone experiment.

The patch formats the database value before the driver can reinterpret it:

- The SELECT projects `to_char(rate_date::timestamp, 'YYYY-MM-DD') AS rate_date_text`.
- The mapper returns `r.rate_date_text` directly.

The [PostgreSQL formatting documentation](https://www.postgresql.org/docs/current/functions-formatting.html) defines timestamp-to-text formatting and the YYYY, MM and DD fields. The explicit timestamp-without-time-zone cast preserves the stored calendar fields. The distinct alias is intentional: the unchanged `ORDER BY rate_date ASC` still refers to the underlying DATE column rather than sorting the formatted text. Currency normalization, bound parameters, date predicates, numeric-rate conversion, response shape, volatility calculation and every other source byte remain unchanged.

The cache key and five-minute TTL remain unchanged. Previously cached results can therefore retain their old date strings until their existing expiry; this packet does not flush Redis or promise an immediate migration of already stored cache entries. It does not add date admission policy or claim general handling for non-finite/BC dates, custom global parsers, or unrelated date fields.

## Verification and publication boundary

The complete serialized patch has two hunks, +2/-2. Pure text checks establish exact forward application to the full pinned preimage, exact reverse application to the prepared postimage, and byte identity everywhere outside the two replacements. Independent Git-blob calculations match the complete native source identity. These checks do not execute the TypeScript or SQL.

The complete 754-entry tree was returned untruncated. Its root CONTRIBUTING.md is the same scaffold notice retained for the earlier public source qualification, with blob `1e015aa7e145db0cd0e306f7032cce130b8acbb8`; no AGENTS or NOTICE path appears in that tree. The root LICENSE is Apache 2.0 (`261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`), root/backend READMEs label MIT, and backend/package.json labels ISC. These inconsistent declarations are preserved as a limitation: only the minimal patch and this guide are published, without a copied full source module or an invented license grant.

No Node/TypeScript/SQL execution, tests, fixtures, lint, build, PostgreSQL/Redis/FX request, browser, timezone experiment, account, wallet, transaction, payment, sponsor contact, upstream source/metadata change or deployment occurs. The other authors' execution evidence is not replayed or relabelled as evidence for this change. Whole-issue acceptance, current funding and award ownership are not established. Separate denied or held PayD routes remain untouched.
