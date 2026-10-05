# Preserve signup's existing fallback when Slack lookup fails

This source continuation is tied to [corecodeio/platform issue #32](https://github.com/corecodeio/platform/issues/32), which requests automatic Slack-ID integration. Current source already registers a team_join listener and calls an email lookup during signup. This packet repairs a concrete error-path defect in that existing lookup; it does not claim completion of every item in the historical issue.

## Production consequence

The signup controller first creates the Stytch account and the local User record, then awaits userEmailHandler(email). The helper already catches lookup failures and intends to return null. However, its diagnostic unconditionally reads error.data.error. Slack's [official Web API error-handling documentation](https://docs.slack.dev/tools/node-slack-sdk/web-api/#handle-errors) describes a data-bearing platform error separately from request errors, which carry an original error, and other error types. An error without data causes this diagnostic itself to throw, preventing the existing return null. The signup controller's outer catch then reports registration failure after its earlier creation steps have completed.

The correction guards only the diagnostic lookup. If error.data exists, the existing error.data.error value is retained; otherwise the log receives the fixed string unknown_error. The helper then reaches its unchanged null fallback. It does not log the raw exception, message, request, token, email or SDK response, and it introduces no retry or network action. Successful lookups, the API call, signup's response construction, account creation order and existing handling of absent Slack membership are unchanged.

This is a static consequence of the retained source and documented error shapes, not a report of an observed live signup failure. The SDK documentation is interface context; no installed dependency or SDK operation was executed.

## Exact source

- Repository: corecodeio/platform.
- Immutable source head: `91ed07b92e7ede625fd1a210c5a2262d6f9d5065`.
- Original `api/src/utils/slack/controllers/userEmailHandler.js`: `6cc807870ba02afba22668ae1e74551b79b8565e`.
- Corrected helper: `5857d176760ae61d58fcfa42845e50ec2c51ed49`.
- Signup caller `api/src/controllers/userControllers/signUp.controller.js`: `6c0ece4d9e22bb60db2ee180c4dfda27588f6778`.
- Slack application wiring: `feee50ebae4947cad69eed6a83f1efd85830e484`.
- Team-join listener: `a66668617e11ece23d49fc7d0785ae8f03ba2c62`, read but unchanged.
- Database model wiring: `a172c1b6e9b8be208a1a24290798932b6bcf1e9f`, read but unchanged.
- API package: `91e08001b3d4746808c989f2012f34b4cc9154cd`; declares @slack/bolt ^3.12.2. No dependency version is changed or claimed installed.

The complete corrected helper is stored at its original relative path in this packet. `slack-lookup-fallback.patch` changes only that source file, with four additions and one removal. Its original complete bytes were read and independently matched to the Git blob above; a later literal-main read returned the same complete preimage.

## Scope and validation

The current issue is open and unassigned. Its comment endpoint returned an empty array despite metadata reporting one comment. A bounded exact issue-number PR search returned zero results; this is not a repository-wide proof of no contribution. The current source tree contains User/Role/Permission wiring, with no observed Staff model or createStaff path. No obsolete staff interface is invented and no whole-issue acceptance is asserted.

The change was reviewed as a one-catch source edit against the complete helper and actual signup caller. No tests, fixtures, application, Slack API, account operation, endpoint, credential lookup or workflow was run. Runtime acceptance, provider reachability and actual account behavior remain unperformed.

The team-join listener's own diagnostics, email normalization, deferred reconciliation, duplicate-signup handling, transactionality and wider Slack synchronization remain outside this correction. The fixed diagnostic does not assert that console output or arbitrary user-defined error getters cannot themselves fail.

The API package reports ISC metadata; the retained complete tree has no separate license file. Upstream source attribution is preserved without inventing license text. This Commons artifact is not an upstream submission, bounty claim, or payment receipt.

Operation: `PLATFORM32-SLACK-LOOKUP-FALLBACK-20261005-7CA6`.
Prepared branch: `work/platform32-slack-lookup-fallback-20261005-7ca6`.
