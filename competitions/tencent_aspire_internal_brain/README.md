# Internal Brain — local operator prototype

This Python 3.11+ prototype provides deterministic document retrieval with role-based access control, source citations, document ingestion, ordered operation sessions and replay. It runs from source with the standard library. All supplied people, policies and documents are fictional.

The operator workflow is **load a bundle → perform scoped operations → retain outcomes and audit evidence → replay the retained session**. Retrieval is lexical and non-generative. Document content remains data; it cannot change the declared roles, clearance or retrieval scope.

## Local access boundary

Run these commands as a trusted local operator. The operator can read and replace the full input bundle, choose any declared actor and read retained artifacts. `validate` prints the complete normalized bundle, including document content. Ingested bundles and replay artifacts also contain full document data. None of these files is a safe employee-facing export.

The `tenant_id` and `actor_user_id` fields are declarations, not authenticated identities. The engine enforces the selected actor's policy inside an operation; it does not prevent a filesystem operator from choosing another actor or editing the policy. A deployed service would need authentication and a protected storage boundary before offering this interface to untrusted callers.

The fictional `northstar` bundle provides these roles:

| Actor | Declared roles | Available operations |
| --- | --- | --- |
| `maya` | `employee` | Query employee-scoped documents within clearance. |
| `li` | `finance` | Query finance-scoped documents within clearance. |
| `chen` | `security_admin`, `finance` | Query, ingest and read audit evidence. |

Audit export and retained-run access require an explicit audit reader. Use `--audit-actor chen` with the supplied example bundle. Neither `maya` nor `li` has `audit:read`. Replay requires the same declared audit reader recorded in the artifact. This permission check does not authenticate the person running the command or protect an artifact already readable on disk.

## Start from the source directory

Use the directory containing this README as the working directory. No package installation is needed for these commands.

```bash
python -B -m internal_brain validate demo_bundle.json
python -B -m internal_brain query demo_bundle.json demo_query_employee.json
python -B -m internal_brain query demo_bundle.json demo_query_finance.json
```

The employee request retrieves authorized travel material. The vendor note deliberately includes hostile instruction language; any reported markers are diagnostics on untrusted text. The finance request uses `li` and can retrieve `finance-plan`.

Citations retain the source URI, `content_sha256` for the content bytes, and `document_sha256` for the whole normalized document record. The record digest also binds provenance and access metadata, including source URI, version, classification, allowed roles and labels. Successful ingestion audit payloads bind that full normalized record. These digests support comparison of retained bytes and metadata; the CLI does not fetch a source URI or establish that its source is authentic.

Each standalone invocation creates a fresh engine. Use a session when later operations must see an earlier ingestion and share one audit chain.

## Run the browser demo

From the directory containing this README:

```bash
python -B -m internal_brain.web_demo demo_bundle.json
```

Open the local URL printed in the terminal. The browser is a real operator surface over the same `InternalBrain` engine used by the CLI: it loads `demo_bundle.json`, executes scoped queries, displays authorization decisions and citations, and reads the engine's audit chain through an audit-capable declared actor.

The page deliberately has no login and no token check. The operator selects one of the declarations already present in the fictional bundle; that selection is not authentication. `/meta` exposes role and clearance declarations without document bodies, `/query` executes the existing authorization-before-retrieval path, and `/audit` returns and verifies the current in-memory audit chain.

### Export a digest-bound AI context packet

The context command runs the same query engine, copies only the already-authorized result evidence into `internal-brain-ai-context/v1`, binds it to the query receipt, and adds explicit downstream constraints. It does not call a model or widen the selected actor's scope.

```bash
python -B -m internal_brain.assistant_context build \
  demo_bundle.json demo_query_finance.json \
  --out finance-context.json
python -B -m internal_brain.assistant_context verify finance-context.json
```

The output is created exclusively. Its `source_result_receipt_sha256` binds the query receipt; `packet_sha256` binds the complete context packet. `NO_AUTHORIZED_MATCH` produces an empty evidence list with `abstain_when_no_authorized_match: true`. Authorized results retain document IDs, snippets, citations, content/document digests and untrusted-instruction markers. The browser `/query` response includes the same verified packet beside the ordinary receipt.

## Run the fictional operator session

`demo_operations.json` supplies eight ordered operations:

| Step | Operation | Intended behavior |
| --- | --- | --- |
| 1 | `maya` queries travel policy. | Return employee-authorized evidence. |
| 2 | `maya` requests `finance-plan` explicitly. | Return `NO_AUTHORIZED_MATCH`; requested IDs cannot grant access. |
| 3 | `li` queries the finance plan. | Return finance-authorized evidence with citations. |
| 4 | `chen` ingests a fictional equipment policy. | Add a new document scoped to `employee` and `security_admin`. |
| 5 | `chen` repeats the same document ID and content with a different source URI. | Record `DOCUMENT_ID_CONFLICT`; retain the original document and provenance. |
| 6 | `maya` queries the new policy. | Retrieve the admitted document with its original source citation. |
| 7 | `maya` attempts another ingestion. | Record `PERMISSION_DENIED`; no document is added. |
| 8 | `maya` queries the equipment policy again. | Continue after the denial and return authorized evidence. |

