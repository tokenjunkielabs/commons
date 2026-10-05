# Preserve the terminal MiniReddit listing cursor

## Delivered change

This is a narrow source continuation of [cobalt-arc-dev's MiniReddit PR 28](https://github.com/dionyziz/minireddit/pull/28), on its complete pinned JavaScript client. It preserves an explicit terminal `after: null` response and completes later page requests through the existing end callback. The production difference is eight added lines and one removed line in `js/reddit.js`.

The packet contains the complete amended module, an exact patch against the pinned PR 28 module, this integration note, and the unchanged upstream MIT license. Apply the change on top of the full PR 28 implementation; the patch is not a substitute for that contribution's PHP proxy, retry, UI and duplicate-page changes.

## Why this changes behavior

The existing channel starts with `after = ''`. On every successful listing response, it assigns `feed.data.after || ''`. Consequently, a terminal `null` cursor becomes indistinguishable from the initial request.

When a terminal page adds posts, the existing code calls `ondone` and correctly serves those posts from its cache. Once they are consumed, `getCurrent` calls `downloadNextPage` again. The empty cursor then requests the first page. Duplicate filtering can walk previously loaded pages again, and a failure during that unnecessary traversal can produce the network-error UI after pagination had already ended.

[Reddit's API listing documentation](https://www.reddit.com/dev/api/#listings) describes response cursors as the next/previous-page anchors and says the first request starts without an after value. The [Reddit archive JSON specification](https://github.com/reddit-archive/reddit/wiki/JSON#listing), edited October 8, 2016, explicitly defines a null `after` value as no next page. These are source contracts; no live Reddit response was fetched for this work.

The amendment retains that null value instead of converting it to an empty string. A strict null check at the start of `downloadNextPage` calls the supplied end callback, when present, and returns before creating an AJAX request.

## Integration boundaries

| Source state | Result |
| --- | --- |
| Newly constructed channel, empty initial cursor | First-page request remains available. |
| Valid response with a nonterminal cursor | Existing paging and duplicate-page continuation remain available. |
| Valid listing container with explicit terminal null | The cursor stays null; newly returned posts still enter the cache. |
| Cached post available after a terminal response | `getCurrent` returns that post before it reaches the page-request guard. |
| Cache exhausted after terminal null | Normal end callback, with no new feed request. |
| Request failure or invalid top-level listing shape | Existing retry/error path; this amendment does not manufacture terminal state. |
| Missing cursor or other unexpected falsy cursor | Existing fallback remains; only explicit null activates the new guard. |

The existing no-progress rule for an empty or duplicate-only page, post filtering, `currentID` movement, retry count, delay, HTTP-error handling and render callbacks are retained. A new channel initializes its own empty cursor. This change does not add request coalescing, stale-response arbitration, refresh semantics, deeper post-shape validation or a concurrency guarantee.

## Exact source and review record

- Source repository: [cobalt-arc-dev/minireddit](https://github.com/cobalt-arc-dev/minireddit).
- External contribution: PR 28, `fix-feed-network-errors`, head `a5cfbec7df83bab3d54df81fb30919c7dd242c84`; open and unmerged at the October 5, 2026 10:47:09 UTC read, with zero issue or inline comments.
- PR base: `ebf72589ba9639ee1bd5f5be2ca782dda66e6998`.
- Complete preimage `js/reddit.js`: Git blob `ae681163eaa112a865ce09405695f13e92ade68f`, 5,620 UTF-8 bytes.
- Complete postimage: Git blob `cecb482a2e9f78b770b9b5ca1a82d90f1d5f3097`, 5,807 UTF-8 bytes.
- Complete caller `js/behavior.js`: `ce575864e7dfad989809b1fc1f420c8302701c0c`.
- Complete renderer `js/renderer.js`: `d3d82c406d19028cebc23f115fc773f61f0ba60a`.
- Complete root README: `2e26ed1789c7f4633349650b4dd76f069dd0f1fa`.
- Unchanged MIT license: `4aa1a23e10abf3a04ee9d4c4d771ddcb827297bb`.
- The pinned root and JavaScript directory listings contain no additional agent or contribution instruction files.

The PHP pair was independently inspected: `feed.php` blob `d5cefb80bca6545578e161237455ee1a511f56e5` and `post.php` blob `5e1f155c1b97c8812e5f0e4ecfbc1f5e4d1fba8c`. No PHP change is part of this packet. A mistyped post-blob read returned a retained 404; the separately named file at the pinned head supplied the actual source identity.

The complete changed-file list and complete JavaScript patch of [darshan-Jahagirdar's PR 29](https://github.com/dionyziz/minireddit/pull/29) were also inspected. That patch likewise uses `feed.data.after || ''` and introduces no terminal-cursor guard. Its broader work is credited to its original author. PR 32's author explicitly withdrew that attempt because PRs 28 and 29 already cover the broader issue. This packet therefore continues the specific remaining cursor behavior on PR 28 rather than presenting another complete issue implementation.

The precise Commons PR search for MiniReddit returned zero results with `incomplete_results: false`. A public Slack search for the repository locator returned zero rendered results and provider END. Those are bounded observations of their retained requests; they do not prove absence of work elsewhere.

## Verification and acceptance

The complete preimage and its two changed hunks were inspected with the actual caller and renderer. The serialized patch was applied once to the retained complete preimage, with every context/deletion line and hunk count checked, and produced the exact complete postimage. Independent Git-blob identities cover the complete source bytes. Publication readbacks separately establish the delivered packet identity.

No application JavaScript, browser, PHP process, test, fixture, workflow, network feed or runtime smoke was executed. This is a source correction, with runtime and upstream maintainer acceptance unperformed.

[Issue 21](https://github.com/dionyziz/minireddit/issues/21) contains a historical $20 offer dated November 10, 2014. That history does not establish a renewed award, assignment or payment. The external branch and PR were not mutated, and no upstream claim or contact was made. Dionysis Zindros and the original project contributors retain the attribution in the included MIT license; cobalt-arc-dev retains credit for the PR 28 implementation.
