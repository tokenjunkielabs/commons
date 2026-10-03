# Operation scope overlap view

The command center includes a read-only view of operation claims in saved Slack
responses. It lets a worker reuse the same source snapshot to find operations
that name the same source path, including workers posting through one shared
Slack identity.

Run it from the repository root:

```sh
python -m integrations.command_center.claim_overlap /private/state/slack-thread.json \
  --workspace-url "$SLACK_WORKSPACE_URL" \
  --channel-id "$SLACK_CHANNEL_ID" --text
```

Supply the actual workspace URL and channel ID for that source. The command does
not query Slack, refresh collectors, register claims, dispatch work, or write to
the source. Keep saved responses and generated views in the existing private
source-custody location. Do not commit private message bodies or generated
reports to this public repository.

## Input and source scope

Save the complete detailed connector result as JSON. Its MCP content may contain
a JSON object whose `messages` field is the detailed rendered thread, with
`From`, `Time`, and `Message TS` fields. Structured message records and detailed
rendered text are also supported. Multiple snapshot filenames can be supplied
to one invocation; use `-` to read standard input.

The view preserves message timestamps and original claim references. It uses
explicit operation keys as the grouping identity; a shared display name or Slack
user ID does not make two operations the same worker. A permalink is constructed
only when the workspace and channel are available from the input or supplied by
the caller.

Coverage always describes the supplied snapshots. A terminal thread page says
nothing about unobserved channels, other threads, earlier omitted pages, or work
that has not been announced there. Empty results never establish that the fleet
has no remaining work. Unsupported or unreadable input produces a nonzero exit
with a diagnostic.

## Reading the result

The parser recognizes explicit claim declarations and retains the source paths
and any explicit function scope attached to them. Mentions of another operation,
retained ownership, and unresolved prose are not permission decisions.

Explicit completion and scope updates are reconciled only with the operation
they name. A shortened operation core can resolve to one earlier dated claim
when that match is unique, with the alias retained in the evidence. Ambiguous
references remain visible for reconciliation. Operations without a reconciled
terminal statement are `unknown_active`; the view does not infer worker
liveness. The output includes unresolved candidates so a reader can open the
original message instead of mistaking a parser omission for free scope.

A shared path produces a **potential overlap**. This is a prompt to read the
existing claims and compose the work. It does not establish a semantic conflict,
revoke custody, select a winner, or prevent execution. Explicitly disjoint
functions can be distinguished when the source supplies them; otherwise the
view keeps the uncertainty. Explicitly different repository contexts are kept
separate. Unknown repositories and unqualified filenames retain their scope
uncertainty instead of silently becoming a fully qualified source identity.

Use `--path` or `--operation` to narrow the result. The default output is JSON;
`--text` provides a compact operator view. It lists every selected operation's
observed state, source scope and statement references, including a single claim
or completed operation with no matched pair. Filtered results retain any
overlapping counterpart so both source statements remain available. Overlaps do
not cause a failed exit: a successful read and projection exits zero.

Existing task ownership continues through `state/claims`,
`host/coordination_state.py`, and the command-center work-item API. This tool is
an additional projection of the existing source, not a replacement work queue.
