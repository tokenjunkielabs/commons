# Stellar issue-recreation wrapper: check the named prerequisite first

The existing `scripts/close_and_recreate_all.sh` closes open issues with Backend, SDK, or Mobile title prefixes before checking any replacement source. It then prints a command for `scripts/create_all_70_detailed.py`; it does not execute that command. The complete retained repository tree does not contain that named script.

This patch places a source prerequisite check before the first GitHub CLI call and resolves paths from the wrapper's own directory. If the named replacement is missing, unreadable, or not a regular file, the wrapper prints an error to standard error and exits before listing or closing issues. If directory resolution or checkout entry fails, it also exits before those calls.

## Exact source and attribution

Project: [Stellar-Analysis/frontend](https://github.com/Stellar-Analysis/frontend). Original project and contributor credit remains with the upstream authors. This is an attributed Commons source continuation, not an upstream submission or an authorization to execute the wrapper.

| Source item | Identity |
|---|---|
| Observed donor ref | `482ee456369418ef82c4056718cb82d3468f762b` |
| Path | `scripts/close_and_recreate_all.sh` |
| Existing mode | `100755` |
| Preimage blob | `2b6d5f31f40dcd536101155fa0fc8ff5fb95a762` |
| Preimage UTF-8 bytes | 940 |
| Postimage blob | `ad33b2f7c127a35baa8605e02e717d9c2469dabc` |
| Postimage UTF-8 bytes | 1,446 |

The entire wrapper was acquired once at the exact donor ref. Native and independent Git-blob identities agree. The patch adds twelve lines after the shebang and blank line. Every existing byte after that insertion remains unchanged; the executable mode is retained.

Root's already-retained recursive tree response has 959 entries and `truncated: false`. It contains neither `scripts/create_all_70_detailed.py` nor another path with that basename. This is transferred native tree evidence: the recursive response's SHA echoes the requested commit, while separate branch metadata names tree `44703ba39198f99b6541450c740db0d1c3c0f7b8`. No independent reconstruction of the complete tree identity is asserted. The missing file was not fetched, recovered, or invented.

A bounded all-state PR search within the upstream repository for the literal filename `close_and_recreate_all.sh` returned zero rows, `incomplete_results: false`. It established no current named carrier in that query; it does not prove global ownership absence. Other backend carriers and their source/acceptance restrictions remain outside this patch.

The preceding generator work preserved three differently attributed MIT notices verbatim under [`work/bounty-intake/stellaranalysis-issue-generator-layout-20261006-7ca6/`](https://github.com/woahwhattheheck/commons/tree/main/work/bounty-intake/stellaranalysis-issue-generator-layout-20261006-7ca6):

| Preserved notice | Exact blob |
|---|---|
| `upstream-licence-mclaughlin.md` | `57740b9d4d86aedf5d518f2f363d5cf192c54127` |
| `upstream-license-menke-laguna.md` | `af5411fa243cfcf2b61c79d081dbb6204e956041` |
| `upstream-license-de-wet.md` | `4a766e268772888af5df56c3f6c608f68558b789` |

These are retained attribution references; no one notice is assigned repository-wide scope or newly asserted to govern this shell file. This packet contains only the narrow patch and this guide, not a republished full module or new license declaration. The later backend handoff in the prior guide is an attributed report, not verified source or permission.

## Why the generator guard does not cover this wrapper

The wrapper never calls `generate_all_issues.py`. It starts with:

1. `gh issue list`, limited to 100 open issues;
2. title-prefix selection through `jq`;
3. independent `gh issue close` calls;
4. a printed suggestion to run a different Python filename.

Commons [31810](https://github.com/woahwhattheheck/commons/pull/31810) changes `generate_all_issues.py` to require the supported source layout before issue creation and anchor its working directory. That source guard is a separate correction. Its generator postimage is `586da41237ab75499f2aba00a2d47b949b62578f`, and the observed upstream generator remains `ffbebec9beed84de953b85cdbaf59fdcd15c51f2`. Neither the Commons patch's deployment nor a control-flow dependency from this wrapper is assumed.

This wrapper patch does not import the generator, require the new generator patch to be installed, substitute a different recreation command, or recreate the absent script. It checks the exact replacement path already printed by the original wrapper.

## Resulting source contract

The preflight derives an absolute script directory with the existing Bash entrypoint, with `CDPATH` cleared for directory resolution. It checks the exact sibling `create_all_70_detailed.py` using Bash's regular-file and readability predicates. Only after those checks does it change to the containing checkout and enter the unchanged original body.

For a checkout consisting of the pinned tracked tree, with no additional replacement file supplied locally, the absent-file branch prevents reaching any `gh` call. This is static control-flow reasoning, not an executed closure test.

Anchoring the working directory makes the printed relative recreation path and the wrapper's ordinary GitHub CLI repository inference refer to its own checkout, rather than the caller's unrelated working directory. It does not override explicit GitHub CLI environment configuration such as `GH_REPO`, validate the configured remote, or grant authority for another repository.

The file check is only a prerequisite check. It does not validate the replacement script's syntax, issue payloads, backend/mobile source layout, credentials, repository selection, behavior, or eventual success. No success is claimed merely because a file exists and is readable.

## Unchanged limitations

The existing wrapper still:

- reads at most 100 open issues and filters title prefixes;
- uses its existing GitHub CLI configuration and issue-selection behavior;
- attempts closures one at a time, without atomicity or rollback;
- suppresses each close command's standard error and does not inspect each exit status;
- can print its existing success message after an individual closure failure;
- prints a later manual recreation command rather than running it.

Those are existing limitations, not guarantees improved by this small ordering repair. In particular, this patch does not promise that closing issues and recreating them forms a safe transaction. It provides no consent, approval, admission, or external-action mechanism.

## Validation and operating boundary

Performed: one complete exact-ref source acquisition, independent native/content identity comparison, retained tree and source-ownership qualification, static review of the preflight order and quoting, and byte-preserving patch composition. Publication checks establish the integrity of these two artifacts.

No shell, Bash parser, script, Python generator, CLI command, GitHub issue listing through the script, issue closure, issue creation, credentials, tests, synthetic fixtures, runtime probe, or upstream submission was executed. Existing issue payloads, external backend carriers, source holds, and author/acceptance conditions remain untouched.

The source change is reviewable in `change.patch`. Any future operation of the wrapper remains separate from this source-only Commons delivery; neither a Commons merge nor the existence of this preflight authorizes it.
