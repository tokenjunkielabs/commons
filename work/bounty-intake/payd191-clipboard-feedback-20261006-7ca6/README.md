# PayD: truthful clipboard fallback feedback

The mounted WalletQRCode copy helper first uses the Clipboard API and then falls back to a selected textarea plus `document.execCommand('copy')`. Its original fallback discards the returned boolean and always reports success. An unsupported or disabled command can therefore produce a success toast without a successful command report. The temporary textarea also remains attached if selection or the command throws before the old removal line.

This focused patch chooses feedback from the settled copy result and puts temporary-element removal in a finally block. It performs no clipboard or account operation in this delivery.

## Canonical source and attribution

Canonical issue: [Protocol-Guild/PayD #191](https://github.com/Protocol-Guild/PayD/issues/191), which requests copy controls and success feedback for public keys and hashes. This packet changes an existing connected helper; it does not implement every copy control or claim whole-issue acceptance.

Canonical donor: `Protocol-Guild/PayD@171c74b454daba241bfb75f36d10a0a3a77a68e5`. Changed production path: `frontend/src/components/WalletQRCode.tsx`.

The complete component, its complete EmployeeEntry caller, and the notification-hook contract were retained. The actual client chain is `main.tsx` → `App` → `/employee` → `EmployeeEntry` → `WalletQRCode`. The current caller renders the component when its notification state has a wallet address. Existing caller props and all copy button handlers remain unchanged. No live notification state, employee record, account identifier, credential value or clipboard data was acquired.

Original PayD contributors retain authorship. The latest returned path commit `cfde2e25077ecf0105db2c1a6025a08d396f5c12`, attributed to Wilfred007, is a repository-wide formatting change and is not represented as sole authorship. The issue was open with no listed assignee in the bounded current page. The numeric PR search returned one unrelated test-count hit; a separate bounded clipboard search returned no PR matches. These results are not a global absence or ownership assertion. No upstream branch, PR, issue, comment, assignment or claim was changed.

| Retained source | Git blob |
| --- | --- |
| `frontend/src/components/WalletQRCode.tsx` | `208fce0d908bd42c6a371b19ea0ed9df2fa3ffff` |
| `frontend/src/pages/EmployeeEntry.tsx` | `b89a5c832191a19a52c4f7b99201da5ece9acef8` |
| `frontend/src/hooks/useNotification.ts` | `782cf022cfa13d25961555d27ddb9b98509f75c8` |
| `frontend/src/App.tsx` | `acc3dfc6f6d5c04ccb1ab693b3a0d5735b81c10c` |
| `frontend/src/main.tsx` | `f84f187971ba135010c48e69fda10f0c0f71ebd9` |

## Exact patch

Apply `clipboard-feedback.patch` to the immutable donor above, or explicitly reconcile the exact contexts against later source.

| Changed source | Original Git blob | Prepared Git blob | Prepared UTF-8 bytes |
| --- | --- | --- | ---: |
| `frontend/src/components/WalletQRCode.tsx` | `208fce0d908bd42c6a371b19ea0ed9df2fa3ffff` | `50be7b30e817faf909a63177a23aeb687a6a4ff7` | 8,697 |

The two-hunk production change is +21/−8, including a dated modification notice:

- Read the already declared `notifyError(message, description?)` method alongside `notifySuccess`.
- Start `copied` as false and set it true only after the awaited modern write fulfills.
- On modern failure, attempt the existing textarea fallback, assigning its command's boolean result to `copied`.
- Catch fallback creation, append, selection or command failures with `copied` false, and remove the optional textarea in finally.
- Show the existing success text only when copied is true. Otherwise use fixed failure text with manual-copy guidance, without including the copied value.

The notification call occurs after either path has settled. A notification exception no longer triggers an additional fallback copy attempt. The QR rendering, reveal control, button arguments, issuer strings, trustline guide, notification-provider state, underlying account creation and all other source bytes remain unchanged.

## API contract and limits

The [Clipboard API specification](https://w3c.github.io/clipboard-apis/#dom-clipboard-writetext) defines an asynchronous write operation. This code uses fulfillment as its reported-success signal. It does not read the clipboard back or prove that later clipboard contents remain unchanged.

Mozilla's [Document.execCommand reference](https://developer.mozilla.org/en-US/docs/Web/API/Document/execCommand#return_value) documents a false result when a command is unsupported or disabled. That existing boolean is now respected. The legacy API is deprecated and depends on browser/user-activation behavior; retaining it does not promise broader compatibility or successful fallback after every permission failure. The change attempts the fallback after a caught modern failure and reports its actual return or exception outcome.

The finally block attempts cleanup for an element that was created, including on a false result or thrown fallback operation. It does not add a guarantee when cleanup or notification APIs themselves throw, nor does it restore the prior focus/selection, serialize repeated clicks, cancel pending writes, or suppress feedback after unmount. Existing render-time secret display and financial/network guidance are not audited or altered. No secret-copy policy, browser-security bypass, permission change, accessibility conformance, network/issuer validity or financial correctness is claimed.

## Validation and distribution

The complete original source is 8,354 UTF-8 bytes. The prepared source is 8,697 bytes. Pure text transformation and independently computed Git blob identities bind the source and patch. Forward patch application reproduces the prepared source exactly; reverse application restores every original byte. Replacing the new handler with the original and removing the modification notice restores the complete original file, proving there are no unrelated source changes.

The independent review considered the supplied source ordering only. No application, compiler, browser, clipboard read/write, synthetic copy sequence, test, fixture, workflow, dependency installation, API, credential/account, wallet, payment, trustline or upstream action was performed. This is source validation, not an observed browser result.

The exact canonical Apache-2.0 notice is retained as `LICENSE`, blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` (11,357 UTF-8 bytes), from the already retained matching donor base. Its complete tree had no separate NOTICE file. Source notices are preserved and the changed source gains a dated modification notice. Only this patch, guide and license are published.
