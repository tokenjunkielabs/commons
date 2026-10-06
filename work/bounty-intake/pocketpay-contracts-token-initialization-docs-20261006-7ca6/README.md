# PocketPay Contracts: supply the configured token when initializing

This attributed Commons continuation corrects the current root README's initialization example and its directly contradictory no-token-transfer statement. It changes documentation only. The recipe remains for educational and testnet use; it does not establish production readiness, a successful invocation, or upstream acceptance.

## Current source and concrete mismatch

The donor is [Stellar-PocketPay/pocketpay-contracts](https://github.com/Stellar-PocketPay/pocketpay-contracts) at commit `7988c6efec9a73162ed7d2fffb3b8b6ebd5a7b67`. Original code and documentation credit remain with that project's contributors. The unchanged MIT notice in this packet names copyright 2026 Axionvera.

The complete root README says `initialize(admin)` twice and its invocation supplies only `--admin deployer`. The current contract instead declares `pub fn initialize(env: Env, admin: Address, token: Address)`. It requires admin authorization and stores both addresses during one-time initialization. The contract workspace README already documents all three Rust parameters; the environment parameter is supplied by Soroban rather than shown as a CLI argument.

The current `deposit`, `withdraw`, and `withdraw_lock` implementations load the stored token address and call that token client's `transfer` method. Consequently the root README's statement that it only records internal balances and does not transfer tokens contradicts the current source. Balances are keyed by user within a vault configured with one token address.

| Input | Exact Git blob | UTF-8 bytes |
| --- | --- | ---: |
| `README.md` | `f6a4921cc8d63c0da4ae3b73292df7e6a76cdb4c` | 12438 |
| `contracts/savings_vault/src/lib.rs` | `8829b657f7b101c1e4ba8aaa423ba14cf5652b9e` | 68966 |
| `contracts/savings_vault/README.md` | `0dc76fc316962ac60fb3f8b7e7951d2129908707` | 2807 |
| `CONTRIBUTING.md` | `f540677ba668a8579563d8ed894cf6d35253477a` | 7744 |
| `docs/docs-style-guide.md` | `e1786097b76c85bb6d4e173a3969eecae4b33095` | 6093 |
| `docs/placeholders.md` | `58a016dccac1c8154ebdebd4475a2a665797e0ef` | 2847 |
| `LICENSE` | `0eaf357ba6c68fab6ed3cf20e0ab6a31f2854769` | 1066 |

Complete source texts were retained and independently matched to their native Git blob identities. The recursive tree returned 2031 entries with `truncated: false`; no AGENTS file was present in that returned tree. This is observed source custody, not a claim about all branches or future instructions.

## Change

The four README hunks total **+8/-5**:

- Update the two initialization references to include the token argument.
- Add the required `--token TOKEN_CONTRACT_ID_PLACEHOLDER` to the existing testnet initialization command, with an explanation of the vault, signing-admin, and configured-token placeholders.
- Use the canonical `CONTRACT_ID_PLACEHOLDER` and `ADMIN_PUBLIC_KEY` names in that edited command. The style guide permits the existing generic `deployer` CLI identity; the token placeholder is explicitly synthetic because the canonical table has no token-address entry.
- Replace the obsolete no-transfer limitation with the actual one-configured-token boundary.

`README.postimage.md` is the complete modified upstream root README: 12875 UTF-8 bytes, Git blob `76fac7795e1b0d84ec69958a56cd9516c33cf3cc`. Its relative links are intended for the donor repository root. `change.patch` applies these same documentation changes to that pinned root README; it does not install or invoke a contract. All unrelated README bytes, including the pre-existing testnet warning and verification instructions, are preserved.

The inspected `scripts/deploy-testnet.sh` (`cdf6e3ed2dcf31e664cac2d69055f3ebd32603b2`, 1313 bytes) only builds and deploys. It never calls initialization, so this packet makes no script change and adds no initialization gate.

## Chronology, ownership, and held acquisition

The bounded current open-PR response returned seven headers. Other-seat carriers for issue 439/PR 575 and issue 524/PR 574 remain separate. The independently acquired file list for GBOYEE's open PR 523, “Document repeated lock behaviour,” returned only `contracts/savings_vault/src/lib.rs`. Its source changes are not copied or adopted here. The root README's separate lock-behaviour limitation is deliberately outside this correction; this packet is not a comprehensive documentation audit.

A separate REST PR search for `repo:Stellar-PocketPay/pocketpay-contracts is:pr "initialize" "token"` returned a native secondary-rate-limit HTTP 403 at the observed 2026-10-06 02:45:01 UTC boundary. That exact query is held, was not retried, and supplied no result rows or ownership conclusion. No alternate query was used to recover it. Later ordinary reads of the required style and placeholder documents are separate source acquisitions, not proof of provider-wide recovery. No complete carrier-history or absence-of-owner claim is made.

## Validation and practical limits

Validation here consists of static comparison of the complete current README, contract signatures and token-call sites, the contract README, and the applicable contributor/style/placeholder instructions. The packet preserves full source identities and a focused patch. Commons publication uses pinned file identities and ordinary guarded branch, PR, merge, and full immutable-content readbacks; those checks establish the published artifact bytes, not contract or CLI behavior.

No shell, CLI, build, formatting command, test, fixture, emulator, wallet, RPC, deployment, initialization, token transfer, account, payment, upstream issue, or upstream PR action was performed. No contract code, storage, authorization, token configuration policy, or deployment wrapper is changed. The command is a corrected source example, not an executed demonstration; it still requires valid caller-supplied testnet addresses and an appropriately authorized identity.

The upstream contribution process asks for `make verify`, CI, review, and acceptance evidence. Those steps remain unperformed and unclaimed here; a Commons documentation continuation does not satisfy or replace upstream acceptance or payment conditions. No tests are added because this packet changes documentation only and runtime verification is outside this authorized source-only task.

## Packet

- `README.postimage.md`: complete modified donor root README.
- `change.patch`: the four focused upstream README hunks.
- `LICENSE`: unchanged donor MIT notice.
- `README.md`: this provenance, source reasoning, and limitations note.

Prepared 2026-10-06 by the Commons infrastructure lane. This note identifies the modification and preserves the donor attribution; it does not assign authorship of the original contract or documentation to the continuation author.
