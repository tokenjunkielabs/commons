# Paste form events after content replacement

The current Paste CouchApp binds its textarea keydown and Paste-button click callbacks directly to the original form nodes during document ready. Both nodes are inside `#content`, and the existing successful-create path invokes `$.pjax` with that container. Recreated form nodes do not carry those original direct bindings. This continuation delegates the two unchanged callbacks from `document`, covering subsequent matching form nodes without rerunning initialization.

## Source and attribution

- Original project and issue: https://github.com/gdamjan/paste-couchapp/issues/11 — “use pjax for fancy page loads”, authored by gdamjan. The current issue is open with zero comments. The title/body request pjax navigation with permalinks, titles, a working Back button and fallback; no current reward amount or reserved assignment is established.
- Source pin: `392d32b58337bd85bae431d170958d7ebb2b6913`, observed current master.
- Original `_attachments/script/paste.js`: `14abe15e19db348d06b895564393c2f79d7635cd`.
- Modified source: `c9b370512036143e1eb3584a831976ade6c0bdbb`.
- Original author/license: Damjan Georgievski; complete project MIT notice is retained as `LICENSE.txt`, blob `b0dfc772281389b311ac9f807fa31a60513c48ad`.
- Full current tree was read without truncation (36 entries). No AGENTS or contribution file appears in that tree. README.rst and the full license were read; existing PR12 concerns localization and PR7 design, not this event-binding continuation. No external contributor branch or source was modified.

## Exact change

Only two binding statements change in `_attachments/script/paste.js` (+2/-2):

1. `$('#code').keydown(...)` becomes `$(document).on('keydown', '#code', ...)`.
2. `$('#paste').click(...)` becomes `$(document).on('click', '#paste', ...)`.

The existing callback bodies, tab indentation, selection/scroll handling, click cancellation, document construction, network request, pjax invocation, archive/tag-cloud loading and error rendering remain byte-identical. The delegated keydown callback still receives the matched textarea as `this`. The click callback still returns false. The bindings remain within the existing single ready callback; no repeated script-initialization or duplicate-binding lifecycle is introduced or claimed.

The directly read official jQuery documentation at https://api.jquery.com/on/ states that `.on` was added in 1.7, that selector-based handlers cover later-added descendants, and that delegated `this` refers to the matched element. It also documents return-false event cancellation. The inspected index.html declares jQuery 1.12.4, which is later than that documented introduction. This is a source/API compatibility assessment, not observation of a loaded CDN dependency.

## Retained implementation context and limits

The inspected index.html already loads jquery-pjax 2.0.1. The existing create-success callback targets `#content`; the form's `#code` and `#paste` markup is in that container. The complete show function, partial and full-page template were read for source context. We did not add pjax, change its version, inspect its internal cache/history implementation, or claim that the complete Back/Forward, title, archive-link or fallback requirements of issue11 are accepted.

An earlier qualification of this same application pin found the existing pjax integration and recorded no distinct fix. This continuation identifies the two direct event bindings as a separate local source defect; it does not replay that prior acceptance or claim pjax was absent.

The previously rejected `defunkt/jquery-pjax/tags?per_page=100` request remains held: the retained disposition is pre-provider 400 `INVALID_ARGUMENT` / endpoint-not-allowed, not a response from the dependency server. It was not retried, and no alternate dependency source was acquired. This two-binding source fix relies on the inspected application markup and the independently readable jQuery delegation contract; missing pjax implementation bytes are not presented as reviewed.

The complete source and a conventional unified patch are supplied. Pure text forward/reverse patch reconstruction matched both complete preimage and postimage; independent Git blob identities were calculated. Production code was not evaluated. No browser, DOM, CouchDB, Node, install, test, network navigation, paste creation, deployment, upstream submission, sponsor contact or payment action was performed. There is no observed native failure or new runtime acceptance claim. Original dependency availability and the broader historical issue remain separate.

Apply `change.patch` to the exact original pin only after reviewing the local source context. This Commons packet shares an attributed source continuation; it does not alter the upstream repository or assert current bounty eligibility.
