# PayD #505 / PR #680 — SMTP misconfiguration health review

## Immutable inputs

- Issue: https://github.com/Protocol-Guild/PayD/issues/505
- Existing sponsor PR: https://github.com/Protocol-Guild/PayD/pull/680
- Reviewed head: `c35d8229a43fac7f5d3d780a3c0b566e219abc24`
- Sponsor base recorded by the PR: `171c74b454daba241bfb75f36d10a0a3a77a68e5`
- Original contributor and payment ownership: `woahwhattheheck` (unchanged)

The issue is open and labelled `GrantFox OSS`, `Maybe Rewarded`, and `Third Campaign`. It asks that SMTP misconfiguration no longer fail silently, including a health endpoint status. PR #680 is open, non-draft, mergeable, and has no review comments at the reviewed snapshot.

## Acceptance blocker

The PR's `MailerService.getHealthStatus()` correctly distinguishes incomplete SMTP configuration:

```ts
return {
  status: 'not_configured',
  error: error.message,
  queuedRetries: this.retryQueue.length,
};
```

However, the health controller only degrades the top-level health result for `disconnected`:

```ts
statusReport.dependencies.email = emailResult.value;
if (emailResult.value.status === 'disconnected') {
  isHealthy = false;
}
```

Therefore an incomplete SMTP configuration—the motivating failure mode in issue #505—is reported in the nested email dependency while the endpoint can still return an overall healthy result. That can let uptime checks miss the exact misconfiguration the issue requires operators to notice.

## Minimal correction

On the exact PR head, treat any configured-email result other than `connected` as unhealthy:

```diff
-      if (emailResult.value.status === 'disconnected') {
+      if (emailResult.value.status !== 'connected') {
         isHealthy = false;
       }
```

This preserves the PR's three-state dependency detail while making both `disconnected` and `not_configured` fail the aggregate health result.

## Focused regression criteria

Add or extend the health-controller test to stub `MailerService.getHealthStatus()` as:

```ts
{
  status: 'not_configured',
  error: 'SMTP configuration incomplete',
  queuedRetries: 0,
}
```

Assert all of:

1. the response is the endpoint's unhealthy status code;
2. `dependencies.email.status` remains `not_configured`;
3. the sanitized configuration error is present;
4. `queuedRetries` remains `0`.

Also retain the existing disconnected and connected cases. No SMTP connection, account action, email delivery, or full suite is required to validate this controller branch.

## Scope and money state

This is a review packet, not a source patch or competing submission. It does not modify PR #680 or the sponsor repository and does not change original contributor/payment rights.

Money state at review time:

- advertised fixed USD amount: not evidenced;
- platform state: GrantFox `Maybe Rewarded` / Third Campaign label;
- funded or escrowed amount: not evidenced;
- awarded: $0 evidenced;
- invoiced: $0;
- received: $0.

Next action: PR #680's author or an authorized publisher should apply the one-condition correction on the existing branch, add the focused controller regression, and preserve the same sponsor PR rather than opening a duplicate.
