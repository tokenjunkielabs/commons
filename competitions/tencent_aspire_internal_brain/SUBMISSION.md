# Aspire submission packet — draft, not submitted

## Intended challenge and present status

The intended track is Aspire's enterprise knowledge challenge within the Tencent Cloud Singapore 2026 hackathon: context-aware retrieval with role-based access control, security logging and an audit trail. See the [official event page](https://tch.tencentcloud.com/contest/44) and Tencent's [September 17 release](https://en.prnasia.com/releases/apac/tencent-cloud-and-ai-singapore-connect-singapore-s-ai-talent-with-real-world-industry-challenges-548305.shtml).

The release says participants must apply Tencent-provided AI tools. The current artifact is an offline, deterministic, non-generative Python prototype; it does not establish that tool requirement, accepted registration, eligibility, cloud deployment or overall challenge readiness. No provider integration or account action is performed by this build. This packet remains a draft for the project owner.

## What the prototype contributes

The operator can run scoped queries, ingest a document, retain an ordered session and reproduce that session from its original normalized bundle. Query citations include source URIs, `content_sha256` for content bytes and `document_sha256` for the whole normalized record, including provenance and access metadata. Successful ingestion audit payloads bind the full document record. Authorization runs before retrieval. A requested document ID cannot widen an actor's access, and document text cannot change policy.

The retained audit chain captures supported decisions in order. The replay command goes further: it executes the retained operations again and compares their outcomes, audit evidence and final bundle digest. A separately retained artifact digest or audit checkpoint provides a comparison with an earlier receipt; local digests alone do not authenticate its author or establish completeness.

## Demonstration walkthrough

Run from the directory containing this file with Python 3.11 or later. Use only the supplied fictional data. [README.md](README.md) explains the command and exit behavior in full.

1. Run `python -B -m internal_brain validate demo_bundle.json`. Show that the trusted operator sees the entire bundle, including policy and document contents. Explain that `maya`, `li` and `chen` are declared local identities rather than authenticated sessions.
2. Run the ordered fictional session below. Inspect the employee travel result and its source citations. The vendor note contains hostile instruction language that remains untrusted document content.
3. Show the employee's explicit `finance-plan` request returning `NO_AUTHORIZED_MATCH`. Show the finance actor's subsequent authorized retrieval. Explain that document exclusion is a completed query, whereas a permission denial is a failed operation.
4. Show `chen` ingesting the fictional equipment policy, followed by `DOCUMENT_ID_CONFLICT` when the same actor attempts to change only its source URI under the same ID. Show `maya` retrieving the admitted document with its original provenance.
5. Show the denied ingestion by `maya` and the successful query after it. Explain why the run records successful and denied outcomes and exits 3.
6. Verify the exported audit chain, then replay the retained session. Show the replay summary and its operation outcomes. Matching the expected denials still produces exit 3; successful replay is reported explicitly in the summary.

```bash
session_rc=0
python -B -m internal_brain session demo_bundle.json demo_operations.json \
  --audit-actor chen \
  --run-out submission-session.json \
  --audit-out submission-audit.json || session_rc=$?
printf 'Session exit status: %s\n' "$session_rc"
```

After inspecting the completed session summary, run:

```bash
python -B -m internal_brain verify-audit submission-audit.json

replay_rc=0
python -B -m internal_brain replay submission-session.json \
  --audit-actor chen || replay_rc=$?
printf 'Replay exit status: %s\n' "$replay_rc"
```

Use unused output names on a later demonstration; existing files and input aliases are refused. Retain the run's `artifact_sha256` separately if an independent replay comparison is needed, and provide it through `--expected-artifact-sha256 HEX`. This digest covers canonical JSON excluding its own field; it is not a checksum of the formatted file bytes. Optional `verify-audit` checkpoints are `--expected-head-digest HEX` and `--expected-event-count N`, using the original summary's `audit_head_digest` and `audit_event_count`. Record values from the actual run rather than copying an illustrative digest or count.

## Materials to retain for owner review

- The exact source commit and the source lineage in [README.md](README.md).
- `demo_bundle.json`, the two existing role-specific query files and `demo_operations.json`.
- The actual session summary, retained run, audit export and replay summary from the demonstrated commit.
- Any independently retained artifact digest or audit checkpoint, with its retention context.
- [THREAT_MODEL.md](THREAT_MODEL.md), including the local identity and full-bundle access limits.

This document is a walkthrough, not an execution receipt. Attach actual command results before claiming that a particular source revision was demonstrated. Retained artifacts contain the full fictional starting bundle and operation inputs; they are suitable for this fictional demonstration, not a template for publishing customer data.

## Architecture and deployment boundary

The local flow is strict JSON loading, declared tenant and actor resolution, authorization, deterministic operation execution, cited results, retained audit evidence and replay. A future answer-generation component would consume only the already-authorized evidence. It must not decide or override access policy.

The current filesystem operator is trusted with the complete tenant bundle and can select any declared actor. The prototype provides no authentication service, encrypted persistent storage, remote append-only audit anchor, shared service concurrency or Tencent integration. Deployment and any challenge-required tool use remain separate work requiring their own implementation and evidence.

## Credits and external actions

Original claim and design credit remains **Z-Aster-67**; official-source qualification credit remains **Z-Cairn-4R7Q**; recovery implementation credit remains **Z-Sol-17**. Their original records and the recovered source commit are linked in [README.md](README.md).

This packet records no competition registration, final submission, customer-data upload, prize acceptance or revenue. Those statuses must be established by the project owner through the official process.
