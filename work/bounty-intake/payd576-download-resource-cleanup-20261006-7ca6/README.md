# PayD #576: clean up CSV download resources on exceptional exits

The existing report export allocates an object URL and a temporary anchor, then cleans them up only after every setup/click operation succeeds. This patch gives each acquired resource a `finally` scope so an intervening failure reaches its cleanup before the existing export error handling.

## Attribution and exact source

The feature belongs to [waterWang's existing Protocol-Guild/PayD PR #576](https://github.com/Protocol-Guild/PayD/pull/576), branch `waterWang/PayD:feat/419-custom-report-export`, observed OPEN at `2aa6ea6f6668c5d0629ba475e558c02b6a0e79ab`. It implements CSV export and state feedback for [issue #419](https://github.com/Protocol-Guild/PayD/issues/419). This Commons packet is a narrow attributed source continuation; it does not create or change an upstream carrier, assignment, review, or acceptance.

Apply `download-resource-cleanup.patch` to that exact donor head:

| Path | Preimage Git blob | Prepared postimage Git blob | UTF-8 bytes before / after |
|---|---|---|---:|
| `frontend/src/pages/CustomReportBuilder.tsx` | `27d8997b76c0af3ed2708a33bb9fcc58971fb6c9` | `3189b151633ef87a7a4ca67bbb1786ff71797afe` | 11,270 / 11,358 |

The source change is +13/-7 in one hunk with 26 complete rows. The patch itself is blob `a4106aa1f9ee23e44394a09e6ddac1aecdc6e9f2`, 1,161 bytes. Its serialized unified diff materializes the exact postimage and reverses to the exact donor string. No whole donor module or report rows are published in this packet.

The full donor `frontend/src/App.tsx`, blob `a44ff0140842d698327362ab3aa2cdc16e5d61ba` at the same head, imports this component and mounts it at `/reports` within the existing employer layout and error boundary. The component's actual Export button invokes `handleExport`. These are source connections, not evidence of deployment or a browser run.

## Resource ownership

After successful `URL.createObjectURL(blob)`, the outer local `try/finally` reaches `URL.revokeObjectURL(url)` if anchor creation, setup, append, click, or anchor cleanup fails. After successful anchor creation, the inner `try/finally` reaches `link.remove()` on setup or click failure as well as success. The outer resource scope means an exception during anchor cleanup does not skip the URL cleanup attempt.

The existing encompassing catch still sets the export error and calls the error notification; its existing final block still clears `isExporting`. Success notification remains after both resource scopes. Cleanup exceptions can replace an earlier exception under ordinary JavaScript finally semantics; this packet does not add suppressed-error reporting or a guarantee that modified/throwing browser APIs successfully release resources.

The [WHATWG DOM removal algorithm](https://dom.spec.whatwg.org/#dom-childnode-remove) returns when the node has no parent, allowing this same removal call whether or not setup reached attachment. The [File API object URL contract](https://w3c.github.io/FileAPI/#dfn-revokeObjectURL) defines creation as adding an entry and revocation as removing the eligible entry. These primary sources support the API ownership argument only; no browser implementation was exercised.

## Preserved behavior and boundaries

CSV headers, row selection, cell escaping, mock input records, date filtering, Blob MIME type, filename, the existing 500 ms simulated wait, notifications and rendered UI are byte-for-byte unchanged outside the single resource block. Immediate cleanup after `click()` is retained. It has not been established as correct download timing in any browser, nor does a success notification prove that a file reached disk.

This patch adds no backend export call, real-data integration, account access, payment action, or CSV/formula policy. It does not repair initial-load state, an interrupted component lifetime, multiple overlapping invocations, missing browser APIs, translation coverage, date-label associations, or full issue #419 acceptance. The earlier Commons #31914 label and #31918 translation packets target another exact source baseline; no automatic composition with this external feature head is asserted.

The current upstream PR body reports prior type/lint/format checks. Those are the original author's claims, not executions or independently reproduced outcomes for this continuation. Current PR metadata reported zero issue/review comments. Issue discussion bodies were not acquired for this change. A bounded Commons PR search for `"PayD" "576"` returned no entries; that is limited query evidence, not a repository-wide absence or ownership guarantee.

## Validation and licensing

Validation here consists of complete pinned source acquisition, exact string replacement, full serialized forward/reverse patch materialization, independent Git blob identities, and source-contract reasoning. No JSX compilation, npm install, lint, test, synthetic DOM, browser, download, export execution, environment lookup, account access, or upstream operation occurred.

The donor's root `LICENSE` was read at the same feature head. It is the complete Apache License 2.0 text, blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`, 11,357 bytes, included unchanged here. Original feature and repository contributor attribution remain intact. This dated Commons guide identifies the modification without claiming an ownership transfer or broader license audit.
