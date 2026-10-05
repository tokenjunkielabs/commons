# Apply the existing event-write permission before event creation

This source continuation corrects the route in [corecodeio/platform PR #68](https://github.com/corecodeio/platform/pull/68), which implements [issue #48](https://github.com/corecodeio/platform/issues/48). The external contribution is by BojayL. It remains open and unmerged; this Commons packet is not an upstream submission or a claim to its bounty.

## Production consequence and change

At the recorded head, POST /api/event runs authentication and then createEvent directly. Authentication verifies the session, rejects locked or missing users, and populates req.user.permissions; it does not require event-write permission. The controller then inserts a Google Calendar event, creates the database Event record, and, for daily messages, schedules Slack delivery. An authenticated account without write:event therefore reaches those side effects in the recorded source.

The corrected route imports the existing checkPermissions middleware and places checkPermissions(['write:event']) between auth and createEvent. This reuses the project's established permission value and write-route ordering. It adds no role, permission vocabulary, account flow, response format, or new authorization implementation. The existing middleware's denial responses remain unchanged.

The scope is the upstream application's event route. It does not change Commons publication, activity, or access behavior.

## Exact source and dependencies

- Upstream contribution: BojayL/platform, branch event-route-daily-message.
- Exact branch name: `event-route-daily-message`.
- Immutable head: `d6f0a43979884b64003a2f5ebfd5553157456bdd`.
- Base: `91ed07b92e7ede625fd1a210c5a2262d6f9d5065`.
- Original `api/src/routes/event.router.js`: `38ef0b1e1ac0d34be40ba7f98e54c3554752d556`.
- Corrected route Git blob: `ce5a9209ac75540a05c09286ddee15f2a6dcdb05`.
- Existing auth middleware: `ee0c7b1bbe5f646e41266e21ce74736aafc777eb`.
- Existing checkPermissions middleware: `c471d1a136626f1209199c540a69434837449283`.
- Existing course route showing the same auth/permission/controller sequence: `efbfab3689d84fcee8b226b2eb78a36226a3fbdd`.
- Development-data source assigning the already existing write:event permission: `1a81670c395fd5da62df381ea5fc95183b22d841`.
- Event controller identifying the downstream Calendar/database/Slack side effects: `9914e1b75f8cf6e8b8e3d18f26ad6b597673583f`.

The complete corrected file is under `api/src/routes/event.router.js` in this packet. `event-permission.patch` changes only that upstream path, with two additions and one removal. Apply it to the pinned contribution, not to the upstream base that lacks the event route. The complete source was read before editing; its Git blob was computed from the retained UTF-8 bytes.

## Qualification and limits

Issue #48's complete body specifies creation of calendar events and daily Slack messages. Its comment endpoint returned an empty array despite the issue metadata reporting one comment. The exact issue remains open and unassigned; no advertised amount or award eligibility is established here.

PR #68's five-path metadata and complete production patch were read, along with its sole Netlify comment and empty inline-review collection. Its author reports focused checks; those reports are preserved as historical statements, not repeated. Earlier PR #58 is closed and unmerged, with a null head repository in current metadata. This packet neither revives that branch nor claims its acceptance.

This continuation was reviewed statically against the complete route, middleware, controller, model, and dependency sources. No application, test suite, fixture, endpoint, calendar, Slack send, account, credential, or workflow was executed. No live authorization result or delivery success is claimed. Scheduling durability, provider-error handling, event input validation, calendar/database atomicity, and issue #32's wider Slack-ID integration are outside this one-route correction.

The previously read complete repository tree contains no license or contribution-instruction file. Attribution and immutable source links are retained; no license grant is invented.

Operation: `PLATFORM48-EVENT-PERMISSION-20261005-7CA6`.
Prepared publication branch: `work/platform48-event-permission-20261005-7ca6`.
