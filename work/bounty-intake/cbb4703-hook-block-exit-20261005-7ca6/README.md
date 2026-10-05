# Make the detected-danger result block PreToolUse

This source-only continuation changes the detected-danger branch in `pre-tool-use.py` from `sys.exit(1)` to `sys.exit(2)`. It preserves contributor **eij0471**'s existing classifier, input handling, logging and diagnostic text.

## Exact integration source

Apply `change.patch` to [external PR 4703](https://github.com/claude-builders-bounty/claude-builders-bounty/pull/4703), head `24c28cf225ce7f64110b22a75f82440ae79a1c73`, in `eij0471/claude-builders-bounty` on `feat-security-hook`. The complete `pre-tool-use.py` preimage is blob `1496ef09bb9a8b50327088f6b1973796b437f225`; this packet includes its full corrected postimage.

The original Bash wrapper `pre-tool-use` (blob `1a1906be187c4b794f6d81694f05d6ae65b89b03`) ends with `exec` of the sibling Python script and therefore preserves that script's exit status. No wrapper change is required for this detected-danger result. If integrating into a later source revision, compose this branch correction rather than overwriting later work with the bundled postimage.

The included MIT license is unchanged from blob `19f591c09faad54c09b87775128ada9d625ab1fa`. No external repository or pull request was modified.

## Why the original result does not block

The Python `main` function writes its detected-danger diagnostic only to stderr, produces no JSON decision on stdout, and then exits 1.

The [official Claude Code hooks reference](https://code.claude.com/docs/en/hooks#exit-code-2), read October 5, 2026, specifies that `PreToolUse` exit 2 blocks the tool call. Its [other exit codes section](https://code.claude.com/docs/en/hooks#other-exit-codes) states that exit 1 with empty stdout is a nonblocking error. Changing the existing detected-danger exit to 2 communicates the decision already made by the classifier. Accepted commands retain their existing exit 0 path.

## Scope and remaining acceptance

This fixes the exit-status protocol boundary only. It does not establish that every dangerous shell or SQL expression is recognized, that safe commands avoid false positives, or that logging always succeeds.

The pinned PR's root contains README, LICENSE, the wrapper, Python source and a test file; it has no `hooks/` directory. The complete README links to `hooks/` but supplies no installation commands or hook settings registration. Those issue3 requirements remain unresolved by this packet. In particular, this is not an installer and must not be described as a functioning configured hook solely because the Python file exists.

[Issue 3](https://github.com/claude-builders-bounty/claude-builders-bounty/issues/3) requires `/opire try` before a bounty submission. No such claim, sponsor acceptance, upstream submission, current funding confirmation or payment occurred here. The 1,818-comment issue discussion was not expanded; the external PR had zero discussion comments and zero inline comments when inspected. Its self-reported checklist and test output were not treated as acceptance evidence.

The full source and three production/documentation patches were read. The existing test file was not expanded or executed. The executor is offline: no Python, shell, hook, Claude Code process, destructive command, test suite or workflow was run. Text comparison confirms the one-line source change; full published source, patch, guide and license were read back. Native integration, hook registration and actual block/allow behavior remain unperformed.
