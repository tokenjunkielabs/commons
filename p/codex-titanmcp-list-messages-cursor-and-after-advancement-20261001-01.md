# TitanMCP list_messages cursor and after semantics advancement

The existing `titanmcp-setup-schema` resource now includes the landed `list_messages` cursor and `after=` classifiers from source commits `b638acb02892bcee17e5a864357680409aaa4d47` and `06a973a9a7094fbd16c1f0697adc34214a8acf4a`.

## Producing outcome

- Consumer: GPT and ChatGPT MCP integration operators that need exact continuation and malformed-`after` behavior without fabricating an error class.
- Cursor classifier: `host/titanmcp_list_messages_cursor.py`, blob `6714449922d7caa0af0ad0b4e144a4acf0cec656`.
- Cursor receipt: `p/cursor-titanmcp-list-messages-cursor-20261001-01.md`, blob `ab1c41ef379f25d370b8aeb4c088c556625ca3b7`.
- Unknown-after classifier: `host/titanmcp_unknown_after.py`, blob `860df4611ba1c07065b028c3a80ed11d208cf3cc`.
- Unknown-after receipt: `p/cursor-titanmcp-unknown-after-20261001-01.md`, blob `366fea77efb796050a1459205510ff59e772f5df`.
- Resource Master claim: [exact claimed paths](https://tokenjunkielabs.slack.com/archives/C0BRGMDQB6G/p1790881236042379).

The landed receipts record that a known COORD RESULT cursor returns HTTP 200 and may leave a listed `assignment_result` bubble without an id. Unknown and empty string `after=` values return HTTP 200, MCP `ok:true`, and the full transcript. Null and numeric `after=` values return MCP `isError` `BAD_ARGUMENT` for argument `after`, not JSON-RPC `-32602`.

## Activation checks and boundaries

Both exact source files compile normally and under `python -O`. The cursor `--bake` and `--deploy` probes and unknown-after `--bake` and `--go` probes return rc=2, `REFUSED`, and `sent=0`.

Fresh live execution was not repeated: each classifier creates remote room/task state and this activation had no exact cleanup receipt. The fresh landed live receipts are the remote evidence. No pad runtime, Commons adapter, deployment workflow, setup-schema code, SAVE/LOAD DRAFT lane, GET identity lane, Origin pair lane, pre-go hardening path, provider configuration, or Titan state was changed. Commons open-door/no-auth behavior is preserved.

No build order was created. Both capabilities are implemented and landed; adjacent pre-go hardening has an active claimant, and missing connector or owner authority is a gate rather than an implementation gap.

## Delta watermark

- Prior terminal main: `4c07bcfe20ffef09ab7808e92f1b2a56119b592d`.
- Activation base main: `31b49408ce2d301c598c0118e99161e3fbcf0377`.
- Delta: five commits, exactly two non-generated source commits.
- Prior terminal Slack timestamp: `1790872947.573039`.
- Latest external delta timestamp: `1790879941.188709`.
- Claim timestamp: `1790881236.042379`.
- Remote branches observed before claim: 4,577 across 47 pages; open PRs: one unrelated PR.
- Required Slack-channel sweep: only #commons had relevant new messages; #delegations, #todo, #shipped-builds, #products, #leads and #sales were empty after the watermark.
- Automation surface: 25 total, two enabled and 23 disabled; no lifecycle mutation.
- Projection: 118 resources / 89 producing / 90 append-only inventory records.

Publication PR, merge SHA, hosted-check accounting, and exact current-main readback are appended below after landing.

**LOCK NOT SHIPPED / AWAITING BRYCE GO.**

