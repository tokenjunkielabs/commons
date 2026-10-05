# BeyondMafia popup failure recovery

This is a narrow repair to the existing shared popup loader, discovered while qualifying https://github.com/BeyondMafia/BeyondMafia-Integration/issues/72. It does not implement or complete that issue's requested user mini-profile, statistics or friend controls.

## Source and application

Current master: 00b164ee3266c8acc19a323fd0c627952856f588.
Modified path: react_main/src/components/Popover.jsx.
Exact preimage: 6aedfc7cb57428e1bc87743d9a1e0dad92fdf5cc.

Apply change.patch to that source or compose its loader/state hunks with newer changes. The full modified file is included for inspection, preserving existing line endings. Do not overwrite a newer component.

Actual error reporter: react_main/src/components/Alerts.jsx, b098d6b5bff8dc50923269da96c8de220b4ff029. Its useErrorAlert only displays a SiteInfo error and does not clear popup state. Actual existing game-info caller: Game.jsx d8dc7b148891591cbd32d62642267581a6e04872, TopBar calls popover.onClick for /game/:id/info. These are source links, not live requests.

## Defect and repair

Opening a main popup sets loadingRef.current=true. The outside-click handler declines dismissal while that flag is true. The old rejected-request path only calls errorAlert, leaving the flag set. A side request similarly leaves sideContentLoading=true, which blocks the existing hover admission condition.

Current main failure now clears loadingRef/loading, hides the popup and side content, and clears the bounding element before reporting the error. Current side failure clears side loading/visibility/title before reporting; clearing the title allows the same hover target to retry.

Independent monotonically increasing main/side request IDs identify current requests. A superseded completion cannot replace newer content or close a newer popup; its stale error is ignored. Side completion no longer clears a still-pending main request's loading flag. Successful current content still uses the existing ready/renderers and dataMod path.

This is not a universal popup lifecycle redesign. It does not add cancellation, timeouts, caching or new data access. Direct external open/ready calls and main-versus-side lifetime policy are not redesigned. A request that never settles still follows the existing loading policy.

## Qualification and limits

The complete popup component and actual error-handler body were read; relevant game caller and user-link bodies were inspected. No generated input, target-code execution, Node/React build, browser, tests, fixture, network popup request, account action, deployment, workflow or upstream submission occurred. Native interaction and failure acceptance remain unperformed.

Issue72's three returned comments include a historical50-token offer, a pie-chart pointer and an interested contributor; an exact linked-PR query returned0/incomplete=false. No current bounty availability or payout is asserted. Current user links still open/suppress navigation and have no user popup renderer; that larger feature remains unimplemented. This repair has its own concrete production failure scope.

## Attribution and license

Original source: BeyondMafia contributors, https://github.com/BeyondMafia/BeyondMafia-Integration/blob/00b164ee3266c8acc19a323fd0c627952856f588/react_main/src/components/Popover.jsx.

Modified 2026-10-05 to recover current main/side requests after failure and distinguish superseded completions; a dated notice is included. Source, patch and adaptation contributions are shared under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International, https://creativecommons.org/licenses/by-nc-sa/4.0/. The unchanged complete upstream LICENSE (848335aeb452b0630ea8fb742ba58cffd12bb63d) is included. Its attribution, noncommercial/share-alike conditions and warranty disclaimer remain applicable. No endorsement or commercial-use permission is implied.
