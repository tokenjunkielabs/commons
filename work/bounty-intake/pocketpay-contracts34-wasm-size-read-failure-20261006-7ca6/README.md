# Preserve WASM byte-count failures before formatting

This is a source-only continuation of the existing PocketPay Contracts release-size reporter. It changes the reporter's byte-count acquisition so a failed `wc` or input redirection cannot be hidden by the following whitespace formatter. No shell, build, WASM artifact, test, deployment, contract invocation, wallet, RPC or account operation was run.

## Source and attribution

The canonical source observed on 2026-10-06 is `Stellar-PocketPay/pocketpay-contracts`, current `main` commit `7988c6efec9a73162ed7d2fffb3b8b6ebd5a7b67`. Its separately observed tree is `18d5b8aa6a05d41303ad7ed459b27015fa1048af`; the complete recursive response returned 2,031 entries with `truncated:false`. This is provider metadata, not an independently reconstructed whole repository tree.

| Source | Git blob | UTF-8 bytes |
|---|---|---:|
| `scripts/report-wasm-size.sh` | `0c7797f71e74e2205093b042f6c97d92c337f334` | 738 |
| `Makefile` | `fef14d079a27c1c2c34d2037e6bba6635b6a4bcf` | 557 |
| Root `README.md` | `f6a4921cc8d63c0da4ae3b73292df7e6a76cdb4c` | 12,438 |
| `CONTRIBUTING.md` | `f540677ba668a8579563d8ed894cf6d35253477a` | 7,744 |
| `LICENSE` | `0eaf357ba6c68fab6ed3cf20e0ab6a31f2854769` | 1,066 |

The original reporting contribution is [Dayz-tech-co's PR #41](https://github.com/Stellar-PocketPay/pocketpay-contracts/pull/41), “ci: report release WASM artifact size,” which names issue #34. Current PR metadata confirms it merged at `c9b54d7353066f12ab2d9179db3d2b8a2468c9cf` from head `db5167a8aa04b3c18f8bff9368e177042d030864`. Its historical validation statements remain the original author's report; this continuation neither reruns nor adopts those results as validation of the new hunk.

The MIT notice, copyright 2026 Axionvera, is preserved verbatim in `LICENSE`. No new per-file license header was added. Upstream contributor requirements were read completely. They include focused changes, verification and review requirements; all runtime, test, build, CI, upstream acceptance and payment-evaluation requirements remain unperformed here. No AGENTS file appeared in the complete observed tree.

## Connected caller and defect

The current Makefile calls this script in both `build-release` and `wasm-size`, explicitly passing `target/wasm32-unknown-unknown/release/savings_vault.wasm`. The root README documents those commands as the contract-size reporting interface and presents both human-readable size and exact bytes.

The original acquisition is:

```sh
bytes=$(wc -c < "$wasm_path" | tr -d '[:space:]')
```

In a POSIX shell with the usual last-command pipeline status, `tr` can return success even when the preceding file redirection or `wc` fails. The initial `-f` check proves neither readability nor a later successful read. The command substitution can therefore supply an empty or partial value while the script continues into `awk` and the report. This is a static source finding, not a reproduced incident or a claim about any previously reported WASM artifact.

The change captures the measurement in a standalone assignment used as the explicit `if` condition:

```sh
if ! bytes=$(wc -c < "$wasm_path"); then
  echo "error: could not read WASM file size: $wasm_path" >&2
  exit 1
fi
bytes=$(printf '%s' "$bytes" | tr -d '[:space:]')
```

The assignment's status now comes from the one `wc` substitution. Failure prints a path-qualified error and exits before the human-size calculation or either normal report line. On success, the same whitespace normalization is applied to the captured count; the existing formatter and successful output stay byte-for-byte unchanged. No shell-specific `pipefail` dependency is introduced.

Primary POSIX Shell Command Language search excerpts retrieved during this review state that a simple command containing only an assignment with command substitution has the substitution's exit status, and that a normal pipeline takes the last command's status. The subsequent direct opening of the [2018 Shell Command Language page](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html) returned HTTP 403. That exact retrieval remains held; no alternate acquisition or claim of a full documentation read was made.

## Delivered change

- `report-wasm-size.sh`: complete postimage, Git blob `4deff24eac07f716f1b12bb1226a2bd269a0ecb0`, 853 UTF-8 bytes. Original executable mode `100755` is retained.
- `change.patch`: one hunk against the exact upstream path, five added lines and one removed line.
- `LICENSE`: unchanged upstream MIT notice.
- This note: source provenance, caller connection, rationale and limits.

The patch is intended for the pinned source above. The copied postimage lives only in this attributed Commons packet; upstream source has not been changed. Apply it only after reconciling any later source edits.

## Scope and static qualification

The bounded repository intake returned 40 issue headers across two pages, with 107 total reported issues and `incomplete_results:false`; offset pagination is not a snapshot. The open PR page returned seven rows. Known other-seat carriers #439/#575 and #524/#574 were excluded. The broad external #411/#451 contract-error carrier was not adopted. A repository-local all-state PR search for “wasm” and “size” returned five rows, including merged #41, without establishing a global ownership absence.

The production contract already supplies the core token-backed deposit behavior named by #276 and the basic amount, maturity and replay guards discussed in #453. This packet does not add a withdrawal policy, change accounting or authorization, alter contract errors, or claim either issue's acceptance.

The static review checks the exact current call chain and the changed shell control flow. Complete source text and provider/independent blob identities are retained. No shell syntax checker, test suite, fixture, read-error injection, benchmark, native artifact measurement, old validation replay or executor was used. Runtime shell/platform behavior and upstream acceptance are therefore unverified.

The existing missing-file guard, default/explicit artifact path, whitespace normalization, size units, `awk` calculation, successful report text and Makefile remain unchanged. The helper still reports the file it reads: it does not validate WASM format, bind an artifact to a build, guarantee a stable file during reading, establish source/build identity, bound file size, or provide a size-policy gate. These remain outside this read-failure correction.
