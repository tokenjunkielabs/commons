# Cloud delivery through the existing account publisher

Use this route for a prepared original GitHub contribution whose description
cannot be updated by the connected installation. The existing public
`woahwhattheheck/commons` Actions repository has the documented
`COMMONS_GITHUB_TOKEN` binding. A workflow can use that binding without copying
the credential into a cloud workspace.

## Observed capability

On October 4, 2026, [run 37202575150](https://github.com/woahwhattheheck/commons/actions/runs/37202575150)
made one authenticated GitHub `GET /user` request. The binding was present;
GitHub returned HTTP 200, account `woahwhattheheck`, ID `293286387`, type
`User`. Only binding presence, status and account identity were logged.

The subsequent [original-description operation](https://github.com/woahwhattheheck/commons/actions/runs/37202855569)
used the documented publisher endpoint with that binding. At 12:39:35 UTC it
returned HTTP 503, `CLASSIFIER_UNAVAILABLE`, reason `model_unavailable`, and
`Retry-After: 60`. A retry of the same operation after that deadline returned
the same result at 12:41:31 UTC. Both target readbacks retained the original PR
head and showed that the prepared description had not been applied.

The credential and authenticated route are established. These observations do
not establish completed author publication or a recovered classifier. Preserve
the pending operation:
`YV81-DESCRIPTION-HANDOFF-1791067384932539-A9C4792E`.
Its original handoff is [the existing YV81 message](https://tokenjunkielabs.slack.com/archives/C0BVANHNB26/p1791067384932539).

## Reuse the existing operation

1. Read the current contribution and its existing publication handoff. Keep the
   original PR, branch, contributor, operation ID and prepared payload. A
   transient retry uses the same operation ID and bytes.
2. Put a bounded, single-run workflow on a separate branch in the existing
   **public** Commons repository. Use a push trigger for that exact branch,
   standard Ubuntu and Node 22. Bind the existing secret to the publication
   step's environment. The demonstrated carrier needs no checkout, package
   install, new schedule, private-repository Actions job, or owner-PC process.
3. Reconcile the target immediately before writing. If its body is already the
   intended body, record that and stop. If its head or body has changed since
   preparation, retain the existing handoff and compose the newer work before
   publishing. Keep historical tested-source pins distinct from newer
   documentation heads.
4. Send the existing named operation through the established publisher:
   `POST https://account-publisher.tjlabs-publisher.workers.dev/v1/publish`.
   The shipping caller uses `Authorization: Bearer <existing binding>`,
   `Content-Type: application/json`, and
   `User-Agent: Commons-Shipping-Enforcer/1.0`.
5. Read the original target after the response when the provider timing permits.
   Record the actual head and exact body comparison. A completed workflow job
   alone establishes only that its script finished.

The named description payload is:

```json
{
  "operation_id": "<existing-operation-id>",
  "operation": "pull.update",
  "args": {
    "owner": "<upstream-owner>",
    "repo": "<upstream-repository>",
    "pull_number": 81,
    "body": "<prepared-public-description>"
  }
}
```

The [executed one-shot workflow](https://github.com/woahwhattheheck/commons/blob/abcf68349013baad6c8e1a6bacb4d32c8a134f22/.github/workflows/yv81-description-publication.yml)
shows the exact request contract and target reconciliation. It contains the
specific YV81 input; preserve that operation rather than replaying it for
another target. Its observation includes publication attempt, publisher HTTP
status, allow/result codes, supplied retry timing, observed head and
`body_matches`.

## Existing free classifier credential

The current publisher can use the existing shared `groq/api-key` credential
through the per-request `X-TJLabs-Groq-Key` HTTPS header. The October 4 health
response advertises `groq-existing-free`, with `persisted: false`; the publisher
does not retain that request key. The existing account equipment completion
records the provider's Free/$0 plan. Retrieve the existing key through the secure
shared credential facility and use it only in the requesting runtime. Keep the
value out of workflow source, logs, Slack, artifacts and Git.

`runner.mjs` accepts an optional `GROQ_API_KEY` already present in its runtime
environment and forwards it only to the fixed central publication endpoint.
Publisher requests refuse redirects; GitHub reads never receive this header.
Missing keys preserve the existing publisher/default classifier behavior, so
this source change alone does not establish classifier recovery.

The historical one-shot workflow above binds only `COMMONS_GITHUB_TOKEN` and
does not carry the Groq header. A later caller using the restored Groq transport
must supply its securely retrieved existing key to this header; the historical
workflow is not evidence that such a runtime binding exists in Actions. Do not
create credentials, new secret bindings, an alternate publisher or a tunnel to
make that example appear ready. The current runtime owner retains recovery and
the existing operation; confirm actual classification and upstream readback.

## Provider timing and private data

Keep a batch sequential and reuse current operation custody. Honor a provider's
`Retry-After` before another publisher call; repeated transient failures merit
longer spacing. A classifier outage is not resolved by changing accounts,
creating another queue, or writing directly around the publisher. Existing
incident holds and the current runtime owner's diagnosis remain authoritative.

Keep credential values and raw private publisher responses out of workflow
source, console logs and public artifacts. Log only the small observed status
fields needed to reconcile the operation. The example's literal public PR body
is suitable for this public carrier; private drafts need the existing private
input route.

## Existing sources

- [Shipping caller](runner.mjs): configured binding, endpoint, headers and
  named-operation payload.
- [Private gateway guide](https://github.com/woahwhattheheck/commons-ship-enforcer/blob/main/work/commons-operations-gateway/README.md):
  original request custody and receipt semantics. Its issue-webhook route uses
  the second account, so it does not establish author permission on these PRs.
- The shipping monitor's current `read_only` and Slack delivery state remains
  described in [README](README.md). This note documents a manual GitHub
  operation through the existing account publisher.
