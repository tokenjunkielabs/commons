<!--
SPDX-FileCopyrightText: 2026 OpenAI
SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Recover the contact import selector after a file read error

This is a narrow source continuation of [Nextcloud Contacts PR #5386](https://github.com/nextcloud/contacts/pull/5386) by SebastianKrupinski. It addresses a concrete failure path in that contribution without claiming the broader import rewrite, vCard conversion, or a live import has been accepted.

## Source consequence and correction

The current processFiles method sets the Pinia import stage to preparing, then awaits readFileAsText for each selected file. The reader rejects on FileReader.onerror. The await has no catch, so one read rejection exits before resetInput, the zero-valid-files reset, or the transition to selecting. Upload is enabled only in the idle stage, and the modal is shown only in selecting or importing. The source therefore leaves the import controls disabled in preparing after this failure.

The correction catches only the readFileAsText await for each file. It shows the existing localized dialog service a fixed filename-only message, then continues with the next selected file. A successfully read file still passes through the unchanged queueFile validation and addedFiles accounting outside the catch. Thus parsing or queue-admission exceptions are not mislabeled as file read failures.

The existing post-loop code resets the input. When no valid file was added it removes queued files and resets the store to idle; when at least one was added it changes to selecting. Successful files retain their order, metadata and contents. No retry, file-content logging, raw exception disclosure, address-book creation, server request, or automatic import is added.

## Immutable source

- Canonical PR: https://github.com/nextcloud/contacts/pull/5386, OPEN/unmerged when read.
- Original author: SebastianKrupinski.
- Head: `2dd6070161dd43b7b6cabf7e6bbdfa4b95194007`.
- Reported base: `e92898da278c9e86b63ecc060258cfbda353db54`.
- Complete component preimage: `cc47a798cb5c8390efec7579d7b8b440e3bae7ae`.
- Corrected component: `ca2a95b0214b0ac8871628fc9683946547c3727a`.
- Complete import store establishing idle/reset behavior: `38394fd8d5084170eb9ee16abd9d59074c318203`, unchanged.
- Upstream COPYING included verbatim from observed main: `ea56f0adb16b03ab38bf737bcb10404939dc8315`.

The packet preserves the complete component at its original relative path, Nextcloud's copyright and AGPL-3.0-or-later header. The accompanying patch changes that one production file by seven additions and one removal. No dependencies, tests, workflows or other PR paths are changed.

## Intake and remaining boundaries

The contribution was found while qualifying [Contacts #492](https://github.com/nextcloud/contacts/issues/492) and its explicitly linked [error-reporting issue #990](https://github.com/nextcloud/contacts/issues/990). Their complete 39 and 17 comment threads were read. Conversion from vCard 2.1 to supported versions remains an open request. This source correction implements neither conversion nor new parser acceptance and does not substitute a version marker for conversion.

PR #5386 replaces the old client parser/import state and requires [nextcloud/server PR #61277](https://github.com/nextcloud/server/pull/61277). That dependency is reported by the original author; its implementation/runtime was not reacquired or validated for this correction. The source packet is a continuation of that proposed PR, not a patch to the current main import path. Its address-book sentinel review and broader server integration remain separate.

The original contribution's two issue comments and five inline comments were read. Any reported coverage or screenshots in those comments are historical author/provider evidence, not new acceptance. The latest maintainer statement in Contacts #243 says this repository no longer has bounties; historical Bountysource badges do not establish payment eligibility.

## Validation and contribution conditions

The complete component and Pinia store were inspected. The exact replacement, complete original/prepared Git blob identities, current PR-head guard and publication readbacks establish the stored source change. A separate retained-source reasoning review agreed with the catch boundary; it was not execution.

No test, fixture, browser, application, FileReader, native executor, build, package install, workflow, import, CardDAV, email, account, credential lookup or external contact was performed. The change does not establish recovery from a read that never settles, an abort that the current reader does not reject, exceptions in queueFile or dialog rendering, or component teardown during reading. It preserves the existing queued-file policy rather than inventing session cancellation.

Upstream contribution instructions require human review, agent/model attribution and a real DCO sign-off. This Commons packet is internal source delivery under the standing authorization, with no upstream push, PR, issue reply, sign-off identity or bounty submission. Any later upstream contribution must satisfy the actual external conditions.

Operation: `NEXTCLOUD-CONTACTS-IMPORT-READ-ERROR-20261005-7CA6`.
Prepared branch: `work/nextcloud-contacts-import-read-error-20261005-7ca6`.
