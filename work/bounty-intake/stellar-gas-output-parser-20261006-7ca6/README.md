# Parse Criterion timing triples without an empty success

This packet corrects the existing `scripts/check_gas_regression.py` in [Stellar-Analysis/frontend at the pinned commit](https://github.com/Stellar-Analysis/frontend/tree/482ee456369418ef82c4056718cb82d3468f762b). It contains a source patch, this integration guide, and verbatim copies of three separately attributed MIT notices found in the donor's documentation directory. It does not publish an upstream change or claim a working contracts benchmark job.

## Exact source and change

| Item | Value |
| --- | --- |
| Donor commit | `482ee456369418ef82c4056718cb82d3468f762b` |
| Source path | `scripts/check_gas_regression.py` |
| File mode | `100644` |
| Preimage | `f3d724b73c1fa6ca27660bb49aa632c4800f8c83`, 4605 UTF-8 bytes |
| Postimage | `9d33878394747ffb1eb542bd708e6e9685a4943d`, 5075 UTF-8 bytes |
| Patch | `criterion-output.patch`, blob `4a8bae8270bcb6c1f5dc4f474104d960e43a8244`, 2079 bytes |
| Change | +18/-6 across four complete hunks, 48 diff rows |

The [complete original script](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/scripts/check_gas_regression.py) was acquired at this immutable pin and independently identified. The bounded file-history read returned [edbee1c528617bf2708a9b3b1356695ab8478590](https://github.com/Stellar-Analysis/frontend/commit/edbee1c528617bf2708a9b3b1356695ab8478590), authored by Stephanie Nwankwo / GoSTEAN, with a message introducing gas benchmarks, the CI comparison and its documentation. That attribution is preserved. A dated modification notice identifies this continuation.

Apply all four hunks only to the exact preimage above and preserve its file mode. The patch records full before/after blob identities. If composing with another source change, account for that distinct preimage instead of presenting this packet as already applied there. The in-memory forward application produced the complete intended postimage, and inverse application reconstructed the complete preimage; neither operation ran Python or a benchmark.

## Concrete failure and corrected behavior

The original regular expression consumes one token for each outer timing estimate. Criterion's ordinary timing interval instead contains three value/unit pairs. After consuming the first number, the original pattern encounters its unit where it expects the middle number. Even the original script's own comment shows a shape that this pattern cannot consume. An empty parsed result then prints a warning and exits successfully, before any baseline comparison.

The [Criterion command-line documentation](https://bheisler.github.io/criterion.rs/book/user_guide/command_line_output.html) describes the left and right values as interval bounds and the center as its per-iteration estimate. The corrected pattern consumes all three pairs and captures the middle number with its own unit. It therefore does not treat an interval bound as the central estimate. This is a timing estimate; the inherited baseline table's “Median time” label is not a new statistical claim made by this packet.

The name can be on the same line as the interval, or on the immediately preceding standalone line. A [retrieved Criterion reporter-source excerpt in Android's vendored source](https://android.googlesource.com/toolchain/rustc/%2B/87880447cc5437c45a3562596a9766d9797e7318/vendor/criterion/src/report.rs) shows the separate-name form used for long identifiers. The parser retains only an immediately preceding single-token line, clears it on other lines, and consumes/clears it on every timing match, including matches with an inline name. A nameless interval without a retained adjacent name does not become a result. This deliberately supports immediate adjacency, not an arbitrary search backward through log output.

If no measurements are parsed, the program now writes an error to stderr and exits with status 2. This happens before either baseline update or comparison. An empty or wholly unsupported input can no longer claim a successful check or baseline update. Status 1 remains the existing regression-detected outcome. When measurements exist but there is no baseline, the existing first-run behavior remains unchanged.

## Actual caller and integration limits

The complete [gas-regression workflow](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/.github/workflows/gas-regression.yml), blob `78a4fa31b740e6f30783681c05f76df739d40808` / 2294 bytes, invokes this script in both its comparison and update steps. It passes the benchmark output and `../docs/GAS_COSTS.md`; the comparison threshold is 0.20. The complete [gas-cost documentation](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/docs/GAS_COSTS.md), blob `e9575e917a65ea2c8192574d69dd257ecb8d080c` / 3175 bytes, describes the same entry point and currently has an empty authoritative baseline table. Both files were full-text and independent-blob checked as source inputs; neither is modified.

The retained native recursive tree at this donor pin returned 959 entries with `truncated:false`, and contained no `contracts` directory or `contracts/Cargo.toml`. The workflow nevertheless specifies `working-directory: ./contracts` and package `contract-benches`. Those source observations establish the intended script call, not a runnable benchmark workspace in this checkout. This patch does not construct that missing workspace, edit a workflow, establish a Criterion dependency version, or demonstrate end-to-end CI operation.

The separately attempted Criterion 0.5.1 reporter page at `https://docs.rs/crate/criterion/0.5.1/source/src/report.rs` returned an inaccessible/Internal Error result. That exact acquisition is held and was not retried or replaced. The cited book and reporter excerpt were independently returned before that failed open. No assertion relies on an unread version-specific file.

## Preserved policy and compatibility boundary

The existing supported units remain ns, microseconds written as µs, ms and s, with the same nanosecond conversion. Names remain single tokens and timing numbers remain ordinary nonnegative decimals in the supported textual shape. ANSI escapes, alternate microsecond spellings, scientific notation, picoseconds and custom measurement units are not newly supported. The parser is not a general log authenticator.

Baseline parsing, output formatting, marker-based baseline updates and the entire comparison/threshold block remain byte-exact. Missing individual benchmark coverage, an empty baseline with otherwise valid measurements, threshold validation, duplicate-name overwrite behavior and baseline precision remain separate concerns. Parsing at least one record does not establish that every intended benchmark ran or that a complete set was supplied. No measurements, timings, costs or performance improvements were generated or inferred.

The current precise public Slack query for the script's filename returned zero results and native END. This is only that bounded query's observation, not an ownership or global-census claim. Existing contributor rights and any independent carrier remain unaffected.

## Notices and repository instructions

The following three original notices are carried verbatim, including their original line endings:

- [upstream-licence-mclaughlin.md](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/docs/LICENCE.md): blob `57740b9d4d86aedf5d518f2f363d5cf192c54127`, 1104 bytes.
- [upstream-license-menke-laguna.md](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/docs/LICENSE.md): blob `af5411fa243cfcf2b61c79d081dbb6204e956041`, 1111 bytes.
- [upstream-license-de-wet.md](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/docs/license.md): blob `4a766e268772888af5df56c3f6c608f68558b789`, 1080 bytes.

Their different authorship is preserved. Their presence in documentation is not treated as a repository-wide license declaration for every source file. The packet is a minimal attributed patch and guide, with no broad license inference.

The retained complete tree contained no AGENTS.md or RULES.md path. The already-read root CONTRIBUTING.md, blob `f66db3b0eece27eb6fa888948c31ee8c7eabcfd2`, is explicitly titled “Contributing to EventSource” and describes that package's release workflow. No package release, npm action or test execution was undertaken in this session.

## Verification and delivery boundary

The source patch was structurally reviewed against the complete pinned script, actual workflow, documentation and returned primary format evidence. All four hunks and all 48 rows were retained without truncation. Exact forward/reverse materialization and independent Git blob identities cover the authored source transformation. A separate nongating design review found no concern with the described immediate-adjacency contract; it did not execute or validate the regex.

This packet contains no tests, fixtures, synthetic benchmark output or generated measurement data. No shell, Python interpreter, cargo command, workflow, benchmark, wallet, RPC, deployment or upstream mutation ran. Publication readbacks and exact final metadata are recorded separately after the real Commons write. Successful source storage is not runtime validation, upstream acceptance or a bounty claim.
