# Desktop-node: guard macOS Dock calls

The actual close control for [issue 3](https://github.com/kryptokrona/desktop-node/issues/3) sends the hide IPC message. The main-process handler currently calls `app.dock.hide()` before `mainWindow.hide()`, although Electron exposes Dock integration for macOS. The two tray visibility actions also access Dock unconditionally.

This source packet limits those three Dock calls to `process.platform === 'darwin'`. The existing window show/hide actions remain in the same order. A Windows invocation of the hide handler can therefore reach the existing window action without first accessing the macOS-only Dock API. This is a source-path correction; no native Windows interaction result is claimed.

## Exact source composition

Fresh upstream main remained `b9e38b0592c4a99db33f16c07741641c63f6d730`, tree `8910dc11b3b9927af694fe2181bcff7388b64ddf`. The prepared main-process input is the complete accepted postimage from [Commons 31610](https://github.com/woahwhattheheck/commons/pull/31610), head `e01e172e761c2d5cd11e94d111d21ec6102e85e4`, merge `ab1fae1ca62e65112571ce36927a9d247cd32f70`.

| File or premise | Exact Git blob |
| --- | --- |
| Original upstream `src/electron.cjs` | `e29d2c99c6a7126aeb4c7c7d77a26ef44b4e4b39` |
| Composed 31610 input `src/electron.cjs` | `748568cce1b9228d04a057eb303adb06b3cc4f65` |
| This packet's complete `src/electron.cjs` | `bd434d968a15830fee3e1feaba5897e56fb074f3` |
| Actual caller `src/components/TrafficLights.svelte` | `d881bc01d1318bb136e5272753bc54903b9db747` |
| Actual layout `src/routes/__layout.svelte` | `eed15fc99de81aa13517d8e1dff074c366d41bbb` |
| Original preload | `f703bdb03d435fc5e1ec6f3592229dca15ca49e7` |
| Unchanged accepted 31610 preload | `7c31d346778439178b5bb8707e0f7446587324ec` |

The complete caller and layout were transferred from the existing source scout, then independently matched to their native Git blob identities. The accepted main-process input and preload came from retained bytes; no accepted source read or runtime was replayed.

`change.patch` has three hunks, +4/-3, and 906 bytes, Git blob `31a9bae49804bb49bc780786b181a6aec1f3ed3c`. Reading its serialized context, removals, additions and hunk offsets reconstructed the complete 6530-byte result exactly. The entire accepted 31610 child-lifecycle block is byte-identical. Apply the patch over the stated 31610 input, not blindly over another source revision.

## Actual caller and platform evidence

The layout mounts TrafficLights after onMount. Its close control calls `window.api.send("hide")`; the preload's generic send forwards that existing channel to the main process. The minimize control uses the separate min channel and is outside these three replacements. The relevant hide handler is present in both the original source and the composed input.

The existing scout directly read the complete official [Electron Dock documentation](https://www.electronjs.org/docs/latest/api/dock) on 2026-10-05. It describes the API as macOS Dock integration and explicitly labels both show and hide as macOS methods. This is a distinct successful primary source, not a retry or alternate for the earlier failed child_process, ipc-main or ipc-renderer pages. Those exact failed routes remain held.

On macOS, the existing Dock calls still execute after the same window action in tray callbacks, and before window hide in the IPC handler. On other platforms only those Dock calls are skipped. Window lifecycle, the existing close-versus-hide behavior, tray availability, preload API, renderer layout and child shutdown semantics are otherwise retained.

## Limits and attribution

The issue also asks about the drag area. The retained layout has a full-width, 40-pixel dragbar, and inspected renderer styles do not show an explicit no-drag rule for the controls. These are observed source facts only. This packet does not change that geometry or infer actual Windows hit testing, pointer behavior, renderer accessibility, or a complete Windows title bar. It is not completion of the whole issue.

No Electron, Svelte, browser, OS window, process, node RPC, test, build, lint, workflow, account or chain operation was executed. There was no upstream source mutation, PR, contact or platform claim. The earlier 31610 acknowledgement remains limited to the tracked child's close, not every descendant or durable flush; platform signal and packaging acceptance remain unverified.

Original application contributors, including Swepool, retain credit. The source carries a 2026-10-05 modification notice. The already read upstream README `29e88d1fc3861279515397e75d52cdbd40a09e8a` declares GPL-3.0. This packet reuses the exact complete GNU GPL version 3 text from the accepted source packet, `e142a525bd3fcc4eb1964d6b6b9a0434eee11d89`, 34,470 bytes. No or-later license expansion is inferred. The previously observed ancestor listings contained no AGENTS/contribution file; that observation is not a repository-wide policy census.

The current issue was OPEN/unassigned with the body about the drag area and traffic lights. Its sole complete observed comment, member Swepool's `1222124964` on 2022-08-22, offered 5,000 XKR. That historical offer is not verified current funding, a USD15+ amount, an award or payment. The precise all-state query `repo:kryptokrona/desktop-node is:pr windows` returned zero with incomplete_results false; that is term-limited coverage, not proof that no related contribution exists. The exact public activity search also returned zero/provider END. No named PR was supplied by the issue comment.
