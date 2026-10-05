# Check async Promise fallthrough in flow-runtime PR306

Target: [gajus/flow-runtime issue2](https://github.com/gajus/flow-runtime/issues/2). Existing contribution: [PR306 by landeqiming666](https://github.com/gajus/flow-runtime/pull/306).

## Concrete gap and correction

The existing Function visitor has two return-annotation paths. Ordinary functions enter the branch containing synthetic-return insertion. Async generic return annotations enter the earlier getFunctionInnerChecks branch, which defines a return checker but does not insert a return at fallthrough.

For example, a block-bodied async function annotated Promise<string> can reach the end without an explicit return. JavaScript resolves its promise with undefined. In the recorded source, the Function visitor builds the existing string-or-Promise<string> return checker, but there is no ReturnStatement for the later visitor to instrument on that path.

This packet adds nine lines inside the existing returnCheck block. Only when the function is async, is not a generator, and the existing getPromisedType helper recognizes Promise<T>, it appends a bare ReturnStatement to a block body that is empty or whose final statement is not a ReturnStatement. This follows the same insertion phase and mechanism as the existing ordinary-function implementation.

The existing ReturnStatement visitor then passes the implicit undefined value to the existing checker. No new assertion implementation or type-conversion rule is introduced. A type admitting undefined retains that behavior. The existing suppression, visited-node and disabled-check guards remain unchanged, so the insertion is not repeated on a visited function.

## Preserved boundaries

- A final explicit return is not duplicated or rewritten by this new block.
- Generators and async generators are excluded.
- Synchronous Promise-return handling remains byte-identical.
- Expression-bodied arrows do not have the block statement array required by this insertion.
- The correction does not perform control-flow analysis. A return appended after an unconditional throw or a nonterminating loop is unreachable; no executed path coverage is claimed.
- The existing return checker determines explicit Promise and value semantics; this packet does not broaden those guarantees.
- CI's separate TypeCastExpression change for issue180 is not part of this complete-file postimage. Integrators must reconcile disjoint hunks rather than overwrite another source packet wholesale.
- The issue177 Map conversion packet touches convert.js and is likewise separate.

## Exact source basis and authorship

| Item | Identity |
| --- | --- |
| External PR306 head | 3a8e5cc784873a6b574aa724cd82486494235cf5 |
| PR306 recorded upstream base | a9b7e1da4a655be52a4eb8949644a257e1f75f33 |
| Original transformVisitors.js | 1d8b0ad5885b293b1603cee0c032d03371446d5f |
| Upstream MIT license retained in this packet | dc87e124ecd62968c037cb8f40c229478c40db2f |

The complete 29,535-character source was retained before inspecting Function, ReturnStatement, getPromisedType and getFunctionInnerChecks. The recorded file already includes landeqiming666's corrected ordinary-function last-statement condition and generator exclusion. Both remain unchanged.

Existing related contributions retain their authorship: [PR249](https://github.com/gajus/flow-runtime/pull/249) is the merged original implicit-return implementation; [PR301](https://github.com/gajus/flow-runtime/pull/301) was closed unmerged; [PR302 by szw9999](https://github.com/gajus/flow-runtime/pull/302) remains open at b89c606c6268caa6528aa82365b4174e65ec92a3 and corrects the ordinary-function condition. The current PR306 metadata remains open/unmerged at the pinned head. Its sole conversation comment is an author follow-up, with no reported inline review comment.

The current issue is open and unassigned. Its complete three-comment discussion includes the maintainer's low-priority assessment and [historical $20 funding comment514631071](https://github.com/gajus/flow-runtime/issues/2#issuecomment-514631071). IssueHunt submission remains a separate requirement. Public source ownership and the current successful all-state upstream author search were reused from the same qualification window; no duplicate own-PR query was made. These observations are bounded source evidence, not a new award, payment or platform-eligibility assertion.

## Delivery and validation

The packet contains the complete production postimage, a one-hunk unified patch with nine added lines and no deletions, this guide, and the upstream MIT notice preserving the 2017 codemix.com copyright.

The serialized patch was applied independently as a text transformation, checking each original context/removal and the resulting full postimage. Publication verifies full immutable and current-main text, Git blob identities, exact PR path set and merge parents.

No compiler, Babel transform, native process, test, fixture, build, package installation or workflow was run. The example above is a source-derived trigger, not an executed reproduction; no ordinary-JavaScript parser result is claimed for this Flow-annotated source. Existing external test claims remain attributed to their authors and are not new validation for this addition.

Apply only after reconciling the exact PR306 preimage and other concurrent source hunks. No upstream PR, branch, comment or IssueHunt action was created. The Commons packet is a source-delivery artifact, not a claim that the entire issue is accepted or paid.