# Capture checklist — PR #3845 real-receiver proof video

Build order: CAST-3845-REAL-RECEIVER-VIDEO-20261002-01
PR: https://github.com/microg/GmsCore/pull/3845
Maintainer requirement: https://github.com/microg/GmsCore/pull/3845#issuecomment-5947015322
("I'm not reviewing any PR unless there is a proof video that this is working.")

This checklist is for a human operator (or an independently authorized carrier)
with a real Cast receiver. Complete it end to end; nothing is "good enough"
without the video + manifest pair at the bottom.

## 0. Privacy pre-pass (do this first, every time)

- [ ] No faces, people, mirrors, or photos in frame.
- [ ] Phone shows no notification content with names/numbers/codes; enable Do Not Disturb.
- [ ] Home screen wallpaper is neutral; no widgets showing personal info.
- [ ] Redact/blur in post if any SSID, IP, account name, or location slips into frame.
- [ ] Recording has no audio of conversations; narration track is fine and recommended.
- [ ] **Do not post the video externally.** Handoff is through the maintainer's own review flow only.

## 1. Pin the code under test

- [ ] Record the PR head SHA from https://github.com/microg/GmsCore/pull/3845:
      `4b21ddf1e3201e049007de4b128ec9e19ad90897` (verify fresh on capture day —
      if the PR moved, re-pin and re-record; never reuse a stale SHA).
- [ ] Obtain the APK built from that exact SHA (CI artifact or local build).
- [ ] `sha256sum` the APK; record package name, versionName, versionCode, and the
      exact build steps/CI run that produced it in the manifest.

## 2. Receiver under test

- [ ] Use a **physical** Cast receiver (e.g. Chromecast-class device) on the same
      LAN as the test phone, running **unmodified stock** receiver runtime.
      (Alternative: an independently authorized cloud Cast-receiver carrier —
      record which one and who authorized it.)
- [ ] Record: receiver model, runtime, firmware version.
- [ ] Receiver is NOT a simulator, emulator shim, or scripted stub. Fabrication
      here poisons the evidence.

## 3. Test app

- [ ] Install an app that uses the Cast SDK `CastContext` (any app that shows a
      cast button; note its name/version in the manifest).

## 4. Capture (one continuous screen recording, no cuts)

1. [ ] Start screen recording on the test phone; state the date/time in narration.
2. [ ] Open the test app; confirm the cast button is **visible** (this is the
       feature: on unfixed microG, `CastState` stays `NO_DEVICES_AVAILABLE` and
       the button hides).
3. [ ] Tap the cast button; show the receiver listed from real discovery.
4. [ ] Connect to the receiver; show session established (e.g. "Connected" state
       / playback controls).
5. [ ] Exercise: play media, then **set volume** and **mute/unmute** (route
       volume path).
6. [ ] **Disconnect**, then reconnect via the connectionless flow
       (`addListener` → `connect` → `onConnectedWithResult`) if the app supports it.
7. [ ] Stop the recording. Record start/end timestamps and timezone.

Expected: button appears, real receiver discovered, session connects,
volume/mute work, disconnect/reconnect clean.
Observed: fill the per-step table in the manifest (`steps`), status
pass/fail/skipped per step, no invented passes.

## 5. Package

- [ ] `sha256sum` the video file; record size, container, duration.
- [ ] Build the manifest: `python3 make-manifest.py --spec capture-spec.json --video <video> --out manifest.json`
- [ ] Verify: `python3 verify-manifest.py manifest.json --video <video>` — all checks PASS.
- [ ] Video + `manifest.json` are the maintainer-ready handoff pair.
