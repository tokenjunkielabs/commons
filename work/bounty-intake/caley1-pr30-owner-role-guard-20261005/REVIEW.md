# Caley issue #1 / PR #30 — OWNER-role boundary review

## Pinned evidence

- Algora issue: https://github.com/caley-io/marketing/issues/1
- Existing external carrier: https://github.com/caley-io/marketing/pull/30
- Reviewed PR head: `c8289bf2ac6c9c9644c7e1530a60e1a0a2d3bf6f`
- Sponsor base recorded by the PR: `03ab7bd017360f1375b4e74b8b95cede8e90c2d9`
- Original contributor and payout owner: `oathis` (unchanged)

Issue #1 is open and carries the bounty label. The creator advertised `/bounty 50`, and Algora's issue reply describes a $50 bounty. PR #30 is open, non-draft, mergeable, and has no discussion or review comments at the reviewed snapshot.

## Concrete residual

PR #30's member-invite endpoint parses the requested role with the complete Prisma enum:

```ts
const inviteMemberBody = z.object({
  email: z.string().trim().email(),
  name: z.string().trim().max(80).optional(),
  role: z.nativeEnum(MembershipRole).default(MembershipRole.USER),
});
```

The UI offers only `USER` and `ADMIN`, but the server accepts `OWNER` too. The helper then authorizes both owners and admins:

```ts
await assertWorkspaceRole({
  userId: options.inviterUserId,
  workspaceId: options.workspaceId,
  roles: [MembershipRole.OWNER, MembershipRole.ADMIN],
});
```

Finally, it writes the caller-supplied role into either an existing membership or the pending invitation:

```ts
data: { role: options.role }
// ...
create: { ..., role: options.role },
update: { ..., role: options.role },
```

This means an ADMIN can call the API directly with `role: OWNER` and grant ownership to another existing or invited account, even though the UI does not expose that transition. The separate member-role update helper correctly requires an OWNER, so the invite path bypasses the intended privilege boundary.

## Smallest safe correction

Keep ordinary USER/ADMIN invitations available to both OWNER and ADMIN, but require the actor to be an OWNER before allowing an OWNER-valued invitation. Put the guard in `inviteWorkspaceMember`, not only in the route schema, so other callers cannot bypass it:

```diff
-  await assertWorkspaceRole({
+  const inviterMembership = await assertWorkspaceRole({
     userId: options.inviterUserId,
     workspaceId: options.workspaceId,
     roles: [MembershipRole.OWNER, MembershipRole.ADMIN],
   });
+
+  if (
+    options.role === MembershipRole.OWNER &&
+    inviterMembership.role !== MembershipRole.OWNER
+  ) {
+    throw new Error("Only owners can invite another owner");
+  }
```

A stricter alternative is to reject `OWNER` in the route schema entirely and continue using the existing owner-only member-role endpoint for promotion. The maintainer should choose explicitly; the important invariant is that an ADMIN cannot create another OWNER.

## Focused regression criteria

Use the existing Prisma/helper test seam or a focused mocked unit around `inviteWorkspaceMember`:

1. ADMIN + USER invitation succeeds.
2. ADMIN + ADMIN invitation succeeds if current policy permits it.
3. ADMIN + OWNER invitation rejects before any membership create, update, or upsert.
4. OWNER + OWNER invitation follows the maintainer's chosen policy.
5. Existing-member and pending-invite branches obey the same boundary.

No account, email, OAuth, browser, database, or bounty-platform action is required for this review packet.

## Scope and money state

This is a review packet only. It does not modify PR #30, create a competing submission, claim the bounty, or change `oathis`'s contributor or payment rights.

- advertised: $50;
- promised: $50 by the creator/Algora issue reply;
- funded or escrowed: not evidenced by the reviewed sources;
- awarded: $0 evidenced;
- invoiced: $0;
- received: $0.

Next action: PR #30's author or an authorized maintainer should add the central OWNER-role guard and focused regression on the same branch, then request sponsor review. Do not open a replacement PR for this residual.
