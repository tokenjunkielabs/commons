# TitanMCP GET /mcp identity and Origin advancement

The existing `titanmcp-setup-schema` resource now includes the landed, read-only identity and Origin classifier from source commit `6b290072b637707ba0c18353559f4a761674db05`.

## Producing outcome

- Consumer: GPT and ChatGPT MCP integration operators distinguishing the private-Origin TitanMCP endpoint from public open Commons before composing a setup or handoff.
- Classifier: `host/titanmcp_get_mcp_identity.py`, blob `24dc64c234fcb32d502c1dfe326f2192787b27d8`.
- Source receipt: `p/cursor-titanmcp-get-mcp-identity-20261001-01.md`, blob `fa9b97f4ca1eadb95ff68b56e426591c9af750ee`.
- Resource Master claim: [exact claimed paths](https://tokenjunkielabs.slack.com/archives/C0BRGMDQB6G/p1790859571853699).

The 2026-10-01 11:38:55 UTC source receipt records TitanMCP 1.4.5 with 24 tools and `open_door=false`; `https://chatgpt.com` receives a 204 preflight with its exact Origin while `https://example.com` receives JSON-RPC `-32000` with HTTP 403. The Commons control remains version 1.4.0, `open_door=true`, and ACAO `*`.

## Activation checks and boundaries

This activation runtime could not resolve the live endpoints. Normal and optimized measurements failed closed with `socket.gaierror` and rc=1, so no fresh remeasurement is claimed. The mutation-oriented `--bake` path returned rc=2, `REFUSED`, and `sent=0`.

No pad runtime, Commons adapter, deployment workflow, SAVE/LOAD DRAFT lane, HTML, provider configuration, or Titan state was changed. Bake, deploy, GO, Devpost submission, buyer contact, payment, revenue, and cash remain false. Commons open-door/no-auth behavior is preserved.

No build order was created: the capability is implemented and landed, and every adjacent unfinished lane is already owned or overlaps active work.

## Delta watermark

- Prior terminal main: `2a70dcd6ddad2094ecc3f823cb6171854f8b0791`.
- Activation base main: `2cf1d769a0198f5d3c0f7d795cb045a093910299`.
- Prior terminal Slack timestamp: `1790850381.736719`.
- Latest external delta timestamp: `1790854735.059489`.
- Claim timestamp: `1790859571.853699`.
- Remote branches observed before claim: 4,573; open PRs: 0.
- Activation PR: [#30187](https://github.com/woahwhattheheck/commons/pull/30187), head `76fe6a7255ecefaab1b7706b3cad94ae5b8bfabb`, merge/readback `a1e3c22db016057e1c0f30f972b4530a54b5966a`.
- Hosted workflows: 6/6 passed before merge.
- Exact activation blobs read back from main: ledger `0e6576663d801a3f4ec216b2b2d5631638802d58`; event `9e12a17367f0b7b33b34cc3ea8be93693040409d`; receipt `fcf76e09298c66c96a8286c70bf1dcba37b481d0`; projection `a5a2e1039b30773c58ed48b620108ba2cd93fd1f`.

**LOCK NOT SHIPPED / AWAITING BRYCE GO.**
