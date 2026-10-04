# Indiana IOT RFP 27-87814 - Enterprise Observability Platform

Revenue pursuit carrier for Commons issue #15651.

## Current posture

`HOLD / PARTNER-FIRST RESEARCH / NO OUTBOUND`.

The live Indiana IDOA notice identifies RFP 27-87814 / event 000670000087814, due October 28, 2026 at 3:00 PM ET, and says IOT seeks an Enterprise Observability Platform that preserves coverage, scales toward 500 monitored applications, and improves detection, resolution, and alert-quality outcomes.

The [official State ZIP](https://secure.in.gov/idoa/proc/solicitations/files/000670000087814.zip) was acquired on October 3 and is retained exactly at `retained/000670000087814.zip`: 967,929 bytes, SHA-256 `cf0ef21dbf8f9bc59cc54220fe9155a705ad98c1a5e8a312921cf138dfc9e55e`. It contains the 23-page main RFP and 15 attachments. The main RFP was read during source recovery. All 15 attachments have now received a retained text, table and package-structure review; [ATTACHMENT_REVIEW.md](ATTACHMENT_REVIEW.md) binds the requirements, workbook cells and remaining questions. Word/Excel rendering and Supplier Portal comparison remain unfinished.

`source_ledger.json` records the published schedule and source anchors. The September 17 mirror remains dated `DISCOVERY_ONLY`; its 9:30 conference time is the general session. The main RFP distinguishes the 10:40 individual session (1.23, pp.14-15).

Only package acquisition, published submission instructions and the schedule are `PROVEN`. No owner platform, staffing, security, completed proposal, contract or accepted workshare evidence has been added. `HOLD` remains the actual decision.

## Retained-evidence trust root

`source_ledger.json` and `requirements.json` are caller/input packets. Their `retained`, `PROVEN`, digest, path, and evidence-id fields are assertions only and can never authenticate themselves.

Positive qualification is possible only when all of these agree:

1. the source-literal SHA-256 pin for `authority_manifest.json`;
2. the exact authority-manifest opportunity/event/generation identity;
3. exact retained source bytes read through descriptor-anchored, no-follow traversal;
4. each retained file's SHA-256;
5. a closed retained-source inventory matching the source ledger;
6. exact evidence bindings to source, requirement, subject, scope, and generation.

The committed authority manifest binds generation `OFFICIAL_ZIP_20261003` to the retained ZIP and three source-information evidence records. It contains no owner qualification evidence. Its raw-byte SHA-256 is:

`6abde186bedd29e009d2701121d75db97be0dbff4ca25608c0c266510175c059`

Changing the manifest, a retained source, or an evidence binding without also publishing a new reviewed source generation fails closed.

## Commercial lane

Current evidence does not support a solo-platform prime posture. The near-term commercial hypothesis is a paid specialist workshare with a qualified platform vendor or integrator: telemetry inventory/migration, deterministic SLO acceptance, synthetic incident/regression packs, ServiceNow integration evidence, rollout scorecards, and AI/agent observability evaluation if allowed.

`partner_targets.json` contains research targets only. It is not an endorsement, selection, representation, or authorization to contact them.

## Current vs historical evaluation

The default CLI uses a process-owned UTC clock. A caller cannot supply the clock for a current readiness decision:

```bash
python -m opportunities.indiana_iot_observability_27_87814.gate \
  --ledger opportunities/indiana_iot_observability_27_87814/source_ledger.json \
  --requirements opportunities/indiana_iot_observability_27_87814/requirements.json \
  --partners opportunities/indiana_iot_observability_27_87814/partner_targets.json \
  --scope opportunities/indiana_iot_observability_27_87814/paid_specialist_scope.json
```

For deterministic archaeology only, `--historical-now 2026-09-17T19:20:00Z` performs a historical replay. Historical replay is deliberately incapable of emitting `PRIME_REVIEW_READY` or `TEAMING_REVIEW_READY`.

Expected current decision with the retained package: `HOLD`, `package_retained=true`, with every external-authority bit false. Open term/security/pricing work orders survive package acquisition and source review. The attachment review identifies the published obligations; selected deployment terms, respondent compliance, completed pricing and accepted partner commitments remain unresolved.

## Next source and owner work

The main RFP sets questions and optional Attachment I for October 7, 3 PM ET; answers/amendments target October 16; proposals and reference checks are due October 28, 3 PM ET (1.23). Recheck the official source before relying on a later generation. Required response items include the AI questions and infrastructure overview (3.2). The completed [attachment review](ATTACHMENT_REVIEW.md) records all 15 retained attachments, the separate product/developer AI disclosures, subcontract obligations and draft owner questions about hosting, sizing, target-scale costs, authorization timing and turnover. No answer, qualification, price or commitment has been supplied on the respondent's behalf. Original pursuit and partner ownership remains Z-KestrelForge-1448, with the existing #15724 source-root repair lineage.

## Single-writer outbound rule

No buyer/vendor/partner email or other external contact is authorized by this carrier. Before any later touch: fresh all-access Slack census, fresh Gmail all-history census, exact Muse arbitration for the recipient/purpose key, and the repository's then-current outbound collision/relationship guards. Re-census immediately before any owner-authorized send.

This package itself grants no Muse, provider, submission, payment, cash, accounting, or revenue authority.
