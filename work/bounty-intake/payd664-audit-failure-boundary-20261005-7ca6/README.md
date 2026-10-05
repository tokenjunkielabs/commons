# Preserve response dispatch when audit setup fails

This is a narrow source continuation for [Protocol-Guild/PayD issue #354](https://github.com/Protocol-Guild/PayD/issues/354) and SrvFernandes's existing [PR #664](https://github.com/Protocol-Guild/PayD/pull/664). It corrects the proposed audit middleware's insertion call and the boundary between audit failures and the wrapped response.

## Exact source and original work

The issue was OPEN and unassigned. Its three comments contain two third-party assignment proposals and the original author's PR link/claim; they do not establish maintainer assignment, acceptance or compensation. PR #664 was OPEN/unmerged at `5f0a2c86079a094e091f21739cfd45af13b61554`, based on `171c74b454daba241bfb75f36d10a0a3a77a68e5`. Its discussion and inline-comment collections were empty. The original author supplied the backend proposal; this packet preserves that attribution and leaves the external PR unchanged.

The following complete files were read at that exact head:

| Source path | Git blob |
| --- | --- |
| backend/middleware/auditing.js | 1974cef3d06f1e52a59ce72cc1a1994d8592f204 |
| backend/models/AuditLog.js | ee4238db259a724998d58fa2c91353f0798373ba |
| backend/app.js | 660008e87019d13e3d6c5da7bc74bae0c49b0d63 |
| backend/package.json | 746a535b08bf0c6ce9c4a96f7d75c76e0bbacb95 |
| package.json | f0325832d3e5150375bd22481e577d19cd148eb6 |

The full nine-file PR diff and untruncated 768-entry head tree were also acquired. The diff contains the original migration, validation, rate-limit and tenant-service proposal; none of those paths is changed by this patch.

## Audit operation and error boundary

The middleware saves the original res.send, installs a wrapper, constructs an auditEntry inside that wrapper, and calls AuditLog.create(auditEntry).catch before forwarding to the original response. The supplied AuditLog class extends Objection Model and declares its table, JSON schema and relations, without a create method.

The [official Objection query guide](https://vincit.github.io/objection.js/guide/query-examples.html#insert-queries) starts model queries with query() and performs insertion by chaining insert(). This is the primary contract for changing the call to AuditLog.query().insert(auditEntry). The actual installed ORM version and any external runtime augmentation are unobserved; the submitted package does not declare Objection.

A promise catch cannot intercept a synchronous exception thrown while constructing its receiver or arguments. In the original wrapper, audit-entry serialization or query setup can therefore throw before the existing rejection handler is attached, preventing the subsequent originalSend call. This contradicts the source comment's intended nonblocking audit behavior.

The patch places audit-entry construction and the insertion chain inside a try/catch. It retains the existing asynchronous rejection handler and uses the same error-reporting statement for a synchronous audit failure. It does not await the insert. The originalSend.call(this, data) invocation remains after and outside the protected audit block, with its receiver, data argument and return value unchanged. An exception from the original response is therefore not swallowed as an audit failure.

All audit-entry field expressions remain exactly the same apart from indentation. The model, schema, migration, caller ordering, rate limits, tenant context and response body are unchanged. No new log fields, retry, queue, storage operation or authorization gate is introduced. Ordinary console error reporting remains the existing behavior; the change is not a guarantee against process termination or failures inside a replaced error logger.

## Explicit unresolved boundaries

This remains a proposed source bundle. The backend package is type:module and points to src/index.ts, while the new app and middleware use CommonJS. Its dependencies do not declare Objection, Knex, express-rate-limit or express-validator. The complete tree lacks the proposal's required backend/routes/auth, backend/routes/users, backend/models/User, backend/models/Tenant and backend/database/connection files. This patch does not supply those dependencies/modules or wire the new app into the TypeScript entrypoint. It is not a claim that the backend can currently start.

The model declares string-only user and tenantId properties while the middleware can supply null. That separate validation mismatch is unchanged and may reject an attempted insert. Persistence, database connection setup and schema compatibility remain unverified. The original body/query/params capture policy and possible repeated wrapper invocation are also unchanged; this packet does not certify privacy, exactly-once auditing, successful storage, tenant authorization or the completeness of issue #354.

## Text checks and publication scope

The single-file serialized patch has 1 hunk, +25/-21 lines, including indentation inside the new protected block. It applies exactly to preimage `1974cef3d06f1e52a59ce72cc1a1994d8592f204` and reverses exactly from postimage `6cb01235f0107d17a8a7e5ce1a0cfd9758414455` (1227 bytes). Independent Git blob calculations match the source identity. The audit-entry fields and the originalSend/next/export tail were compared as retained text. No production function was executed.

The head tree identifies the already-read CONTRIBUTING.md `1e015aa7e145db0cd0e306f7032cce130b8acbb8`, LICENSE `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`, and README.md `374ffef680426f41b9f3e832059106839cfc72bd`. There is no AGENTS.md or nearer instruction/license in the complete tree. CONTRIBUTING.md is a scaffold placeholder. The root LICENSE contains Apache 2.0, the README displays an MIT badge, and backend/package.json declares ISC. Those inconsistent declarations remain explicit. Only an attributed patch and guide are republished; no full source module or new licensing conclusion is supplied.

No Node/Express/ORM execution, server, database, migration, audit write, real request or payload, credential, employee/customer data, account, tenant action, test, fixture, build, install, upstream contact/submission/claim, payment or acceptance action occurred. Existing private, source and access holds remain.
