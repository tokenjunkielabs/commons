# PayD #353 / PR #650 — use the rate-window cardinality

The submitted Redis limiter queues five commands but reads the fourth reply as its request count. That fourth reply belongs to ZADD, which reports newly inserted members. The fifth reply belongs to the already-queued ZCARD, which reports the window set's cardinality. This patch changes one array index so the existing allowed and remaining calculations use the intended count.

## Canonical source and attribution

Source: [Protocol-Guild/PayD issue #353](https://github.com/Protocol-Guild/PayD/issues/353) and SrvFernandes's [PR #650](https://github.com/Protocol-Guild/PayD/pull/650).

- External head: `4395f9b0eb574354efe533672e4f5dd03722c91e`.
- External branch: `feat/onlydust-fix-353-1790985002051`.
- Observed base field: `171c74b454daba241bfb75f36d10a0a3a77a68e5`.
- Production path: `src/middleware/rateLimit.js`.
- Complete original: `055b339d547f59205ff86100a67b4cc45da49baa`, 2818 UTF-8 bytes.
- Complete postimage: `fa2371b9e17927afa159d645e2402feb0a005273`, 2818 UTF-8 bytes.

At qualification PR #650 is OPEN and unmerged, with fourteen changed files and no discussion or inline-review comments. Issue #353 requests generic backend auditing, rate limiting and multi-tenant robustness. Its two comments are a contributor's assignment request and the donor author's PR link/claim. Those are not maintainer acceptance or reward eligibility. The donor body also names a different issue number; this packet preserves the actual #353-to-#650 comment linkage without treating that inconsistent numbering as a new implementation contract.

The complete limiter, configuration module `src/config/database.js` (`5b4a9317bf97e3b60b7383a94342c3176128b0a4`) and root `package.json` (`bb083e6733b4b2f9b9c51e2d913b1bc8eb1c7773`) were read. All fourteen native file patches and the untruncated 771-entry tree were retained. Complete added-file patches reconcile to their provider blobs before their caller context is used. No live environment, stored request, account, tenant or credential data was read.

## Exact correction

The pipeline's zero-based reply mapping is:

| Index | Queued command | Use in this correction |
| --- | --- | --- |
| 0 | INCR of the separate counter key | Unchanged |
| 1 | EXPIREAT of that counter | Unchanged |
| 2 | ZREMRANGEBYSCORE of the window set | Unchanged |
| 3 | ZADD of this request's member | Was incorrectly used as the total count |
| 4 | ZCARD of the window set | Now supplies the existing count variable |

Only `const count = results[3][1];` becomes `const count = results[4][1];`. The command sequence, sorted-set pruning, member generation, clock, key names, configured limits, comparison, remaining calculation, response headers, status code, fallback and route mounting are unchanged.

Under successful ordinary command replies, ZADD's one-member insertion result cannot represent the number of members accumulated in the window. ZCARD is already queued after pruning and insertion, so selecting its reply repairs the direct count mismatch without adding a Redis call. This conclusion follows from source order and documented command semantics; it is not an observed request sequence or a performance measurement.

The current [ioredis primary README](https://github.com/redis/ioredis#pipelining) documents replies in queued order as error/result pairs. The [Redis ZADD reference](https://redis.io/docs/latest/commands/zadd/) describes its default insertion count; [ZCARD](https://redis.io/docs/latest/commands/zcard/) returns sorted-set cardinality. These references support the reply mapping only. The donor declares ioredis `^5.3.2`; installed resolution was not established. A separate attempt to read the exact v5.3.2 README returned an Internal Error and remains held, without retry or alternate acquisition. The successfully read current README is not represented as a version-pinned source or runtime check.

The actual new `src/index.js` mounts payment and tenant routers. Their complete added-file patches import and use the existing apiRateLimit middleware. This establishes a submitted caller for the limiter, not a deployed or successfully started application. The strict limiter export and all route paths remain as submitted.

## Limits that remain

This correction assumes a successful five-entry pipeline response. It does not validate null results, individual error entries, result types or partial command failures. Existing command-error handling may therefore still yield unsuitable behavior; no fail-open or fail-closed guarantee is made.

The pipeline is not made into a transaction or atomic admission operation. Other clients can interleave work, the random member identifier can collide, and request/clock ordering can affect the observed set. Existing pruning boundaries and the treatment of denied requests remain unchanged. No exact distributed-limit or fairness guarantee is asserted.

The separate INCR counter and its expiration still run although the decision uses the window set. The sorted-set key still lacks its own expiration; memory fallback still retains per-key state. Existing reset/retry metadata, option defaults, tenant-key construction and memory-versus-Redis differences are untouched. No new limits, identities, permissions, routes or admission policy are introduced.

The root package now targets `src/index.js` and declares Express `^4.18.2`, ioredis `^5.3.2` and PostgreSQL dependencies. This donor replaces the previous frontend-oriented manifest and README; this packet does not endorse that broader replacement, lockfile compatibility or installed dependency state. The submitted CommonJS modules, database/migration assumptions, authentication and tenant behavior, audit buffering, error handling and shutdown behavior have separate unresolved scope. No entire-PR readiness, security, multi-tenant isolation or deployment claim follows from this one-line correction.

## Licensing and validation

The current tree has the already fully read `CONTRIBUTING.md` at `1e015aa7e145db0cd0e306f7032cce130b8acbb8` and root `LICENSE` at `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`. The contribution file is a placeholder. The root license is Apache-2.0 while the donor README labels the project MIT; that discrepancy is retained. No AGENTS.md, RULES.md or nearer license/instruction appears in the qualified tree. The packet contains an authored patch and guide, preserving SrvFernandes's provenance; it does not republish the full module or alter upstream terms.

The patch is one hunk, +1/-1. Exact source-string forward application yields the recorded complete postimage; reverse application yields the complete original. Provider and independent original identities agree, and the postimage identity is recorded independently. A separate supplied-source review confirmed the reply-index ordering, with no provider or runtime call.

No Redis connection or command, server request, rate-limit exercise, environment lookup, data migration, account, tenant, credential, payment, test, install, build, workflow, runtime or upstream action was performed. Artifact readbacks establish publication identity, not operational acceptance.
