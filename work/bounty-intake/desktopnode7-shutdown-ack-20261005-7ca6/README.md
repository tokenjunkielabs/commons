# Desktop-node shutdown acknowledgement

[Issue 7](https://github.com/kryptokrona/desktop-node/issues/7) asks to shut down the node correctly and keep a spinner until confirmation. The pinned main process sends SIGINT and immediately changes its running flag, while the renderer immediately navigates away. Restart uses a fixed fifteen-second timer. None of those steps establishes that the spawned child has closed.

This packet changes that source path to wait for the tracked child lifecycle, exposes completion through IPC, and leaves Stop/Restart visibly pending until that completion or an error. It composes the already delivered [sync ETA source packet, Commons 31603](https://github.com/woahwhattheheck/commons/pull/31603).

## Exact input and composition

Upstream main is `b9e38b0592c4a99db33f16c07741641c63f6d730`, tree `8910dc11b3b9927af694fe2181bcff7388b64ddf`. The complete main-process and preload sources were transferred from the retained source qualification and independently matched to their native Git blob identities.

The store and dashboard inputs are the complete accepted postimages from Commons 31603, head `1b1ebfaf4458ee2f273f282ebf2e270743b667d9`, merge `5cb578708d3f7f061ce4f20cbdb128ce5b2edccf`. They were consumed from retained bytes, without rereading or replaying the accepted estimator.

| Production path | Exact input blob | Prepared result blob |
| --- | --- | --- |
| `src/electron.cjs` | `e29d2c99c6a7126aeb4c7c7d77a26ef44b4e4b39` | `748568cce1b9228d04a057eb303adb06b3cc4f65` |
| `src/preload.cjs` | `f703bdb03d435fc5e1ec6f3592229dca15ca49e7` | `7c31d346778439178b5bb8707e0f7446587324ec` |
| `src/lib/store.js` | `8e6bac57153ab06da0dfab88b2861cccd4e57acf` | `7dbad990352cd70d897c7c80174043407807fa26` |
| `src/routes/dashboard.svelte` | `90f15bbb8944547aa2666521d490f8a9df7698e5` | `a0abac676a5f57969955f0a2282fae5c889477ba` |

The four complete postimages are included under their production paths. Apply `change.patch` to this composed input, not directly to an upstream store/dashboard that lack 31603. The patch has eight hunks and +137/-45 production lines; its Git blob is `4bcbd8e4ad0c4a8f0784e65e8a836a4ab6283b46`, 7,977 bytes. Independently reading its serialized hunk headers, context and removal rows reconstructed all four complete postimages exactly. The accepted `recordSyncSample` function is byte-identical.

## Child lifecycle and command ordering

The executable is now spawned directly with the same four existing arguments and detached option. Removing `shell: true` makes the tracked child the executable rather than a shell wrapper. The executable name and detached process-group SIGINT model are inherited; this packet does not introduce a Windows process-tree implementation.

A record owns that child, its spawn promise, close promise and shared stop promise. Listeners and record ownership are installed synchronously before any awaited step. Start completion means the child emitted spawn, not that RPC, synchronization or the application is ready. An error listener handles spawn rejection. A child that exits immediately after spawning is not automatically restarted.

Stop reuses the current record's stop promise. If stop or quit arrives while spawn is pending, it waits for that same spawn outcome before signalling the process group; a failed spawn waits for the same child's close. After successful spawn, SIGINT is requested once for the coalesced stop. A non-ESRCH signalling error rejects the command and permits a later attempt; it does not mark the child as stopped. ESRCH by itself is not acknowledgement: the path still waits for the tracked close event.

Only close marks the record closed. Its callback clears the current-child slot only when it still points to that exact record. A command with no current record has no tracked child left to wait for. No search for untracked or externally started nodes is performed.

A command generation resolves competing start, stop and restart intentions. A later command or quit supersedes an older pending command. Restart checks its generation after awaited close and immediately before spawning a replacement, then checks again after spawn acknowledgement. A superseded command rejects rather than reporting its older intent as the current result. The renderer prevents overlapping local Stop/Restart clicks, while this main-process coordination also covers another renderer or tray quit.

The tray uses the application's quit path. A before-quit listener prevents quitting while the shared stop is pending, invalidates pending restart intent and permits the actual quit only after acknowledgement. A signalling failure logs the error and leaves the application open. This is not a promise about forced operating-system termination or every platform shutdown mechanism.

## Renderer and store

Preload returns `ipcRenderer.invoke` promises for Stop and Restart, paired with `ipcMain.handle`. Start retains its original fire-and-forget renderer interface, with failures handled in the main process.

The dashboard awaits the chosen promise, shows the existing Moon spinner plus stopping/restarting text, disables both controls, and displays a rejected command's message. It no longer resets state or navigates before IPC completion. Successful Stop clears node state, sets the existing appState running flag false and navigates home. Successful Restart clears the old observations after the replacement has spawned, allowing the existing loading view and polls to observe the new process.

The accepted dashboard already imported `resetStore` while the complete store exported no such function. This packet supplies that actual missing export for these callers. It clones the declared initial node state, clears the ETA sample/value, and advances the settled request sequence beyond all already-issued info requests. A pending old info response therefore cannot restore pre-reset node data. The existing five-second poll, supply request, appState shape and ETA calculation remain as recorded; supply errors, unmount lifecycle and unrelated startup/navigation behavior are not expanded.

The existing one-million network-height loading threshold and current CSS remain. Spinner/error controls are in the existing dashboard action area; no claim is made about a redesigned startup screen or accessibility acceptance.

## Exact meaning and limits of confirmation

The acknowledgement is the close lifecycle of the tracked direct child and its streams. It is not evidence that every descendant has terminated, that the node flushed durable data, that the chain is healthy, or that a replacement is ready. The process may spawn independent descendants; this packet does not track them. SIGINT is a shutdown request, not a verified persistence protocol.

There is no timeout or forced-kill fallback. If the tracked child or its inherited streams never close, Stop/Restart remains pending and normal quit continues to wait. This preserves the distinction between an actual acknowledgement and a timer expiry. Platform signal behavior, executable packaging, open streams, Electron IPC integration and native shutdown still require their real application acceptance.

The package declares Electron 19, Svelte 3.49 and SvelteKit next.372. No production function was invoked, and no Electron, Svelte compiler, Node child, localhost request, chain, browser, test, lint, build, workflow, wallet or account operation was run. Validation here is complete-source reasoning, byte identities and serialized patch reconstruction only; this is not a runtime or whole-issue completion claim.

Three exact documentation opens returned ServerError and remain held without retry or alternate: `https://nodejs.org/api/child_process.html`, `https://www.electronjs.org/docs/latest/api/ipc-main`, and `https://www.electronjs.org/docs/latest/api/ipc-renderer`. No successfully retrieved primary documentation is claimed for those routes. The earlier 31603 performance.now documentation failure remains held as well.

## Attribution, license and intake

Original application contributors, including Swepool, retain credit. Changed production sections carry the 2026-10-05 date. The previously read complete upstream README `29e88d1fc3861279515397e75d52cdbd40a09e8a` declares GPL-3.0; package blob `1706b6f052e95fae2ce1cdd633524e3c9fe93695` is unchanged. No separate root LICENSE or AGENTS/contribution instructions appeared in the observed root/src/routes/lib ancestor listings; that observation is not a repository-wide policy census.

The complete GNU GPL version 3 text is reused unchanged from the accepted 31603 packet: `e142a525bd3fcc4eb1964d6b6b9a0434eee11d89`, 34,470 bytes. Its earlier Commons asset filename does not expand upstream's license declaration to an or-later grant.

Issue 7 was OPEN/unassigned with an empty body and one complete observed comment. Member Swepool's comment `1222125595`, dated 2022-08-22, offers 20,000 XKR. That is a historical member offer, not verified current funding, a USD15+ lead, bounty eligibility, acceptance or payment. No upstream contribution, external claim, sponsor contact, duplicate platform submission or account action was made. This Commons source packet is the delivery surface.
