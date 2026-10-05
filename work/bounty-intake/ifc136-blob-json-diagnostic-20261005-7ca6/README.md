# IFC loader: diagnose JSON object/array payloads behind blob URLs

This is an attributed source continuation over [TeapoyY's PR195](https://github.com/ThatOpen/web-ifc-three/pull/195), not an upstream submission. The original request is [web-ifc-three issue136](https://github.com/ThatOpen/web-ifc-three/issues/136). Its actual caller creates a blob URL from a selected file and calls `loadAsync(ifcURL)`. A blob URL does not preserve the selected filename, so the contribution's `url.endsWith('.json')` guard misses that caller.

## Source and integration

- Repository: `TeapoyY/web-ifc-three`.
- Donor head: `bf66da21f685f91c22e1301c16b2bc6cca688796`; base: `f58bfa92c4e27d257bd0aa37da841b48334c7420`.
- Exact path: `web-ifc-three/src/IFCLoader.ts`.
- Preimage blob: `a7359cb579e93a79a80f1dfc8de4c5de6482f409`.
- Package source: `8de8e2327b19e609853126fe11e700f50c686df7`, web-ifc-three0.0.125 / three^0.149.0.
- Full postimage is included at the original relative path; `change.patch` applies to the exact donor pin. Review and compose with any later loader changes instead of replacing newer source.
- Original IFC.js license is included unchanged as `LICENSE.md`. TeapoyY's message and diagnostic intent are preserved with this explicit attribution.

## Resulting behavior

The downloaded `ArrayBuffer` is viewed through `Uint8Array` inside the existing FileLoader callback's try/catch. The scanner skips an optional UTF8 BOM and ASCII JSON whitespace (space, tab, LF, CR), then checks for an opening object brace or array bracket. Those payloads raise the explanatory JSON/metadata error through the existing callback and loading-manager error path, before IFC parsing. This also works independently of URL query strings, capitalization and filename extensions.

The filename-only early rejection is removed. A URL ending in `.json` that actually returns IFC data now follows the existing parser. JSON diagnostics consequently require downloading the content; no extra request is added. Other bytes retain the same parse call. The view does not copy the buffer or decode/parse the complete JSON document. The prefix scan uses constant auxiliary space and inspects only the BOM/leading whitespace plus first significant byte.

The diagnostic deliberately recognizes object/array-shaped UTF8 payloads. It is not a JSON validator, cannot distinguish a malformed object-like document from valid JSON, and does not detect scalar or UTF16 JSON. Direct `parse(buffer)` behavior is unchanged. Geometry cannot be reconstructed here from an exported properties-only document: the existing message directs callers to load IFC geometry and attach JSON properties through `addModelJSONData()`. No JSON geometry support is added.

## Scope and acceptance

Current issue136's eight comments contain historical take/drop cycles; current PR195 is open, unmerged, with no discussion comments. The full loader, package, MIT license and contribution guide were read. The current upstream README explicitly marks this library deprecated and points to Components. No current bounty, sponsor acceptance, upstream merge or payment is claimed.

Validation is AI-assisted static source reasoning and exact published-byte readback only. No compiler, model, browser, WASM, tests, fixtures, build, workflow or networked application was run. Native integration, callback behavior in a running application and maintainer acceptance remain unperformed. The reported blob URL failure is source-bound; the packet does not claim the broader original request is complete.

Changed 2026-10-05: content-based diagnostic replaces filename-only detection; no unrelated loader API or property-manager changes.
