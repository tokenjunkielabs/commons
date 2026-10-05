# Shipli React Native plist selection continuation

This packet corrects a narrow iOS metadata-selection error in [hummusonrails' existing React Native PR15](https://github.com/prasenjeet-symon/shipli-ai/pull/15). It does not implement React Native support again or claim completion of the broader [issue1](https://github.com/prasenjeet-symon/shipli-ai/issues/1).

## Exact source and attribution

| Source | Identity |
|---|---|
| External head repository | `hummusonrails/shipli-ai` |
| Head branch / commit | `feat/react-native-support` / `592b3b981820046f2937ae52db7bde1e67b37684` |
| Observed upstream base in PR listing | `11871929c45f7b8e961666ce26634eaa237bf360` |
| Original `src/plist-reader.js` | `959de2f7eba74c43c4efa0bb72df363c0b8628a6`, 1,083 bytes |
| Complete postimage | `57a81299f4f032992cf65658b13c576dca0b6c86`, 1,161 bytes |
| Original MIT license | `14fac913ccf80234b1848540089a3bbcb6e5283d` |

The original React Native detection, scanner, prompts, CLI and MCP integration remain hummusonrails' contribution. The separate [GautamJainoo PR14](https://github.com/prasenjeet-symon/shipli-ai/pull/14), head `543554a4ad90e42bfba96649e72e0104a27f099a`, already uses discovered plist candidates with a Flutter preference and fallback. Its plist blob is `044eee68709de61687b5ef730a7a728fdab1f8db`. This continuation integrates that existing selection approach into PR15's different implementation, retaining PR15's Pods/build exclusions and error handling. It claims no new selection algorithm.

## Trigger and correction

PR15 builds a candidate array by unconditionally prepending `ios/Runner/Info.plist` to its glob results, then reads only `candidates[0]`. When a React Native application's plist lives under its own iOS target directory, the forced Runner path is absent. The existing ENOENT handler then returns `found: false`, even though the glob already discovered an applicable plist. Both the CLI and MCP store-audit call the shared reader and pass its permission metadata to the auditor.

The postimage uses the existing glob results directly. It prefers a discovered candidate resolving to `ios/Runner/Info.plist`; otherwise it selects the first discovered candidate. An empty result still returns the existing not-found object. Normalizing only the preference comparison with the already-imported `path.resolve` keeps an equivalent absolute path comparable.

The parser, permission-key extraction, bundle ID result, ENOENT handling and non-ENOENT exception propagation are unchanged. The glob still excludes Pods and build directories. Selection among multiple non-Runner targets follows the existing first-discovered policy; this packet does not add target disambiguation, Expo-generated native metadata, permission completeness or native build guarantees. A candidate disappearing after discovery retains the existing ENOENT result rather than introducing a retry.

## Package and repository context

The observed package is `@prasenjeet/shipli` 1.3.0, ESM, Node >=18, with CLI and MCP entry points and existing `fast-glob`, `plist` and MIT dependencies/license. No dependency, package manifest, lockfile, prompt, scanner or executable entry point is changed. The observed repository root and pinned PR15 src directory contain no AGENTS/CONTRIBUTING file. All twelve observed repository PR rows included no contribution by the connected account; PR14 and PR15 were both open external submissions. The exact Commons Shipli PR search returned zero matches, and the public Slack Shipli query reached provider END with zero results. Those observations are bounded source/activity checks, not a global absence claim.

## Apply and validation boundary

Apply `change.patch` to the exact PR15 preimage above. The adjacent `src/plist-reader.js` is the complete resulting file, and `LICENSE` preserves the MIT text. Do not replace another contributor's branch or submit a new upstream claim from this packet.

Static validation retained the full original/postimage, independently computed their Git blob identities, and parsed/applied the serialized one-hunk patch to the original bytes. That produced the complete postimage exactly: +8/-9. No production function, Node/CLI/MCP process, glob, plist parser, synthetic project, test, build, workflow, filesystem probe, native device or API audit was executed. Author-reported verification in external PR bodies is not a new result from this continuation.

The initial internal activity-read request had a pre-provider argument validation error (`thread_ts` instead of `message_ts`); it sent no read. The corrected equal-bound request returned only the parent, so no claim readback is inferred from it. A subsequent explicitly overlapping read returned the claim and matched the complete requested body after removal of the one observed provider-added ChatGPT attribution footer. The source/publication record retains this distinction.

## Funding and external coordination

The owner-authored issue body explicitly offers **500 INR** for a complete and accepted implementation and asks contributors to comment before starting so work can be coordinated. All sixteen issue comments were read; they are third-party interest/attempt/submission messages and do not establish a sponsor acceptance or new assignment. No sponsor contact, claim, upstream PR, account/payment action or award assertion is made here. The amount is not converted into or counted as a USD15+ lead. The broader React Native issue and its existing external contributions remain separate from this narrow source maintenance packet.
