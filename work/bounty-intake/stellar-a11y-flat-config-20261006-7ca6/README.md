# Connect the accessibility policy to the dedicated lint command

Prepared 2026-10-06 from Stellar-Analysis/frontend at `482ee456369418ef82c4056718cb82d3468f762b`. This is an attributed Commons source continuation for the existing accessibility lint entry point.

## Problem and resulting behavior

The package command currently supplies `--rule 'jsx-a11y/*: error'`. ESLint's rule option takes named rule IDs and their configuration; that string names a literal wildcard rule rather than selecting the plugin's rules. The existing flat configuration loads Next's base configurations but does not read the repository's separate `.eslintrc.a11y.json` policy.

The patch points the dedicated command at a new `eslint.a11y.config.mjs`. The command retains `--ext .tsx,.ts` and the `src/` target. The adapter starts with the existing flat configuration, merges the plugin's recommended rules with the 32 exact explicit policy rules, and appends the existing test-file override last. Its module-relative URL reads the policy beside the adapter. It does not depend on the invoking directory to locate that JSON file.

The explicit policy wins over recommended defaults. Existing severities and complete option arrays remain intact, including the custom component mappings. The final override keeps `jsx-a11y/no-autofocus` disabled for the existing `**/*.test.tsx` and `**/*.test.ts` patterns.

## Scope

Only one existing line changes in `package.json`; the new adapter is 19 lines. The complete patch contains two hunks, 20 additions and one deletion. The base configuration, legacy policy, package dependencies, lockfile and workflows are unchanged.

The plugin is already a direct development dependency at version 6.10.2. The retained lockfile resolves it as `6.10.2(eslint@9.39.5(jiti@2.7.0))` and also uses that plugin version for Next's configuration. No installation or dependency repair is part of this change.

The adapter reads the recommended rules without registering another plugin object or replacing the parser. The existing Next configurations keep their file patterns, parser, settings and ignores. Legacy top-level `extends` and string `plugins` entries are not forwarded into flat configuration. The current override contains only `files` and `rules`; this adapter is not a general legacy-configuration converter.

## Exact source identities

All source paths below are relative to the pinned donor repository. Complete UTF-8 source strings were acquired, with native blob identities and independently computed Git blob hashes matching.

| Source path | Original Git blob | Bytes | Result |
| --- | --- | ---: | --- |
| package.json | 2b1c6ac1f83096666c7fd6d5ba3fd22780e6b8eb | 3,119 | 6c85848de90912ce38f69e2376ef8cdc1ecc9367; 3,124 bytes |
| eslint.a11y.config.mjs | Absent from the complete 33-entry root directory listing | 0 | 7a15db012151f0d0e27ff9d1be1d7da8dbeb5d89; 519 bytes |
| eslint.config.mjs | 759a1e7c8f10f4b082b542cc3a2311775c3fbb65 | 521 | Unchanged |
| .eslintrc.a11y.json | a2b135a1a6dd40468ad34fd23801a13d7a7e8072 | 3,655 | Unchanged |
| pnpm-lock.yaml | 7ecba249d1b7cd41e629e2fff2782ed6805186f5 | 359,885 | Unchanged |

Both changed paths use mode `100644`. The new-file patch has a `/dev/null` preimage and a zero old-line count. The patch itself is 1,467 bytes, Git blob `f68c725df8388894e8a3320667e9d89e72339cb3`.

## Verification and remaining limits

The actual serialized patch was parsed and applied to the exact retained preimages. Both forward materializations matched their complete intended postimages, and both inverse applications recovered their exact originals. Every hunk and row was included with no truncated line. A structural manifest comparison confirmed that only the dedicated lint command changed. These are text and identity checks on the proposed source.

No ESLint configuration was imported or executed. No lint, package installation, build, accessibility suite, browser or CI run occurred. Configuration resolution with the locked dependency installation and the resulting lint findings remain unverified. Activating the existing rules can expose existing findings; this packet does not claim a passing lint run or accessibility compliance.

No upstream branch, pull request, issue claim, acceptance or reward action is included. Commons publication makes the patch and its provenance reviewable; applying it upstream is a separate action. Existing source changes elsewhere in the fleet are not incorporated or replayed here.

## Attribution and retained notices

The original manifest and accessibility policy belong to the contributors of [Stellar-Analysis/frontend](https://github.com/Stellar-Analysis/frontend/tree/482ee456369418ef82c4056718cb82d3468f762b). The original configuration is retained; this continuation supplies the explicit flat-config bridge and command change. No claim of sole authorship of the donor source is made. The latest inspected history entry for the policy path is [59fad72d9fbef9cfd6f47e215392da44488fcdc4](https://github.com/Stellar-Analysis/frontend/commit/59fad72d9fbef9cfd6f47e215392da44488fcdc4), authored by christabel888 on 2026-09-12, which records moving the frontend into the repository root; it is not a claim of original authorship of every rule.

The packet copies all three inspected donor notices verbatim, preserving their distinct filenames and line endings:

| Packet notice | Donor path | Git blob | Bytes |
| --- | --- | --- | ---: |
| upstream-licence-mclaughlin.md | docs/LICENCE.md | 57740b9d4d86aedf5d518f2f363d5cf192c54127 | 1,104 |
| upstream-license-menke-laguna.md | docs/LICENSE.md | af5411fa243cfcf2b61c79d081dbb6204e956041 | 1,111 |
| upstream-license-de-wet.md | docs/license.md | 4a766e268772888af5df56c3f6c608f68558b789 | 1,080 |

These files retain the named holders' notices. Their presence is not a finding that one notice governs every file in the repository.

## Primary technical references

- [ESLint command-line interface](https://eslint.org/docs/latest/use/command-line-interface): the `--rule` option specifies rule IDs and configurations.
- [ESLint flat configuration files](https://eslint.org/docs/latest/use/configure/configuration-files): rule configuration and ordered configuration objects.
- [Next.js ESLint configuration](https://nextjs.org/docs/app/api-reference/config/eslint): composing the supplied configurations and overriding rules.
- [jsx-eslint accessibility plugin](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y): the default plugin object and `flatConfigs.recommended.rules` interface.

The retrieved documentation describes the configuration APIs. It does not substitute for execution against this pinned repository's installed dependencies.
