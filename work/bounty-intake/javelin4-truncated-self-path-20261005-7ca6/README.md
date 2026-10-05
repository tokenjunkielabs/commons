# Reject truncated executable paths in py-workedtask PR49

This source packet makes the fixed-buffer executable-path lookup reject truncation before the existing integrity check reads a file. It is a narrow follow-up to brok-best's contribution, not a new implementation of issue #4.

## Canonical source and credit

- Issue: https://github.com/javelin-anticheat/py-workedtask/issues/4
- Existing PR49: https://github.com/javelin-anticheat/py-workedtask/pull/49
- Author: brok-best; branch `feat/integrity-verification`
- Complete inspected head: `1dea325bd16f1267d479eff59104adbab6124bac`
- Upstream base reported by PR49: `8796d971d98d392dc8423ffb18693a4985f36d26`
- Original `AntiCheat.cpp` blob: `26e7030f2e9f1f8d10f59d0fb80b90404a2bfc4d`
- Complete postimage blob: `d7923b24ed1c691c0556a0f4448c41c3986a6633`
- Serialized patch blob: `d30e4ac5af58f67c29d9fb3fb879e76e29a357be`
- The original MIT notice, copyright 2025 EA Javelin Anticheat, is retained unchanged in `LICENSE`.

The current issue body is open, has no assignee, and already checks its acceptance boxes. Its full 35-comment discussion names multiple existing implementations. The Algora comment 3198284752 advertises $100 and requires an attempt plan, a claiming PR and a short demonstration; sponsor comment 3198248802 originally offered $50. These are advertised terms, not an award or payment receipt. No external attempt, claim, submission, contact or payout action was made here.

PR49 is open and unmerged; its one discussion comment concerns the author's payment availability, not maintainer acceptance. PR41 by kitwongpixel is also open at `ed597c17af24e16051c575703cff6e809937013c` and describes a different canonical-marker implementation. That contribution and all original authorship remain separate. The historical upstream PR-census rate-limit failure was not retried or routed around; this packet uses direct issue-named PR reads and asserts no complete PR census or absence of an existing own-account PR.

## Exact source defect and change

The old helper calls `GetModuleFileNameW(nullptr, path, MAX_PATH)` and rejects only zero. Every other return is treated as a complete null-terminated path. Both existing CRC32 and SHA-256 checks then read the file named by that helper.

Microsoft's official [GetModuleFileNameW documentation](https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-getmodulefilenamew), inspected October 5, 2026, states that a too-small buffer yields a truncated result with return value equal to the supplied capacity. Its Windows XP note also warns that this truncated result may lack a terminator. A successful complete result instead returns the path length excluding the terminator.

The one +3/-2 hunk records the returned DWORD, rejects zero or any length at least MAX_PATH, and assigns precisely the accepted length to the output string. It neither reads nor constructs a string from a rejected buffer. The two existing integrity callers already return false when the helper fails, so their existing guarded failure path is preserved.

This retains the fixed MAX_PATH limit: longer paths are rejected, not supported. The patch changes no debugger detection, process scanning, hashing algorithm, expected-value parsing, configuration, Python path, exit code or transport. No dynamic buffer or retry is introduced.

## Existing limits remain material

PR49's `INTEGRITY.md` blob `9727f631b891e6f2aadc36cd5c83f41ec536381f` suggests computing a built executable's SHA-256 and recompiling once with that value. Recompilation with a new embedded constant changes the executable being hashed; that instruction does not establish a matching whole-executable baseline. This packet does not implement sealing, normalized hashing or an external trust anchor, and does not certify the existing expected-hash setup. PR41's different marker approach is credited as an existing alternative, not independently executed or reproduced here.

Rejecting an incomplete path only binds this helper to the complete name returned by Windows. It does not provide authenticity against an actor who can change both code and expected hash, or guarantee that the on-disk file cannot change after path lookup or during reading. Existing native build and runtime limitations are unchanged. The issue as a whole remains uncompleted by this packet.

## Static validation and integration

All original C++, Python and integrity-guide bodies were retained before inspection. The pinned root listing contains five files and no AGENTS or CONTRIBUTING file; its README links the integrity guide, and the full MIT license is included.

The exact serialized patch was independently reconstructed against the complete original source, with every context/removal line and old/new hunk count checked. Its result matches the full postimage byte for byte. Content hashes bind the complete source and patch. Publication checks compare all four complete immutable and main texts with their computed/provider Git blob identities and the exact PR path set.

No native executor, C++ compiler, Python program, test, fixture, device, debugger, process enumeration or workflow was run. No runtime or source-acceptance result is claimed. Integration should apply `truncated-self-path.patch` to the identified PR49 source and preserve the original contributor's carrier. The complete `source/AntiCheat.cpp` is the corresponding postimage; it is not permission to overwrite unrelated later changes.
