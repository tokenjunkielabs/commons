# PayD: clear queued export headers before JSON errors

The existing export controller prepares PDF, Excel or CSV download headers before awaiting document generation. If an operation fails before any headers have been sent, its catch branch switches to an HTTP 500 JSON response, but does not explicitly clear the queued download metadata. This patch removes Content-Type and Content-Disposition in that existing unsent-response branch before the existing JSON call.

The concrete change is removal of queued download headers. It is not a runtime observation of a browser download or a claim about the unavailable exact Express response implementation.

## Canonical source and attribution

Intake: [Protocol-Guild/PayD issue192](https://github.com/Protocol-Guild/PayD/issues/192), the receipt-download request. That broader frontend feature, organization branding and whole-issue acceptance are not implemented or claimed by this packet.

Canonical donor: `Protocol-Guild/PayD@171c74b454daba241bfb75f36d10a0a3a77a68e5`. Changed production file: `backend/src/controllers/exportController.ts`.

The complete controller, generator service, export router and version-one router were retained. The export router binds the PDF, Excel and CSV handlers; the complete version-one router mounts it at /exports. Current canonical app.ts code-search excerpts show the v1 import and `app.use('/api/v1', v1Routes)`. The package entrypoint is src/index.ts. These source observations establish the route connection, not a deployed or successfully started server.

Original PayD contributors retain authorship. The latest returned path commit is `bfa3661fa80a8c5c7161cc63a335739696a9c4e4`, attributed to Uchechukwu-Ekezie, an integrated-state sync rather than evidence of sole authorship. No external branch, PR, issue, comment, assignment or claim was changed. The bounded numeric issue192 PR query returned no rows; bounded receipt/export searches returned unrelated frontend or other carriers. Those are not a global absence or ownership assertion.

| Retained source | Git blob |
| --- | --- |
| backend/src/controllers/exportController.ts | ab32c67d75a8ecbf676377c0f8724e4adde7ad0f |
| backend/src/services/exportService.ts | d2c28d8378a143f0e3dc91fa7f0d9c025e878880 |
| backend/src/routes/exportRoutes.ts | b6d8ad85f17a53a1187b9ec8ccc9faf7b7d384a7 |
| backend/src/routes/v1/index.ts | 764671221be230029249d835ddd38dbe01e6af6a |
| backend/package.json | 746a535b08bf0c6ce9c4a96f7d75c76e0bbacb95 |
| backend/package-lock.json | 2803b2048d296fadbd21baae3ad89b660226cd47 |

## Patch and response boundary

Apply `export-json-headers.patch` to the immutable donor, or explicitly reconcile the exact contexts against a later revision.

| Changed production source | Preimage | Prepared postimage | Prepared UTF-8 bytes |
| --- | --- | --- | ---: |
| backend/src/controllers/exportController.ts | ab32c67d75a8ecbf676377c0f8724e4adde7ad0f | f9ac605769c6beac953cd9ac55db425b439bdc37 | 4,203 |

The four-hunk change is +7/-0, including a dated modification notice. Each of the three existing `if (!res.headersSent)` branches gains exactly these two statements, before its unchanged status and JSON calls:

```ts
res.removeHeader('Content-Type');
res.removeHeader('Content-Disposition');
```

The successful generator paths and their download headers are unchanged. The existing 404 behavior, HTTP 500 status, fixed error payloads, logger calls, queries, transaction fields, batch limit, service implementations and already-sent `res.end()` branches are unchanged. There is no additional await between the unsent check and header removal.

This handles the controller's queued-header transition only. It does not abort generators, detach stream listeners, destroy a response, retract bytes already sent, reset unrelated headers, prevent a later producer from writing, guarantee error recovery after disconnect, or validate document content. Stream races, backpressure, query scope/authorization, employee privacy, transaction authenticity, asset/date/amount correctness, branding and filename validation are outside this change.

## API evidence and exact-source limitation

The complete package and lock bind Express 5.2.1 (manifest range ^5.2.1) and PDFKit 0.17.2. They are source configuration, not proof of an installed or deployed runtime.

[Node's HTTP documentation](https://nodejs.org/api/http.html#responseremoveheadername) describes removeHeader as removal of an outgoing header queued for implicit sending; headersSent distinguishes whether response headers have been sent. The existing check is retained, and removal happens only in that branch.

[Express 5's response documentation](https://expressjs.com/en/5x/api/response/#res.json) describes res.json as the JSON response method. Its attachment documentation identifies Content-Disposition as download metadata. This patch explicitly clears the two previously queued download fields before the existing JSON response call.

The attempted direct source page `https://github.com/expressjs/express/blob/5.2.1/lib/response.js` returned DisabledError. That exact source route remains held: it was not retried or acquired through another route. This guide does not infer that missing implementation's precise Content-Type preservation logic. The narrower queued-header correction rests on the complete donor controller and the documented response APIs.

## Validation and distribution

The complete original controller is 3,849 UTF-8 bytes; the prepared controller is 4,203 bytes. Independent Git identities bind both. Forward patch application reproduces the entire prepared source; reverse application restores the original exactly. Removing the six inserted header calls and the modification notice restores all original bytes. No source module was executed.

No HTTP request, document generation, database, stream experiment, synthetic error, fixture, test, compiler, application, browser, workflow, dependency installation, employee/account data, wallet, payment or upstream action was performed. Source identity and ordering assessment are not runtime or end-to-end acceptance.

The exact canonical Apache-2.0 notice is retained as LICENSE, blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`, 11,357 UTF-8 bytes, from the already retained matching donor base. The complete tree has no separate NOTICE file. Only the focused patch, this guide and the license are published; existing source notices are preserved and the changed source gains a dated modification notice.
