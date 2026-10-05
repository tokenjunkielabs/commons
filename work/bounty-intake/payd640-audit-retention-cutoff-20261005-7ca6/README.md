# PayD #341 / PR #640 — audit retention and hash readers

The submitted `purgeOldLogs` method computes a retention cutoff and then deletes every scanned tenant audit key without checking age. This attributed patch reads the timestamp already written by the same service and deletes only records with a finite parsed timestamp strictly before that cutoff. A second correction makes the list method read those same hash records through HGETALL, matching the existing single-record reader. These are source corrections, not an executed retention job, audit query or claim that the broader backend submission works.

## Canonical donor and source identity

Source: [Protocol-Guild/PayD issue #341](https://github.com/Protocol-Guild/PayD/issues/341) and SrvFernandes's [PR #640](https://github.com/Protocol-Guild/PayD/pull/640).

- Donor head: `004ce3c71338e75c036e723123c3351401d8e4af`.
- External branch: `SrvFernandes/PayD:feat/onlydust-fix-341-1790979324629`.
- Observed PR base field: `171c74b454daba241bfb75f36d10a0a3a77a68e5`.
- Changed source: `src/services/audit.service.ts`.
- Full original: `7625ed07518e719ccde47c7005ad5b620d1f4eff`, 4,757 UTF-8 bytes.
- Full postimage: `151fd354151f19b9018ad851dc542beab622f881`, 4,981 UTF-8 bytes. The prior retention-only postimage remains `4f836e1b390632c63e593d95ed001cda22cebaf5`; the new list-reader change composes with it.

At qualification the external PR is OPEN and unmerged, with seven added files, no discussion comments and no inline review. Issue #341 has a separate contributor's assignment request and SrvFernandes's PR link/claim; the issue itself is unassigned. Those comments do not establish maintainer selection, accepted work or reward eligibility. The actual issue body requests generic backend auditing, rate limiting and multi-tenant robustness. The concrete change here follows the supplied method's existing name, parameter and unused cutoff; no missing product policy is invented.

The complete service, `src/index.ts` (`9806f1b64d7a5986404a3d21f2155cd1148d0c22`) and `src/middleware/audit.ts` (`3153b6ef31bece072018b8bfb60a33315a3b0fbd`) were read, together with the full seven-file native patch set and untruncated 765-entry tree. Source acquisition did not read stored audit entries, live requests, tenant records, environment values or credentials.

## Exact behavior change

The original writer uses `HSET` on `audit:<tenantId>:<id>` and serializes its timestamp through `entry.timestamp.toISOString()`. The public `purgeOldLogs(tenantId, daysToKeep = 90)` method computes one cutoff, walks the existing SCAN cursor and matches the existing tenant-key pattern. Previously it bulk-deleted every returned key and incremented its count by the page length, irrespective of timestamp or whether those keys still existed.

The one-hunk patch replaces that bulk deletion with these steps:

1. Read only the hash's `timestamp` field using the already-imported Redis client.
2. Skip a missing key or field.
3. Parse the returned timestamp. Skip a non-finite parse result.
4. Delete the individual key only when its parsed instant is strictly earlier than the existing fixed cutoff.
5. Add the returned DEL count to `deleted`.

An equal-to-cutoff or newer instant is retained. An expired or concurrently removed key contributes zero actual removals; a repeated scan key cannot be overcounted merely because it appeared in the returned list. The cursor loop, key pattern, default parameter, cutoff calculation, method signature and propagated command-error behavior remain as supplied. No new reader of other audit fields, request admission rule, authorization mechanism, tenant selection or scheduled caller is introduced.

The official [Redis HGET contract](https://redis.io/docs/latest/commands/hget/) provides a hash field's string or nil when the field/key is absent. The official [DEL contract](https://redis.io/docs/latest/commands/del/) counts keys actually removed and ignores nonexistent keys. These primary references support command semantics only; they are not observations of an installed Redis server or this application's execution.

## Hash-list continuation

The same complete service writes audit entries as hashes with HSET and reads one record with HGETALL in `getAuditLog`. Its list method instead used MGET and JSON.parse against the selected hash keys, which did not match that stored representation.

The additional one-hunk correction uses `Promise.all(keys.map((key) => redis.hgetall(key)))` and filters empty returned objects before using the same raw-record cast as the single reader. No keys produces an empty result without Redis commands; a missing/expired hash is omitted. Returned records keep the selected key order. A command failure rejects the operation; no partial-result fallback is added. A selected key containing a non-hash value now follows HGETALL's type-error behavior rather than being silently treated as a missing string by MGET.

Direct [Redis MGET documentation](https://redis.io/docs/latest/commands/mget/) states that non-string keys produce nil. Direct [HGETALL documentation](https://redis.io/docs/latest/commands/hgetall/) specifies hash fields/values and includes the ioredis object response used by the existing single reader. These are command/type conventions, not a live service result.

The earlier retention hunk from [Commons #31763](https://github.com/woahwhattheheck/commons/pull/31763) remains byte-exact. This continuation changes two production lines (+2/-2); the cumulative original-donor patch has two hunks and +10/-5. It adds one HGETALL per selected key in place of one MGET. That is an explicit request-cost tradeoff, not a performance improvement claim.

This aligns Redis data types only. The raw hash fields still have the same string representation as the existing single-record reader; Date objects and nested metadata are not reconstructed. The declared AuditLogEntry cast does not validate or decode those fields. The existing single SCAN, slice, unspecified scan ordering, ignored filter/offset options and unmaintained count index remain unchanged, so the returned `total` can still disagree with readable rows. No snapshot, complete pagination, installed-server behavior or audit-data acceptance is asserted.

## Scope and remaining source limitations

The method-level age rule is qualified for an ordinary finite nonnegative `daysToKeep` and the writer's ISO timestamp format. The patch does not add parameter validation or enforce a strict timestamp schema beyond checking the parse result. It does not establish that arbitrary noncanonical date strings represent trustworthy audit times.

Reading a timestamp and deleting its key are separate operations. There is no atomic compare-and-delete guarantee if another writer changes or replaces the same key between those operations. The existing scan is not a frozen snapshot or an exhaustive account of keys added/removed during the pass. A command failure can leave earlier eligible deletions complete before the method rejects; no transaction, rollback, retry or best-effort swallowing is added. The extra work is one HGET per returned key and an individual DEL for each eligible observation; no latency or throughput result is claimed.

The service's existing write TTL of 2,592,000 seconds remains distinct from its manual purge default of 90 days. This patch does not promise 90-day retention, restore previously expired entries, change the TTL, flush buffered entries first, repair nested-field serialization, maintain the unused count index, or make shutdown flushing complete. No actual caller of `purgeOldLogs` was established in the bounded source assessment; it is not newly mounted as a route or scheduled.

The root package `f0325832d3e5150375bd22481e577d19cd148eb6` is the retained frontend manifest and does not declare this added service's backend dependencies. The separate backend manifest `746a535b08bf0c6ce9c4a96f7d75c76e0bbacb95` declares ioredis ^5.9.3, but its scripts target `backend/src`, not the new root `src` files. Installed dependency resolution, deployment entrypoint and TypeScript compilation are unestablished. Other submitted middleware has independent import/type/syntax and ordering issues, including the literal unparenthesized `||`/`??` expression in its IP helper. The full tree does not supply the imported root `src/services/tenant.service` implementation. This small patch does not make the whole PR ready or establish tenant isolation.

## Attribution, licensing and validation

The donor tree matches the previously fully read CONTRIBUTING.md `1e015aa7e145db0cd0e306f7032cce130b8acbb8`, LICENSE `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` and README `374ffef680426f41b9f3e832059106839cfc72bd`. The contribution file is a short placeholder. The root license is Apache-2.0, the README advertises MIT, and the separate backend manifest labels itself ISC; those discrepancies remain unresolved. No AGENTS.md, RULES.md or nearer license/instruction appears in the qualified tree. This packet publishes an authored patch and guide, preserving the external author's provenance; it does not republish the full module or alter external terms.

The cumulative patch contains two hunks, +10/-5 production lines: the original +8/-3 retention change and the new +2/-2 list-reader correction. Exact forward application to the full pinned preimage yields the recorded postimage, and exact reverse application yields the original bytes. Native and independently computed original blob identities agree; the postimage identity is independently recorded. These are source-string/serialized-patch checks.

No Redis connection, HGET, DEL, purge, audit query, environment lookup, account, tenant, credential, payment, runtime, test, install, build or upstream action was performed. Commons publication readbacks verify the artifacts and their source identity, not live behavior, data retention, security or sponsor acceptance.
