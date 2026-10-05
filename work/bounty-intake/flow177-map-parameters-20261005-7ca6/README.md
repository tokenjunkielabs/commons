# Preserve Map parameter validation in flow-runtime PR308

Source target: [gajus/flow-runtime issue177](https://github.com/gajus/flow-runtime/issues/177). Existing contribution: [PR308 by landeqiming666](https://github.com/gajus/flow-runtime/pull/308).

## Problem and resulting behavior

PR308 changes class-property annotations for global Map, Date, Promise and Set into constructor-valued runtime references. For Map, a constructor supplied by Babel's runtime/polyfill can differ from the native constructor registered inside flow-runtime.

At that exact source, TypeContext.ref looks up a constructor by identity. If it is unregistered, it constructs GenericType. GenericType.errors and GenericType.accepts check only whether the input is an instance of that constructor; they do not validate the supplied key and value types. TypeParameterApplication forwards those parameters, but the generic implementation ignores them. Consequently, an instance may satisfy the class check even when its entries violate the declared Map<K,V> annotation.

This correction removes only Map from GLOBAL_TYPE_VALUE_REFS. A global Map annotation consequently retains the existing named Map reference, which resolves to the registered MapType and validates both entry keys and values. PR308's already-added Map predicate continues to recognize native instances and values with the existing Map brand. The conditional guarantee is entry validation for values accepted by that predicate; this packet does not strengthen its brand check or claim universal polyfill compatibility.

The whitelist is reached only in the converter's unresolved-global branch. Local type aliases, type parameters and other resolved entities take separate branches and remain byte-identical. Date, Promise and Set remain on the existing value-reference path. No TypeContext, GenericType, registration, predicate, transformer visitor or generated fixture is modified.

## Exact source basis and attribution

| Item | Immutable identity |
| --- | --- |
| External PR308 head | ad31c52c9649039bb7a67894dda417d9eeecf8fa |
| PR308 recorded upstream base | a9b7e1da4a655be52a4eb8949644a257e1f75f33 |
| Original convert.js | 56639b7aba9a999328c3de699f4bd139d54a3169 |
| TypeContext.js | 443ce3baca06fbd3cfdd5ba27c9e5c3d0a26830e |
| GenericType.js | 9c4f6708e5d5f5f1ef1463028c96d43d23b212bd |
| TypeParameterApplication.js | 68bee645d928831bb826061d9c9e50297fa5e55a |
| registerBuiltins.js | 122e3217aa07a9a02887b5ae5ba961956f8425f0 |
| Existing PR308 Map predicate | 5209fcee08990c239c2a2d3af609931ea66c6c85 |
| Upstream MIT license | dc87e124ecd62968c037cb8f40c229478c40db2f |

All listed source files were retained completely at the PR308 pin before reading the relevant functions. The separate production patches were also read for [PR286 by dicnunz](https://github.com/gajus/flow-runtime/pull/286), [PR289 by selimeneserd](https://github.com/gajus/flow-runtime/pull/289), and [PR298 by ncthuc2004](https://github.com/gajus/flow-runtime/pull/298). At observation, 286,289 and308 were open/unmerged;298 was closed/unmerged. Their compiler and compatibility contributions remain credited and unchanged upstream. PR308's one conversation comment was its author's follow-up; no inline review comments were reported.

The complete issue and all three comments establish the historical $50 IssueHunt funding, including [comment514631735](https://github.com/gajus/flow-runtime/issues/177#issuecomment-514631735), and the platform submission condition. No new award, escrow, acceptance or payment was verified. An exact public ownership search returned zero results; a current all-state upstream PR search for author woahwhattheheck also returned zero. These bounded observations are not universal absence proofs.

## Packet and static verification

- source/packages/babel-plugin-flow-runtime/src/convert.js is the complete production postimage.
- preserve-map-parameters.patch is a single-hunk unified patch against the exact PR308 file: two added lines and one removed line.
- LICENSE.md preserves the upstream MIT notice and 2017 codemix.com copyright.
- This README records the source dependency and validation limits.

The serialized patch was independently applied as a text transformation, checking every context and removed line, and reconstructed the complete postimage exactly. Full Git blob identities are recorded by the delivery publication and checked during immutable and current-main readbacks.

No Babel transform, runtime assertion, native process, test, fixture, build, workflow or package installation was run. The source uses Flow syntax, so no ordinary JavaScript parse result is claimed. Existing PR308 fixture expectations for a constructor-valued Map reference may require reconciliation by the upstream integrator; they were not inspected or changed here. This packet establishes the narrow source correction and its static call-chain rationale, not completion of the entire issue or proof that every Babel/plugin ordering is covered.

## Integration boundary

Apply this patch only to the recorded PR308 source or a successor whose exact relevant source has been reconciled. Its named Map route relies on the existing PR308 runtime predicate. Do not drop it onto an unrelated upstream version while assuming the same behavior.

The observed upstream repository grants pull access but not push access to this connection. Commons is the authorized source-delivery route. No upstream branch, PR, issue comment, maintainer contact or IssueHunt submission was created. Original external contribution and acceptance custody remain intact.