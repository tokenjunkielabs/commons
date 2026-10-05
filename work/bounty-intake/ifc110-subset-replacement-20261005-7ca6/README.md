# Keep replaced IFC subset membership consistent

This maintenance patch clears the stored ID set when `createSubset({ removePrevious: true, ... })` replaces the existing subset geometry. It addresses a selection correctness gap found while inspecting [ThatOpen/web-ifc-three issue 110](https://github.com/ThatOpen/web-ifc-three/issues/110); it does not complete that issue's broader performance request.

The upstream README explicitly marks this library deprecated and directs new development to [IFC.js Components](https://github.com/ifcjs/components). This packet is for an existing legacy deployment or source integrator. No current bounty funding, award, upstream acceptance or payment is established.

## Source and integration

The full production postimage and `change.patch` target current upstream main commit `f58bfa92c4e27d257bd0aa37da841b48334c7420`.

| Source | Immutable blob |
| --- | --- |
| `web-ifc-three/src/IFC/components/subsets/SubsetCreator.ts` before this change | `1d5a915b8fe4a0ae6261cb351f346ee15a4fb2cf` |
| `web-ifc-three/src/IFC/components/subsets/SubsetManager.ts` caller | `3cbd5306f1b130a1207673ad3061015bb433e549` |
| `web-ifc-three/src/IFC/BaseDefinitions.ts` public configuration | `69928d1a3ede9e82c0adff7893a96a9668a2ffa3` |
| `LICENSE.md` | `97284c8b321ff5aafc9fc05aa2071d92ed86b20d` |

Apply the one-line patch to the named production path on that pin. For a newer source tree, compose only the membership reset into its replacement branch; do not overwrite the newer file with this full historical postimage. The bundled MIT license preserves IFC.js's copyright and permission notice.

Contributor `ryanngit`'s separate [PR 202](https://github.com/ThatOpen/web-ifc-three/pull/202), head `cfd59c0128d8bc6d6bf8268b38d48c2af84bc09d`, groups requested indices by material. Its complete SubsetCreator source (`b7a0b706c3d4ee9fc8606364d4f4d1db29e0bce2`) has the same unchanged replacement branch, so this reset composes with that optimization. The packet does not contain or claim that contributor's optimization, and neither external branch was modified.

## Source reasoning

`SubsetManager.createSubset` forwards the configuration directly. `SubsetCreator.filterIndices` previously emptied the geometry index and reset material groups on replacement, but retained the old ID set. `createSubset` then added the replacement IDs into that existing set.

For distinct selections A and B, replacing A with B therefore left membership A union B while geometry held B. The append branch filters out IDs already in that set, so appending A could skip geometry that was no longer present. The removal path also converts that set back into a replacement request and could reconstruct discarded IDs.

The reset makes replacement membership follow the newly requested IDs. It occurs in the same existing branch that discards previous geometry, before `createSubset` records the replacement IDs. Appending without replacement retains its existing duplicate filtering.

`SubsetManager.removeFromSubset` first removes its requested IDs and builds `ids: Array.from(previousIDs)` before invoking `createSubset`; clearing the retained Set inside the later call does not erase that already-created array. Empty replacements similarly leave empty membership. Material groups, index construction, custom subset keys, BVH calls and mesh parenting are unchanged.

## Acceptance limits

This is source delivery with static caller and state-transition reasoning only. The executor is offline. No TypeScript compilation, suite, model load, rendering, selection interaction, performance measurement, native probe or workflow was performed. The patch was checked as text against the complete pinned preimage and full published files were read back.

Runtime integration remains to be exercised in an existing authorized environment: replacement followed by append, replacement followed by removal, empty replacement, and the existing original/custom-material and BVH paths. These are pending acceptance boundaries, not a new fixture or an assertion of a passing run. Existing broader ID validation, failure recovery and performance behavior are outside this one-line change.
