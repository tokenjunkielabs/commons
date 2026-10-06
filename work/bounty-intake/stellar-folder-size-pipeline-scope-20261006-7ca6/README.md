# Keep the folder-size failure decision with its pipeline state

This packet corrects the existing folder-size policy script in [Stellar-Analysis/frontend](https://github.com/Stellar-Analysis/frontend/tree/482ee456369418ef82c4056718cb82d3468f762b). The script already detects oversized directories, but its failure flag is written inside a pipeline loop and then inspected outside that loop. The patch puts the flag, loop and failure decision in one pipeline stage.

## Source identity and attribution

| Item | Value |
| --- | --- |
| Donor commit | `482ee456369418ef82c4056718cb82d3468f762b` |
| Path | `scripts/check_folder_size.sh` |
| File mode | `100644` |
| Preimage | `0326de024e231ea0c762a125da1b075d88c01023`, 697 UTF-8 bytes |
| Postimage | `33d607f4de6065b9e3cba75951a2d2b150e0d32d`, 819 UTF-8 bytes |
| Patch | `folder-size-pipeline-scope.patch`, blob `2dafdd02f4b9aab0641c9112766e099d3a05055c`, 1526 bytes |
| Complete change | +15/-12, one hunk, 37 diff rows |

The [complete original script](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/scripts/check_folder_size.sh) was acquired at the immutable donor revision and independently identified. Its bounded path history returned [d31eb692ffb7922cd32f2dc684072d95e463abae](https://github.com/Stellar-Analysis/frontend/commit/d31eb692ffb7922cd32f2dc684072d95e463abae), authored by Ndifreke Ekanem / Ndifreke000 on 2026-03-31, introducing the folder-size enforcement alongside documentation cleanup. That authorship is retained. A dated source comment identifies this continuation.

Apply the complete patch to the exact preimage above. The original file has no final newline; the postimage preserves that property, and the unified patch carries its explicit no-newline marker. The file mode is unchanged. Exact materialization from the serialized patch reconstructs both complete files, including the EOF boundary.

## Why the original decision can pass

The original script initializes `BAD=0` in its parent shell, then uses `find . -type d -print0 | while ...` to measure directories. In ordinary Bash pipeline execution, the loop runs in a separate shell environment. Its `BAD=1` assignment does not update the parent's variable. The later parent-side `if` therefore sees the original zero and reaches the success message even after the loop printed an oversized-directory error.

This is a control-flow conclusion from the complete source under its standalone Bash execution contract. It is not a recorded shell run. The script does not enable Bash's `lastpipe` option, and the correction does not rely on that option or a particular job-control setting.

## Corrected control flow

The final pipeline command is now a brace group. It initializes `BAD`, runs the existing measurement loop, and makes the existing violation decision inside that group. An oversized directory sets the same flag that the group's final decision reads. The explicit violation `exit 1` supplies a nonzero result for that pipeline stage.

The success echo remains after the completed, standalone pipeline. The existing `set -euo pipefail` remains active: a nonzero producer or final-stage status prevents reaching that echo in the intended invocation. The measurement assignment still contains the original `du | awk` pipeline; neither its command text nor its failure handling is replaced. Grouping does not require state to be copied back into the parent.

The pipeline is not placed in an enclosing `if`, `||` or other conditional status context that could change the intended `errexit` behavior. There is no process-substitution producer whose status would fall outside this pipeline. The group works with the same local flag and decision whether Bash executes the final stage in a subshell or in the current shell.

A separate nongating design review considered that scope and status relationship and identified no concern with the proposed standalone grouping. It did not execute Bash or supply runtime validation.

## Actual caller and preserved policy

The complete [enforcement workflow](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/.github/workflows/enforce-folder-size.yml), blob `c6d24388eb8c7d806fc055184a2daeb6c5bfd05a` / 301 bytes, runs on pushes and pull requests. After checkout it marks this script executable and invokes it. That is the retained, direct caller; the workflow is not modified or dispatched.

The limit stays `MAX_MB=200`, using the inherited `du -sm` measurement and output label. The script still traverses every directory below its current working directory, including the root it starts from. Per-directory measurement, NUL-delimited traversal, quoting, the strict greater-than comparison, all existing output messages and the violation exit status remain intact. The patch does not introduce an exclusion list or redefine the size policy.

Each directory still invokes its own measurement. This avoids introducing a new shared multi-argument `du` invocation or a different counting policy. No throughput improvement is claimed. Concurrent filesystem changes, permission diagnostics suppressed by the inherited redirection, and the chosen scope and threshold remain properties of the existing script.

## Source qualification and held documentation

The retained donor tree returned 959 entries with `truncated:false`; no AGENTS.md or RULES.md path appeared. The already-read root CONTRIBUTING.md, blob `f66db3b0eece27eb6fa888948c31ee8c7eabcfd2`, explicitly describes contributing to EventSource and that package's release process. No package release or test command was run.

The precise public Slack query for `check_folder_size.sh` returned zero results and native END. That describes this bounded query only; it does not establish global ownership absence or clear any other contributor's lane.

Two attempted GNU Bash documentation opens, `https://www.gnu.org/software/bash/manual/html_node/Pipelines.html` and `https://www.gnu.org/software/bash/manual/html_node/Command-Grouping.html`, returned timeout errors. Those exact acquisitions remain held. Neither page was retried, substituted or represented as successfully read. The explanation here distinguishes source inspection and Bash control-flow reasoning from fetched documentation or runtime evidence.

## Preserved notices

Three separately attributed documentation notices are copied verbatim, with their original line endings:

| Packet file | Original donor path | Blob | Bytes |
| --- | --- | --- | ---: |
| `upstream-licence-mclaughlin.md` | [docs/LICENCE.md](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/docs/LICENCE.md) | `57740b9d4d86aedf5d518f2f363d5cf192c54127` | 1104 |
| `upstream-license-menke-laguna.md` | [docs/LICENSE.md](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/docs/LICENSE.md) | `af5411fa243cfcf2b61c79d081dbb6204e956041` | 1111 |
| `upstream-license-de-wet.md` | [docs/license.md](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/docs/license.md) | `4a766e268772888af5df56c3f6c608f68558b789` | 1080 |

The different original authors and notices are preserved. Their presence in the documentation directory is not treated as a license declaration for every repository file.

## Verification and delivery boundary

All 37 rows of the actual one-hunk patch were retained without truncation. Parsing that serialized patch, including its EOF marker, yielded the exact complete preimage and postimage. Independent Git blob calculations cover the source, patch, guide and copied notices. These are checks of the actual authored transformation and publication contents.

No synthetic directory tree, fixture, test, shell, `find`, `du`, workflow or runtime was executed. No upstream branch, PR or issue was changed. Commons publication readbacks and final metadata are recorded separately after the real write. This attributed source packet does not claim deployed CI behavior, upstream acceptance or a reward.
