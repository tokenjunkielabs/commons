# PayD #417: associate the upgrade modal's existing input labels

The current upgrade modal renders separate labels and inputs for the new WASM hash and the admin secret key. Neither label has `htmlFor`, neither input has `id`, and the labels do not wrap their inputs. This patch adds one generated ID for each pair so the existing visible caption identifies its corresponding control.

## Exact source and attribution

This is a narrow source continuation for [Protocol-Guild/PayD issue #417](https://github.com/Protocol-Guild/PayD/issues/417), opened by Wilfred007. The observed issue is OPEN and unassigned. Its three complete comments are requests to work on the issue by bukeeastrey and guptakumarranjeet150; they are not assignment or acceptance evidence. A bounded repository PR query for `417` returned no matches, and a separate Commons query for `"UpgradeConfirmModal"` returned none. These query results do not prove global absence or authorize upstream work.

The donor is current `Protocol-Guild/PayD@171c74b454daba241bfb75f36d10a0a3a77a68e5`. Original repository contributors remain credited. The bounded three-entry path history includes commit `4f5dd01b31a0b7445e50408398b6fbe9b52d8f48` (author field “Mainnet-ops”, design-language adoption) and Godbrand0/Thompson commits `1a867a6c92d19ea7851f915bb44778aa600813d7` and `82bcf1876d891615db50eb1d7753ee94eed0db03` (formatting and mobile layout). This is observed recent history, not an original-authorship census.

Apply `input-labels.patch` to this exact source:

| Path | Preimage Git blob | Prepared postimage Git blob | UTF-8 bytes before / after |
|---|---|---|---:|
| `frontend/src/components/UpgradeConfirmModal.tsx` | `5478483e6ef82ea383b249326b5febc9f106f0f6` | `e0c8ea028df87b389a7c8256cd17869ac019399c` | 35523 / 35709 |

The source change is +7/−3 in four hunks with 36 complete rows. The patch is blob `ef520e431c31e87e803c5e910c0e5e4ab5b660d7`, 1615 UTF-8 bytes. Its actual serialized unified diff materializes the full prepared postimage and reverses to the full pinned donor string. The complete donor module is not copied into this packet.

## Connected caller and React contract

The same-ref `frontend/src/App.tsx`, blob `acc3dfc6f6d5c04ccb1ab693b3a0d5735b81c10c`, mounts `AdminPanel` at `/admin` inside the existing employer layout and error boundary. This is not an authentication or deployment claim.

The full `frontend/src/pages/AdminPanel.tsx`, blob `a7952a1fddd20aa6b44b6276782a2b09d80e4c0c`, renders `ContractUpgradeTab` for its contracts tab. That component, blob `c99bed605973d45cc93a77211fc6f2c2cc05db78`, renders the modal when a selected contract and admin address are present. These source links establish an actual caller; no account, contract registry, or browser was accessed.

The donor `frontend/package.json`, blob `33e58d67eca11b200b6988835b1f8450f179d2c2`, declares React and React DOM `^19.2.0` and React types `^19.2.14`. This is manifest evidence, not an installed-version or compiler result. The [primary React useId reference](https://react.dev/reference/react/useId) documents top-level calls for unique accessibility IDs and shows matching `htmlFor`/`id` associations.

Both new `useId()` calls are unconditional in the modal component, before its existing state declarations. The input and authorize steps remain conditional render branches; the hooks are not placed inside those branches. Each label and input uses its own ID. Existing input types, values, change handlers, captions, validation, state transitions, cancellation policy, simulation, execution, polling and notifications are unchanged outside these four hunks.

## Limits and validation

The issue also requests focus trapping, keyboard dismissal, roles, broader labels and manual accessibility review. This packet addresses only these two source label associations. It does not establish complete modal semantics, focus behavior, accessibility conformance, assistive-technology compatibility, hydration behavior, or whole issue #417 acceptance.

The password input already exists in the donor. The patch neither acquires nor generates credentials and does not change how values are collected, transmitted, signed, cleared or retained. Existing security text in the donor is not independently validated. No wallet, signing, upgrade, simulation, transaction, API, clipboard or cancellation action was performed.

Validation consists of complete pinned public source acquisition, source-contract inspection, exact string edits, serialized forward/inverse patch materialization, and independent Git blob identities. No JSX compilation, lint, tests, fixtures, install, browser, runtime, account or upstream operation occurred. The original issue's requested lint/type checks remain unexecuted here.

The retained complete donor Apache License 2.0 text, blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` (11,357 bytes), is included unchanged as `LICENSE`. This dated guide identifies the modification and preserves contributor attribution without claiming an ownership transfer or a repository-wide licensing audit.
