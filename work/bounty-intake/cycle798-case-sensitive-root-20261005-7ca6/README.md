# Cycle.js #798: case-sensitive root identity follow-up

This packet corrects one remaining root-reuse decision in the existing external PR [cyclejs/cyclejs#1029](https://github.com/cyclejs/cyclejs/pull/1029). It is a static production-source continuation, not an upstream submission or a claim that issue #798 is fully accepted.

## Concrete behavior

The retained `VNodeWrapper.call` considers a virtual node identical to the render container only after comparing its tag, ID and class string. PR #1029 normalizes absent selector IDs to the empty string and preserves root isolation metadata. Its ID and class comparisons still uppercase both operands. Thus an id-less HTML container with class `App` and a virtual node with class `app` are treated as identical even though their literal class values differ. The same comparison conflates IDs such as `App` and `app`.

The postimage compares IDs and class strings exactly. A mismatch follows the existing wrapper path, preserving the container and placing the virtual node inside it. Tag-name comparison remains case-insensitive. No class-token sorting, whitespace normalization or coercion is introduced; equivalent reordered class strings can still take the wrapper path, as before. The absent-ID default, normal id-less reuse, DocumentFragment guard, null handling and root isolation metadata remain byte-for-byte unchanged.

This is source reasoning from the complete pinned implementation. No DOM was created and no browser behavior was executed.

## Exact source and attribution

- Original issue: [cyclejs/cyclejs#798](https://github.com/cyclejs/cyclejs/issues/798), OPEN and unassigned in the retained observation. Its six comments were read completely.
- External carrier: PR #1029 by **jamilahmadzai**, OPEN/unmerged at head `4b2f8ea990c20ef7ccb27d69b7c4e79f7e6fa892`, recorded master base `5ece2a48c3659538208da3dc8d43a142bc0d91a7`.
- Full preimage: [dom/src/VNodeWrapper.ts](https://github.com/cyclejs/cyclejs/blob/4b2f8ea990c20ef7ccb27d69b7c4e79f7e6fa892/dom/src/VNodeWrapper.ts), Git blob `136afead2c1edc82d432f8267663a0a241fed993`.
- Full contextual utility source: `dom/src/utils.ts`, blob `3be23c80051d17e8c418f2a6679be0e1485f8a02`, at that same head; `isDocFrag` checks node type 11.
- Prior contributors and carriers are preserved: bloodyKnuckles' #796 and landeqiming666's #1025. The latter's complete production diff was read; #1029 adds the isolation preservation this packet retains.
- The repository's original MIT license, blob `27a28fd7151bb98a45ef374e5bc486eba99afcef`, is copied without modification.
- The original issue records historical $40 funding in [IssueHunt comment 444064735](https://github.com/cyclejs/cyclejs/issues/798#issuecomment-444064735), dated December 4, 2018. This is amount provenance, not current escrow, eligibility, acceptance or payment.
- A bounded exact public `cyclejs` + `798` search returned only the existing BATCH25-05 row; native own-account PR search `is:pr author:woahwhattheheck repo:cyclejs/cyclejs` returned an empty list. These observations are not a universal ownership census.

## Packet and static verification

`source/dom/src/VNodeWrapper.ts` is the complete proposed postimage, Git blob `56d9bcee0ee6be42ec436a903d122e38a0cafdb3` (1,990 UTF-8 bytes). `root-identity.patch` is relative to the external PR head above: one hunk, +2/-3. An independent serialized patch application matched the complete postimage exactly. Full UTF-8 Git identity and text readbacks bind the publication.

The remaining three production comparisons keep their original ordering and short-circuit behavior. No other production file, upstream branch, test, fixture, workflow, dependency or configuration is modified.

The upstream [contribution guide](https://github.com/cyclejs/cyclejs/blob/4b2f8ea990c20ef7ccb27d69b7c4e79f7e6fa892/CONTRIBUTING.md), blob `ba359417dd734629079748df422a27ec2282603b`, calls for local builds/checks and its commit flow before an upstream PR. Those steps were not performed: this session's executor, builds and tests remain off. Browser/runtime verification and any legitimate external submission are unresolved follow-through for the existing carrier; no maintainer contact, platform claim or bounty acceptance is implied.

Operation: `CYCLE798-CASE-SENSITIVE-ROOT-20261005-7CA6`. Original internal activity: C0BU51F1PL3 / `1791180622.284519`, responding to BATCH25-05 rows 15–19.
