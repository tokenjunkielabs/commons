# Effector #91: retain intermediate nodes in the graph example

Canonical issue: https://github.com/effector/effector/issues/91
Existing contribution: https://github.com/effector/effector/pull/1334

This packet is a two-line documentation follow-up to landeqiming666's existing graph-link contribution at `63c8326c386fd5079f0bbd68c5899e6032c41d05`. The issue's external assignee remains zerobias. Original contribution and Zero Bias MIT attribution are retained; no upstream or payment-platform action is included.

## Concrete example gap

The English and Russian `includeLinks: true` examples create a node map for only `unit` declarations. Their following `link` branch creates edges from owners to `d.id` and from `d.id` to targets, but never inserts that intermediate link node. A consumer using the example's node map cannot resolve the intermediate ID it just placed in those edges.

Both node-insertion guards now accept `unit` or `link`. The same existing insertion records ID, label and kind before the link branch records its edges. The pinned public `Declaration` union gives both variants the fields used by that insertion. The example's label fallback to the ID and its optional kind remain unchanged.

Only these two guards change. All surrounding prose, translations, anchors, imports, edge logic and other examples stay exact. No runtime, public types, graph acquisition, layout or renderer code changes.

## Source custody

The packet contains complete postimages at the original English and Russian paths, the two-hunk `link-nodes.patch`, a precise `source.json` manifest, this guide and the unchanged upstream license.

| File | Before blob | After blob |
| --- | --- | --- |
| English inspect.mdx | 65809433855b0fbe822f644c87f4a2d2f9a95b5f | e436585151c172d8e9c1275bfeade3360b77ae93 |
| Russian inspect.mdx | e3bac500abde074e35a87cf1bc1d61b5385bc158 | f2fc7fd0433d850691cca16059515706850e3ed0 |

The changes target the existing PR head and must be reconciled with any later upstream edits. They do not replace the external contribution or broader visualization proposal #1320.

## Evidence and limits

Complete current issue and PR discussions, all PR patches, both pinned documents and the full public declaration types were read. Each candidate is one exact substitution; reversing it reconstructs the corresponding complete preimage. The patch's context and removed/added lines match those source bytes. No example execution, typecheck, documentation build, tests, fixture, browser renderer, workflow or native process occurred.

This correction records each observed link declaration in the example's node map. It does not establish that every referenced owner or target has already been observed, replay historical nodes, add factory/region nodes, collect `graph.next` edges, prove graph completeness, or deliver a visualization UI. Existing subscription and runtime behavior remains as defined by PR1334.

The issue remains open and assigned to zerobias; the external PR retains landeqiming666's authorship. Own-PR and Commons packet searches returned no matching items, with query application unverified. Historical advertised funding is separate from current eligibility, allocation, acceptance and payout.
