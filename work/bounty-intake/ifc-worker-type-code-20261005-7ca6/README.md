# IFC worker: type-code forwarding and header-line dispatch

This packet contains two source-bound corrections at the existing main-thread/worker boundary. It retains [Commons31611](https://github.com/woahwhattheheck/commons/pull/31611)'s type-code fix and adds the missing header-line receiver.

`WebIfcHandler.GetNameFromTypeCode(type)` sends `{ type }`. The original worker reads absent `data.args.modelID`. The worker now forwards `data.args.type`, preserving its result/post path.

`WebIfcHandler.GetHeaderLine(modelID, headerType)` sends the existing action string `getHeaderLine` to `WorkerAPIs.webIfc`. The original WebIfcWorker has no such method; the dispatcher rejects the unknown action before a result can be posted. The new lower-case adapter forwards both existing arguments to `this.webIFC.GetHeaderLine()` and posts the existing envelope. Its required `WebIfcWorkerAPI` entry records the same action. No new action or request format is introduced.

## Exact source and composition

- Upstream: `ThatOpen/web-ifc-three`, main `f58bfa92c4e27d257bd0aa37da841b48334c7420`.
- `web-ifc-three/src/IFC/web-workers/workers/WebIfcWorker.ts` preimage: `a4362dc634f3e3ddec4bcea0d6b36420b60e7265`.
- `web-ifc-three/src/IFC/web-workers/BaseDefinitions.ts` preimage: `53923903c27b8d1c26d0a7c45b92c73344cea2f9`.
- Actual producer: `web-ifc-three/src/IFC/web-workers/handlers/WebIfcHandler.ts`, `41fe0814e3dec444f40df5d58d426a0a94d52adc`.
- Existing native signature is also used by `WebIfcPropertyManager.getHeaderLine(modelID, headerType)`, source `89435dde8a819e0f0b2cbff92351cb23ec455c30`.
- Dispatch source: `IFCWorker.ts`, `cd3c3d526bf0b1f2f45973cce7dcefe28a9118b8`; `IFCWorkerHandler.ts`, `0394b3a965a6cc781e1438c76a27e86f96dbf908`.

`change.patch` is now cumulative against those two upstream preimages. It replaces the earlier one-file patch; do not apply both independently. The full worker postimage includes the prior type-code correction, and the full definitions file includes the one added interface entry. Compose with later source instead of overwriting it.

The earlier source packet's worker preimage `3ff201e85f9e27874a8caa523dd593550558272f`, patch and guide were checked on fresh Commons main before this continuation. The existing original IFC.js MIT license remains unchanged. Related merged upstream PR153 by beachtom introduced the type-code mismatch; original contributor attribution remains intact.

## Boundaries

The header adapter returns the existing native result through the ordinary post envelope. It adds no special serializer or class reconstruction. Request IDs, action values, normal response handling, model IDs in unrelated operations and mesh streaming are unchanged.

The original [issue59](https://github.com/ThatOpen/web-ifc-three/issues/59) generated-class identity request remains unresolved. General worker exception/rejection transport, streaming completion, disposal and postMessage failure handling are outside these corrections. In particular, native exceptions still follow the existing outer-dispatch behavior; this packet does not claim they are now delivered to the caller.

## Acceptance limits

The full producer, worker, dispatcher, handler, property caller and relevant interface definitions were read. Existing contribution instructions and MIT terms remain applicable. The current README marks this library deprecated and recommends Components. No current funding, sponsor acceptance or upstream adoption is claimed.

Validation is AI-assisted static producer/consumer and dispatch reasoning plus complete published-byte readback. No worker, browser, WASM, native program, model, compiler, tests, fixtures, build, workflow or upstream submission occurred. Runtime lookup/header behavior and integration acceptance remain unperformed.

Changed 2026-10-05: preserve the type payload correction and add the missing lower-case header dispatch adapter/interface entry.
