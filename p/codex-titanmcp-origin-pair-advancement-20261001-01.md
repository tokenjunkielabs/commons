# TitanMCP allowed-Origin pair and method-boundary advancement

The existing `titanmcp-setup-schema` resource now includes the landed, read-only allowed-Origin pair classifier from source commit `603d300152f132aafe738b7db20c7457ae4f486c`.

## Producing outcome

- Consumer: GPT and ChatGPT MCP integration operators needing the exact TitanMCP allowed-Origin pair and OPTIONS/GET/POST boundary before composing a bounded setup or handoff.
- Classifier: `host/titanmcp_origin_pair.py`, blob `dfaa9b3ab933b16506b40e4d3305d43a9adb5a23`.
- Source receipt: `p/cursor-titanmcp-origin-pair-20261001-01.md`, blob `d7e9489042a7a4282237df26fb74fd7f2ccaa206`.
- Resource Master claim: [exact claimed paths](https://tokenjunkielabs.slack.com/archives/C0BRGMDQB6G/p1790870876649739).

The landed receipt records `https://chatgpt.com` and `https://webmcp-pad.vercel.app` as allowed on OPTIONS/GET/POST with exact ACAO echo and `Vary=Origin`. `https://chat.openai.com` and `https://example.com` return HTTP 403 with JSON-RPC `-32000`. Commons OPTIONS/GET/POST remains ACAO `*`; the pad preflight includes `Authorization`, while the Commons control does not.

## Activation checks and boundaries

This activation runtime could not resolve the live endpoints. Normal and optimized measurements failed closed with rc=1, so no fresh remeasurement is claimed. The mutation-oriented `--bake` path returned rc=2, `REFUSED`, and `sent=0`.

No pad runtime, Commons adapter, deployment workflow, setup-schema lane, SAVE/LOAD DRAFT lane, GET identity lane, HTML, provider configuration, or Titan state was changed. Bake, deploy, GO, Devpost submission, buyer contact, payment, revenue, and cash remain false. Commons open-door/no-auth behavior is preserved.

No build order was created: the capability is implemented and landed, and every adjacent unfinished lane is already owned or overlaps active work.

## Delta watermark

- Prior terminal main: `d79fd7d2fc837486c3b471febf86fbbf90297bde`.
- Activation base main: `a7e3e7c1e4926ca6bab546b4a0c0a0ddd05f1ff8`.
- Prior terminal Slack timestamp: `1790861376.874899`.
- Latest external delta timestamp: `1790863762.151499`.
- Claim timestamp: `1790870876.649739`.
- Remote branches observed before claim: 4,575; open PRs: 0.
- Activation PR, merge, hosted workflows, exact current-main blobs, and terminal Slack receipt will be written after merge/readback.

**LOCK NOT SHIPPED / AWAITING BRYCE GO.**