Choose unused output paths. The session deliberately includes authorization denials, so a completed run has exit status **3**. Capture that status if your shell normally stops on nonzero exits:

```bash
session_rc=0
python -B -m internal_brain session demo_bundle.json demo_operations.json \
  --audit-actor chen \
  --run-out session-run.json \
  --audit-out session-audit.json || session_rc=$?
printf 'Session exit status: %s\n' "$session_rc"
```

Inspect the emitted summary and ordered outcomes before proceeding. Status 3 in this example represents the intentional denials; an input, schema or file error needs correction. The original `demo_bundle.json` stays unchanged. The retained run records the starting normalized bundle, ordered operations and outcomes needed to reproduce the session.

### Verify the audit chain

```bash
python -B -m internal_brain verify-audit session-audit.json
```

This checks event structure, order and digest links. It does not execute the operations or establish that the retained chain is complete. To compare against an independently retained checkpoint, supply `--expected-head-digest HEX` and `--expected-event-count N` with the values retained from the original run. A checkpoint copied from the file currently being checked is not independent evidence.

### Replay the session

```bash
replay_rc=0
python -B -m internal_brain replay session-run.json \
  --audit-actor chen || replay_rc=$?
printf 'Replay exit status: %s\n' "$replay_rc"
```

Replay verifies the retained artifact digest, constructs a fresh engine from the initial normalized bundle, and reexecutes the ordered operations. It compares ordered outcomes, the complete audit chain and head, and the final bundle digest. Inspect `replay_verified` in the summary: a matching replay reports `true`. Reproducing this session also reproduces its intentional denials, so a matching replay still exits **3**.

For a stronger comparison, retain the original artifact digest separately and pass it as `--expected-artifact-sha256 HEX`. Without that independent value, an editor who consistently rewrites the entire artifact and recomputes its digest can produce another internally consistent run. Replay establishes reproducibility from the retained inputs, not who created them, when they were created or whether other operations were omitted.

### Find retained evidence and checkpoint values

The run artifact uses schema `internal-brain-session/v1`. Its fields make the replay inputs and comparisons explicit:

| Field | Retained evidence |
| --- | --- |
| `initial_bundle`, `initial_bundle_sha256` | Starting normalized bundle and its digest. |
| `audit_actor_user_id` | Declared audit reader used for the run. |
| `operations`, `outcomes` | Ordered requests and their `ok`, `denied` or `error` outcomes, each with a receipt or error. |
| `audit.events`, `audit.verification` | Complete retained audit chain and its verification result. |
| `final_bundle_sha256` | Digest of the final normalized bundle. |
| `summary` | Operation totals and resulting process status. |
| `artifact_sha256` | Digest of the complete artifact excluding this digest field. |

The emitted command summary includes `audit_head_digest` and `audit_event_count`. The artifact's `summary` includes `operation_count`, `successful_count`, `denied_count`, `failed_count`, `no_authorized_match_count` and `exit_code`; use the actual values from your run.

Retain `artifact_sha256` separately for `--expected-artifact-sha256`. It hashes canonical JSON with its own field excluded, **not the raw bytes of the formatted JSON file**. A generic file checksum is therefore not the expected value for this option.

## Other operator commands

### Export the audit from a single query

```bash
python -B -m internal_brain query demo_bundle.json demo_query_employee.json \
  --audit-actor chen --audit-out employee-query-audit.json
```

The query still runs as `maya` from the request. `chen` is the separately declared audit reader. Add `--run-out NEW_PATH` to retain a replayable single-query run as well. With `--run-out`, the command emits the operation outcome and artifact summary; without it, the command keeps the original query receipt or error format.

### Ingest one document and retain the updated bundle

For a document file using `internal-brain-document/v1`, the command form is:

```text
python -B -m internal_brain ingest BUNDLE DOCUMENT --tenant northstar --actor chen --audit-actor chen --bundle-out NEW_PATH [--audit-out NEW_PATH] [--run-out NEW_PATH]
```

Replace the uppercase placeholders with local paths; brackets mark optional arguments. The equipment policy in `demo_operations.json` provides a fictional document example. The required `--bundle-out` retains the updated normalized bundle after successful ingestion for later standalone commands. A denied ingestion creates no replacement bundle; requested run and audit outputs can still retain its denial. `--run-out` retains a replayable ingestion run. To try ingestion immediately without preparing another document file, use the session above.

An exact repeat of a normalized document can return `IDEMPOTENT_REPLAY`. Reusing its ID with any different document field returns `DOCUMENT_ID_CONFLICT`; it cannot silently replace content, provenance or access metadata. This ingestion decision is separate from the `replay` command.

### Operations input format

An operations file has schema `internal-brain-operations/v1` and an ordered `operations` list. Each item contains `operation` and `request`. A `query` request uses `internal-brain-query/v1`; an `ingest` request contains `tenant_id`, `actor_user_id` and a document using `internal-brain-document/v1`. See the complete fictional example in [demo_operations.json](demo_operations.json).

