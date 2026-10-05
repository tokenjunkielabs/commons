# Match Habitat PR66's voting controls to its template

This is a narrow continuation over shad-k's [WIP PR66](https://github.com/0xHabitat/habitat-rollup/pull/66), associated with [issue60](https://github.com/0xHabitat/habitat-rollup/issues/60).

The redesigned signal controls intentionally remove their plus/minus buttons, while the binary controls still contain No/Yes buttons. The PR comments out both existing button-handler registrations for every input. Consequently the remaining binary buttons have no handler to select their intended signal. Separately, `renderFlavor('signal')` still dereferences `#add` or `#sub` when shares change, although neither element exists in the new signal template.

The correction restores the existing `CustomButtonHandler` registrations only for the binary input container and removes the obsolete signal-button highlight block. It keeps the existing `change` callback, input-change dispatch, numeric limits, vote calculations and signing path. The signal input and slider remain the redesign's controls.

## Apply to the documented contribution

Apply `change.patch` to the PR head below. The included full module is that pin's corrected postimage, not a replacement for a newer module. In particular, do not apply the deletion of signal-button highlighting to older/current-master templates that still have those buttons.

| Source | Identity |
| --- | --- |
| Original contributor/carrier | shad-k; external PR66 remains untouched |
| PR head | `c5d2361d5317d200fc75ba02c14d6b99008a81c0` |
| PR base observed | `58844130c7b3839f40aa900fd5736fea6fea4ce3` |
| `web/lib/HabitatProposalCard.js` preimage | `e9fa764aecd6593989b6be310e02f0300029ba51` |
| Root README | `679c1c44fe40b68e4825d24adce12f16cb83a590` |
| Library README | `1e05dd60df306604ccdc1c036df87cc660f91e1c` |
| Original Unlicense | `fdddb29aa445bf3d6a5d843d6dd77e10a9f99657`; included unchanged |

The full immutable tree has no AGENTS.md or CONTRIBUTING file. Governing README and license identities match the already-read Habitat material. The production patch is +4/-7 lines.

## Acceptance limits

The exact template, handler registration, callback and rendering source were inspected; no runtime, browser, build, test, wallet/RPC, governance transaction, deployment or upstream submission was performed. Browser integration remains unperformed.

This does not finish the larger visual redesign or change its subtopic layout, sorting, module configuration, external data sources, transaction construction or wallet behavior. Existing handler gesture semantics are retained. This packet is separate from the current-master empty-cart correction and the PR74 wallet-library correction; compose only their relevant hunks against the intended contribution.

The original issue's Gitcoin worker/application history is preserved. A later maintainer [comment1013425664](https://github.com/0xHabitat/habitat-rollup/issues/72#issuecomment-1013425664) paused reassessment of Habitat bounties in January2022. No current reward, broad issue completion, maintainer acceptance or payment is claimed.
