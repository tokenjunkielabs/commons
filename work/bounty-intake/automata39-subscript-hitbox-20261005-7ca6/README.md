# Automata PR60 aggregate-label hit rectangle

This is a narrow continuation of [cobalt-arc-dev’s open PR60](https://github.com/dionyziz/Automata/pull/60), addressing the geometry used to click an already-rendered subscript portion of a transition label. PR60 supplies the double-click editing feature requested in [issue39](https://github.com/dionyziz/Automata/issues/39); that contribution remains credited to its original author.

## Exact source

| Item | Identity |
|---|---|
| Existing contribution | `cobalt-arc-dev/Automata`, branch `edit-transition-labels` |
| Pinned PR60 head | `8d9ed88a444db05d3c4e13214386f15fdf443ab0` |
| Observed upstream base | `3abdc507a0193af7e997b9b9cb3953f1564d58c5` |
| Original complete `site/js/render.js` | `f4ae80c369f09080f980e34231ab4ac0df60bf2c`, 27,185 bytes |
| Complete postimage | `d3899f713d15c18e9ef1c103bb31547c31c71215`, 28,658 bytes |
| Serialized patch | `5502d1ee340c6823cf8372f260e6ca8db19d5547` |
| Original README with full MIT grant | `f560dab24092a604dc1ff7d98b629f300ff28d96` |

PR60’s complete one-file patch and full renderer were read. Its current metadata reported open/unmerged, zero issue/review comments, and one changed file. The recursive pinned tree reported `truncated: false`; no AGENTS, CONTRIBUTING, separate license file or package manifest was observed. The README contains the complete MIT grant, copied verbatim from its copyright line into this packet’s LICENSE. Its contributor guidance invites pull requests, without an additional prerequisite. No upstream contribution is submitted by this packet.

## Reachable discrepancy

The existing model permits single-character transition symbols, including underscore, and rejects ordinary symbols longer than one character. The existing input handler splits entered symbols on commas. This continuation does not assume that a multi-character symbol such as a subscript expression can be entered.

Instead, PR60’s `transitionText` combines all symbols connecting a state pair using comma-space separators. The existing `renderText` treats the first underscore anywhere in that aggregate string as a subscript boundary, discards underscores, and draws the remaining suffix at 8pt to the right of the centered 12pt main string. An underscore symbol followed in that aggregate by other parallel symbols therefore reaches the subscript renderer. Those formatting rules are preserved, even where they produce an unusual display.

PR60’s new `hitTestText` measures the entire raw string at 12pt and centers its hit rectangle at the label position. This rectangle does not follow the drawn suffix’s origin and font, so a sufficiently extended visible suffix can fall outside the clickable region.

The postimage adds a branch for a nonempty rendered subscript. It mirrors the renderer’s character split, measures the main part at 12pt and suffix at 8pt, and uses their actual horizontal draw origins. Its vertical interval combines the existing approximate main-height model with the suffix’s shifted baseline and 8pt height estimate. The existing six-pixel padding remains. Canvas state is restored in `finally`, including a return or measurement failure from that new branch.

The ordinary/empty-subscript path is byte-for-byte unchanged. This deliberately includes the old behavior for a trailing underscore with no subsequent character. No rendering, transition-position calculation, alphabet validation, event dispatch, editor input, state hit testing or arrowhead behavior changes. The vertical rectangle remains approximate; this is not an exact glyph-metrics, canvas-transform or general text-layout implementation.

## Source binding and attribution

The parallel Automata37 lane supplied retained actual excerpts from PR62’s editor and model, whose respective unchanged paths match the shared base. Its editor source is `6de6c5a3e8bdbd7ab74a3803aeef3ff548856038` on PR62 head `8e5f68b41b494634bb79fc1ba568a49cb31d2e82`; the model blob is `65e1ac0759acd290c3c7437a5d91d36e91d677fa`, also observed in our complete PR60 tree. The model’s `addTransition` rejects `via.length > 1` except the internal `$$` symbol. The editor’s double-click handler uses the renderer’s transition target to open its existing label input. These excerpts bind reachability; no new full-model or editor audit is asserted here.

The existing author’s straight, arced, detached and self-transition position work stays untouched. The separate copy/paste qualification of PR62 found no additional supported source hunk and made no edit. No editor.js change is included in this renderer packet.

## Validation and boundaries

Static comparison verified the complete original/postimage Git blob identities, the one-hunk serialized patch (+40/-0), and exact postimage reconstruction from that patch. All bytes outside `hitTestText` are unchanged. No production function, browser, canvas, font engine, Node process, synthetic example, test, build or workflow was executed. PR60’s author-reported historical checks are not new validation by this continuation.

Both issue comments were read. The owner’s November 2014 comment offers $5; the May 2026 comment links PR60. This historical amount is not a USD15+ lead, current escrow, acceptance, award or payout evidence. No sponsor contact, external claim, upstream mutation or broad issue-completion claim is made.

Internal activity `1791201117.605449` records this source scope. Its initial complete readback matched after removal of the observed provider-added ChatGPT attribution footer. Source publication and final release are recorded separately.
