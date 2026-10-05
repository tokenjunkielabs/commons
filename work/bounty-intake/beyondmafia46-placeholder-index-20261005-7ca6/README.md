# BeyondMafia PR956: placeholder capture and index correction

This noncommercial source continuation fixes the token/index boundary in quantbitrealmSimon's proposed forum renderer. It does not constitute an upstream submission, a bounty claim, or completion of all of issue46.

## Integration pin

- Original request: https://github.com/BeyondMafia/BeyondMafia-Integration/issues/46
- Contributor implementation: https://github.com/BeyondMafia/BeyondMafia-Integration/pull/956
- Author/fork: quantbitrealmSimon, quantbitrealmSimon/BeyondMafia-Integration, feat/forum-spoiler-youtube-embed.
- Exact head: e67b9da93682a9230fdc48034558ec4eb26e983c.
- Base observed in current PR metadata: 00b164ee3266c8acc19a323fd0c627952856f588.
- Modified path: react_main/src/components/EnhancedMarkdown.jsx.
- Exact preimage: 3ae9ce58adadf9a420bd5b69da648b2233831b47.
- Actual caller: react_main/src/pages/Community/Forums/Thread.jsx, cf244dbcfbcd8e7741963a0e549ab334b02eca12. Post passes its displayed content to EnhancedMarkdown.
- Frontend package: 6a47c5b713bef525393a591147f64ad9fbe6a5cc, declaring react-markdown ^4.3.1 and React ^16.13.1.

Apply change.patch to that contributor head, or compose the same hunk with later source. The mirrored full postimage is supplied for inspection; do not overwrite a newer implementation. PR956's existing Thread import/caller and markdown.css changes are prerequisites and remain untouched.

## Source defect and change

JavaScript split inserts every capturing group into the returned array. The original expression captures the whole placeholder, its type, and its digits. Each branch then parses parts[i + 1], which is the type string, producing NaN instead of the index. The separate type/digit captures also reach the ordinary text fallback.

The correction captures only the whole placeholder while splitting. An anchored match on that same token supplies its type and numeric index. A token renders only when its referenced item exists in the corresponding generated array; unavailable tokens remain ordinary literal text. The obsolete capture-skipping condition is removed, so adjacent ordinary numbers remain ordinary text.

Primary language reference: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/split (Return value and Description, capturing-group behavior). This reasoning follows the actual retained source; no synthetic input or target execution was used.

## Acceptance limits

This is a source-only correction. No React build, browser, tests, fixtures, live embed, account, network playback, or upstream action ran. The original author's checked testing list is not independent acceptance. An attempted versioned react-markdown documentation read was unavailable; native integration and the existing renderer API remain unverified here.

The existing raw-text preprocessing, placeholder namespace collisions, empty/missing-source handling, spoiler state lifetime, Markdown nesting and iframe layout are not redesigned. The original request's quoted-post anchors, custom colors/fonts and broader media behavior remain outside this change. This packet does not make a complete forum-feature or safety claim.

Issue46 supplied two returned comments against three reported in the intake metadata. One collaborator comment offered 50 tokens for issues46 and75 combined historically; no current reward availability, eligibility or payment is asserted. PR956 remains the original author's open submission.

## Attribution and license

Original component and integration: quantbitrealmSimon and BeyondMafia contributors. Source: the pinned PR/path above. Modified 2026-10-05 to correct placeholder capture/index handling and preserve unavailable tokens as text; a dated notice is included in the postimage.

The source, patch and adaptation contributions are shared under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International, https://creativecommons.org/licenses/by-nc-sa/4.0/. The unchanged complete upstream LICENSE is included (848335aeb452b0630ea8fb742ba58cffd12bb63d). No endorsement is implied; the upstream warranty disclaimer and license terms remain applicable. This packet grants no commercial-use permission.
