# PocketPay onboarding: key format and network copy

This source-only continuation removes two claims that a Stellar secret seed identifies a network. The import banner keeps the app's Testnet restriction and advises a key reserved for testing, never one used on Mainnet. The existing recovery-message entry now describes a reported network setup error without asserting that the key belongs to another network.

## Source and attribution

Canonical repository: https://github.com/Stellar-PocketPay/pocketpay-mobile  
Source commit: `c3a24abacb45030eb4fef41aabc46b312aaf54a3`

The original onboarding-copy feature is already complete: [issue 7](https://github.com/Stellar-PocketPay/pocketpay-mobile/issues/7) is closed and assigned to khalifa-zoro; [PR 74](https://github.com/Stellar-PocketPay/pocketpay-mobile/pull/74), authored by khalifa-zoro, was merged on 2026-07-17 at the observed head `709a5c746426885f1ef2cc20119182d86bb8a17e`. All five issue comments and the PR's sole comment were read. This patch credits that work and the repository's subsequent contributors. It does not reopen the original feature, transfer an assignment, or assert upstream acceptance or a reward.

The actual current import and recovery-message files were transferred from retained complete source and independently checked against their Git blob identities. A source-transfer transcription correction was applied before the identity check; it is not a production change. A bounded current PR-body search and two precise public activity searches did not establish a completed correction of these exact wording claims; this is not an exhaustive repository history claim.

## Why the current words are wrong

The import screen trims the input, checks the S prefix, length, alphabet, and `StrKey.isValidEd25519SecretSeed`, then calls `importWallet(trimmedKey)`. Its selected local `pocketpay-sdk` implementation calls `Keypair.fromSecret` and returns the derived public key; it performs no network test.

The official [StrKey source](https://stellar.github.io/js-stellar-base/strkey.js.html) decodes and validates the secret-seed type, encoding and checksum. The official [Keypair source](https://stellar.github.io/js-stellar-base/keypair.js.html) passes the decoded seed to keypair derivation without a network argument. These source contracts support the conclusion that an ordinary encoded secret seed does not itself identify Testnet or Mainnet. The separate network-specific genesis/master-key API is not the import path.

Stellar's [network documentation](https://developers.stellar.org/docs/networks) describes network passphrases and their role in transaction hashing/signing and network separation. The current application's transaction service also selects its network passphrase separately. This does not establish that importing a key creates or funds an account on any network, nor that an account exists there.

The official [saved-keypairs guidance](https://developers.stellar.org/docs/tools/lab/saved/keypairs) warns against reusing Mainnet keypairs on Testnet. The corrected banner preserves that practical separation; it does not encourage using a live-funds key.

The recovery classifier presently maps messages containing "network" or "testnet" to the legacy `secret_key_wrong_network` identifier. That identifier and classifier remain unchanged for compatibility. Only its rendered title, message and guidance become neutral about the key. `WalletEmptyState` reads the message table in both failed-import and failed-creation flows; the latter shares the corrected copy. No new error taxonomy or network diagnosis is claimed.

## Exact production changes

| Path | Before Git blob | After Git blob | Change |
| --- | --- | --- | --- |
| `app/(auth)/import.tsx` | `38a3f75f9aafb94084456110853457f792f2aab3` | `04191e59a818529b85c90bac8ac2e3b55a0b4a52` | One banner sentence, +1/-1 |
| `src/types/onboarding.ts` | `cc4586ac32bf7dd00d110ffa8bcddce0badc66ec` | `877b78413dc1d457a21f7953c14a9e12303a04b7` | Legacy-key comment and rendered error copy, +4/-3 |

Total: +5/-4 across two source files. The patch changes no validation, classifier branch, import handler, key derivation, persistence, transaction, network configuration, routing or layout behavior.

Relevant unchanged inputs at the same sponsor commit:

| Path | Git blob | Role |
| --- | --- | --- |
| `src/components/WalletEmptyState.tsx` | `53b024e09ed8021f3f474186dce0f0140ffb27b3` | Actual message-table consumer |
| `src/sdk-stub/pocketpay-sdk.js` | `ec02c486d040a884f86bc69aa637cb68ad9056e3` | Selected local import implementation |
| `package.json` | `08681ade42555a374cf7ba5d55660cc226515681` | Local SDK dependency and Stellar SDK range |
| `src/services/stellar.ts` | `3cbe4124bbefb3f7a6539fdaef2502f84921715f` | Separate transaction network configuration |
| `docs/security.md` | `ea0b3c4e05d644ec10fd0de148911a74ae3031e7` | Current Testnet-only and key-handling instructions |
| `CONTRIBUTING.md` | `d8493281d318b348f98a9bd999c2ffd6cc966d0d` | Upstream contribution requirements |

## Integration and limits

Apply `key-network-copy.patch` to the two exact preimages above, or compose its small hunks with newer source. Preserve the existing [Commons 31698](https://github.com/woahwhattheheck/commons/pull/31698) import-cancel continuation and the separate `work/bounty-intake/pocketpay76-onboarding-progress-20261006-7ca6/` progress patch when combining work. Do not replace whole newer files with the pinned postimages.

The complete sponsor tree used for this task contained no LICENSE file. This packet therefore contains only the narrow attributed patch and this integration guide, not full sponsor modules or an invented license grant.

Validation is static: complete input identities, literal changed hunks and the actual caller/import path were inspected; the packet's publication uses full immutable file readbacks. No app, SDK, test, typecheck, lint, wallet, storage, device, network, transaction or account operation was run. Official documentation establishes the stated contracts but is not a claim about executing an installed SDK version.

The upstream contribution requirements for UI-state documentation, screen-test matrix, accessibility review and relevant automated checks remain pending for any upstream integration. This Commons delivery is not an upstream submission, release, security audit, whole-onboarding acceptance, funding, award or payment claim.
