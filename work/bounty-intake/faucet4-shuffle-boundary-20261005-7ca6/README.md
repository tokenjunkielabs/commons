# Kryptokrona faucet: separate the backup shuffle statements

## Result and target

This packet contains a one-character production correction for [kryptokrona/kryptokrona-faucet PR7](https://github.com/kryptokrona/kryptokrona-faucet/pull/7), authored by jamilahmadzai. It targets that contribution's `nodeConfig.js` at commit `7adcdb9bd5b544437c95c9d28081124ca64e4b73` on `jamilahmadzai/kryptokrona-faucet:bounty/backup-node-failover`.

The PR was open and unmerged at the current metadata read; its base was `b70875c42e8ff54ab40d7f398e9d132493f79eec`. The patch applies to the contributed module, which is newly added by PR7. It is not a patch against a module already present on upstream main.

## Caller-backed defect

The complete contributed module constructs the candidate list as the primary node followed by `shuffleNodes(parseNodeList(env.BACKUP_NODES || ''))`. The shuffle copies the supplied backup list and enters its loop only when at least two entries remain after parsing.

Inside that loop, the line declaring `const j` has no terminating semicolon and the following destructuring assignment starts with `[`. JavaScript's automatic semicolon insertion does not separate those lines: the bracket expression can continue the initializer as computed property access. Evaluation then reads the same local `j` inside the computed property key before its initializer has completed. The entered loop therefore raises a ReferenceError before the intended swap. This is a runtime consequence of parseable source, not a parse-time SyntaxError.

The actual wallet caller obtains this list at the start of `selectDaemon()`; `initWallet()` awaits that selection before starting the wallet. The failure therefore occurs before any candidate daemon availability check. The PR's README itself documents a two-backup configuration, so this is on its stated feature path. Empty and one-entry backup lists do not enter the affected loop.

The language rule is documented by [MDN's automatic semicolon insertion reference](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Lexical_grammar#automatic_semicolon_insertion): a following bracket can continue an expression as member access, and an explicit separator is needed in this situation. The specific ReferenceError and caller consequence above are static deductions from the retained production source.

## Correction

`fix.patch` prefixes the destructuring assignment with a semicolon. This separates the index declaration from the existing swap while retaining the module's semicolon-free surrounding style. It preserves the random-index expression, Fisher-Yates loop bounds, copied input list, primary-first ordering, parser and exported API. Every other byte of the complete module is unchanged.

The patch has one hunk, with one removed line and one added line. It contains the minimal changed context; the complete third-party module is not duplicated in this packet.

## Source custody

All source paths below were acquired at the same immutable PR head.

| Path | Git blob |
| --- | --- |
| `nodeConfig.js` | `d346c83e0deeb334a82cb9f97f93207cc2eb3571` |
| `wallet.js` | `7d178f47f2147600078dce5a64b806636586cd9e` |
| `README.md` | `0004525fc0d494bf21f01b618de92800941dbe28` |
| `package.json` | `2fece2f01f740f2963de0369edda8fcd337f6677` |

The full root directory inventory was read. No root AGENTS.md or standalone license file was present in that inventory. The target file is at the root, so there is no intervening subdirectory instruction path.

Licensing declarations in the actual source differ: package.json declares ISC, while README.md says GPL-3.0. This packet records both declarations without choosing between them or inventing a copyright notice or license grant. Original project and contributor attribution is retained through the source links and immutable identity.

## Verification and limits

The complete original module is 1,840 UTF-8 bytes and independently computes to its native blob `d346c83e0deeb334a82cb9f97f93207cc2eb3571`. Applying the actual serialized patch to that retained preimage matches the intended complete 1,841-byte postimage exactly, with Git blob `3d16da82442501e58593e612cca07b1406dc1600`. Every context and removed line and both hunk line counts were checked.

These are source, patch-application and identity checks. The production module, Node, npm, existing tests, daemon connections and wallet operations were not executed. No successful live failover or broader wallet/network behavior is claimed.

[Original issue4](https://github.com/kryptokrona/kryptokrona-faucet/issues/4) asks for a backup node. Repository-member comment1222122897 from 2022-08-22 advertises 5,000 XKR. That is historical issue context, not a current award or USD valuation. The source correction is published only in this owned workspace repository; the original external PR, upstream issue, contributor claim and payout state are unchanged.
