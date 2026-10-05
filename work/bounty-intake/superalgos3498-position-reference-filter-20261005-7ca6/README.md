# Select incoming Position votes or contribution claims

This is an attributed, source-only continuation of [Superalgos issue #3498](https://github.com/Superalgos/Superalgos/issues/3498). The issue's maintainer clarification specifically distinguishes votes from claims referencing a Position. The current generic incoming-reference action highlights both together.

## Delivered source behavior

Position now has **Highlight Weight Votes** and **Highlight Contribution Claims** menu choices. Both reuse the existing Highlight Referencing Nodes action, menu dispatch, existing highlight icon assets, and the exact Governance node types already declared in the application schemas.

The Visual-Scripting action switch forwards the menu's existing relatedNodeType and relatedNodeProject fields. ReferenceChildren optionally selects children with that exact type and project. An absent type remains the all-reference selection: the dispatcher supplies the action project even for the existing generic icon, so the implementation explicitly ignores that default project unless a type was supplied.

Before changing selection, the helper clears the exact UI objects that it previously highlighted. It decides whether the same filter was selected before resetting state. Selecting the same filter toggles it off; selecting a different filter replaces it; selecting the generic action after a typed selection switches to all incoming references. A group with no matching live reference objects clears the old selection and shows a type-specific empty message. The number in the information message is the number of matching reference nodes, not unique users, votes, voting power, or accepted claims.

The stored objects are UI instances, not just nodes whose payload could later point to a replacement. Finalized UI objects have undefined payloads and are skipped during cleanup. Existing generic highlight state without a stored list uses the original current-reference cleanup behavior. The helper retains the current unCollapseParent, drawReferenceLine, and highlight calls; no graph edge, saved governance configuration, reward distribution, ballot, claim, wallet, identity, or token balance is changed.

Only Position's two menu choices are exposed in this packet. Other governance destination schemas and other kinds of references are unchanged. The new English labels use the menu's established fallback when no translation key is supplied; no translations are claimed.

## Exact source custody

Repository: https://github.com/Superalgos/Superalgos
Pinned master: `9f0fb59edd4bae7afa08d06c366e0bcb48103aec`.

| Production path | Original Git blob | Prepared Git blob |
| --- | --- | --- |
| `Projects/Visual-Scripting/UI/Node-Action-Functions/ReferenceChildren.js` | `7bf317ee3f8309477841b0877847011d97d4be79` | `79d5d68efca7f1ed90fd6d34b8fd01fb6ae502a0` |
| `Projects/Visual-Scripting/UI/Node-Action-Functions/NodeActionSwitch.js` | `fb110dad5019660b9a5112bedae5312dbfb04d65` | `68010aecaead29ebc223be477cf009c562b3fbec` |
| `Projects/Governance/Schemas/App-Schema/position.json` | `e2662cc8a28c0dcc9033c14f47ef219eb3da347a` | `acb0305e908e3eb1b342c4064a1d91282d78cbed` |

Complete unchanged dependency leaves retained; the inspected production sections establish:

- Position Weight Vote schema: `a92f3e8e171b2dd8bb6595c9e3157f41f70c2377`, references Position or Position Class.
- Position Contribution Claim schema: `9e5100fdcf6b8dcc7b80e0a3ea6ef82fd7a69121`, references Position.
- CircularMenuItem: `616649b89b1c06d329b1862f0b745aa596b8d11a`, forwards relatedUiObject / relatedUiObjectProject and retains the label fallback.
- UiObjectConstructor: `a636a723e7565ab97fad02079de619d5fc2c2303`, combines schema menu items with the generic incoming-reference icon.
- UiObject: `51280e4224ff8313496e0992ee77851750281014`, initializes the highlight flag false and clears payload on finalization.

The three complete prepared production files retain their original paths inside this packet. The companion position-reference-filter.patch describes only those files against the pinned source. Source edits and postimage identities were checked directly; no application function was executed to establish behavior. NOTICE records the modifications and upstream attribution; LICENSE is copied verbatim from blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`.

## Original request and remaining conditions

Both issue comments were read. Comment [1221265994](https://github.com/Superalgos/Superalgos/issues/3498#issuecomment-1221265994) describes the mixed Position weight-vote and contribution-claim references; [1671909902](https://github.com/Superalgos/Superalgos/issues/3498#issuecomment-1671909902) offers a historical token bounty for that request. No current award, payment eligibility, upstream acceptance, or whole-issue completion is inferred.

The bounded issue-number PR search and exact public activity search returned no matching contribution. These are query observations, not a complete repository or ownership census. Current source and the existing application schema establish this specific remaining behavior.

The complete root CONTRIBUTING file (`0ce8d8579e92425c231db34514b6de71a6472393`) links to the official contribution page. One attempt to open that page was inaccessible; the route remains held without retry or alternate acquisition. CODEOWNERS (`7bbc500fa12709b26c78c8d1bb9ac8bc4e358fa3`) names the existing Visual-Scripting and Governance project teams. Their attribution and any applicable external submission conditions remain. This Commons packet does not submit or claim the work upstream.

## Validation limits

Static source reasoning, JSON syntax parsing of the actual prepared schema, exact patch/postimage construction, original/prepared Git blob identity, current source preimage checks, and guarded publication readbacks are the evidence for this packet. The state reasoning was independently discussed from the retained source contract; that discussion was not execution.

No tests, fixtures, browser or Superalgos application session, native executor, build, dependency installation, workflow, live graph, governance calculation, token operation, account action, credential retrieval, external message, or upstream mutation was performed. Runtime menu layout, actual highlight rendering and interaction timing remain unperformed. The existing highlight mechanism is shared UI state: this does not add cross-feature ownership or restore an unrelated highlight that another action overwrote. UI teardown and unrelated concurrent highlighters are not newly certified.

Operation: `SUPERALGOS3498-POSITION-REFERENCE-FILTER-20261005-7CA6`.
Stable prepared branch: `work/superalgos3498-position-reference-filter-20261005-7ca6`.
