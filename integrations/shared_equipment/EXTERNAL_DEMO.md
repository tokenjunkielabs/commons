# Michael external demo delivery

The generic `slack_post_message` operation retains its internal workspace
contract. Use `slack_post_external_demo_message` for public demo copy in
`michael-external-demo` (`C0C7S2D5QRE`). Its destination is built into this
concrete route: no channel, sender, username, or icon argument is accepted.

The tool uses the same existing encrypted Slack account and the current
publication and customer-link checks. Keep internal fleet instructions,
credentials, provider/model bylines, internal evidence URLs, and customer
contact details out of the public text. No channel member is contacted by DM
and no schedule or background relay is created.

## Discovery

Both tools are catalogued in `harnesses/catalog.json` (capability
`external-demo-slack`, returned by `discover_commons_capabilities` with
`capability: "external demo"`), in `integrations/shared_equipment/role_equipment.json`
(`tools`), and in the dynamic `equipment_capability_manifest` / `GET
http://127.0.0.1:8878/v1/tools` listing. Call shape: `POST
http://127.0.0.1:8878/v1/tools/call` with `{"request_id","call_id","name","arguments"}`,
where the sender takes `operation_id` and `text` (optional `thread_ts`) and the
read-only status tool takes `operation_id` (optional `message_ts`). Seats without
loopback access send the same object as a `commons_equipment_request` envelope in
`C0BU51F1PL3` thread `1788567066.179399` and read `commons_equipment_result`.

## Enable in the existing gateway

Deploy `external_demo.py` plus the additive `services.py` registration into the
existing equipment service checkout; preserve local service modifications and
all private journals. Reload that existing gateway using its normal process
procedure. No additional runtime configuration or credential is required.
Its existing Slack carrier stays in the internal live channel for request and
result envelopes. Do not point that carrier at the external demo conversation.

After reload, `/v1/tools` must expose both dedicated demo tool names. Submit
through the existing `/v1/tools/call` route or an internal carrier envelope,
using stable request/call IDs and a stable message operation ID:

```json
{"request_id":"michael-demo-recovery-20261006","call_id":"demo-message-01","name":"slack_post_external_demo_message","arguments":{"operation_id":"michael-demo-recovery-20261006-01","text":"The demo channel is receiving project updates again."}}
```

Only public demo copy belongs in `text`. The route does not forward everything
from the internal live channel. The sender must match the installed account
`U0BTGV2G589` / `B0BTD42EMFY` in workspace `T0BRETUB5TK`; provider channel
metadata must describe the exact existing Slack Connect conversation. Its
public/private setting may change without changing this fixed destination;
the owner changed it to public on 2026-10-06. This route changes no channel
setting.
The current installed bot returned `missing_scope` for `conversations.info`:
needed `channels:read,groups:read,mpim:read,im:read`, provided
`app_mentions:read,chat:write,channels:history,groups:history`. For that exact
scope failure only, the route reuses the owner's native Slack metadata read
on 2026-10-06 and requires a fresh successful bot history read of this channel.
That read confirmed the channel ID/name/workspace and private, shared,
external, active, nonpending flags, and listed the fixed bot as a member.
`inspect.destination_probe` records the provider's metadata failure, membership
result and metadata provenance. Other metadata errors do not use this fallback;
provider-answered channel flags are checked directly. No new OAuth scopes or
credentials are created.

The gateway ToolCallStore journals every tool call, including the dedicated
sender. Consumers of the optional connected router must mark a sender dispatch
`effect: "write"`; status is a read. Use direct gateway calls for this route
unless a concrete connected-router route is already configured. The private
demo journal additionally suppresses duplicate message operation IDs across
fresh gateway requests and restarts.

### Internal carrier receipts

When the request is submitted through the internal Slack equipment carrier,
the carrier emits a small machine-readable
`<commons_equipment_receipt>...</commons_equipment_receipt>` reply keyed by
`request_id` and the message `operation_id`. These receipts stay in the
internal carrier conversation; they are never copied into
`michael-external-demo`.

A post first emits `ACCEPTED` after the envelope is parsed and before the
outward tool call. The terminal receipt is one of:

- `DELIVERED` with only the fixed channel ID and provider Slack timestamp.
- `DUPLICATE` with the original safe delivery receipt when the message
  operation ID was already delivered.
- `FAILED` with a stable state/error code and an `uncertain` marker when
  reconciliation is required.

Receipt posts use their own ToolCallStore keys, so replaying the same equipment
request does not duplicate the ACK, terminal receipt, or outward message.
Receipt bodies deliberately omit the requested demo text and provider error
messages. The existing `<commons_equipment_result>` envelope remains
unchanged for compatibility.

## One-shot execution without a gateway restart

With the existing private account custody available in the current runtime:

```bash
python -m integrations.shared_equipment.external_demo inspect
python -m integrations.shared_equipment.external_demo post < /private/path/demo-message.json
python -m integrations.shared_equipment.external_demo status < /private/path/demo-status.json
```

`inspect` performs only account and destination reads. `post` accepts the same
message arguments as the dedicated tool; `status` accepts `operation_id` and
an optional `message_ts` recovered from the provider after an interruption.
Use `--journal /private/path/external_demo.sqlite3` consistently if overriding
the default private journal. Preserve that journal across calls and deployment.

In an already equipped Python runtime, reuse its in-memory token loader:

```python
from integrations.shared_equipment.external_demo import ExternalDemoMessages

route = ExternalDemoMessages(existing_equipment, journal_path=private_journal)
try:
    result = route.submit(message_arguments)
finally:
    route.close()
```

No credential value enters the message, command arguments, output, or journal.

## Outcomes and reconciliation

`DELIVERED` requires fresh provider readback matching the fixed sender, bot,
exact channel/message timestamp, and exact text. A returned permalink is
optional; its lookup cannot erase a successful readback. Any appended footer
is a mismatch. A repeated operation with identical input returns the prior
confirmed receipt without another send; changed input is an idempotency
conflict.

`RECONCILE_REQUIRED` never resends. Run the status tool using a new call ID
and the original message operation ID. If the provider accepted the send but
the process lost its timestamp before journal save, recover its exact message
timestamp from the channel and supply `message_ts` to status. Status still
verifies the complete original body and sender. A missing timestamp cannot be
converted into a claim that no message was delivered.

`REJECTED` records a definitive provider rejection with `delivered: false`.
Fix that exact provider condition before a new send operation; preserve the
original rejection and follow any returned Retry-After. The route performs no
automatic retry, sleep, invitation, account switch, or channel creation.
