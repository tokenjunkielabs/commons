# Derive release identities from the retained publisher result

`host/connected_publication_identity.cjs` provides `formatGitHubPublicationIdentities(publication)`, a pure formatter for the identity fields already returned by the connected GitHub publisher. It avoids manually recopying a head, merge, readback ref, or PR URL into release prose.

The concrete motivation was the original Slack release for Commons #31839: a manually transcribed head SHA omitted one middle digit. The Slack comparison correctly matched the authored message; it was not responsible for verifying that the author's copied SHA matched the publisher result. The same Slack message was subsequently corrected from retained `publisher.commit_sha` and fully read back. That historical release is not reformatted, resent, or replayed by this work.

## Existing surfaces and bounded qualification

The existing publisher returns the needed structured identities. Its source and guide were inspected from retained custody at blobs `405da1680c690e75e066ac4d9079d794e9989dbb` and `4360abc1c5e47989955abfe3db940786bb76c3f4`. They document native journals, immutable readbacks and named-main alias receipts, but do not format a release identity block.

A retained historical host inventory contained 975 entries. It predates the operation recorder and is not a current repository census. The following public receipt-related implementations were acquired completely at their exact retained blob pins and independently identified:

| Source | Blob | Existing role |
| --- | --- | --- |
| `host/slack_receipt.py` | `c913f55d3e57b1cb3e55b4a3fa2061b5ae0ae88c` | Classifies a particular historical receipt/catalog/tree-presence case. |
| `host/strict_receipt.py` | `1bd433e22c2b6f7f85860bb2c76bb0670f235d83` | Validates experiment panels, scores, and canonical provenance. |
| `host/commons_slack_full_body.py` | `63d755c93d2ee3f8b919015053d3efb769d361e2` | Formats existing post bodies for a Commons/Slack mirror; its input is a post file or text. |
| `host/commons_slack_full_body_ship.py` | `7c827b22111d1db768aef9d319ffbf69dab01659` | Drives that historical mirror's filesystem/subprocess ship checks. |

The retained complete export list for `connected_slack_publish.cjs` at `f0d00f385290ff37dc807262a0476799dfcd3de3` consists of publication, readback, and comparison functions, with no message formatter. Its source was not reacquired or changed for this addition. The inspected contracts do not provide the required publisher-result-to-identity-block function; this is a bounded source assessment, not a claim that every receipt-related file or future branch was searched. Private-topic receipt sources were not inspected.

All existing publisher, recorder, Slack publisher, comparison and receipt modules remain unchanged. This addition does not adopt any historical receipt classification or execution policy.

## Interface and use on a fresh publication

```javascript
const {formatGitHubPublicationIdentities} =
  require('./host/connected_publication_identity.cjs');

// publisherResult is the actual retained result of the new publication.
// Existing source/readback/final checks are completed separately.
const identities = formatGitHubPublicationIdentities(publisherResult);

store(actualPrivateIdentityReceiptKey, {
  publisher_result_key: actualPublisherResultKey,
  formatter_source_blob: adoptedFormatterBlob,
  identities,
});

const releaseText = [
  preparedOutcomeAndBehavior,
  identities.text,
  preparedValidationAndLimits,
].join('\n\n');

// Supply releaseText unchanged to the existing authorized Slack operation.
// Retain and compare that operation with the existing publication tools.
```

The example contains caller variables, not a fabricated publication or executed fixture. Pure-V8 callers can adopt the complete identified CommonJS source using their existing loader; the module performs no source loading of its own. Call it once for the genuinely new release being prepared. Do not run it against an old accepted release to create first-use evidence.

The result has `schema: "commons.github_publication_identities/v1"`, a readable `text` block, selected `fields`, three local `relationships`, a `disagreements` list, counts, fixed limits, and explicit scope. Keep the result attached to the actual publisher-result locator. The formatter does not discover private custody keys or authenticate the retained object.

## Exact field mapping

