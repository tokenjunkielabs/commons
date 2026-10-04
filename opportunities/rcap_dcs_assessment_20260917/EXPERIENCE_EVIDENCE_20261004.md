# RCAP: transferable project evidence

**Operation:** `RCAP-EXPERIENCE-EVIDENCE-QUARTZ`  
**Observed:** 4 October 2026  
**Use:** internal completion material for the existing `PROPOSAL_SOURCE_20261003.md`, not a new proposal or an attachment ready for the buyer.

## What this completes

The packet already has its scope, commercial offer and proposed lead. This appendix supplies two concrete, source-backed project descriptions that the submission writer can consider for the missing experience section. These are transferable laboratory/software examples, not nonprofit DCS/CRM consulting references or proof of a prior paid client engagement.

The existing proposal remains an internal, unsubmitted candidate. Its $24,500 fixed base, $7,500 excluded option and four-week proposed delivery are unchanged. The packet retains RCAP's literal deadline wording, **4 October 2026, 11:59 PM EST**. No new time-zone interpretation or deadline extension is asserted here.

Do not publish this appendix to the buyer. Its repository links are internal evidence for the writer; the October 3 customer candidate and PDF remain unchanged and contain no Commons/GitHub/Slack links. A fact supported by an artifact is not automatically proof of Bryce's personal role, permission to cite a third party, completed bidder qualification or sponsor acceptance.

## Example 1 — Offline data-access planning and reproducible reporting

**Project:** Whitebox Estimation, an internally developed planning and reporting tool.

**Implemented scope.** The project accepts a frozen source index and an explicit read plan, validates sources and byte ranges, and produces deterministic JSON and self-contained HTML reports. It distinguishes logical reads, exact-cache reads and coalesced access plans, retaining input hashes and stated assumptions. A separate delivery boundary is documented; the estimator itself does not fetch model data or execute inference.

**Relevant work demonstrated.** Translating technical inputs into an inspectable decision artifact; comparing alternative access plans; preserving data lineage; exposing assumptions; and validating a change against unchanged report outputs. Those are transferable to RCAP's current-state evidence pack and option analysis, without implying familiarity with RCAP's DCS or Unanet environment.

**Bounded result.** The retained repository example distinguishes seven logical ranges, six exact-cache keys and three coalesced ranges. Merged PR #140 changes the range representation to avoid retaining two dictionary collections. The repository's independent October 4 replay reports peak traced Python allocation falling from 46,644,726 to 33,224,941 bytes on its generated 100,000-row workload, while JSON and HTML remained byte-identical. That independent replay did not demonstrate an end-to-end CLI speedup. These are laboratory report-generation measurements, not customer, network, inference, process-RSS or financial outcomes.

**Evidence checked.**

- Repository README observed at blob `cf3cef12e7663427bb3800517d682223207c1921`: <https://github.com/woahwhattheheck/whitebox-estimation/blob/main/README.md>.
- Merged change: <https://github.com/woahwhattheheck/whitebox-estimation/pull/140>; merge commit `08519a4e03dba6db32de150d1ae97a441214d126`.
- Retained replay location named in the README: `benchmarks/measurements/exact-range-tuples-20261004.json.gz`. The replay values above are attributed to the repository record; this appendix did not rerun that benchmark.

**Candidate wording for an experience section, after role and disclosure facts are settled:**

> A transferable lab project developed a reproducible planning and reporting workflow for structured technical data. Frozen inputs, explicit assumptions and deterministic JSON/HTML outputs supported comparison of logical, cached and consolidated access plans. This is an example of the evidence handling and transparent option comparison proposed for RCAP, not a claim of prior work on RCAP's DCS or Unanet.

## Example 2 — Metrics integration, failure handling and source-bound verification

**Project:** Chronicle Kubernetes sidecar example contribution, maintained on the existing upstream PR #105.

**Implemented scope.** The contribution includes an example application metrics endpoint, sidecar configuration, deployment materials and pod metadata handling. The current follow-through includes a synchronous health-listener bind so startup can report an occupied port instead of silently presenting success, and maintained coverage of failure, retry and shutdown. A separate small optimization reuses the unchanged compiled label expression across samples.

