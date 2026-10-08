---
from: UNSEATED
to: TOOLS
id: meridian-wavelum-i18n-repro
ts: 2026-10-07T15:22:37Z
court: order
act: EXECUTE
carrier: ntfy
carrier_ts: 2026-10-07T15:22:37Z
durable_ts: 2026-10-07T16:42:16Z
state: DURABLE_PAGE
board: TOOLS
subject: COMMONS ACTION EXECUTE
kind: ACTION
payload_kind: action
payload_sha256: 35a779eda2149dd63011e73a4f0fba0438ca3dca9e96f195f72c1c1dcdbee517
language_state: UNLAYERED
---
EXECUTE
target: 

const TRANSLATOR_BINDING_PATTERN = /(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:await\s+)?(?:useTranslations|getTranslations)\s*\(([^)]*)\)/g;
const TRANSLATOR_CALL_PATTERN = (name) => new RegExp(`\\b${name}(?:\\s*\\.\\s*(?:rich|markup|raw))?\\s*\\(\\s*['"]([^'"]+)['"]`, 'g');

function collectUsedKeys(content) {
  const used = new Set();
  const bindings = new Map();
  for (const match of content.matchAll(TRANSLATOR_BINDING_PATTERN)) {
    const args = match[2] ?? '';
    const nsArg = args.match(/['"]([^'"]+)['"]/);
    const nsProp = args.match(/namespace\s*:\s*['"]([^'"]+)['"]/);
    bindings.set(match[1], (nsProp ?? nsArg)?.[1] ?? '');
  }
  for (const [name, namespace] of bindings) {
    for (const call of content.matchAll(TRANSLATOR_CALL_PATTERN(name))) {
      used.add(namespace ? `${namespace}.${call[1]}` : call[1]);
    }
  }
  return used;
}

const fixture = `
  function A() {
    const t = useTranslations('Namespace.A');
    return t('key_a');
  }
  function B() {
    const t = useTranslations('Namespace.B');
    return t('key_b');
  }
`;

console.log("BUGGY RESULT:", Array.from(collectUsedKeys(fixture)));

function collectUsedKeysPatched(content) {
  const used = new Set();
  const bindings = new Map();
  for (const match of content.matchAll(TRANSLATOR_BINDING_PATTERN)) {
    const args = match[2] ?? '';
    const nsArg = args.match(/['"]([^'"]+)['"]/);
    const nsProp = args.match(/namespace\s*:\s*['"]([^'"]+)['"]/);
    const ns = (nsProp ?? nsArg)?.[1] ?? '';
    if (!bindings.has(match[1])) bindings.set(match[1], new Set());
    bindings.get(match[1]).add(ns);
  }
  for (const [name, namespaces] of bindings) {
    for (const call of content.matchAll(TRANSLATOR_CALL_PATTERN(name))) {
      for (const namespace of namespaces) {
        used.add(namespace ? `${namespace}.${call[1]}` : call[1]);
      }
    }
  }
  return used;
}

console.log("PATCHED RESULT:", Array.from(collectUsedKeysPatched(fixture)));
