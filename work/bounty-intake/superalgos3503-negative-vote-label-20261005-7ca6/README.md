# Display configured negative votes in the percentage label

This is a narrow UI continuation of [Superalgos issue #3503](https://github.com/Superalgos/Superalgos/issues/3503). Its latest maintainer [comment 1544257167](https://github.com/Superalgos/Superalgos/issues/3503#issuecomment-1544257167) reports that negative votes work in the Governance panel and asks for a visual indication when a vote's negative configuration is set. This packet addresses that percentage label, not restoration or revalidation of the governance algorithm.

## Source consequence and change

The current VotingProgram draws a node's allocation percentage before forwarding its voting power. Its reference-forwarding branch later checks the strict configuration boolean negative === true and multiplies the transferred votes by the existing sign. The displayed allocation percentage never receives that sign, so it stays positive.

The ordinary vote display branch now supplies a fourth, optional display flag to NodeCalculations.drawPercentage. It uses the same reference-parent presence and three switch exclusions as the existing forwarding branch, with the strict negative configuration boolean. User Profile, User Profile Vote, Voting Program, and target-node drawing paths return earlier and remain unchanged.

The existing formatter obtains the same percentage.toFixed(2) text. Only when the optional flag is exactly true and the percentage is nonnegative does it prefix one minus sign. Already-negative numbers keep their original single sign. Zero can therefore display as -0.00 when configured negative. This is a string-formatting decision; the allocation percentage, vote value, target transfer, configuration and payload data are not modified.

The existing undefined return and nonnumeric reset remain before formatting. In particular, the existing fixed-amount sentinel still resets the percentage label. Callers omitting the new display flag retain their existing formatting, angle and counter behavior.

The label describes configured negative outgoing voting intent. It does not claim that a vote passed the later self-vote checks, was accepted, changed any reward amount, or was included in a distribution. The existing error and validation paths remain authoritative.

## Immutable source and artifact contents

Repository: https://github.com/Superalgos/Superalgos
Pinned source: `9f0fb59edd4bae7afa08d06c366e0bcb48103aec`.

| Production path | Original Git blob | Prepared Git blob |
| --- | --- | --- |
| `Projects/Governance/UI/Function-Libraries/VotingProgram.js` | `83644981d552d1636e8aae12287f002a861fb2cd` | `53e94388bf4f3f0a552670c2613a548878bad068` |
| `Projects/Governance/UI/Utilities/NodeCalculations.js` | `1548cf757fe600665b37ddb30c887b4256fffc45` | `4a2638eea7c52d9782e660855f7b04987d5a735e` |

Both complete production files are included at their original paths. negative-vote-label.patch contains three focused hunks, fourteen added and three removed source lines. Source notices identify the modifications. LICENSE is the upstream Apache License, Version 2.0, copied verbatim from `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`; NOTICE preserves attribution and scope.

The complete VotingProgram and NodeCalculations leaves were read. The retained NodeConfig loader `a9d72dd08a4c68b196e1f2a66f175bea8b3b5574` returns the parsed configuration value without coercing it. The relevant retained UiObject.setPercentage implementation in `51280e4224ff8313496e0992ee77851750281014` stores the supplied display value. Neither dependency is modified.

The entire VotingProgram source prefix preceding drawVotes is byte-for-byte identical to the original. That prefix contains vote resets, vote allocation, self-vote rejection, sign application, recursion, bonus invocation and all distribution arithmetic. The entire NodeCalculations prefix preceding drawPercentage, including getDistributionConfig, is also byte-for-byte identical. The source patch touches display handling only.

## Chronology and external boundaries

All six issue comments were read. The original defect concerns an old token-power inflation exploit, but the later maintainer report says negative values are ignored where intended and negative voting works in their scenarios. That historical report is preserved as the author's evidence, not a new runtime result.

The explicitly linked [PR #4824](https://github.com/Superalgos/Superalgos/pull/4824) is merged at `277bcfca093dc6c6a2e24da079c3524a65dc3102`; its optimization makes zero-power changes visible sooner. This packet does not replay that work or modify its calculations. The bounded negative-keyword contribution lookup contains older algorithm/documentation contributions and dependency updates; it is not a complete contribution census. The exact Commons/activity lookups found no existing matching packet at the time of preparation.

The existing root CONTRIBUTING file links to an official page that was inaccessible on the prior necessary source qualification. That route remains held without retry or alternate acquisition. Existing Governance CODEOWNERS attribution and any external submission conditions remain. This is internal Commons source delivery only: no upstream PR, comment, submission, identity assertion or token-bounty claim.

## Validation and remaining limits

Validation consists of static source reasoning, the three exact source replacements, actual-source patch reconstruction, complete original/prepared Git blob identities, fresh current-source preimage checks and guarded publication readbacks. A separate reasoning review found the display-only flag consistent with the supplied transfer predicate; it was not code execution.

No governance program, UI, browser, native executor, test, fixture, build, dependency installation, workflow, live vote, claim, distribution, token transaction, wallet, account, credential, external contact or upstream mutation was performed. Runtime label rendering remains unperformed. The package neither claims whole-issue closure nor establishes the historic bounty's current availability or payment eligibility.

Operation: `SUPERALGOS3503-NEGATIVE-VOTE-LABEL-20261005-7CA6`.
Stable branch: `work/superalgos3503-negative-vote-label-20261005-7ca6`.
