# BeyondMafia issue87: latest thread page and bottom Reply control

This noncommercial source continuation implements the two concrete navigation affordances requested at https://github.com/BeyondMafia/BeyondMafia-Integration/issues/87. It is prepared from the actual current production source, with native application acceptance still pending.

## Exact source and integration

Current master: 00b164ee3266c8acc19a323fd0c627952856f588.

- routes/forums.js preimage: 07c7035c99de95362db3ae442b7053ab9f07be8e.
- react_main/src/pages/Community/Forums/Thread.jsx preimage: a6d8a428002c08e54e4d2f54ad23d6ea7d6627af.
- Upstream license: 848335aeb452b0630ea8fb742ba58cffd12bb63d.

Apply change.patch to this pin or compose its small additive hunks with current source. Full postimages are included for inspection; do not overwrite newer modules. Source line endings are preserved. No dependency, schema, permission, service credential, or styling change is required.

The separate PR956 / Commons31594 enhanced-markdown continuation modifies the thread's Markdown import and renderer; its change can be composed with this bottom-control hunk. Neither packet replaces the other.

## Behavior

The thread page initially fetches /forums/thread/:id with an optional reply selector. The server previously chose page1 when no page was supplied. After loading and checking the requested thread, the new branch uses the same existing reply-count/replies-per-page calculation as the returned pageCount. An empty thread remains page1. The response's page and selected replies now refer to the same latest page.

Only a request with no explicit page and no nonempty reply selector takes this default. Explicit page requests, valid reply deep links and the existing invalid-selector behavior retain their original paths. Stored page grouping, chronological order within a page, deleted-reply filtering and view-count rules remain unchanged. This does not reverse replies, renumber historical pages or redesign pagination.

A Reply button now sits below the bottom PageNav. Its visibility matches the thread reply icon's deleted-thread, postReply and locked-thread conditions. It reuses onReplyClick, the existing reply form, existing scrolling behavior and existing submission path. It does not itself submit or change server authorization. The existing POST /reply continues to enforce login, board-scoped permission, rate limits, lock policy and content constraints.

## Source review and acceptance limits

The complete current Thread component and the relevant GET-thread and POST-reply route bodies were inspected. Their full repository files are retained, but unrelated API routes were not independently audited. The current master is PR956's exact base; the complete three-file PR delta and recursive tree establish the reused license/README and absence of additional AGENTS/CONTRIBUTING files for these paths.

The sole returned issue comment is a historical collaborator offer of 20 tokens. A bounded exact issue-number PR search returned 0 with incomplete_results=false; the exact issue URL public search returned 0/END. These observations do not establish current reward availability or a globally complete submission census.

No Node/React execution, database, browser, tests, fixtures, live forum interaction, account changes, workflow or upstream submission occurred. Native visual/navigation/server acceptance remains unperformed. This packet does not claim a bounty award, payment, deployed behavior or a broader forum audit.

## Attribution and license

Original source: BeyondMafia contributors, https://github.com/BeyondMafia/BeyondMafia-Integration/tree/00b164ee3266c8acc19a323fd0c627952856f588. The request credits forum user null in the original issue.

Modified 2026-10-05 to default unselected threads to their latest page and add the bottom permission-aware reply control. Dated notices are present in both postimages.

Source, patch and adaptation contributions are shared under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International, https://creativecommons.org/licenses/by-nc-sa/4.0/. The complete unchanged upstream LICENSE is included. Attribution, noncommercial/share-alike conditions and warranty disclaimer remain applicable; no endorsement or commercial-use permission is implied.
