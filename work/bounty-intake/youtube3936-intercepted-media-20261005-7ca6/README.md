# YouTube PR3936: pause the intercepted media element

This one-line source continuation corrects media-element selection in jiangyj545's existing proposal. It does not prove or complete the larger initial-autoplay request, and it is not an upstream submission.

## Pin and application

- Original issue: https://github.com/code-charity/youtube/issues/1461
- Existing proposal: https://github.com/code-charity/youtube/pull/3936
- Author/fork: jiangyj545/youtube.
- Exact head: 06be7eaa37c621c5687286b4ad718f247ca2af9a.
- Base observed: 84d23cca7462dc6b7e3dde49dd3c0111ee32f61a.
- Path: js&css/web-accessible/functions.js.
- Exact preimage: c8d7144e2fcef2ac4dc7f8649ab8d9a1906caff3.

Apply change.patch to this exact pin or compose the one-line change with later source. The full postimage is included for inspection; do not overwrite newer source or another autoplay proposal.

## Concrete error

The code is inside the ordinary function assigned to HTMLMediaElement.prototype.play. The receiver is the intercepted media element. The proposal instead calls this.querySelector('video') and falls back to document.querySelector('video'). Element.querySelector searches descendants rather than the receiver, so the document fallback can select a different video.

The correction assigns the existing receiver directly to video. Both the immediate pause and existing delayed closure now retain the same intercepted element. All feature conditions, preview exclusion, ad/user-interaction checks, player API calls, timeout and returned promise remain unchanged.

Primary DOM reference: https://developer.mozilla.org/en-US/docs/Web/API/Element/querySelector. This is static reasoning about the retained actual hook, not a constructed DOM or browser reproduction.

## Scope and contribution custody

The full source and sole production patch were retained; the complete hook and surrounding caller behavior were inspected. The maintainer's comment 4641608251 requests clarity about contribution seriousness and questions whether issue1461 is current. PR3849's earlier-initialization alternative and its maintainer comparison were also read; neither is replaced by this continuation.

This correction is AI-assisted source work. No target code, Node, browser, fixture, tests, live playback, YouTube account/history, workflow or upstream action ran. Browser timing and history behavior remain unverified. Existing contributor comments about latency and preventing history entries are not independent evidence, and this packet does not adopt them as guarantees.

CONTRIBUTING.md at 9eb194b5543bc9b41a93e675bb81450330a64118 was read. Its wiki reference has an existing provider-failure hold from another lane and was not retried. Current public maintainer comments requesting disclosure are preserved; no contributor's mistaken assertion of a blanket AI ban is treated as project policy.

## Attribution and terms

Original source: code-charity / ImprovedTube contributors; the specific proposal is by jiangyj545 at the linked PR and exact source pin above. Modified 2026-10-05 only to bind the pause target to the intercepted media element.

The exact upstream custom LICENSE, 8c94d5c5af752f3587f16e9fbdb54e1c64be6316, is included unchanged. This is a free, noncommercial source correction, retaining source and contributor credit. The license's existing contributor, copyleft, publication and commercial-reuse provisions remain as written; they are not relabeled as a standard permissive license. No endorsement, commercial-use authorization, bounty eligibility, acceptance or payment is asserted.