| Record | Source path | Text label |
| --- | --- | --- |
| `repository` | `publication.repository_full_name` | Repository |
| `pr_number` | `publication.pull_request.number` | Used only for the local URL relationship. |
| `pr_url` | `publication.pull_request.url` | PR |
| `head` | `publication.commit_sha` | Head |
| `pr_head` | `publication.pull_request.head_sha` | PR head |
| `merge` | `publication.merge_sha` | Merge |
| `readback_ref` | `publication.readback_ref` | Readback ref |

Every present value is copied literally. The formatter does not shorten SHAs, change case, trim strings, reconstruct an absent URL, or fall back from one head field to another. SHA fields must have the publisher's 40-lowercase-hex shape. Repository names and GitHub pull URLs have bounded literal syntax; checking that syntax does not establish that the repository or PR exists.

Each selected field records its source path and one of `present`, `missing`, `null`, or `invalid`. A missing own field differs from an explicit null and from an invalid value. Missing/null/invalid pull-request parents retain that cause in the child record's reason and parent source path. Undefined is invalid. Selected accessor properties are reported invalid without reading the accessor. Malformed values and unrelated input fields are not copied into diagnostics.

The text prints `unknown (missing)`, `unknown (null)`, or `unknown (invalid)` for unavailable identities; it never substitutes an empty or shortened SHA. The seven metadata records remain the detailed account of what was read. A non-plain root input throws a local TypeError. Inputs are caller-owned ordinary JSON-like publisher results; proxy objects or hostile language-level objects are outside the contract.

Three relationships are evaluated only when all necessary selected fields are present:

- `commit_sha` equals `pull_request.head_sha`;
- `merge_sha` equals `readback_ref`;
- the literal PR URL equals the URL corresponding to the supplied repository and PR number.

A known inequality is included in the text as an identity disagreement and retained structurally. Unknown relationships are null, not false or successful. Equality is only a comparison of supplied metadata; it is not a provider, content, merge, or acceptance verification.

## Bounds and omitted scope

The function inspects exactly seven scalar field positions and their one pull-request parent. Repository text is at most 201 characters; PR URL text at most 512; a PR number must be a positive safe integer; SHA values have the fixed shape above. Output text has a fixed 4096 UTF-16-character cap and is never silently truncated. The formatter does not traverse input file arrays, source bodies, native errors, request arguments, or arbitrary extra fields.

It deliberately generates no completion/status verdict, source-origin claim, file verification, authentication conclusion, current-main statement, owner/admission decision, or upstream acceptance assertion. Main observation receipts differ across real callers: some use a fresh named ref plus immutable equivalence, while others retain separately read literal-main files after the branch advanced. This first API does not normalize or certify either path. Keep those actual observations and their time/provenance in separately prepared prose or structured receipts.

The function also cannot detect every wrong-but-well-formed input. If a caller fabricates or manually alters the publisher result before passing it in, syntax and equality do not recover the original truth. Supply the unchanged retained result, keep its locator, and continue the existing exact publication and readback checks.

No native bindings, filesystem, network, clocks, retry, send/edit behavior, access rules, or publication protocol are introduced. Formatting failure does not authorize repeating a writer. The existing Slack comparison remains responsible for matching the intended authored text and target under its explicit normalization mode; this formatter merely derives one portion of that text from structured identities before the message is sent.

## Validation and first-use boundary

At source authoring, this formatter has not been invoked. No synthetic input, fixture, test suite, old-release replay, provider call, or runtime experiment was used to exercise it. Source review covers the seven selected fields, bounded formatting, exact string preservation, missing/null/invalid distinctions, and local conflict handling.

The intended first consumer is this new source-and-guide packet's own forthcoming release: after its ordinary guarded publication, complete immutable identities and final checks, format that new publisher result and retain the generated block before sending. Any actual result will be recorded operationally with the new publication receipt. Unavailable-field, disagreement, invalid-input and limit branches remain unexercised unless a real future operation supplies them. No status-only amendment or historical reformatting is required.
