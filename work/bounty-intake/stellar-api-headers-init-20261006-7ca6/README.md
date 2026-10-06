# Preserve supported Fetch header inputs in the API client

This attributed source continuation changes only `src/lib/api-client.ts` in **Stellar-Analysis/frontend@482ee456369418ef82c4056718cb82d3468f762b**. The exported API helpers accept `ApiOptions extends RequestInit`, but the shared request builder currently object-spreads `options.headers`. That operation does not implement the supported Fetch header-input contract.

The patch creates a fresh `Headers` instance from the caller's input, adds the existing JSON content-type default only when that header is absent, and uses `set()` for the generated trace and CSRF headers. The source delta is **+6 / -6 lines**, in two hunks. This Commons packet is an independently reviewable proposed source change; it is not an upstream merge or runtime result.

## Exact source and connected documentation

| Input | Git blob | UTF-8 bytes |
| --- | --- | ---: |
| `src/lib/api-client.ts` | `12c2b7e4b2dbd081c6a7520e6ca5dadd2b38f5a5` | 5,515 |
| `docs/offline-sync.md` | `99552f0a03d2bf4eea7903328e3bb872870e2a35` | 18,476 |
| Proposed `src/lib/api-client.ts` | `86485c374b44dac55b3c9489a2fdbf07070cf7f4` | 5,576 |
| `headers-init.patch` | `c6463fbccffc6b88cc15554164991acab806d6fa` | 1,316 |

The complete original source and documentation were acquired at the named commit. Their native file SHAs and independent UTF-8 Git-blob identities agreed. The complete recursive `src` tree identifies the source as mode `100644`; that exact entry was transferred by the concurrent source worker. The file mode is preserved.

The actual exports `apiGet`, `apiPost`, `apiPut`, `apiPatch`, `apiDelete`, and `apiReconcile` pass their options to this shared builder. The repository's offline-sync documentation describes `apiReconcile` as the frontend recovery path for `POST /api/rpc/reconcile`. The documentation still uses the older `frontend/` prefix; the pinned current tree establishes the file's root-relative location.

This establishes an existing documented API surface. No claim is made that a mounted application caller passing a `Headers` object or tuple array was observed in production. The bounded GitHub code search returned no matches, which is not proof that callers are absent.

Source links:

- [Original API client](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/src/lib/api-client.ts)
- [Existing reconciliation documentation](https://github.com/Stellar-Analysis/frontend/blob/482ee456369418ef82c4056718cb82d3468f762b/docs/offline-sync.md)

## Why the change is needed

A `Headers` object stores its header list through its API; object spread does not copy that list. An array of header pairs is a valid Fetch input, but spreading the array into a record creates numeric properties instead of the intended header names. Even ordinary records can supply a differently cased content-type name, while the current default is added under a fixed spelling.

The [WHATWG Fetch standard, Headers class](https://fetch.spec.whatwg.org/#headers-class) defines construction from the supported initializer forms and the header-list operations. [MDN's Headers constructor documentation](https://developer.mozilla.org/en-US/docs/Web/API/Headers/Headers) also describes constructing from an existing Headers object. The patch delegates input normalization to that platform API.

The resulting behavior follows directly from the changed source and the platform contract:

- Caller-provided record, pair-array, and Headers inputs enter a new header collection.
- The JSON content-type default is added only when no content-type header is present, using a case-insensitive header-list check.
- The generated trace value and required CSRF token replace an existing same-name value through `set()`, including differently cased spellings.
- The caller's Headers object or input collection is not modified by these additions.

Native Headers normalization, validation, and casing rules now apply when the collection is constructed. Malformed input can therefore fail earlier than the existing `fetch()` call. The trace insertion remains inside the existing catch block, and CSRF insertion remains in its existing method/skip guard. This packet does not establish browser, server, telemetry, or transport behavior by execution.

## Scope and source review

The request method, other RequestInit options, body construction, CSRF lookup and missing-token error, trace-context calls, single 503 retry, response handling, and exported method signatures are unchanged. Both attempts still use the same constructed request options. The telemetry module was not acquired or modified for this header-only continuation.

The complete serialized unified patch was parsed and applied to the exact preimage, producing the entire proposed postimage byte for byte. Applying the same serialized hunks in reverse recovered the entire original. All two hunks and all 29 hunk rows were reviewed with no truncation. The six insertions and six deletions are confined to the header construction and its two generated-header assignments.

These were source-text and artifact-identity checks. No application code, browser, HTTP request, CSRF flow, lint, compiler, dependency installation, test fixture, test suite, workflow, deployment, or upstream submission was run. There is no acceptance, payment, or broader API-correctness claim.

The bounded Commons PR query for `"api-client" "headers"` and exact public Slack header-topic search returned no matches. Those results support limited overlap screening only; they do not establish exclusive ownership or exhaustive coverage. The current activity notice is advisory.

## Attribution and notices

The API client and connected documentation remain work of the upstream project and its contributors. The bounded current-path history returned the root-relocation commit [59fad72d9fbef9cfd6f47e215392da44488fcdc4](https://github.com/Stellar-Analysis/frontend/commit/59fad72d9fbef9cfd6f47e215392da44488fcdc4), associated with christabel888. That observation identifies the relocation, not sole authorship of the client or its previous changes. This packet claims only the narrow continuation described above.

The three distinct MIT notices present in the donor's documentation are included unchanged, with their exact case-distinct origins preserved here:

| Original donor path | Included file | Git blob |
| --- | --- | --- |
| `docs/LICENCE.md` | `upstream-licence-mclaughlin.md` | `57740b9d4d86aedf5d518f2f363d5cf192c54127` |
| `docs/LICENSE.md` | `upstream-license-menke-laguna.md` | `af5411fa243cfcf2b61c79d081dbb6204e956041` |
| `docs/license.md` | `upstream-license-de-wet.md` | `4a766e268772888af5df56c3f6c608f68558b789` |

The notices retain Michael Mclaughlin, Romain Menke and Antonio Laguna, and Declan de Wet's respective attribution. Their inclusion does not assign any of those authors a particular line in the API client.
