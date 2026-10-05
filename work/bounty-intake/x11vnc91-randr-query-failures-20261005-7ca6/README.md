# x11vnc 91: reject failed RANDR resize queries

This source continuation builds on [maxnet's existing PR 107](https://github.com/LibVNC/x11vnc/pull/107) for [issue 91](https://github.com/LibVNC/x11vnc/issues/91). The original contribution implements the optional SetDesktopSize hook and RANDR scaling. This packet closes four failure paths inside its existing `xrandr_set_scale_from` function.

## Failure and resulting behavior

The function ignores the status from `XRRQueryVersion` before inspecting its output variables. It also immediately dereferences the pointers returned by `XRRGetScreenResourcesCurrent`, `XRRGetOutputInfo` and `XRRGetCrtcInfo`. The library's failure paths can leave the version outputs unwritten or return a null pointer.

The revised function checks each result before using it. Every new failure path logs the failed query, releases any earlier resource objects, unlocks the existing X lock, and returns `FALSE`. The unchanged SetDesktopSize caller in `src/screen.c` maps that result to `rfbExtDesktopSize_InvalidScreenLayout`.

| Failed query | Resource cleanup before returning |
| --- | --- |
| `XRRQueryVersion` | No resource object has been acquired. |
| `XRRGetScreenResourcesCurrent` | No successful resource pointer is available. |
| `XRRGetOutputInfo` | Free the previously acquired screen resources. |
| `XRRGetCrtcInfo` | Free the acquired output info and screen resources. |

These branches occur before their path reaches `XGrabServer` or any screen-size, CRTC configuration or transform write. The existing `xrandr = 1` assignment still precedes the output-info and CRTC queries, so those two failures may leave event monitoring enabled. This packet does not claim that every process state is unchanged.

The existing version threshold, size clamping, primary-output fallback, headless handling, reset path, physical scaling, view-only restriction and framebuffer-event processing remain in place. Later RANDR configuration failures and rollback are separate work. In particular, this change does not establish a fix for the larger-than-initial-display freeze reported in [comment 2880783386](https://github.com/LibVNC/x11vnc/issues/91#issuecomment-2880783386), or complete multi-monitor and headless-driver compatibility.

## Exact source and integration

| Source identity | Value |
| --- | --- |
| Existing contribution | LibVNC/x11vnc PR 107, author maxnet |
| Contributor repository | maxnet/x11vnc |
| Contributor head | 2872260fff9cc786137a060e2efb5251ff3043f4 |
| Observed upstream base | cb88cb27825e7ced4f9f7ea3939c1ded0edfea3c |
| Production path | src/xrandr.c |
| Original blob | 9574e46528af56c277ec0376d71fb4e7e55fbedb, 12,852 UTF-8 bytes |
| Revised blob | 0cd47d712d75ece044d501ef891429ee9f2dc06f, 13,540 UTF-8 bytes |
| Mode | 100644 |

Apply `randr-query-failures.patch` from the pinned contributor checkout's root. The complete revised file is provided under `source/src/xrandr.c`. The patch has five hunks, +24/-1: four query guards and a dated modification notice. The original 457-line file has 456 unchanged lines; the former unchecked version-query statement is replaced by its guarded form.

`COPYING` is the complete original license file, blob d159169d1050894d3ea3b98e1c965c4058208fe1. The source's GNU GPL version 2-or-later notice and OpenSSL linking exception are preserved. A prominent 2026-10-05 modification notice is included in the revised source.

## Source basis and validation boundary

The full production file, all ten patches in PR 107, the complete root and source directory listings, the exact regular-file tree entry and the complete license were read. The existing caller's full added hook establishes its failure-result mapping. The unchanged `HAVE_SETDESKTOPSIZE` boundary retains the contributor's compatibility structure; no old-library build result is asserted.

The library behavior is supported by the published libXrandr 1.3.0 source in Debian's source archive:

- [Xrandr.c](https://sources.debian.org/src/libxrandr/2:1.3.0-3%2Bsqueeze1%2Bbuild1/src/Xrandr.c): a failed version reply returns zero before assigning the caller's output integers.
- [XrrScreen.c](https://sources.debian.org/src/libxrandr/2:1.3.0-3%2Bsqueeze1%2Bbuild1/src/XrrScreen.c): the current-resources wrapper uses a shared query implementation with null failure returns.
- [XrrOutput.c](https://sources.debian.org/src/libxrandr/2:1.3.0-3%2Bsqueeze1%2Bbuild1/src/XrrOutput.c) and [XrrCrtc.c](https://sources.debian.org/src/libxrandr/2:1.3.0-3%2Bsqueeze1%2Bbuild1/src/XrrCrtc.c): failed replies or resource allocations return null. The corresponding free functions release the successful allocations.

This is a source-level result. The complete source identities and line delta were checked, and independently applying the serialized patch to the retained original text rebuilt the complete revised text. No C compiler, X server, VNC client, hardware, fault injection, test, fixture or workflow was run. A live display disconnection may also involve Xlib error handling outside these returned-result paths.

All 27 issue comments and all eight PR discussion comments were read. PR 107 was reconfirmed open and unmerged at the exact head above. Maintainer discussion about driver limitations and older library compatibility remains unresolved by this packet. The historical $50 funding and review request are context, not a new reward, acceptance or payment event. This Commons continuation preserves maxnet's contribution and makes no upstream submission or whole-issue completion claim.
