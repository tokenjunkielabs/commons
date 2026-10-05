# Soundbounce #82: per-item batch capacity correction

This internal source packet fixes an incidental batch-capacity overrun in the old Soundbounce server. A room that starts below `ROOM_MAX_TRACKS` can receive several new tracks in one request; the original code checks capacity once and uses that answer for every track. The patch retains that initial gate and also checks the live room length immediately before each synchronous insertion. Only admitted new tracks enter the outgoing `add` payload.

This does **not** complete [upstream issue #82](https://github.com/pdaddyo/soundbounce/issues/82). Its requested replacement of no-vote tracks in a full room, room-admin configuration, and removal-notification/client work remain outstanding. No upstream contribution or deployment is made by this packet.

## Source and attribution

All original implementation credit remains with Paul Barrass and Soundbounce contributors. The complete original MIT license is copied unchanged as `LICENSE.md`.

The source is pinned to [pdaddyo/soundbounce commit 2e14e8fbad66fe4b1a8c65092e796fca60f35048](https://github.com/pdaddyo/soundbounce/tree/2e14e8fbad66fe4b1a8c65092e796fca60f35048), whose tree is `231bb3d6a397e44135486186e591b3ac9e361fb2`.

| Source | Git blob |
| --- | --- |
| `src/server/soundbounce-server.js` preimage | `ac7f204fccca46675d43a8664f10311cb0f6da7c` |
| `src/server/public/jsx/room/room.jsx` | `6470bf06422802334dbce826661a6008bd12d306` |
| `src/server/public/js/shared.js` | `48ac47d74a2e044511b4eefaad5b63e82d3eae52` |
| Root `README.md` | `5a60615ad99790706fcef7e3f52b2ed21e23b80f` |
| Root `LICENSE.md` | `ee33d3b2a8878d595169d443add5b222586feb6b` |

The upstream README explicitly says this version is no longer maintained and points to Soundbounce v2. V2 has not been inspected. This packet concerns only the pinned old version. The issue's $20 Bountysource badge is historical; current funding, eligibility, acceptance, and payment have not been established.

## Producer and mutation boundary

The retained `room.jsx` producer `handleDrop` splits newline-separated dropped URLs into track IDs, passes the array to `sendAddOrVote`, and sends it as the `add-or-vote` socket payload. The server dispatch passes that payload to `processAdds`, which limits requests to 50 IDs and processes the returned tracks in a synchronous `forEach`.

The original `canAdd` value is computed once before the loop. The new condition is:

```js
if (canAdd && room.tracks.length < server.ROOM_MAX_TRACKS) {
    simpleTracks.push(simpleTrack);
    // existing insertion follows
}
```

The existing shared insertion helper inserts into `room.tracks`; it does not enforce this capacity limit itself. A separate shared playlist update may remove elapsed tracks, and this patch does not redesign that behavior.

The initial full-room rejection and outer broadcast gate are retained. Existing tracks still take the earlier duplicate branch and enter `voteList`, with the later `processVotes` call unchanged. The `dontVote` condition and recycle caller are untouched. No tracks are evicted by this change. Client code, compiled code, event names, and the existing empty-add-envelope behavior remain unchanged.

## Packet and verification

- `soundbounce-server.js`: complete patched server source for upstream `src/server/soundbounce-server.js`.
- `change.patch`: a unified patch against the exact pinned upstream preimage.
- `LICENSE.md`: unchanged original MIT license.
- This guide records scope, provenance, and limits.

The source edit is one hunk with three removed lines and two added lines. All other server bytes remain identical to the pinned preimage. The actual serialized patch was parsed and applied as text to the retained preimage, and the reconstruction matched the complete postimage exactly.

| Artifact | Bytes | Git blob |
| --- | ---: | --- |
| Original server | 56082 | `ac7f204fccca46675d43a8664f10311cb0f6da7c` |
| Patched server | 56132 | `584381ca05915916980b6ef4b4cf0e56c5f74ef8` |
| Unified patch | 811 | `01a7c7c3d41cb598c24f3fb0f2e6d0599a644f66` |
| Unchanged license | 1095 | `ee33d3b2a8878d595169d443add5b222586feb6b` |

Verification consists of source binding, exact text patch reconstruction, Git blob identity calculation, and publication readbacks. No production code, application test, native application, Spotify API, audio/playback, account, or runtime operation was executed. Runtime behavior and upstream acceptance remain unverified.
