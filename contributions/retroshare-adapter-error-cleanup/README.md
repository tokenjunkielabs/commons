# Release the Windows adapter buffer when enumeration fails

This source packet adds one `free(adapter_addresses)` call to the existing Windows error branch of `getLocalAddresses`. If `GetAdaptersAddresses` returns an error after the successful 16,000-byte allocation, the buffer is released before the existing diagnostic and `false` return.

The allocation-failure return, successful enumeration and its existing cleanup, API flags, address filtering, Unix path and socket behavior retain their original bytes. This change does not add an overflow retry, interface selection, persistent network settings or an exception-safety rewrite.

## Source and related issue

- Canonical feature request: https://github.com/RetroShare/RetroShare/issues/865
- Current library revision: https://github.com/RetroShare/libretroshare/tree/7304d207877c2211aab60bfe128234d831852bc7
- Original source: https://github.com/RetroShare/libretroshare/blob/7304d207877c2211aab60bfe128234d831852bc7/src/pqi/pqinetwork.cc
- Original source Git blob: `aebf1b6736557d85cee16560bdb162f7f08e7864`.
- Modified source Git blob: `bdd3fe1253dfae95d037db34551948468d2284bc`.
- Unified patch Git blob: `7070dfb777a27f8dcaef904f6dc1ea555ce9575c`.

The broader issue requests an interface selector and saved binding policy. Its complete current body and five comments were read; they do not supply an implementation or establish that this cleanup resolves the request. No issue closure, sponsor claim, funded eligibility, upstream submission or bounty payment is asserted.

The application revision `34f810ee82c533550003794ef9f4f7123dd216fb` pins libretroshare `2f093fd7b3a013c463dacc65a1756e7643f543c0`, whose complete source has the same original blob. The later library master revision above independently retains it.

## Production consequence and scope

The complete current `src/util/rsmemory.h` (blob `a40d3fe34cfe8805caa8e6397a201f2c7a508773`) shows that `rs_malloc` allocates through `malloc`; the original successful path already uses `free` for this same pointer. The non-success branch previously returned without releasing it. The added call executes only after allocation succeeded and before leaving that branch.

The current direct-call search returned the declaration, implementation and two production callers. Retained source places calls in local-address selection in `src/pqi/p3netmgr.cc` (blob `68524c32b031f36ad86921f0a60bea46a4ced17f`) and local-address advertisement in `src/pqi/p3peermgr.cc` (blob `b07e8c2b6c8e4c6f37cbfe7935b5c150e9e31fc9`). This identifies real consumers; it does not measure call frequency, leak growth or platform behavior.

Exact bounded searches observed no open contribution under the shared author and no PR mentioning `GetAdaptersAddresses`. The public source-path custody search returned no result. These are query observations, not an exhaustive repository or ownership census.

## Apply and validation boundary

The packet includes the full modified `src/pqi/pqinetwork.cc` and `adapter-error-cleanup.patch`, based on the immutable original blob above. Compose the patch against the actual target tree and preserve any intervening source changes. The inline dated notice marks the one modified line.

Validation here is static source inspection and exact source/patch comparison. No C++ build, Windows process, network enumeration, runtime, test, fixture, workflow or hardware operation was performed. Windows executable acceptance remains unperformed. The patch does not claim to make failed enumeration succeed.

The original copyright and LGPL notices are retained. Unchanged copies of the upstream LGPL-3.0-or-later and GPL-3.0-or-later texts accompany the source. Modification date: 2026-10-05. Operation: `RETROSHARE-ADAPTER-ERROR-CLEANUP-20261005-7CA6`.
