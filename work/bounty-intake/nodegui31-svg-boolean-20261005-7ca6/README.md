# NodeGUI SVG: quote true-valued XML attributes

## Production change

This packet repairs one serializer statement in the existing [SVG contribution, react-nodegui PR390](https://github.com/nodegui/react-nodegui/pull/390). Its `SvgPrimitive` type accepts booleans. The serializer already converts a retained value to a string, but its final append special-cases `true` into a bare attribute name. The resulting XML omits the required equals sign and quoted value.

The changed statement always appends the existing escaped, quoted value. A retained true-valued attribute therefore has the form `name="true"`. This follows XML 1.0 section 3.1: an attribute comprises its name, equality separator and delimited value. Qt documents the byte-array overload of `QSvgWidget::load` as accepting a serialized XML representation of SVG. This is a source-level grammar correction; no Qt rendering failure or successful native render was reproduced here.

The complete production diff is one hunk, **+1 / −1**. Every other source byte is preserved. The existing treatment of false, null and undefined (omission), property filtering, attribute-name mapping, style serialization, escaping, namespace insertion, text serialization, child moves and widget lifecycle remains unchanged. This does not redesign the broader boolean/ARIA contract.

## Contents and use

| File | Purpose |
| --- | --- |
| `source/src/components/Svg/RNSvg.ts` | Complete postimage of the contributor's production file, including only this one-line correction. |
| `boolean-attributes.patch` | Unified patch against the exact PR390 source preimage below, preserving mode 100644. |
| `LICENSE` | Unmodified upstream MIT license, copyright 2019 Atul R. |
| `README.md` | Attribution, source identities, rationale and integration limits. |

Apply the patch to a checkout containing the pinned PR390 preimage, or integrate the one changed statement into that contribution. The copied file is not a standalone SVG implementation: its existing imports, component configuration and reconciler support come from that PR. A different source revision needs a fresh source comparison before integration.

## Source identities and attribution

Observed on 2026-10-05:

| Source | Exact identity |
| --- | --- |
| Canonical repository | `nodegui/react-nodegui` |
| Existing PR390 author and fork | `bpc-oss`, `bpc-oss/react-nodegui` |
| PR390 head | `877fa355f92e9619158423c95994f5e246e52da0` |
| Canonical base at the observation | `87c844050c86e0eb548c3e6e8c57bd40d5174546` |
| Original `RNSvg.ts` Git blob / UTF-8 bytes | `8f42815b4835cf903bbea2a74b2936055e83acd8` / 15,562 |
| Changed `RNSvg.ts` Git blob / UTF-8 bytes | `49eef0d3c1135f3e02ba6ff1c8b8926804a0e8f0` / 15,529 |
| Source directory tree / file mode | `8cdb32cc6dcb998ed5d61f04563fc01bbbce3347` / `100644` |
| Upstream license blob | `abfb6db7ba282b912297966dbcdc897e20ee661f` |
| Linked organization contribution guide blob | `cafb12dfca226c26ba452eaaaa7da4927e280279` |

The NodeGUI project and Atul R retain the original attribution. The earlier [PR389](https://github.com/nodegui/react-nodegui/pull/389) is by `jamilahmadzai` (head `fd7732b228823e286ff15ff36466716e5cc6bb4d`). The inspected PR390 by `bpc-oss` supplies the complete SVG implementation and its text/reorder changes. Those contributors' feature work is not represented as new work in this packet.

[Issue31](https://github.com/nodegui/react-nodegui/issues/31) remained open and unassigned; PR390 remained open and unmerged. The issue's historical IssueHunt $20 label is context, not confirmation of current escrow, eligibility, an award, or payment. This packet does not complete the entire SVG issue or establish upstream acceptance. No new upstream PR, issue comment, platform claim, contributor contact or payment action was made.

## Validation scope

The complete original source was retained and matched its Git blob identity. The source directory tree independently binds the same blob and regular-file mode. A complete text comparison found one changed line; an independent pass over the serialized unified patch reproduced the entire postimage from the retained preimage. The changed JavaScript statement was parsed without invocation.

This does not constitute a TypeScript build, dependency compatibility check, XML parser execution, Qt/NodeGUI run or graphical acceptance. No tests, fixtures, acceptance scripts or workflows were added or run, and no prior contributor execution claim is adopted as our result. Publication readbacks establish the committed source identity only.

## Primary references

- [Pinned PR390 production source](https://github.com/bpc-oss/react-nodegui/blob/877fa355f92e9619158423c95994f5e246e52da0/src/components/Svg/RNSvg.ts).
- [XML 1.0, section 3.1 and Attribute production](https://www.w3.org/TR/xml/#NT-Attribute).
- [Qt 5.15 QSvgWidget documentation](https://doc.qt.io/archives/qt-5.15/qsvgwidget.html).
- [NodeGUI contribution guidelines](https://github.com/nodegui/.github/blob/master/CONTRIBUTING.md).
