#!/usr/bin/env node
/** Inspect a supplied tool inventory without discovering, authenticating or publishing. */

const WRITES = Object.freeze({
  github: ['create_blob', 'create_tree', 'create_commit', 'create_branch', 'update_ref',
    'create_file', 'update_file', 'create_pull_request', 'merge_pull_request'],
  slack: ['send_message', 'create_conversation', 'edit_message'],
});
const PROBES = Object.freeze({
  github: ['get_profile', 'list_installations', 'get_repo_collaborator_permission'],
  slack: ['list_workspaces'],
});

function entriesFrom(snapshot) {
  if (Array.isArray(snapshot)) return snapshot;
  if (snapshot && typeof snapshot === 'object' && Array.isArray(snapshot.tools)) return snapshot.tools;
  throw new TypeError('Expected a tool array or an object with a tools array; an unreadable inventory is not an empty inventory');
}

function identify(name) {
  const match = name.match(/^mcp__codex_apps__(github|slack)_(.+)$/i)
    || name.match(/^mcp__(github|slack)__(.+)$/i)
    || name.match(/^(github|slack)[.:/_](.+)$/i);
  if (!match) return null;
  const provider = match[1].toLowerCase();
  let action = match[2].toLowerCase();
  if (action.startsWith(provider + '_')) action = action.slice(provider.length + 1);
  return {provider, action};
}

function inventory(snapshot) {
  const entries = entriesFrom(snapshot);
  const unique = new Map();
  const duplicateNames = new Set();
  for (const [index, entry] of entries.entries()) {
    const name = typeof entry === 'string' ? entry : entry?.name;
    if (typeof name !== 'string' || !name.trim()) {
      throw new TypeError(`Tool entry ${index} has no nonempty name; the observation was not classified`);
    }
    if (name !== name.trim()) throw new TypeError(`Tool entry ${index} has whitespace around its name`);
    if (unique.has(name)) {
      duplicateNames.add(name);
      // Repeated exports may supply a name-only object before its definition,
      // or add schema fields separately. Preserve every supplied field without
      // letting a later name-only record erase an available definition.
      if (typeof entry === 'object') {
        const previous = unique.get(name);
        const supplied = Object.fromEntries(Object.entries(entry).filter(([, value]) => value != null));
        unique.set(name, {...(typeof previous === 'object' ? previous : {}), ...supplied});
      }
    } else unique.set(name, entry);
  }
  const providers = {github: [], slack: []};
  for (const [name, entry] of unique) {
    const id = identify(name);
    if (id) providers[id.provider].push({name, action: id.action, entry});
  }
  for (const rows of Object.values(providers)) rows.sort((a, b) => a.name.localeCompare(b.name));
  return {entries, unique, duplicateNames, providers};
}

function actionNames(rows, requested) {
  return Object.fromEntries(requested.map(action => [action,
    rows.filter(row => row.action === action).map(row => row.name)]));
}

/** Pure inspection: the caller keeps using its actual discovery and provider bindings. */
export function inspectPublishingTools(snapshot, {includeNames = false, previous} = {}) {
  const current = inventory(snapshot);
  const providers = {};
  let missing = 0;
  for (const provider of ['github', 'slack']) {
    const rows = current.providers[provider];
    const writes = actionNames(rows, WRITES[provider]);
    const missingWrites = Object.keys(writes).filter(action => !writes[action].length);
    missing += missingWrites.length;
    providers[provider] = {
      observed_tools: rows.length,
      write_tools: writes,
      write_primitives_not_observed: missingWrites,
      probe_tools: actionNames(rows, PROBES[provider]),
      ...(includeNames ? {tool_names: rows.map(row => row.name)} : {}),
    };
  }
  const count = providers.github.observed_tools + providers.slack.observed_tools;
  const report = {
    schema: 'commons-connected-publishing-tools/v1',
    ...(snapshot?.observed_at ? {observed_at: snapshot.observed_at} : {}),
    inventory_entries: current.entries.length,
    unique_tool_names: current.unique.size,
    duplicate_tool_names: [...current.duplicateNames].sort(),
    github_slack_tools: count,
    other_tool_names: current.unique.size - count,
    observed_count_hint: [44, 66].includes(count) ? 'owner_observed_partial_set'
      : [125, 127].includes(count) ? 'owner_observed_full_set' : 'other_observed_count',
    write_observation: missing ? 'write_primitives_not_yet_observed' : 'all_requested_write_primitives_observed',
    repeat_discovery: missing > 0 || [44, 66].includes(count),
    providers,
    next_action: missing > 0 || [44, 66].includes(count)
      ? 'Continue useful work and repeat the same available discovery at ordinary work boundaries; inspect newly exposed schemas'
      : 'Use the discovered schemas and harmless account/repository probes, then perform the already-authorized work',
    publication_state: 'not_determined_by_inventory',
    account_state: 'not_probed_by_this_inspector',
    operation_state: 'not_attempted_by_this_inspector',
  };
  if (previous !== undefined) {
    const prior = inventory(previous);
    const names = value => new Set(Object.values(value.providers).flat().map(row => row.name));
    const before = names(prior), after = names(current);
    report.previous_observation = {
      ...(previous?.observed_at ? {observed_at: previous.observed_at} : {}),
      github_slack_tools: before.size,
      newly_observed: [...after].filter(name => !before.has(name)).sort(),
      not_reobserved: [...before].filter(name => !after.has(name)).sort(),
      interpretation: 'A missing name in this observation is not proof that the capability is absent',
    };
  }
  return report;
}

