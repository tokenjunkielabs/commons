# Encompass #93: preserve stdout-only transaction exports

The existing [Encompass PR #155](https://github.com/mazaclub/encompass/pull/155), authored by yanyishuai, adds `exporttxhistory <file|-> [json|csv|txids]`. Its helper writes the selected payload to stdout when the destination is `-`. The command then returns a summary dictionary, and the actual CLI dispatcher prints every non-None result. A successful streamed export therefore receives an extra JSON object after its JSON, CSV or transaction-ID content.

This packet makes the command return `None` after the helper successfully writes a stdout export. The existing dispatcher already suppresses None results. Exports to named files retain their original summary dictionary, and the helper continues to return its record count to its existing callers.

## Source and attribution

- Original issue: [mazaclub/encompass #93](https://github.com/mazaclub/encompass/issues/93).
- Existing external contribution: [PR #155](https://github.com/mazaclub/encompass/pull/155); author yanyishuai.
- Exact external head: `0154e24e7f020aa4fd3ed1ffcfebb3149c382320`, branch `feat/issue-93-export-tx-history` in `yanyishuai/encompass`.
- Observed base: `110a4dee78e30a87a7212f26374c3991e887d040`.
- Complete preimage `lib/commands.py`: `fb3c5578f8b0d28979aad38beaa35df2b9bcf98b`, 20,403 bytes.
- Complete postimage `commands.py`: `2c94abe1788fc72c2017f7265343e4c4ef5beb37`, 20,604 bytes.
- Unchanged helper `lib/history_export.py`: `2c9d8eca3593ef6333b50ce74a2deaef1a884ce9`.
- Unchanged actual CLI entry point `encompass`: `e702aec3fafd9dfce56eec2080c6dc54560dc5fa`.
- Original GPL version 3 license: `94a9ed024d3859793618152ea559a168bbcbb5e2`.

The postimage preserves the original copyright and GPL-3.0-or-later source notice and adds a dated modification notice. The original complete license is included. This is a narrow continuation of the named contribution; the external PR and its author are unchanged.

## Exact source behavior

The existing `run_command` dispatcher calls the command, performs its existing cleanup, then uses:

```python
if type(result) == str:
    print_msg(result)
elif result is not None:
    print_json(result)
```

The correction occurs after the successful call to `write_history_export`:

```python
count = write_history_export(self.wallet, file_name, export_format)
# The helper owns stdout; run_command prints non-None results.
if file_name == '-':
    return None
return {'exported': count, 'format': export_format or 'json', 'file': file_name}
```

For a named file, the same summary is returned. For `-`, the helper's payload is the only output introduced by this command's successful return path. No additional stdout newline, stderr summary, reserialization or in-memory capture is added. The same rule covers JSON, CSV and txids because all three already use the same destination sentinel.

This does not claim that every legacy startup, failure or daemon path is machine-readable: existing exception reporting and unrelated console output are unchanged. The helper's validation, ordering, timestamp handling, encoding, CSV behavior and GUI integration are also unchanged. Direct callers of `Commands.exporttxhistory('-', ...)` now receive None rather than the summary dictionary; that is intentional and matches the existing CLI suppression contract. `write_history_export` itself retains its count return value.

## Static validation and limits

The complete production preimage, helper, entry point, contribution guide, license and 232-entry untruncated Git tree were retained before editing. No AGENTS.md or RULES.md was present in that upstream tree. The patch has two hunks, +4/-0: the modification notice and the three-line successful-stdout branch/comment. Original CRLF line endings are preserved. A separate line-oriented application of the serialized unified patch reproduced the complete postimage exactly; computed Git blob identities bind the source bytes.

No Python interpreter, wallet, network connection, transaction, GUI, dependency installation, test, build, benchmark or workflow was invoked. This is source reasoning and text/identity validation, not runtime acceptance. The upstream contribution guide describes real usage/testing and a develop-branch submission workflow; those external steps were not performed. No upstream fork or submission was created.

## Funding and delivery boundary

Issue #93 contains a historical $200 Bountysource offer. Its 2015 comments already credit the original plugin work and confirm it worked after configuration; this packet does not claim to be that original implementation. The June 2026 external PR adds CLI export, and this packet addresses its specific successful-stdout return path. The historical offer does not establish current funds, a new award, first-reporter status or payout eligibility.

At qualification, the current external PR was open with no PR comments or inline review comments. The bounded public Slack search returned no matching Encompass activity, and the exact all-state own-author PR search returned zero matches; neither observation proves universal ownership absence. No sponsor, contributor or account was contacted.

To inspect or integrate the correction, use `change.patch` against the exact external head and compare the resulting `lib/commands.py` with the included complete postimage. The other three original PR paths remain outside this packet.
