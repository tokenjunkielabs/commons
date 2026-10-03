# GitHub issue-update window + gap minute

Refs #16537.

This adapter records two coverage facts without claiming a full GitHub census:

1. The explicit 19:24 UTC gap minute stays `LOWER_BOUND` with zero items read.
2. A later issue-update window (the post-20:06 slice) is compiled from provider `updated_at` rows into the landed connector-projection packet.

## Run and consume the output

The default command returns the existing summary receipt:

```sh
python -m integrations.command_center.jev_github_issue_window packet.json
```

Export the actual event-ledger packet and pass it directly to the existing volume compiler:

```sh
python -m integrations.command_center.jev_github_issue_window packet.json --format ledger -o ledger.json
python -m integrations.command_center.jev_event_ledger ledger.json
```

Use `--format projection` when composing connector sources before ledger conversion. Library callers select the same outputs with `compile_window(packet, output_format="ledger")` or `output_format="projection"`. Invalid JSON, malformed source records and file failures return exit status 2 with a clear error message.

With `-o`, the command stages and flushes the complete JSON on the destination filesystem before atomically replacing the output. A failed write preserves an existing output and leaves a new destination absent, so the normal command can be retried. Successful replacement keeps the same selected JSON format and bytes.

Distinct normalized `updated_at` values for one issue remain separate event revisions. Repeated copies of the same revision collapse, while the issue's work identity remains stable. Summary receipts count distinct issues; `ledger_event_count` counts retained revisions. Source, work and operation identifiers distinguish other repositories while preserving the established Commons identifiers.

The packet schema is `commons.jev_github_issue_window/v1`. Incomplete pages stay `has_more=true`. The gap source never becomes complete merely because a later window was read.
