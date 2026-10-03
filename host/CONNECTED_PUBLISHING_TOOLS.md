# Inspect connected publishing tools

`connected_publishing_tools.mjs` inspects a real supplied dynamic tool inventory. It counts the GitHub/Slack subset, maps the requested write primitives and harmless account probes to their actual callable names, and can return one requested schema. It does not call providers, publish, authenticate, change permissions, or decide whether an operation is permitted.

Use the harness's available discovery first. Keep working and repeat that same discovery at normal work boundaries after a partial result, as described in [RULES.md, rule 34](../RULES.md). A registry can contain hundreds of unrelated provider tools. Counting the whole registry does not identify the GitHub/Slack result; searching descriptions for provider names can also include unrelated tools and print a very large amount of documentation.

## Read a live export

Export the actual registry as an array of names or `{name, description, ...}` entries, or as `{observed_at, tools: [...]}`. Retain the actual `observed_at` value when one is available. Names-only exports are enough for counts and action lookup. Schema lookup needs the tool's real definition from the current registry.

```sh
node host/connected_publishing_tools.mjs --input /private/current-tools.json
node host/connected_publishing_tools.mjs --input /private/current-tools.json --names
node host/connected_publishing_tools.mjs --input /private/current-tools.json --schema github.create_commit
node host/connected_publishing_tools.mjs --input /private/current-tools.json --previous /private/prior-tools.json
```

Standard input is supported with `--input -`, the default. The module also exports `inspectPublishingTools(snapshot, options)` and `publishingToolDefinitions(snapshot, selector)` for an existing Node host. Importing the module performs no collection or scheduled work.

For a native code-mode registry, a compact first inspection can use:

```js
const publishing = ALL_TOOLS.filter(tool =>
  /^mcp__codex_apps__(github_|slack_)/.test(tool.name));
text({count: publishing.length, names: publishing.map(tool => tool.name)});
```

Retrieve a particular definition only after observing its exact name:

```js
const name = 'mcp__codex_apps__github_create_commit';
text(ALL_TOOLS.find(tool => tool.name === name));
```

Use the exposed registry and discovery interface in the current harness; a missing interface name is not a capability verdict. The inspector recognizes the current native names, MCP provider namespaces, and direct `github.action` / `slack.action` names. It does not guess a provider from arbitrary description text. Unknown namespaces remain included in `other_tool_names` and need their real schema inspected.

## Read the observation accurately

The owner-observed 44/66 and 125/127 counts are hints. Actual write names determine `write_observation`. Even a 125/127 observation asks for more discovery if a required primitive is missing. A differing count with every requested writer retains those writers as observed. `--previous` shows newly observed and not-reobserved names without declaring a previously available capability absent.

The output keeps inventory, account state and attempted-operation state separate. After locating the tool, use harmless authenticated profile, installation, workspace and target-repository permission reads where exposed. Then execute the authorized operation through its actual schema. A provider authentication error, repository-policy rejection, provider permission error and failed typed operation are distinct outcomes; none is inferred from the count.

Partial discovery is a successful inspection and exits **0** so the inspector cannot become a work gate. Malformed or unreadable input exits **2** with a clear error instead of pretending the registry is empty. A requested schema that is absent or has only a name also exits **2**; its JSON describes the missing observation. Correct the input or repeat native discovery while continuing independent work.

Keep session observations private unless a specific diagnostic is operationally useful. The merged implementation is the record; no recurring census, new worker, public registry dump, acknowledgment post or provider mutation is created by this tool.
