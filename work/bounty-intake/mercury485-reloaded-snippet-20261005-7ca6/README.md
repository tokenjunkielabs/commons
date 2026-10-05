# Mercury: replace reloaded snippet registrations

Repeated `Mercury.Snippet.load` calls can load a saved identity that is already registered. The original method appends another instance, while `Snippet.find` returns the first match. Region editing and serialization therefore keep resolving the old options.

This continuation constructs the new instance, then replaces the existing first-match registry slot. New identities still append. Other identities, their order, the registry array object, the options schema and the existing unique-ID allocator stay intact. Constructing before replacing also leaves the earlier entry present if construction fails.

## Source and integration

- Repository: https://github.com/jejacks0n/mercury
- Source commit: `a6a7e8d3b924266aa39be73359aa5c73c81363e1`.
- Original `app/assets/javascripts/mercury/snippet.js.coffee` blob: `52d61fa63bd14bd6faa8d360a06abb37e0b43460`.
- `change.patch` changes only the existing load method (+4/-1). The full CoffeeScript postimage is included at its original relative path.
- Apply the patch to that pin or compose the hunk with newer source. Do not replace a newer implementation with the full pinned file.
- The original Jeremy Jackson license is retained in `LICENSE`.

The actual region implementation (`region.js.coffee`, blob `2bf0b24a74e1c33af8c5013d50bda2679c443f24`) resolves each serialized element through `Snippet.find`. The snippet region's edit action (`regions/snippets.js.coffee`, blob `18c4c02c6d5cc79603e98044e9862fc3c31e9ec5`) also resolves by identity. The README documents saved-snippet loading at `mercury:ready` and dynamically replaced content; PageEditor (`ce715c15a044efec478b768a57354d67f6daa73c`) uses the existing global Mercury instance when initializing an iframe.

## Limits

This is a source-level correction to repeated loads. It does not refresh an already open snippet-options modal or previously retained object references, redesign undo history, merge colliding identities from independent documents, or remap DOM identities. The caller remains responsible for loading the correct saved map and replacing content consistently.

Issue https://github.com/jejacks0n/mercury/issues/485 supplies a broader custom Rails persistence report with no follow-up comments. This packet does not establish that repeated loading caused that report or that its server integration is repaired. Existing merged PR158 addressed new-ID allocation; that allocator is already present and unchanged here.

The source README states this legacy version is no longer maintained by its author. The historical $15 Bountysource badge is not a current award, assignment or payment claim. No upstream branch or submission is changed.

## Validation

The current source, callers, documentation and exact text change were inspected. CoffeeScript compilation, browser editing, persistence, native execution and tests were not performed because the executor is unavailable. Runtime and upstream integration acceptance remain unperformed. Publication readback verifies delivered source bytes only.
