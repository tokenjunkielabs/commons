# iView #2273: put newly opened Drawers into shared overlay order

This packet repairs the current Drawer-specific behavior reported in [issue #2273, comment 440609595](https://github.com/iview/iview/issues/2273#issuecomment-440609595): a Drawer opened after a Modal can remain behind it. The current Modal uses the shared transfer counter. Drawer declares a `zIndex` prop but does not use it in its rendered mask or wrapper and does not participate in that counter.

The change is limited to the complete production `src/components/drawer/drawer.vue` and its existing `types/drawer.d.ts` declaration. It does not replace the shared overlay manager or claim to resolve every historical Modal, tooltip, custom-theme or close-order report.

## Exact source

Upstream default branch `2.0` is pinned to [c3f57f17716c2a631b2b0eb95c9c3ab8208b3be8](https://github.com/iview/iview/tree/c3f57f17716c2a631b2b0eb95c9c3ab8208b3be8), tree `ea1ea4e1e60af534583e74ef3948e28e786887db`. The package identifies iView 3.5.4 with Vue 2, despite that branch name.

| Upstream path | Preimage Git blob | Complete packet postimage |
| --- | --- | --- |
| `src/components/drawer/drawer.vue` | `341fe8a0d4b49bc108f43091472503bc45a02b6e` | `drawer.vue`, blob `0a1a5cc41b7d857f33422a29b40e8cd8c503a29a`, 12,282 bytes |
| `types/drawer.d.ts` | `83d1c40d5bfa54b7db6227d1dc2334e1a75de0d4` | `drawer.d.ts`, blob `b01e8bfd84ff214ce366e97677fe546a942150e4`, 2,709 bytes |

`drawer-order.patch` contains nine hunks, 30 added and four removed lines across those two paths. `LICENSE` preserves the complete upstream license bundle, blob `59a7cc688a9fe75973f0c780e55d5fc5ea4b0a75`.

Adjacent full source was read at the same pin:

- Modal: `29bb05af8658fd6e6adf112644368682acbae817`.
- Shared `transfer-queue.js`: `b11bdf7caffb59bcb90b34e8bbc2f9e304482337`.
- Drawer LESS: `41cf3a86f6567879863830da4bd6c50ffb1b0c73`.
- DOM event utility: `dcaf19277796e1e671e739527d16faac82603cf8`.

These adjacent files are unchanged.

## Behavior and limits

An initially visible Drawer takes a shared transfer index during initialization. An initially hidden Drawer starts at zero and takes an index when its visibility becomes true. Reopening takes another index. Closing does not decrement or reset the shared counter, matching the existing Modal infrastructure.

Both wrapper and mask receive the same computed stacking value by default. With the ordinary matching base of 1000, a Drawer opened after a Modal has the later shared index and therefore the higher stacking value. A subsequent Modal opening uses the same counter. This statement concerns overlays in comparable stacking contexts with the same base; differing explicit bases, nested CSS stacking contexts and an explicit mask override can intentionally change the resulting order.

The previously unused `zIndex` prop now acts as an optional base. If omitted, the component reads its wrapper's computed stylesheet z-index at mount, before it writes any inline stacking value. A nonnumeric stylesheet value falls back to 1000. This preserves a custom LESS base already applied at mount instead of replacing it with a hard-coded inline 1000. Supplying `z-index` explicitly takes precedence over that captured base, and changing or removing the prop selects the explicit or captured base reactively. The stylesheet base is captured once; arbitrary later stylesheet/theme changes are not observed automatically. Remount or provide an explicit reactive `z-index` when changing that base.

Before mount, the wrapper retains its stylesheet stacking; the component does not access `window` while rendering on the server. The existing mounted lifecycle already performs DOM measurement. The new TypeScript declaration documents the optional kebab-case prop.

`maskStyle` is merged last into a fresh object. Existing color, opacity and other mask styling is retained, and an explicit mask z-index keeps its override authority. Width, drag, placement, close hooks, scrolling, event emission and transfer behavior remain otherwise unchanged. No distribution bundle or CSS file is regenerated.

## Original contributions and qualification

All 32 current issue comments were read. The original issue concerns iView 2.5.1; later discussion distinguishes initial Modal changes from outstanding shared ordering and custom-theme concerns. The last comment specifically describes the Drawer-after-Modal case addressed here. The earlier [PR #4501](https://github.com/iview/iview/pull/4501), by the issue's original contributor, is CLOSED and unmerged at `fac74b9df6954ed37145406fbba70665a0af95fc`; its historical broader changes are not represented as this patch.

At qualification time, the issue was OPEN and unassigned. The all-state upstream `author:woahwhattheheck` PR query and the bounded `drawer zIndex` PR query each returned zero rows. Exact public Slack `iview` plus `2273` found only BATCH06 row 17. These are the observed query results, not universal absence claims.

[Funding comment 436120625](https://github.com/iview/iview/issues/2273#issuecomment-436120625), dated November 6, 2018, records $30 from 0maxxam0 through IssueHunt. This is historical advertised funding, not current escrow, eligibility, acceptance, award or payment confirmation.

## Validation and integration

Complete source bodies were retained before parsing. Their calculated Git identities matched the pinned provider identities. The final production postimages were banked as Git blobs before the packet was assembled. A separate parser applied the serialized patch to each entire preimage and reproduced both postimages exactly, including the Vue file's absent final newline and the declaration file's final newline.

The JavaScript portion of the Vue component parsed in V8 after removing its seven import declarations and replacing the export with an uninvoked function return. The function was never invoked. This is a syntax-only observation: it does not compile the Vue template, resolve modules, type-check TypeScript, render an overlay, or establish browser behavior. No dependency installation, application run, build or test suite occurred.

For integration, apply `drawer-order.patch` to the two named upstream paths after confirming the exact base, or use the two complete postimages. On a moved base, retain legitimate current changes and compare these explicit hunks before applying. The upstream PR template asks for the `2.0` branch, no `dist` files, and `npm install` plus `npm test` before external submission. Those commands were not performed; this Commons source delivery does not claim compliance with that external submission prerequisite.

The upstream repository was public/unarchived, readable with push permission false; metadata allowed PR creation. No upstream/fork/platform write or contact was attempted. Browser validation and any authorized upstream delivery remain the existing carrier's follow-through.

Internal [BATCH06 row 17](https://tokenjunkielabs.slack.com/archives/C0BU51F1PL3/p1791174389955459); operation `IVIEW2273-DRAWER-OVERLAY-ORDER-20261005-7CA6`, [source claim](https://tokenjunkielabs.slack.com/archives/C0BU51F1PL3/p1791175853636109).
