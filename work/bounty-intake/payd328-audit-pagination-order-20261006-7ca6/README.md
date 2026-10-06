# Deterministic ordering for tied transaction-audit timestamps

The mounted transaction-audit listing uses LIMIT/OFFSET but orders only by `tal.created_at DESC`. Different transaction records can have the same creation timestamp. This patch adds `tal.id DESC` as a second key, preserving the existing primary order while making the order of distinct returned transactions unique for a fixed result set.

This is a narrow source continuation associated with [Protocol-Guild/PayD issue 328](https://github.com/Protocol-Guild/PayD/issues/328). It does not implement or claim PostgreSQL index tuning, measured performance improvement, or completion of that broader issue.

## Canonical source and attribution

Repository: [Protocol-Guild/PayD](https://github.com/Protocol-Guild/PayD).
Donor commit: `171c74b454daba241bfb75f36d10a0a3a77a68e5`.
Changed path: `backend/src/services/transactionAuditService.ts`.
Source blob: `82bf96c35e3a39d9fae87822a6661b03a04bc328`, 5851 UTF-8 bytes.
Prepared blob: `b182b439672f70a29642ebe84df81c6fa36f51f2`, 5945 UTF-8 bytes.

The bounded current repository-specific PR query for issue 328 returned no matches. The one returned public issue comment, by rupesh-kumar-sah, requests assignment and describes a proposed implementation; it is not a maintainer acceptance or assignment. The current issue metadata listed no assignee. This packet does not take over that contributor's work or act upstream.

The latest returned path-history entry is commit `8d07522a75eb7226940f6886c5666a12d8082fcd`, attributed to Uchechukwu-Ekezie. That entry is an observed path-history attribution, not a claim of sole authorship of every line. Original repository contributors retain their authorship.

The exact repository-root Apache-2.0 LICENSE is retained as blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` (11,357 bytes). The backend package separately labels itself ISC; this packet records that metadata and makes no broader licensing determination. Only a focused patch, this guide and the unchanged root notice are published; the complete donor module is not republished. A dated modification comment is included in the patch.

## Actual caller and schema contract

Complete retained sources establish this caller chain:

`backend/package.json` dev/build/start scripts → `backend/src/index.ts` → `app.ts` → `routes/v1/index.ts` mounted at `/api/v1` → `auditRoutes.ts` at `/audit` → `TransactionAuditController.listAuditRecords` → `TransactionAuditService.list`.

| Exact path | Git blob |
| --- | --- |
| backend/package.json | 746a535b08bf0c6ce9c4a96f7d75c76e0bbacb95 |
| backend/src/index.ts | c883ae8949f35230c651c798e1e413306e5f47f1 |
| backend/src/app.ts | e2a3bab453f710e31c16daccc9cf6860ef677d75 |
| backend/src/routes/v1/index.ts | 764671221be230029249d835ddd38dbe01e6af6a |
| backend/src/routes/auditRoutes.ts | 68f4fb0e78c4e2f927b67769581a0ed5d583ebeb |
| backend/src/controllers/transactionAuditController.ts | e61f0f185b77e764710c36bb7c1575c951715aad |
| backend/src/services/transactionAuditService.ts | 82bf96c35e3a39d9fae87822a6661b03a04bc328 |
| backend/src/db/migrations/006_create_transaction_audit_logs.sql | 3f9af4c9a25d941bfcdc81aadf214814835886a3 |
| backend/src/db/migrations/001_create_tables.sql | 31f957cf4c3cd7ecb84d6ac112882fe98b23caf7 |

The controller already validates positive integer page and limit, with limit capped at 100. Migration 006 declares `transaction_audit_logs.id SERIAL PRIMARY KEY`, unique transaction hashes and `created_at TIMESTAMP DEFAULT NOW()`. The data query groups payroll rows by transaction hash before the join, then joins employees by their primary key. The added ID therefore distinguishes separate transaction rows, including rows tied on the first sort expression.

The published [PostgreSQL 16 LIMIT/OFFSET documentation](https://www.postgresql.org/docs/16/queries-limit.html) explains why a unique ORDER BY is needed for a predictable subset. This is primary documentation for SQL ordering semantics, not evidence of a deployed database version or an executed query.

The separately inspected INDEXING_STRATEGY guide concerns logical SDS payroll indexing. Its performance claims and examples were not run or adopted as evidence for physical PostgreSQL index selection.

## Exact change and validation

The only executable-source edit is:

`ORDER BY tal.created_at DESC` → `ORDER BY tal.created_at DESC, tal.id DESC`.

The dated notice makes the complete source delta +2/-1 in two hunks. The SQL column selection, aggregate joins, COUNT query, optional filters, parameter ordering, pagination arithmetic, values array, return type, Horizon calls and stored transaction behavior remain byte-identical outside that edit.

Complete source text and native Git blob identities were retained before editing. Independently computed source, postimage and patch identities matched their intended bytes. Forward patch reconstruction equals the prepared complete source, reverse reconstruction equals the original source, and removing the notice plus the one sort-key addition restores the original bytes exactly. This is source/patch identity validation only.

No SQL, migration, database connection, EXPLAIN, benchmark, package install, compiler, tests, application runtime, fixture or synthetic transaction was executed. No account, employee record, wallet, transaction, payment, sponsor contact, upstream issue/PR or assignment action occurred.

## Limits

The tie-breaker does not provide a shared snapshot across page requests. Concurrent insertion, deletion or updates can still shift OFFSET pages. It does not introduce keyset pagination or alter existing null timestamp behavior.

The count query joins individual payroll rows while the data query aggregates them; consistency of employee/asset filters between those two forms remains a separate existing concern. The inherited date-end, status/type, tenant/authentication and audit-integrity behavior is unchanged. No financial correctness, index-performance, installation/deployment readiness, complete issue acceptance or economic reward is claimed.

The patch applies to the exact donor blob above; later source movement must be reconciled explicitly. Existing source/access failures and unrelated contributor ownership remain in force.
