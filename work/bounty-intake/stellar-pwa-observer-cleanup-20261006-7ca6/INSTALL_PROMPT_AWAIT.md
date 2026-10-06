# Await the existing PWA install prompt

The current install handler calls `installPrompt.prompt()` inside a try block but discards its returned Promise. It then awaits `userChoice`. A rejection of the discarded prompt Promise is not caught merely because its invocation is lexically inside that try block. This additional patch awaits that existing invocation so its rejection reaches the handler's existing error and loading cleanup.

## Exact source and composition

- Canonical repository: https://github.com/Stellar-Analysis/frontend
- Immutable source commit: `482ee456369418ef82c4056718cb82d3468f762b`.
- Production path: `src/hooks/useProgressiveWebApp.ts`.
- Original upstream blob: `c7b1b8a74c88e1c9f07da6deef246b5e71bc6f7a`.
- Postimage of this standalone change: `6a62aca01bf7ab320ef7235eb9b5ab0ad18c9eb0`.
- Delta: +1/-1, solely `installPrompt.prompt();` to `await installPrompt.prompt();`.

This adds `install-prompt-await.patch` and this note to the existing PWA continuation directory. The original observer-cleanup patch and README from https://github.com/woahwhattheheck/commons/pull/31882 remain unchanged. That earlier patch changed the initialization effect above this handler and preserved the install-action suffix. Compose both patches by their exact context; the earlier additions shift this hunk's line number. The two separate patches are not asserted to have identical line-number headers or to provide a newly verified combined-module hash. Do not overwrite a newer module with an old full source copy.

The original implementation and contributor credit remain with the source repository. This is current-main follow-through, not an external PR submission, reassignment or whole-PWA completion. The prior bounded PWA chronology found only closed PR115 describing other PWA/SSR/status work, and no hook cleanup carrier. A distinct repository/prompt-expression Slack check was empty; its genuinely later interval after the environment restart was also empty. Those results are bounded chronology, not a contributor census. The fresh source-main guard still named the immutable source above.

## Actual caller and behavior

The already read settings page mounts ProgressiveWebApp. That complete component invokes this hook and its Install button calls a handler that awaits `install()`; the button is disabled while the hook reports loading. The hook's handler sets loading and INSTALLING, invokes the browser prompt, consumes the user's choice, and has existing catch/finally branches.

The invocation remains before the first suspension in this handler: adding `await` does not defer the call into a later effect or timer. After fulfillment, the existing `userChoice` read and accepted/dismissed branches remain unchanged. A prompt rejection now enters the existing catch, which records the Error and restores READY; finally clears loading. A synchronous throw remains handled by the same catch. No new error strings, outcome mapping, return type or user-action policy is introduced.

## Primary contracts

- https://developer.mozilla.org/en-US/docs/Web/API/BeforeInstallPromptEvent/prompt documents a Promise return, a user-action invocation requirement, and at most one invocation per event instance. It labels the API non-standard and of limited browser availability.
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/await documents that rejection of an awaited Promise throws the rejection reason in the surrounding async function.

These contracts support the source-level rejection propagation. No particular browser exception, rejection frequency or installation outcome was observed. An optional exact Chromium implementation lookup was inaccessible and remains held; it is not cited as implementation evidence.

## Boundaries and checks

The source byte identity was independently matched after acquiring the exact immutable blob as input to this new correction. A complete bounded diff found exactly one inserted and one deleted line; reversing that replacement reproduced the source. No hook, browser method, synthetic event, fixture, test or runtime was executed.

No declaration/import of the ambient BeforeInstallPromptEvent type appears in this hook. The retained repository tree did not establish its declaration path. This change does not claim to fix the existing ambient type/build contract or establish installed-browser compatibility.

The API's single-use event requirement remains in force. The existing READY retry policy and component visibility behavior are not rewritten, and successful retry of an already-consumed event is not promised. Error clearing on retry, overlapping calls, unmount behavior, pending promises without a settlement, browser installation semantics, cache policy and manual update behavior remain separate. This correction neither cancels a prompt nor forces a user choice.

The source repository's differently attributed docs license notices were not treated as a license for this hook. Only a minimal contextual patch and this original note are added. Existing contribution/source/assignment boundaries and exact failed provider routes remain unchanged.

No browser/device, service-worker registration, cache/storage, runtime/test, account, upstream issue/PR/review, acceptance, award or payment action was performed.

Operation: STELLAR-PWA-INSTALL-PROMISE-20261006-7CA6.
