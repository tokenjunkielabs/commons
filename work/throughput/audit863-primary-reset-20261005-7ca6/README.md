# Bind audit reset deadlines to exhausted primary quota

This packet supplies a narrow source continuation for [bounty-concierge #863](https://github.com/woahwhattheheck/bounty-concierge/pull/863), the existing integration of the Search-scoped shared cooldown into canonical bounty audits. It is internal maintenance of the controlled fork, not a sponsor submission or an unpaid acceptance package for another claimant.

## Source and original work

PR #863, authored by `woahwhattheheck`, was observed merged from `8bef729ba4bb27c9749be5e5b03d36ee75718f92` at `678ad971906a94cf5fc37edd2eaefdb9cecd66a3`, which was also the acquired current main. Its native two-file delta contains the production audit integration and a historical test-file change. The latter was not executed, modified or republished.

Complete current sources were read:

| Path | Git blob | Bytes |
| --- | --- | --- |
| concierge/bounty_audit.py | f50645de64dc93d9ab4d8af841d904bf2e14c17c | 41080 |
| concierge/github_cooldown.py | f276f8132f26529e64013ab856e44d27c55e6c17 | 13146 |

Original scope remains credited: Search-specific cooldown state, immediate existing timeline fallback on a demonstrated Search throttle, direct resource reads kept distinct, and no automatic retry or scheduler. This packet preserves those behaviors.

## Concrete integration mismatch

The HTTP error reader already retains `Retry-After`, `X-RateLimit-Reset` and a parsed integer `X-RateLimit-Remaining`. The throttle classifier distinguishes demonstrated Search throttling from an ordinary permission 403. When recording an established throttle, the integration first uses valid nonnegative Retry-After seconds. If that produces no deadline, it currently accepts any finite future reset header, regardless of the remaining count.

A primary reset header describes the primary rate window. It does not identify when a secondary throttle ends while primary quota remains. The [official GitHub rate-limit documentation](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api#exceeding-the-rate-limit) conditions the reset wait on a zero remaining count and otherwise describes the separate secondary-limit backoff. The already present `cooldown_deadline` helper in the full source likewise gates reset use on `primary_exhausted`. The new audit integration omitted that distinction.

Consequently, a supported throttled response with positive or unknown remaining count and no usable Retry-After can record an unrelated primary-window deadline for the Search scope. This is source-derived behavior, not a captured live response or a measured delay.

The patch adds `exc.rate_limit_remaining == 0` to the existing reset fallback condition. It preserves the numeric Retry-After branch and its precedence, the finite/future reset validation, and the exhausted-primary path. Positive or unavailable remaining values now reach the existing `extend_unknown_secondary()` path when no explicit delay was selected. That path retains its established bounded escalation; it does not reveal the provider's exact secondary reset time or authorize a request.

The sole production hunk is +6/-1. All other source bytes are unchanged, including Search-scope selection, the throttle classifier, error metadata, permission errors, fail-closed store errors, timeline fallback, pagination, cache behavior and audit result fields. No new environment setting or credential access is introduced. Callers without the opt-in shared store retain their existing behavior.

Existing recorded deadlines are not rewritten or shortened. The shared store's extension operations retain the maximum deadline, so a previously stored later deadline can remain in force until its ordinary expiry. This patch corrects future deadline selection after adoption; it is not a cooldown-state migration or bypass.

## Packet and verification boundary

The packet contains the complete modified `concierge/bounty_audit.py`, `primary-reset.patch`, the original MIT LICENSE and this guide. The 41,226-byte postimage has Git blob `57aeff15f22db0a3218618f5e166bc778ab4d0a2`. Exact forward and reverse text reconciliation against the complete preimage passes, and all bytes outside the intended condition/comment replacement remain identical. Independent blob identities agree with the native complete source identity.

The root instruction and licensing custody is inherited from the directly preceding parent `bfff853a125aebf76275e75e981a417eff7b5b2a`: AGENTS.md `4bff17819cb6f83f1e79df2607b12023e1c6ee36`, CONTRIBUTING.md `f953f75d0efa6897fe8adef66f4dc64e41d8e939`, and full CRLF MIT LICENSE `b19d0ab1000f055c9e1d1a40d0d1e43e0707ac9e`. Its complete 1,222-entry tree was untruncated and had no nearer instruction/license for the module; #863 changes only the two reported paths. The original SPDX and copyright notice are preserved.

A separate agent assessed the supplied predicate and control-flow contract without provider calls, runtime or full-file execution; that reasoning found no concrete semantic concern. It is not a test result or an approval gate.

No Python execution, tests, replay cases, fixtures, SQLite access, rate-limit request, retry, scheduler, token/environment read, live bounty audit, upstream mutation/contact or payment action occurs. Historical execution claims are not transferred to this patch. The separate held status-CLI credential route remains held. Publication in Commons does not deploy or change the original command, establish sponsor acceptance, or measure throughput.
