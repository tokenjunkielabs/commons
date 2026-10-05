# IFC plan camera: retain the cached model identity

This source continuation addresses a remaining exit/reentry path in [javi-codeworks' PR264](https://github.com/ThatOpen/web-ifc-viewer/pull/264). That contribution handles model-centered camera moves and direct switches between models for [issue126](https://github.com/ThatOpen/web-ifc-viewer/issues/126) and [issue102](https://github.com/ThatOpen/web-ifc-viewer/issues/102). This packet changes only which saved camera view may be restored.

## Exact integration

- Donor: `javi-codeworks/web-ifc-viewer`, head `f29e3b4a7e70ca92605c99c1df8b0608d8f538f0`.
- Base: `1f5c975ad6d019e7355c8759369f318f9fa3e339`.
- File: `viewer/src/components/display/plans/plan-manager.ts`.
- Preimage: `606393fa3a336719625d0fa4f63486710b879fdd`.
- Apply `change.patch` to that exact donor source, or compose its three changed lines into later code. The full postimage is included under the original path; do not overwrite a newer plan manager.
- Original IFC.js MIT license is included unchanged. Original contributor credit remains with javi-codeworks.

## Source defect and correction

`exitPlanView()` sets `active = false`, saves the floor-plan camera state, and clears `currentPlan`. A later `goTo()` for another model therefore computes `isChangingModel = false`. Its camera movement sees the shared boolean cache and restores the previous model's view instead of using the requested model's center.

The boolean is replaced by `cachedFloorPlanModelID?: number`. Saving the camera records `currentPlan?.modelID`. Restoration requires an existing current plan and an exact matching modelID, as well as the existing `!ignoreCache` condition. Model0 works because this uses explicit equality instead of a truthiness check.

For a different model or no matching cache, the contribution's existing model-bounds/plan-height camera calculation runs. For the same model, existing cached-view restoration stays available. This is a single last-saved camera cache tagged with its model, not a new per-model cache collection.

The existing active-model-switch path, plan clipping/elevation calculations, coordination matrices, camera APIs, animation options and disposal behavior are unchanged. This does not resolve all transform issues from126 or placement issues from102, and it does not add cancellation for overlapping animated navigation or handle external code overwriting camera-controls' saved state.

## Source qualification and acceptance limits

PR264 is open and unmerged at the donor pin. The full plan-manager source and both production patches from closed, unmerged PR263 were read; the alternative also retains an unkeyed camera cache. The current PR264 maintainer comment explicitly says web-ifc-viewer is deprecated and no longer maintained, recommending Components. That status remains; there is no current funding or acceptance claim.

The root contribution guide and code of conduct were read. The complete immutable tree listed no AGENTS.md or nested contribution file. License identity is `97284c8b321ff5aafc9fc05aa2071d92ed86b20d`.

Validation is AI-assisted static control-flow review and complete published-byte readback only. No browser, model, renderer, native program, compiler, tests, fixtures, build, workflow or upstream submission occurred. Runtime camera behavior and upstream acceptance remain unperformed.

Changed 2026-10-05: three production line replacements bind camera-cache restoration to its originating model.
