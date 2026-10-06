# Await the returned audit shutdown promise

The donor SIGTERM handler calls `audit.shutdown()` and immediately reaches `process.exit(0)`. The audit service's shutdown method clears its timer and returns `this.flush()`; that asynchronous method can be waiting on the audit INSERT. The caller discards the promise and can terminate before this flush settles.

This patch awaits the existing returned promise before reaching the existing Redis-quit and exit sequence. A synchronous flag is set before the first await so a second SIGTERM callback cannot start another shutdown and reach exit ahead of the pending first callback. A directly thrown or rejected shutdown error is logged, then the original final sequence runs. The existing explicit exit status remains zero.

## Source and attribution

Canonical carrier: [Protocol-Guild/PayD PR 650](https://github.com/Protocol-Guild/PayD/pull/650), authored by `SrvFernandes`, associated with [issue 353](https://github.com/Protocol-Guild/PayD/issues/353). The donor branch is `SrvFernandes/PayD:feat/onlydust-fix-353-1790985002051`, exact head `4395f9b0eb574354efe533672e4f5dd03722c91e`, against base `171c74b454daba241bfb75f36d10a0a3a77a68e5`.

The original PR provides the audit service, application and other backend work. This Commons packet changes its shutdown caller only. The observed issue is open and unassigned; no author claim, assignment, award, funding or upstream acceptance condition is changed or satisfied by this packet. The PR's mixed numeric references, including its older 273 wording, remain external metadata; this guide identifies canonical issue 353 without editing that PR.

The existing [Commons #31784](https://github.com/woahwhattheheck/commons/pull/31784) corrects a different file's rate-window reply index. Its artifacts and result remain unchanged, and this patch composes on `src/index.js`. The prior ioredis v5.3.2 README source failure remains held; no dependency retry or alternate acquisition occurred.

## Complete source contract

| Donor path | Git blob | UTF-8 bytes |
| --- | --- | ---: |
| `src/index.js` | `95d4f47a399298e6930efa6e1b71a2564bf60edf` | 1105 |
| `src/services/audit.js` | `633700c17ebd501414746ed2792d390c22940026` | 2460 |
| `package.json` | `bb083e6733b4b2f9b9c51e2d913b1bc8eb1c7773` | 635 |

Complete source texts and independently calculated identities matched the donor's provider blobs. The fourteen-path PR diff supplies the exact changed-file identities and leaves the base license and root contributing instructions unchanged. No whole-repository execution or proof of all import paths is implied.

The root manifest names `src/index.js` as its main/start entrypoint and declares Express, PostgreSQL and ioredis version ranges. That source-level wiring differs from a deployment or installed dependency check. No lockfile installation, database configuration, route action or external service was exercised for this correction.

The full audit implementation establishes the relevant distinction:

- `shutdown()` cancels its interval and returns one call to `flush()`.
- `flush()` returns immediately when its buffer is empty.
- Otherwise it removes the current batch from the buffer and awaits its INSERT.
- It catches an INSERT failure, logs it and restores the removed entries; this path normally resolves rather than rejecting.
- Earlier flushes may already have removed their own batches. Their promises are not tracked or returned by this shutdown call.

The official [Node.js process documentation](https://nodejs.org/api/process.html#processexitcode), read on 2026-10-06, describes explicit process exit as synchronous termination that can abandon pending asynchronous work. This is the runtime contract motivating the caller ordering; no Node version was executed or installed.

## Resulting ordering and limits

On the first SIGTERM handled by this module, the flag is set, the existing shutdown function is invoked and its returned promise is awaited. Only after that promise settles does this caller initiate the original Redis quit and explicit zero-status exit. A repeated SIGTERM handled during the wait returns early. The flag is local to this module instance; there is no inter-process coordination.

This is a narrow ordering repair, not a durable audit drain:

- A flush already in flight before shutdown may have spliced its batch out of the buffer. Awaiting the new flush does not wait for that earlier operation.
- The HTTP server is not closed, and incoming requests or later audit records are not quiesced.
- A failed INSERT that the audit service catches and requeues still leads to the preserved exit-zero path; queued entries are not retried here.
- Redis quit is still initiated without waiting for completion. Pool closure, other process listeners and other asynchronous work are unchanged.
- There is no deadline or force-exit escalation. A never-settling shutdown promise leaves this handler waiting; subsequent SIGTERM callbacks do not bypass that wait. SIGKILL or external termination is outside this logic.
- The unchanged Redis quit invocation can itself fail. This packet does not establish successful process termination or log delivery under every cleanup failure.

Audit SQL, serialization, buffering, read filters, authentication, tenant policy, rate limiting and payment operations are not changed.

## Exact patch

`audit-shutdown-await.patch` applies to `src/index.js` at the exact donor head. It has two hunks, +14/-4 including a dated modification notice. Complete forward application reproduces postimage `1626c2de78727851ea74a9a7cf9ed872bfe5b63a` (1,375 UTF-8 bytes); complete reverse application reproduces preimage `95d4f47a399298e6930efa6e1b71a2564bf60edf` (1,105 bytes). These checks compare source strings and patch application only.

Only the focused patch, this guide and the exact existing license are published. The external PR and the earlier rate-window packet remain separate.

## Verification and licensing

Verification used complete source inspection, independent blob hashing, exact forward/reverse patch identity, the primary Node.js contract, and retained-source reasoning on the first-await/repeated-signal ordering. No Node application, signal delivery, database, Redis, test, fixture, build, workflow, backend request or synthetic execution was performed. No end-to-end durability, deployed readiness, upstream acceptance or reward is claimed.

The base `LICENSE`, Apache License 2.0, is reproduced unchanged: `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`, 11,357 bytes. Its presence is retained file custody, not a whole-repository legal conclusion. The patch includes a dated modification notice and preserves attribution to the source author.
