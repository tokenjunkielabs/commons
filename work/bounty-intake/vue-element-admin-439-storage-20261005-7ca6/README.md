# Keep chunk recovery bounded when browser storage fails

This is a narrow production follow-up to [cerredz's existing pull request4353](https://github.com/PanJiaChen/vue-element-admin/pull/4353) for [vue-element-admin439](https://github.com/PanJiaChen/vue-element-admin/issues/439). It builds on that contribution's chunk detector, router registration and ten-second same-URL retry policy. It does not replace or resubmit the carrier.

The original helper reads `window.sessionStorage` in both exported functions' default parameters, outside its catches. It also permits a reload when storage is absent, treats a storage read exception as an absent marker, and ignores a failed marker write. A browser that cannot retain the retry marker can therefore repeatedly re-enter the automatic reload path. These are source-derived failure paths; this packet does not claim a browser reproduction.

The revised helper resolves the default storage object inside guarded logic. `handleChunkLoadError` reaches that lookup only after recognizing a chunk error. Missing storage, failed access, failed reads or writes, and a differing readback return false from `shouldReloadForChunkLoadError`. The helper permits automatic recovery only when it reads back the exact marker string it just wrote. Malformed stored JSON still counts as an absent marker, but a new marker must be written and read back before reload is allowed. The [HTML storage specification](https://html.spec.whatwg.org/multipage/webstorage.html#the-sessionstorage-attribute) documents storage-access and write exceptions.

The detection expression, current-URL argument, reload call, ten-second comparison, and handled-error return convention are unchanged. For a recognized chunk error, `handleChunkLoadError` still returns true even when it suppresses automatic recovery; it still returns false for unrelated errors. Manual refresh remains available. Successful immediate readback is evidence for that marker at that time, not a guarantee against later clearing, browser data eviction, cross-document changes, or an application startup failure. This change does not preserve form state or recover the originally attempted destination.

## Source and integration

The exact base is `cerredz/vue-element-admin@9444f9db28198900db0d03544200b2e683593c6c`, branch `issuehunt-439-chunk-load-retry`. The original production file is blob `062743a3933fcc323d1c40b2f292cd504b129353`; the complete postimage is `d6e8dba469a2f6fb0640d7b564e899e7d7752687`. `source-manifest.json` binds these identities and the original BATCH25-05 row10 operation.

Files in this packet:

- `src/router/chunk-load-error.js`: complete revised production file.
- `change.patch`: one-file patch against the exact existing contribution.
- `source-manifest.json`: source and scope bindings.
- `LICENSE`: unchanged upstream MIT license.
- This guide.

Before advancing the existing carrier, compare its current source/head with those pins and compose any intervening edits. Preserve the external author, existing router change and other contribution files. The patch is intended for this PR head; current upstream master does not yet contain the helper. It is not a second upstream pull request or a claim to the existing author's work. No provider mutation was attempted against that author's repository.

## Validation and remaining work

The complete original source was read and bound to its Git blob. The patch's removed span matches that source and its inserted span reconstructs the full postimage exactly. All changed branches were inspected as source. No JavaScript application execution, browser session, fixture, test, build or workflow was run. The existing contribution's reported checks describe its original head, not this follow-up.

Current intake observed the issue open and unassigned, this carrier open at the stated head, no issue-thread comments on the carrier, and no matching open PR by woahwhattheheck. These are observed intake facts, not sponsor acceptance, reward eligibility, an exclusive assignment or payment. Applying and exercising this follow-up remains a separate delivery step under the original work order.
