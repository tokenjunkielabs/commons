# Temporal resolve: size a replacement camera pass

## Change and attribution

This packet continues [0beqz's external temporal-resolving PR 241](https://github.com/gkjohnson/three-gpu-pathtracer/pull/241), pinned to head `fc044fd7eccb9d4c8795a0991ba34d21500309de`. The original temporal resolve implementation, demos and prior rendering improvements belong to that contributor, with the project author's reviews and referenced shader credit retained in the original PR.

The additional correction is one **+4/-2** hunk in `src/temporal-resolve/TemporalResolve.js`. It captures whether the camera changed before replacing the pass, then includes that flag in the existing resize condition. A replacement pass therefore receives the path tracer target's current width and height even when those dimensions have not changed since the preceding frame.

The package includes the complete modified class, a focused unified diff, this guide and the unchanged original MIT license. It composes with the pinned external contribution; it is not a standalone replacement for all of PR 241.

## Source-grounded failure path

The complete original class establishes this sequence:

1. `update()` compares the current path-tracer camera with `activeCamera`.
2. If the camera differs, `initNewCamera()` replaces `temporalResolvePass` with a new instance and updates the camera and texture references.
3. The new pass's constructor sizes its render/depth/velocity targets and history framebuffers from the browser window.
4. The later resize check compares the path tracer target's dimensions only with `lastSize`, which still describes the previous pass's accepted size.
5. If the path tracer target dimensions are unchanged, that condition is false. When those dimensions differ from the window, the replacement pass remains at the wrong size.

Capturing `cameraChanged` before replacement is necessary because `initNewCamera()` updates `activeCamera`. The patch reuses the existing `initNewSize(width, height)` path after replacement. That method updates the saved size, output target and current temporal pass together; the pass's existing `setSize` method updates its render target, depth target, velocity target and history framebuffers.

The unchanged-camera cases retain their original decisions: a target-size change resizes, and an unchanged target size does not. A camera replacement now enters that same resize path once, including when a size change happens in the same update. This is a control-flow and dimension-binding correction, not a measured rendering or performance result.

## Evidence and original issue context

[Issue 60](https://github.com/gkjohnson/three-gpu-pathtracer/issues/60) requests investigation of temporal reprojection for sample retention. Its complete ten-comment chronology includes a historical June 2022 USD 500 offer and the owner's July 2022 note that 0beqz was already working on it. That is not current funding or assignment authority for this packet. The separate USD 1,000 offer mentioned for a different Three.js issue is not combined with this issue's historical amount.

The external PR was open and unmerged at the same head on a fresh read, with 22 discussion comments and 18 inline review comments. Both complete comment collections were read. They discuss prior resizing and tiling work, as well as unresolved background flicker, disocclusion and ghosting behavior. This correction does not claim to resolve those visual reports or complete issue 60.

All 12 changed-path records were retained. The three complete implementation modules used for this analysis were read; both demo patches were also read and show calls to `temporalResolve.update()`. No video, screenshot, live demo or complete demo source was inspected, so no visual comparison or specific demonstrated camera-switch result is asserted.

| Source | Exact identity |
| --- | --- |
| External PR head | `fc044fd7eccb9d4c8795a0991ba34d21500309de` |
| Head's immediate parent | `e0a9a0a3f65e925c9f5437bd1ef8bab7639ae3b9` |
| Complete source tree | `72611196f15a3c526e8821df2917ee2cdf367034` |
| Original TemporalResolve class, 3,685 UTF-8 bytes | `eb575b1205c22a61b24c451cde327e953583bac3` |
| Modified class, 3,820 UTF-8 bytes | `d39ea2558a40cf19d22d32fe89fe86472c35d723` |
| TemporalResolvePass | `a5b67e589f8632e2d8f40686804aeffc7323e03a` |
| VelocityPass | `c798a19468f612e2ff44623153718397c547d64b` |
| README | `f0a92adadf8cfe1753e6ed09faa4040694fe2aef` |
| Contribution guide | `3fa9c0d726cbf48d046d7fc311dd989d16b68878` |
| Original MIT license | `950920d1ed4a3e831659b71933311725b40e1787` |
| Package metadata | `8af8c2226dcd84b871450e98eca64e3e7028a723` |

The README's PathTracingRenderer camera/target/size documentation and complete TemporalResolve section were read; the rest of its 26,293-character API catalog was not fully reviewed. The package identifies this source as version 0.0.6, with different declared development and peer Three.js ranges; no dependency installation or deployed version was observed. The correction uses only the existing source methods and fields, with no new dependency API.

Primary source links:

- [Pinned TemporalResolve class](https://github.com/gkjohnson/three-gpu-pathtracer/blob/fc044fd7eccb9d4c8795a0991ba34d21500309de/src/temporal-resolve/TemporalResolve.js)
- [Pinned pass and its sizing path](https://github.com/gkjohnson/three-gpu-pathtracer/blob/fc044fd7eccb9d4c8795a0991ba34d21500309de/src/temporal-resolve/passes/TemporalResolvePass.js)
- [Pinned velocity pass](https://github.com/gkjohnson/three-gpu-pathtracer/blob/fc044fd7eccb9d4c8795a0991ba34d21500309de/src/temporal-resolve/passes/VelocityPass.js)
- [Pinned README](https://github.com/gkjohnson/three-gpu-pathtracer/blob/fc044fd7eccb9d4c8795a0991ba34d21500309de/README.md)
- [Pinned contribution guide](https://github.com/gkjohnson/three-gpu-pathtracer/blob/fc044fd7eccb9d4c8795a0991ba34d21500309de/CONTRIBUTING.md)

## Validation and limits

The actual serialized `camera-resize.patch` was parsed and applied to the complete retained preimage. Its path, hunk locations/counts and all context/removal rows matched exactly; the resulting full text matched the modified class and its independently calculated Git blob identity. The original UTF-8 byte-order mark, tabs, line endings and every byte outside the replacement block are preserved.

No application, GPU, WebGL context, renderer, browser, model, screenshot, video, dependency installation, test suite or workflow was run. This packet makes no observed image-quality, frame-time, memory-use, browser compatibility or whole-feature claim. It does not change temporal blending, shaders, render-state restoration, resource disposal or camera-specific parameter persistence.

The narrow Commons PR query returned four unrelated-title records; it was not treated as proof that no related work exists. The exact filename query returned zero records with `incomplete_results: true`, which is likewise not exhaustive. The bounded public Slack query returned no rendered matches and provider end, without independently proving query application.

## Contribution boundaries and license

The full 117-entry recursive tree was untruncated and contained the root contribution guide and license, with no AGENTS file or nested contribution/license file. The complete contribution guide and license were read. The guide asks for focused logic changes, explanatory comments, discussion before upstream contributions and new commits when responding to review. This packet uses a small explanatory source comment and does not submit or modify an upstream contribution.

The original MIT license, copyright 2021 Garrett Johnson, is included unchanged. 0beqz retains credit for the original temporal-resolving implementation. This Commons publication is not upstream approval, issue completion, a bounty claim or payment evidence.