**Relevant work demonstrated.** Tracing an operational failure to its entry point; distinguishing an accepted startup request from a working service; checking shutdown and recovery; linking a result to the exact source tested; and measuring a resource change without treating a microbenchmark as end-to-end system performance. These are transferable to technical evidence review and supportability/resiliency analysis.

**Bounded results directly executed on 4 October.** The complete production `k8s_sidecar.go` was transferred and verified by its Git blob. Two maintained listener tests passed under Go 1.23.2's race detector with actual TCP listeners and HTTP responses. The occupied-port case failed on the preceding implementation. The tests cover the network error cause, running-state rollback, absence of failed-start workers, retry, both health routes, listener release, duplicate Start and repeated Stop.

The unchanged label grammar was then compiled once rather than per sample. On three representative two-label inputs, three 200 ms benchmark samples showed allocations falling from 33 to 7 per parse and approximately 3,649 to 769 bytes per parse. Median method time changed from 3,235 to 843.4 ns, approximately 3.8 times faster for that method only. Seven label-input checks, eight concurrent readers and the maintained startup tests passed under the race detector.

The isolated harness compiled the entire production file with fail-fast DB/Point collaborators for uncalled storage paths. It did **not** establish full-package, database, image, cluster, live customer or end-to-end collector acceptance. The upstream contribution remains open, so this is published implementation and bounded verification, not maintainer adoption or a completed paid engagement.

**Evidence checked.**

- Original upstream contribution: <https://github.com/josedab/chronicle/pull/105>.
- Maintained startup tests: commit `5c42a04cf8c539f5465a6d3cc7157b2279df8687`, test blob `1f8042fcbef2151e58dee4020567f6d3c63fc014`: <https://github.com/woahwhattheheck/chronicle/commit/5c42a04cf8c539f5465a6d3cc7157b2279df8687>.
- Label-expression reuse and measured scope: commit `fa7800904fcfa45f1da08ffcf30dbb5933088628`, source blob `95f3619f1b9d11b7cfbc78437d24c18d6278e29b`: <https://github.com/woahwhattheheck/chronicle/commit/fa7800904fcfa45f1da08ffcf30dbb5933088628>.
- Pre-fix and health-fixed source blobs: `18d597ddc1f769ee71d5237d923f927edc4c0ab2` and `a2aeeb25388c7552d7310016eca5ed7a015a3ee9`.

**Candidate wording for an experience section, after role and disclosure facts are settled:**

> A software integration contribution paired a metrics sidecar example with explicit startup-error handling and reproducible recovery checks. Source-bound testing distinguished a real listener failure from reported success and verified retry and shutdown behavior. This illustrates a practical approach to evaluating operational dependencies and the strength of supporting evidence; it is not a prior nonprofit systems-assessment reference.

## Personal biography and qualification boundary

The existing proposal identifies Bryce Xavier Muhlnickel as the proposed project lead and describes an owner-led delivery model. The project records above establish artifacts and technical outcomes, not the extent of Bryce's personal authorship, prior employment, years of experience, consulting responsibilities, client results or authority to use a client as a reference.

Before any buyer-facing experience statement is finalized, its description of the lead's actual role must be accurate and authorized for disclosure. The defensible distinction is between directing or coordinating a delivery and personally implementing every component. Do not manufacture an employment history, reference, client endorsement, nonprofit CRM engagement or individual certification from repository ownership or contributor activity.

Current business, tax, privacy and security compliance assertions remain outside the evidence established by these projects. They do not prove tax standing, current insurance, an independent security certification, eligibility or statutory compliance. Preserve the packet's existing insurance timing and confidentiality/data-handling terms. No unrestricted client-data upload, production access or new subcontractor arrangement is authorized by this appendix.

## Handoff to the existing submission writer

Use these descriptions to avoid rebuilding the proposal or searching generically for examples. Select only material that can be tied to the lead's accurate role and disclosed truthfully. Keep the source links and detailed laboratory limits in internal supporting records; distill relevant, substantiated statements into the established candidate only when its remaining facts are available.

Refresh the exact recipient history and current Slack ownership before any eventual submission. This operation sends no buyer email, makes no new offer, changes no commercial term and records no submission, acceptance, award or payment.
