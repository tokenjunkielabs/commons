# Temporal resolve: preserve size and weight settings across cameras

## Change and attribution

This packet continues [0beqz's external temporal-resolving PR 241](https://github.com/gkjohnson/three-gpu-pathtracer/pull/241), pinned to head `fc044fd7eccb9d4c8795a0991ba34d21500309de`. The original temporal resolve implementation, demos and prior rendering improvements belong to that contributor, with the project author's reviews and referenced shader credit retained in the original PR.

The cumulative correction is one **+6/-2** hunk in `src/temporal-resolve/TemporalResolve.js`. The initial [camera-sizing correction in Commons 31630](https://github.com/woahwhattheheck/commons/pull/31630) captures whether the camera changed before replacing the pass, then includes that flag in the existing resize condition. A replacement pass receives the path tracer target's current width and height even when those dimensions have not changed since the preceding frame.

The follow-through adds **two source lines** to that existing class: capture the currently selected `weightTransform` before replacing the pass and reapply it afterward through its existing setter. This preserves the selected shader setting in the new material while retaining the complete earlier size correction.

The package includes the complete modified class, a focused unified diff, this guide and the unchanged original MIT license. It composes with the pinned external contribution; it is not a standalone replacement for all of PR 241.

## Source-grounded failure paths

### Replacement-pass sizing

The complete original class establishes this sequence:

1. `update()` compares the current path-tracer camera with `activeCamera`.
2. If the camera differs, `initNewCamera()` replaces `temporalResolvePass` with a new instance and updates the camera and texture references.
3. The new pass's constructor sizes its render/depth/velocity targets and history framebuffers from the browser window.
4. The later resize check compares the path tracer target's dimensions only with `lastSize`, which still describes the previous pass's accepted size.
5. If the path tracer target dimensions are unchanged, that condition is false. When those dimensions differ from the window, the replacement pass remains at the wrong size.

Capturing `cameraChanged` before replacement is necessary because `initNewCamera()` updates `activeCamera`. The patch reuses the existing `initNewSize(width, height)` path after replacement. That method updates the saved size, output target and current temporal pass together; the pass's existing `setSize` method updates its render target, depth target, velocity target and history framebuffers.

The unchanged-camera cases retain their original decisions: a target-size change resizes, and an unchanged target size does not. A camera replacement now enters that same resize path once, including when a size change happens in the same update. This is a control-flow and dimension-binding correction, not a measured rendering or performance result.

### Selected weight transform

The complete class defines `weightTransform` with a closure-backed getter and a setter that writes `(1 - value).toFixed(5)` to the current material's `WEIGHT_TRANSFORM` define and marks that material for update. Both retained demo patches contain a GUI control whose change callback assigns this property. The README documents the property as a numeric setting with default zero.

A camera change constructs a fresh `TemporalResolvePass`, whose complete constructor constructs a fresh `TemporalResolveMaterial`. The newly read complete material constructor initializes `WEIGHT_TRANSFORM` to `'1.0'`. The previous class then continued rendering without reapplying the selected property. Its getter still returned the user's saved value, while the new material used the constructor default. The other four public tuning values are refreshed through the existing per-frame uniform assignments; this define was absent from that refresh path.

The additional two lines snapshot the getter before `initNewCamera(camera)` and call the existing setter with that value afterward. They run only in the camera-change branch of `update()`, so an unchanged camera gains no additional setter call. The setter continues to own numeric formatting and the material update flag. Constructor initialization order stays unchanged: its first pass is created before the property descriptor exists. Direct calls to the internal initialization method are outside this update-path correction.

The retained native fragment-shader patch was inspected at the two `WEIGHT_TRANSFORM` consumers in `transformColor` and `undoColorTransform`; the complete shader source was not read. These source bindings establish the setting mismatch and its repair, not an observed contrast, noise, ghosting or image-quality result.

## Evidence and original issue context

[Issue 60](https://github.com/gkjohnson/three-gpu-pathtracer/issues/60) requests investigation of temporal reprojection for sample retention. Its complete ten-comment chronology includes a historical June 2022 USD 500 offer and the owner's July 2022 note that 0beqz was already working on it. That is not current funding or assignment authority for this packet. The separate USD 1,000 offer mentioned for a different Three.js issue is not combined with this issue's historical amount.

The external PR was open and unmerged at the same head on a fresh read, with 22 discussion comments and 18 inline review comments. Both complete comment collections were read. They discuss prior resizing and tiling work, as well as unresolved background flicker, disocclusion and ghosting behavior. This correction does not claim to resolve those visual reports or complete issue 60.

All 12 changed-path records were retained. The three complete implementation modules used for the initial sizing analysis were read; the follow-through also read the complete TemporalResolveMaterial. Both demo patches were read and show calls to `temporalResolve.update()`. No video, screenshot, live demo or complete demo source was inspected, so no visual comparison or specific demonstrated camera-switch result is asserted.

| Source | Exact identity |
| --- | --- |
| External PR head | `fc044fd7eccb9d4c8795a0991ba34d21500309de` |
| Head's immediate parent | `e0a9a0a3f65e925c9f5437bd1ef8bab7639ae3b9` |
| Complete source tree | `72611196f15a3c526e8821df2917ee2cdf367034` |
| Original TemporalResolve class, 3,685 UTF-8 bytes | `eb575b1205c22a61b24c451cde327e953583bac3` |
| Earlier size-corrected class, 3,820 UTF-8 bytes | `d39ea2558a40cf19d22d32fe89fe86472c35d723` |
| Current size-and-weight class, 3,912 UTF-8 bytes | `75595e4234e239cb16a08bc951f93349e897266c` |
| TemporalResolvePass | `a5b67e589f8632e2d8f40686804aeffc7323e03a` |
| TemporalResolveMaterial, complete source read for the follow-through | `e257be71ff513acb5f34be6fdbe8e19374ee5e26` |
| VelocityPass | `c798a19468f612e2ff44623153718397c547d64b` |
| README | `f0a92adadf8cfe1753e6ed09faa4040694fe2aef` |
| Contribution guide | `3fa9c0d726cbf48d046d7fc311dd989d16b68878` |
| Original MIT license | `950920d1ed4a3e831659b71933311725b40e1787` |
| Package metadata | `8af8c2226dcd84b871450e98eca64e3e7028a723` |

The README's PathTracingRenderer camera/target/size documentation and complete TemporalResolve section were read; the rest of its 26,293-character API catalog was not fully reviewed. The package identifies this source as version 0.0.6, with different declared development and peer Three.js ranges; no dependency installation or deployed version was observed. The correction uses only the existing source methods and fields, with no new dependency API.

Primary source links:

- [Pinned TemporalResolve class](https://github.com/gkjohnson/three-gpu-pathtracer/blob/fc044fd7eccb9d4c8795a0991ba34d21500309de/src/temporal-resolve/TemporalResolve.js)
- [Pinned pass and its sizing path](https://github.com/gkjohnson/three-gpu-pathtracer/blob/fc044fd7eccb9d4c8795a0991ba34d21500309de/src/temporal-resolve/passes/TemporalResolvePass.js)
- [Pinned material and its default define](https://github.com/0beqz/three-gpu-pathtracer/blob/fc044fd7eccb9d4c8795a0991ba34d21500309de/src/temporal-resolve/materials/TemporalResolveMaterial.js)
- [Pinned velocity pass](https://github.com/gkjohnson/three-gpu-pathtracer/blob/fc044fd7eccb9d4c8795a0991ba34d21500309de/src/temporal-resolve/passes/VelocityPass.js)
- [Pinned README](https://github.com/gkjohnson/three-gpu-pathtracer/blob/fc044fd7eccb9d4c8795a0991ba34d21500309de/README.md)
- [Pinned contribution guide](https://github.com/gkjohnson/three-gpu-pathtracer/blob/fc044fd7eccb9d4c8795a0991ba34d21500309de/CONTRIBUTING.md)

## Validation and limits

The actual serialized cumulative `camera-resize.patch` was parsed and applied to the complete retained original preimage, covering both the earlier size correction and the two added setting-preservation lines. Its path, hunk locations/counts and all context/removal rows matched exactly; the resulting full text matched the modified class and its independently calculated Git blob identity. The original UTF-8 byte-order mark, tabs, line endings and every byte outside the replacement block are preserved.

No application, GPU, WebGL context, renderer, browser, model, screenshot, video, dependency installation, test suite or workflow was run. This packet makes no observed image-quality, frame-time, memory-use, browser compatibility or whole-feature claim. Shader source, temporal-blending equations, render-state restoration and resource disposal are unchanged. Only the existing `weightTransform` setter is reapplied when `update()` replaces the camera pass.

The narrow Commons PR query returned four unrelated-title records; it was not treated as proof that no related work exists. The exact filename query returned zero records with `incomplete_results: true`, which is likewise not exhaustive. The bounded public Slack query returned no rendered matches and provider end, without independently proving query application. For the follow-through, a fresh native PR read retained the same open/unmerged `fc044fd7` head and comment counts; an exact Commons PR query for `weightTransform` returned zero records with `incomplete_results: false`. That bounded result is not a global absence claim.

## Contribution boundaries and license

The full 117-entry recursive tree was untruncated and contained the root contribution guide and license, with no AGENTS file or nested contribution/license file. The complete contribution guide and license were read. The guide asks for focused logic changes, explanatory comments, discussion before upstream contributions and new commits when responding to review. This packet uses a small explanatory source comment and does not submit or modify an upstream contribution.

The original MIT license, copyright 2021 Garrett Johnson, is included unchanged. 0beqz retains credit for the original temporal-resolving implementation. This Commons publication is not upstream approval, issue completion, a bounty claim or payment evidence.
