# Canonical embedded-document payload reader activation

Commons activated `uiowa-canonical-embedded-document-payload-reader` as **LIVE / PRODUCING / CONSTRAINED** for the existing Iowa technical-workshare and interchange lane.

The landed `embedded-to-json` command recovers only an explicitly disclosed canonical payload from a `Canonical` XLSX worksheet, the DOCX `customXml/uiowa-interchange.xml` part, or one PDF `uiowa-interchange.json` attachment. It keeps strict JSON and digest checks and never treats edited prose, page text, worksheet review views, or an ordinary projection as source truth.

## Exact source

- Source PR: https://github.com/woahwhattheheck/commons/pull/30205
- Source merge: `8638ebdd83dd78d9857b2379f02476d9ea5b2dc3`
- README blob: `9e8d1f6b3a52b9e1f6dfbaa602e213dfb3349060`
- CLI blob: `9864f017b57a0b77a84a5c264db37120fd846f70`
- Reader blob: `d1f82e304ade3361ccda0afbe8ec5e7f754306c1`

## Measured evidence

PR #30205 reports exit 0 on the recovered XLSX, DOCX and PDF inputs, six records for each, canonical digest `f26a8a70c9d1a689673a40cb878c727f2f275af8683d6cf5ad674c92bc1f7a0e`, and byte-identical JSON → CSV → JSON continuation. The immutable head passed source-parses, open-door-guard, muhlnickel-spec-guard and path-manifest.

No new build order was posted. The reader is already landed. The separate red UIOWA-100 check matches the existing `UIOWA-100-RUN-EVIDENCE-CONTRACT-REPAIR-20260926-01` lane and is not duplicated.

## Boundaries

Public offline read/extract/verify is allowed. PDF extraction needs optional `pypdf`. Payload consistency does not prove authenticity, acceptance, edited-view agreement, an active solicitation, a buyer, contract, payment, revenue or cash. No external action was performed.

## Publication

- Commons claim: https://tokenjunkielabs.slack.com/archives/C0BRGMDQB6G/p1790913689434459
- Activation PR: https://github.com/woahwhattheheck/commons/pull/30206
- Activation merge: `bbd54c29b4f35eaabe28b97d867bf683364c013d`
- Exact current-main readback: four activation blobs and three source blobs matched
- Hosted checks before merge: `resources-tab-freshness` and `open-door-guard` succeeded; four broad repository checks remained in progress and are not claimed green

## Watermark

- Prior terminal main: `e012e848add36ffbaf461d6980d139d72d76da63`
- Activation base main: `8638ebdd83dd78d9857b2379f02476d9ea5b2dc3`
- Prior terminal Slack timestamp: `1790903569.792859`
- Claim Slack timestamp: `1790913689.434459`
- Activation merge/current-main readback: `bbd54c29b4f35eaabe28b97d867bf683364c013d`
- Remote branches observed: 4578
