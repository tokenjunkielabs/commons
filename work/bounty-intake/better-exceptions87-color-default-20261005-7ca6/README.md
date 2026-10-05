# Preserve the runtime color default in the existing logging contribution

## Change and reason

The existing [better-exceptions PR149](https://github.com/Qix-/better-exceptions/pull/149) adds an explicit `colored` argument to `format_exception`. Its default is `SUPPORTS_COLOR`, evaluated when Python defines the function. Ordinary calls therefore retain the initial value even after a caller changes `better_exceptions.SUPPORTS_COLOR`. Before that contribution, the function read the global while constructing its formatter on every call; its existing source comment explicitly describes that behavior for global configuration.

This packet changes the default to `None` and resolves that sentinel inside the function. The production patch is one hunk, **+3 / −1**. All other bytes of the selected module remain unchanged.

| Argument | Resulting color selection |
| --- | --- |
| Omitted or `colored=None` | Read the current module-level `SUPPORTS_COLOR` on this call. |
| `colored=False` | Pass false through, independent of the global. |
| `colored=True` | Pass true through, independent of the global. |

The existing PR149 logging code passes an explicit per-handler color policy. Its formatter cloning, shared-record cache isolation, assertion-argument restoration and handler selection are preserved in that contributor's branch. This patch does not change when logging handlers capture or refresh their own policy.

## Existing work and attribution

This is a compatibility follow-up to `dicnunz`'s existing logging contribution, not a new file-logging implementation. The complete selected production module and the relevant logging implementation were read from PR149's immutable head.

The same `None` sentinel pattern already appears in [PR164](https://github.com/Qix-/better-exceptions/pull/164) by `jjjkkll157`, observed closed and unmerged at `c5056c0468a4867d6da27b31df4457d830c76537`. The complete resulting initializer has exactly the same Git blob identity as PR164's initializer, `5e532988c1c3cb4c204cd989cc3659139a435350`. The useful integration here pairs that existing color-default behavior with PR149's existing logging design; no novelty is claimed for the sentinel pattern. PR164's other logging changes are not copied.

Josh Junon's existing source notice and the unmodified MIT license are retained. The source notice says 2017 and the repository license says 2016; both remain as supplied.

## Pinned source

Observed 2026-10-05:

| Item | Identity |
| --- | --- |
| Target contribution | Qix-/better-exceptions PR149, author `dicnunz`, open/unmerged |
| Fork head | `dicnunz/better-exceptions@ba53553af7790167cbbd0bec7eb51f20d6e1ac5a` |
| Reported PR base | `8fa00a74cf2a43e5f7012f158f0e16ea6216eaa0` |
| Source path | `better_exceptions/__init__.py` |
| Original blob / UTF-8 bytes | `83ffd559073996db116d3f2f1a0422521b8f4192` / 1,828 |
| Postimage blob / UTF-8 bytes | `5e532988c1c3cb4c204cd989cc3659139a435350` / 1,875 |
| Package tree / mode | `25ff49c695005c94c3d47a9269f1c7615a2d06b2` / `100644` |
| Unchanged PR149 logging blob | `358391dd5d6d0a4bfbfb735a1007a9c7c7e437d9` |
| MIT license blob | `7e1ceda43f73dbec535d0bdccc7ae0c9ec417df0` |

## Integration and validation

`dynamic-color-default.patch` targets the exact PR149 preimage above. `source/better_exceptions/__init__.py` is its complete postimage and requires the rest of that existing package. Apply the patch to the pinned contribution; compare fresh source before adapting it to another revision.

Validation consists of complete retained source and Git blob identities, the source-tree mode, an exact one-hunk text comparison, and independent reconstruction of the entire postimage by reading the serialized patch against the preimage. No Python interpreter, syntax compiler, formatter, logger, test, fixture, IPython session or workflow was invoked. No terminal/log-file behavior or contributor test result is presented as newly executed evidence. Publication readbacks establish source identity only.

[Issue87](https://github.com/Qix-/better-exceptions/issues/87) remains broader than this patch. Its historical $50 funding and the old maintainer award discussion for PR99 are not an award to this work. Existing authors, proposals and external acceptance conditions remain separate. No upstream PR, issue comment, platform claim, contributor contact or payment action was made.

The separate IPython [issue10](https://github.com/Qix-/better-exceptions/issues/10) already has several opt-in extension submissions, including PR169's handler restoration and special-rendering paths. No IPython implementation or full-issue completion is claimed here.

## Primary references

- [Selected initializer](https://github.com/dicnunz/better-exceptions/blob/ba53553af7790167cbbd0bec7eb51f20d6e1ac5a/better_exceptions/__init__.py).
- [Unchanged logging contribution](https://github.com/dicnunz/better-exceptions/blob/ba53553af7790167cbbd0bec7eb51f20d6e1ac5a/better_exceptions/log.py).
- [Python language reference: function definitions and default argument evaluation](https://docs.python.org/3/reference/compound_stmts.html#function-definitions).
