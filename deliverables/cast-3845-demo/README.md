# cast-3845 real-receiver video evidence lane

Build order: **CAST-3845-REAL-RECEIVER-VIDEO-20261002-01**

## What this lane is

microG GmsCore PR [#3845](https://github.com/microg/GmsCore/pull/3845)
"Implement Google Cast sessions on microG" (head `bounty/cast580-w01-20261001`
in `woahwhattheheck/GmsCore`) received a maintainer comment
([issuecomment-5947015322](https://github.com/microg/GmsCore/pull/3845#issuecomment-5947015322),
Tthecreator, 2026-10-02T06:56:26Z):

> This look AI-ey again. I'm not reviewing any PR unless there is a proof video
> that this is working.

This lane builds **everything that can be built without a Cast receiver**:
the capture checklist a human (or an authorized carrier) follows, the
evidence-manifest schema, the manifest builder/verifier tooling, and the
build-order receipt. It contains **no video and no claim of a capture**.

## Hardware reality (this run)

- This VM has **no physical Cast receiver** and **no independently authorized
  cloud Cast receiver**.
- Per the build order: the independent components were built; the smallest
  hardware dependency is named below; no `HOLD` terminal was marked; and it is
  stated explicitly that **no receiver video could be captured this run**.
- **Zero fabrication rule:** nothing in this lane simulates a receiver,
  splices/fabricates a video, or claims a real capture. Any manifest produced
  by the tooling without a real video is stamped `STUB-NO-HARDWARE`.

## Smallest hardware dependency

> **One physical, network-reachable Cast receiver (e.g. a Chromecast-class
> device) on the same LAN as the Android device under test, running an
> unmodified stock receiver runtime/firmware** — OR an independently
> authorized cloud Cast-receiver carrier — plus an Android device with a screen
> recorder and the PR-#3845 microG build installed.

That is the entire hardware gate. Everything else (checklist, manifest,
hashing, verification) is already built in this lane.

## Lane contents

| File | Purpose |
|---|---|
| `capture-checklist.md` | Human-operated, step-by-step capture checklist for a real receiver (privacy-safe). |
| `manifest-schema.json` | Evidence-manifest JSON schema (draft-07 style, stdlib-validated). |
| `make-manifest.py` | Builds a manifest from a captured video + spec JSON; hashes video; validates fields. |
| `verify-manifest.py` | Readback verifier: recomputes hashes, checks required fields, PASS/FAIL per check. |
| `TESTLOG.md` | Focused lint/test run for this lane's tooling. |

## Human gate (staged, not prompted)

The capture step requires a human with a real receiver. It is staged silently:
follow `capture-checklist.md`, run `make-manifest.py`, verify with
`verify-manifest.py`, and hand the video + manifest to the maintainer. **Do not
post the video or manifest externally** (build-order instruction); handoff only
through the maintainer's own review flow.

## What the feature does (PR #3845 summary)

Implements the full Google Cast path in microG: mDNS discovery,
the in-tree CastV2 channel (TLS + deviceauth, virtual connections, heartbeat),
`CastDeviceControllerImpl` serving every `ICastDeviceController` transaction
(connect/launch/join/leave/stop/volume/mute/namespace messages, legacy and
connectionless flows), `CastServiceImpl` for `CAST_API`, `CastMediaRouteProvider`
(passive discovery, serialized resolves, tolerant TXT parsing, variable-volume
routes), `CastMediaRouteController`, and the cast-framework dynamite module
(discovery manager, session manager, reconnection service).

## Hard limits (from the build order)

- No second GmsCore PR and no code rewrite of #3845.
- No bounty claim/re-claim, provider submission, or resend of anything.
- Do not touch Terry's phone/accounts/identity/devices.
- No credentials, household/network identifiers, or private filenames committed.
- No external posts. No approval prompts.
