# Keep Unicode subject separators inside Git log records

This maintenance continuation applies to edvinas1573's [CBB PR4712](https://github.com/claude-builders-bounty/claude-builders-bounty/pull/4712), commit `42cf8437b93a94b7fbd7d26a576ca3dfbd7e3bf8`. The original `changelog.py` blob is `091e295c72b185776ff67533ffb8da225b4996a3`. The original author supplied the generator, Bash entry point, documentation and example. This packet changes only record splitting in that generator.

The generator asks Git for `--format=%H%x00%s`. Git separates these records with line feeds; the NUL separates the commit ID from its subject. Python's `str.splitlines()` also splits U+0085, U+2028, U+2029 and several other characters. When such a separator occurs inside subject text, the loop can treat the rest of the subject as another record and fail the required NUL split before reaching `markdown()`.

The correction uses literal `split('\\n')` and skips empty records, including Git's trailing delimiter and an empty history. Subject characters then reach the existing Markdown sanitization as part of their original record. Git arguments, tag boundary selection, shallow-history rejection, classification, commit IDs, exclusive output creation and explicit `--force` behavior are unchanged. This is not a general parser for arbitrary corrupt Git output or a change to Git's subject formatting.

## Integration

Apply `change.patch` to the pinned PR4712 checkout, or replace its root `changelog.py` with the supplied postimage after confirming the preimage. Keep `changelog.sh` next to it as the original guide requires. Compose the patch with newer changes; do not overwrite a newer generator. The two prior Commons continuations for eij0471's PR4698 and PR4703 address different source implementations and are not prerequisites for this patch.

## Evidence and acceptance boundary

Static source review establishes the delimiter mismatch. Primary references: [Git pretty formats](https://git-scm.com/docs/pretty-formats) documents `%s`, `%x00` and terminator semantics; [Python str.splitlines](https://docs.python.org/3/library/stdtypes.html#str.splitlines) lists the additional Unicode boundaries and contrasts literal splitting. No Python, Git command, shell, parser, constructed history, fixture, test, build or workflow was executed for this continuation. The external PR's historical validation is its author's claim and was not repeated. Native acceptance remains unperformed.

The external contributor's branch is untouched. This source packet does not satisfy the board's `/opire try` prerequisite, submit an upstream PR, establish bounty acceptance, or claim payment. The original MIT license is included unchanged.
