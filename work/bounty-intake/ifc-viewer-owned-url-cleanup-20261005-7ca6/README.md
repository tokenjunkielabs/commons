# Release IFC file URLs after loading settles

## Result

`IfcManager.loadIfc(file)` creates an object URL and passes it to `loadIfcUrl`, but the original function never releases that URL. This continuation gives that locally created resource a bounded lifetime: await the existing load in a try block and revoke the URL in finally.

The await is necessary. Returning the pending promise directly from the try block would run finally before loading settles. The correction releases the URL after a returned model, the loader's existing null-on-error result, or a rejection such as an error callback throwing. It does not revoke URLs supplied directly by callers to loadIfcUrl.

## Exact source

- Repository: https://github.com/ThatOpen/web-ifc-viewer
- Current master: `1f5c975ad6d019e7355c8759369f318f9fa3e339`.
- Full current source: https://github.com/ThatOpen/web-ifc-viewer/blob/1f5c975ad6d019e7355c8759369f318f9fa3e339/viewer/src/components/ifc/ifc-manager.ts
- Original source blob: `b63213d3bd258c0463c2bbf5ba38484535ea85e1`, 8673 UTF-8 bytes.
- Corrected source blob: `d5151b805102e3babb19fee832fcc9b80a658e90`, 8745 UTF-8 bytes.
- Unchanged upstream MIT license: `97284c8b321ff5aafc9fc05aa2071d92ed86b20d`, copyright 2020-2022 IFC.js.

The complete 8,673-byte original manager was acquired and read. Its local url appears only at creation, forwarding, the loadIfcUrl parameter and the awaited loader.loadAsync call. The awaited flow finishes model registration, optional coordination-matrix setup and frame fitting before returning. Its existing error handler logs and calls onError before returning null; those behaviors are preserved.

The complete root README, CONTRIBUTING, root package and viewer package were read. The recursive tree returned 128 entries with truncated=false, no AGENTS file and no nested contribution instruction. The viewer declares web-ifc ^0.0.39 and web-ifc-three ^0.0.125, and obtains IFCLoader from that dependency. The source and exact upstream license are included with attribution.

## Scope and original issue

This source was inspected while qualifying https://github.com/ThatOpen/web-ifc-viewer/issues/160, which reports a CSP unsafe-eval failure in generated web-ifc-api.js. All ten returned issue comments were read. Collaborator comment1712756825 and the current README explicitly deprecate this viewer in favor of components.

No viewer-local correction to that generated dependency failure was established. This packet is a separate object-URL lifetime repair and does not resolve issue160, change Content Security Policy, enable evaluation, alter the parser, replace WASM, or claim compatibility with a strict enterprise policy.

Only loadIfc's local resource lifetime changes. The load arguments, progress/error behavior, model/scene operations, direct URL API, configuration choices and all other source bytes are unchanged. A separate observed USE_FAST_BOOLS defaulting expression remains unmodified; no imported setting contract was inferred for that potential change.

## Validation and remaining limits

The actual serialized patch contains one production hunk, +5/-1. Its complete context and deleted line match the full retained preimage. Applying the parsed serialized rows exactly produces the retained postimage, with independently computed Git blob identities. No synthetic input or application code execution was used for this source transformation check.

No browser, file picker, File/Blob operation, IFC model, WASM parser, renderer, compiler, application, build, test, fixture or hosted workflow ran. No memory measurement or runtime acceptance is claimed. Final publication checks bind complete source/patch/guide/license bytes, exact paths, the contribution head and immutable merge.

Two direct primary documentation reads returned ServerError and remain held without retries or alternate retrieval:
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/script-src
- https://developer.mozilla.org/en-US/docs/Web/API/URL/revokeObjectURL_static

Neither page is described as successfully verified. The change is supported here by the complete actual control flow and explicit ownership of the created URL.

## Contribution and overlap

The original module and library are attributed to IFC.js. Current CONTRIBUTING asks contributors to communicate and submit a named PR; this packet does not submit or contact upstream. Historical bounty labels do not establish current payment.

Bounded native PR searches for revokeObjectURL and USE_FAST_BOOLS returned zero results. The broader memory search returned a closed 2D-dimension proposal and the already merged single-model disposal PR180; their titles/bodies are not a new URL-cleanup handoff. The scoped Commons PR and public Slack searches returned no result, with only bounded response coverage. This is not an exhaustive proof that no related work exists.
