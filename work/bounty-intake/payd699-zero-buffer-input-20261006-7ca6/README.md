# Preserve an explicit zero yellow-buffer input

The Forecasting page renders a saved `yellowBufferPct` of zero correctly, but its change handler uses `Number(value) || 10`. Entering zero therefore writes ten back into the controlled draft. This patch preserves zero while keeping the existing default of ten for blank or unparseable input.

## Pinned source and credit

- Canonical repository: [Protocol-Guild/PayD](https://github.com/Protocol-Guild/PayD).
- Existing carrier: [PR 699](https://github.com/Protocol-Guild/PayD/pull/699), authored by `woahwhattheheck`.
- Donor repository and branch: `woahwhattheheck/PayD:fix/forecast-subscription-lifecycle-543`.
- Donor head: `1131f2daafb9ba7dbb27bcb4d3842e9d28e1be43`; observed base: `171c74b454daba241bfb75f36d10a0a3a77a68e5`.
- Changed production path: `frontend/src/pages/Forecasting.tsx`.
- Complete preimage: `89701bc7454343c3e61a25f1f1eb0da8b11df7a9`, 9,925 UTF-8 bytes.
- Prepared postimage: `e14c51214fd05c0c11e0a0f0233a2f7058adf08b`, 10,165 UTF-8 bytes.

The carrier addresses [issue 543](https://github.com/Protocol-Guild/PayD/issues/543), the separate WebSocket subscription-lifecycle request. That issue is open and unassigned in the observed metadata. Its four returned comments include waterWang's earlier [PR 567](https://github.com/Protocol-Guild/PayD/pull/567) report and two requests for assignment from guptakumarranjeet150. Those statements are preserved as external attribution, not assignment or acceptance. This packet does not reacquire, supersede or validate PR 567.

The prepared change is a distinct input correction in the current carrier. Its subscription effect, captured organization identity, load cancellation, alerts, refresh and save handlers remain unchanged. The carrier's historical six lifecycle cases and transpilation report are not new evidence for this packet.

## Existing contract

The controlled input already uses:

```tsx
value={String(settingsDraft.yellowBufferPct ?? 10)}
```

The frontend API declares `yellowBufferPct?: number` and sends the draft in the existing settings request. The existing controller forwards that field. The corresponding calculation uses:

```ts
const yellowBufferPct = Number(liquiditySettings.yellowBufferPct ?? 10);
```

Thus the inspected source chain distinguishes zero from an absent setting. The patch aligns the edit handler with that existing representation; it does not recommend a percentage or change financial policy.

## Change

The handler captures and trims the string, converts it once with `Number`, then applies the existing default only when the string is blank or the parsed result is `NaN`:

```tsx
const value = e.target.value.trim();
const parsed = Number(value);
setSettingsDraft((s) => ({
  ...s,
  yellowBufferPct: value !== '' && !Number.isNaN(parsed) ? parsed : 10,
}));
```

An explicit numeric zero, including negative zero under JavaScript number semantics, reaches the draft. Blank and whitespace-only strings, and strings that convert to `NaN`, retain the default ten. Other existing numeric conversion behavior is preserved. Capturing the value before the functional updater also avoids retaining the event object inside that updater.

This does not introduce range validation, a finite-number policy, clamping, integer-only percentages or a new admission condition. It does not change the calculation, defaults for an absent setting, API payload shape, tenant isolation, authorization, persistence or routing.

## Complete source custody

| Source path | Git blob | UTF-8 bytes |
| --- | --- | ---: |
| `frontend/src/pages/Forecasting.tsx` | `89701bc7454343c3e61a25f1f1eb0da8b11df7a9` | 9925 |
| `frontend/src/services/forecastApi.ts` | `9b28116851539b8777b3e54ebf1ef19e2bb90da1` | 2294 |
| `backend/src/routes/forecastRoutes.ts` | `3ba68e66ebde8b7eaa5364ef9d467de0eed630be` | 628 |
| `backend/src/controllers/forecastController.ts` | `2504df0dce104b66329213f82335ff0ddfa2d7e1` | 3305 |
| `backend/src/services/forecasting/forecastingService.ts` | `0daef6e057cbe5c724bfb2d40186c6b4cb72a895` | 8998 |

All five complete texts were retained and their Git blob identities independently matched. The nontruncated 753-entry donor tree contains no AGENTS/RULES or NOTICE file. Its root CONTRIBUTING (`1e015aa7e145db0cd0e306f7032cce130b8acbb8`) and Apache 2.0 LICENSE (`261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`) exactly match the previously retained complete texts. The source patch carries a dated modification notice, and the exact license is included. The unchanged root README at `374ffef680426f41b9f3e832059106839cfc72bd` has a conflicting MIT badge; this packet does not resolve that metadata discrepancy.

## Verification and limits

The two-hunk patch has nine added and three removed production lines, including the modification notice. Exact forward application and reverse reconstruction match the complete preimage and prepared postimage. Independent source reasoning found no ordering issue under the existing string-input contract. These are source and byte-identity checks, not execution results.

No browser, component, backend, database, network service, fixture, test, build, compiler, settings request or account action was run. The page's actual deployment entrypoint, complete API mounting, input-library behavior, loading races, permissible percentage range and broader application readiness are not established here. The existing Refresh/Save race behavior and subscription implementation are outside this narrow correction.

Apply `zero-buffer-input.patch` relative to the exact donor root and preimage above. Later source changes require explicit reconciliation. The Commons packet publishes a focused patch, this guide and the license; it does not republish the full module or update an upstream branch.

Maintainer review, the original issue's lifecycle acceptance, assignment and any reward remain external. No sponsor contact, upstream claim/submission, credentials, employee records, wallet, chain, payment or live financial input is included or acted upon.
