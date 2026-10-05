# IFC worker: forward the requested type code

The actual main-thread `WebIfcHandler.GetNameFromTypeCode(type)` sends `{ type }`. Its worker counterpart reads `data.args.modelID`, a key the caller never sends. This one-line continuation forwards `data.args.type` to the existing native API call and preserves its result/post path.

## Exact source

- Repository: `ThatOpen/web-ifc-three`.
- Current main: `f58bfa92c4e27d257bd0aa37da841b48334c7420`.
- Changed path: `web-ifc-three/src/IFC/web-workers/workers/WebIfcWorker.ts`.
- Preimage: `a4362dc634f3e3ddec4bcea0d6b36420b60e7265`.
- Actual producer: `web-ifc-three/src/IFC/web-workers/handlers/WebIfcHandler.ts`, `41fe0814e3dec444f40df5d58d426a0a94d52adc`.
- Existing direct type-code consumer: `web-ifc-three/src/IFC/components/properties/WebIfcPropertyManager.ts`, `89435dde8a819e0f0b2cbff92351cb23ec455c30`, passes the entity's typeID to the same API.

The exact related [PR153](https://github.com/ThatOpen/web-ifc-three/pull/153) by beachtom is already merged at `7c7e8a4697b45a2afecb4de8652efd5939effd12`; its original two relevant worker patches contain this same mismatch. This packet corrects the current source rather than replaying that update. Original IFC.js and contributor attribution is retained; the MIT license is included unchanged.

Apply `change.patch` at the documented current-main pin, or compose the single argument-key correction into later source. The full postimage is included at its original relative path. No external branch or upstream PR is changed.

## Scope

Only the native API argument key changes. Worker actions, request IDs, response serialization, model IDs in other operations, and streaming behavior are untouched. The correction does not promise that every numeric type code has a valid IFC name.

The defect was discovered while qualifying [issue59](https://github.com/ThatOpen/web-ifc-three/issues/59), whose generated-class identity request remains unresolved. No IFC class reconstruction is added. Broader worker exception handling, rejection transport, stream completion and disposal require separate work and are not represented as fixed.

## Acceptance limits

The full worker, producer, property caller, current source instructions and relevant historical production patches were read. The current README marks this library deprecated and recommends Components. No current funding, sponsor acceptance or upstream adoption is claimed.

This is AI-assisted static producer/consumer reasoning and complete published-byte readback only. No worker, browser, WASM, native program, model, compiler, tests, fixtures, build, workflow or upstream submission was run. Runtime name lookup and integration acceptance remain unperformed.

Changed 2026-10-05: forward the existing `type` payload field instead of absent `modelID`.
