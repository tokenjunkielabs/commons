# Configure separate Redis rate-limit stores

This is an attributed source continuation of [Protocol-Guild/PayD issue #355](https://github.com/Protocol-Guild/PayD/issues/355) and SrvFernandes's [PR #672](https://github.com/Protocol-Guild/PayD/pull/672). The submitted standard and strict limiters need a supported Redis command adapter and independent key prefixes. This packet contains a patch and guide; it does not install, connect or deploy them.

## Canonical source and original contribution

The canonical repository is Protocol-Guild/PayD. PR #672 was OPEN/unmerged at `87c62604b1ee39e7a95b7a0cd75d67445e120a99`, branch `SrvFernandes/PayD:feat/onlydust-fix-355-1791075930013`, against base `171c74b454daba241bfb75f36d10a0a3a77a68e5`. Issue #355 was OPEN/unassigned. Its three complete comments contain two proposals and the original author's PR link/claim; they do not establish maintainer assignment or acceptance. The PR discussion and inline-comment collections were empty at qualification.

The complete source file is `src/middleware/rateLimiter.ts`, blob `3ae088e095ae4e589cfe273cf3f825df6fffcfdb` (936 UTF-8 bytes). The complete caller `src/routes/tenantRoutes.ts`, blob `9dfea5890440714923cf778e1f2f8cce96d5916f`, registers strictRateLimiter on POST / and rateLimiter on PUT /:id and DELETE /:id. Existing tenant middleware/controllers and their ordering are unchanged. No upstream branch, claim or PR is modified.

## Concrete source defects and correction

Both submitted RedisStore objects receive only `client: redisClient`. The inspected primary API requires a command-sending function. Both also omit prefix, so the same client key would address the same default Redis namespace. Different store objects alone do not distinguish their counters. That is inconsistent with the caller's separate 100-request/15-minute and 10-request/one-minute policies.

The patch uses a named ESM RedisStore import and a type-only RedisReply import. One shared sendCommand adapter forwards the command name and all arguments to the existing ioredis client's call method and returns its promise, with the documented RedisReply type assertion. Both stores use that adapter. Their prefixes are `payd:tenants:standard:` and `payd:tenants:strict:`, so the same generated client key is distinct across these two policies.

The existing client construction, environment-variable reference, limits, windows, messages and response-header options remain byte-for-byte unchanged. There is still one client and two store objects. No new client, retry layer, fallback, IP identity rule, authentication restriction, tenant authorization rule or route is added.

These are source-derived corrections. The original configuration fails the inspected constructor contract before any counter interaction; shared-key interference is the separate latent issue once a compatible store transport is supplied. No actual server error, quota consumption or Redis data was observed.

Changing prefixes creates new counter namespaces; this patch does not migrate or preserve any existing default-prefix counters. The fixed names distinguish these two policies, not unrelated deployments using the same Redis database and names. Deployment namespace policy, connection lifecycle, outage behavior and operational rollout remain outside this source packet.

## Pinned primary dependency contract

The [official rate-limit-redis documentation](https://github.com/express-rate-limit/rate-limit-redis) documents its ESM import, ioredis sendCommand adapter and default prefix. Independently retained complete primary source at commit `88db3128ccd0617b4c932edb69f027eed167aca0` establishes the exact inspected contract:

| Primary path | Git blob |
| --- | --- |
| source/lib.ts | 754ab0e7dfce610212da06a313a76aadf0ea7bbd |
| source/types.ts | 6ede764c6fce4c9b1b0e3cb83b42d951868a012e |
| package.json | 89a276153cffc69e5b65c1e24bfb4848b3a77e75 |

That source requires exactly one of sendCommand and sendCommandCluster, defaults prefix to rl:, and constructs Redis keys by concatenating prefix and the supplied key. Its package declares version 6.0.1 and peer express-rate-limit >=8.6.0. These are inspected dependency facts, not a claim that PayD has those versions installed. No dependency implementation is copied into this packet.

## Remaining integration and source boundaries

The untruncated 765-entry submitted tree identifies root package.json `f0325832d3e5150375bd22481e577d19cd148eb6` and backend/package.json `746a535b08bf0c6ce9c4a96f7d75c76e0bbacb95`, matching already-retained complete manifests. Neither declares express-rate-limit or rate-limit-redis. The backend manifest declares ioredis ^5.9.3; the changed middleware is under root src, not backend/src. Package selection, compatible dependency installation, module/type resolution and application entrypoint mounting are not established or supplied here. This is not a claim that the whole proposal compiles or starts.

The new tenant route file was read completely; no live request was sent. No tenant/account/customer body, environment value, Redis URL, stored record or audit payload was acquired. The separate tenant-isolation/authentication and model/audit contracts are unchanged and are not certified by this correction.

The same tree pins already-read CONTRIBUTING.md `1e015aa7e145db0cd0e306f7032cce130b8acbb8`, LICENSE `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` and README.md `374ffef680426f41b9f3e832059106839cfc72bd`, with no AGENTS.md or nearer instruction/license. CONTRIBUTING is a scaffold placeholder; root LICENSE is Apache 2.0, README displays an MIT badge, and the backend package declares ISC. Those discrepancies remain explicit. Only this attributed patch and guide are published, without a full source-module copy or a new licensing conclusion.

## Text verification and delivery scope

The serialized patch contains 2 hunks, +9/-4 production lines. It applies exactly to the complete preimage and reverses exactly from postimage `9380c6ba72c0ffa761456d0d91e02cf24c668c90` (1129 UTF-8 bytes). Independent Git blob identities are retained. Verification is text and source reasoning only: no production function, Redis client, network connection, HTTP request, fixture, test, TypeScript compiler, package install, application or workflow was executed.

Original author, assignment, upstream acceptance and reward conditions remain separate. No external submission/contact/claim, account, wallet, payment or transaction action occurred. This packet does not establish whole issue #355 or PR #672 completion.
