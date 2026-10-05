# Reset the Habitat cart's closed state when it empties

The current transaction cart permanently sets `_closedManually` after a manual toggle. Its message handler only opens or collapses the cart while that flag is false, so a closed cart stays suppressed even after its previous transactions disappear and a later batch arrives.

This four-line correction clears the flag when an incoming `hbt-tx-bundle` is empty. The existing handler then collapses the empty cart, and a later nonempty batch can open it. Closing a still-populated batch retains the existing behavior.

The empty transition is part of the actual source path: `HabitatProposalCard.buildTransactions` returns no transaction when `changePending` is false; `HabitatCommunity.submitChanges` aggregates those arrays and posts the resulting batch, including an empty array. Proposal input changes and source updates flow through the existing signal-change event. `HabitatEvolution` inherits the same community behavior.

## Integration source

Apply `change.patch` to the documented master source, or use the included module as that pin's exact corrected postimage. Reconcile the hunk with later source instead of replacing a newer full file.

| Source | Identity |
| --- | --- |
| Report | [0xHabitat/habitat-rollup#65](https://github.com/0xHabitat/habitat-rollup/issues/65) |
| Upstream master inspected | `583fd9b565609f3d31f1ca5d2ade4fdf8dd46974` |
| `web/lib/HabitatTransactionCart.js` preimage | `d696f970c71a4f3fe0c1d0d5be73b623c7c90b84` |
| `web/lib/HabitatCommunity.js` | `5ead4d774a14264af459aba2b51a7cbca4dcc92c` |
| `web/lib/HabitatProposalCard.js` | `79007f82a9e7f89120e1696d85e94b497e1e159b` |
| `web/lib/HabitatEvolution.js` | `a029610231bd2c52e59dbf926d87208ff2100eac` |
| Existing signing implementation `web/lib/rollup.js` | `4c0fa090f85ab8bb3bc984e022b85f3aae0376bc` |
| Original Unlicense | `fdddb29aa445bf3d6a5d843d6dd77e10a9f99657`; included unchanged |

Current source-tree inspection found no AGENTS.md or CONTRIBUTING file. The root and library README and license identities match the material already read for the separate PR74 continuation.

## Scope and acceptance

This is a UI state correction, based on actual retained production source. No runtime, browser, wallet connection, RPC, voting transaction, build, test, deployment or upstream submission was performed. Native integration remains unperformed.

Transaction construction, amounts, signing, account selection and message handling are unchanged. This does not force the cart to reopen for every edit to a nonempty batch, or implement the report's larger visual redesign.

The separate [lau-bin PR67](https://github.com/0xHabitat/habitat-rollup/pull/67), inspected at `3595c900596483d08797b25b12bd30d50abb976a`, is an unfinished visual prototype: its new template does not retain the old handler's DOM identifiers. This patch targets current master and must be reconciled if that redesign is integrated; neither that external contribution nor its author attribution was changed.

Contributor comment [953672890](https://github.com/0xHabitat/habitat-rollup/issues/65#issuecomment-953672890) says the historical bounty was already promised to another contributor. Later maintainer comment [1013425664](https://github.com/0xHabitat/habitat-rollup/issues/72#issuecomment-1013425664) paused reassessment of Habitat bounties. No redesign completion, current funding, maintainer acceptance or payment is claimed.
