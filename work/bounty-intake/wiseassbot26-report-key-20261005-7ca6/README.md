# Preserve distinct report callbacks in Workers KV

The admin-report implementation in [birlug/WiseAssBot PR30](https://github.com/birlug/WiseAssBot/pull/30) identifies records by chat, reported user, whole-second processing time and reporting administrator. Distinct callback events with the same tuple share a KV key. Their writes can compete for the same value and the provider's per-key write allowance.

This continuation appends the callback query ID to that existing key stem. Two distinct query IDs processed within the same second therefore produce different record keys. The complete Rust postimage is in `src/bot.rs`; `change.patch` applies only this call-site change to the source below.

## Source and attribution

| Item | Pinned source |
| --- | --- |
| Original issue | [birlug/WiseAssBot#26](https://github.com/birlug/WiseAssBot/issues/26) |
| Existing implementation | TheOnlyOne001, PR30, `e9f0f12717e19299ece63486712a19f1147b2b32` |
| Original `src/bot.rs` Git blob | `43c8ff52ca8fc6718d432c53c95afa84228e48ed` |
| License | MIT, copyright 2025 birlug; reproduced unchanged as `LICENSE` |

The original bot and administrator-report feature retain their authorship. PR29 is a separate external implementation whose report key is only the reported user ID. Neither external branch is modified by this packet.

## Change and compatibility

Only the storage-key construction in `report_join_request` changes. The existing `report_key` helper remains the tuple-stem builder. The suffix is the callback ID already received from Telegram and already used to answer that callback; it is not a new user-supplied identity requirement.

The JSON report fields, timestamps, administrator lookup, success acknowledgement after the KV write, propagated write errors, report prefix and existing keys remain as before. The packet contains no migration, new dependency, deployment or bot configuration. Consumers that parse exactly four colon-delimited fields from the old storage-key suffix must accommodate the new trailing callback ID; consumers of the report JSON fields are unaffected. This does not create an export service.

The old seconds-based stem remains, so redelivery of the same callback in a later second can still create another record. This is a distinct-callback collision repair, not exactly-once delivery or a transactional append log. A repeated write to the same resulting key remains subject to Workers KV's limits and consistency model. The provider's 512-byte key limit still applies; no truncation of callback IDs is introduced.

## Primary API contracts

- [Telegram Bot API: CallbackQuery](https://core.telegram.org/bots/api#callbackquery) defines `id` as the unique identifier for the query. The existing callback argument supplies this value.
- [Cloudflare Workers KV: writes](https://developers.cloudflare.com/kv/api/write-key-value-pairs/) documents `put` as both creating a key and updating its value. Competing writes to one key can replace each other, and writing the same key more than once per second can return 429. Distinct callbacks now avoid that shared key.

These provider contracts establish the source-level collision and the purpose of the suffix; no production collision rate or performance measurement is claimed.

## Integration and acceptance

Apply `change.patch` against the pinned PR30 source, or compare the complete postimage before incorporating it into a newer branch. The patch adds four source lines net and leaves the existing embedded test section byte-for-byte unchanged.

Validation here is static source inspection and exact source/patch publication only. Rust compilation, formatting, tests, Worker execution, KV writes and Telegram webhook actions have not been run. The repository's `AGENTS.md` asks for formatting and integration tests before an upstream commit; those obligations are outstanding for an authorized upstream integrator. No upstream PR, issue comment, live bot contact, deployment, reward request or payment action is included.

The bounty label has no amount or approved payment terms in the five issue comments read on 2026-10-05. This packet does not assert a funded award or completion of all issue26 acceptance.