## Output and exit behavior

Output files are created exclusively. An existing output, an alias of an input, or colliding output paths are refused. Select fresh names instead of overwriting originals. A final success summary is printed only after the requested writes complete; consult the actual result if any write fails.

Sessions retain per-operation authorization and request-schema failures in order and continue to later operations. An invalid starting bundle, operations envelope or operation kind prevents the session from starting. Per-operation outcomes and tenant audit events are different records: request-schema failures remain outcomes; normalized authorization denials for the engine's own tenant can enter its audit stream; cross-tenant requests do not write to the target tenant's audit.

| Status | Meaning |
| --- | --- |
| `0` | Successful command, or a session/replay whose operations all succeeded. `NO_AUTHORIZED_MATCH` is a completed query and does not itself produce a nonzero status. |
| `3` | Authorization denial. A completed session or verified replay with a denied operation retains this nonzero status. |
| `2` | Schema, malformed-input, audit/replay verification or file failure; per-operation schema/other failures take precedence over authorization denials in a session. |
| `1` | Other engine error outside the session's per-operation failure handling. |

Use the emitted result as well as the process status. Audit-chain verification success alone does not imply successful replay or successful authorization for every operation.

## Security scope and limits

Authorization precedes lexical scoring. Document classification and allowed roles filter the evidence set; `document_ids` only narrows it. A tie between the highest-scoring authorized candidates remains ambiguous even when the requested result limit hides one of them. Role scope and clearance also constrain ingestion.

The local audit chain and replay artifact bind retained evidence through SHA-256 digests. They are not signatures, authenticated timestamps or remote append-only storage. The prototype does not supply identity federation, encrypted persistent tenant storage, concurrent writers, a semantic index or an answer-generation service. [THREAT_MODEL.md](THREAT_MODEL.md) describes these limits in detail.

## Source lineage and challenge status

- Original competition claim and design: **Z-Aster-67** — [original claim](https://tokenjunkielabs.slack.com/archives/C0BVDDS04G2/p1789700015945249).
- Official-source qualification: **Z-Cairn-4R7Q** — [donor research](https://tokenjunkielabs.slack.com/archives/C0BVDDS04G2/p1789700767921429).
- Recovery implementation carrier: **Z-Sol-17** — [recovery claim](https://tokenjunkielabs.slack.com/archives/C0BVDDS04G2/p1789713709603279).
- Recovered implementation: [source at commit `6230a5bc1d4b47c4f6f3922381cd447a45997e31`](https://github.com/woahwhattheheck/commons/tree/6230a5bc1d4b47c4f6f3922381cd447a45997e31/competitions/tencent_aspire_internal_brain).

The [submission packet](SUBMISSION.md) remains a draft. Tencent's [official release](https://en.prnasia.com/releases/apac/tencent-cloud-and-ai-singapore-connect-singapore-s-ai-talent-with-real-world-industry-challenges-548305.shtml) describes a requirement to apply Tencent-provided AI tools. This offline, non-generative prototype does not establish fulfillment of that requirement or overall challenge readiness. It performs no provider call, registration or submission.

### Official event details

- Event: [Tencent Cloud AI CAN DO IT Hackathon Singapore 2026](https://tch.tencentcloud.com/contest/44)
- Team registration: [official registration form](https://qdrl.qq.com/65xN1yft)
- Project submission: [official project-submission form](https://tinyurl.com/TCHackathonSGProjectSubmission)
- Submission deadline shown by the official event page: `2026-10-16 23:59:59`. The event page does not state a timezone for this timestamp.
- Track: **FinTech - The Internal Brain: Building a Context-Aware Enterprise Knowledge System with RBAC, Security Logging & Audit Trail**

### Alignment with the official judging dimensions

| Judging dimension | Current project evidence |
| --- | --- |
| Relevance | Implements context-aware enterprise knowledge access with RBAC decisions, security events and an inspectable audit trail. |
| Human-centric design | Adds a browser workflow for role selection, questions, decisions, evidence, citations and the audit chain. |
| Use of AI | Supplies a governed, authorized-evidence layer that an AI assistant can consume. Actual Tencent CodeBuddy, WorkBuddy or Miora use is recorded separately only after it occurs in the corresponding product account and leaves retained evidence. |
| Technical execution | Provides a runnable Python package, CLI workflows, the real browser surface, strict schemas, replay and digest-bound evidence. |
| Feasibility | Runs locally from a supplied bundle and exposes a boundary for enterprise identity, knowledge and logging integrations. |
| Responsible AI practices | Authorization precedes retrieval; document text remains data; role scope, provenance, denials and audit evidence stay visible. |
| Potential business impact | Reduces time spent finding and reusing internal knowledge while retaining control over access and accountability. |

### Tencent product-use record

Tencent CodeBuddy, WorkBuddy and Miora activity is an account/process fact separate from repository source history. Record a product as used only after work has actually been performed in that product. Retain the product name, date, account or workspace, task performed and resulting output or provider reference.
