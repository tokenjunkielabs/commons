# Habitat PR74: load wallet libraries when connecting

This continuation fixes an import-time regression in biendeveloper's [WalletConnect contribution](https://github.com/0xHabitat/habitat-rollup/pull/74). It is an integration packet for that contribution, not a complete WalletConnect migration.

The contribution adds Web3Modal and WalletConnect scripts to `web/app/index.html`, then reads their globals immediately when `web/lib/utils.js` is imported. The same utility module is imported by the block explorer, whose entry page does not load those scripts. Accessing `window.Web3Modal.default` therefore throws before the explorer's own rendering setup can run when that global is absent.

The corrected module initializes the existing cached Web3Modal instance only when `getSigner` needs a wallet connection. Read-only utility imports no longer depend on those wallet globals. An explicit wallet request on a page without the libraries rejects with a clear error through the existing async call path. The app keeps the original provider options and successful-instance cache. Existing signer reuse, network checks, provider wrapping and authorization behavior are unchanged.

## Source and application

Apply `change.patch` to the documented PR head, or use `web/lib/utils.js` as its exact corrected postimage. Reconcile the patch with newer source; do not overwrite a newer module with this historical full file.

| Source | Identity |
| --- | --- |
| Original issue | [0xHabitat/habitat-rollup#72](https://github.com/0xHabitat/habitat-rollup/issues/72) |
| Contributor | biendeveloper; original PR74 remains untouched |
| PR74 head | `c54f252837ccf03439434521524303a32fd1646f` |
| PR74 base observed | `28af3b4bc4436ba45ddda35aa2b8fd7eb6c8dc9d` |
| Utility preimage | `c9e8799eb7b67868387ff9acfd4b36983a4ffe0e` |
| App entry | `fbe56b641739af9384fa167e08cb1c507dffc80e` |
| Explorer entry | `bfb567ba8dd6580c1ab2fff699c002f46365296a` |
| Explorer direct importer | `b8ca3cb8419f9c7888ebdb0aaff6b5a2226f40c6` |
| Explorer shared importer | `b1998a81023d7052d76fdfbe5f4b1ca91f3fb3bb` |
| Shared page bootstrap | `b59fe2c14e9b53619e5761e8c37bfe1873bc0363` |
| Navigation importer/caller | `8a14f6d7e01e7685b511f9a5d5aca5b94cbab1fa` |
| Original Unlicense | `fdddb29aa445bf3d6a5d843d6dd77e10a9f99657`; included unchanged |

The complete source tree and governing README material were inspected. No AGENTS.md or CONTRIBUTING file appeared in that tree.

## Acceptance limits

This is static source work. No JavaScript runtime, browser, wallet connection, RPC call, build, test, deployment or upstream submission was performed. The actual import chain and exact source text establish the failure condition; browser integration remains unperformed.

This does not supply wallet scripts to every page, add an injected-wallet fallback, upgrade the old WalletConnect packages, replace the contributor's Infura configuration, or change connection/disconnection lifecycle. A wallet action on a page that lacks its libraries still fails explicitly. External package/service availability and current mobile-wallet behavior were not established. The app entry's existing operational notice is untouched.

The issue's 1,000 DAI offer is historical. Maintainer comment [1013425664](https://github.com/0xHabitat/habitat-rollup/issues/72#issuecomment-1013425664) paused and deferred reassessment of these bounties on January 14, 2022. No current funding, bounty completion, maintainer acceptance or payment is claimed.
