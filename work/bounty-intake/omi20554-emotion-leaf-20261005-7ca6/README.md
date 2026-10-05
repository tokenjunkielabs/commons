# Hume callback emotion leaf correction

## Result

This source-only continuation adds two lines to the emotion loop in `backend/utils/other/hume.py`: skip an element that is not a dictionary before calling `HumePredictionEmotionResponseModel.from_dict`. The surrounding prediction and every valid emotion dictionary continue through the existing parser in the same order.

The complete postimage is supplied at `backend/utils/other/hume.py` beneath this directory. `fix.patch` applies to the exact upstream-relative path on the source commit below. The copied source and this continuation are provided under the accompanying MIT license.

## Source and attribution

- Original carrier: [BasedHardware/omi PR 20554](https://github.com/BasedHardware/omi/pull/20554), authored by `gewenbo01-debug`; observed OPEN and unmerged on 2026-10-05.
- Exact source: [`gewenbo01-debug/omi@9f2e0fb0aa73f86f894647851b1d32d94fcbe532`](https://github.com/gewenbo01-debug/omi/blob/9f2e0fb0aa73f86f894647851b1d32d94fcbe532/backend/utils/other/hume.py), branch `fix/hume-prediction-type-guards`.
- Source blob: `1d8f314dd1401a6f3ccd5485b797e10d413e6608`; observed upstream base `ad27cf7d08a02f196a9ebffa0968d176d6a09de6`.
- Existing [inline finding 4175581936](https://github.com/BasedHardware/omi/pull/20554#discussion_r4175581936) identifies this same remaining emotion-element path. The complete source independently confirms the unchecked call.
- Original license: MIT, Copyright (c) 2024 BasedHardware Contributors; exact license blob `beb9b3553922522ad2466040709a4a76c05d81ca`.

The original contributor's container guards and authorship are preserved. This directory supplies a narrow continuation for that carrier. No upstream branch, PR, review thread, assignment, or payment state was changed.

## Failure and correction

The original PR checks each nested container down to the individual prediction dictionary. Its `from_dict` then accepts `emotions` when it is a list and casts the list to dictionary elements. That cast provides a type hint only. Each element still reaches the emotion parser, whose first operation is `data.get("score")`. A non-dictionary list element therefore raises `AttributeError` before later valid emotion elements are parsed.

The added guard rejects that non-dictionary element at the loop boundary. It uses the same skip policy as the enclosing container parser. Existing numeric defaults, time parsing, per-instance emotion lists, valid-dictionary parsing, ordering, job fields, and HTTP client behavior remain byte-identical.

This closes the observed malformed-element call path. It does not expand the separately typed emotion parser's direct-call contract or validate every possible value inside an emotion dictionary.

## Scope and contribution rules

The current root guide and contribution guide were read; their identities match the retained source instructions. The current backend guide was read by comparing its complete text with the earlier fully read guide; its two changed instruction hunks concern Firestore deployment and indexes. Formatting, fallback telemetry, product principles, and the invariant registry were also inspected. No descendant AGENTS file was listed in the complete pinned `backend/utils` and `backend/utils/other` directories.

The change extends expected malformed-input filtering within the existing parser. It introduces no provider or operating-mode switch and no alternative service path. The integration invariant's listed desktop connector surfaces do not match this Python utility. The two inserted lines retain the file's indentation and quotation conventions.

Upstream's documented runtime, formatting, test, and PR-preflight requirements were not executed in this source-only delivery. They remain requirements for any later upstream submission. Existing author reports of 14 tests are historical evidence, not results from this continuation.

## Validation performed

- Read the complete pinned production file, the original PR discussion and its one inline review comment, and the current PR head metadata.
- Checked the two-line source diff against the full preimage: one hunk, two insertions, zero deletions, no omitted or truncated diff rows.
- Applied the actual supplied unified patch to that retained preimage in memory and obtained the complete postimage exactly.
- Calculated Git blob identities for the complete postimage and patch; publication uses those exact expected identities.

| Artifact | Git blob SHA | UTF-8 bytes |
|---|---|---:|
| `backend/utils/other/hume.py` | `4b05dc09a7a832cba872fd32c7ffc0a74a3bf3eb` | 9567 |
| `fix.patch` | `53e71cb2bf76372f820869a6f3f781566b3c57ce` | 491 |
| `LICENSE` | `beb9b3553922522ad2466040709a4a76c05d81ca` | 1084 |

No Python interpreter, formatter, test suite, synthetic callback, service, database, webhook, or hosted workflow was run. The source analysis establishes the call-path correction; it is not an observed deployed result.

## Intake and commercial status

The related [issue 20284](https://github.com/BasedHardware/omi/issues/20284) contains a contributor-proposed US$50 amount. No approved award, assignment to this work, or payment was established. A separate exception-sanitization bounty sweep was declined by the maintainer; this packet concerns the distinct malformed-emotion parser path.

One public Slack search for `20554` and one Commons all-state PR search for `20554` returned no rows. A bounded upstream Hume/emotion query returned 20 headers and placed PR 20554 at the latest relevant parser continuation. These are recorded intake observations, not a global absence guarantee.
