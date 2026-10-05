# Compare notification generations by their timestamps

This source packet corrects duplicate-generation selection in the existing [bounty-concierge #861 notification queue](https://github.com/woahwhattheheck/bounty-concierge/pull/861), authored and merged in the controlled fork by `woahwhattheheck`. It is internal source maintenance, not a sponsor claim or a review package for a competing bounty submission.

## Source custody and original behavior

The original PR is merged at `b6ea4554c1e43f0b2ec62facec8c877c44497e75`, from head `f67df94193b523f0f78955da584e7aab000e4674`. Its public release describes a compiler that consumes retained Notifications API JSON, selects the newest copy of each thread before filtering read notifications, then emits a bounded priority queue and deduplicated exact API URLs. Original authorship and those capabilities remain credited.

Current main was acquired at `bfff853a125aebf76275e75e981a417eff7b5b2a`. The complete 1,222-entry tree `c97a76a52e89995839f40838d6a03989c325786a` is untruncated. The full current production file `concierge/github_notification_queue.py` is blob `60cbd598e9e866d5a7559a84d1bbcc8faef3c5c8`, 9,657 bytes, unchanged by the subsequent cooldown work. The actual pyproject entry point maps `concierge-notifications` to this module's `main`.

## Source defect and repair

The timestamp parser accepts timezone-aware ISO text, converts it to UTC and serializes with the default `datetime.isoformat()` precision. Duplicate selection then compares the serialized strings with `>`.

Python's [datetime documentation](https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat) specifies that the default precision omits fractional seconds when microseconds are zero and includes them otherwise. For two accepted instants within the same UTC second, the later fractional form contains a period where the earlier whole-second form contains `Z`. Their string ordering is therefore opposite to their chronological ordering. Depending on arrival order, the older generation can displace or suppress the newer one. Because unread filtering happens afterward, this can preserve an older unread copy after the later copy was marked read, or suppress a later unread copy.

This is a defect inferred from the full source and the documented format contract. No actual notification exhibiting it, deployed failure, synthetic payload or runtime reproduction is claimed.

The patch compares the two already validated UTC values as aware datetime objects instead. The documented datetime ordering compares instants. It does not convert them to floating-point epoch seconds or change their public text representation. The short-circuit for a previously unseen thread is preserved. Equal instants retain the original first-copy tie policy.

The one production hunk is +6/-1. Every other source byte remains exact: timestamp validation and serialization, unsupported-type handling, unread filtering, reason/subject priority, existing final queue sorting, limits, URL deduplication, output schema and the no-provider/no-acceptance fields. Equal-update conflict policy, general timestamp-range handling and final-sort floating-point precision are outside this narrow change.

## Packet and source-only checks

- `concierge/github_notification_queue.py` is the complete modified module.
- `generation-time.patch` applies to the full original source path.
- `LICENSE` preserves the complete MIT notice and CRLF bytes.
- This guide records integration and evidence limits.

The prepared module is 9,942 bytes, blob `a0d007c4a2e56d05048cd1087db8d6a3f81932b2`. Pure text reconciliation confirms exact forward and reverse application of the serialized patch and exact bytes outside the intended replacement. Native source identity and independent Git-blob identity agree. No Python source was executed or syntax-compiled.

The root AGENTS.md (`4bff17819cb6f83f1e79df2607b12023e1c6ee36`) and CONTRIBUTING.md (`f953f75d0efa6897fe8adef66f4dc64e41d8e939`) were read in full. The latter preserves production delivery without recreating the removed test-suite infrastructure. The full source tree contains no nearer instruction or license file for this module. Root MIT LICENSE is `b19d0ab1000f055c9e1d1a40d0d1e43e0707ac9e`; the module's MIT SPDX notice is retained.

Publication is a separate Commons source packet. The original bounty-concierge branch, installed command and active cooldown/audit paths are not modified by this packet. Adoption requires applying the exact patch to a compatible source version.

No tests, fixtures, runtime, provider notification reads, credential/environment access, network queue execution, upstream submission/contact or payment action occurs. The prior author's reported execution is historical, and the explicitly blocked test-file routes and separate status-CLI credential edit remain held. No performance, deployed behavior, maintainer authorship, acceptance, reward or merge-payment result is inferred from a notification.
