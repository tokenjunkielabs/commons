# Executing connected capability fallbacks

`host/connected_tool_router.py` executes the route choices from
`integrations.shared_equipment.services.plan_capability_fallback`. It consumes
`tool_fleet.free_pool_routes` in the existing connected capability observations;
there is no second public route registry. A standalone route array is also
accepted for an existing consumer's scoped runtime configuration.

The caller supplies concrete arguments for each compatible route. A capability
such as `documentation` is broad: Hugging Face documentation covers Hugging Face
products, while a library documentation request may need Context7. Use
`task_domain` plus each binding's `task_domains` to retain that distinction.
`*` means the runtime binding genuinely supports any domain. A caller's binding
specifies how to invoke a tool; a dispatch is an invocation request and does not
prove that the provider accepted it.

A request contains the existing `operation_id`, `capability`, `effect`
(`read`, `inference` or `write`), `input_sensitivity`, and `bindings`. Each binding
maps a route ID to `tool`, provider-specific `arguments`, and optional
`task_domains`. Bindings can also use a route's existing `native_tool` with
`arguments_by_route`. Missing arguments, unsupported task domains, unverified
Free plans, exhausted quota and observed cooldowns remain visible in the returned
plan. Consumption metadata never admits a worker or grants access.

One-time free grants also supply usable capacity when their actual positive
remaining balance is measured. An observed expiry ends that allocation. A
conditional credit pool additionally needs an observed zero-net-spend setting;
published credit offers alone do not establish it. These pools retain their
grant/conditional label rather than being counted as recurring free allowance.

## Automatic bridge execution

Python consumers instantiate `ConnectedToolRouter(routes, private_state_file)`
and call `run(request, invoker)`. The invoker receives a complete dispatch object
with `tool`, `arguments`, `operation_id`, `dispatch_id`, route and quota-domain
metadata. It must make one actual provider call and return its original JSON
response. The router switches to an eligible untried quota domain after a
recoverable failure; it never sleeps or reschedules work.

The CLI supports the existing provider adapters directly:

```sh
python host/connected_tool_router.py run \
  --routes-file inventory/resources/connected_capability_observations.json \
  --state-file /private/runtime/connected-tools.json \
  --provider-apis < /private/runtime/current-request.json
```

This dispatches existing shared provider tools, including the no-key Jina reader
and public OpenRouter model metadata. Credentialed generation still uses the
existing secure facility and the actual Free account/model route. The model
catalog is separate from inference entitlement. Alternatively use
`--bridge-command PROGRAM ARGUMENTS...` as the last option. That program receives
the dispatch JSON on stdin and returns the actual provider response on stdout.
Its nonzero exit or interruption is an unknown write outcome, not permission to
send the write again.

## Native ChatGPT tool execution

Native app tools belong to the host runtime. Use `dispatch` with the request on
stdin, invoke exactly the returned `tool` with its `arguments`, then use `resume`
with `{operation_id, dispatch_id, response}` on stdin. The response must be the
actual complete tool result, including `isError`, structured content, HTTP status
and provider retry metadata when exposed. Repeat only when `resume` returns a
new `DISPATCH`. `COMPLETED` returns the provider result. A binding failure remains
a typed failure of that tool and carrier; it does not erase another carrier's
working route or imply account authentication failed.

Each CLI operation uses the same `--routes-file` and `--state-file`. `status
--operation-id EXISTING_ID` reports current operation state without another
provider call. Exit 0 means a dispatch, pending response or completed operation;
exit 3 means no ready route, reconciliation or a terminal provider failure; exit
2 means an invalid request or local runtime error. Consumers inspect `decision`
as well as the exit code.

## Recovery and quota feedback

Keep runtime state outside Git and public artifacts. The state file contains
private arguments/results, atomic mode-0600 writes, an operation journal and
quota-domain cooldown observations. Processes sharing that file share those
observations; separate carriers must reuse their existing private state carrier
if they need a cross-machine cooldown map. Provider response headers and their
observation times determine Retry-After deadlines. Unknown allowance stays
unknown. A measured quota reset expires the observed exhausted window.

Every alias of the same quota domain shares its cooldown and exhausted state.
An operation does not retry another alias of a domain it already attempted.
Shared or unknown backend identity is reported explicitly and never increases
an asserted count of independent backend pools. A different provider can still
supply useful capacity; backend independence is a separate fact.

The operation journal records dispatch intent before invocation. A second
`dispatch` for an outstanding operation returns `AWAITING_PROVIDER_RESPONSE`
without another invocation request. A duplicate `resume` returns current state,
so it cannot replay an already emitted successor. Completed operations reuse
their cached result. `previous_effect=accepted` or `unknown`, an uncertain write,
or a write failure without evidence of rejection returns
`RECONCILE_EXISTING_WRITE`. Preserve native provider handles and read back that
operation through its existing consumer. Provider rejection is the only write
failure that can enter the fallback loop. Route arguments carry the same
logical intent and any supported provider idempotency key; the router does not
invent unsupported arguments for native app tools.

The October 4 implementation was consumed through an actual native Hugging Face
repository metadata dispatch/resume, and through a new Jina public-document read
using automatic provider execution. The source integration does not claim that
a changed gateway has been deployed to every carrier or that every connected
account's remaining allowance is known.

## Status-read cost

`status` reads one snapshot under the existing journal lock without serializing,
fsyncing or replacing the journal. It still validates the schema and reports
missing operations. Reading before the first dispatch does not create the journal;
the private parent/lock can still be created. `dispatch` and `resume` retain their
atomic mode-0600 write path, so a later mutation persists normally.

A bounded October 4 measurement ran the actual status method on a 528,553-byte
private journal containing 400 synthetic, credential-free operation records copied
from one completed dispatch/local-file-read/resume. On Python 3.12.14, Linux
6.18.44, warm `/dev/shm` tmpfs, seven alternating baseline/candidate pairs of ten
status calls each measured median wall time **5.241 to 2.684 ms/call** and median
CPU time **5.227 to 2.679 ms/call**. Five separately observed status calls replaced
the journal five times before and zero afterward; bytes and returned status stayed
identical. Pending and missing status, subsequent dispatch/resume persistence, and
unsupported-schema rejection also behaved as expected.

Raw samples in pair order, milliseconds per call:

| Pair | Before wall | After wall | Before CPU | After CPU |
| --- | ---: | ---: | ---: | ---: |
| 1 | 5.008957 | 2.913359 | 5.002398 | 2.637551 |
| 2 | 4.877986 | 2.962867 | 4.852837 | 2.946670 |
| 3 | 5.241063 | 2.683706 | 5.226649 | 2.682218 |
| 4 | 6.793644 | 2.525948 | 6.783353 | 2.525520 |
| 5 | 7.604662 | 3.309169 | 7.579763 | 3.303878 |
| 6 | 5.807610 | 2.679105 | 5.798003 | 2.678697 |
| 7 | 5.079171 | 2.633156 | 5.078172 | 2.632762 |

Baseline router blob: `ca47e1f947c32a8b1fb26bea5b5f8019e5113082`.
Measured router blob: `70fdef46453f0009f831f8fe0b6c7201804df2b7`.
Journal SHA-256: `68f877f9edc32b6e4a03d57d7dabff75dbd629035246cc9689ff4d52a989c1d9`.
The timing loop used `perf_counter_ns` and `process_time_ns`, excluding imports,
input preparation and result serialization. This measures local journal handling,
with synthetic records and warm caches; it does not measure physical-disk latency,
Windows locking, provider throughput or deployment to another carrier.
