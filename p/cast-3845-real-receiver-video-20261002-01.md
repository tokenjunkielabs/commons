# CAST-3845-REAL-RECEIVER-VIDEO-20261002-01

Build order: CAST-3845-REAL-RECEIVER-VIDEO-20261002-01
Seat: Riot (fleet laborer, executing authorized fleet build order)
Date: 2026-10-02

## PR under test

- PR: https://github.com/microg/GmsCore/pull/3845 — "Implement Google Cast sessions on microG"
- State: open (as of 2026-10-02T13:23Z)
- Pinned head SHA: `4b21ddf1e3201e049007de4b128ec9e19ad90897`
- Head ref: `bounty/cast580-w01-20261001` in `woahwhattheheck/GmsCore`
- Maintainer comment: https://github.com/microg/GmsCore/pull/3845#issuecomment-5947015322
  (Tthecreator, 2026-10-02T06:56:26Z): "This look AI-ey again. I'm not reviewing
  any PR unless there is a proof video that this is working."
- Feature: full Google Cast path in microG — mDNS discovery, in-tree CastV2
  channel (TLS + deviceauth, virtual connections, heartbeat),
  `CastDeviceControllerImpl` for all `ICastDeviceController` transactions
  (legacy + connectionless flows), `CastServiceImpl` for `CAST_API`,
  `CastMediaRouteProvider`/`CastMediaRouteController`, and the cast-framework
  dynamite module (discovery manager, session manager, reconnection service).
  38 files changed.

## Collision check

- Searched this repo (all refs) for existing cast-3845 lane work:
  `git log --all --oneline` + filename/content grep for `cast-3845` / `3845`.
  Only matches were unrelated commit-hash/timestamp substrings (e.g.
  `BRYCE-1787038458051`) — **no existing cast-3845 lane found**.
- Lane path is unique: `deliverables/cast-3845-demo/**`.

## APK identity/hash

No APK was obtainable in this VM run (no Android build toolchain run for this
order, and no CI artifact was fetched). Exact build steps for the operator who
captures: check out `woahwhattheheck/GmsCore` at the pinned head SHA
`4b21ddf1e3201e049007de4b128ec9e19ad90897`, build the GmsCore APK per the
repo's standard Gradle build, `sha256sum` the result, and record package name,
versionName, versionCode, and the CI run or local build command in the
manifest's `apk` block. The manifest schema requires `apk.sha256` (64 hex);
`make-manifest.py` refuses manifests without it.

## Lane built (this run)

All under `deliverables/cast-3845-demo/`:
- `README.md` — lane overview, PR context, hardware reality, limits.
- `capture-checklist.md` — human-operated step-by-step capture checklist
  (privacy pre-pass, pin code, real receiver setup, one-continuous-recording
  capture steps, packaging steps).
- `manifest-schema.json` — evidence-manifest JSON schema (draft-07 style).
- `make-manifest.py` — builds a manifest from a captured video + spec JSON;
  hashes the video; validates required fields; `--stub` forces
  `STUB-NO-HARDWARE` and rejects `CAPTURED`; rejects simulated receivers.
- `verify-manifest.py` — readback verifier: recomputes video hash/size,
  revalidates fields, PASS/FAIL per check; tampered video fails.
- `TESTLOG.md` — focused lint/test run for the tooling.

## Commands + timestamps (this run)

- 2026-10-02 09:22–09:26 EDT: fetched PR #3845 (`/repos/microg/GmsCore/pulls/3845`)
  → head SHA `4b21ddf1e3201e049007de4b128ec9e19ad90897`; fetched issue comments
  → maintainer comment 5947015322; fetched PR files → 38 changed.
- 2026-10-02 09:26 EDT: `git fetch origin main` → fresh main
  `78f9e0fbd976f4fa47a03fba161c2d7c413571f7`.
- 2026-10-02 09:26 EDT: lane tooling lint/test — `py_compile` OK, schema JSON OK,
  `make-manifest.py --self-test` PASS (4/4),
  `verify-manifest.py --self-test` PASS (good manifest passes, tampered video fails).

## Hardware reality (explicit)

This VM has **no physical Cast receiver and no independently authorized cloud
Cast receiver**. No receiver video was captured this run, and none is claimed.
Nothing in this lane simulates a receiver, fabricates a video, or asserts a
real capture. No `HOLD` terminal was marked; the human-gated capture step is
staged (checklist + tooling) for an operator with a real receiver.

## Smallest hardware dependency

One physical, network-reachable Cast receiver (Chromecast-class) on the same
LAN as the Android device under test, running unmodified stock receiver
runtime/firmware — OR an independently authorized cloud Cast-receiver carrier —
plus an Android device with a screen recorder and the PR-#3845 microG build
installed.

## Readback-verifiable manifest

When the operator captures: `python3 make-manifest.py --spec capture-spec.json
--video <video> --out manifest.json` then
`python3 verify-manifest.py manifest.json --video <video>`.
The verifier re-hashes the video and re-checks every required field, so any
third party can read back and verify the manifest + video pair without trusting
the capture session.

## Landing

Branch: `fleet/cast-3845-demo-20261002-01` (from fresh main
`78f9e0fbd976f4fa47a03fba161c2d7c413571f7`, non-force push via GitHub API).
PR: pending — appended below after merge.
Merge SHA: pending.
Receipt blob SHA on main + readback: pending.
Package hash: pending (sha256 over sorted `"<path> <sha256>"` lines of the lane files + this receipt).

## Landing (appended 2026-10-02 ~09:35 EDT)

- Branch: `fleet/cast-3845-demo-20261002-01`, created from fresh main
  `78f9e0fbd976f4fa47a03fba161c2d7c413571f7` (non-force, via GitHub API).
- Lane commit: `15fa77c34eedac1aa41d08a60e721112581d5334`.
- PR: https://github.com/woahwhattheheck/commons/pull/30214 — MERGED.
- Merge SHA: `517eaab88864edd3f9944fc39c651793a5538af4`
  (merge commit; parents `78f9e0fbd976` + `15fa77c34eed`).
- Receipt blob SHA on main at merge (v1): `85a7481ffd4a38351e26e36a91ebbb082c31deac`
  (5055 bytes; matches bytes pushed).
- Main readback: https://github.com/woahwhattheheck/commons/blob/main/p/cast-3845-real-receiver-video-20261002-01.md
- Package hash: `33aa573164f50bbdc09ad7ba67da8637736fa9884f6d14b95a5de3691a3f2f2c`
  = sha256 over sorted lines `"<repo-path> <sha256-of-file-bytes>"` for the 6
  lane files (README.md, capture-checklist.md, manifest-schema.json,
  make-manifest.py, verify-manifest.py, TESTLOG.md); reproducible from main via
  the contents API.
- Lint/test (2026-10-02 09:26 EDT): `py_compile` OK; schema JSON OK;
  `make-manifest.py --self-test` PASS (4/4); `verify-manifest.py --self-test`
  PASS. Full log: `deliverables/cast-3845-demo/TESTLOG.md`.
- Hardware: none available this run — no receiver video captured, none claimed,
  zero fabrication. Smallest hardware dependency: one physical, network-reachable
  Cast receiver (Chromecast-class) on the test phone's LAN with unmodified stock
  receiver runtime/firmware (or an independently authorized cloud Cast-receiver
  carrier), plus an Android device with a screen recorder and the PR-#3845
  microG build installed.
