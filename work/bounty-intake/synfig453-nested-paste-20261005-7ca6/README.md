# Synfig nested skeleton paste continuation

Copying a group containing a skeleton does not populate the bone-remapping table in the inspected [Synfig PR3702](https://github.com/synfig/synfig/pull/3702). Its paste loop records only each clipboard root, while the special-node collector recognizes only skeleton and duplicate layers. For a group-only selection, the inner skeleton is therefore absent from that collector's inputs.

This packet extends that existing implementation by collecting the ordered source and clone descendants with the same `traverse_layers` policy already used by `LayerDuplicate::prepare`. Both lists must have equal size before pairing; the resulting entries feed the PR's existing special-node collection and replacement. The whole-paste map and per-root insertion order remain: a repeated source pointer is still assigned by the later processed root. The existing traversal defaults include static and dynamic inline canvases and exclude non-inline canvases.

The change is two hunks, +24/-2: the root-only assignment becomes descendant collection/pairing, and the source header records this modification's date. No other production file changes. A size mismatch logs an error and returns before adding the current cloned root; this is not a new rollback guarantee for earlier actions in the same paste. Foreign exported-value choices, duplicate-index export, special-node lookup, action grouping, selection and the original replacement logic remain as supplied by PR3702.

## Source and credit

Canonical issue: [synfig/synfig453](https://github.com/synfig/synfig/issues/453). Existing implementation author: **locky504**. The original Synfig maintainers retain their source notices. This is a narrow continuation to that external contribution, not a replacement PR or a claim to have independently implemented its skeleton repair.

All implementation comparisons use PR head `242e6528adc353bf054bf572b71d18587da70c4f`, based on `11765ffea272cb64b194e65869ef6e2045e6c5eb`:

| Source | Complete Git blob |
|---|---|
| `synfig-studio/src/gui/actionmanagers/layeractionmanager.cpp` preimage | `a2ba16159820f3704fe80dde3202ab7ef3950f00` |
| `synfig-studio/src/synfigapp/actions/layerduplicate.cpp` existing traversal mechanism | `3b45ebcffdf514d1b70de8880aaa34314d91be8f` |
| `synfig-core/src/synfig/synfig_iterations.cpp` | `b2f17da79c195ffad953cd67ae9b224068c868ef` |
| `synfig-core/src/synfig/synfig_iterations.h` | `d89350ad53e03b756ec1f306b8b3ee1e2796d312` |

The proposed complete `layeractionmanager.cpp` is `7f6b5172d4aa6566dc42f2b2bc56776cc0ecb06b`, 29261 UTF-8 bytes. `change.patch` applies to the named preimage. `LICENSE` preserves the repository's complete GPL text, blob `f288702d2fa16d3cdf0035b15a9fcbc552cd88e7`; existing source notices are retained. The mechanism is credited to the existing Synfig duplicate action and PR3702.

## Validation and remaining work

Complete source was retained before editing. An independent application of the serialized unified patch reproduced the complete postimage, and its computed Git blob matched the publication blob. Source comparison confirmed that only the two described hunks changed.

No C++ compilation, desktop copy/paste, undo/redo, animation, build, tests or native execution was performed. In particular, this packet does not independently establish every existing skeleton, exported-node or cross-canvas behavior in PR3702. The next legitimate runtime check is a group-only copy containing a nested skeleton, including repeated paste and undo/redo, on the actual Synfig application. That work is not claimed here.

The upstream contribution guidelines were read; their manual/automated validation and external coordination steps have not been performed for this internal source packet. No upstream branch, PR, comment, issue assignment, account or payment was changed.

## Funding and delivery scope

Reporter/backer zozorg's [2017 $50 comment](https://github.com/synfig/synfig/issues/453#issuecomment-343231717) and [additional $10 comment](https://github.com/synfig/synfig/issues/453#issuecomment-345612967) establish historical funding. PR3702's contributor [asked about an alternative payout route](https://github.com/synfig/synfig/pull/3702#issuecomment-4006594637); no response resolving that question appeared in the inspected comments. A contributor's platform-shutdown statement is not independently verified here.

The issue and existing PR were open in the qualification observation. This source delivery is not sponsor acceptance, a complete fix for issue453, a newly qualified current $60 opportunity, or an award/payment claim. The external author/carrier and maintainer acceptance process remain intact.
