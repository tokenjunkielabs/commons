# Reconciliation shutdown handling for Stellar Analysis issue 380

This packet provides a focused source continuation of the existing draft [Stellar-Analysis/frontend PR #394](https://github.com/Stellar-Analysis/frontend/pull/394), authored by s6pa1rta3n-lab. It changes the shutdown waits in the donor's exported reconciliation library. A shutdown request or loss of all shutdown senders stops the loop; false control updates preserve a pending retry delay.

The production change is **+23/-16 in one file, four hunks**, including a modification notice. The packet contains a patch, this original guide and three unchanged upstream notices. It does not contain a reconstructed backend, an executable proof, or the donor's test suite.

## Exact source and connection

| Item | Observed identity |
| --- | --- |
| Canonical issue | [Stellar-Analysis/frontend #380](https://github.com/Stellar-Analysis/frontend/issues/380) |
| Existing carrier | PR #394, OPEN and draft in the observed metadata; head owner s6pa1rta3n-lab |
| Donor repository | `s6pa1rta3n-lab/Stellar-inights` |
| Donor branch | `fix-issue-380` |
| Donor commit | `de6a5b36097acabf97f4c10f3ef64e1676cb0560` |
| Production path | `backend/src/reconciliation/compare.rs` |
| Complete preimage | `b090291ed8bcb5427fff339e1360e278640b34f4`, 20,125 UTF-8 bytes |
| Complete postimage | `bb06d4135c3f75e1532d9985b18fc90a4a45f5a0`, 20,452 UTF-8 bytes |
| Preserved mode | `100644` |
| Patch | `shutdown-control.patch`, `a92a518c3953a54bfc02791849e078d78bc3d023`, 3,893 UTF-8 bytes |

The [complete donor source](https://github.com/s6pa1rta3n-lab/Stellar-inights/blob/de6a5b36097acabf97f4c10f3ef64e1676cb0560/backend/src/reconciliation/compare.rs) was acquired and identified before editing. The donor's `backend/Cargo.toml` declares the `stellar-insights-backend` package and Tokio 1 with full features. Its complete lockfile pins **Tokio 1.53.1**. Relevant retained identities are:

| Dependency or export | Git blob |
| --- | --- |
| `backend/Cargo.toml` | `fc7178963acf9cb260579bdf127cfb092aeefb30` |
| `backend/Cargo.lock` | `d7442e897794e830656bc2be52c41c3c58a71175` |
| `backend/src/lib.rs` | `e689d1cb2389cb00bf9446a4f4447666232842c6` |
| `backend/src/reconciliation/mod.rs` | `0f677bdaa25ea212d2176f192b7babf69f076f04` |
| `backend/src/reconciliation/resubmit.rs` | `d3da1d449216563cc7b209f62805fde6aeac414f` |

The actual library root exports `reconciliation`; that module exports `compare` and re-exports `ReconciliationJob`. The existing public `run_forever` method delegates to `run_until_shutdown`. This establishes the library connection. It does not establish a deployed daemon, a process startup site, or live use of this draft.

Canonical frontend main was separately observed at `482ee456369418ef82c4056718cb82d3468f762b`; its retained complete tree lacks `backend/src`. The correction therefore targets the named donor commit. It is not presented as an applied change to canonical frontend main or to the separate backend repository.

## Why the shutdown waits need a correction

The donor's outer tick selection and its two retry-delay selections each awaited `shutdown.changed()`, discarded the returned result and only exited when the borrowed boolean was true. A closed channel whose last value is false can therefore remain immediately ready without causing an exit. A false notification during either delay also completes the original selection, abandoning that delay before its deadline. Startup did not inspect an already-current true value.

The [Tokio 1.53.1 receiver documentation](https://docs.rs/tokio/1.53.1/tokio/sync/watch/struct.Receiver.html) describes the relevant contract: `has_changed` reports channel closure; `wait_for` checks the current value, continues waiting while its predicate is false, and completes on a matching value or channel closure. It also documents the returned borrow and cancellation behavior. These are API facts used for source reasoning, not a runtime observation of this application.

## Resulting behavior

| Observed control state or event | Corrected behavior |
| --- | --- |
| True value or closed channel observed by the entry guard | Return before creating the interval or starting the first tick |
| Open channel with false value | Continue using the existing interval and reconciliation flow |
| False notification during retry delay | Keep waiting with the same paired sleep future |
| True value observed by a shutdown wait | Exit the daemon loop |
| All shutdown senders dropped | Exit when the shutdown wait completes with closure |
| A tick or alert operation already selected and awaiting I/O | Finish its existing awaited work before a later shutdown-selection opportunity |

Each of the three control arms now uses a unit-returning async block around `wait_for(|requested| *requested)`. The returned `Result<Ref<bool>, RecvError>` is consumed inside that block, so no returned watch borrow is carried into the selected handler. Both terminal results intentionally stop the loop. The entry borrow is scoped entirely before the first await.

Watch retains the latest value. This correction does not promise observation of every transient true/false notification, an atomic boundary against concurrent senders, or immediate cancellation. A signal can race a tick that has already been selected. A hung reconciliation or alert await still prevents the loop from reaching its next shutdown wait.

## Preserved behavior and limits

The complete source preceding `run_until_shutdown`, apart from the single modification notice, is byte-for-byte preserved. This includes `run_once`, period comparisons, discrepancy handling, retry-store operations, the optional resubmission phase, batch selection and backoff calculation. The separate resubmission module and every other source file are untouched. The original interval and missed-tick policy remain.

The original `run_forever` wrapper still owns its sender while awaiting this method. The change does not replace its public return type, invent persistent storage, modify transaction submission, or add a new shutdown producer.

The donor still has limitations outside this patch: its default retry store is in-memory, durable-store failures and backlog policy retain their existing behavior, and interval/backoff configuration is not newly validated. There is no claim of whole-issue acceptance, complete fault tolerance, crash recovery, service liveness, CPU measurements, or payout eligibility.

## Validation performed

The complete preimage and final postimage were identified independently as Git blobs. All four hunks and all 71 diff rows were retained without truncation. Forward application against the exact preimage reconstructed the complete postimage; inverse application reconstructed the complete preimage. The unchanged pre-shutdown implementation was compared as a complete contiguous source region.

The package, lockfile and library exports were read as actual inputs. No Rust source, application, test, fixture, synthetic scenario, shell, compiler, formatter, daemon, database, RPC, wallet, or transaction was executed. The existing draft's test claims were not used as newly executed evidence. Runtime and compiler validation remain unperformed.

## Attribution, instructions and publication scope

s6pa1rta3n-lab retains authorship of the draft reconciliation implementation. The original issue author and external implementation-interest comments are not replaced by this Commons continuation. No upstream branch, PR body, issue assignment or claim is changed.

The donor's complete recursive response contained 1,515 entries with `truncated:false`. It included no `AGENTS` or `RULES` path. `docs/CONTRIBUTING.md`, blob `f66db3b0eece27eb6fa888948c31ee8c7eabcfd2`, is headed “Contributing to EventSource” and describes that project's test and npm-release workflow. No such workflow was run.

Three differently attributed MIT notices in the donor tree are preserved verbatim from already retained bytes:

| Carried file | Donor notice path | Git blob |
| --- | --- | --- |
| `upstream-licence-mclaughlin.md` | `docs/LICENCE.md` | `57740b9d4d86aedf5d518f2f363d5cf192c54127` |
| `upstream-license-menke-laguna.md` | `docs/LICENSE.md` | `af5411fa243cfcf2b61c79d081dbb6204e956041` |
| `upstream-license-de-wet.md` | `docs/license.md` | `4a766e268772888af5df56c3f6c608f68558b789` |

Their distinct provenance is preserved; their presence is not treated as a repository-wide licensing statement for the backend. No root license was inferred.

An exact existing-carrier search in Commons was rate-limited during qualification and remains unresolved; no alternate query recovered it. The bounded Slack results likewise do not establish global absence of prior work. Publication is limited to this attributed patch with exact source and destination identities. No private messages, native operation records, financial identifiers, or unrelated blocked-source payloads are included.

The publishing receipt separately records immutable artifact readbacks, final PR and merge identities, and any observation of named main. It distinguishes direct file reads from identity-based main aliases.
