# Record an empty initial UTXO snapshot

This is a narrow source continuation over troggy's [LeapDAO PR18](https://github.com/leapdao/spending-conditions/pull/18), commit `0978c57af0ea0492e31338aa6c0a3ab61edd5e62`. The original `tools/hashLockCondition.js` blob is `53034a268bd46e72afa7d6087fa51ff4f9b67ca4`. PR18's existing work supports spending conditions with preexisting UTXOs. The member's [issue comment](https://github.com/leapdao/spending-conditions/issues/17#issuecomment-547848140) invites continuation.

The poller initializes `txs` only inside `if (res.length)`. A successful empty response therefore leaves it uninitialized. The first later nonempty response is recorded as the initial snapshot and returns without recognizing any new output. A caller observing an initially empty address can wait indefinitely after its first deposit.

The patch moves the existing initialization before the nonempty-result check. The first successful response now establishes the baseline even when it is empty. JavaScript's empty array remains truthy, so a later result is compared with that recorded empty baseline. Initial nonempty responses remain the baseline as before; repeated empty responses do not produce a transaction. RPC failure behavior and all transaction construction remain unchanged. A deposit already present before the first successful poll is still treated as preexisting; this patch does not create an earlier snapshot or change that race boundary.

## Integration and remaining scope

Apply `change.patch` to the pinned PR18 source, or copy `tools/hashLockCondition.js` after checking the preimage. Compose with newer source rather than replacing a newer file wholesale. The supplied source and modifications remain under MPL-2.0; the original license is included unchanged.

This does not complete issue17's gas repair. The original `gasPrice: 0`, missing gas deduction, network rejection investigation, undeclared transaction variables and other existing behavior remain outside this polling-only correction. The separately observed PR22 is closed/unmerged and changes gas handling, not the polling snapshot. No source from its unaccepted gas proposal is adopted.

## Evidence boundary

The retained actual PR18 source, its one-file patch, package manifest and public issue discussion establish the branch ordering defect by static inspection. No Node, contract compilation, test, synthetic provider response, network request from the application, RPC, chain transaction, account operation or workflow was executed. Native acceptance is unperformed. The upstream branch is untouched; this packet is not an upstream submission, bounty claim, gas estimate, payment claim or evidence that the legacy network works.
