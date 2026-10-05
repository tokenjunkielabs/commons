# SMTP configuration in aggregate health

The complete review in [REVIEW.md](REVIEW.md), delivered as Commons #31689, identifies a remaining condition in the existing PayD #680 proposal. This source continuation supplies the exact one-condition patch against the reviewed head.

## Original request and retained source

- Issue: https://github.com/Protocol-Guild/PayD/issues/505 — SMTP misconfiguration must no longer fail silently; email-service health and retry/logging behavior are requested.
- Existing PR: https://github.com/Protocol-Guild/PayD/pull/680, by `woahwhattheheck`, observed open and unmerged with head `c35d8229a43fac7f5d3d780a3c0b566e219abc24`. Its current metadata records zero comments and zero inline review comments.
- The sole issue comment is an external request for assignment. It does not supply maintainer assignment, acceptance or payment authority.
- Full controller preimage: `backend/src/controllers/healthController.ts`, blob `1a4ef16713d1378ea86a16596f14fd3c749ea18c` (5309 bytes).
- Full supporting producer: `backend/src/services/notifications/mailerService.ts`, blob `900ea171a0f7dedad2e5b70ed21335a4d6b5fc88`.
- Exact review: Commons #31689 at merge `33f9c1e9436b3fd7c0936defa65f701302404f3c`, review blob `2d379b1313efc4e24e4cb1bb815fe10a481eb622`.
- Prepared controller postimage: `832c35155d0322d5219f174fd83a9776e20f1c2a` (5306 bytes), retained in source custody; the module is not republished in this packet.

Original PR authorship and the review's investigation retain their credit. The sponsor PR, its existing tests and all contributor/award rights remain unchanged. This adds a concrete source patch to the existing review directory; it does not create a replacement sponsor PR.

## One-condition behavior

The mailer declares exactly three health states: connected, disconnected and not_configured. With incomplete SMTP settings it records a down transition and returns not_configured, an error description and the retry-queue count. The controller copies that dependency object but currently changes aggregate health only for disconnected.

The patch changes `emailResult.value.status === 'disconnected'` to `emailResult.value.status !== 'connected'`. For the producer's declared union, both disconnected and not_configured then set `isHealthy = false`, reaching the existing degraded/HTTP503 path. A connected email result leaves the aggregate flag unchanged; other dependencies can still degrade it. The nested email status, error and queuedRetries remain exact.

The separate rejected or timed-out email path already degrades and is untouched. Redis's existing optional not_configured treatment is also untouched: this is the email branch identified by the issue and producer's down status, not a global policy for every dependency. Liveness, timeout implementation, database/Horizon checks, mail retry scheduling, SMTP configuration and delivery functions are unchanged.

The complete serialized patch contains one hunk, +1/-1. Forward application to the retained complete preimage and reverse application to the retained postimage are byte-exact. Reversing the one predicate replacement produces the complete original controller, establishing that all other bytes are unchanged. These are text/source checks, not production execution or regression tests.

## Publication and verification boundaries

The current source tree has 755 entries and was returned untruncated. Root CONTRIBUTING.md is a short scaffold notice rather than a project-specific workflow; root and backend READMEs contain setup/contribution instructions. They label the project MIT, while the actual root LICENSE contains Apache License 2.0. This packet preserves that inconsistent declaration instead of selecting or inventing a license for a full copied module; only the minimal patch and this guide are published. The complete original declarations remain in retained source custody.

No test is added or run here. The earlier review's focused controller criteria remain unperformed and are not relabelled as a pass. No Node/TypeScript runtime, build, lint, browser, SMTP connection, email, database/Redis/Horizon request, wallet, payment, account, sponsor contact, upstream source/metadata mutation, assignment or deployment occurs. No private configuration or credentials were read.

The separate known PayD access/publication holds are unchanged. This public source qualification does not retry those routes or supply authority to publish upstream. Current award, funding, payment and whole-issue acceptance are not established. Apply the patch only to the exact PR head after reviewing local integration and the existing owner's workflow.
