# Caley legacy PR43: declare the workspace provider client boundary

This packet adds `'use client';` to the workspace context provider in mini0n-ai's existing [caley-io/marketing PR43](https://github.com/caley-io/marketing/pull/43). The provider uses React context and state hooks and is imported through the server app layout. The two-line addition declares the boundary required by the pinned Next.js 14 app; every original provider byte remains unchanged after the new prefix.

This is a source correction to that legacy pull request. The repository's current README says the project moved to the [Rails successor](https://github.com/caley-io/caley). This packet does not change the successor or establish an active bounty, deployment, or completion of the broader [workspace issue1](https://github.com/caley-io/marketing/issues/1).

## Exact source and attribution

Observed on 2026-10-05:

| Source | Immutable identity |
| --- | --- |
| Existing external PR43 author | mini0n-ai |
| PR43 head | `b056dfdea9329173aa606865e16c786bb3f1201e` |
| PR43 base and observed upstream main | `03ab7bd017360f1375b4e74b8b95cede8e90c2d9` |
| Original `apps/web/providers/WorkspaceProvider.tsx` | `098249333b1599b900555fb3fbcbbb05b008e3fc` (1,737 bytes) |
| Corrected provider | `745a3f0ee7448ba05cdfdf569cf7a3e556096253` (1,752 bytes) |
| Importer `apps/web/app/(app)/providers.tsx` | `e1a362bcaba766304fd4c4dd13180d44068c0f22` |
| Server `apps/web/app/(app)/layout.tsx` | `f0eb92b841d31f9bae701ea21c0717bc19a5f039` |
| `apps/web/package.json` | `db4d362e2f00ac9e9d68818d4aace864e3693b7e` |
| Current README, including Rails move | `7aec1d5132a29d198820f2e89844ebb8b6cd53db` |
| Exact upstream AGPL-3.0 license | `0ad25db4bd1d86c452db3f9602ccdbe172438f52` |

The complete corrected provider is in `source/apps/web/providers/WorkspaceProvider.tsx`. The serialized patch targets its original upstream path. The included `LICENSE` is the complete upstream AGPL-3.0 text; original project and pull-request authorship is retained.

## Source diagnosis and change

The fully read import chain is:

1. The async app layout awaits `auth()` and imports `Providers`; it has no client directive.
2. `Providers` imports and renders `WorkspaceProvider`; it also has no client directive.
3. The new workspace provider calls `createContext`, `useContext`, and `useState` without declaring a client boundary.

The package pins Next.js 14.0.4 and React 18.2. The official [Next.js 14 composition documentation](https://nextjs.org/docs/14/app/building-your-application/rendering/composition-patterns) identifies React context providers as client components and demonstrates placing the directive in the provider while rendering it from a server layout. Merely passing server-rendered children through other providers does not change this module's import boundary.

The patch adds the directive and a blank line at the beginning of `WorkspaceProvider.tsx`. The async layout, authentication call, importer, workspace state, account update behavior, and exports are unchanged. No persistence, role management, invitations, Gmail linking, or other broad issue feature is added.

## Validation performed

- Verified the retained complete preimage against its Git blob identity.
- Verified the postimage is exactly the directive plus a blank line followed by the complete preimage.
- Independently applied the serialized unified patch in memory and compared its full result with the authored postimage.
- Confirmed one hunk, two added lines, zero removed lines, and preservation of the original final-line ending.
- Read the complete production import chain and relevant pinned package metadata, current README, contribution template, and license.

These are source and text-integrity checks. No package install, TypeScript compiler, Next.js build, React runtime, test suite, authentication session, migration, or browser interaction was run. The upstream build command includes a database migration and was not invoked. Existing PR43 statements about tests are the external author's statements, not results of this packet.

## Delivery and commercial boundary

PR43 was open and unmerged with zero issue comments and zero inline review comments when qualified. The issue's 21 comments include several existing external attempts and PRs; their claims and attribution remain intact. The exact own-account PR search returned zero results, which describes that query only.

The historical sponsor comment [1911895554](https://github.com/caley-io/marketing/issues/1#issuecomment-1911895554) advertises $50. The associated [Algora terms](https://github.com/caley-io/marketing/issues/1#issuecomment-1911895757) require an attempt comment, a claim-bearing pull request, and supported payout eligibility. This packet performs none of those platform actions and does not establish current funding, acceptance, or payment. Previously failed sponsor-comment and publisher routes remain unretried.

A maintainer can apply the patch to the exact PR43 head, or compose it with a later source revision after checking that revision. Upstream submission, any required runtime validation, acceptance of the full workspace feature, and commercial follow-through remain external to this Commons source delivery.
