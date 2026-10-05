# Synfig exported-value reconnection inside nested inline groups

Source-only continuation for [synfig/synfig issue 426](https://github.com/synfig/synfig/issues/426), prepared 2026-10-05. The existing submission reconnects values inside one group level. This continuation visits every reachable cloned inline group canvas, so a layer inside two or more groups reaches the same existing reconnection logic.

This is a Commons integration packet, not an upstream submission, a desktop execution result, an accepted fix or a bounty award. The issue's $100 Bountysource history is not a current funding or payment assurance.

## Exact source and credit

The basis is Mohamed Adham's existing [PR3029](https://github.com/synfig/synfig/pull/3029), still open and unmerged when read, at `7917243610cf25c588e192aedfa53cfd7662d8ce` in `mohamedAdhamc/synfig`. Preserve that contributor's implementation and authorship.

| Input | Original Git blob |
| --- | --- |
| `synfig-studio/src/synfigapp/actions/valuedescexport.cpp` | `8dcf63199f005b51c5354ceb67580217f059f77b` |
| Required unchanged `valuedescexport.h` | `7b89f45120531efd56e74cecef3a30447ad4b7af` |
| `synfig-core/src/synfig/canvas.cpp` | `baf1997d696172e7e6a3566a5a768a3c046172d9` |
| `synfig-core/src/synfig/layer.cpp` | `cf2a65c40982af3ab86d2c2ee70cfd97500fd26f` |
| `synfig-core/src/synfig/layers/layer_pastecanvas.h` | `307d3a3113f94fa08f92f4965dee47c84201a323` |
| `LICENSE` | `f288702d2fa16d3cdf0035b15a9fcbc552cd88e7` |

The source retains its existing copyright notices and GPL version 2-or-later notice; the unchanged repository license accompanies it. The dated modification notice identifies this continuation.

Current upstream master `b385fbb2ce4b02b3fe628ed3f3c7480586a48cb3` has export-action blob `5df0c4a690212bb5300e645766bdce1869686f10`, which still scans only top-level layers. Existing [PR3750](https://github.com/synfig/synfig/pull/3750), bomlinux92-byte at `8976885c7203761b064db625be29513ba117bf28`, changes ValueNode-link recursion rather than group-layer depth; its separate proposal is neither incorporated nor replaced. Both external branches remain untouched.

## What changes

Only the layer-scan block changes behavior. Its local queue starts at the supplied canvas, scans each canvas once, and adds the subcanvas of a Group only when recursive mode is enabled and that subcanvas is inline. The visited set prevents repeated canvas traversal; there is no fixed depth cutoff and this new traversal does not add recursive C++ calls.

The source-defined isolation boundary matters: `Layer::clone` copies inline canvas parameters, whereas non-inline canvas references remain shared. Following a non-inline Group could reconnect values in an original linked document. This continuation deliberately follows only the copied inline subgraph. It does not implement embedding of external/named child canvases from issue416.

It calls the existing `scan_layer` for each reached layer. ValueDescConnect construction, original exported-node lookup, action ordering outside this layer pass, canvas creation, original-canvas false-mode scan, named-child scan, and the separate exported-value scan remain unchanged. Descendant layers are visited breadth first. Inline `Canvas::value_node_list()` delegates to its parent, so recursively calling `scan_canvas` on every inline group would rescan ancestor exports; this implementation traverses layers without doing that.

Static complexity for this added traversal is O((V + E) log(V + 1) + L), with O(V + E) temporary handles in the worst case, where V is visited canvases, E is traversed inline group references and L is their layers. This is reasoning from the source, not a measured speed claim. It does not claim to repair cycles or recursion inside the unchanged ValueNode scanner.

## Integration and remaining acceptance

The complete .cpp postimage and unchanged .h are included under their original paths. `change.patch` applies only to the exact PR3029 source pin above. It is not a patch against current upstream master; a maintainer integrating elsewhere must compose it with the current export-action changes. Do not overwrite a newer complete action with this historical postimage.

Source chronology coverage: all10 issue comments, both PR3029 comments, PR3750's one bot comment, the two relevant submission diffs, current master action and the pinned clone/canvas contracts. Exact issue-number PR search returned3 results (the third was an unrelated renderer PR); own-author PR search returned0. These are bounded observations, not a complete repository census.

No C++ compiler, formatter, automated tests, GUI, save/reopen, undo/redo, rendering, workflow or live document operation ran. The executor remains offline. The [upstream contribution guide](https://synfig-docs-dev.readthedocs.io/en/latest/community/contribution%20guidelines.html) expects coordination and native checks before an upstream submission; those acceptance requirements remain with the upstream integrator. No maintainer was contacted and no upstream branch or PR was written.

Native acceptance remains unperformed for the original issue scenario, a value under multiple inline groups, linked non-inline document isolation, repeated canvas references, ordinary top-level values, and undo/redo plus save/reopen. No tests or fixtures are added to this packet.