/** Return only the exact requested definitions, never every provider description. */
export function publishingToolDefinitions(snapshot, selector) {
  if (typeof selector !== 'string' || !selector) throw new TypeError('A tool name or provider.action selector is required');
  const current = inventory(snapshot);
  const all = Object.values(current.providers).flat();
  const exact = all.filter(row => row.name === selector);
  const id = identify(selector);
  const matches = exact.length ? exact : id ? all.filter(row => row.action === id.action && identify(row.name).provider === id.provider) : [];
  return {
    selector,
    found: matches.length > 0,
    tools: matches.map(({name, entry}) => ({
      name,
      definition_available: typeof entry === 'object' && ['description', 'inputSchema', 'input_schema', 'parameters'].some(key => entry[key] != null),
      definition: typeof entry === 'object' ? entry : {name},
    })),
    ...(!matches.length ? {next_action: 'Repeat discovery and load this schema from the actual current tool registry; it was not observed in this export'} : {}),
  };
}

async function main(argv) {
  const {readFileSync} = await import('node:fs');
  let input = '-', previous, schema, includeNames = false;
  for (let index = 0; index < argv.length; index++) {
    const option = argv[index];
    if (option === '--help' || option === '-h') {
      console.log('Usage: node host/connected_publishing_tools.mjs [--input FILE|-] [--previous FILE] [--names] [--schema PROVIDER.ACTION|TOOL_NAME]\nReads one real JSON tool inventory. Partial discovery exits 0; malformed input and missing requested schemas exit 2. No network requests or provider writes.');
      return 0;
    }
    if (option === '--names') { includeNames = true; continue; }
    if (!['--input', '--previous', '--schema'].includes(option)) throw new TypeError(`Unknown option: ${option}`);
    const value = argv[++index];
    if (!value || value.startsWith('--')) throw new TypeError(`Missing value for ${option}`);
    if (option === '--input') input = value;
    else if (option === '--previous') previous = value;
    else schema = value;
  }
  const read = path => JSON.parse(readFileSync(path === '-' ? 0 : path, 'utf8'));
  const snapshot = read(input);
  const result = schema === undefined
    ? inspectPublishingTools(snapshot, {includeNames, ...(previous === undefined ? {} : {previous: read(previous)})})
    : publishingToolDefinitions(snapshot, schema);
  console.log(JSON.stringify(result, null, 2));
  return schema !== undefined && (!result.found || result.tools.some(row => !row.definition_available)) ? 2 : 0;
}

if (typeof process !== 'undefined' && process.argv?.[1]) {
  const {pathToFileURL} = await import('node:url');
  if (import.meta.url === pathToFileURL(process.argv[1]).href) {
    try { process.exitCode = await main(process.argv.slice(2)); }
    catch (error) {
      console.error(JSON.stringify({error: 'inventory_inspection_failed', message: error.message,
        publication_state: 'not_determined_by_inventory'}));
      process.exitCode = 2;
    }
  }
}
