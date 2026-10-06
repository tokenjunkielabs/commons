# Release the readiness client before draining its pool

The donor PostgreSQL readiness probe acquires a client, runs `SELECT 1`, releases it, and then drains its temporary pool. If the query rejects, the normal release statement is skipped. The outer `finally` still awaits `pool.end()`, which can wait for that same checked-out client instead of allowing the existing failure result to settle.

This patch places release in a nested `finally` immediately after successful acquisition. Query fulfillment and rejection both return the client before the outer pool drain. The existing success value, failure logging/false result, one-pool-per-check design, SQL, connection configuration and response structure remain unchanged.

## Canonical source and attribution

- Canonical repository: [Protocol-Guild/PayD](https://github.com/Protocol-Guild/PayD).
- Existing carrier: [PR 662](https://github.com/Protocol-Guild/PayD/pull/662), authored by `SrvFernandes`.
- Donor repository and branch: `SrvFernandes/PayD:feat/onlydust-fix-204-1790990760819`.
- Exact donor head: `e5beba9b05f952d469ff30017381b813aedc5188`.
- Observed base: `171c74b454daba241bfb75f36d10a0a3a77a68e5`.
- Request: [issue 204](https://github.com/Protocol-Guild/PayD/issues/204), infrastructure liveness and dependency-readiness endpoints.

The external PR supplies the controller and route implementation. This Commons packet is an attributed correction to one cleanup path, not an upstream replacement or a claim to the original feature. The observed issue is open and unassigned; its two returned comments are a separate contributor's interest and the author's existing PR/claim notice. Neither is new assignment, maintainer acceptance or a reward determination. External claim and award terms remain with the original carrier; no contact, registration or upstream mutation was made.

## Complete retained source contract

| Donor path | Git blob | UTF-8 bytes |
| --- | --- | ---: |
| `src/controllers/healthController.js` | `7525b56ab6c5342f92fa56f6c7603cec812eda70` | 1642 |
| `src/routes/healthRoutes.js` | `7f7d3d146673fd45fbbeb1c8d28eb74219707bf3` | 259 |
| `src/app.js` | `d47253a5178524b2fd817e6ca7a7fc32f9c0c133` | 270 |
| `package.json` | `f0325832d3e5150375bd22481e577d19cd148eb6` | 2117 |

All three changed source paths were read completely at the exact donor head. Their provider and independently calculated Git blob identities matched the complete PR file list. The root manifest was also read completely.

The root `src/app.js` is a placeholder integration snippet: it refers to `app` without constructing or exporting an application. The root manifest declares `type: module`, while these added files use CommonJS, and it does not declare `pg`, `redis` or `express`. Its start script launches the scaffold/Vite workflow. These observations do not establish that this root module is installed, executable or mounted in the actual backend. No missing application, module boundary, dependency manifest or deployment route has been reconstructed. This patch is useful at the donor source level and does not establish production readiness of PR 662.

## Library basis and exception ordering

The official [node-postgres pooling guide](https://node-postgres.com/features/pooling), read on 2026-10-06, requires acquired clients to be returned after query errors and describes pool shutdown as waiting for checked-out clients to return. The [Pool API](https://node-postgres.com/apis/pool) defines the release operation on acquired clients. This documents the interface used by the donor; no installed package version or live database behavior was verified.

- If acquisition rejects, the nested scope is never entered; the original catch and pool cleanup still run.
- If the query fulfills, the client is released before returning true and before pool cleanup.
- If the query rejects, release runs first, then the original catch logs and returns false, subject to the unchanged outer cleanup.
- An error from release or pool shutdown can still affect the result. A connection or query that never settles is not given a timeout by this patch.
- Redis creation, connection, ping and unconditional quit are unchanged. Redis cleanup/error-event behavior and the outer parallel readiness aggregation are separate unresolved paths.

There is no new connection, authentication, tenant, network or readiness policy.

## Exact patch and use

`readiness-client-release.patch` applies only to `src/controllers/healthController.js` on the donor head above. It has two hunks and +6/-2 source lines, including a dated modification notice. Complete forward application reproduces postimage `1e42ac225d60b55f5435d4eef9c0788c04e6c5b5` (1,762 UTF-8 bytes); reverse application reproduces the exact 1,642-byte donor preimage. Those are string/patch identity checks, not execution of the controller.

The packet publishes a focused patch, this guide and the exact existing license. It does not vendor the complete sponsor module or change another Commons packet.

## Verification and limits

Verification consisted of complete immutable source inspection, exact preimage matching, patch construction and forward/reverse identity, the two primary library references, and retained-source reasoning on exception order. No Node process, syntax compiler, application, database, Redis server, liveness/readiness request, dependency installation, test, fixture, build, workflow or browser was run. No timeout, whole-endpoint availability, installed-version compatibility, upstream acceptance, payment or reward claim is made.

## License custody

The unchanged base `LICENSE` is Apache License 2.0, Git blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`, 11,357 UTF-8 bytes, reproduced exactly as `LICENSE`. The retained base tree and three-path PR diff leave this license and the root contributing instructions unchanged. The root README's conflicting MIT badge is not resolved by this packet; the observed license is not represented as a legal conclusion about every repository file. The source patch carries its dated modification notice and retains original source context and author attribution.
