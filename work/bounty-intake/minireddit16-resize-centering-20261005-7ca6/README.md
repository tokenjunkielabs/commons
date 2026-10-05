# MiniReddit: keep images centered when the viewport changes

## Result

This source continuation adds a window-resize handler to the existing UI module in [dionyziz/minireddit PR30](https://github.com/dionyziz/minireddit/pull/30). It recomputes the horizontal position of the current image and the outgoing page-transition image using the application's existing centering formula.

The production change is one hunk, **+8/-0**, in `js/ui.js`. The packet includes the complete corrected module, its exact patch and the original MIT license.

## Current source and scope

The external mobile contribution is authored by cobalt-arc-dev on `cobalt-arc-dev/minireddit:mobile-support`, head `ca2053c39efd2f9b15c0c5b90291857d531fd329`, base `ebf72589ba9639ee1bd5f5be2ca782dda66e6998`. The current metadata read still showed it open and unmerged, with no issue or inline review comments.

Its four changed files add the viewport meta tag, responsive image widths, a scrollable dashboard and mobile toolbar styling. This correction composes with that work and preserves its authorship.

## Source-backed gap

The contributed stylesheet gives `#img` and `#oldimg` responsive maximum widths. The renderer independently stores an inline pixel `left` value, calculated from the viewport and rendered image widths.

The complete renderer sets that position in the image-load callback and when it creates the outgoing image in `Render.motion()`. The complete UI, dashboard and behavior modules contain no viewport-resize handler that updates those positions. A viewport change can therefore change the image's rendered width while retaining a position calculated for the previous dimensions. The old position can leave the image off-center or partly outside the viewport until another image load or page transition occurs.

This consequence follows from the stored inline position and the responsive CSS. No browser observation or device reproduction is claimed.

## Correction

The new handler reads the current window width once, then selects the currently present `#img` and `#oldimg` elements and applies the existing calculation:

`Math.floor(viewportWidth / 2 - $image.width() / 2)`

The dynamic selection includes an outgoing image if one has been created since the handler was registered. It uses each image's own current rendered width. Initial loading and navigation retain their existing positioning paths.

The handler writes only the horizontal `left` property. It adds no feed request, image reload, navigation step, loading-state update or read-history update. Existing animation transforms, opacity and image size rules are preserved. The source page already loads jQuery 1.8.1 before this UI module.

## Immutable source identities

| Path | Git blob |
| --- | --- |
| Original `js/ui.js` | `e9ba08e90cda399aaacf7a91b8d8409b5919ec2e` |
| Corrected `js/ui.js` | `f155bf1fbcd4d624766e92c7941e1bf0d00a2ae1` |
| `js/renderer.js` | `bfb3ff90291cb886f18ec2989788d7f25cb0898c` |
| `js/dashboard.js` | `50b0b1d84a2b9fd7452c0eca283367aece919997` |
| `js/behavior.js` | `a9ec863454859ed4c734c0b71381c044f1d63988` |
| `css/style.css` | `18243ae8963eddfad69105d3fd4b753d4b36f150` |
| `index.php` | `1e7fd5c2202e2c6c4a67f026de13bca86725fc7d` |
| `LICENSE` | `4aa1a23e10abf3a04ee9d4c4d771ddcb827297bb` |

The complete 39-entry recursive tree at the contribution head reported `truncated: false`; it contained no AGENTS.md or contributor-instruction file. The README and MIT license identities match the already retained complete source texts. Tree metadata was provider-reported, not independently hashed as a whole.

## Verification

The complete original UI module is 2,365 UTF-8 bytes and independently computes to its native Git blob. The corrected module is 2,615 bytes and computes to `f155bf1fbcd4d624766e92c7941e1bf0d00a2ae1`.

Applying the actual serialized patch to the full retained preimage matched the intended postimage exactly. All context lines and the old/new hunk counts matched. Source review covered the actual renderer positioning sites, viewport/styles, script loading order and UI/dashboard/behavior event paths.

No application code, browser, device, PHP server, existing tests or synthetic inputs were executed. The original contributor's PHP/CSS/HTTP validation statements remain their historical claims. This packet does not assert complete mobile acceptance.

Two attempted primary documentation reads, MDN's Window resize-event page and jQuery's .on() page, returned ServerError. Their exact requests and responses were retained; those routes were not retried and no successful documentation verification is claimed.

[Original issue16](https://github.com/dionyziz/minireddit/issues/16) asks to optimize the site for mobile use. Owner comment63228840 advertises 15 euros, last edited 2015-07-02. That is historical offer context, not current funding or a paid completion. Publication is confined to this owned source workspace; the external contribution and claim remain unchanged.
