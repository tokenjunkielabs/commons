# pREST mock-adapter permissions documentation correction

The permissions example in the existing [prest/docs PR #3](https://github.com/prest/docs/pull/3) configures global access settings and supplies three arguments. Current pREST reads the mock instance's `AccessConf` field and requires five arguments. This packet contains a four-hunk correction to that example and its explanation; it preserves the surrounding contribution.

## Exact source and contribution custody

- Original funded request: [prest/prest issue #284](https://github.com/prest/prest/issues/284). The issue was open and unassigned in the bounded October 5, 2026 read. All four comments were read, including the historical IssueHunt $20 notice. The historical amount does not establish an award or payment.
- Original author: **rafael81**. [prest/prest PR #963](https://github.com/prest/prest/pull/963) is the predecessor. [Member comment 4430692107](https://github.com/prest/prest/pull/963#issuecomment-4430692107) directs this documentation to `prest/docs`; the author's following comments identify docs PR #3.
- External carrier: docs PR #3, open and unmerged at head `d449e12e35c8f634d38b74a77dc79f39fc6f616b`, branch `rafael81/docs:docs/mock-adapter`. The reported base was `47c403f05a240b150ce0c4f4050749ece022789e`. Its two issue comments and one inline comment were read; the heading suggestion was already addressed, and no permissions-example correction appeared.
- Exact guide preimage: [get-prest/mock-adapter.md](https://github.com/prest/docs/blob/d449e12e35c8f634d38b74a77dc79f39fc6f616b/get-prest/mock-adapter.md), blob `1984d67ea6b8c146d81682382b2a596d8b410360`, 2743 UTF-8 bytes.
- Implementation premise: [adapters/mock/mock.go](https://github.com/prest/prest/blob/b84da9b48fc5ae0765af67ab523314665f3d6741/adapters/mock/mock.go), blob `57708dd35eced7b3e50b67e314cc237a96866a15`. The complete relevant definitions of `Mock`, `New`, and `TablePermissions` were read.
- Configuration premise: [config/config.go](https://github.com/prest/prest/blob/b84da9b48fc5ae0765af67ab523314665f3d6741/config/config.go), blob `f5eb2019c30e7322d5c33bd9bb2cc806ea80b01e`. The `AccessConf`, `TablesConf`, and global adapter fields were inspected.
- The pinned [development guide](https://github.com/prest/docs/blob/d449e12e35c8f634d38b74a77dc79f39fc6f616b/get-prest/development-guide.md), blob `ef21d9a41e6ccd9c3054e0eecc64e7adeea6ab9b`, was read. Its external review/test requirements remain with the original contribution. No repository license was reported in the observed docs metadata; no new license is asserted here.

The exact public Slack search for `prest` and `284` returned one intake result and provider end. A canonical all-state own-account PR query covering both repositories returned zero with `incomplete_results:false`. These are bounded observations. They neither transfer rafael81's contribution nor grant access to their branch.

## Patch behavior

`mock-adapter-permissions.patch` applies to the exact external guide preimage. It changes the permissions paragraph and two assignments to `adapter.AccessConf`, supplies two leading empty arguments to `TablePermissions`, and explains that this mock ignores those arguments. The original `config.TablesConf` table configuration and its named fields match the inspected types.

When restrictions are enabled, the current method reads the instance's tables and optional user overrides. The example requests the configured table's read permission with an empty user name. No runtime method, adapter framework, fixture, test, global configuration implementation, or other documentation section is changed.

The corrected complete guide has 2922 UTF-8 bytes and Git blob identity `8678ef4dd2f67776292446b7a39f196ff71f9aa9`. The packet distributes the corrective patch and exact identities; the original complete guide remains at its author's pinned carrier.

## Verification and remaining work

The complete native preimage was retained and its computed Git blob matched the provider. A separate parser applied the serialized unified patch to that full preimage and compared every resulting character, including the final newline, with the prepared full candidate. The patch changes one upstream path, with four hunks, eight added lines and four removed lines. All other guide bytes remain exact.

This is static source alignment. No Go compiler, test, documentation build, database, native executor, external PR submission, platform submission, or runtime acceptance was performed. Existing examples outside the changed permissions section were preserved; they were not comprehensively revalidated. No completion of broad issue #284, maintainer acceptance, or reward is claimed. Any external continuation belongs on the current maintainer-selected carrier after its source/head is reconciled, preserving original authorship and applicable contribution requirements.
