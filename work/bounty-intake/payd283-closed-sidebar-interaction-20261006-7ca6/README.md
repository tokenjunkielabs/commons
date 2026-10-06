# PayD 283: closed mobile sidebar interaction

The mounted employer layout keeps its mobile sidebar in the DOM while closing it with a horizontal translation. Its navigation links can therefore remain interactive after the sidebar moves off screen. This source-only patch synchronizes the native `HTMLElement.inert` property with the existing open state and exposes that same state through the toggle's accessibility attributes.

## Source and attribution

Canonical issue: https://github.com/Protocol-Guild/PayD/issues/283  
Canonical repository and immutable source: `Protocol-Guild/PayD@171c74b454daba241bfb75f36d10a0a3a77a68e5`  
Changed production path: `frontend/src/components/EmployerLayout.tsx`

This is a continuation of the existing PayD contributors' source. It does not claim authorship of the original layout. The source issue remained open with no listed assignee in the bounded current issue page; its generic accessibility request is not whole-issue acceptance. The repository-specific current PR query returned zero matches, which is only that query's result and not a global absence proof. Issue comments and unrelated account, employee, payment and authentication implementations were not needed or expanded. No upstream issue, PR, assignment or claim was changed.

| Retained source | Git blob |
| --- | --- |
| `frontend/src/components/EmployerLayout.tsx` | `5cd117fcdaf260873f1e9f8655787857a3288ca2` |
| `frontend/src/components/DashboardSidebar.tsx` | `2b32a0870f3ec3de67259b746bd5f84073982695` |
| `frontend/src/App.tsx` | `acc3dfc6f6d5c04ccb1ab693b3a0d5735b81c10c` |
| `frontend/src/main.tsx` | `f84f187971ba135010c48e69fda10f0c0f71ebd9` |
| `frontend/package.json` | `33e58d67eca11b200b6988835b1f8450f179d2c2` |

The actual caller chain is `main.tsx` → `App` → `EmployerLayout` → `DashboardSidebar`. The mounted layout renders separate desktop and mobile sidebar wrappers. The older `AppLayout` / `AppNav` pair was inspected to establish that it is not the selected mounting path; neither is edited.

The manifest declares React and React DOM `^19.2.0`, TypeScript `~5.9.3` and React types `^19.2.14`. These are declared dependencies, not installed-version or compiler evidence.

## Exact change

Apply `closed-sidebar-interaction.patch` to the named immutable donor or reconcile it explicitly against later source.

| Changed source | Preimage | Prepared postimage | Prepared UTF-8 bytes |
| --- | --- | --- | ---: |
| `frontend/src/components/EmployerLayout.tsx` | `5cd117fcdaf260873f1e9f8655787857a3288ca2` | `df0e9c3166ef0edc094fcab5f23b416e37175094` | 3391 |

The four-hunk production change is +9/-1, including a dated modification notice:
- Call `useId` unconditionally for a stable mobile-wrapper ID.
- Assign that ID to the existing always-mounted mobile wrapper.
- Use a block-bodied callback ref to set `node.inert = !isSidebarOpen` when React attaches the DOM node. The callback is recreated on render, so the attachment uses the current state; its block returns no cleanup value.
- Set the toggle's `aria-expanded` from `isSidebarOpen` and `aria-controls` to the wrapper ID.

The existing toggle, overlay click, sidebar navigation-close callbacks, desktop wrapper, route destinations, transform classes and transition duration remain unchanged. The panel stays mounted, so the control target exists in both states and its existing transform styling is retained. No new permission, identity or account rule is introduced.

## Platform contract and limits

The [HTML Standard's inert subtree definition](https://html.spec.whatwg.org/multipage/interaction.html#inert-subtrees) makes inert content unavailable for normal focus and interaction. It expressly discusses off-screen navigation as a use case. The native [`HTMLElement.inert` property](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/inert) is boolean.

React's [common DOM-component reference](https://react.dev/reference/react-dom/components/common) documents callback refs and recommends `useId` for instance-safe identifiers. An inline callback is detached and attached again when its function identity changes. The null callback case performs no property write; the following non-null attachment applies the current closed/open state. This patch uses the native DOM property through that callback contract; it does not depend on a claimed JSX `inert` prop implementation.

The current entrypoint uses client `createRoot`. This is not an SSR or hydration fix. It supplies no legacy-browser polyfill, focus trap, Escape handler, focus restoration, breakpoint-state reset or complete modal behavior. It does not promise that an already focused descendant is restored to the toggle when closing. Those behaviors, overall accessibility conformance and browser/assistive-technology acceptance remain separate.

The exact React v19.2.0 changelog web request returned DisabledError, and a distinct tagged React DOM source-file request returned an unreadable-file error. Both exact requests remain held; neither was retried or fetched by an alternate route. They do not supply compatibility evidence. The selected implementation uses the independently retrieved native-property and callback-ref contracts above.

## Validation and license custody

The complete changed source and actual caller modules were retained before editing. Pure source transformation produced the patch, and forward application reproduced the prepared postimage exactly; reverse application restored the original bytes. Independent Git blob identities were computed for both source versions and the patch. This is exact source validation, not a React execution or browser result.

No compiler, app, browser, accessibility scanner, tests, fixture, workflow or dependency installation was run or added. No account, wallet, employee record, payment, transaction or upstream action occurred. No broad issue closure, deployment readiness or economic result is claimed.

The existing Apache-2.0 license is retained verbatim as `LICENSE`, blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` (11,357 UTF-8 bytes), from the already retained matching canonical base. The full base tree contained no separate NOTICE file. Original source notices are preserved and the changed file gains a dated modification notice. Only the focused patch, this guide and that license are published.
