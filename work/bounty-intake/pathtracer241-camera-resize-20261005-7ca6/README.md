# Temporal resolve: preserve camera state, restore temporary state and release owned resources

## Change and attribution

This packet continues [0beqz's external temporal-resolving PR 241](https://github.com/gkjohnson/three-gpu-pathtracer/pull/241), pinned to head `fc044fd7eccb9d4c8795a0991ba34d21500309de`. The original temporal resolve implementation, demos and prior rendering improvements belong to that contributor, with the project author's reviews and referenced shader credit retained in the original PR.

The cumulative correction is **+138/-69 across 11 hunks in three production files**. It retains the earlier **+6/-2** camera-size and weight-setting correction and **+36/-5** resource-ownership continuation. The new temporary-state continuation is **+102/-68 across 9 hunks** relative to [Commons 31646](https://github.com/woahwhattheheck/commons/pull/31646); much of its controller delta is the indentation required by one enclosing try/finally. The initial [camera-sizing correction in Commons 31630](https://github.com/woahwhattheheck/commons/pull/31630) captures whether the camera changed before replacing the pass, then includes that flag in the existing resize condition. A replacement pass receives the path tracer target's current width and height even when those dimensions have not changed since the preceding frame.

The [weight-setting correction in Commons 31639](https://github.com/woahwhattheheck/commons/pull/31639) added **two source lines** to that existing class: capture the currently selected `weightTransform` before replacing the pass and reapply it afterward through its existing setter. This preserves the selected shader setting in the new material while retaining the complete earlier size correction. Both changes remain intact.

The resource continuation constructs and binds a replacement temporal pass before retiring its predecessor, extends the pass's disposal to its depth and velocity resources, and tracks generated velocity materials so their private history textures and materials can be released on replacement or pass retirement.

The package includes all three complete modified implementation files, the cumulative `camera-resize.patch`, this guide and the unchanged original MIT license. The original patch filename is retained for existing consumers; it now covers the controller and both pass files. It composes with the pinned external contribution; it is not a standalone replacement for all of PR 241.

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

## Owned resources and replacement order

### Temporal pass ownership

The complete original controller replaces `temporalResolvePass` in `initNewCamera()` without disposing the previous instance. The original pass constructs a render target, depth target, velocity pass, two framebuffer-history textures and its fullscreen material. Its existing `dispose()` releases the main render target, both history textures and fullscreen material, but omits the depth target and velocity pass.

The controller now constructs the replacement in a local variable and binds its borrowed sample texture before changing the active pass and camera fields. It then points the composing material at the replacement target and retires the previous pass if present. Initial construction has no previous pass. If the new pass constructor throws, the controller has not yet replaced its old pass or active-camera fields; this ordering is not a guarantee of cleanup for every allocation or exception inside that constructor.

The pass's disposal now also calls `depthRenderTarget.dispose()` and `velocityPass.dispose()`. These resources were allocated by that pass. The path tracer's input target and sample texture, scene, camera and scene materials are not retired by this code. The earlier camera-size and weight-setting logic remains exact and still runs through the normal update path.

### Generated velocity materials and private bone history

The original velocity pass caches each object's original material and generated velocity material in a `WeakMap`. If the original material changes, a new shader material is constructed and the prior generated material is abandoned. The old `dispose()` releases only the velocity render target, so it cannot enumerate or retire generated materials.

The continuation adds a set containing only the shader materials created by this pass. After a new shader material is successfully constructed and registered, a superseded generated material is retired and removed from the set. Terminal pass disposal retires every remaining tracked generated material, clears the set and replaces the cache with a fresh `WeakMap`. Materials associated with objects removed from the scene remain tracked until pass retirement; this change does not add per-frame removal detection or claim immediate reclamation on scene removal.

Each generated shader material uses the existing `UniformsUtils.clone(VelocityShader.uniforms)` construction. The already retained native new-file shader patch explicitly initializes `prevBoneTexture` to null. The complete velocity source allocates that history texture with `new DataTexture(...)` from a copy of the skeleton's matrix data, and already replaces/disposes a previous history texture when its size changes. The new disposal helper retires that private `prevBoneTexture`, if present, and the generated material itself.

The separate `boneTexture` uniform is assigned directly from the scene object's skeleton. It is borrowed and is not passed to `dispose()`. Original scene materials are likewise absent from the ownership set. The disposal continuation did not alter shader equations, matrix-update arithmetic or live skeleton data. The later restoration continuation changes when end-of-render history updates run after failures, as described below.

### Shared resources remain shared

The depth material is allocated once at module scope and reused by multiple pass instances. It is not disposed when one camera's pass is retired.

The newly read [Three.js r141 FullScreenQuad implementation](https://github.com/mrdoob/three.js/blob/r141/examples/jsm/postprocessing/Pass.js) constructs all quads using the same module-global `_geometry`; its `dispose()` disposes that shared geometry. Per-camera retirement therefore does not call `fsQuad.dispose()`. This ownership observation is tied to the inspected r141 development revision, not a claim that every allowed or deployed dependency version was inspected.

The change does not add an overall `TemporalResolve.dispose()` API or change the shared geometry's owner or lifetime. The separate temporary-state continuation below now addresses the bounded render-exception restoration paths. It establishes explicit retirement of the generated resources listed above; it does not measure GPU memory, garbage collection or performance.

## Temporary scene and renderer state

The three complete Commons 31646 postimages, cumulative patch, guide and unchanged license were read at immutable commit `37e1e4355317345a8ba132575236f642b74cf28e`, with independently calculated blob identities matching all six returned identities. This is a new continuation of the restoration gap explicitly left outside that completed disposal change.

### Caller render target and scoped depth override

The controller's `update()` saved the caller's current renderer target but reached its restoring call only after every camera, matrix, temporal and composing operation returned normally. Those same operations now sit inside one try/finally, whose cleanup calls `setRenderTarget(origRenderTarget)`. Their order and text are unchanged apart from indentation. The intentionally persistent `stableTiles = false`, camera/size updates and all existing tuning assignments remain as before.

Depth rendering formerly installed the shared depth material, changed the background, rendered, then restored the background and assigned a literal null override. A failure could strand the temporary state, and a successful call discarded a pre-existing caller override. The depth scope now captures both original fields before mutation and restores them in finally. The remaining temporal pass body is unchanged.

Restoring a non-null caller override before velocity rendering requires a corresponding velocity scope: otherwise Three.js would use that override instead of the generated velocity materials. Velocity therefore temporarily sets `overrideMaterial = null` during its draw and restores the exact captured override afterward, along with the captured background. This preserves the intended depth-then-generated-velocity rendering path while retaining caller state.

### Exact material records and success-only end-of-render history

The original velocity cleanup traversed the current scene again and looked up each current object's original material in the cache. A partial setup failure could leave earlier objects swapped; a render or history exception could bypass restoration; an object removed or reparented during the call could be missed by the second traversal. Newly encountered objects could also lack the assumed generated uniforms or cache entry.

Setup now creates a Map keyed by each actual object and records its original material and generated material before the first material assignment. A repeated traversal visit to the same object is skipped. The replacement-material disposal and private-history ownership paths remain intact. The complete setup call is inside render's protected try, so cleanup can use all records accumulated before a later setup failure.

After the renderer returns successfully, a flag enables the existing end-of-render velocity matrix and bone-history updates. These updates use the captured generated material. `saveBoneTexture(object, material = object.material)` preserves the original one-argument behavior and lets this recorded-material path avoid depending on a potentially changed `object.material`. Initial allocation/copy of bone history during creation of a new generated material remains in setup; it is not an end-of-render success update.

`unsetVelocityMaterialInScene(updateHistory = true)` keeps the existing no-argument paired-helper behavior. Its history loop is enclosed by a finally that restores every recorded object's original material and clears the Map, without traversing the scene again. Render passes false if setup, target selection, clearing or rendering throws, so no end-of-render history update occurs on those paths. If a history update itself throws after a successful render, material restoration still runs. Scene background and override are restored before that history/cleanup helper is called.

This is restoration of ordinary scene fields and object material references, not transactional rendering. Earlier history writes, cache entries, allocations, matrices and renderer side effects are not rolled back if a later operation throws. Removed objects' generated materials remain owned until the existing pass-retirement path. No custom throwing-property-setter, recursive/reentrant invocation, repeated unpaired setup, renderer-target restoration failure, constructor-allocation cleanup or new overall controller-lifetime guarantee is asserted. The standalone pass target behavior remains unchanged; caller target restoration is provided by `TemporalResolve.update()`.

| Latest production postimage | Git blob | UTF-8 bytes |
| --- | --- | --- |
| `src/temporal-resolve/TemporalResolve.js` | `be983fadfff36b8cd0ec9a079dbbb8f5a458f679` | 4086 |
| `src/temporal-resolve/passes/TemporalResolvePass.js` | `9ab0a50510e18910243c6d3db8d09327b90c637f` | 4307 |
| `src/temporal-resolve/passes/VelocityPass.js` | `2a23ac97aff2a25364be119bf9a69028c8fe00dd` | 5042 |

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
| Prior size-and-weight class, 3,912 UTF-8 bytes | `75595e4234e239cb16a08bc951f93349e897266c` |
| Controller after Commons 31646 camera retirement, 4,049 UTF-8 bytes | `225535c4bbe4fe7abdbbd18dc3df369b67629bf0` |
| Original TemporalResolvePass, 4,124 UTF-8 bytes | `a5b67e589f8632e2d8f40686804aeffc7323e03a` |
| TemporalResolvePass after Commons 31646, 4,191 UTF-8 bytes | `1f802c4ab333a3577d3af007ed2bcc050e8d3b95` |
| TemporalResolveMaterial, complete source read for the follow-through | `e257be71ff513acb5f34be6fdbe8e19374ee5e26` |
| Original VelocityPass, 3,574 UTF-8 bytes | `c798a19468f612e2ff44623153718397c547d64b` |
| VelocityPass after Commons 31646, 4,245 UTF-8 bytes | `36debcdb7bd41295043712efbb93e93855767750` |
| VelocityShader, retained native PR patch and tree identity | `fdef3dfeada0411ce7a889016c2d288b44657b18` |
| Three.js r141 Pass.js, complete newly read source | `c3bf9d9b84ec46afb4cfbe86ec795ffaaf50fc8e` |
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

The actual serialized cumulative `camera-resize.patch` was parsed and applied to all three complete retained original preimages. Its three paths, 11 hunk locations/counts and every context/removal row matched exactly. All three resulting full texts matched the prepared implementation files and their independently calculated Git blob identities. The original UTF-8 byte-order marks, tabs, line endings and every byte outside the changed hunks are preserved. The latest restoration delta is 9 hunks, +102/-68; the cumulative patch is 11 hunks, +138/-69. The three original preimages were recovered by reversing the retained cumulative patch against the complete immutable packet postimages and matched their already documented original blob identities. The actual new serialized patch was then applied to those exact preimages; this is text reconstruction, not application execution or a repeated rendering acceptance check. The controller's protected body matches its preimage after removing one indentation level, the temporal pass body after depth rendering is exact, and the velocity disposal and sizing methods are unchanged.

For the earlier disposal continuation, a second reviewer assessed the supplied exact construction, allocation, ownership and replacement snippets. That review found no established ownership or ordering defect and specifically checked private history textures against the borrowed skeleton texture. It was source reasoning, without a separate dependency-body read or execution.

A separate source review of the literal restoration hunks checked the Map record before mutation, the incomplete-record success flag, depth/velocity override scopes, explicit generated-material history arguments and the history loop's encompassing finally. No concrete ordering defect was identified within the stated ordinary-material, paired-call scope. This was independent source reasoning; no production execution or dependency-body replay was performed.

No application, GPU, WebGL context, renderer, browser, model, screenshot, video, dependency installation, test suite or workflow was run. This packet makes no observed image-quality, frame-time, memory-use, browser compatibility or whole-feature claim. Shader source and temporal-blending equations are unchanged. Resource disposal retains the prior ownership paths; temporary-state restoration changes only the scoped paths described above. The existing `weightTransform` setter is still reapplied when `update()` replaces the camera pass.

The narrow Commons PR query returned four unrelated-title records; it was not treated as proof that no related work exists. The exact filename query returned zero records with `incomplete_results: true`, which is likewise not exhaustive. The bounded public Slack query returned no rendered matches and provider end, without independently proving query application. For the follow-through, a fresh native PR read retained the same open/unmerged `fc044fd7` head and comment counts; an exact Commons PR query for `weightTransform` returned zero records with `incomplete_results: false`. That bounded result is not a global absence claim. The resource continuation's separate exact Commons PR query for `velocityMaterials` also returned zero records with `incomplete_results: false`; its fresh PR read retained the same open/unmerged external head, 22 discussion comments and 18 inline comments.

One resource lookup used the wrong root path, `src/materials/VelocityShader.js`, and received a native HTTP 404. That exact request remains failed and held, with no retry or alternate acquisition. The relevant shader defaults above came from the actual native PR patch already retained before that lookup, at the tree-confirmed path `src/temporal-resolve/materials/VelocityShader.js`. No standalone full shader-file retrieval is claimed for this continuation.

## Contribution boundaries and license

The full 117-entry recursive tree was untruncated and contained the root contribution guide and license, with no AGENTS file or nested contribution/license file. The complete contribution guide and license were read. The guide asks for focused logic changes, explanatory comments, discussion before upstream contributions and new commits when responding to review. This packet uses a small explanatory source comment and does not submit or modify an upstream contribution.

The original MIT license, copyright 2021 Garrett Johnson, is included unchanged. 0beqz retains credit for the original temporal-resolving implementation. This Commons publication is not upstream approval, issue completion, a bounty claim or payment evidence.
