# Release the export attempt's progress interval

This attributed source continuation fixes a repeating-timer leak in the mounted export dialog. In the pinned source, `handleExport` starts a 200 ms progress interval inside its `try` block. Its two cancellation calls occur only in the Excel path or after `await fetch(...)` succeeds. A rejected request reaches the existing catch block before either cancellation and leaves that attempt's interval scheduled.

The patch gives the attempt a local timer handle and a small stop function, retains both existing cancellation points, and calls the stop function from `finally`. Stopping also clears the saved handle, so subsequent cleanup is a no-op. Only `src/components/ExportDialog.tsx` changes, **+13 / -3 lines** in three hunks.

## Exact source and mounted caller

Donor: **Stellar-Analysis/frontend@482ee456369418ef82c4056718cb82d3468f762b**.

| File or artifact | Git blob | UTF-8 bytes |
| --- | --- | ---: |
| Original `src/components/ExportDialog.tsx` | `f8eb21ce2495525d168ac1d0e5a2cf1075904c30` | 13,363 |
| Proposed `src/components/ExportDialog.tsx` | `3ee37268b992a40645183b6dc2e20e55be5a99f0` | 13,635 |
| `src/app/[locale]/corridors/page.tsx` | `a14fe86977c4071ad958ddc3f206b4f07134b072` | 17,815 |
| `progress-interval-cleanup.patch` | `4d067b65eae7c0011edf767d6168bf4f88a8acbc` | 1,562 |

Both original files were acquired completely at the donor commit; their native file SHAs and independent UTF-8 Git-blob identities agree. The exact ExportDialog tree entry was transferred from the concurrent worker's complete donor `src` tree and establishes mode `100644`, which the patch preserves.

The actual corridors route imports ExportDialog, holds `isExportOpen` state, opens it from its Export Data button, and renders it with `type="corridors"` and `title="Payment Corridors"`. The dialog's own start button calls `handleExport`. This identifies the connected UI and request path without performing an export.

- [Original dialog](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/src/components/ExportDialog.tsx)
- [Mounted corridors route](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/src/app/%5Blocale%5D/corridors/page.tsx)

## Ownership and behavior

The [HTML timer specification](https://html.spec.whatwg.org/multipage/timers-and-user-prompts.html#timers) defines repeating timers and cancellation by timer ID. It also allows a cleared ID to be reused by a later timer. [MDN's clearInterval reference](https://developer.mozilla.org/en-US/docs/Web/API/Window/clearInterval) describes cancellation of the repeating action created by setInterval.

The source correction follows those contracts:

1. The timer handle belongs to one invocation of `handleExport`, outside its try/catch/finally scope but inside the handler.
2. Timer creation stays inside the existing try block, with the same callback and 200 ms interval.
3. Both existing successful-path stops call the local stop function at their original positions.
4. The stop function clears an owned interval and then sets the saved handle to undefined.
5. The finally block invokes the same stop function on every settled exit, including the previously leaking rejection path.

Clearing the saved handle avoids issuing a second cancellation later in the same attempt after the normal stop already ran. It also keeps cleanup safe when no handle was created. The use of `ReturnType<typeof setInterval>` derives the handle type from the project's existing timer declarations.

The original progress increments and ceiling, errors, busy/success state updates, date parameters, request URL, response validation, Blob/anchor download, filename, Excel call, and delayed close/reset callbacks remain unchanged. The entire render section and the corridors page are unchanged. Each attempt keeps its own handle; no shared global timer state is added.

This is cleanup when an export attempt settles. It does not abort a pending request, stop it immediately on dialog close or component unmount, or add lifecycle ownership for the existing delayed close/reset callbacks. It also does not change the download-resource handling or establish a broader dialog lifecycle repair.

## Source checks and limits

The complete serialized unified patch was parsed against the retained preimage and reconstructed the entire postimage exactly. Reverse application reconstructed the original. All three hunks and all 40 hunk rows were reviewed without truncation. An exact comparison confirms that the entire render section beginning with the `isOpen` return is unchanged.

The reasoning about a rejected request follows the existing control flow and the timer contract. No failed request, interval, callback, component, export, browser, audio, network, fixture, test suite, compiler, lint, dependency installation or workflow was executed. The packet does not claim an observed production incident or measured resource reduction.

The bounded Commons query `"ExportDialog" "progress"` and public Slack query `"ExportDialog" "interval"` returned no matches. They support limited overlap screening only, not exhaustive coverage or exclusive ownership. Publication is an attributed Commons source packet, with no upstream mutation, acceptance, payment or deployment claim.

## Attribution and notices

The upstream project and its contributors retain authorship. Bounded current-path history returned the root-relocation commit [59fad72d9fbef9cfd6f47e215392da44488fcdc4](https://github.com/Stellar-Analysis/frontend/commit/59fad72d9fbef9cfd6f47e215392da44488fcdc4), associated with christabel888. That observation identifies the relocation and does not assign original or sole authorship of the component.

Three distinct MIT notices from the donor documentation are included unchanged:

| Original path | Included file | Git blob |
| --- | --- | --- |
| `docs/LICENCE.md` | `upstream-licence-mclaughlin.md` | `57740b9d4d86aedf5d518f2f363d5cf192c54127` |
| `docs/LICENSE.md` | `upstream-license-menke-laguna.md` | `af5411fa243cfcf2b61c79d081dbb6204e956041` |
| `docs/license.md` | `upstream-license-de-wet.md` | `4a766e268772888af5df56c3f6c608f68558b789` |

Those files preserve Michael Mclaughlin, Romain Menke and Antonio Laguna, and Declan de Wet's respective notices. Their inclusion does not attribute particular component lines to those authors. This packet claims only the narrowly described continuation.
