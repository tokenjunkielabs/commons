# Report failed placeholder searches as failed audits

This source packet corrects the placeholder-search status handling in [Stellar-Analysis/frontend](https://github.com/Stellar-Analysis/frontend/tree/482ee456369418ef82c4056718cb82d3468f762b). The existing script treats a search error like a clean no-match result. The correction records the immediate exit status, preserves normal match/no-match behavior, and makes other statuses fail the audit.

## Exact source

| Item | Value |
| --- | --- |
| Donor commit | `482ee456369418ef82c4056718cb82d3468f762b` |
| Path | `scripts/config-audit.sh` |
| Executable mode | `100755` |
| Preimage | `b08890b61a061988c1b12ea46f66c5a6b1bbde8d`, 2209 UTF-8 bytes |
| Postimage | `a7a4a64c7250eb97f69ffa07768b26c14a0a82d7`, 2502 UTF-8 bytes |
| Patch | `placeholder-search-status.patch`, blob `061e73655b909b2c70830dae56c37cc767252524`, 1049 bytes |
| Complete change | +6/-1, two hunks, 18 diff rows |

The [complete script](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/scripts/config-audit.sh) was acquired at this immutable revision and independently identified. The bounded path history returned [da308f058a49d223e4350a4925d5290070a7e2ae](https://github.com/Stellar-Analysis/frontend/commit/da308f058a49d223e4350a4925d5290070a7e2ae), attributed to Ndifreke000 and describing the introduction of the audit script with other security work. This observation preserves that contribution without claiming an exhaustive authorship history. A dated modification comment marks this continuation.

Apply both hunks only to the exact preimage above, preserving mode and final newline. The actual serialized patch was parsed and materialized in both directions: forward produced the complete intended postimage, and reverse reconstructed the complete preimage. All 18 diff rows were retained without truncation.

## Existing defect and change

The original loop runs a recursive `grep` for each of its three configured placeholder strings. It sets `EXIT_CODE=1` only when the immediate status equals zero. Any other status leaves the accumulated result unchanged. Consequently, an unsuccessful search operation can reach the same success path as an ordinary no-match result when the other checks have not already failed.

The correction captures that status immediately in `scan_status`. It applies the normal grep status distinction explicitly:

| Captured status | Corrected handling |
| --- | --- |
| 0 | Retain the existing found-placeholder diagnostic and set `EXIT_CODE=1`. |
| 1 | Continue without a new failure; this is the ordinary no-match outcome. |
| Any other status | Emit a scan-failed diagnostic on stderr, including the configured placeholder label and numeric status, and set `EXIT_CODE=1`. |

The flag remains accumulated across all placeholders. A later no-match result cannot clear an earlier match or scan error. The loop still continues so the existing later checks can run and report their own outcomes.

No global `set -e` or trap is added: ordinary no-match status is handled explicitly, not converted into an unintended early stop. The original recursive grep command, patterns, exclusions and output behavior are unchanged. The new diagnostic distinguishes an incomplete search from a finding; a nonzero audit result alone is not evidence that a secret was found.

This is reasoning about the complete source and its expected grep exit-status convention. It is not an observed process run. An attempted open of `https://www.gnu.org/software/grep/manual/html_node/Exit-Status.html` returned a timeout error. That exact route remains held and was not retried or replaced. No claim is based on having successfully read that page.

## Direct CI invocation

The complete [security-audit workflow](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/.github/workflows/security-audit.yml), blob `15814931bf7a8398b084b2b4297f8c13f43f3135` / 927 bytes, directly marks `./scripts/config-audit.sh` executable and invokes it in its Codebase Configuration Audit step. That step has no `continue-on-error` setting, while several adjacent dependency-audit steps do. The workflow runs on pushes and pull requests targeting main/master.

This establishes the script's intended caller from retained source. It does not demonstrate that the complete job currently runs successfully: other steps still reference the former nested frontend/mobile layout. This packet changes neither workflow settings nor repository layout, and it does not recreate missing backend or mobile source.

The separately read `package.json`, blob `2b1c6ac1f83096666c7fd6d5ba3fd22780e6b8eb`, contains no package-script invocation for this audit. The direct workflow call above supplies the concrete connection.

## Scope preserved

Everything from the backend template-check section through the final `exit $EXIT_CODE` remains byte-exact. In particular, an absent `backend/.env.example` is still explicitly skipped, present-template matching still uses its existing expression, and the mobile fallback check remains advisory. This patch does not redefine those policies or claim that every component was scanned.

The configured placeholders, recursive search root, directory/file exclusions, matching-line output, template variable names, existing success/failure summaries and exit-code mechanism remain unchanged. The source still uses its inherited working-directory assumptions. No credential, environment, database, repository scan, or authentication operation was performed while preparing the patch.

The read [configuration-validation guide](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/docs/configuration-validation.md), blob `d7adbc8914025c8a41ab3d54f3d11a83a4a65aa2` / 1582 bytes, describes wider component validation requirements. Those descriptions are not treated as runtime evidence or expanded into additional source changes here.

The exact public Slack filename query returned zero results and native END. This is a bounded query observation, not a global ownership or duplicate-work guarantee. The retained donor tree had 959 entries with `truncated:false` and no AGENTS.md or RULES.md path. The already-read root CONTRIBUTING.md, blob `f66db3b0eece27eb6fa888948c31ee8c7eabcfd2`, is explicitly an EventSource contribution/release guide; no package release or tests were run.

## Preserved notices

Three separately attributed documentation notices are included verbatim with their original line endings:

| Packet file | Donor source | Blob | Bytes |
| --- | --- | --- | ---: |
| `upstream-licence-mclaughlin.md` | [docs/LICENCE.md](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/docs/LICENCE.md) | `57740b9d4d86aedf5d518f2f363d5cf192c54127` | 1104 |
| `upstream-license-menke-laguna.md` | [docs/LICENSE.md](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/docs/LICENSE.md) | `af5411fa243cfcf2b61c79d081dbb6204e956041` | 1111 |
| `upstream-license-de-wet.md` | [docs/license.md](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/docs/license.md) | `4a766e268772888af5df56c3f6c608f68558b789` | 1080 |

Their original authorship is preserved. Their presence in a documentation directory does not establish a repository-wide license for every source file.

## Verification and delivery

Independent Git blob calculations identify the exact source transformation, patch, guide and notice copies. Structural review and complete forward/reverse materialization concern the actual authored patch; no synthetic input, permission-error fixture or test suite was created.

No Bash, grep, filesystem audit, npm/cargo audit, workflow, runtime, secret lookup or upstream action ran. Publication readbacks and final Git metadata are recorded after the actual Commons write. This source packet does not assert a clean security audit, deployed behavior, whole-project security, upstream acceptance or reward approval.
