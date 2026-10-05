# Preserve an explicit false fast-boolean setting in the IFC viewer

Operation: IFC-VIEWER-FAST-BOOL-FALSE-20261005-7CA6  
State: source-only attributed continuation; native/browser integration unperformed.

The current viewer's loadIfcUrl reads the configured USE_FAST_BOOLS value, applies `|| true`, and writes the result back through applyWebIfcConfig before loading. Consequently a caller's explicit false becomes true.

[fast-bool-false.patch](fast-bool-false.patch) changes that one expression to `?? true`. A missing setting keeps the viewer's existing true default; false is forwarded as false, and true remains true. The interpretation is supported by the dependency's actual optional-boolean interface, not by an assumed geometry outcome.

## Source contract

| Input | Immutable identity |
|---|---|
| ThatOpen/web-ifc-viewer current master | `1f5c975ad6d019e7355c8759369f318f9fa3e339` |
| viewer/src/components/ifc/ifc-manager.ts | `b63213d3bd258c0463c2bbf5ba38484535ea85e1` |
| viewer/package.json | `45000a07e3ad3e9074db48cd72746d98bd001155` |
| CONTRIBUTING.md | `1031d1920deea4ad02e41133e6688e797d05f746` |
| LICENSE.md | `97284c8b321ff5aafc9fc05aa2071d92ed86b20d` |
| web-ifc release 0.0.39 commit | `7f41e454642e52f43d8976a5410df68af5c0a3dd` |
| Its src/web-ifc-api.ts | `3fd87fd012661e34ed520f1fa37171b1cb9d7136` |

The [viewer source](https://github.com/ThatOpen/web-ifc-viewer/blob/1f5c975ad6d019e7355c8759369f318f9fa3e339/viewer/src/components/ifc/ifc-manager.ts) imports LoaderSettings directly from web-ifc. Its public applyWebIfcConfig accepts that type; loadIfcUrl reads the loader's stored settings and applies the two selected options before loadAsync. The [declared manifest](https://github.com/ThatOpen/web-ifc-viewer/blob/1f5c975ad6d019e7355c8759369f318f9fa3e339/viewer/package.json) specifies web-ifc ^0.0.39 and TypeScript ^4.3.2.

The official [0.0.39 release](https://github.com/ThatOpen/engine_web-ifc/releases/tag/0.0.39) identifies the pinned dependency source. Its [API](https://github.com/ThatOpen/engine_web-ifc/blob/7f41e454642e52f43d8976a5410df68af5c0a3dd/src/web-ifc-api.ts) declares `USE_FAST_BOOLS?: boolean` and marks the option deprecated. OpenModel creates defaults then spreads supplied settings, preserving an explicit false before forwarding to its WASM module. This establishes the setting-passthrough contract; it does not establish that the deprecated option changes every native geometry path.

The actual checked-in dependency snapshots are stale relative to the current manifest: root package-lock.json (`e1926b0a06e1c9648685625aeb8f8e56cf6e1433`) records web-ifc 0.0.35 and the older viewer1.0.206 dependency set; viewer/yarn.lock (`1b81c58a670c3101c43ae1e37fbb441520fae9c8`) records web-ifc0.0.20 through web-ifc-three0.0.31. No installed resolution is asserted, and no lockfile is invented or repaired here.

## Integration and limits

Apply the single hunk to the pinned manager or compose the same expression change into its current successor. This patch-only delivery deliberately touches loadIfcUrl alone. Preserve the separate completed loadIfc object-URL cleanup when composing; do not replace the whole manager with an older postimage.

The coordinate-origin logic, first-model behavior, loadAsync call, error callback and other wrapper behavior are unchanged. This is not a repair for model distortion, georeferencing, subset visibility, fragment parsing or all loader configuration handling. Runtime values outside the declared optional-boolean contract are not newly validated.

The complete current source, manifest, release metadata and dependency API were inspected. The immutable production hunk is +1/-1. No build, package installation, browser/native/WASM run, tests, synthetic fixture or prior object-URL proof was executed. The held IFCFragmentParser route is unrelated to this direct web-ifc type and was neither read nor reacquired elsewhere.

The two exact bounded viewer/Commons searches for USE_FAST_BOOLS supplied no matching implementation carrier; this is not an exhaustive absence claim. This packet does not mutate an upstream branch, open an upstream PR, contact maintainers or claim active bounty funding or upstream acceptance. ThatOpen's withdrawn bounty availability remains separate from this source correction.

The IFC.js contributors retain attribution. [LICENSE.md](LICENSE.md) reproduces the current viewer's MIT notice exactly, including its lack of a trailing newline. The actual contributor guide encourages discussing contributions; this internal Commons integration artifact makes no claim of an upstream discussion or approval.
