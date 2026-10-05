# Flow Runtime 207: keep runtime reuse at program scope

This is a source continuation of [dicnunz's existing PR 287](https://github.com/gajus/flow-runtime/pull/287) for [issue 207](https://github.com/gajus/flow-runtime/issues/207). The original contribution adds the `libraryImport: 'require'` option and retains the default ES module output. This packet fixes one scope error in its existing-binding reuse.

## Problem and change

The first-pass visitor shares one `ConversionContext` across the file. Its `VariableDeclarator` handler recognizes `require(libraryName)` inside any scope, assigns that local identifier to `context.libraryId`, and clears `context.shouldImport`. A declaration inside a function or block can therefore suppress the program's generated runtime declaration even though its identifier is unavailable to generated type calls outside that scope.

The two added conditions require the variable declaration's immediate parent to be a `Program`. Nested function, block, loop and other wrapped declarations continue through the original value-discovery loop without taking over the program runtime. If no eligible runtime binding was found, the existing attachment path remains responsible for adding it. Direct program declarations retain the original reuse behavior.

All 297 original source lines remain unchanged. There is one production hunk, +2/-0, in `packages/babel-plugin-flow-runtime/src/firstPassVisitors.js`. The first ancestry condition also handles a missing enclosing path without calling `isProgram()` on it.

## Apply to the existing contribution

Use the exact source revision below, or reconcile this small hunk if the contributor has advanced it.

| Source identity | Value |
| --- | --- |
| Existing contribution | gajus/flow-runtime PR 287, author dicnunz |
| Contributor repository | dicnunz/flow-runtime |
| Contributor head | a91148be3fafd29b5de6259660bfbc1220f731a0 |
| Observed base | a9b7e1da4a655be52a4eb8949644a257e1f75f33 |
| Production preimage | 2b92dc83f0f5561ff9e8e626fdf2d6da2188b84a, 9,160 UTF-8 bytes |
| Production postimage | 7a5dfaaa5e8051088128ffe08a1af54ab7a391fa, 9,248 UTF-8 bytes |
| Source file mode | 100644 |

Apply `runtime-scope.patch` from that checkout's root. The complete postimage is also supplied under `source/packages/babel-plugin-flow-runtime/src/firstPassVisitors.js`. `LICENSE.md` preserves the source's MIT notice, including the 2017 codemix.com copyright.

This packet preserves the contributor's import option, custom library name, top-level require reuse, identifier collision logic and all other visitors. It does not address ordering before an existing program-level initializer, reassigned bindings, shadowing of a reused program binding, or shadowing of `require`. Those broader cases need their own source work before claiming complete CommonJS coverage.

## Source basis and limits

The complete first-pass source, attachment helper, conversion context, option constructor, plugin entry point and standalone transform entry point were read at the pinned contributor head. The plugin entry point checks `shouldImport` after its first traversal; the standalone traversal uses the first-pass `Program.exit` handler. Both consume the same flag and library identifier. This is why the scope check belongs where an existing binding is selected.

The source ancestry follows the [Babel AST variable declaration model](https://babel.dev/docs/babel-types#variabledeclaration) and [program model](https://babel.dev/docs/babel-types#program). The pinned source already uses the same parent-path and `isProgram()` APIs elsewhere. The dependency manifest names the Babel 7 family; no Babel 8 compatibility is claimed.

Full source hashes, the regular-file tree entry, the complete text delta and independent application of the serialized patch to the retained preimage were checked. The rebuilt text equals the supplied full postimage. No target JavaScript, Babel transformation, compiler, browser, fixture, test suite or workflow was executed.

Issue 207 was observed open and unassigned; all five comments were read. PR 287 was observed open with no discussion comments. The other named proposal, [PR 294](https://github.com/gajus/flow-runtime/pull/294), was observed closed and unmerged; its separate `importType` option remains attributed to that proposal. The historical $40 funding notice is not an award or payment. This Commons source packet creates no new upstream contribution, platform submission, sponsor claim or acceptance event.
