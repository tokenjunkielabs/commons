# Desktop-node: Dock guards and clickable window controls

The actual close control for [issue 3](https://github.com/kryptokrona/desktop-node/issues/3) sends the hide IPC message. [Commons 31615](https://github.com/woahwhattheheck/commons/pull/31615) guarded the three macOS-only Dock calls so other platforms can reach the existing window show/hide actions. This continuation adds an explicit non-draggable region to the two existing trafficlight controls, whose source rectangles overlap the draggable title strip.

The only new production change is a dated notice and `-webkit-app-region: no-drag` in the existing `.actions div` rule. It applies to the two inner clickable controls. Their parent, intervening gap, positions, sizes, colors, handlers and surrounding dragbar remain unchanged. This is a source correction supported by the actual layout and official Electron documentation; native Windows pointer behavior has not been exercised.

## Exact source composition

The observed upstream main was `b9e38b0592c4a99db33f16c07741641c63f6d730`, tree `8910dc11b3b9927af694fe2181bcff7388b64ddf`. Complete caller and layout bytes were retained from the existing source scout and independently matched to the native Git blobs. No accepted source acquisition or runtime was replayed.

| File or premise | Exact Git blob |
| --- | --- |
| Original upstream `src/electron.cjs` | `e29d2c99c6a7126aeb4c7c7d77a26ef44b4e4b39` |
| Accepted 31610 input `src/electron.cjs` | `748568cce1b9228d04a057eb303adb06b3cc4f65` |
| Unchanged 31615 / this packet `src/electron.cjs` | `bd434d968a15830fee3e1feaba5897e56fb074f3` |
| Original `src/components/TrafficLights.svelte` | `d881bc01d1318bb136e5272753bc54903b9db747` |
| New complete `src/components/TrafficLights.svelte` | `84cf766516b0ca643ea7ed0f7395fe10523b1858` |
| Unchanged source premise `src/routes/__layout.svelte` | `eed15fc99de81aa13517d8e1dff074c366d41bbb` |
| Unchanged accepted 31610 preload | `7c31d346778439178b5bb8707e0f7446587324ec` |

The original 31615 packet merged at `13a25b99f75182438afe5a2b8c7601ea1678fef1`, head `561953e7d39dba499619712f9d299a23025e31e5`. Its complete 6530-byte electron file and the GPL text are unchanged here. The accepted 31610 child-lifecycle block remains byte-identical, and no IPC or process path changes in this continuation.

`change.patch` is cumulative within this packet: the original three Dock hunks over accepted 31610 plus one TrafficLights hunk over the stated upstream caller. It contains four hunks, +6/-3, 1316 bytes, Git blob `530685d588c855e9d470f9d6d3f236c23c225043`. Reading its actual serialized context, removals, additions and hunk offsets reconstructed both complete postimages exactly. The TrafficLights file remains without an ending newline, as in the input. The new delta after 31615 is only +2/-0 in that component. The cumulative patch replaces the previous `31a9bae49804bb49bc780786b181a6aec1f3ed3c` patch; do not apply both or blindly use a different source revision.

## Source path and primary convention

The layout mounts TrafficLights after onMount. Its full-width dragbar is 40 pixels high and declares `-webkit-app-region: drag`. The controls are fixed at top 11 pixels with a 12-pixel height in the inspected source. Their original rule had no non-draggable declaration. Those rectangles establish the source overlap; they do not establish a native hit-testing result.

The official [Electron Custom Window Interactions documentation](https://www.electronjs.org/docs/latest/tutorial/custom-window-interactions) was directly read on 2026-10-05. It explains that overlapping draggable regions suppress pointer events and that title-bar controls need a non-draggable region. The patch follows the existing application's prefixed property spelling. Current documentation is convention evidence, not a test of this application's declared Electron 19 dependency or its installed package.

The earlier scout directly read the official [Electron Dock documentation](https://www.electronjs.org/docs/latest/api/dock), which identifies show and hide as macOS methods. The preserved guards restrict only those three calls to `process.platform === 'darwin'`. Their original ordering relative to window actions is unchanged. The close control still sends hide, and minimize still sends min.

These successful primary reads are distinct from the earlier failed child_process, ipc-main, ipc-renderer and performance.now pages. Those exact failed routes remain held. No alternative to a failed route was used.

## Scope, chronology and attribution

31615 explicitly left CSS untouched. This follow-through addresses its retained no-drag source question; it does not retroactively claim a CSS result for that earlier packet. No Electron, Svelte, browser, OS window, process, node RPC, test, build, lint, workflow, account or chain operation was executed. Actual platform behavior, renderer accessibility and completion of the whole Windows UI request remain unverified. The 31610 acknowledgement remains limited to the tracked child's close, not every descendant or durable flush.

Original application contributors, including Swepool, retain credit. Modified source sections carry 2026-10-05 notices. Upstream README `29e88d1fc3861279515397e75d52cdbd40a09e8a` declares GPL-3.0. This packet retains the exact complete GNU GPL version 3 text, `e142a525bd3fcc4eb1964d6b6b9a0434eee11d89`, 34,470 bytes; no or-later expansion is inferred. The previously observed ancestor listings contained no AGENTS/contribution file; that bounded observation is not a repository-wide policy census.

The issue was OPEN/unassigned with the drag-area/trafficlights request. Its sole complete observed comment, member Swepool's `1222124964` on 2022-08-22, offered 5,000 XKR. That historical offer is not current verified funding, a USD amount, an award or payment. The earlier all-state query `repo:kryptokrona/desktop-node is:pr windows` returned zero with incomplete_results false; that is term-limited coverage. The exact public activity search returned zero/provider END. No named PR was supplied by the issue comment. This continuation uses the existing Commons packet and operation; there is no upstream mutation, submission or contact.
