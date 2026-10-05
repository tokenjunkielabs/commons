# Count the mounted payment route once per sensitive limiter

This is a narrow source continuation for [Protocol-Guild/PayD issue #347](https://github.com/Protocol-Guild/PayD/issues/347) and SrvFernandes's existing [PR #668](https://github.com/Protocol-Guild/PayD/pull/668). It removes a duplicate registration of the same sensitive rate-limiter instance along the submitted app-to-router path.

## Source and original work

The issue was observed OPEN and unassigned. Its two comments are third-party requests: one asks for assignment; the original PR author links #668 and claims the issue. Neither establishes maintainer assignment, acceptance or payment. The current PR was OPEN/unmerged at `aaedd022da6860eba7468d1fca086d93683d9d50`, with base `171c74b454daba241bfb75f36d10a0a3a77a68e5`; its discussion and inline-comment collections were empty.

Three complete source files were read at that head:

| Path | Git blob |
| --- | --- |
| src/app.js | 9786a84c0a775c53654f99c38c2838ef7389a3a0 |
| src/routes/payments.js | 11b3a4b8847443a6b8f5b6ec27cae8992e519c7b |
| src/middleware/rateLimit.js | 55b95277f4ad49ddb87aa638280b18d8250dd735 |

The original author added audit, rate-limit and tenant middleware plus a payment route/model proposal. This patch retains their authorship and does not declare that larger proposal complete.

## Duplicate middleware path

The limiter module constructs and exports one general limiter and one sensitive limiter. The sensitive configuration declares a fifteen-minute window and max 10; it is the same exported instance used by the auth and payments mounts.

The app first runs the general limiter, then registers the sensitive limiter for /api/auth and /api/payments. It subsequently runs tenant middleware and mounts the payments router. That router imports the same sensitive limiter and registers it again before its POST handler. A request that reaches both sensitive registrations therefore invokes the same middleware twice.

The [official express-rate-limit double-count documentation](https://express-rate-limit.mintlify.app/reference/error-codes#err-erl-double-count) identifies repeated invocation of the same instance as a cause of counting a request more than once and directs removal of extra calls when only one limit is intended. This is the documentary basis for the source correction. The diagnostic itself was added in version 6.9.0; this packet does not assert that version 6.7.0 emits it. The submitted package declares ^6.7.0, while an installed version was not observed. The exact v6.7.0 source-page request returned DisabledError and remains held; its implementation call site was not independently recovered.

The one-hunk patch removes only the payments router's duplicate import, comment and registration: +0/-4. The app's /api/payments registration remains in its original position before tenant processing. The general limiter, auth registration, sensitive configuration, shared instance/store and POST handler remain byte-identical. Thus the actual submitted app path keeps its existing pre-tenant limit and avoids the extra router invocation. It does not create separate auth/payment budgets or change configured limits.

The scope is this mounted router. The packet does not promise a limiter if someone imports that router under a different app without the established app-level registration. It also does not claim every historical request reached the duplicate call: an earlier limiter, tenant rejection or other error can end processing first. No actual counter, response, retry time, throughput or quota experiment was performed.

## Text checks and unresolved integration

The original payments.js blob `11b3a4b8847443a6b8f5b6ec27cae8992e519c7b` maps to postimage `3e0526335ec16e3c45831d3743b8d8827739a953` (499 bytes). The serialized patch applies exactly to the complete preimage and reverses exactly to it; all bytes outside the removed registration block remain unchanged. These are source-text checks, not runtime validation.

The broader PR remains incomplete. Its package diff contains JSON comments and a trailing comma; the complete untruncated 764-entry tree lacks the declared src/index.js and required src/routes/auth.js; the submitted payment handler references Payment without importing it. The patch does not invent those missing implementations or alter tenant trust, model semantics, authentication, auditing, financial fields or payment processing. It should not be reported as a runnable backend or whole issue #347 resolution.

The acquired tree identifies the same complete instruction/licensing blobs already read for the separate #660 qualification: CONTRIBUTING.md `1e015aa7e145db0cd0e306f7032cce130b8acbb8`, LICENSE `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`, and README.md `374ffef680426f41b9f3e832059106839cfc72bd`. There is no AGENTS.md or nearer instruction/license in that tree. CONTRIBUTING.md is a scaffold placeholder. LICENSE is Apache 2.0 while README shows an MIT badge. This packet retains that discrepancy and publishes only an attributed patch and guide, not a full source module.

No Node/Express execution, dependencies, tests, fixtures, build, server, HTTP payment request, counter/store access, employee/customer input, account, credential, wallet/transaction, upstream contact/submission/claim, award or payment action occurred. Existing access and topic holds remain. Publication in Commons does not alter the original PR or establish native acceptance.
